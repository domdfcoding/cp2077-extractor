#!/usr/bin/env python3
#
#  io.py
"""
File IO operations.
"""
#
#  Copyright © 2025 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import binascii
import inspect
import struct
import warnings
from collections.abc import Iterator
from typing import IO, Any, NamedTuple, TypeVar

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from cp2077_extractor.cr2w.datatypes import Chunk, lookup_type
from cp2077_extractor.cr2w.utils import get_names_list
from cp2077_extractor.utils import decompress

# this package
from .header_structs import (
		CR2WBufferInfo,
		CR2WEmbeddedInfo,
		CR2WExportInfo,
		CR2WFile,
		CR2WFileHeader,
		CR2WFileInfo,
		CR2WImport,
		CR2WImportInfo,
		CR2WMetadata,
		CR2WNameInfo,
		CR2WProperty,
		CR2WPropertyInfo,
		CR2WTable,
		Struct
		)

__all__ = [
		"CNameError",
		"ParsingData",
		"parse_cr2w_buffer",
		"parse_cr2w_file",
		"read_buffer",
		"read_c_name",
		"read_chunk",
		"read_file_info",
		"read_struct",
		"read_tables",
		]

_S = TypeVar("_S", bound=Struct)


def read_tables(fp: IO, table_struct: type[_S], header: CR2WTable) -> Iterator[_S]:
	"""
	Read a tables of the given type in from the opened file.

	:param fp:
	:param table_struct:
	:param header:

	:returns: An iterator over instances of ``table_struct``.
	"""

	table_bytes = fp.read(table_struct._size * header.item_count)
	crc32 = binascii.crc32(table_bytes)
	assert crc32 == header.crc32, (crc32, header.crc32)
	for idx in range(header.item_count):
		chunk = table_bytes[0 + (idx * table_struct._size):table_struct._size + (idx * table_struct._size)]
		yield table_struct(*struct.unpack(table_struct._struct_format, chunk))


class CNameError(Exception):
	"""
	Error raised when an invalid name is read.
	"""


def read_c_name(fp: IO, names_list: list[bytes]) -> bytes:
	"""
	Read a name from the open file.

	Reads the ordinal of the name, and looks up the name string in ``names_list``.

	:param fp:
	:param names_list: Ordered list of names used in the file, for lookups.
	"""

	string_index = struct.unpack("<H", fp.read(2))[0]
	assert string_index < len(names_list)
	c_name = names_list[string_index]
	assert c_name
	if c_name == b"None":
		raise CNameError()
	return c_name


def read_struct(fp: IO, struct_type: type[_S]) -> _S:
	"""
	Read the given struct from the open file.

	:param fp:
	:param struct_type:
	"""

	return struct_type(*struct.unpack(struct_type._struct_format, fp.read(struct_type._size)))


def read_file_info(fp: IO) -> CR2WFileInfo:
	"""
	Read the file header and metadata.

	:param fp:
	"""

	magic = fp.read(4)
	assert magic == b"CR2W"

	# File Header
	file_header = read_struct(fp, CR2WFileHeader)  # type: ignore[type-var]

	if file_header.version > 195 or file_header.version < 163:
		raise ValueError("Unsupported Version")

	# Tables [7-9] are not used in cr2w so far.
	table_headers = [read_struct(fp, CR2WTable) for _ in range(10)]  # type: ignore[type-var]

	# Read strings - block 1 (index 0)
	assert fp.tell() == table_headers[0].offset, (fp.tell(), table_headers[0].offset)

	string_dict: dict[int, bytes] = {}
	while fp.tell() < (table_headers[0].offset + table_headers[0].item_count):
		pos = fp.tell() - table_headers[0].offset
		string = b''
		while True:
			char = fp.read(1)
			if char == b"\0":
				break
			string += (char)
		if not string:
			string = b"None"
		string_dict[pos] = string

	# Read the other tables
	name_info: list[CR2WNameInfo] = list(read_tables(fp, CR2WNameInfo, table_headers[1]))  # type: ignore[type-var]
	import_info: list[CR2WImportInfo] = list(
			read_tables(fp, CR2WImportInfo, table_headers[2])  # type: ignore[type-var]
			)
	property_info: list[CR2WPropertyInfo] = list(
			read_tables(fp, CR2WPropertyInfo, table_headers[3])  # type: ignore[type-var]
			)
	export_info: list[CR2WExportInfo] = list(
			read_tables(fp, CR2WExportInfo, table_headers[4])  # type: ignore[type-var]
			)
	buffer_info: list[CR2WBufferInfo] = list(
			read_tables(fp, CR2WBufferInfo, table_headers[5])  # type: ignore[type-var]
			)
	embedded_info: list[CR2WEmbeddedInfo] = list(
			read_tables(fp, CR2WEmbeddedInfo, table_headers[6])  # type: ignore[type-var]
			)

	_names_list: list[bytes] = []
	for a_name_info in name_info:
		assert a_name_info.offset in string_dict
		_names_list.append(string_dict[a_name_info.offset])

	_imports_list = []
	for an_import_info in import_info:
		assert an_import_info.offset in string_dict
		ret = CR2WImport(
				class_name=_names_list[an_import_info.class_name],
				depot_path=b'',  # TODO:  = depot_path or '',
				flags=an_import_info.flags,
				)
		_imports_list.append(ret)

	return CR2WFileInfo(
			file_header=file_header,
			string_dict=string_dict,
			name_info=name_info,
			import_info=import_info,
			property_info=property_info,
			export_info=export_info,
			buffer_info=buffer_info,
			embedded_info=embedded_info,
			imports=_imports_list,
			)


