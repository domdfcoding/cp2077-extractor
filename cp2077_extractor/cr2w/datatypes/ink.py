#!/usr/bin/env python3
#
#  ink.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``ink``).
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
from cp2077_extractor.cr2w.datatypes.base import Chunk

__all__ = [
		"CursorRootController",
		"GamepadCursorRootController",
		"HDRColor",
		"inkCreditsResource",
		"inkCreditsSectionEntry",
		"inkIEffect",
		"inkIWidgetController",
		"inkIWidgetLogicController",
		"inkMargin",
		"inkPropertyBinding",
		"inkPropertyManager",
		"inkStyle",
		"inkStyleOverride",
		"inkStyleProperty",
		"inkStyleResource",
		"inkStyleResourceWrapper",
		"inkStyleTheme",
		"inkUITransform",
		"inkUserData",
		"inkWidget",
		"inkWidgetLayout",
		"inkWidgetLogicController",
		"inkWidgetReference",
		"inkanimDefinition",
		"inkanimEvent",
		"inkanimInterpolator",
		"inkanimProxy",
		]


@dataclass
class HDRColor(Chunk):
	red: float = 0.0
	green: float = 0.0
	blue: float = 0.0
	alpha: float = 0.0


class inkanimProxy(Chunk):
	pass


@dataclass
class inkMargin(Chunk):
	left: float = 0.0
	top: float = 0.0
	right: float = 0.0
	bottom: float = 0.0


@dataclass
class inkanimEvent(Chunk):
	start_time: float = 0.0


@dataclass
class inkUITransform(Chunk):
	translation: tuple[float, float] = (0.0, 0.0)
	scale: tuple[float, float] = (1.0, 1.0)
	shear: tuple[float, float] = (0.0, 0.0)
	rotation: float = 0.0


@dataclass
class inkIEffect(Chunk):
	is_enabled: bool = False
	effect_name: str = ''


@dataclass
class inkIWidgetLogicController(Chunk):
	audio_metadata_name: str = ''


@dataclass
class inkWidgetLogicController(inkIWidgetLogicController):
	pass


@dataclass
class inkCreditsSectionEntry(Chunk):
	"""
	A section in the game credits.
	"""

	#: The names to credit.
	names: list[bytes]

	display_mode: enums.inkDisplayMode

	#: A heading (e.g. "Programming") or a role title (e.g. "Senior Programmer")
	section_title: str = ''


@dataclass
class inkCreditsResource(Chunk):
	"""
	Data for the game's credits.
	"""

	cooking_platform: enums.ECookingPlatform
	sections: list[inkCreditsSectionEntry]


@dataclass
class inkanimInterpolator(Chunk):
	interpolation_mode: enums.inkanimInterpolationMode = enums.inkanimInterpolationMode.EasyIn
	interpolation_type: enums.inkanimInterpolationType = enums.inkanimInterpolationType.Linear
	interpolation_direction: enums.inkanimInterpolationDirection = enums.inkanimInterpolationDirection.To
	duration: float = 0.0
	start_delay: float = 0.0
	use_relative_duration: bool = False
	is_additive: bool = False


@dataclass
class inkanimDefinition(Chunk):
	interpolators: list[inkanimInterpolator] = field(default_factory=list)
	events: list[inkanimEvent] = field(default_factory=list)


@dataclass
class inkWidgetLayout(Chunk):
	padding: inkMargin = field(default_factory=inkMargin)
	margin: inkMargin = field(default_factory=inkMargin)
	halign: enums.inkEHorizontalAlign = enums.inkEHorizontalAlign.Fill
	valign: enums.inkEVerticalAlign = enums.inkEVerticalAlign.Fill
	anchor: enums.inkEAnchor = enums.inkEAnchor.TopLeft
	anchor_point: tuple[float, float] = (0.0, 0.0)
	size_rule: enums.inkESizeRule = enums.inkESizeRule.Fixed
	size_coefficient: float = 1.0


class inkUserData(Chunk):
	pass


@dataclass
class inkPropertyBinding(Chunk):
	property_name: str = ''
	style_path: str = ''


@dataclass
class inkStyleProperty(Chunk):
	property_path: str = ''
	value: Any = None  # TODO: CVariant = field(default_factory=CVariant)


@dataclass
class inkStyle(Chunk):
	style_id: str = ''
	state: str = ''
	properties: list[inkStyleProperty] = field(default_factory=list)


@dataclass
class inkStyleResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	styles: list[inkStyle] = field(default_factory=list)
	style_imports: list["inkStyleResource"] = field(default_factory=list)  # TODO: CResourceReference
	themes: list["inkStyleTheme"] = field(default_factory=list)
	overrides: list["inkStyleOverride"] = field(default_factory=list)
	hide_in_inheriting_styles: bool = False


@dataclass
class inkStyleOverride(Chunk):
	override_type: enums.inkStyleOverrideType = enums.inkStyleOverrideType.Invalid
	style_resource: inkStyleResource = field(default_factory=inkStyleResource)  # TODO: CResourceReference


@dataclass
class inkStyleTheme(Chunk):
	theme_id: str = ''
	style_resource: inkStyleResource = field(default_factory=inkStyleResource)  # TODO: CResourceReference


@dataclass
class inkStyleResourceWrapper(Chunk):
	style_resource: inkStyleResource = field(default_factory=inkStyleResource)  # TODO: CResourceAsyncReference


@dataclass
class inkPropertyManager(Chunk):
	bindings: list[inkPropertyBinding] = field(default_factory=list)


@dataclass
class inkWidget(Chunk):
	logic_controller: inkWidgetLogicController = field(default_factory=inkWidgetLogicController)
	secondary_controllers: list[inkWidgetLogicController] = field(default_factory=list)
	user_data: list[inkUserData] = field(default_factory=list)
	name: str = "UNINITIALIZED_WIDGET"
	state: str = "Default"
	visible: bool = True
	affects_layout_when_hidden: bool = False
	is_interactive: bool = False
	can_support_focus: bool = False
	style: inkStyleResourceWrapper = field(default_factory=inkStyleResourceWrapper)
	parent_widget: "inkWidget" = field(default_factory=lambda: inkWidget())
	property_manager: inkPropertyManager = field(default_factory=inkPropertyManager)
	fit_to_content: bool = False
	layout: inkWidgetLayout = field(default_factory=inkWidgetLayout)
	opacity: float = 1.0
	tint_color: HDRColor = field(default_factory=lambda: HDRColor(1.0, 1.0, 1.0, 1.0))
	size: tuple[float, float] = (0.0, 0.0)
	render_transform_pivot: tuple[float, float] = (0.5, 0.5)
	render_transform: inkUITransform = field(default_factory=inkUITransform)
	effects: list[inkIEffect] = field(default_factory=list)


@dataclass
class inkWidgetReference(Chunk):
	widget: inkWidget = field(default_factory=inkWidget)


@dataclass
class CursorRootController(inkWidgetLogicController):
	main_cursor: inkWidgetReference = field(default_factory=inkWidgetReference)
	cursor_pattern: inkWidgetReference = field(default_factory=inkWidgetReference)
	progress_bar: inkWidgetReference = field(default_factory=inkWidgetReference)
	progress_bar_frame: inkWidgetReference = field(default_factory=inkWidgetReference)
	anim_proxy: inkanimProxy = field(default_factory=inkanimProxy)


@dataclass
class GamepadCursorRootController(CursorRootController):
	pass


@dataclass
class inkIWidgetController(Chunk):
	audio_metadata_name: str = ''
