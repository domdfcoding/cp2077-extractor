#!/usr/bin/env python3
#
#  ent.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``ent``).
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
from dataclasses import dataclass

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, redTagList

__all__ = [
		"entIBinding",
		"entTagMask",
		"entTemplateBindingOverride",
		"entTemplateComponentBackendDataOverrideInfo",
		"entTemplateComponentResolveSettings",
		"entVisualTagsSchema"
		]


@dataclass
class entVisualTagsSchema(Chunk):  # noqa: D101
	visual_tags: redTagList
	schema: str


@dataclass
class entTemplateComponentResolveSettings(Chunk):  # noqa: D101
	component_name: str
	name_param: str
	mode: enums.entTemplateComponentResolveMode


@dataclass
class entTagMask(Chunk):  # noqa: D101
	hard_tags: redTagList
	soft_tags: redTagList
	excluded_tags: redTagList


@dataclass
class entIBinding(Chunk):  # noqa: D101
	enabled: bool
	enable_mask: entTagMask
	bind_name: str


@dataclass
class entTemplateBindingOverride(Chunk):  # noqa: D101
	component_name: str
	property_name: str
	binding: entIBinding


@dataclass
class entTemplateComponentBackendDataOverrideInfo(Chunk):  # noqa: D101
	component_name: str
	offset: tuple[int, int]


# @dataclass
# class entTemplateInclude(Chunk):
# 	name: str
# 	template: Any  # CResourceAsyncReference<entEntityTemplate>

# @dataclass
# class entTemplateAppearance(Chunk):
# 	name: str
# 	appearance_resource: Any  # CResourceAsyncReference<appearanceAppearanceResource>
# 	appearance_name: str

# @dataclass
# class entEntityTemplate(Chunk):
# 	cooking_platform: enums.ECookingPlatform
# 	includes: list[entTemplateInclude]
# 	appearances: list[entTemplateAppearance]
# 	default_appearance: str
# 	visual_tags_schema: entVisualTagsSchema
# 	component_resolve_settings: list[entTemplateComponentResolveSettings]
# 	binding_overrides: list[entTemplateBindingOverride]
# 	backend_data_overrides: list[entTemplateComponentBackendDataOverrideInfo]
# 	local_data: Any  # DataBuffer
# 	include_instance_buffer: Any  # DataBuffer
# 	compiled_data: Any  # DataBuffer
# 	resolved_dependencies: list[Any]  # list[CResourceAsyncReference<CResource>]
# 	inplace_resources: list[Any]  # list[CResourceReference<CResource>]
# 	compiled_entity_lod_flags: int
