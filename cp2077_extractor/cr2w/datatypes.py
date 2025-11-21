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
import struct
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import Any

# this package
from cp2077_extractor.cr2w.enums import (
		ECookingPlatform,
		ETextureCompression,
		ETextureRawFormat,
		GpuWrapApieTextureGroup,
		GpuWrapApieTextureType
		)
from cp2077_extractor.cr2w.io import read_c_name
from cp2077_extractor.cr2w.textures import DDSFormat
from cp2077_extractor.utils import to_snake_case

# this package
from . import enums

__all__ = [
		"CBitmapTexture",
		"Chunk",
		"Name",
		"STextureGroupSetup",
		"array_rendRenderTextureBlobMipMapInfo",
		"get_chunk_variables",
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


class Name:

	@classmethod
	def lookup(cls, value: bytes, names_list: list[bytes]):
		return names_list[uint(value)]


class Chunk:

	@classmethod
	def from_cr2w_kwargs(cls, kwargs: dict[bytes, Any]):
		new_kwargs: dict[str, Any] = {
				to_snake_case(arg_name.decode("UTF-8")): arg_value
				for arg_name, arg_value in kwargs.items()
				}
		return cls(**new_kwargs)

	@classmethod
	def from_chunk(cls, chunk: bytes, names_list: list[bytes], chunks: list[bytes]):
		kwargs = parse_chunk(chunk, names_list, chunks)
		return cls.from_cr2w_kwargs(kwargs)


def uint(value: bytes):
	return int.from_bytes(value, byteorder="little")


def lookup_type(red_type_name: bytes) -> type:
	if red_type_name in _red_type_lookup:
		# print("Looked up", red_type_name, "as", _red_type_lookup[red_type_name])
		return _red_type_lookup[red_type_name]

	else:
		raise NotImplementedError(red_type_name)


def get_chunk_variables(chunk: bytes, names_list: list[bytes]) -> list[tuple[bytes, bytes, Any]]:
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


def parse_chunk(chunk: bytes, names_list: list[bytes], chunks: list[bytes]) -> dict[bytes, Any]:

	variables = get_chunk_variables(chunk, names_list)

	kwargs: dict[bytes, Any] = {}
	for (var_c_name, red_type_name, value) in variables:
		kwargs[var_c_name] = instantiate_type(red_type_name, value, names_list, chunks)

	return kwargs


def instantiate_type(red_type_name: bytes, value: bytes, names_list: list[bytes], chunks: list[bytes]):
	var_type = lookup_type(red_type_name)

	if var_type is Name:
		# print(f"{var_c_name} =", Name.lookup(value, names_list))
		return (red_type_name, Name.lookup(value, names_list))
	elif inspect.isclass(var_type) and issubclass(var_type, Enum):
		return var_type.from_red_name(Name.lookup(value, names_list))
	elif var_type is Chunk:
		return (red_type_name, parse_chunk(value, names_list, chunks))
	elif inspect.isclass(var_type) and issubclass(var_type, Chunk):
		return var_type.from_chunk(value, names_list, chunks)
	elif var_type is handle:
		return var_type(value, names_list, chunks)
	else:
		# print(f"{var_c_name} =",  var_type(value))
		return var_type(value)


class array_rendRenderTextureBlobMipMapInfo(bytes):
	# TODO: parse the array
	def __repr__(self):
		return f"array:rendRenderTextureBlobMipMapInfo({super().__repr__()})"

	__str__ = __repr__


def handle(handle: bytes, names_list: list[bytes], chunks: list[bytes]):
	handle_idx = int.from_bytes(handle, "little") - 1
	return instantiate_type(chunks[handle_idx][1], chunks[handle_idx][0], names_list, chunks)


class serializationDeferredDataBuffer(bytes):
	# TODO: Two bytes. With one buffer it's 1 0.
	# Maybe number of buffers and indices?
	# Find buffer itself in file_info.buffer_info
	def __repr__(self):
		return f"serializationDeferredDataBuffer({super().__repr__()})"

	def get_buffer_idx(self):
		# TODO
		return 0

	__str__ = __repr__


@dataclass
class rendRenderTextureBlobTextureInfo(Chunk):
	texture_data_size: int
	slice_size: int
	data_alignment: int
	slice_count: int
	mip_count: int
	type: GpuWrapApieTextureType = GpuWrapApieTextureType.TEXTYPE_2D


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
	texture_data: serializationDeferredDataBuffer  # TODO: lookup data


@dataclass
class STextureGroupSetup(Chunk):
	compression: ETextureCompression
	is_gamma: bool
	platform_mip_bias_pc: int = 0
	platform_mip_bias_console: int = 0
	is_streamable: bool = True
	has_mipchain: bool = True
	allow_texture_downgrade: bool = True
	group: GpuWrapApieTextureGroup = GpuWrapApieTextureGroup.TEXG_Generic_Color
	raw_format: ETextureRawFormat = ETextureRawFormat.TRF_TrueColor


@dataclass
class rendRenderTextureResource(Chunk):

	# render_resource_blob_pc: handle_IRenderResourceBlob  # CHandle
	render_resource_blob_pc: dict[bytes, Any]  # CHandle


@dataclass
class CBitmapTexture(Chunk):
	cooking_platform: ECookingPlatform
	width: int
	height: int
	# render_resource_blob: Any  # RenderResourceBlob  # TODO: check resolved type
	render_texture_resource: rendRenderTextureResource  # TODO: default is new rendRenderTextureResource
	setup: STextureGroupSetup = field(default_factory=STextureGroupSetup)
	depth: int = 1
	hist_bias_mul_coef: tuple[float, float, float] = (1.0, 1.0, 1.0)  # Vector3
	hist_bias_add_coef: tuple[float, float, float] = (0.0, 0.0, 0.0)  # Vector3


_red_type_lookup = {
		b"ECookingPlatform": Name,
		b"Uint32": uint,
		b"Uint16": uint,
		b"Uint8": uint,
		b"STextureGroupSetup": STextureGroupSetup,
		b"rendRenderTextureResource": rendRenderTextureResource,
		b"rendRenderTextureBlobHeader": rendRenderTextureBlobHeader,
		b"serializationDeferredDataBuffer": serializationDeferredDataBuffer,
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
