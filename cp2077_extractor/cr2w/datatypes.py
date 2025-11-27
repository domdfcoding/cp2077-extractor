#!/usr/bin/env python3
#
#  datatypes.py
"""
Classes to represent datatypes within CR2W/W2RC files.
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
from typing import TYPE_CHECKING, Any, TypedDict, cast

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.utils import get_array_variables, get_chunk_variables
from cp2077_extractor.utils import to_snake_case

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.io import ParsingData

__all__ = [
		"Array",
		"CBitmapTexture",
		"Chunk",
		"DeferredBufferData",
		"HandleData",
		"STextureGroupSetup",
		"array_String",
		"handle",
		"inkCreditsResource",
		"inkCreditsSectionEntry",
		"instantiate_type",
		"lookup_type",
		"parse_array",
		"parse_chunk",
		"rendRenderTextureBlobHeader",
		"rendRenderTextureBlobPC",
		"rendRenderTextureBlobSizeInfo",
		"rendRenderTextureBlobTextureInfo",
		"rendRenderTextureResource",
		"serialization_deferred_data_buffer"
		]


class Chunk:
	"""
	Base class for chunks in CR2W/W2RC files; packed data containing variable names, types and values.
	"""

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
	value_red_type_name: bytes


# def uint(value: bytes) -> int:
# 	return int.from_bytes(value, byteorder="little")

uint = functools.partial(int.from_bytes, byteorder="little")


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


def parse_array(chunk: bytes, parsing_data: "ParsingData") -> dict[bytes, Any]:
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

	var_type = lookup_type(red_type_name)

	if inspect.isclass(var_type) and issubclass(var_type, enums.REDEnum):
		return var_type.from_red_name(parsing_data.names_list[uint(value)])
	elif var_type is Chunk:
		return (red_type_name, parse_chunk(value, parsing_data))
	elif isinstance(var_type, Array):
		array_value_type = lookup_type(var_type.value_red_type_name)
		if inspect.isclass(array_value_type) and issubclass(array_value_type, Chunk):
			return (
					red_type_name,
					[array_value_type.from_cr2w_kwargs(av) for av in parse_array(value, parsing_data)]
					)
		else:
			raise NotImplementedError(array_value_type)
	elif inspect.isclass(var_type) and issubclass(var_type, Chunk):
		return var_type.from_chunk(value, parsing_data)
	elif var_type in {handle, serialization_deferred_data_buffer}:
		return var_type(value, parsing_data)
	else:
		return var_type(value)


class array_String(bytes):  # noqa: D101
	# TODO: parse the array
	def __repr__(self) -> str:
		return f"array:String({super().__repr__()})"

	__str__ = __repr__


class HandleData(TypedDict):
	"""
	Return type of :func:`~.handle`.
	"""

	handle_id: int
	data: Chunk


def handle(handle: bytes, parsing_data: "ParsingData") -> HandleData:
	"""
	A handle points to the data in another chunk. Read that chunk and return the resulting data.

	:param handle: Raw bytes of the handle (the value of a ``handle:Ixxxxxx`` type), referring to the target chunk.
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
	buffer_idx = 0  # TODO: proper lookup implementation
	buffer, buffer_info = parsing_data.buffers[buffer_idx]
	return {"buffer_id": buffer_idx, "flags": buffer_info.flags, "bytes": buffer}


@dataclass
class rendRenderTextureBlobTextureInfo(Chunk):  # noqa: D101
	texture_data_size: int
	slice_size: int
	data_alignment: int
	slice_count: int
	mip_count: int
	type: enums.GpuWrapApieTextureType = enums.GpuWrapApieTextureType.TEXTYPE_2D


@dataclass
class rendRenderTextureBlobSizeInfo(Chunk):
	"""
	Size info for a texture.
	"""

	width: int
	height: int
	depth: int = 1


@dataclass
class rendRenderTextureBlobHeader(Chunk):
	"""
	Header for texture data and associated properties.
	"""

	version: int
	size_info: rendRenderTextureBlobSizeInfo
	texture_info: rendRenderTextureBlobTextureInfo
	flags: int
	mip_map_info: list[Any] = field(default_factory=list)  # list[MipMapInfo]  # TODO: parse array
	histogram_data: list[Any] = field(default_factory=list)  # list[HistogramData]


@dataclass
class rendRenderTextureBlobPC(Chunk):  # noqa: D101
	header: rendRenderTextureBlobHeader
	texture_data: DeferredBufferData


@dataclass
class STextureGroupSetup(Chunk):
	"""
	Properties of a texture file.
	"""

	compression: enums.ETextureCompression
	is_gamma: bool = False
	platform_mip_bias_pc: int = 0
	platform_mip_bias_console: int = 0
	is_streamable: bool = True
	has_mipchain: bool = True
	allow_texture_downgrade: bool = True
	group: enums.GpuWrapApieTextureGroup = enums.GpuWrapApieTextureGroup.TEXG_Generic_Color
	raw_format: enums.ETextureRawFormat = enums.ETextureRawFormat.TRF_TrueColor


@dataclass
class rendRenderTextureResource(Chunk):  # noqa: D101

	render_resource_blob_pc: HandleData  # CHandle


@dataclass
class CBitmapTexture(Chunk):
	"""
	A texture file.
	"""

	cooking_platform: enums.ECookingPlatform
	width: int
	height: int
	# render_resource_blob: Any  # RenderResourceBlob  # TODO: check resolved type
	render_texture_resource: rendRenderTextureResource  # TODO: default is new rendRenderTextureResource
	setup: STextureGroupSetup = field(default_factory=STextureGroupSetup)  # type: ignore[arg-type]
	depth: int = 1
	hist_bias_mul_coef: tuple[float, float, float] = (1.0, 1.0, 1.0)  # Vector3
	hist_bias_add_coef: tuple[float, float, float] = (0.0, 0.0, 0.0)  # Vector3


@dataclass
class inkCreditsSectionEntry(Chunk):
	names: list[bytes]
	display_mode: enums.inkDisplayMode
	section_title: bytes = ''


@dataclass
class inkCreditsResource(Chunk):
	cooking_platform: enums.ECookingPlatform
	sections: list[inkCreditsSectionEntry]


_red_type_lookup: dict[bytes, type | Callable[..., object]] = {
		b"array:String": array_String,  # TODO
		b"Bool": bool,
		b"CBitmapTexture": CBitmapTexture,
		b"ECookingPlatform": enums.ECookingPlatform,
		b"handle:IRenderResourceBlob": handle,
		b"inkCreditsResource": inkCreditsResource,
		b"inkCreditsSectionEntry": inkCreditsSectionEntry,
		b"rendRenderTextureBlobHeader": rendRenderTextureBlobHeader,
		b"rendRenderTextureBlobPC": rendRenderTextureBlobPC,
		b"rendRenderTextureBlobSizeInfo": rendRenderTextureBlobSizeInfo,
		b"rendRenderTextureBlobTextureInfo": rendRenderTextureBlobTextureInfo,
		b"rendRenderTextureResource": rendRenderTextureResource,
		b"serializationDeferredDataBuffer": serialization_deferred_data_buffer,
		b"STextureGroupSetup": STextureGroupSetup,
		b"String": bytes,
		b"Uint16": uint,
		b"Uint32": uint,
		b"Uint8": uint,
		}

_red_enum_list = enums.__all__[:]
_red_enum_list.remove("REDEnum")
for _class_name in _red_enum_list:
	_red_type_lookup[_class_name.encode("UTF-8")] = getattr(enums, _class_name)
