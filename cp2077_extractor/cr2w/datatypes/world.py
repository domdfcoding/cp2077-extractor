#!/usr/bin/env python3
#
#  world.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``world``).
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
from cp2077_extractor.cr2w.datatypes.base import Chunk, Quaternion

__all__ = ["worldCompiledEffectEventInfo", "worldCompiledEffectInfo", "worldCompiledEffectPlacementInfo"]


@dataclass
class worldCompiledEffectPlacementInfo(Chunk):
	placement_tag_index: int = 255
	relative_position_index: int = 255
	relative_rotation_index: int = 255
	flags: int = 0


@dataclass
class worldCompiledEffectEventInfo(Chunk):
	event_ruid: int = 0
	placement_index_mask: int = 0
	component_index_mask: int = 0
	flags: int = 1


@dataclass
class worldCompiledEffectInfo(Chunk):
	placement_tags: list[str] = field(default_factory=list)
	component_names: list[str] = field(default_factory=list)
	relative_positions: list[tuple[float, float, float]] = field(default_factory=list)
	relative_rotations: list[Quaternion] = field(default_factory=list)
	placement_infos: list[worldCompiledEffectPlacementInfo] = field(default_factory=list)
	events_sorted_by_ruid: list[worldCompiledEffectEventInfo] = field(default_factory=list)
