#!/usr/bin/env python3
#
#  scn.py
"""
Classes to represent scenes within CR2W/W2RC files (prefoxed ``scn``).
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
from typing import Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, Transform
from cp2077_extractor.cr2w.datatypes.game import gameEntityReference
from cp2077_extractor.cr2w.datatypes.world import worldCompiledEffectInfo

__all__ = [
		"scnActorDef",
		"scnActorId",
		"scnAdditionalSpeaker",
		"scnAdditionalSpeakers",
		"scnAnimSetAnimNames",
		"scnAnimSetDynAnimNames",
		"scnCheckSpeakersDistanceInterruptCondition",
		"scnCheckSpeakersDistanceInterruptConditionParams",
		"scnCheckSpeakersDistanceReturnCondition",
		"scnCheckSpeakersDistanceReturnConditionParams",
		"scnCinematicAnimSetSRRef",
		"scnCinematicAnimSetSRRefId",
		"scnCommunityParams",
		"scnDebugSymbols",
		"scnDialogLineEvent",
		"scnDialogLineVoParams",
		"scnDynamicAnimSetSRRef",
		"scnDynamicAnimSetSRRefId",
		"scnEffectDef",
		"scnEffectId",
		"scnEffectInstance",
		"scnEffectInstanceId",
		"scnEndNode",
		"scnEntryPoint",
		"scnExecutionTag",
		"scnExecutionTagEntry",
		"scnExitPoint",
		"scnFindEntityInContextParams",
		"scnFindEntityInEntityParams",
		"scnFindEntityInNodeParams",
		"scnFindEntityInWorldParams",
		"scnFindNetworkPlayerParams",
		"scnGameplayAnimSetSRRef",
		"scnGenderMask",
		"scnIInterruptCondition",
		"scnIReturnCondition",
		"scnIScalingData",
		"scnInputSocketId",
		"scnInputSocketStamp",
		"scnInterruptFactConditionType",
		"scnInterruptionScenario",
		"scnInterruptionScenarioId",
		"scnLipsyncAnimSetSRRef",
		"scnLipsyncAnimSetSRRefId",
		"scnLocalMarker",
		"scnMarker",
		"scnNodeId",
		"scnNodeSymbol",
		"scnNotablePoint",
		"scnOutputSocket",
		"scnOutputSocketStamp",
		"scnPerformerId",
		"scnPerformerSymbol",
		"scnPlayerActorDef",
		"scnPropDef",
		"scnPropId",
		"scnPropOwnershipTransferOptions",
		"scnReferencePointDef",
		"scnReferencePointId",
		"scnRidAnimSetSRRef",
		"scnRidAnimSetSRRefId",
		"scnRidAnimationContainerSRRef",
		"scnRidAnimationContainerSRRefAnimContainer",
		"scnRidAnimationContainerSRRefAnimContainerContext",
		"scnRidAnimationSRRef",
		"scnRidAnimationSRRefId",
		"scnRidCameraAnimationSRRef",
		"scnRidCyberwareAnimSetSRRefId",
		"scnRidDeformationAnimSetSRRefId",
		"scnRidFacialAnimSetSRRefId",
		"scnRidResourceHandler",
		"scnRidResourceId",
		"scnRidSerialNumber",
		"scnSRRefCollection",
		"scnSRRefId",
		"scnSceneEvent",
		"scnSceneEventId",
		"scnSceneEventSymbol",
		"scnSceneGraph",
		"scnSceneGraphNode",
		"scnSceneResource",
		"scnSceneSolutionHash",
		"scnSceneSolutionHashHash",
		"scnSceneTime",
		"scnSceneVOInfo",
		"scnSceneWorkspotDataId",
		"scnSceneWorkspotInstanceId",
		"scnSectionInternalsActorBehavior",
		"scnSectionNode",
		"scnSpawnDespawnEntityParams",
		"scnSpawnSetParams",
		"scnSpawnerParams",
		"scnStartNode",
		"scnVoicetagId",
		"scnWorkspotData",
		"scnWorkspotInstance",
		"scnWorkspotSymbol",
		"scnlocLocStoreEmbedded",
		"scnlocLocStoreEmbeddedVariantDescriptorEntry",
		"scnlocLocStoreEmbeddedVariantPayloadEntry",
		"scnlocLocstringId",
		"scnlocSignature",
		"scnlocVariantId",
		"scnscreenplayChoiceOption",
		"scnscreenplayDialogLine",
		"scnscreenplayItemId",
		"scnscreenplayLineUsage",
		"scnscreenplayOptionUsage",
		"scnscreenplayStore"
		]


@dataclass
class scnPerformerId(Chunk):
	id: int = 4294967040


@dataclass
class scnPerformerSymbol(Chunk):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	entity_ref: gameEntityReference = field(default_factory=gameEntityReference)
	editor_performer_id: int = 0


class scnIScalingData(Chunk):
	pass


@dataclass
class scnSceneEventId(Chunk):
	id: int


@dataclass
class scnSceneWorkspotDataId(Chunk):
	id: int


@dataclass
class scnscreenplayItemId(Chunk):
	id: int = 4294967040


@dataclass
class scnInterruptionScenarioId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnlocLocstringId(Chunk):
	ruid: int = 0


@dataclass
class scnRidAnimationSRRefId(Chunk):
	id: int


@dataclass
class scnNodeId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnActorId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnVoicetagId(Chunk):
	id: int


@dataclass
class scnSRRefId(Chunk):
	id: int


@dataclass
class scnSceneWorkspotInstanceId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnCinematicAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnDynamicAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnLipsyncAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnRidCyberwareAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnRidDeformationAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnRidFacialAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnPropId(Chunk):
	id: int


@dataclass
class scnRidAnimSetSRRefId(Chunk):
	id: int


@dataclass
class scnRidResourceId(Chunk):
	id: int


@dataclass
class scnFindNetworkPlayerParams(Chunk):
	network_id: int


@dataclass
class scnEntryPoint(Chunk):
	name: str
	node_id: scnNodeId


@dataclass
class scnExitPoint(Chunk):
	name: str
	node_id: scnNodeId


@dataclass
class scnNotablePoint(Chunk):
	name: str
	node_id: scnNodeId


@dataclass
class scnFindEntityInWorldParams(Chunk):
	actor_ref: gameEntityReference
	force_max_visibility: bool


@dataclass
class scnExecutionTagEntry(Chunk):
	name: str
	flags: int


@dataclass
class scnFindEntityInContextParams(Chunk):
	contextual_name: enums.scnContextualActorName
	voice_vag_id: scnVoicetagId
	spec_record_id: int
	context_actor_name: int = 0
	force_max_visibility: bool = False


@dataclass
class scnSpawnSetParams(Chunk):
	reference: str
	entry_name: str
	force_max_visibility: bool


@dataclass
class scnCommunityParams(Chunk):
	reference: str
	entry_name: str
	force_max_visibility: bool


@dataclass
class scnSpawnerParams(Chunk):
	reference: str
	force_max_visibility: bool


@dataclass
class scnFindEntityInNodeParams(Chunk):
	node_ref: str
	force_max_visibility: bool


@dataclass
class scnSpawnDespawnEntityParams(Chunk):
	dynamic_entity_unique_name: str
	spawn_marker: str
	spawn_marker_type: enums.scnMarkerType
	spawn_marker_node_ref: str
	spawn_offset: Transform
	item_owner_id: scnPerformerId
	spec_record_id: int
	appearance: str
	spawn_on_start: bool
	is_enabled: bool
	validate_spawn_postion: bool
	always_spawned: bool
	keep_alive: bool
	find_in_world: bool
	force_max_visibility: bool
	prefetch_appearance: bool


@dataclass
class scnActorDef(Chunk):
	voicetag_id: scnVoicetagId
	acquisition_plan: enums.scnEntityAcquisitionPlan
	find_actor_in_context_params: scnFindEntityInContextParams
	# find_actor_in_world_params: scnFindEntityInWorldParams
	# spawn_despawn_params: scnSpawnDespawnEntityParams
	# spawn_set_params: scnSpawnSetParams
	# community_params: scnCommunityParams
	# spawner_params: scnSpawnerParams
	actor_name: str
	actor_id: scnActorId
	anim_sets: list[scnSRRefId] = field(default_factory=list)
	lipsync_anim_set: scnLipsyncAnimSetSRRefId = field(
			default_factory=lambda: scnLipsyncAnimSetSRRefId(id=sys.maxsize)
			)
	facial_anim_sets: list[scnRidFacialAnimSetSRRefId] = field(default_factory=list)
	cyberware_anim_sets: list[scnRidCyberwareAnimSetSRRefId] = field(default_factory=list)
	deformation_anim_sets: list[scnRidDeformationAnimSetSRRefId] = field(default_factory=list)
	body_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	facial_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	cyberware_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId] = field(default_factory=list)
	# holocall_init_scn: Any  # TODO: CResourceAsyncReference<CResource>
	spec_character_record_id: int = 0
	spec_appearance: str = "default"


@dataclass
class scnPlayerActorDef(Chunk):
	actor_id: scnActorId
	spec_template: str
	spec_character_record_id: int
	spec_appearance: str
	voicetag_id: scnVoicetagId
	anim_sets: list[scnSRRefId]
	lipsync_anim_set: scnLipsyncAnimSetSRRefId
	facial_anim_sets: list[scnRidFacialAnimSetSRRefId]
	cyberware_anim_sets: list[scnRidCyberwareAnimSetSRRefId]
	deformation_anim_sets: list[scnRidDeformationAnimSetSRRefId]
	body_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId]
	facial_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId]
	cyberware_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId]
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId]
	acquisition_plan: enums.scnEntityAcquisitionPlan
	find_network_player_params: scnFindNetworkPlayerParams
	find_actor_in_context_params: scnFindEntityInContextParams
	player_name: str


@dataclass
class scnInputSocketStamp(Chunk):
	name: int
	ordinal: int


@dataclass
class scnOutputSocketStamp(Chunk):
	name: int
	ordinal: int


@dataclass
class scnInputSocketId(Chunk):
	node_id: scnNodeId
	isock_stamp: scnInputSocketStamp


@dataclass
class scnOutputSocket(Chunk):
	stamp: scnOutputSocketStamp
	destinations: list[scnInputSocketId] = field(default_factory=list)


@dataclass
class scnDialogLineVoParams(Chunk):
	vo_context: enums.locVoiceoverContext = enums.locVoiceoverContext.Vo_Context_Quest
	vo_expression: enums.locVoiceoverExpression = enums.locVoiceoverExpression.Vo_Expression_Spoken
	custom_vo_event: str = ''
	disable_head_movement: bool = False
	is_holocall_speaker: bool = False
	ignore_speaker_incapacitation: bool = False
	always_use_brain_gender: bool = False


@dataclass
class scnAdditionalSpeaker(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	type: enums.scnAdditionalSpeakerType = enums.scnAdditionalSpeakerType.Normal


@dataclass
class scnAdditionalSpeakers(Chunk):
	execution_tag: int = 0
	role: enums.scnAdditionalSpeakerRole = enums.scnAdditionalSpeakerRole.Full
	speakers: list[scnAdditionalSpeaker] = field(default_factory=list)


@dataclass
class scnSceneEvent(Chunk):
	id: scnSceneEventId
	start_time: int = 0
	duration: int = 0
	execution_tag_flags: int = 0
	scaling_data: scnIScalingData = field(default_factory=scnIScalingData)
	# TODO: type: enums.scnEventType = None


@dataclass
class scnDialogLineEvent(scnSceneEvent):
	screenplay_line_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	vo_params: scnDialogLineVoParams = field(default_factory=scnDialogLineVoParams)
	visual_style: enums.scnDialogLineVisualStyle = enums.scnDialogLineVisualStyle.regular
	additional_speakers: scnAdditionalSpeakers = field(default_factory=scnAdditionalSpeakers)


class scnInterruptFactConditionType(Chunk):
	pass


class scnIInterruptCondition(Chunk):
	pass


class scnIReturnCondition(Chunk):
	pass


@dataclass
class scnInterruptionScenario(Chunk):
	id: scnInterruptionScenarioId
	name: str
	queue_name: str = ''
	enabled: bool = True
	talk_on_return: bool = True
	play_interrupt_line: bool = True
	force_play_return_line: bool = False
	interruption_spamming_safeguard: bool = False
	playing_lines_behavior: enums.scnInterruptReturnLinesBehavior = enums.scnInterruptReturnLinesBehavior.Default
	post_interrupt_signal_time_delay: float = 0.0
	post_return_signal_time_delay: float = 0.0
	post_interrupt_signal_fact_condition: scnInterruptFactConditionType = field(
			default_factory=scnInterruptFactConditionType
			)
	post_return_signal_fact_condition: scnInterruptFactConditionType = field(
			default_factory=scnInterruptFactConditionType
			)
	interrupt_conditions: list[scnIInterruptCondition] = field(default_factory=list)
	return_conditions: list[scnIReturnCondition] = field(default_factory=list)


@dataclass
class scnSceneGraphNode(Chunk):
	node_id: scnNodeId
	ff_strategy: enums.scnFastForwardStrategy = enums.scnFastForwardStrategy.automatic
	output_sockets: list[scnOutputSocket] = field(default_factory=list)


@dataclass
class scnStartNode(scnSceneGraphNode):
	pass


@dataclass
class scnEndNode(scnSceneGraphNode):
	type: enums.scnEndNodeNsType = enums.scnEndNodeNsType.Terminating


@dataclass
class scnSceneTime(Chunk):
	stu: int = 0


@dataclass
class scnSectionInternalsActorBehavior(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	behavior_mode: enums.scnSectionInternalsActorBehaviorMode = enums.scnSectionInternalsActorBehaviorMode.OnlyIfAlive


@dataclass
class scnSectionNode(scnSceneGraphNode):
	events: list[scnSceneEvent] = field(default_factory=list)
	section_duration: scnSceneTime = field(default_factory=scnSceneTime)
	actor_behaviors: list[scnSectionInternalsActorBehavior] = field(default_factory=list)
	is_focus_clue: bool = False


@dataclass
class scnSceneGraph(Chunk):
	graph: list[scnSceneGraphNode] = field(default_factory=list)
	start_nodes: list[scnNodeId] = field(default_factory=list)
	end_nodes: list[scnNodeId] = field(default_factory=list)


@dataclass
class scnLocalMarker(Chunk):
	transform_ls: Transform
	name: str


@dataclass
class scnPropOwnershipTransferOptions(Chunk):
	type: enums.scnPropOwnershipTransferOptionsType
	dettach_from_slot: bool
	remove_from_inventory: bool


@dataclass
class scnFindEntityInEntityParams(Chunk):
	actor_id: scnActorId
	performer_id: scnPerformerId
	item_id: int
	slot_id: int
	force_max_visibility: bool
	ownership_transfer_options: scnPropOwnershipTransferOptions


@dataclass
class scnPropDef(Chunk):
	prop_id: scnPropId
	prop_name: str
	spec_prop_record_id: int
	anim_sets: list[scnRidAnimSetSRRefId]
	cinematic_anim_sets: list[scnCinematicAnimSetSRRefId]
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId]
	entity_acquisition_plan: enums.scnEntityAcquisitionPlan
	find_entity_in_entity_params: scnFindEntityInEntityParams
	spawn_despawn_params: scnSpawnDespawnEntityParams
	spawn_set_params: scnSpawnSetParams
	community_params: scnCommunityParams
	spawner_params: scnSpawnerParams
	find_entity_in_node_params: scnFindEntityInNodeParams
	find_entity_in_world_params: scnFindEntityInWorldParams


@dataclass
class scnRidResourceHandler(Chunk):
	id: scnRidResourceId
	rid_resource: Any  # TODO: CResourceReference<scnRidResource>


@dataclass
class scnWorkspotData(Chunk):
	data_d: scnSceneWorkspotDataId


@dataclass
class scnMarker(Chunk):
	type: enums.scnMarkerType = enums.scnMarkerType.Local
	local_marker_id: str = ''
	node_ref: str = ''
	entity_ref: gameEntityReference = field(default_factory=gameEntityReference)
	slot_name: str = ''
	is_mounted: bool = False


@dataclass
class scnWorkspotInstance(Chunk):
	workspot_instance_id: scnSceneWorkspotInstanceId
	data_id: scnSceneWorkspotDataId
	local_transform: Transform
	play_at_actor_location: bool
	origin_marker: scnMarker


@dataclass
class scnRidSerialNumber(Chunk):
	serial_number: int


@dataclass
class scnRidAnimationSRRef(Chunk):
	resource_id: scnRidResourceId
	animation_sn: scnRidSerialNumber


@dataclass
class scnRidAnimSetSRRef(Chunk):
	animations: list[scnSRRefId]


@dataclass
class scnLipsyncAnimSetSRRef(Chunk):
	lipsync_anim_set: Any = None  # TODO: CResourceReference<animAnimSet>
	async_ref_lipsync_anim_set: Any = None  # TODO: CResourceAsyncReference<animAnimSet>


@dataclass
class scnRidCameraAnimationSRRef(Chunk):
	resource_id: scnRidResourceId
	animation_sn: scnRidSerialNumber


@dataclass
class scnCinematicAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: CResourceAsyncReference<animAnimSet>
	priority: int
	is_override: bool


@dataclass
class scnGameplayAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: CResourceAsyncReference<animAnimSet>


@dataclass
class scnDynamicAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: CResourceAsyncReference<animAnimSet>


@dataclass
class scnAnimSetAnimNames(Chunk):
	animation_names: list[str]


@dataclass
class scnGenderMask(Chunk):
	mask: int


@dataclass
class scnRidAnimationContainerSRRefAnimContainerContext(Chunk):
	gender_mask: scnGenderMask


@dataclass
class scnRidAnimationContainerSRRefAnimContainer(Chunk):
	animation: scnRidAnimationSRRefId
	context: scnRidAnimationContainerSRRefAnimContainerContext


@dataclass
class scnRidAnimationContainerSRRef(Chunk):
	animations: list[scnRidAnimationContainerSRRefAnimContainer]


@dataclass
class scnAnimSetDynAnimNames(Chunk):
	anim_variable: str
	anim_names: list[str]


@dataclass
class scnSRRefCollection(Chunk):
	rid_animations: list[scnRidAnimationSRRef] = field(default_factory=list)
	rid_anim_sets: list[scnRidAnimSetSRRef] = field(default_factory=list)
	rid_facial_anim_sets: list[scnRidAnimSetSRRef] = field(default_factory=list)
	rid_cyberware_anim_sets: list[scnRidAnimSetSRRef] = field(default_factory=list)
	rid_deformation_anim_sets: list[scnRidAnimSetSRRef] = field(default_factory=list)
	lipsync_anim_sets: list[scnLipsyncAnimSetSRRef] = field(default_factory=list)
	rid_camera_animations: list[scnRidCameraAnimationSRRef] = field(default_factory=list)
	cinematic_anim_sets: list[scnCinematicAnimSetSRRef] = field(default_factory=list)
	gameplay_anim_sets: list[scnGameplayAnimSetSRRef] = field(default_factory=list)
	dynamic_anim_sets: list[scnDynamicAnimSetSRRef] = field(default_factory=list)
	cinematic_anim_names: list[scnAnimSetAnimNames] = field(default_factory=list)
	gameplay_anim_names: list[scnAnimSetAnimNames] = field(default_factory=list)
	dynamic_anim_names: list[scnAnimSetDynAnimNames] = field(default_factory=list)
	rid_animation_containers: list[scnRidAnimationContainerSRRef] = field(default_factory=list)


@dataclass
class scnscreenplayLineUsage(Chunk):
	player_gender_mask: scnGenderMask


@dataclass
class scnscreenplayOptionUsage(Chunk):
	player_gender_mask: scnGenderMask


@dataclass
class scnscreenplayDialogLine(Chunk):
	item_id: scnscreenplayItemId
	speaker: scnActorId
	addressee: scnActorId
	usage: scnscreenplayLineUsage
	locstring_id: scnlocLocstringId
	male_lipsync_animation_name: str
	female_lipsync_animation_name: str


@dataclass
class scnscreenplayChoiceOption(Chunk):
	item_id: scnscreenplayItemId
	usage: scnscreenplayOptionUsage
	locstring_id: scnlocLocstringId


@dataclass
class scnscreenplayStore(Chunk):
	lines: list[scnscreenplayDialogLine] = field(default_factory=list)
	options: list[scnscreenplayChoiceOption] = field(default_factory=list)


@dataclass
class scnlocVariantId(Chunk):
	ruid: int = 0


@dataclass
class scnlocSignature(Chunk):
	val: int = 0


@dataclass
class scnlocLocStoreEmbeddedVariantDescriptorEntry(Chunk):
	variant_id: scnlocVariantId = field(default_factory=scnlocVariantId)
	locstring_id: scnlocLocstringId = field(default_factory=scnlocLocstringId)
	locale_id: enums.scnlocLocaleId = enums.scnlocLocaleId.db_db
	signature: scnlocSignature = field(default_factory=scnlocSignature)
	vpe_index: int = sys.maxsize


@dataclass
class scnlocLocStoreEmbeddedVariantPayloadEntry(Chunk):
	variant_id: scnlocVariantId
	content: str = ''


@dataclass
class scnlocLocStoreEmbedded(Chunk):
	vd_entries: list[scnlocLocStoreEmbeddedVariantDescriptorEntry] = field(default_factory=list)
	vp_entries: list[scnlocLocStoreEmbeddedVariantPayloadEntry] = field(default_factory=list)


class scnSceneVOInfo(Chunk):
	in_vo_trigger: str
	out_vo_trigger: str
	duration: float
	id: int


@dataclass
class scnWorkspotSymbol(Chunk):
	ws_instance: scnSceneWorkspotInstanceId
	ws_node_id: scnNodeId
	ws_editor_event_id: int = sys.maxsize


@dataclass
class scnSceneEventSymbol(Chunk):
	editor_event_id: int = sys.maxsize
	origin_node_id: scnNodeId = field(default_factory=scnNodeId)
	scene_event_ids: list[scnSceneEventId] = field(default_factory=list)


@dataclass
class scnNodeSymbol(Chunk):
	node_id: scnNodeId
	editor_node_id: scnNodeId
	editor_event_id: int = sys.maxsize


@dataclass
class scnDebugSymbols(Chunk):
	performers_debug_symbols: list[scnPerformerSymbol] = field(default_factory=list)
	workspots_debug_symbols: list[scnWorkspotSymbol] = field(default_factory=list)
	scene_events_debug_symbols: list[scnSceneEventSymbol] = field(default_factory=list)
	scene_nodes_debug_symbols: list[scnNodeSymbol] = field(default_factory=list)


@dataclass
class scnEffectId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnEffectDef(Chunk):
	id: scnEffectId
	effect: Any  # TODO: CResourceAsyncReference<worldEffect>


@dataclass
class scnEffectInstanceId(Chunk):
	effect_id: scnEffectId
	id: int = sys.maxsize


@dataclass
class scnEffectInstance(Chunk):
	effect_instance_id: scnEffectInstanceId
	compiled_effect: worldCompiledEffectInfo


@dataclass
class scnExecutionTag(Chunk):
	flags: int


@dataclass
class scnReferencePointId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnReferencePointDef(Chunk):
	id: scnReferencePointId
	offset: tuple[float, float, float]
	origin_marker: scnMarker = field(
			default_factory=lambda: scnMarker(type=enums.scnMarkerType.Global, is_mounted=True)
			)


@dataclass
class scnSceneSolutionHashHash(Chunk):
	scene_solution_hash_date: int = 0


@dataclass
class scnSceneSolutionHash(Chunk):
	scene_solution_hash: scnSceneSolutionHashHash = field(default_factory=scnSceneSolutionHashHash)


@dataclass
class scnSceneResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	entry_points: list[scnEntryPoint] = field(default_factory=list)
	exit_points: list[scnExitPoint] = field(default_factory=list)
	notable_points: list[scnNotablePoint] = field(default_factory=list)
	execution_tag_entries: list[scnExecutionTagEntry] = field(default_factory=list)
	actors: list[scnActorDef] = field(default_factory=list)
	player_actors: list[scnPlayerActorDef] = field(default_factory=list)
	scene_graph: scnSceneGraph = field(default_factory=scnSceneGraph)
	local_markers: list[scnLocalMarker] = field(default_factory=list)
	props: list[scnPropDef] = field(default_factory=list)
	rid_resources: list[scnRidResourceHandler] = field(default_factory=list)
	workspots: list[scnWorkspotData] = field(default_factory=list)
	workspot_instances: list[scnWorkspotInstance] = field(default_factory=list)
	resoures_references: scnSRRefCollection = field(default_factory=scnSRRefCollection)
	screenplay_store: scnscreenplayStore = field(default_factory=scnscreenplayStore)
	loc_store: scnlocLocStoreEmbedded = field(default_factory=scnlocLocStoreEmbedded)
	version: int = 0
	vo_info: list[scnSceneVOInfo] = field(default_factory=list)
	effect_definitions: list[scnEffectDef] = field(default_factory=list)
	effect_instances: list[scnEffectInstance] = field(default_factory=list)
	execution_tags: list[scnExecutionTag] = field(default_factory=list)
	reference_points: list[scnReferencePointDef] = field(default_factory=list)
	interruption_scenarios: list[scnInterruptionScenario] = field(default_factory=list)
	scene_solution_hash: scnSceneSolutionHash = field(default_factory=scnSceneSolutionHash)
	scene_category_tag: enums.scnSceneCategoryTag = enums.scnSceneCategoryTag.other
	debug_symbols: scnDebugSymbols = field(default_factory=scnDebugSymbols)


@dataclass
class scnCheckSpeakersDistanceInterruptConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnCheckSpeakersDistanceReturnConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnCheckSpeakersDistanceInterruptCondition(Chunk):
	params: scnCheckSpeakersDistanceInterruptConditionParams = field(
			default_factory=scnCheckSpeakersDistanceInterruptConditionParams
			)


@dataclass
class scnCheckSpeakersDistanceReturnCondition(Chunk):
	params: scnCheckSpeakersDistanceReturnConditionParams = field(
			default_factory=scnCheckSpeakersDistanceReturnConditionParams
			)