def read_chunk(fp: IO, chunk_index: int, file_info: CR2WFileInfo) -> tuple[bytes, bytes]:
	"""
	Read an export chunk from the file.

	:param fp:
	:param chunk_index:
	:param file_info:

	:returns: A tuple of the raw chunk data and the chunk's datatype.
	"""

	names_list = get_names_list(file_info)

	info = file_info.export_info[chunk_index]
	red_type_name = names_list[info.class_name]

	assert fp.tell() == info.data_offset
	data = fp.read(info.data_size)

	if (fp.tell() - info.data_offset != info.data_size):
		warnings.warn("Chunk size mismatch! Could lead to problems")
		fp.seek(info.data_offset + info.data_size)

	return data, red_type_name


def read_buffer(fp: IO, info: CR2WBufferInfo) -> bytes:
	"""
	Read a buffer from the CR2W/W2RC file.

	:param fp:
	:param info: Metadata about the buffer
	"""

	assert fp.tell() == info.offset

	# buffer = fp.read(info.disk_size)
	buffer = fp.read(info.mem_size)

	if buffer[:4] == b"KARK":
		# Compressed with oodle
		decompressed_size = int.from_bytes(buffer[4:8], "little")
		buffer = decompress(buffer[8:], decompressed_size)

	# TODO: check crc32 (figure out what the input data is)
	# crc32 = binascii.crc32(buffer)
	# assert crc32 == info.crc32, (crc32, info.crc32)

	return buffer


class ParsingData(NamedTuple):
	"""
	Working data for parsing CR2W/W2RC files.
	"""

	#: Name lookup table for the file.
	names_list: list[bytes]

	#: List of tuples of the raw chunk data and the chunk's datatype
	chunks: list[tuple[bytes, bytes]]

	#: List of tuples of the raw buffer data and the buffer metadata
	buffers: list[tuple[bytes, CR2WBufferInfo]]


def parse_cr2w_file(filename: PathLike) -> CR2WFile:
	"""
	Parse a CR2W/W2RC file from the given path.

	:param filename:
	"""

	filename_p = PathPlus(filename)
	with filename_p.open("rb") as fp:
		return parse_cr2w_buffer(fp, filename_p)


def parse_cr2w_buffer(fp: IO, filename: PathLike | None = None) -> CR2WFile:
	"""
	Parse a CR2W/W2RC file from an opened file.

	:param fp:
	:param filename: Optionally, the path of the opened file for inclusion in metadata.
	"""

	info = read_file_info(fp)
	assert info.string_dict, "Malformed file"

	# # TODO:
	hash_version = None
	# # use 1st string as field 0 is always empty
	# hash_version = identify_hash(info.string_dict[1], info.name_info[1].hash)
	# if (hash_version == HashVersion.Unknown):
	# 	raise ValueError("Failed to identify hash version")

	properties: list[CR2WProperty] = []
	for property_info in info.property_info:
		# TODO: properties.append(read_property(property_info))
		properties.append(CR2WProperty())

	if not properties:
		raise ValueError("Found unsupported PropertyInfo")

	# TODO: ensure CHandle/CWeakHandle can be resolved

	chunks: list[tuple[bytes, bytes]] = []

	for i in range(len(info.export_info)):
		chunks.append(read_chunk(fp, i, info))

	buffer_data: list[tuple[bytes, CR2WBufferInfo]] = []

	for buffer_info in info.buffer_info:
		buffer_data.append((read_buffer(fp, buffer_info), buffer_info))

	parsing_data = ParsingData(get_names_list(info), chunks, buffer_data)

	root_chunk_type = chunks[0][1]
	var_type = lookup_type(root_chunk_type)
	assert inspect.isclass(var_type)
	assert issubclass(var_type, Chunk)
	root_chunk = var_type.from_chunk(chunks[0][0], parsing_data)

	# TODO: read embedded files
	embedded_files: list[Any] = []  # TODO: value type
	# for embedded_info in info.embedded_info:
	# 	embedded_files.Add(read_embedded(embedded_info))

	# TODO: check fp.tell() against header field giving file length (if there is one)
	rem = fp.read(999999)
	if len(rem) != 0:
		warnings.warn(f"{len(rem)} bytes remaining in file!")

	if filename:
		meta_filename = PathPlus(filename).abspath().as_posix()
	else:
		meta_filename = None

	metadata = CR2WMetadata(
			file_name=meta_filename,
			version=info.file_header.version,
			build_version=info.file_header.build_version,
			objects_end=info.file_header.objects_end,
			hash_version=hash_version,
			)

	return CR2WFile(
			info=info,
			metadata=metadata,
			properties=properties,
			root_chunk=root_chunk,
			embedded_files=embedded_files,
			)
