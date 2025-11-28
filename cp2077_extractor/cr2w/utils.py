#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
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
import struct
from io import BytesIO
from typing import Any

# this package
from cp2077_extractor.cr2w.header_structs import CR2WFileInfo

__all__ = ["get_array_variables", "get_chunk_variables", "get_names_list"]


def get_names_list(file_info: CR2WFileInfo) -> list[bytes]:
	"""
	Returns the name lookup table for the file.

	:param file_info:
	"""

	_names_list: list[bytes] = []
	for a_name_info in file_info.name_info:
		assert a_name_info.offset in file_info.string_dict
		_names_list.append(file_info.string_dict[a_name_info.offset])

	return _names_list


def get_chunk_variables(chunk: bytes, names_list: list[bytes]) -> list[tuple[bytes, bytes, Any]]:
	"""
	Parse variables from the given chunk.

	:param chunk:
	:param names_list: Name lookup table for the file.

	:returns: List of variables, as tuples of variable name, variable REDengine type, variable value.
	"""

	return _read_class(BytesIO(chunk), len(chunk), names_list)


def get_array_variables(chunk: bytes, names_list: list[bytes]) -> list[list[tuple[bytes, bytes, Any]]]:
	"""
	Parse variables for an array from the given chunk.

	:param chunk:
	:param names_list: Name lookup table for the file.

	:returns: List of lists of variables, as tuples of variable name, variable REDengine type, variable value.
	"""

	buffer = BytesIO(chunk)
	array_size = int.from_bytes(buffer.read(4), "little")
	variables: list[list[tuple[bytes, bytes, Any]]] = []

	for _ in range(array_size):
		# variables.append(_read_class(buffer, len(chunk), names_list))
		variables.append(_read_class(buffer, 0, names_list))

	assert buffer.tell() == len(chunk)

	return variables


def _read_class(buffer: BytesIO, chunk_size: int, names_list: list[bytes]) -> list[tuple[bytes, bytes, Any]]:
	# this package
	from cp2077_extractor.cr2w.io import CNameError, read_c_name

	zero = buffer.read(1)[0]
	assert zero == 0, f"Tried parsing a CVariable: zero read {zero}."

	variables: list[tuple[bytes, bytes, Any]] = []
	# while buffer.tell() < chunk_size:
	while True:
		try:
			var_c_name = read_c_name(buffer, names_list)
		except CNameError:
			break
		red_type_name = read_c_name(buffer, names_list)
		size = struct.unpack("<I", buffer.read(4))[0] - 4
		value = buffer.read(size)
		variables.append((var_c_name, red_type_name, value))

	if chunk_size:
		assert buffer.tell() == chunk_size, (buffer.tell(), chunk_size)

	return variables
