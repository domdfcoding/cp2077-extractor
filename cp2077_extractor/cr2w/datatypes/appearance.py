#!/usr/bin/env python3
#
#  appearance.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``appearance``).
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
import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, Transform, redTagList
from cp2077_extractor.cr2w.datatypes.mesh import CMesh

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.datatypes.ent import (
			entdismembermentEffectResource,
			entdismembermentWoundResource,
			entdismembermentWoundsConfigSet,
			entEntityParametersBuffer,
			entEntityTemplate
			)
	from cp2077_extractor.cr2w.datatypes.game import gameHitRepresentationOverride

__all__ = [
		"appearanceAlternateAppearanceEntry",
		"appearanceAppearanceDefinition",
		"appearanceAppearancePart",
		"appearanceAppearancePartOverrides",
		"appearanceAppearanceResource",
		"appearanceCensorshipEntry",
		"appearanceCookedAppearanceData",
		"appearancePartComponentOverrides",
		]


@dataclass
class appearanceAlternateAppearanceEntry(Chunk):
	original: str = ''
	alternate: str = ''
	alternate_appearance_index: int = 0


@dataclass
class appearanceCensorshipEntry(Chunk):
	original: str = ''
	censored: str = ''
	censor_flags: int = 0


@dataclass
class appearancePartComponentOverrides(Chunk):
	component_name: str = ''
	mesh_appearance: str = "default"
	chunk_mask: int = sys.maxsize
	use_custom_transform: bool = False
	initial_transform: Transform = field(default_factory=Transform)
	visual_scale: tuple[float, float, float] = (0.0, 0.0, 0.0)
	accept_dismemberment: bool = True


@dataclass
class appearanceCookedAppearanceData(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	dependencies: list[Chunk] = field(default_factory=list)  # TODO: CResourceReference
	total_size_on_disk: int = 0


@dataclass
class appearanceAppearancePart(Chunk):
	resource: "entEntityTemplate" = field(
			default_factory=lambda: entEntityTemplate()
			)  # TODO: resolve default class (circular import)  # TODO: CResourceAsyncReference


@dataclass
class appearanceAppearancePartOverrides(Chunk):
	part_resource: "entEntityTemplate" = field(
			default_factory=lambda: entEntityTemplate()
			)  # TODO: resolve default class (circular import)    # TODO: CResourceAsyncReference
	components_overrides: list[appearancePartComponentOverrides] = field(default_factory=list)


@dataclass
class appearanceAppearanceDefinition(Chunk):
	name: str = ''
	parent_appearance: str = ''
	parts_masks: list[list[str]] = field(default_factory=list)
	parts_values: list[appearanceAppearancePart] = field(default_factory=list)
	parts_overrides: list[appearanceAppearancePartOverrides] = field(default_factory=list)
	proxy_mesh: CMesh = field(default_factory=CMesh)  # TODO: CResourceAsyncReference
	forced_lod_distance: int = 0
	proxy_mesh_appearance: str = ''
	cooked_data_path_override: Chunk = field(default_factory=Chunk)  # TODO: CResourceAsyncReference
	parameters_buffer: "entEntityParametersBuffer" = field(
			default_factory=lambda: entEntityParametersBuffer()
			)  # TODO: resolve default class (circular import)
	visual_tags: redTagList = field(default_factory=redTagList)
	inherited_visual_tags: redTagList = field(default_factory=redTagList)
	hit_representation_overrides: list["gameHitRepresentationOverride"] = field(default_factory=list)
	compiled_data: Any = None  # TODO: SerializationDeferredDataBuffer = field(default_factory=SerializationDeferredDataBuffer)
	resolved_dependencies: list[Chunk] = field(default_factory=list)  # TODO: CResourceAsyncReference
	loose_dependencies: list[Chunk] = field(default_factory=list)  # TODO: CResourceAsyncReference
	censor_flags: int = 0


class appearanceAppearanceResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	alternate_appearance_setting_name: str = ''
	alternate_appearance_suffixes: list[str] = field(default_factory=list)
	alternate_appearance_mapping: list[appearanceAlternateAppearanceEntry] = field(default_factory=list)
	censorship_mapping: list[appearanceCensorshipEntry] = field(default_factory=list)
	wounds: list["entdismembermentWoundResource"] = field(default_factory=list)
	dism_effects: list["entdismembermentEffectResource"] = field(default_factory=list)
	dism_wound_config: "entdismembermentWoundsConfigSet" = field(
			default_factory=lambda: entdismembermentWoundsConfigSet()
			)  # TODO: resolve default class (circular import)
	base_type: str = ''
	base_entity_type: str = ''
	base_entity: "entEntityTemplate" = field(
			default_factory=lambda: entEntityTemplate()
			)  # TODO: resolve default class (circular import)   # TODO: CResourceAsyncReference
	part_type: str = ''
	preset: str = ''
	appearances: list[appearanceAppearanceDefinition] = field(default_factory=list)
	common_cook_data: appearanceCookedAppearanceData = field(
			default_factory=appearanceCookedAppearanceData
			)  # TODO: CResourceAsyncReference
	proxy_poly_count: int = 1400
	force_compile_proxy: bool = False
	generate_player_blocking_collision_for_proxy: bool = False
