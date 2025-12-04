#!/usr/bin/env python3
#
#  quest.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``quest``).
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
from cp2077_extractor.cr2w.datatypes.base import Chunk
from cp2077_extractor.cr2w.datatypes.game import gameTier3CameraSettings
from cp2077_extractor.cr2w.datatypes.graph import graphGraphNodeDefinition, graphGraphSocketDefinition
from cp2077_extractor.cr2w.datatypes.work import workWorkEntryId

__all__ = [
		"graphIGraphNodeCondition",
		"questAICommandParams",
		"questDisableableNodeDefinition",
		"questFactsDBManagerNodeDefinition",
		"questIBaseCondition",
		"questIConditionType",
		"questIFactsDBManagerNodeType",
		"questISceneConditionType",
		"questITimeConditionType",
		"questNodeDefinition",
		"questPauseConditionNodeDefinition",
		"questRealtimeDelay_ConditionType",
		"questSetVar_NodeType",
		"questSignalStoppingNodeDefinition",
		"questSocketDefinition",
		"questTimeCondition",
		"questTypedCondition",
		"questUseWorkspotParamsV1",
		"questUseWorkspotPlayerParams",
		"scnAICommandFactory",
		]


@dataclass
class scnAICommandFactory(Chunk):
	pass


@dataclass
class questAICommandParams(scnAICommandFactory):
	pass


class graphIGraphNodeCondition(Chunk):
	pass


class questIBaseCondition(graphIGraphNodeCondition):
	pass


@dataclass
class questUseWorkspotPlayerParams(Chunk):
	tier: enums.questUseWorkspotTier = enums.questUseWorkspotTier.Tier3
	camera_settings: gameTier3CameraSettings = field(default_factory=gameTier3CameraSettings)
	empty_hands: bool = False
	camera_use_trajectory_space: bool = True
	apply_camera_params: bool = False
	vehicle_procedural_camera_weight: float = 1.0
	parallax_weight: float = 1.0
	parallax_space: enums.questCameraParallaxSpace = enums.questCameraParallaxSpace.Trajectory


@dataclass
class questUseWorkspotParamsV1(questAICommandParams):
	function: enums.questUseWorkspotNodeFunctions = enums.questUseWorkspotNodeFunctions.UseWorkspot
	workspot_node: str = ''
	teleport: bool = True
	finish_animation: bool = True
	force_entry_anim_name: str = ''
	jump_to_entry: bool = False
	entry_id: workWorkEntryId = field(default_factory=workWorkEntryId)
	entry_tag: str = ''
	change_workspot: bool = True
	enable_idle_mode: bool = False
	exit_entry_id: workWorkEntryId = field(default_factory=workWorkEntryId)
	exit_anim_name: str = ''
	instant: bool = False
	is_workspot_infinite: bool = True
	is_player: bool = False
	player_params: questUseWorkspotPlayerParams = field(
			default_factory=questUseWorkspotPlayerParams
			)  # TODO: new questUseWorkspotPlayerParams { CameraSettings = new gameTier3CameraSettings { YawLeftLimit = 60.000000F, YawRightLimit = 60.000000F, PitchTopLimit = 60.000000F, PitchBottomLimit = 45.000000F, PitchSpeedMultiplier = 1.000000F, YawSpeedMultiplier = 1.000000F }, CameraUseTrajectorySpace = true, VehicleProceduralCameraWeight = 1.000000F, ParallaxWeight = 1.000000F };
	repeat_command_on_interrupt: bool = True
	work_excluded_gestures: list[workWorkEntryId] = field(default_factory=list)
	movement_type: enums.moveMovementType = enums.moveMovementType.Walk
	continue_in_combat: bool = False
	max_anim_time_limit: float = 0.0
	mesh_dissolving_enabled: bool = True
	dangle_reset_simulation: bool = False


@dataclass
class questNodeDefinition(graphGraphNodeDefinition):
	id: int = 0


class questISceneConditionType(Chunk):
	pass


@dataclass
class questDisableableNodeDefinition(questNodeDefinition):
	pass


@dataclass
class questIFactsDBManagerNodeType(Chunk):
	pass


@dataclass
class questFactsDBManagerNodeDefinition(questDisableableNodeDefinition):
	# TODO: Id = sys.maxsize
	type: questIFactsDBManagerNodeType = field(default_factory=questIFactsDBManagerNodeType)


@dataclass
class questSocketDefinition(graphGraphSocketDefinition):
	type: enums.questSocketType = enums.questSocketType.Undefined


@dataclass
class questSetVar_NodeType(questIFactsDBManagerNodeType):
	fact_name: str = ''
	value: int = 1
	set_exact_value: bool = False


@dataclass
class questSignalStoppingNodeDefinition(questDisableableNodeDefinition):
	pass


@dataclass
class questPauseConditionNodeDefinition(questSignalStoppingNodeDefinition):
	# TODO: id = sys.maxsize
	condition: questIBaseCondition = field(default_factory=questIBaseCondition)


@dataclass
class questTypedCondition(questIBaseCondition):
	pass


class questIConditionType(Chunk):
	pass


@dataclass
class questITimeConditionType(questIConditionType):
	pass


@dataclass
class questRealtimeDelay_ConditionType(questITimeConditionType):
	hours: int = 0
	minutes: int = 0
	seconds: int = 0
	miliseconds: int = 0


@dataclass
class questTimeCondition(questTypedCondition):
	type: questITimeConditionType = field(default_factory=questITimeConditionType)
