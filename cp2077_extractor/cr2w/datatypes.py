#!/usr/bin/env python3
#
#  datatypes.py
"""
Classes to represent datatypes within CR2W/W2RC files.
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
import functools
import inspect
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypedDict, cast

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.utils import get_array_variables, get_chunk_variables
from cp2077_extractor.utils import StringReader, to_snake_case

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.io import ParsingData

__all__ = [
		"Array",
		"CBitmapTexture",
		"Chunk",
		"DeferredBufferData",
		"HandleData",
		"Quaternion",
		"STextureGroupSetup",
		"Transform",
		"entIBinding",
		"entTagMask",
		"entTemplateBindingOverride",
		"entTemplateComponentBackendDataOverrideInfo",
		"entTemplateComponentResolveSettings",
		"entVisualTagsSchema",
		"gameEntityReference",
		"handle",
		"inkCreditsResource",
		"inkCreditsSectionEntry",
		"instantiate_type",
		"lookup_type",
		"parse_array",
		"parse_chunk",
		"parse_handle_array",
		"parse_string",
		"parse_string_array",
		"redTagList",
		"rendRenderTextureBlobHeader",
		"rendRenderTextureBlobMemoryLayout",
		"rendRenderTextureBlobMipMapInfo",
		"rendRenderTextureBlobPC",
		"rendRenderTextureBlobPlacement",
		"rendRenderTextureBlobSizeInfo",
		"rendRenderTextureBlobTextureInfo",
		"rendRenderTextureResource",
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
		"scnscreenplayStore",
		"serialization_deferred_data_buffer",
		"worldCompiledEffectEventInfo",
		"worldCompiledEffectInfo",
		"worldCompiledEffectPlacementInfo",
		]

_red_type_lookup: dict[bytes, type | Callable[..., object]] = {}

_red_enum_list = enums.__all__[:]
_red_enum_list.remove("REDEnum")
for _class_name in _red_enum_list:
	_red_type_lookup[_class_name.encode("UTF-8")] = getattr(enums, _class_name)


class Chunk:
	"""
	Base class for chunks in CR2W/W2RC files; packed data containing variable names, types and values.
	"""

	def __init_subclass__(cls, *args, **kwargs):
		_red_type_lookup[cls.__name__.encode("UTF-8")] = cls

	@classmethod
	def from_cr2w_kwargs(cls, kwargs: dict[bytes, Any]) -> "Chunk":
		"""
		Construct from a mapping of REDengine variable names and values (as Python types).
		"""
		new_kwargs: dict[str, Any] = {
				to_snake_case(arg_name.decode("UTF-8")): arg_value
				for arg_name, arg_value in kwargs.items()
				}
		return cls(**new_kwargs)

	@classmethod
	def from_chunk(cls, chunk: bytes, parsing_data: "ParsingData") -> "Chunk":
		"""
		Parse raw bytes.

		:param chunk: The raw bytes.
		:param parsing_data:
		"""

		kwargs = parse_chunk(chunk, parsing_data)
		return cls.from_cr2w_kwargs(kwargs)


@dataclass
class Array:
	"""
	Type of an array in a CR2W/W2RC file, with the name of the inner type.
	"""

	value_red_type_name: bytes

	def __call__(self, value: bytes, parsing_data: "ParsingData") -> list:
		"""
		Convert ``value`` (representing an array) into a Python list.

		:param value:
		:param parsing_data:
		"""

		array_value_type = lookup_type(self.value_red_type_name)
		if inspect.isclass(array_value_type) and issubclass(array_value_type, Chunk):
			return [array_value_type.from_cr2w_kwargs(av) for av in parse_array(value, parsing_data)]
		elif self.value_red_type_name == b"String":
			return parse_string_array(value)
		elif self.value_red_type_name.startswith(b"handle:"):
			return parse_handle_array(value, parsing_data)
		else:
			raise NotImplementedError(array_value_type)


# def uint(value: bytes) -> int:
# 	return int.from_bytes(value, byteorder="little")

uint = functools.partial(int.from_bytes, byteorder="little")


def lookup_type(red_type_name: bytes) -> type | Callable[..., object]:
	"""
	Lookup a Python type from its REDengine equivalent's name.

	:param red_type_name:
	"""

	if red_type_name in _red_type_lookup:
		# print("Looked up", red_type_name, "as", _red_type_lookup[red_type_name])
		return _red_type_lookup[red_type_name]
	elif red_type_name.startswith(b"array:"):
		return Array(red_type_name.split(b":", 1)[1])
	elif red_type_name.startswith(b"handle:"):
		return handle
	else:
		raise NotImplementedError(red_type_name)


def parse_chunk(chunk: bytes, parsing_data: "ParsingData") -> dict[bytes, Any]:
	"""
	Parse the given chunk of data and return a mapping of variable names to values.

	:param chunk:
	:param parsing_data:
	"""

	variables = get_chunk_variables(chunk, parsing_data.names_list)

	kwargs: dict[bytes, Any] = {}
	for (var_c_name, red_type_name, value) in variables:
		kwargs[var_c_name] = instantiate_type(red_type_name, value, parsing_data)

	return kwargs


def parse_array(chunk: bytes, parsing_data: "ParsingData") -> list[dict[bytes, str]]:
	"""
	Parse the given chunk of data as an array and return a list of mapping of variable names to values.

	:param chunk:
	:param parsing_data:
	"""

	variables = get_array_variables(chunk, parsing_data.names_list)

	array_contents = []
	for array_item in variables:

		kwargs: dict[bytes, Any] = {}
		for (var_c_name, red_type_name, value) in array_item:
			kwargs[var_c_name] = instantiate_type(red_type_name, value, parsing_data)

		array_contents.append(kwargs)

	return array_contents


def instantiate_type(red_type_name: bytes, value: bytes, parsing_data: "ParsingData") -> object:
	"""
	Create a Python class instance for the given REDengine type and the given value.

	:param red_type_name:
	:param value:
	:param parsing_data:
	"""

	# this package
	from cp2077_extractor.cr2w.io import read_c_name

	if red_type_name == b"CName":
		return read_c_name(BytesIO(value), parsing_data.names_list)

	var_type = lookup_type(red_type_name)

	if inspect.isclass(var_type) and issubclass(var_type, enums.REDEnum):
		return var_type.from_red_name(parsing_data.names_list[uint(value)])
	elif var_type is Chunk:
		return (red_type_name, parse_chunk(value, parsing_data))
	elif isinstance(var_type, Array):
		return var_type(value, parsing_data)
	elif inspect.isclass(var_type) and issubclass(var_type, Chunk):
		return var_type.from_chunk(value, parsing_data)
	elif var_type in {handle, serialization_deferred_data_buffer}:
		return var_type(value, parsing_data)
	else:
		return var_type(value)


class HandleData(TypedDict):
	"""
	Return type of :func:`~.handle`.
	"""

	handle_id: int
	data: Chunk


def handle(handle: bytes, parsing_data: "ParsingData") -> HandleData:
	"""
	A handle points to the data in another chunk. Read that chunk and return the resulting data.

	:param handle: Raw bytes of the handle (the value of a ``handle:xxxxxx`` type), referring to the target chunk.
	:param parsing_data:
	"""

	handle_idx = int.from_bytes(handle, "little") - 1
	chunk = parsing_data.chunks[handle_idx]
	return {"handle_id": handle_idx, "data": cast(Chunk, instantiate_type(chunk[1], chunk[0], parsing_data))}


class DeferredBufferData(TypedDict):
	"""
	Return type of :func:`~.serialization_deferred_data_buffer`.
	"""

	buffer_id: int
	flags: int
	bytes: bytes


def serialization_deferred_data_buffer(
		buffer_id: bytes,
		parsing_data: "ParsingData",
		) -> DeferredBufferData:
	"""
	A ``serializationDeferredDataBuffer`` points to a buffer in the CR2W/W2RC file, containing the actual data e.g. a texture.

	:param buffer_id: The ID of the buffer. Unknown format. Currently ignored and assumed to point to the first buffer.
	:param parsing_data:
	"""

	# TODO: Two bytes. With one buffer it's 1 0.
	assert buffer_id == b"\1\0"
	buffer_idx = 0  # TODO: proper lookup implementation
	buffer, buffer_info = parsing_data.buffers[buffer_idx]
	return {"buffer_id": buffer_idx, "flags": buffer_info.flags, "bytes": buffer}


@dataclass
class scnPerformerId(Chunk):
	id: int = 4294967040


@dataclass
class gameEntityReference(Chunk):
	type: enums.gameEntityReferenceType = enums.gameEntityReferenceType.EntityRef
	reference: str = ''
	names: list[str] = field(default_factory=list)
	slot_name: str = ''
	scene_actor_context_name: str = ''
	dynamic_entity_unique_name: str = ''


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
class Quaternion(Chunk):
	i: float
	j: float
	k: float
	r: float


@dataclass
class Transform(Chunk):
	position: tuple[int, int, int, int]
	orientation: Quaternion


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
class rendRenderTextureBlobTextureInfo(Chunk):  # noqa: D101
	texture_data_size: int
	slice_size: int
	data_alignment: int
	slice_count: int
	mip_count: int
	type: enums.GpuWrapApieTextureType = enums.GpuWrapApieTextureType.TEXTYPE_2D


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


@dataclass
class rendRenderTextureBlobSizeInfo(Chunk):
	"""
	Size info for a texture.
	"""

	width: int
	height: int
	depth: int = 1


@dataclass
class rendRenderTextureBlobHeader(Chunk):
	"""
	Header for texture data and associated properties.
	"""

	version: int
	size_info: rendRenderTextureBlobSizeInfo
	texture_info: rendRenderTextureBlobTextureInfo
	flags: int
	mip_map_info: list[Any] = field(default_factory=list)  # list[MipMapInfo]  # TODO: parse array
	histogram_data: list[Any] = field(default_factory=list)  # list[HistogramData]


@dataclass
class rendRenderTextureBlobPC(Chunk):  # noqa: D101
	header: rendRenderTextureBlobHeader
	texture_data: DeferredBufferData


@dataclass
class STextureGroupSetup(Chunk):
	"""
	Properties of a texture file.
	"""

	compression: enums.ETextureCompression
	is_gamma: bool = False
	platform_mip_bias_pc: int = 0
	platform_mip_bias_console: int = 0
	is_streamable: bool = True
	has_mipchain: bool = True
	allow_texture_downgrade: bool = True
	group: enums.GpuWrapApieTextureGroup = enums.GpuWrapApieTextureGroup.TEXG_Generic_Color
	raw_format: enums.ETextureRawFormat = enums.ETextureRawFormat.TRF_TrueColor


@dataclass
class rendRenderTextureResource(Chunk):  # noqa: D101
	render_resource_blob_pc: HandleData  # CHandle


@dataclass
class CBitmapTexture(Chunk):
	"""
	A texture file.
	"""

	cooking_platform: enums.ECookingPlatform
	width: int
	height: int
	# render_resource_blob: Any  # RenderResourceBlob  # TODO: check resolved type
	render_texture_resource: rendRenderTextureResource  # TODO: default is new rendRenderTextureResource
	setup: STextureGroupSetup = field(default_factory=STextureGroupSetup)  # type: ignore[arg-type]
	depth: int = 1
	hist_bias_mul_coef: tuple[float, float, float] = (1.0, 1.0, 1.0)  # Vector3
	hist_bias_add_coef: tuple[float, float, float] = (0.0, 0.0, 0.0)  # Vector3


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
class rendRenderTextureBlobMemoryLayout(Chunk):  # noqa: D101
	row_pitch: int = 0
	slice_pitch: int = 0


@dataclass
class rendRenderTextureBlobPlacement(Chunk):  # noqa: D101
	size: int = 0
	offset: int = 0


@dataclass
class rendRenderTextureBlobMipMapInfo(Chunk):  # noqa: D101
	layout: rendRenderTextureBlobMemoryLayout = field(default_factory=rendRenderTextureBlobMemoryLayout)
	placement: rendRenderTextureBlobPlacement = field(default_factory=rendRenderTextureBlobPlacement)


@dataclass
class redTagList(Chunk):  # noqa: D101
	tags: list[str]


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


def parse_string(data: bytes) -> str:
	"""
	Parse a bytes string (which has a VLQ i32 size prefix) to a Python string.

	:param
	"""

	return StringReader(data).parse_string()


def parse_string_array(data: bytes) -> list[str]:
	"""
	Parse an array of strings.

	:param data:
	"""

	array_size = int.from_bytes(data[:4], "little")
	string_reader = StringReader(data[4:])
	return [string_reader.parse_string() for _ in range(array_size)]


def parse_handle_array(data: bytes, parsing_data: "ParsingData") -> list[HandleData]:
	"""
	Parse an array of handles (each 4 bytes long).

	:param data:
	"""

	array_size = int.from_bytes(data[:4], "little")
	array = [handle(data[4 + (4 * idx):8 + (4 * idx)], parsing_data) for idx in range(array_size)]
	return array


_red_type_lookup.update({
		# b"DataBuffer": bytes,  # TODO
		b"Bool": bool,
		b"String": parse_string,
		b"Uint16": uint,
		b"Uint32": uint,
		b"Uint64": uint,
		b"Uint8": uint,
		b"CRUID": uint,
		b"TweakDBID": uint,
		b"handle": handle,
		b"raRef:animAnimSet": bytes,  # TODO
		b"serializationDeferredDataBuffer": serialization_deferred_data_buffer,
		})
