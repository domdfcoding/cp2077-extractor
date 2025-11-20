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
import struct
import warnings
from collections.abc import Iterator
from typing import IO, TypeVar

# this package
from cp2077_extractor.cr2w import get_names_list

# this package
from .header_structs import (
		CR2WBufferInfo,
		CR2WEmbeddedInfo,
		CR2WExportInfo,
		CR2WFileHeader,
		CR2WFileInfo,
		CR2WImport,
		CR2WImportInfo,
		CR2WNameInfo,
		CR2WPropertyInfo,
		CR2WTable,
		Struct
		)

__all__ = ["read_c_name", "read_chunk", "read_file_info", "read_struct", "read_tables"]

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
	assert c_name != b"None"
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

	_names_list = get_names_list(file_info)

	info = file_info.export_info[chunk_index]
	red_type_name = _names_list[info.class_name]

	assert fp.tell() == info.data_offset
	data = fp.read(info.data_size)

	if (fp.tell() - info.data_offset != info.data_size):
		warnings.warn("Chunk size mismatch! Could lead to problems")
		fp.seek(info.data_offset + info.data_size)

	return data, red_type_name
