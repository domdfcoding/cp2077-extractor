#!/usr/bin/env python3
#
#  mesh.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``mesh``).
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
from cp2077_extractor.cr2w.datatypes.base import Box, Chunk, CMatrix, HandleData

__all__ = [
		"CMaterialInstance",
		"CMesh",
		"CMeshMaterialEntry",
		"IMaterial",
		"meshLocalMaterialHeader",
		"meshMeshAppearance",
		"meshMeshMaterialBuffer",
		"meshMeshParameter",
		]


@dataclass
class IMaterial(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None


@dataclass
class CMaterialInstance(IMaterial):
	base_material: IMaterial = field(default_factory=IMaterial)  # TODO: CResourceReference
	enable_mask: bool = False
	audio_tag: str = ''
	resource_version: int = 0


@dataclass
class meshMeshAppearance(Chunk):
	name: str = "default"
	chunk_materials: list[str] = field(default_factory=list)
	tags: list[str] = field(default_factory=list)


@dataclass
class meshLocalMaterialHeader(Chunk):
	offset: int = 0
	size: int = 0


@dataclass
class meshMeshMaterialBuffer(Chunk):
	raw_data: Any = None  # TODO: DataBuffer = field(default_factory=DataBuffer)
	raw_data_headers: list[meshLocalMaterialHeader] = field(default_factory=list)


class meshMeshParameter(Chunk):
	pass


@dataclass
class CMeshMaterialEntry(Chunk):
	name: str = ''
	index: int = 0
	is_local_instance: bool = False


@dataclass
class CMesh(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	# Missing ordinal 1
	parameters: list[meshMeshParameter] = field(default_factory=list)
	bounding_box: Box = field(
			default_factory=Box
			)  # TODO: Box { Min = new Vector4 { X = float.MaxValue, Y = float.MaxValue, Z = float.MaxValue, W = float.MaxValue }, Max = new Vector4 { X = float.MinValue, Y = float.MinValue, Z = float.MinValue, W = float.MinValue } };
	surface_area_per_axis: tuple[float, float, float] = (-1.0, -1.0, -1.0)
	# Missing ordinal 5
	material_entries: list[CMeshMaterialEntry] = field(default_factory=list)
	external_materials: list[IMaterial] = field(default_factory=list)  # TODO: CResourceAsyncReference
	local_material_instances: list[CMaterialInstance] = field(default_factory=list)
	local_material_buffer: meshMeshMaterialBuffer = field(default_factory=meshMeshMaterialBuffer)
	preload_external_materials: list[IMaterial] = field(default_factory=list)  # TODO: CResourceReference
	preload_local_material_instances: list[IMaterial] = field(default_factory=list)
	inplace_resources: list[Chunk] = field(default_factory=list)  # TODO: CResourceReference
	appearances: list[meshMeshAppearance] = field(default_factory=list)
	object_type: enums.ERenderObjectType = enums.ERenderObjectType.ROT_Static
	render_resource_blob: HandleData[Chunk] = field(  # TODO: Handle inner type
		default_factory=dict
		)  # type: ignore[assignment]  # IRenderResourceBlob
	lod_level_info: list[float] = field(default_factory=list)
	float_track_names: list[str] = field(default_factory=list)
	bone_names: list[str] = field(default_factory=list)
	bone_rig_matrices: list[CMatrix] = field(default_factory=list)
	bone_vertex_epsilons: list[float] = field(default_factory=list)
	lod_bone_mask: list[int] = field(default_factory=list)
	# Missing ordinal 22
	constrain_auto_hide_distance_to_terrain_height_map: bool = False
	force_load_all_appearances: bool = False
	cast_global_shadows_cached_in_cook: bool = False
	cast_local_shadows_cached_in_cook: bool = False
	use_ray_tracing_shadow_lodbias: bool = False
	casts_ray_traced_shadows_from_original_geometry: bool = False
	is_shadow_mesh: bool = False
	is_player_shadow_mesh: bool = False
