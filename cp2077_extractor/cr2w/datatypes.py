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
import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.utils import get_chunk_variables
from cp2077_extractor.utils import to_snake_case

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.io import ParsingData

__all__ = [
		"CBitmapTexture",
		"Chunk",
		"STextureGroupSetup",
		"array_rendRenderTextureBlobMipMapInfo",
		"handle",
		"instantiate_type",
		"lookup_type",
		"parse_chunk",
		"rendRenderTextureBlobHeader",
		"rendRenderTextureBlobPC",
		"rendRenderTextureBlobSizeInfo",
		"rendRenderTextureBlobTextureInfo",
		"rendRenderTextureResource",
		"serializationDeferredDataBuffer",
		"uint"
		]


class Chunk:

	@classmethod
	def from_cr2w_kwargs(cls, kwargs: dict[bytes, Any]) -> "Chunk":
		new_kwargs: dict[str, Any] = {
				to_snake_case(arg_name.decode("UTF-8")): arg_value
				for arg_name, arg_value in kwargs.items()
				}
		return cls(**new_kwargs)

	@classmethod
	def from_chunk(cls, chunk: bytes, parsing_data: "ParsingData") -> "Chunk":
		kwargs = parse_chunk(chunk, parsing_data)
		return cls.from_cr2w_kwargs(kwargs)


def uint(value: bytes) -> int:
	return int.from_bytes(value, byteorder="little")


def lookup_type(red_type_name: bytes) -> type:
	if red_type_name in _red_type_lookup:
		# print("Looked up", red_type_name, "as", _red_type_lookup[red_type_name])
		return _red_type_lookup[red_type_name]

	else:
		raise NotImplementedError(red_type_name)


def parse_chunk(chunk: bytes, parsing_data: "ParsingData") -> dict[bytes, Any]:

	variables = get_chunk_variables(chunk, parsing_data.names_list)

	kwargs: dict[bytes, Any] = {}
	for (var_c_name, red_type_name, value) in variables:
		kwargs[var_c_name] = instantiate_type(red_type_name, value, parsing_data)

	return kwargs


def instantiate_type(red_type_name: bytes, value: bytes, parsing_data: "ParsingData") -> object:
	var_type = lookup_type(red_type_name)

	if inspect.isclass(var_type) and issubclass(var_type, Enum):
		return var_type.from_red_name(parsing_data.names_list[uint(value)])
	elif var_type is Chunk:
		return (red_type_name, parse_chunk(value, parsing_data))
	elif inspect.isclass(var_type) and issubclass(var_type, Chunk):
		return var_type.from_chunk(value, parsing_data)
	elif var_type in {handle, serialization_deferred_data_buffer}:
		return var_type(value, parsing_data)
	else:
		return var_type(value)


class array_rendRenderTextureBlobMipMapInfo(bytes):
	# TODO: parse the array
	def __repr__(self) -> str:
		return f"array:rendRenderTextureBlobMipMapInfo({super().__repr__()})"

	__str__ = __repr__


def handle(handle: bytes, parsing_data: "ParsingData") -> dict[str, Any]:  # TODO: TypedDict or class
	handle_idx = int.from_bytes(handle, "little") - 1
	chunk = parsing_data.chunks[handle_idx]
	return {"handle_id": handle_idx, "data": instantiate_type(chunk[1], chunk[0], parsing_data)}


def serialization_deferred_data_buffer(
		buffer_id: bytes,
		parsing_data: "ParsingData",
		) -> dict[str, Any]:  # TODO: TypedDict or class
	# TODO: Two bytes. With one buffer it's 1 0.
	buffer_idx = 0  # TODO: proper lookup implementation
	buffer, buffer_info = parsing_data.buffers[buffer_idx]
	return {"buffer_id": buffer_idx, "flags": buffer_info.flags, "bytes": buffer}


@dataclass
class rendRenderTextureBlobTextureInfo(Chunk):
	texture_data_size: int
	slice_size: int
	data_alignment: int
	slice_count: int
	mip_count: int
	type: enums.GpuWrapApieTextureType = enums.GpuWrapApieTextureType.TEXTYPE_2D


@dataclass
class rendRenderTextureBlobSizeInfo(Chunk):
	width: int
	height: int
	depth: int = 1


@dataclass
class rendRenderTextureBlobHeader(Chunk):
	version: int
	size_info: rendRenderTextureBlobSizeInfo
	texture_info: rendRenderTextureBlobTextureInfo
	flags: int
	mip_map_info: list[Any] = field(default_factory=list)  # list[MipMapInfo]  # TODO: parse array
	histogram_data: list[Any] = field(default_factory=list)  # list[HistogramData]


@dataclass
class rendRenderTextureBlobPC(Chunk):
	header: rendRenderTextureBlobHeader
	texture_data: bytes  # TODO: Type to cover this, buffer_id, & flags


@dataclass
class STextureGroupSetup(Chunk):
	compression: enums.ETextureCompression
	is_gamma: bool
	platform_mip_bias_pc: int = 0
	platform_mip_bias_console: int = 0
	is_streamable: bool = True
	has_mipchain: bool = True
	allow_texture_downgrade: bool = True
	group: enums.GpuWrapApieTextureGroup = enums.GpuWrapApieTextureGroup.TEXG_Generic_Color
	raw_format: enums.ETextureRawFormat = enums.ETextureRawFormat.TRF_TrueColor


@dataclass
class rendRenderTextureResource(Chunk):

	# render_resource_blob_pc: handle_IRenderResourceBlob  # CHandle
	render_resource_blob_pc: dict[bytes, Any]  # CHandle


@dataclass
class CBitmapTexture(Chunk):
	cooking_platform: enums.ECookingPlatform
	width: int
	height: int
	# render_resource_blob: Any  # RenderResourceBlob  # TODO: check resolved type
	render_texture_resource: rendRenderTextureResource  # TODO: default is new rendRenderTextureResource
	setup: STextureGroupSetup = field(default_factory=STextureGroupSetup)
	depth: int = 1
	hist_bias_mul_coef: tuple[float, float, float] = (1.0, 1.0, 1.0)  # Vector3
	hist_bias_add_coef: tuple[float, float, float] = (0.0, 0.0, 0.0)  # Vector3


_red_type_lookup = {
		b"ECookingPlatform": enums.ECookingPlatform,
		b"Uint32": uint,
		b"Uint16": uint,
		b"Uint8": uint,
		b"STextureGroupSetup": STextureGroupSetup,
		b"rendRenderTextureResource": rendRenderTextureResource,
		b"rendRenderTextureBlobHeader": rendRenderTextureBlobHeader,
		b"serializationDeferredDataBuffer": serialization_deferred_data_buffer,
		# b"handle:IRenderResourceBlob": handle_IRenderResourceBlob,
		b"handle:IRenderResourceBlob": handle,
		b"Bool": bool,
		b"rendRenderTextureBlobSizeInfo": rendRenderTextureBlobSizeInfo,
		b"rendRenderTextureBlobTextureInfo": rendRenderTextureBlobTextureInfo,
		b"array:rendRenderTextureBlobMipMapInfo": array_rendRenderTextureBlobMipMapInfo,
		b"rendRenderTextureBlobPC": rendRenderTextureBlobPC,
		b"CBitmapTexture": CBitmapTexture,
		}

_red_enum_list = enums.__all__[:]
_red_enum_list.remove("REDEnum")
for _class_name in _red_enum_list:
	_red_type_lookup[_class_name.encode("UTF-8")] = getattr(enums, _class_name)
