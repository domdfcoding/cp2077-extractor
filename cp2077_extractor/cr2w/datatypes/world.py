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
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import CColor, Chunk, Quaternion
from cp2077_extractor.cr2w.datatypes.ink import inkIWidgetController

__all__ = [
		"AreaShapeOutline",
		"FixedPoint",
		"IAreaSettings",
		"WorldPosition",
		"WorldRenderAreaSettings",
		"WorldTransform",
		"effectBaseItem",
		"effectLoopData",
		"effectTrackBase",
		"effectTrackGroup",
		"effectTrackItem",
		"worldAreaShapeNode",
		"worldAreaShapeNodeInstance",
		"worldCompiledEffectEventInfo",
		"worldCompiledEffectInfo",
		"worldCompiledEffectPlacementInfo",
		"worldEffect",
		"worldEffectBlackboard",
		"worldIMarker",
		"worldINodeInstance",
		"worldIRuntimeSystem",
		"worldNode",
		"worlduiIWidgetGameController",
		]


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


@dataclass
class FixedPoint(Chunk):
	bits: int = 0


@dataclass
class WorldPosition(Chunk):
	x: FixedPoint = field(default_factory=FixedPoint)
	y: FixedPoint = field(default_factory=FixedPoint)
	z: FixedPoint = field(default_factory=FixedPoint)


@dataclass
class WorldTransform(Chunk):
	position: WorldPosition = field(default_factory=WorldPosition)
	orientation: Quaternion = field(default_factory=Quaternion)


@dataclass
class worldIRuntimeSystem(Chunk):
	pass


@dataclass
class worlduiIWidgetGameController(inkIWidgetController):
	element_record_id: int = 0


class worldIMarker(Chunk):
	pass


@dataclass
class IAreaSettings(Chunk):
	enable: bool = False
	disabled_indexed_properties: int = 0


@dataclass
class WorldRenderAreaSettings(Chunk):
	area_parameters: list[IAreaSettings] = field(default_factory=list)


@dataclass
class worldNode(Chunk):
	# Missing ordinal 0
	# Missing ordinal 1
	is_visible_in_game: bool = True
	is_host_only: bool = False


@dataclass
class AreaShapeOutline(Chunk):
	points: list[tuple[float, float, float]] = field(
			default_factory=lambda: list(((-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)))
			)
	height: float = 2.0


@dataclass
class worldAreaShapeNode(worldNode):
	color: CColor = field(default_factory=CColor)
	outline: AreaShapeOutline = field(default_factory=AreaShapeOutline)


class worldINodeInstance(Chunk):
	pass


@dataclass
class worldAreaShapeNodeInstance(worldINodeInstance):
	pass


class worldEffectBlackboard(Chunk):
	pass


class effectBaseItem(Chunk):
	pass


class effectTrackBase(effectBaseItem):
	pass


@dataclass
class effectTrackGroup(effectTrackBase):
	tracks: list[effectTrackBase] = field(default_factory=list)
	component_name: str = ''


@dataclass
class effectTrackItem(effectBaseItem):
	time_begin: float = 0.0
	time_duration: float = 0.0
	ruid: int = 0


@dataclass
class effectLoopData(Chunk):
	start_time: float = 0.0
	end_time: float = 0.0


@dataclass
class worldEffect(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	name: str = ''
	length: float = 1.0
	input_parameter_names: list[str] = field(default_factory=list)
	track_root: effectTrackGroup = field(default_factory=effectTrackGroup)
	events: list[effectTrackItem] = field(default_factory=list)
	effect_loops: list[effectLoopData] = field(default_factory=list)
