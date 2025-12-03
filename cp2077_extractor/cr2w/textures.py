#!/usr/bin/env python3
#
#  textures.py
"""
Texture extraction and conversion logic.
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
from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING, cast

# 3rd party
import texture2ddecoder
from PIL import Image

# this package
from cp2077_extractor.cr2w.datatypes import rendRenderTextureBlobPC
from cp2077_extractor.cr2w.enums import ETextureCompression

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.datatypes import CBitmapTexture

__all__ = ["DDSFormat", "get_dds_decoder", "get_dds_format_from_compression", "texture_to_image"]


class DDSFormat(Enum):
	"""
	Enum of different formats for DirectDraw Surface ``.dds`` files.
	"""

	R8G8B8A8_UNORM = 0
	BC1_UNORM = 1
	BC3_UNORM = 2
	BC7_UNORM = 7
	BC4_UNORM = 4
	BC5_UNORM = 5


def get_dds_decoder(dds_format: DDSFormat) -> Callable[[bytes, int, int], bytes]:
	"""
	Returns the function to decode a DDS texture, for use with :meth:`PIL.Image.frombytes`.

	:param dds_format:
	"""

	if dds_format == DDSFormat.R8G8B8A8_UNORM:
		raise NotImplementedError
	elif dds_format == DDSFormat.BC1_UNORM:
		return texture2ddecoder.decode_bc1
	elif dds_format == DDSFormat.BC3_UNORM:
		return texture2ddecoder.decode_bc3
	elif dds_format == DDSFormat.BC7_UNORM:
		return texture2ddecoder.decode_bc7
	elif dds_format == DDSFormat.BC4_UNORM:
		return texture2ddecoder.decode_bc4
	elif dds_format == DDSFormat.BC5_UNORM:
		return texture2ddecoder.decode_bc5
	else:
		raise ValueError(f"Unknown format {dds_format!r}")


def get_dds_format_from_compression(compression: ETextureCompression) -> DDSFormat:
	"""
	Find the DDS format for the given texture compression type.

	:param compression
	"""

	if compression == ETextureCompression.TCM_None:
		return DDSFormat.R8G8B8A8_UNORM

	if compression == ETextureCompression.TCM_DXTNoAlpha:
		return DDSFormat.BC1_UNORM
	if compression == ETextureCompression.TCM_Normals:
		return DDSFormat.BC1_UNORM

	if compression == ETextureCompression.TCM_DXTAlpha:
		return DDSFormat.BC3_UNORM
	if compression == ETextureCompression.TCM_NormalsHigh:
		return DDSFormat.BC3_UNORM
	if compression == ETextureCompression.TCM_NormalsGloss:
		return DDSFormat.BC3_UNORM

	if compression == ETextureCompression.TCM_QualityColor:
		return DDSFormat.BC7_UNORM

	if compression == ETextureCompression.TCM_QualityR:
		return DDSFormat.BC4_UNORM

	if compression == ETextureCompression.TCM_QualityRG:
		return DDSFormat.BC5_UNORM
	if compression == ETextureCompression.TCM_Normalmap:
		return DDSFormat.BC5_UNORM

	# if compression == ETextureCompression.TCM_DXTAlphaLinear:
	# 	pass
	# if compression == ETextureCompression.TCM_RGBE:
	# 	pass

	else:
		raise NotImplementedError(compression)


def texture_to_image(texture: "CBitmapTexture") -> Image.Image:
	"""
	Convert a texture to a PIL image.

	:param texture:
	"""

	texture_data = cast(
			rendRenderTextureBlobPC,
			texture.render_texture_resource.render_resource_blob_pc["data"],
			).texture_data["bytes"]
	size = (texture.width, texture.height)
	decoder = get_dds_decoder(get_dds_format_from_compression(texture.setup.compression))

	decoded_data = decoder(texture_data, *size)

	# TODO: check params against other formats
	img = Image.frombytes("RGBA", size, decoded_data, "raw", ("BGRA")).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
	return img
