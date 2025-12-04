#!/usr/bin/env python3
#
#  base.py
"""
Basic classes for representing datatypes within CR2W/W2RC files.
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
import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

# 3rd party
from typing_extensions import TypedDict

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.utils import get_array_variables, get_chunk_variables
from cp2077_extractor.utils import StringReader, to_snake_case

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.io import ParsingData

__all__ = [
		"Array",
		"Box",
		"CColor",
		"CMatrix",
		"Chunk",
		"DeferredBufferData",
		"EulerAngles",
		"HandleData",
		"Plane",
		"QsTransform",
		"Quaternion",
		"Sphere",
		"Transform",
		"handle",
		"instantiate_type",
		"lookup_type",
		"parse_array",
		"parse_chunk",
		"parse_cname_array",
		"parse_handle_array",
		"parse_string",
		"parse_string_array",
		"redTagList",
		"serialization_deferred_data_buffer",
		]

_red_type_lookup: dict[bytes, type | Callable[..., object]] = {}

_red_enum_list = enums.__all__[:]
_red_enum_list.remove("REDEnum")
for _class_name in _red_enum_list:
	_red_type_lookup[_class_name.encode("UTF-8")] = getattr(enums, _class_name)


class Chunk:
	"""
	Base class for chunks in CR2W/W2RC files; packed data containing variable names, types and values.
	"""

	def __init_subclass__(cls, *args, **kwargs):
		_red_type_lookup[cls.__name__.encode("UTF-8")] = cls

	@classmethod
	def from_cr2w_kwargs(cls, kwargs: dict[bytes, Any]) -> "Chunk":
		"""
		Construct from a mapping of REDengine variable names and values (as Python types).
		"""
		new_kwargs: dict[str, Any] = {
				to_snake_case(arg_name.decode("UTF-8")): arg_value
				for arg_name, arg_value in kwargs.items()
				}
		return cls(**new_kwargs)

	@classmethod
	def from_chunk(cls, chunk: bytes, parsing_data: "ParsingData") -> "Chunk":
		"""
		Parse raw bytes.

		:param chunk: The raw bytes.
		:param parsing_data:
		"""

		kwargs = parse_chunk(chunk, parsing_data)
		return cls.from_cr2w_kwargs(kwargs)


@dataclass
class Array:
	"""
	Type of an array in a CR2W/W2RC file, with the name of the inner type.
	"""

	value_red_type_name: bytes

	def __call__(self, value: bytes, parsing_data: "ParsingData") -> list:
		"""
		Convert ``value`` (representing an array) into a Python list.

		:param value:
		:param parsing_data:
		"""

		if self.value_red_type_name == b"CName":
			return parse_cname_array(value, parsing_data)

		array_value_type = lookup_type(self.value_red_type_name)
		if inspect.isclass(array_value_type) and issubclass(array_value_type, Chunk):
			return [array_value_type.from_cr2w_kwargs(av) for av in parse_array(value, parsing_data)]
		elif self.value_red_type_name == b"String":
			return parse_string_array(value)
		elif self.value_red_type_name.startswith(b"handle:"):
			return parse_handle_array(value, parsing_data)
		else:
			raise NotImplementedError(array_value_type)


def lookup_type(red_type_name: bytes) -> type | Callable[..., object]:
	"""
	Lookup a Python type from its REDengine equivalent's name.

	:param red_type_name:
	"""

	if red_type_name in _red_type_lookup:
		# print("Looked up", red_type_name, "as", _red_type_lookup[red_type_name])
		return _red_type_lookup[red_type_name]
	elif red_type_name.startswith(b"array:"):
		return Array(red_type_name.split(b":", 1)[1])
	elif red_type_name.startswith(b"handle:"):
		return handle
	else:
		raise NotImplementedError(red_type_name)


def parse_chunk(chunk: bytes, parsing_data: "ParsingData") -> dict[bytes, Any]:
	"""
	Parse the given chunk of data and return a mapping of variable names to values.

	:param chunk:
	:param parsing_data:
	"""

	variables = get_chunk_variables(chunk, parsing_data.names_list)

	kwargs: dict[bytes, Any] = {}
	for (var_c_name, red_type_name, value) in variables:
		kwargs[var_c_name] = instantiate_type(red_type_name, value, parsing_data)

	return kwargs


def parse_array(chunk: bytes, parsing_data: "ParsingData") -> list[dict[bytes, str]]:
	"""
	Parse the given chunk of data as an array and return a list of mapping of variable names to values.

	:param chunk:
	:param parsing_data:
	"""

	variables = get_array_variables(chunk, parsing_data.names_list)

	array_contents = []
	for array_item in variables:

		kwargs: dict[bytes, Any] = {}
		for (var_c_name, red_type_name, value) in array_item:
			kwargs[var_c_name] = instantiate_type(red_type_name, value, parsing_data)

		array_contents.append(kwargs)

	return array_contents


def instantiate_type(red_type_name: bytes, value: bytes, parsing_data: "ParsingData") -> object:
	"""
	Create a Python class instance for the given REDengine type and the given value.

	:param red_type_name:
	:param value:
	:param parsing_data:
	"""

	# this package
	from cp2077_extractor.cr2w.io import read_c_name

	if red_type_name == b"CName":
		return read_c_name(BytesIO(value), parsing_data.names_list)

	var_type = lookup_type(red_type_name)

	if inspect.isclass(var_type) and issubclass(var_type, enums.REDEnum):
		return var_type.from_red_name(parsing_data.names_list[uint(value)])
	elif var_type is Chunk:
		return (red_type_name, parse_chunk(value, parsing_data))
	elif isinstance(var_type, Array):
		return var_type(value, parsing_data)
	elif inspect.isclass(var_type) and issubclass(var_type, Chunk):
		return var_type.from_chunk(value, parsing_data)
	elif var_type in {handle, serialization_deferred_data_buffer}:
		return var_type(value, parsing_data)
	else:
		return var_type(value)


HandleVarType = TypeVar("HandleVarType", bound=Chunk)


class HandleData(TypedDict, Generic[HandleVarType]):
	"""
	Return type of :func:`~.handle`.
	"""

	handle_id: int
	data: HandleVarType


def handle(handle: bytes, parsing_data: "ParsingData") -> HandleData[Chunk]:
	"""
	A handle points to the data in another chunk. Read that chunk and return the resulting data.

	:param handle: Raw bytes of the handle (the value of a ``handle:xxxxxx`` type), referring to the target chunk.
	:param parsing_data:
	"""

	handle_idx = int.from_bytes(handle, "little") - 1
	chunk = parsing_data.chunks[handle_idx]
	return {"handle_id": handle_idx, "data": cast(Chunk, instantiate_type(chunk[1], chunk[0], parsing_data))}


class DeferredBufferData(TypedDict):
	"""
	Return type of :func:`~.serialization_deferred_data_buffer`.
	"""

	buffer_id: int
	flags: int
	bytes: bytes


def serialization_deferred_data_buffer(
		buffer_id: bytes,
		parsing_data: "ParsingData",
		) -> DeferredBufferData:
	"""
	A ``serializationDeferredDataBuffer`` points to a buffer in the CR2W/W2RC file, containing the actual data e.g. a texture.

	:param buffer_id: The ID of the buffer. Unknown format. Currently ignored and assumed to point to the first buffer.
	:param parsing_data:
	"""

	# TODO: Two bytes. With one buffer it's 1 0.
	assert buffer_id == b"\1\0"
	buffer_idx = 0  # TODO: proper lookup implementation
	buffer, buffer_info = parsing_data.buffers[buffer_idx]
	return {"buffer_id": buffer_idx, "flags": buffer_info.flags, "bytes": buffer}


def parse_string(data: bytes) -> str:
	"""
	Parse a bytes string (which has a VLQ i32 size prefix) to a Python string.

	:param
	"""

	return StringReader(data).parse_string()


def parse_string_array(data: bytes) -> list[str]:
	"""
	Parse an array of strings.

	:param data:
	"""

	array_size = int.from_bytes(data[:4], "little")
	string_reader = StringReader(data[4:])
	return [string_reader.parse_string() for _ in range(array_size)]


def parse_cname_array(data: bytes, parsing_data: "ParsingData") -> list[bytes]:
	"""
	Parse an array of c names.

	:param data:
	"""

	# this package
	from cp2077_extractor.cr2w.io import read_c_name

	array_size = int.from_bytes(data[:4], "little")
	buffer = BytesIO(data[4:])
	return [read_c_name(buffer, parsing_data.names_list) for _ in range(array_size)]


def parse_handle_array(data: bytes, parsing_data: "ParsingData") -> list[HandleData[Chunk]]:
	"""
	Parse an array of handles (each 4 bytes long).

	:param data:
	"""

	array_size = int.from_bytes(data[:4], "little")
	array = [handle(data[4 + (4 * idx):8 + (4 * idx)], parsing_data) for idx in range(array_size)]
	return array


@dataclass
class Quaternion(Chunk):
	i: float = 0.0
	j: float = 0.0
	k: float = 0.0
	r: float = 1.0


@dataclass
class Transform(Chunk):
	position: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	orientation: Quaternion = field(default_factory=Quaternion)


@dataclass
class redTagList(Chunk):
	tags: list[str] = field(default_factory=list)


# def uint(value: bytes) -> int:
# 	return int.from_bytes(value, byteorder="little")

uint = functools.partial(int.from_bytes, byteorder="little")

_red_type_lookup.update({
		# b"DataBuffer": bytes,  # TODO
		b"Bool": bool,
		b"String": parse_string,
		b"Uint16": uint,
		b"Uint32": uint,
		b"Uint64": uint,
		b"Uint8": uint,
		b"CRUID": uint,
		b"TweakDBID": uint,
		b"handle": handle,
		b"raRef:animAnimSet": bytes,  # TODO
		b"serializationDeferredDataBuffer": serialization_deferred_data_buffer,
		b"NodeRef": bytes,
		b"[32]Uint8": bytes,
		})


@dataclass
class EulerAngles(Chunk):
	pitch: float = 0.0
	yaw: float = 0.0
	roll: float = 0.0


@dataclass
class QsTransform(Chunk):
	translation: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	rotation: Quaternion = field(default_factory=Quaternion)
	scale: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)


@dataclass
class CColor(Chunk):
	red: int = 0
	green: int = 0
	blue: int = 0
	alpha: int = 0


@dataclass
class Sphere(Chunk):
	center_radius2: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


@dataclass
class CMatrix(Chunk):
	x: tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0)
	y: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 0.0)
	z: tuple[float, float, float, float] = (0.0, 0.0, 1.0, 0.0)
	w: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)


@dataclass
class Box(Chunk):
	min: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	max: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


@dataclass
class Plane(Chunk):
	normal_distance: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
