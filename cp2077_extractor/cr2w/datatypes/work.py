#!/usr/bin/env python3
#
#  work.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``work``).
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

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.anim import animAnimSet, animAnimSetup, animRig
from cp2077_extractor.cr2w.datatypes.base import Chunk, redTagList
from cp2077_extractor.cr2w.datatypes.ent import entEntityTemplate
from cp2077_extractor.cr2w.datatypes.game import gameScriptableComponent

__all__ = [
		"WorkspotEntryData",
		"WorkspotMapData",
		"WorkspotMapperComponent",
		"workIEntry",
		"workIWorkspotItemAction",
		"workTransitionAnim",
		"workWorkEntryId",
		"workWorkspotAnimsetEntry",
		"workWorkspotGlobalProp",
		"workWorkspotItemOverride",
		"workWorkspotItemOverrideItemOverride",
		"workWorkspotItemOverridePropOverride",
		"workWorkspotTree",
		]


@dataclass
class workWorkEntryId(Chunk):
	id: int = sys.maxsize


@dataclass
class workWorkspotItemOverridePropOverride(Chunk):
	prev_item_id: str = ''
	new_item_id: str = ''


@dataclass
class workWorkspotItemOverrideItemOverride(Chunk):
	prev_item_id: int = 0
	new_item_id: int = 0


@dataclass
class workWorkspotItemOverride(Chunk):
	prop_overrides: list[workWorkspotItemOverridePropOverride] = field(default_factory=list)
	item_overrides: list[workWorkspotItemOverrideItemOverride] = field(default_factory=list)


@dataclass
class WorkspotEntryData(Chunk):
	workspot_ref: str = ''
	is_enabled: bool = False
	is_available: bool = False


@dataclass
class WorkspotMapData(Chunk):
	action: enums.gamedataWorkspotActionType = enums.gamedataWorkspotActionType.DeviceInvestigation
	workspots: list[WorkspotEntryData] = field(default_factory=list)


@dataclass
class WorkspotMapperComponent(gameScriptableComponent):
	workspots_map: list[WorkspotMapData] = field(default_factory=list)


@dataclass
class workIWorkspotItemAction(Chunk):
	pass


@dataclass
class workWorkspotGlobalProp(Chunk):
	id: str = ''
	bone_name: str = ''
	prop: entEntityTemplate = field(default_factory=entEntityTemplate)  # CResourceAsyncReference


@dataclass
class workIEntry(Chunk):
	id: workWorkEntryId = field(default_factory=workWorkEntryId)
	flags: int = 0


@dataclass
class workWorkspotAnimsetEntry(Chunk):
	rig: animRig = field(default_factory=animRig)  # TODO: CResourceAsyncReference
	animations: animAnimSetup = field(default_factory=animAnimSetup)
	loading_handles: list[animAnimSet] = field(default_factory=list)  # TODO: CResourceReference


@dataclass
class workTransitionAnim(Chunk):
	idle_a: str = ''
	idle_b: str = ''
	transition_ato_b: str = ''
	transition_bto_a: str = ''


@dataclass
class workWorkspotTree(Chunk):
	workspot_rig: animRig = field(default_factory=animRig)  # TODO: CResourceAsyncReference
	global_props: list[workWorkspotGlobalProp] = field(default_factory=list)
	props_play_sync_anim: bool = False
	root_entry: workIEntry = field(default_factory=workIEntry)
	id_counter: int = 0
	dont_inject_workspot_graph: bool = False
	anim_graph_slot_name: str = "WORKSPOT"
	auto_transition_blend_time: float = 1.0
	initial_actions: list[workIWorkspotItemAction] = field(default_factory=list)
	initial_can_use_exits: bool = True
	blend_out_time: float = 0.0
	final_animsets: list[workWorkspotAnimsetEntry] = field(default_factory=list)
	tags: redTagList = field(default_factory=redTagList)
	items_policy: enums.workWorkspotItemPolicy = enums.workWorkspotItemPolicy.ItemPolicy_SpawnItemOnIdleChange | enums.workWorkspotItemPolicy.ItemPolicy_DespawnItemOnIdleChange | enums.workWorkspotItemPolicy.ItemPolicy_DespawnItemOnReaction  # TODO: CBitField
	censorship_flags: enums.CensorshipFlags = enums.CensorshipFlags.Censor_Nudity  # TODO: CBitField
	custom_transition_anims: list[workTransitionAnim] = field(default_factory=list)
	inertialization_duration_enter: float = 0.5
	inertialization_duration_exit_natural: float = 0.5
	inertialization_duration_exit_forced: float = 0.2
	use_time_limit_for_sequences: bool = False
	freze_at_the_last_frame_use_with_caution: bool = False
	sequences_time_limit: float = 1.0
	snap_to_terrain: bool = False
	unmount_body_carry: bool = True
	status_effect_id: int = 0
	whitelist_visual_tags: redTagList = field(default_factory=redTagList)
	blacklist_visual_tags: redTagList = field(default_factory=redTagList)
