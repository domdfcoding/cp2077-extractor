#!/usr/bin/env python3
#
#  physics.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``physics``).
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

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, Quaternion

__all__ = [
		"physicsCustomFilterData",
		"physicsFilterData",
		"physicsMaterialReference",
		"physicsQueryFilter",
		"physicsQueryPreset",
		"physicsRagdollBodyInfo",
		"physicsRagdollBodyNames",
		"physicsSimulationFilter",
		]


@dataclass
class physicsRagdollBodyInfo(Chunk):
	parent_anim_index: int = -1
	child_anim_index: int = -1
	parent_body_index: int = -1
	body_part: enums.physicsRagdollBodyPartE = enums.physicsRagdollBodyPartE.HEAD  # TODO: CBitField
	shape_type: enums.physicsRagdollShapeType = enums.physicsRagdollShapeType.CAPSULE
	shape_radius: float = 0.05
	half_height: float = 0.05
	shape_local_translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
	shape_local_rotation: Quaternion = field(default_factory=Quaternion)
	is_root_displacement_part: bool = False
	swing_angles_y: list[float] = field(default_factory=list)
	swing_angles_z: list[float] = field(default_factory=list)
	twist_angles: list[float] = field(default_factory=list)
	is_stiff: bool = False
	exclude_from_early_collision: bool = False
	filter_data_override: str = ''


@dataclass
class physicsRagdollBodyNames(Chunk):
	parent_anim_name: str = ''
	child_anim_name: str = ''


@dataclass
class physicsQueryPreset(Chunk):
	preset_name: str = ''


@dataclass
class physicsSimulationFilter(Chunk):
	mask1: int = 0
	mask2: int = 0


@dataclass
class physicsCustomFilterData(Chunk):
	collision_type: list[str] = field(default_factory=list)
	collide_with: list[str] = field(default_factory=list)
	query_detect: list[str] = field(default_factory=list)


@dataclass
class physicsMaterialReference(Chunk):
	name: str = ''


@dataclass
class physicsQueryFilter(Chunk):
	mask1: int = 0
	mask2: int = 0


@dataclass
class physicsFilterData(Chunk):
	simulation_filter: physicsSimulationFilter = field(default_factory=physicsSimulationFilter)
	query_filter: physicsQueryFilter = field(default_factory=physicsQueryFilter)
	preset: str = ''
	custom_filter_data: physicsCustomFilterData = field(default_factory=physicsCustomFilterData)
