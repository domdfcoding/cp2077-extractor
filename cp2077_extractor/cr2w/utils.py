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

__all__ = ["get_chunk_variables", "get_names_list"]


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

	# this package
	from cp2077_extractor.cr2w.io import read_c_name

	variables: list[tuple[bytes, bytes, Any]] = []
	buffer = BytesIO(chunk)
	zero = buffer.read(1)
	assert zero == b"\0", f"Tried parsing a CVariable: zero read {zero}."
	while buffer.tell() < len(chunk) - 1:
		try:
			var_c_name = read_c_name(buffer, names_list)
			red_type_name = read_c_name(buffer, names_list)
			size = struct.unpack("<I", buffer.read(4))[0] - 4
			value = buffer.read(size)
			variables.append((var_c_name, red_type_name, value))
		except:
			# Run out of buffer
			break

	return variables
