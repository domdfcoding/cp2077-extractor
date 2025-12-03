#!/usr/bin/env python3
#
#  __init__.py
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
from dataclasses import dataclass, field
from typing import Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.anim import *
from cp2077_extractor.cr2w.datatypes.appearance import *
from cp2077_extractor.cr2w.datatypes.base import *
from cp2077_extractor.cr2w.datatypes.ent import *
from cp2077_extractor.cr2w.datatypes.game import *
from cp2077_extractor.cr2w.datatypes.graph import *
from cp2077_extractor.cr2w.datatypes.ink import *
from cp2077_extractor.cr2w.datatypes.physics import *
from cp2077_extractor.cr2w.datatypes.quest import *
from cp2077_extractor.cr2w.datatypes.rend import *
from cp2077_extractor.cr2w.datatypes.scn import *
from cp2077_extractor.cr2w.datatypes.work import *
from cp2077_extractor.cr2w.datatypes.world import *

__all__ = ["CBitmapTexture", "STextureGroupSetup"]


@dataclass
class STextureGroupSetup(Chunk):
	"""
	Properties of a texture file.
	"""

	group: enums.GpuWrapApieTextureGroup = enums.GpuWrapApieTextureGroup.TEXG_Generic_Color
	raw_format: enums.ETextureRawFormat = enums.ETextureRawFormat.TRF_TrueColor
	compression: enums.ETextureCompression = enums.ETextureCompression.TCM_None
	is_streamable: bool = True
	has_mipchain: bool = True
	is_gamma: bool = False
	platform_mip_bias_pc: int = 0
	platform_mip_bias_console: int = 0
	allow_texture_downgrade: bool = True


@dataclass
class CBitmapTexture(Chunk):
	"""
	A texture file.
	"""

	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	width: int = 0
	height: int = 0
	depth: int = 1
	setup: STextureGroupSetup = field(default_factory=STextureGroupSetup)
	hist_bias_mul_coef: tuple[float, float, float] = (1.0, 1.0, 1.0)
	hist_bias_add_coef: tuple[float, float, float] = (0.0, 0.0, 0.0)
	render_resource_blob: Any = None  # TODO: IRenderResourceBlob = field(default_factory=IRenderResourceBlob) # TODO: check resolved type
	render_texture_resource: rendRenderTextureResource = field(default_factory=rendRenderTextureResource)
