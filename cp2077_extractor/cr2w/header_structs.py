#!/usr/bin/env python3
#
#  header_structs.py
"""
Classes to represent header data in CR2W/W2RC files.
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
from typing import NamedTuple, Protocol

__all__ = [
		"CR2WBufferInfo",
		"CR2WEmbeddedInfo",
		"CR2WExportInfo",
		"CR2WFileHeader",
		"CR2WFileInfo",
		"CR2WImport",
		"CR2WImportInfo",
		"CR2WNameInfo",
		"CR2WPropertyInfo",
		"CR2WTable",
		"Struct"
		]


class Struct(Protocol):
	"""
	:class:`~typing.Protocol` for a :class:`~typing.NamedTuple` representing structured binary data in a file.
	"""

	#: The format for :func:`struct.unpack`.
	_struct_format: str

	#: The size of the struct, in bytes.
	_size: int


class CR2WTable(NamedTuple):
	offset: int
	item_count: int
	crc32: int

	_struct_format = "<III"  # type: ignore[misc]
	_size = 12  # type: ignore[misc]


class CR2WNameInfo(NamedTuple):
	offset: int
	hash: int

	_struct_format = "<II"  # type: ignore[misc]
	_size = 8  # type: ignore[misc]


class CR2WImportInfo(NamedTuple):
	offset: int
	class_name: int  # ushort (H, 2 bytes)
	flags: int  # ushort (H, 2 bytes)

	_struct_format = "<IHH"  # type: ignore[misc]
	_size = 8  # type: ignore[misc]


class CR2WPropertyInfo(NamedTuple):
	class_name: int  # ushort (H, 2 bytes)
	class_flags: int  # ushort (H, 2 bytes)
	property_name: int  # ushort (H, 2 bytes)
	property_flags: int  # ushort (H, 2 bytes)
	hash: int  # ulong (C# version Q, 8 bytes)

	_struct_format = "<HHHHQ"  # type: ignore[misc]
	_size = 16  # type: ignore[misc]


class CR2WExportInfo(NamedTuple):
	class_name: int  # ushort (H, 2 bytes)  # needs to be registered upon new creation and updated on file write!
	object_flags: int  # ushort (H, 2 bytes)  #  0 means uncooked, 8192 is cooked
	parent_id: int
	data_size: int  # created upon data write
	data_offset: int  # created upon data write
	template: int  # can be 0
	crc32: int  # created upon write

	_struct_format = "<HHIIIII"  # type: ignore[misc]
	_size = 24  # type: ignore[misc]


class CR2WBufferInfo(NamedTuple):
	flags: int
	index: int  # type: ignore[assignment]  # TODO (make into class with tuple interface (dataclass/attrs))

	#: offset inside a cr2w file, buffers are compressed and appended to a cr2w file
	offset: int

	#: This is the compressed size of the buffer; it's called disksize because buffers are compressed and appended to a cr2w file
	disk_size: int

	#: This is the uncompressed size of the buffer; it's called memSize because buffers are uncompressed at runtime in the game
	mem_size: int

	#: crc32 over the compressed buffer
	crc32: int

	_struct_format = "<IIIIII"  # type: ignore[misc]
	_size = 24  # type: ignore[misc]


class CR2WEmbeddedInfo(NamedTuple):
	import_index: int
	chunk_index: int
	path_hash: int  # ulong (C# version Q, 8 bytes)

	_struct_format = "<IIQ"  # type: ignore[misc]
	_size = 16  # type: ignore[misc]


class CR2WImport(NamedTuple):
	depot_path: bytes
	class_name: bytes
	flags: int


class CR2WFileHeader(NamedTuple):
	version: int
	flags: int
	time_stamp: int  # ulong (C# version Q, 8 bytes)
	build_version: int
	objects_end: int
	buffers_end: int
	crc32: int
	num_chunks: int

	_struct_format = "<IIQIIIII"  # type: ignore[misc]
	_size = 36  # type: ignore[misc]


class CR2WFileInfo(NamedTuple):
	file_header: CR2WFileHeader
	string_dict: dict[int, bytes]
	name_info: list[CR2WNameInfo]
	import_info: list[CR2WImportInfo]
	property_info: list[CR2WPropertyInfo]
	export_info: list[CR2WExportInfo]
	buffer_info: list[CR2WBufferInfo]
	embedded_info: list[CR2WEmbeddedInfo]

	imports: list[CR2WImport]

	def get_imports(self) -> list[bytes]:  # list[ResourcePath]

		result: list[bytes] = []  # list[ResourcePath]
		for import_info in self.import_info:
			# result.append((ResourcePath)StringDict[importInfo.offset]);
			result.append(self.string_dict[import_info.offset])

		return result
