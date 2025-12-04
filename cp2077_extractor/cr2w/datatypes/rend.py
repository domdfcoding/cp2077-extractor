#!/usr/bin/env python3
#
#  rend.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``rend``).
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
from dataclasses import dataclass, field
from typing import Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, DeferredBufferData, HandleData

__all__ = [
		"rendRenderTextureBlobHeader",
		"rendRenderTextureBlobMemoryLayout",
		"rendRenderTextureBlobMipMapInfo",
		"rendRenderTextureBlobPC",
		"rendRenderTextureBlobPlacement",
		"rendRenderTextureBlobSizeInfo",
		"rendRenderTextureBlobTextureInfo",
		"rendRenderTextureResource",
		"rendSLightFlickering",
		]


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
class rendRenderTextureBlobPC(Chunk):
	header: rendRenderTextureBlobHeader
	texture_data: DeferredBufferData


@dataclass
class rendRenderTextureResource(Chunk):
	render_resource_blob_pc: HandleData[Chunk] = field(
			default_factory=dict
			)  # type: ignore[assignment] # TODO: handle inner type # CHandle


@dataclass
class rendRenderTextureBlobMemoryLayout(Chunk):
	row_pitch: int = 0
	slice_pitch: int = 0


@dataclass
class rendRenderTextureBlobPlacement(Chunk):
	size: int = 0
	offset: int = 0


@dataclass
class rendRenderTextureBlobMipMapInfo(Chunk):
	layout: rendRenderTextureBlobMemoryLayout = field(default_factory=rendRenderTextureBlobMemoryLayout)
	placement: rendRenderTextureBlobPlacement = field(default_factory=rendRenderTextureBlobPlacement)


@dataclass
class rendSLightFlickering(Chunk):
	position_offset: float = 0.0
	flicker_strength: float = 0.0
	flicker_period: float = 0.2
