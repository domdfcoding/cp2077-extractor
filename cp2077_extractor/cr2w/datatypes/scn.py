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
from cp2077_extractor.cr2w.datatypes.anim import (
		animAnimation,
		animAnimEvent,
		animAnimFeature,
		animAnimSet,
		animEventsContainer,
		animFacialEmotionTransitionBaked,
		animIAnimationBuffer,
		animIKTargetRequest,
		animLookAtLimits,
		animLookAtRequestForPart,
		animPoseCorrectionGroup
		)
from cp2077_extractor.cr2w.datatypes.base import Chunk, EulerAngles, HandleData, Quaternion, Transform
from cp2077_extractor.cr2w.datatypes.ent import entVoicesetInputToBlock
from cp2077_extractor.cr2w.datatypes.game import (
		gameComponent,
		gameComponentPS,
		gameEntityReference,
		gameIAttachmentSlotsListener,
		gameinteractionsChoiceTypeWrapper,
		gameinteractionsvisIVisualizerTimeProvider,
		gameISceneSystem,
		gameIStatPoolsListener,
		gameIStatusEffectListener,
		gameObject,
		gamePlayerScriptableSystemRequest,
		gameSceneTierData
		)
from cp2077_extractor.cr2w.datatypes.quest import (
		questIBaseCondition,
		questISceneConditionType,
		questNodeDefinition,
		questUseWorkspotParamsV1
		)
from cp2077_extractor.cr2w.datatypes.work import workWorkEntryId, workWorkspotItemOverride, workWorkspotTree
from cp2077_extractor.cr2w.datatypes.world import WorldRenderAreaSettings, worldCompiledEffectInfo, worldIMarker

__all__ = [
		"scnActorDef",
		"scnActorId",
		"scnActorRid",
		"scnAddIdleAnimEvent",
		"scnAddIdleWithBlendAnimEvent",
		"scnAdditionalSpeaker",
		"scnAdditionalSpeakers",
		"scnAndNode",
		"scnAnimName",
		"scnAnimSetAnimNames",
		"scnAnimSetDynAnimNames",
		"scnAnimTargetBasicData",
		"scnAnimationMotionSample",
		"scnAnimationRid",
		"scnAnimationRidAudioData",
		"scnAudioDurationEvent",
		"scnAudioEvent",
		"scnBluelineSelectedRequest",
		"scnBraindanceJumpInProgress_ConditionType",
		"scnBraindanceLayer_ConditionType",
		"scnBraindancePaused_ConditionType",
		"scnBraindancePerspective_ConditionType",
		"scnBraindancePlaying_ConditionType",
		"scnBraindanceResetting_ConditionType",
		"scnBraindanceRewinding_ConditionType",
		"scnCameraAnimationLOD",
		"scnCameraAnimationRid",
		"scnCameraRid",
		"scnChangeIdleAnimEvent",
		"scnChatter",
		"scnChatterModuleSharedState",
		"scnCheckAnyoneDistractedInterruptCondition",
		"scnCheckDistractedReturnCondition",
		"scnCheckDistractedReturnConditionParams",
		"scnCheckFactInterruptCondition",
		"scnCheckFactInterruptConditionParams",
		"scnCheckFactReturnCondition",
		"scnCheckFactReturnConditionParams",
		"scnCheckMountedVehicleImpactInterruptCondition",
		"scnCheckPlayerCombatInterruptCondition",
		"scnCheckPlayerCombatInterruptConditionParams",
		"scnCheckPlayerCombatReturnCondition",
		"scnCheckPlayerCombatReturnConditionParams",
		"scnCheckPlayerTargetEntityDistanceInterruptCondition",
		"scnCheckPlayerTargetEntityDistanceInterruptConditionParams",
		"scnCheckPlayerTargetEntityDistanceReturnCondition",
		"scnCheckPlayerTargetEntityDistanceReturnConditionParams",
		"scnCheckPlayerTargetNodeDistanceInterruptCondition",
		"scnCheckPlayerTargetNodeDistanceInterruptConditionParams",
		"scnCheckPlayerTargetNodeDistanceReturnCondition",
		"scnCheckPlayerTargetNodeDistanceReturnConditionParams",
		"scnCheckSpeakerDistractedInterruptCondition",
		"scnCheckSpeakerOrAddressDistractedInterruptCondition",
		"scnCheckSpeakersDistanceInterruptCondition",
		"scnCheckSpeakersDistanceInterruptConditionParams",
		"scnCheckSpeakersDistanceReturnCondition",
		"scnCheckSpeakersDistanceReturnConditionParams",
		"scnCheckTriggerInterruptCondition",
		"scnCheckTriggerInterruptConditionParams",
		"scnCheckTriggerReturnCondition",
		"scnCheckTriggerReturnConditionParams",
		"scnChoiceHubPartId",
		"scnChoiceNode",
		"scnChoiceNodeNsActorReminderParams",
		"scnChoiceNodeNsAdaptiveLookAtParams",
		"scnChoiceNodeNsAdaptiveLookAtReferencePoint",
		"scnChoiceNodeNsAttachToActorParams",
		"scnChoiceNodeNsAttachToGameObjectParams",
		"scnChoiceNodeNsAttachToPropParams",
		"scnChoiceNodeNsAttachToScreenParams",
		"scnChoiceNodeNsAttachToWorldParams",
		"scnChoiceNodeNsBasicLookAtParams",
		"scnChoiceNodeNsDeprecatedParams",
		"scnChoiceNodeNsLookAtParams",
		"scnChoiceNodeNsMappinParams",
		"scnChoiceNodeNsReminderParams",
		"scnChoiceNodeNsTimedParams",
		"scnChoiceNodeOption",
		"scnCinematicAnimSetSRRef",
		"scnCinematicAnimSetSRRefId",
		"scnCommunityParams",
		"scnCutControlNode",
		"scnDebugSymbols",
		"scnDeletionMarkerNode",
		"scnDialogDisplayString",
		"scnDialogLineData",
		"scnDialogLineDuplicationParams",
		"scnDialogLineEvent",
		"scnDialogLineVoParams",
		"scnDummyAlwaysTrueReturnCondition",
		"scnDynamicAnimSetSRRef",
		"scnDynamicAnimSetSRRefId",
		"scnEffectDef",
		"scnEffectEntry",
		"scnEffectId",
		"scnEffectInstance",
		"scnEffectInstanceId",
		"scnEndNode",
		"scnEntityItemsListener",
		"scnEntryPoint",
		"scnEventBlendWorkspotSetupParameters",
		"scnExecutionTag",
		"scnExecutionTagEntry",
		"scnExitPoint",
		"scnFindEntityInContextParams",
		"scnFindEntityInEntityParams",
		"scnFindEntityInNodeParams",
		"scnFindEntityInWorldParams",
		"scnFindNetworkPlayerParams",
		"scnFlowControlNode",
		"scnGameplayActionEvent",
		"scnGameplayActionSetVehicleSuspensionData",
		"scnGameplayAnimSetSRRef",
		"scnGameplayTransitionEvent",
		"scnGenderMask",
		"scnHubNode",
		"scnIBraindanceConditionType",
		"scnIGameplayActionData",
		"scnIInterruptCondition",
		"scnIInterruptManager_Operation",
		"scnIInterruptionOperation",
		"scnIInterruptionScenarioOperation",
		"scnIKEvent",
		"scnIKEventData",
		"scnIReturnCondition",
		"scnIScalingData",
		"scnISceneSystem",
		"scnInputSocketId",
		"scnInputSocketStamp",
		"scnInteractionShapeParams",
		"scnInterestingConversationData",
		"scnInterestingConversation_DEPRECATED",
		"scnInterestingConversationsGroup",
		"scnInterestingConversationsResource",
		"scnInterruptAvailability_Operation",
		"scnInterruptFactConditionType",
		"scnInterruptManagerNode",
		"scnInterruptionScenario",
		"scnInterruptionScenarioId",
		"scnIsAliveListener",
		"scnLipsyncAnimSetSRRef",
		"scnLipsyncAnimSetSRRefId",
		"scnLocalMarker",
		"scnLookAtAdvancedEvent",
		"scnLookAtAdvancedEventData",
		"scnLookAtBasicEventData",
		"scnLookAtBodyPartProperties",
		"scnLookAtBodyPartPropertiesAdvanced",
		"scnLookAtChestProperties",
		"scnLookAtEvent",
		"scnLookAtEventData",
		"scnLookAtEyesProperties",
		"scnLookAtHeadProperties",
		"scnLookAtTwoHandedProperties",
		"scnMarker",
		"scnNPCStatusEffectsListener",
		"scnNodeId",
		"scnNodeSymbol",
		"scnNotablePoint",
		"scnOutputSocket",
		"scnOutputSocketId",
		"scnOutputSocketStamp",
		"scnOverrideInterruptConditions_InterruptionScenarioOperation",
		"scnOverrideInterruptConditions_Operation",
		"scnOverrideInterruptionScenario_InterruptionOperation",
		"scnOverridePhantomParamsEvent",
		"scnOverridePhantomParamsEventParams",
		"scnOverrideReturnConditions_InterruptionScenarioOperation",
		"scnOverrideReturnConditions_Operation",
		"scnOverrideTalkOnReturn_InterruptionScenarioOperation",
		"scnPerformerId",
		"scnPerformerSymbol",
		"scnPlacementEvent",
		"scnPlayAnimEvent",
		"scnPlayAnimEventData",
		"scnPlayDefaultMountedSlotWorkspotEvent",
		"scnPlayFPPControlAnimEvent",
		"scnPlayRidAnimEvent",
		"scnPlaySkAnimEvent",
		"scnPlaySkAnimEventData",
		"scnPlaySkAnimRootMotionData",
		"scnPlayVideoEvent",
		"scnPlayerActorDef",
		"scnPlayerAnimData",
		"scnPoseCorrectionEvent",
		"scnPropDef",
		"scnPropId",
		"scnPropOwnershipTransferOptions",
		"scnQuestNode",
		"scnRandomizerNode",
		"scnReferencePointDef",
		"scnReferencePointId",
		"scnReminderCondition",
		"scnRewindableSectionEvent",
		"scnRewindableSectionNode",
		"scnRewindableSectionPlaySpeedModifiers",
		"scnRidAnimSetSRRef",
		"scnRidAnimSetSRRefId",
		"scnRidAnimationContainerSRRef",
		"scnRidAnimationContainerSRRefAnimContainer",
		"scnRidAnimationContainerSRRefAnimContainerContext",
		"scnRidAnimationContainerSRRefId",
		"scnRidAnimationSRRef",
		"scnRidAnimationSRRefId",
		"scnRidCameraAnimationSRRef",
		"scnRidCameraAnimationSRRefId",
		"scnRidCyberwareAnimSetSRRefId",
		"scnRidDeformationAnimSetSRRefId",
		"scnRidFacialAnimSetSRRefId",
		"scnRidResource",
		"scnRidResourceHandler",
		"scnRidResourceId",
		"scnRidSerialNumber",
		"scnRidTag",
		"scnSRRefCollection",
		"scnSRRefId",
		"scnScalingData_KeepRelationWithOtherEvents",
		"scnSceneEvent",
		"scnSceneEventId",
		"scnSceneEventSymbol",
		"scnSceneGraph",
		"scnSceneGraphNode",
		"scnSceneId",
		"scnSceneInstanceId",
		"scnSceneInstanceOwnerId",
		"scnSceneMarker",
		"scnSceneMarkerInternalsAnimEventEntry",
		"scnSceneMarkerInternalsWorkspotEntry",
		"scnSceneMarkerInternalsWorkspotEntrySocket",
		"scnSceneResource",
		"scnSceneSharedState",
		"scnSceneSolutionHash",
		"scnSceneSolutionHashHash",
		"scnSceneSystem",
		"scnSceneSystemGlobalSettings",
		"scnSceneTime",
		"scnSceneTimeProvider",
		"scnSceneVOInfo",
		"scnSceneWorkspotDataId",
		"scnSceneWorkspotInstanceId",
		"scnScenesVersions",
		"scnScenesVersionsChangedRecord",
		"scnScenesVersionsSceneChanges",
		"scnScriptInterface",
		"scnSectionInternalsActorBehavior",
		"scnSectionNode",
		"scnSetupSyncWorkspotRelationshipsEvent",
		"scnSpawnDespawnEntityParams",
		"scnSpawnSetParams",
		"scnSpawnerParams",
		"scnStartNode",
		"scnSyncNodeSignal",
		"scnSystemSharedState",
		"scnTalkInteractionListener",
		"scnTalkOnReturn_Operation",
		"scnTimedCondition",
		"scnToggleInterruption_InterruptionOperation",
		"scnToggleScenario_InterruptionScenarioOperation",
		"scnUnmountEvent",
		"scnUseSceneWorkspotParamsV1",
		"scnVarComparison_FactConditionType",
		"scnVarComparison_FactConditionTypeParams",
		"scnVarVsVarComparison_FactConditionType",
		"scnVarVsVarComparison_FactConditionTypeParams",
		"scnVoicesetComponent",
		"scnVoicesetComponentPS",
		"scnVoicetagId",
		"scnWalkToEvent",
		"scnWorkspotData",
		"scnWorkspotData_EmbeddedWorkspotTree",
		"scnWorkspotData_ExternalWorkspotResource",
		"scnWorkspotInstance",
		"scnWorkspotSymbol",
		"scnWorldMarker",
		"scnXorNode",
		"scndevEvent",
		"scneventsAttachPropToNode",
		"scneventsAttachPropToPerformer",
		"scneventsAttachPropToPerformerCachedFallbackBone",
		"scneventsAttachPropToPerformerFallbackData",
		"scneventsAttachPropToWorld",
		"scneventsAttachPropToWorldCachedFallbackBone",
		"scneventsAttachPropToWorldFallbackData",
		"scneventsBraindanceVisibilityEvent",
		"scneventsCameraEvent",
		"scneventsCameraOverrideSettings",
		"scneventsCameraParamsEvent",
		"scneventsCameraPlacementEvent",
		"scneventsClueEvent",
		"scneventsDespawnEntityEvent",
		"scneventsDespawnEntityEventParams",
		"scneventsEquipItemToPerformer",
		"scneventsMountEvent",
		"scneventsPlayAnimEventData",
		"scneventsPlayAnimEventExData",
		"scneventsPlayRidCameraAnimEvent",
		"scneventsPlayerLookAtEvent",
		"scneventsPlayerLookAtEventParams",
		"scneventsRagdollEvent",
		"scneventsSetAnimFeatureEvent",
		"scneventsSetAnimsetWeight",
		"scneventsSocket",
		"scneventsSpawnEntityEvent",
		"scneventsSpawnEntityEventCachedFallbackBone",
		"scneventsSpawnEntityEventFallbackData",
		"scneventsSpawnEntityEventParams",
		"scneventsUIAnimationBraindanceEvent",
		"scneventsUIAnimationEvent",
		"scneventsUnequipItemFromPerformer",
		"scneventsUnequipItemFromPerformerByItem",
		"scneventsVFXBraindanceEvent",
		"scneventsVFXDurationEvent",
		"scneventsVFXEvent",
		"scnfppGenderSpecificParams",
		"scnlocLangId",
		"scnlocLocStoreEmbedded",
		"scnlocLocStoreEmbeddedVariantDescriptorEntry",
		"scnlocLocStoreEmbeddedVariantPayloadEntry",
		"scnlocLocstringId",
		"scnlocSignature",
		"scnlocVariantId",
		"scnprvSpawnDespawnItem",
		"scnscreenplayChoiceOption",
		"scnscreenplayDialogLine",
		"scnscreenplayItemId",
		"scnscreenplayLineUsage",
		"scnscreenplayOptionUsage",
		"scnscreenplayStandaloneComment",
		"scnscreenplayStore",
		"scnsimActionsScenarios",
		"scnsimActionsScenariosNodeScenarios",
		"scnsimIActionScenario",
		]
# TODO
LocalizationString = str


@dataclass
class scnPerformerId(Chunk):
	id: int = 4294967040


@dataclass
class scnPerformerSymbol(Chunk):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	entity_ref: gameEntityReference = field(default_factory=gameEntityReference)
	editor_performer_id: int = 0


class scnScriptInterface(Chunk):
	pass


class scnsimIActionScenario(Chunk):
	pass


class scnIScalingData(Chunk):
	pass


@dataclass
class scnSceneEventId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnSceneWorkspotDataId(Chunk):
	id: int = sys.maxsize


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
	id: int = sys.maxsize


@dataclass
class scnNodeId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnActorId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnVoicetagId(Chunk):
	id: int = 0


@dataclass
class scnSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnSceneWorkspotInstanceId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnCinematicAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnDynamicAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnLipsyncAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidCyberwareAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidCameraAnimationSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidDeformationAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidFacialAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnPropId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidAnimSetSRRefId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnRidResourceId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnFindNetworkPlayerParams(Chunk):
	network_id: int = 0


@dataclass
class scnEntryPoint(Chunk):
	name: str = ''
	node_id: scnNodeId = field(default_factory=scnNodeId)


@dataclass
class scnExitPoint(Chunk):
	name: str = ''
	node_id: scnNodeId = field(default_factory=scnNodeId)


@dataclass
class scnNotablePoint(Chunk):
	name: str = ''
	node_id: scnNodeId = field(default_factory=scnNodeId)


@dataclass
class scnFindEntityInWorldParams(Chunk):
	actor_ref: gameEntityReference = field(default_factory=gameEntityReference)
	force_max_visibility: bool = False


@dataclass
class scnExecutionTagEntry(Chunk):
	name: str = ''
	flags: int = 0


@dataclass
class scnFindEntityInContextParams(Chunk):
	contextual_name: enums.scnContextualActorName = enums.scnContextualActorName.Player
	voice_vag_id: scnVoicetagId = field(default_factory=scnVoicetagId)
	context_actor_name: str = ''
	spec_record_id: int = 0
	force_max_visibility: bool = False


@dataclass
class scnSpawnSetParams(Chunk):
	reference: str = ''
	entry_name: str = ''
	force_max_visibility: bool = False


@dataclass
class scnCommunityParams(Chunk):
	reference: str = ''
	entry_name: str = ''
	force_max_visibility: bool = False


@dataclass
class scnSpawnerParams(Chunk):
	reference: str = ''
	force_max_visibility: bool = False


@dataclass
class scnFindEntityInNodeParams(Chunk):
	node_ref: str = ''
	force_max_visibility: bool = False


@dataclass
class scnSpawnDespawnEntityParams(Chunk):
	dynamic_entity_unique_name: str = ''
	spawn_marker: str = ''
	spawn_marker_type: enums.scnMarkerType = enums.scnMarkerType.Local
	spawn_marker_node_ref: str = ''
	spawn_offset: Transform = field(default_factory=Transform)
	item_owner_id: scnPerformerId = field(default_factory=scnPerformerId)
	spec_record_id: int = 0
	appearance: str = ''
	spawn_on_start: bool = True
	is_enabled: bool = True
	validate_spawn_postion: bool = True
	always_spawned: bool = False
	keep_alive: bool = False
	find_in_world: bool = False
	force_max_visibility: bool = False
	prefetch_appearance: bool = False


@dataclass
class scnActorDef(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	voicetag_id: scnVoicetagId = field(default_factory=scnVoicetagId)
	acquisition_plan: enums.scnEntityAcquisitionPlan = enums.scnEntityAcquisitionPlan.findInContext
	find_actor_in_context_params: scnFindEntityInContextParams = field(
			default_factory=scnFindEntityInContextParams
			)
	find_actor_in_world_params: scnFindEntityInWorldParams = field(default_factory=scnFindEntityInWorldParams)
	spawn_despawn_params: scnSpawnDespawnEntityParams = field(default_factory=scnSpawnDespawnEntityParams)
	spawn_set_params: scnSpawnSetParams = field(default_factory=scnSpawnSetParams)
	community_params: scnCommunityParams = field(default_factory=scnCommunityParams)
	spawner_params: scnSpawnerParams = field(default_factory=scnSpawnerParams)
	anim_sets: list[scnSRRefId] = field(default_factory=list)
	lipsync_anim_set: scnLipsyncAnimSetSRRefId = field(default_factory=scnLipsyncAnimSetSRRefId)
	facial_anim_sets: list[scnRidFacialAnimSetSRRefId] = field(default_factory=list)
	cyberware_anim_sets: list[scnRidCyberwareAnimSetSRRefId] = field(default_factory=list)
	deformation_anim_sets: list[scnRidDeformationAnimSetSRRefId] = field(default_factory=list)
	body_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	facial_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	cyberware_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId] = field(default_factory=list)
	holocall_init_scn: Chunk = field(default_factory=Chunk)  # TODO: CResourceAsyncReference
	actor_name: str = ''
	spec_character_record_id: int = 0
	spec_appearance: str = "default"


@dataclass
class scnAnimationMotionSample(Chunk):
	time: float = 0.0
	transform: Transform = field(default_factory=Transform)


@dataclass
class scnAnimationRidAudioData(Chunk):
	events: list[animAnimEvent] = field(default_factory=list)


@dataclass
class scnAnimName(Chunk):
	type: enums.scnAnimNameType = enums.scnAnimNameType.direct


@dataclass
class scnAnimTargetBasicData(Chunk):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	is_start: bool = True
	target_performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	target_slot: str = "pla_default_tgt"
	target_offset_entity_space: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	static_target: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
	target_actor_id: scnActorId = field(default_factory=scnActorId)
	target_prop_id: scnPropId = field(default_factory=scnPropId)
	target_type: enums.scnLookAtTargetType = enums.scnLookAtTargetType.Actor


@dataclass
class scnBluelineSelectedRequest(gamePlayerScriptableSystemRequest):
	pass


@dataclass
class scnCameraAnimationLOD(Chunk):
	trajectory: scnAnimationMotionSample = field(default_factory=scnAnimationMotionSample)
	tracks: float = 0.0


@dataclass
class scnCheckDistractedReturnConditionParams(Chunk):
	distracted: bool = False
	target: enums.scnDistractedConditionTarget = enums.scnDistractedConditionTarget.Anyone


@dataclass
class scnCheckPlayerCombatInterruptConditionParams(Chunk):
	is_in_combat: bool = True


@dataclass
class scnCheckPlayerCombatReturnConditionParams(Chunk):
	is_in_combat: bool = False


@dataclass
class scnCheckPlayerTargetEntityDistanceInterruptConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater
	target_entity: gameEntityReference = field(default_factory=gameEntityReference)


@dataclass
class scnCheckPlayerTargetEntityDistanceReturnConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater
	target_entity: gameEntityReference = field(default_factory=gameEntityReference)


@dataclass
class scnCheckPlayerTargetNodeDistanceInterruptConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater
	target_node: str = ''


@dataclass
class scnCheckPlayerTargetNodeDistanceReturnConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater
	target_node: str = ''


@dataclass
class scnCheckTriggerInterruptConditionParams(Chunk):
	inside: bool = False
	trigger_area: str = ''


@dataclass
class scnCheckTriggerReturnConditionParams(Chunk):
	inside: bool = True
	trigger_area: str = ''


@dataclass
class scnChoiceHubPartId(Chunk):
	id: int = 0


@dataclass
class scnChoiceNodeNsAttachToActorParams(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	visualizer_style: enums.scnChoiceNodeNsVisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.onScreen


@dataclass
class scnChoiceNodeNsAttachToGameObjectParams(Chunk):
	node_ref: str = ''
	visualizer_style: enums.scnChoiceNodeNsVisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.inWorld


@dataclass
class scnChoiceNodeNsAttachToPropParams(Chunk):
	prop_id: scnPropId = field(default_factory=scnPropId)
	visualizer_style: enums.scnChoiceNodeNsVisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.inWorld


@dataclass
class scnChoiceNodeNsAttachToScreenParams(Chunk):
	pass


@dataclass
class scnChoiceNodeNsAttachToWorldParams(Chunk):
	entity_position: tuple[float, float, float] = (0.0, 0.0, 0.0)
	entity_orientation: Quaternion = field(default_factory=Quaternion)
	custom_entity_radius: float = 0.0
	visualizer_style: enums.scnChoiceNodeNsVisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.onScreen


@dataclass
class scnChoiceNodeNsMappinParams(Chunk):
	location_type: enums.scnChoiceNodeNsMappinLocation = enums.scnChoiceNodeNsMappinLocation._None
	mappin_settings: int = 0


@dataclass
class scndevEvent(Chunk):
	node_id: scnNodeId = field(default_factory=scnNodeId)
	type: enums.scndevEventType = enums.scndevEventType.NodeFailed
	message: str = ''


@dataclass
class scnDialogDisplayString(Chunk):
	text: str = ''
	translation: str = ''
	pre_translated_text: str = ''
	post_translated_text: str = ''
	language: enums.scnDialogLineLanguage = enums.scnDialogLineLanguage.Origin


@dataclass
class scnDialogLineData(Chunk):
	id: int = 0
	text: str = ''
	type: enums.scnDialogLineType = enums.scnDialogLineType._None
	speaker: gameObject = field(default_factory=gameObject)
	speaker_name: str = ''
	is_persistent: bool = False
	duration: float = 0.0


@dataclass
class scnDialogLineDuplicationParams(Chunk):
	execution_tag: int = 0
	additional_speaker_id: scnActorId = field(default_factory=scnActorId)
	is_holocall_speaker: bool = False


@dataclass
class scnEntityItemsListener(gameIAttachmentSlotsListener):
	pass


@dataclass
class scnEventBlendWorkspotSetupParameters(Chunk):
	workspot_id: scnSceneWorkspotInstanceId = field(default_factory=scnSceneWorkspotInstanceId)
	sequence_entry_id: workWorkEntryId = field(default_factory=workWorkEntryId)
	idle_only_mode: bool = True
	work_excluded_gestures: list[workWorkEntryId] = field(default_factory=list)
	item_override: workWorkspotItemOverride = field(default_factory=workWorkspotItemOverride)


@dataclass
class scneventsAttachPropToPerformerCachedFallbackBone(Chunk):
	bone_name: str = ''
	model_space_transform: Transform = field(default_factory=Transform)


@dataclass
class scneventsAttachPropToPerformerFallbackData(Chunk):
	owner: scnPerformerId = field(default_factory=scnPerformerId)
	fallback_cached_bones: scneventsAttachPropToPerformerCachedFallbackBone = field(
			default_factory=scneventsAttachPropToPerformerCachedFallbackBone
			)
	fallback_animset: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceReference
	fallback_animation_name: str = ''
	fallback_anim_time: float = 0.0


@dataclass
class scneventsAttachPropToWorldCachedFallbackBone(Chunk):
	bone_name: str = ''
	model_space_transform: Transform = field(default_factory=Transform)


@dataclass
class scneventsAttachPropToWorldFallbackData(Chunk):
	owner: scnPerformerId = field(default_factory=scnPerformerId)
	fallback_cached_bones: scneventsAttachPropToWorldCachedFallbackBone = field(
			default_factory=scneventsAttachPropToWorldCachedFallbackBone
			)
	fallback_animset: animAnimSet = field(default_factory=animAnimSet)  # CResourceReference
	fallback_animation_name: str = ''
	fallback_anim_time: float = 0.0


@dataclass
class scneventsCameraOverrideSettings(Chunk):
	override_fov: bool = True
	override_dof: bool = True
	reset_fov: bool = False
	reset_dof: bool = False


@dataclass
class scneventsDespawnEntityEventParams(Chunk):
	performer: scnPerformerId = field(default_factory=scnPerformerId)


@dataclass
class scneventsPlayAnimEventData(Chunk):
	blend_in: float = 0.0
	blend_out: float = 0.0
	clip_front: float = 0.0
	clip_end: float = 0.0
	stretch: float = 1.0
	blend_in_curve: enums.scnEasingType = enums.scnEasingType.SinusoidalEaseInOut
	blend_out_curve: enums.scnEasingType = enums.scnEasingType.SinusoidalEaseInOut


@dataclass
class scneventsPlayAnimEventExData(Chunk):
	basic: scneventsPlayAnimEventData = field(default_factory=scneventsPlayAnimEventData)
	weight: float = 1.0
	body_part_mask: str = ''


@dataclass
class scneventsPlayerLookAtEventParams(Chunk):
	slot_name: str = ''
	offset_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	duration: float = 0.25
	adjust_pitch: bool = False
	adjust_yaw: bool = False
	end_on_target_reached: bool = False
	end_on_camera_input_applied: bool = False
	end_on_time_exceeded: bool = False
	camera_input_mag_to_break: float = 0.0
	precision: float = 0.0
	max_duration: float = 0.0
	ease_in: bool = True
	ease_out: bool = True


@dataclass
class scneventsSpawnEntityEventCachedFallbackBone(Chunk):
	bone_name: str = ''
	model_space_transform: Transform = field(default_factory=Transform)


@dataclass
class scneventsSpawnEntityEventFallbackData(Chunk):
	owner: scnPerformerId = field(default_factory=scnPerformerId)
	fallback_cached_bones: scneventsSpawnEntityEventCachedFallbackBone = field(
			default_factory=scneventsSpawnEntityEventCachedFallbackBone
			)
	fallback_animset: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceReference
	fallback_animation_name: str = ''
	fallback_anim_time: float = 0.0


@dataclass
class scneventsSpawnEntityEventParams(Chunk):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	reference_performer: scnPerformerId = field(default_factory=scnPerformerId)
	reference_performer_slot_id: int = 0
	reference_performer_item_id: int = 0
	fallback_data: list[scneventsSpawnEntityEventFallbackData] = field(default_factory=list)


class scnIGameplayActionData(Chunk):
	pass


@dataclass
class scnGameplayActionSetVehicleSuspensionData(scnIGameplayActionData):
	active: bool = False
	cooldown_time: float = 0.0


@dataclass
class scnIBraindanceConditionType(questISceneConditionType):
	pass


class scnIInterruptionOperation(Chunk):
	pass


class scnIInterruptionScenarioOperation(Chunk):
	pass


class scnIInterruptManager_Operation(Chunk):
	pass


@dataclass
class scnIKEventData(Chunk):
	orientation: Quaternion = field(default_factory=Quaternion)
	basic: scnAnimTargetBasicData = field(default_factory=scnAnimTargetBasicData)
	chain_name: str = "ikRightArm"
	request: animIKTargetRequest = field(default_factory=animIKTargetRequest)


@dataclass
class scnInteractionShapeParams(Chunk):
	preset: enums.scnChoiceNodeNsSizePreset = enums.scnChoiceNodeNsSizePreset.normal
	offset: tuple[float, float, float] = (0.0, 0.0, 0.0)
	rotation: Quaternion = field(default_factory=Quaternion)
	custom_indication_range: float = 0.0
	custom_activation_range: float = 0.0
	activation_yaw_limit: float = 0.0
	activation_base_length: float = 1.0
	activation_height: float = 3.0


@dataclass
class scnInterruptAvailability_Operation(scnIInterruptManager_Operation):
	available: bool = False


@dataclass
class scnIsAliveListener(gameIStatPoolsListener):
	pass


@dataclass
class scnISceneSystem(gameISceneSystem):
	pass


@dataclass
class scnSceneSystem(scnISceneSystem):
	pass


@dataclass
class scnlocLangId(Chunk):
	lang_id: int = 255


@dataclass
class scnLookAtAdvancedEventData(Chunk):
	basic: scnAnimTargetBasicData = field(default_factory=scnAnimTargetBasicData)
	requests: list[animLookAtRequestForPart] = field(
			default_factory=list
			)  # TODO: new() { new animLookAtRequestForPart { BodyPart = "RightHand", Request = new animLookAtRequest { TransitionSpeed = 60.000000F, OutTransitionSpeed = 60.000000F, FollowingSpeedFactorOverride = -1.000000F, Limits = new animLookAtLimits { SoftLimitDegrees = 360.000000F, HardLimitDegrees = 360.000000F, HardLimitDistance = 1000000.000000F, BackLimitDegrees = 180.000000F }, Suppress = 1.000000F, Mode = 1, Priority = -1, AdditionalParts = new(0) } } };


@dataclass
class scnLookAtBasicEventData(Chunk):
	basic: scnAnimTargetBasicData = field(default_factory=scnAnimTargetBasicData)
	remove_previous_advanced_look_ats: bool = True
	requests: list[animLookAtRequestForPart] = field(
			default_factory=list
			)  # TODO: new() { new animLookAtRequestForPart { BodyPart = "Eyes", Request = new animLookAtRequest { TransitionSpeed = 60.000000F, OutTransitionSpeed = 60.000000F, FollowingSpeedFactorOverride = -1.000000F, Limits = new animLookAtLimits { SoftLimitDegrees = 360.000000F, HardLimitDegrees = 270.000000F, HardLimitDistance = 1000000.000000F, BackLimitDegrees = 210.000000F }, Priority = -1, AdditionalParts = new(2) }, AttachLeftHandToRightHand = -1, AttachRightHandToLeftHand = -1 } };


@dataclass
class scnLookAtBodyPartProperties(Chunk):
	enable_factor: float = 1.0
	override: float = 0.0
	mode: int = 0


@dataclass
class scnLookAtBodyPartPropertiesAdvanced(Chunk):
	body_part_name: str = "Head"


@dataclass
class scnLookAtChestProperties(Chunk):
	enable_factor: float = 0.35
	override: float = 0.0
	mode: int = 0


@dataclass
class scnLookAtEventData(Chunk):
	id: int = sys.maxsize
	enable: bool = True
	single_body_part_name: str = ''
	single_target_slot: str = ''
	body_target_slot: str = ''
	head_target_slot: str = ''
	eyes_target_slot: str = ''
	single_weight: float = 1.0
	body_weight: float = 1.0
	head_weight: float = 1.0
	eyes_weight: float = 1.0
	use_single_weight_curve: bool = False
	use_body_weight_curve: bool = False
	use_head_weight_curve: bool = False
	use_eyes_weight_curve: bool = False
	single_weight_curve: list[float] = field(default_factory=list)
	body_weight_curve: list[float] = field(default_factory=list)
	head_weight_curve: list[float] = field(default_factory=list)
	eyes_weight_curve: list[float] = field(default_factory=list)
	single_limits: animLookAtLimits = field(default_factory=animLookAtLimits)
	body_limits: animLookAtLimits = field(default_factory=animLookAtLimits)
	head_limits: animLookAtLimits = field(default_factory=animLookAtLimits)
	eyes_limits: animLookAtLimits = field(default_factory=animLookAtLimits)


@dataclass
class scnLookAtEyesProperties(Chunk):
	enable_factor: float = 1.0
	override: float = 0.0
	mode: int = 0


@dataclass
class scnLookAtHeadProperties(Chunk):
	enable_factor: float = 0.75
	override: float = 0.0
	mode: int = 0


@dataclass
class scnLookAtTwoHandedProperties(Chunk):
	enable_factor: float = 0.0
	override: float = 0.0
	mode: int = 0


@dataclass
class scnNPCStatusEffectsListener(gameIStatusEffectListener):
	pass


@dataclass
class scnOverrideInterruptionScenario_InterruptionOperation(scnIInterruptionOperation):
	scenario_id: scnInterruptionScenarioId = field(default_factory=scnInterruptionScenarioId)
	scenario_operations: list[scnIInterruptionScenarioOperation] = field(default_factory=list)


@dataclass
class scnOverridePhantomParamsEventParams(Chunk):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	override_spawn_effect: str = ''
	override_idle_effect: str = ''


@dataclass
class scnOverrideTalkOnReturn_InterruptionScenarioOperation(scnIInterruptionScenarioOperation):
	talk_on_return: bool = True


@dataclass
class scnPlayAnimEventData(Chunk):
	blend_in: float = 0.0
	blend_out: float = 0.0
	clip_front: float = 0.0
	stretch: float = 1.0
	weight: float = 1.0
	body_part_mask: str = ''


@dataclass
class scnPlayerAnimData(Chunk):
	tier_data: gameSceneTierData = field(default_factory=gameSceneTierData)
	use_zsnapping: bool = False
	unmount_body_carry: bool = True
	is_end_of_carrying_animation: bool = False


@dataclass
class scnPlaySkAnimEventData(Chunk):
	anim_name: str = ''
	blend_in: float = 0.0
	blend_out: float = 0.0
	clip_front: float = 0.0
	stretch: float = 1.0
	weight: float = 1.0
	body_part_mask: str = ''


@dataclass
class scnprvSpawnDespawnItem(Chunk):
	record_id: int = 0
	final_transform: Transform = field(default_factory=Transform)


@dataclass
class scnRewindableSectionEvent(Chunk):
	active: bool = False


@dataclass
class scnRewindableSectionPlaySpeedModifiers(Chunk):
	forward_very_fast: float = 6.0
	forward_fast: float = 3.0
	forward_slow: float = 0.5
	backward_very_fast: float = 6.0
	backward_fast: float = 3.0
	backward_slow: float = 0.5


@dataclass
class scnSceneId(Chunk):
	res_path_hash: int = 0


@dataclass
class scnSceneInstanceOwnerId(Chunk):
	hash: int = 0


@dataclass
class scnSceneInstanceId(Chunk):
	scene_id: scnSceneId = field(default_factory=scnSceneId)
	owner_id: scnSceneInstanceOwnerId = field(default_factory=scnSceneInstanceOwnerId)
	internal_id: int = 255
	hash: int = 6242570315725555409


@dataclass
class scnSceneMarkerInternalsAnimEventEntry(Chunk):
	start_name: str = ''
	end_name: str = ''
	start_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	end_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	start_dir: tuple[float, float, float] = (0.0, 0.0, 0.0)
	end_dir: tuple[float, float, float] = (0.0, 0.0, 0.0)
	flags: int = 0


@dataclass
class scnSceneMarkerInternalsWorkspotEntrySocket(Chunk):
	name: str = ''
	transform: Transform = field(default_factory=Transform)


@dataclass
class scnSceneMarkerInternalsWorkspotEntry(Chunk):
	instance_id: int = 0
	instance_origin: Transform = field(default_factory=Transform)
	entries: list[scnSceneMarkerInternalsWorkspotEntrySocket] = field(default_factory=list)
	exits: list[scnSceneMarkerInternalsWorkspotEntrySocket] = field(default_factory=list)


@dataclass
class scnSceneMarker(worldIMarker):
	markers: list[scnSceneMarkerInternalsAnimEventEntry] = field(default_factory=list)
	workspot_markers: list[scnSceneMarkerInternalsWorkspotEntry] = field(default_factory=list)


@dataclass
class scnSyncNodeSignal(Chunk):
	node_id: int = 0
	name: int = 0
	ordinal: int = 0
	num_runs: int = 0


@dataclass
class scnSceneSharedState(Chunk):
	entrypoint: str = ''
	sync_nodes_visited: list[scnSyncNodeSignal] = field(default_factory=list)
	instance_hash: int = 6242570315725555409
	finished_on_server: bool = False
	finished_on_client: bool = False


@dataclass
class scnScenesVersions(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	current_version: int = 0
	scenes: list["scnScenesVersionsSceneChanges"] = field(default_factory=list)


@dataclass
class scnSceneSystemGlobalSettings(Chunk):
	sync_lipsync_to_scene_time: bool = False


@dataclass
class scnSceneTimeProvider(gameinteractionsvisIVisualizerTimeProvider):
	pass


@dataclass
class scnscreenplayStandaloneComment(Chunk):
	item_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	comment: str = ''


@dataclass
class scnsimActionsScenariosNodeScenarios(Chunk):
	node_id: scnNodeId = field(default_factory=scnNodeId)
	scenarios: list[scnsimIActionScenario] = field(default_factory=list)
	fallback: scnsimIActionScenario = field(default_factory=scnsimIActionScenario)


@dataclass
class scnsimActionsScenarios(Chunk):
	all_scenarios: list[scnsimActionsScenariosNodeScenarios] = field(default_factory=list)


class scnSystemSharedState(Chunk):
	pass


class scnTalkInteractionListener(Chunk):
	pass


@dataclass
class scnTalkOnReturn_Operation(scnIInterruptManager_Operation):
	talk_on_return: bool = False


@dataclass
class scnToggleInterruption_InterruptionOperation(scnIInterruptionOperation):
	enable: bool = True


@dataclass
class scnToggleScenario_InterruptionScenarioOperation(scnIInterruptionScenarioOperation):
	enable: bool = True


@dataclass
class scnUseSceneWorkspotParamsV1(questUseWorkspotParamsV1):

	workspot_instance_id: scnSceneWorkspotInstanceId = field(default_factory=scnSceneWorkspotInstanceId)
	play_at_actor_location: bool = False
	item_override: workWorkspotItemOverride = field(default_factory=workWorkspotItemOverride)


@dataclass
class scnVarVsVarComparison_FactConditionTypeParams(Chunk):
	fact_name1: str = ''
	fact_name2: str = ''
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnVoicesetComponent(gameComponent):
	# TODO: name = "VoicesetComponent";
	combat_vo_settings_name: str = ''


@dataclass
class scnChatter(Chunk):
	id: int = sys.maxsize
	voiceset_component: scnVoicesetComponent = field(default_factory=scnVoicesetComponent)


@dataclass
class scnChatterModuleSharedState(Chunk):
	chatter_history: list[scnChatter] = field(default_factory=list)


@dataclass
class scnVoicesetComponentPS(gameComponentPS):
	blocked_inputs: list[entVoicesetInputToBlock] = field(default_factory=list)
	voice_tag: str = ''
	npchigh_level_state: enums.gamedataNPCHighLevelState = enums.gamedataNPCHighLevelState.Invalid
	grunt_set_index: int = 0
	are_voiceset_lines_enabled: bool = True
	are_voiceset_grunts_enabled: bool = True


@dataclass
class scnWorldMarker(Chunk):
	type: enums.scnWorldMarkerType = enums.scnWorldMarkerType.NodeRef
	tag: str = ''
	node_ref: str = ''


@dataclass
class scnPlayerActorDef(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	spec_template: str = "(None)"
	spec_character_record_id: int = 0
	spec_appearance: str = "default"
	voicetag_id: scnVoicetagId = field(default_factory=scnVoicetagId)
	anim_sets: list[scnSRRefId] = field(default_factory=list)
	lipsync_anim_set: scnLipsyncAnimSetSRRefId = field(default_factory=scnLipsyncAnimSetSRRefId)
	facial_anim_sets: list[scnRidFacialAnimSetSRRefId] = field(default_factory=list)
	cyberware_anim_sets: list[scnRidCyberwareAnimSetSRRefId] = field(default_factory=list)
	deformation_anim_sets: list[scnRidDeformationAnimSetSRRefId] = field(default_factory=list)
	body_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	facial_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	cyberware_cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId] = field(default_factory=list)
	acquisition_plan: enums.scnEntityAcquisitionPlan = enums.scnEntityAcquisitionPlan.findInContext
	find_network_player_params: scnFindNetworkPlayerParams = field(default_factory=scnFindNetworkPlayerParams)
	find_actor_in_context_params: scnFindEntityInContextParams = field(
			default_factory=scnFindEntityInContextParams
			)
	player_name: str = ''


@dataclass
class scnInputSocketStamp(Chunk):
	name: int = sys.maxsize
	ordinal: int = sys.maxsize


@dataclass
class scnOutputSocketStamp(Chunk):
	name: int = sys.maxsize
	ordinal: int = sys.maxsize


@dataclass
class scnOutputSocketId(Chunk):
	node_id: scnNodeId = field(default_factory=scnNodeId)
	osock_stamp: scnOutputSocketStamp = field(default_factory=scnOutputSocketStamp)


@dataclass
class scnInputSocketId(Chunk):
	node_id: scnNodeId = field(default_factory=scnNodeId)
	isock_stamp: scnInputSocketStamp = field(default_factory=scnInputSocketStamp)


@dataclass
class scnOutputSocket(Chunk):
	stamp: scnOutputSocketStamp = field(default_factory=scnOutputSocketStamp)
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
	id: scnSceneEventId = field(default_factory=scnSceneEventId)
	# TODO: type: enums.scnEventType
	start_time: int = 0
	duration: int = 0
	execution_tag_flags: int = 0
	scaling_data: scnIScalingData = field(default_factory=scnIScalingData)


@dataclass
class scnAudioDurationEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	audio_event_name: str = ''
	playback_direction_support: enums.scnAudioPlaybackDirectionSupportFlag = enums.scnAudioPlaybackDirectionSupportFlag.Forward


@dataclass
class scnAudioEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	audio_event_name: str = ''
	ambient_unique_name: str = ''
	emitter_name: str = ''
	fast_forward_support: enums.scnAudioFastForwardSupport = enums.scnAudioFastForwardSupport.MuteDuringFastForward


@dataclass
class scneventsAttachPropToNode(scnSceneEvent):
	prop_id: scnPropId = field(default_factory=scnPropId)
	node_ref: str = ''
	custom_offset_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	custom_offset_rot: Quaternion = field(default_factory=Quaternion)


@dataclass
class scneventsAttachPropToPerformer(scnSceneEvent):
	prop_id: scnPropId = field(default_factory=scnPropId)
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	slot: str = "(Root)"
	offset_mode: enums.scnOffsetMode = enums.scnOffsetMode.useRealOffset
	custom_offset_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	custom_offset_rot: Quaternion = field(default_factory=Quaternion)
	fallback_data: list[Any] = field(default_factory=list)  # TODO: scneventsAttachPropToPerformerFallbackData


@dataclass
class scneventsAttachPropToWorld(scnSceneEvent):
	prop_id: scnPropId = field(default_factory=scnPropId)
	offset_mode: enums.scnOffsetMode = enums.scnOffsetMode.useRealOffset
	custom_offset_pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
	custom_offset_rot: Quaternion = field(default_factory=Quaternion)
	reference_performer: scnPerformerId = field(default_factory=scnPerformerId)
	reference_performer_slot_id: int = 0
	reference_performer_item_id: int = 0
	fallback_data: list[Any] = field(default_factory=list)  # TODO: scneventsAttachPropToWorldFallbackData


@dataclass
class scneventsBraindanceVisibilityEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	custom_material_param: enums.ECustomMaterialParam = enums.ECustomMaterialParam.ECMP_CustomParam0
	parameter_index: int = 0
	override: bool = False
	priority: int = 7
	event_start_end_blend: float = 0.0
	perspective_blend: float = 0.5
	render_settings_fpp: WorldRenderAreaSettings = field(default_factory=WorldRenderAreaSettings)
	render_settings_tpp: WorldRenderAreaSettings = field(default_factory=WorldRenderAreaSettings)


@dataclass
class scneventsCameraEvent(scnSceneEvent):
	camera_ref: str = ''
	is_blend_in: bool = True
	blend_time: float = 0.0


@dataclass
class scneventsCameraParamsEvent(scnSceneEvent):
	camera_ref: str = ''
	fov_value: float = 51.0
	fov_weigh: float = 1.0
	dof_intensity: float = 0.0
	dof_near_blur: float = 0.0
	dof_near_focus: float = 0.0
	dof_far_blur: float = 0.0
	dof_far_focus: float = 0.0
	use_near_plane: bool = True
	use_far_plane: bool = True
	is_player_camera: bool = False
	camera_override_settings: scneventsCameraOverrideSettings = field(
			default_factory=scneventsCameraOverrideSettings
			)
	target_actor: scnPerformerId = field(default_factory=scnPerformerId)
	target_slot: str = ''


@dataclass
class scneventsCameraPlacementEvent(scnSceneEvent):
	camera_ref: str = ''
	camera_transform_ls: Transform = field(default_factory=Transform)


@dataclass
class scneventsClueEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	clue_entity: gameEntityReference = field(default_factory=gameEntityReference)
	marked_on_timeline: bool = True
	clue_name: str = ''
	layer: enums.gameuiEBraindanceLayer = enums.gameuiEBraindanceLayer.Visual
	override_fact: bool = True
	fact_name: str = ''


@dataclass
class scneventsDespawnEntityEvent(scnSceneEvent):
	params: scneventsDespawnEntityEventParams = field(default_factory=scneventsDespawnEntityEventParams)


@dataclass
class scneventsEquipItemToPerformer(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	slot_id: int = 0
	item_id: int = 0


@dataclass
class scneventsMountEvent(scnSceneEvent):
	parent: scnPerformerId = field(default_factory=scnPerformerId)
	child: scnPerformerId = field(default_factory=scnPerformerId)
	slot_name: str = ''
	carry_style: enums.gamePSMBodyCarryingStyle = enums.gamePSMBodyCarryingStyle.Any
	is_instant: bool = True
	remove_pitch_roll_rotation_on_dismount: bool = False
	keep_transform: bool = False
	is_carrying: bool = False
	switch_render_plane: bool = True


@dataclass
class scneventsPlayerLookAtEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''
	look_at_params: scneventsPlayerLookAtEventParams = field(default_factory=scneventsPlayerLookAtEventParams)


@dataclass
class scneventsRagdollEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	enable_ragdoll: bool = True


@dataclass
class scneventsSetAnimFeatureEvent(scnSceneEvent):
	actor_id: scnActorId = field(default_factory=scnActorId)
	anim_feature_name: str = ''
	anim_feature: animAnimFeature = field(default_factory=animAnimFeature)


@dataclass
class scneventsSetAnimsetWeight(scnSceneEvent):
	actor_id: scnActorId = field(default_factory=scnActorId)
	animset_name: str = ''
	weight: float = 0.0


@dataclass
class scneventsSocket(scnSceneEvent):
	osock_stamp: scnOutputSocketStamp = field(default_factory=scnOutputSocketStamp)


@dataclass
class scneventsSpawnEntityEvent(scnSceneEvent):
	params: scneventsSpawnEntityEventParams = field(default_factory=scneventsSpawnEntityEventParams)


@dataclass
class scneventsUIAnimationBraindanceEvent(scnSceneEvent):
	animation_name: str = ''
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''


@dataclass
class scneventsUIAnimationEvent(scnSceneEvent):
	animation_name: str = ''
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''


@dataclass
class scneventsUnequipItemFromPerformer(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	slot_id: int = 0
	restore_gameplay_item: bool = False


@dataclass
class scneventsUnequipItemFromPerformerByItem(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	item_id: int = 0
	restore_gameplay_item: bool = False


@dataclass
class scnGameplayActionEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	gameplay_action_data: scnIGameplayActionData = field(default_factory=scnIGameplayActionData)


@dataclass
class scnGameplayTransitionEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	veh_state: enums.scnPuppetVehicleState = enums.scnPuppetVehicleState.IdleMounted


@dataclass
class scnIKEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	ik_data: scnIKEventData = field(default_factory=scnIKEventData)


@dataclass
class scnLookAtAdvancedEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	advanced_data: scnLookAtAdvancedEventData = field(default_factory=scnLookAtAdvancedEventData)


@dataclass
class scnLookAtEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	basic_data: scnLookAtBasicEventData = field(
			default_factory=scnLookAtBasicEventData
			)  # TODO: new scnLookAtBasicEventData { Basic = new scnAnimTargetBasicData { PerformerId, IsStart = true, TargetPerformerId, TargetSlot = "pla_default_tgt", StaticTarget = new Vector4 { W = 1.000000F }, }, RemovePreviousAdvancedLookAts = true, Requests = new() { new animLookAtRequestForPart { BodyPart = "Eyes", Request = new animLookAtRequest { TransitionSpeed = 60.000000F, OutTransitionSpeed = 60.000000F, FollowingSpeedFactorOverride = -1.000000F, Priority = -1,  }, AttachLeftHandToRightHand = -1, AttachRightHandToLeftHand = -1 } } };


@dataclass
class scnOverridePhantomParamsEvent(scnSceneEvent):
	params: scnOverridePhantomParamsEventParams = field(default_factory=scnOverridePhantomParamsEventParams)


@dataclass
class scnPlayAnimEvent(scnSceneEvent):
	anim_data: scneventsPlayAnimEventExData = field(default_factory=scneventsPlayAnimEventExData)
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	actor_component: str = ''
	convert_to_additive: bool = False
	# TODO: mute_anim_events: CBitField<animMuteAnimEvents> = field(default_factory=CBitField<animMuteAnimEvents>)
	neck_weight: float = 0.0
	upper_face_blend_additive: bool = False
	lower_face_blend_additive: bool = False
	eyes_blend_additive: bool = False


@dataclass
class scnChangeIdleAnimEvent(scnPlayAnimEvent):
	# TODO: duration: int = 1000
	# TODO: neck_weight = 1.000000F;
	# TODO: upper_face_blend_additive = True
	# TODO: lower_face_blend_additive = True
	# TODO: eyes_blend_additive = True
	# TODO: baked_facial_transition = new animFacialEmotionTransitionBaked { transition_type = enums.animFacialEmotionTransitionType.Fast, to_idle_weight = 1.0 };
	idle_anim_name: str = ''
	add_idle_anim_name: str = ''
	is_enabled: bool = True
	anim_name: str = ''
	baked_facial_transition: animFacialEmotionTransitionBaked = field(
			default_factory=animFacialEmotionTransitionBaked
			)
	facial_instant_transition: bool = False


@dataclass
class scnPlayDefaultMountedSlotWorkspotEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)
	parent_ref: gameEntityReference = field(default_factory=gameEntityReference)
	slot_name: str = ''
	puppet_vehicle_state: enums.scnPuppetVehicleState = enums.scnPuppetVehicleState.IdleMounted


@dataclass
class scnPlayVideoEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	video_path: str = ''
	is_phone_call: bool = False
	force_frame_rate: bool = False


@dataclass
class scnPoseCorrectionEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	pose_correction_group: animPoseCorrectionGroup = field(default_factory=animPoseCorrectionGroup)


@dataclass
class scnSetupSyncWorkspotRelationshipsEvent(scnSceneEvent):
	synced_workspot_ids: scnSceneWorkspotInstanceId = field(default_factory=lambda: scnSceneWorkspotInstanceId(0))


@dataclass
class scnUnmountEvent(scnSceneEvent):
	performer: scnPerformerId = field(default_factory=scnPerformerId)


@dataclass
class scnWalkToEvent(scnSceneEvent):
	actor_id: scnActorId = field(default_factory=scnActorId)
	target_waypoint_tag: str = ''
	use_pathfinding: bool = False


@dataclass
class scnDialogLineEvent(scnSceneEvent):
	# TODO: duration: int = 1000
	screenplay_line_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	vo_params: scnDialogLineVoParams = field(default_factory=scnDialogLineVoParams)
	visual_style: enums.scnDialogLineVisualStyle = enums.scnDialogLineVisualStyle.regular
	additional_speakers: scnAdditionalSpeakers = field(default_factory=scnAdditionalSpeakers)


class scnInterruptFactConditionType(Chunk):
	pass


class scnIInterruptCondition(Chunk):
	pass


@dataclass
class scnVarComparison_FactConditionTypeParams(Chunk):
	fact_name: str = ''
	value: int = 0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnVarComparison_FactConditionType(scnInterruptFactConditionType):
	params: scnVarComparison_FactConditionTypeParams = field(
			default_factory=scnVarComparison_FactConditionTypeParams
			)


@dataclass
class scnVarVsVarComparison_FactConditionType(scnInterruptFactConditionType):
	params: scnVarVsVarComparison_FactConditionTypeParams = field(
			default_factory=scnVarVsVarComparison_FactConditionTypeParams
			)


@dataclass
class scnCheckFactInterruptConditionParams(Chunk):
	fact_condition: scnInterruptFactConditionType = field(default_factory=scnInterruptFactConditionType)


@dataclass
class scnCheckFactReturnConditionParams(Chunk):
	fact_condition: scnInterruptFactConditionType = field(default_factory=scnInterruptFactConditionType)


@dataclass
class scnCheckAnyoneDistractedInterruptCondition(scnIInterruptCondition):
	pass


@dataclass
class scnCheckFactInterruptCondition(scnIInterruptCondition):
	params: scnCheckFactInterruptConditionParams = field(default_factory=scnCheckFactInterruptConditionParams)


@dataclass
class scnCheckMountedVehicleImpactInterruptCondition(scnIInterruptCondition):
	pass


@dataclass
class scnCheckPlayerCombatInterruptCondition(scnIInterruptCondition):
	params: scnCheckPlayerCombatInterruptConditionParams = field(
			default_factory=scnCheckPlayerCombatInterruptConditionParams
			)


@dataclass
class scnCheckPlayerTargetEntityDistanceInterruptCondition(scnIInterruptCondition):
	params: scnCheckPlayerTargetEntityDistanceInterruptConditionParams = field(
			default_factory=lambda: scnCheckPlayerTargetEntityDistanceInterruptConditionParams(distance=6.0)
			)


@dataclass
class scnCheckPlayerTargetNodeDistanceInterruptCondition(scnIInterruptCondition):
	params: scnCheckPlayerTargetNodeDistanceInterruptConditionParams = field(
			default_factory=lambda: scnCheckPlayerTargetNodeDistanceInterruptConditionParams(distance=6.0)
			)


@dataclass
class scnCheckSpeakerDistractedInterruptCondition(scnIInterruptCondition):
	pass


@dataclass
class scnCheckSpeakerOrAddressDistractedInterruptCondition(scnIInterruptCondition):
	pass


@dataclass
class scnCheckTriggerInterruptCondition(scnIInterruptCondition):
	params: scnCheckTriggerInterruptConditionParams = field(
			default_factory=scnCheckTriggerInterruptConditionParams
			)


@dataclass
class scnOverrideInterruptConditions_InterruptionScenarioOperation(scnIInterruptionScenarioOperation):
	interrupt_conditions: list[scnIInterruptCondition] = field(default_factory=list)


@dataclass
class scnOverrideInterruptConditions_Operation(scnIInterruptManager_Operation):
	interrupt_conditions: list[scnIInterruptCondition] = field(default_factory=list)


class scnIReturnCondition(Chunk):
	pass


@dataclass
class scnCheckDistractedReturnCondition(scnIReturnCondition):
	params: scnCheckDistractedReturnConditionParams = field(
			default_factory=scnCheckDistractedReturnConditionParams
			)


@dataclass
class scnCheckFactReturnCondition(scnIReturnCondition):
	params: scnCheckFactReturnConditionParams = field(default_factory=scnCheckFactReturnConditionParams)


@dataclass
class scnCheckPlayerCombatReturnCondition(scnIReturnCondition):
	params: scnCheckPlayerCombatReturnConditionParams = field(
			default_factory=scnCheckPlayerCombatReturnConditionParams
			)


@dataclass
class scnCheckPlayerTargetEntityDistanceReturnCondition(scnIReturnCondition):
	params: scnCheckPlayerTargetEntityDistanceReturnConditionParams = field(
			default_factory=lambda: scnCheckPlayerTargetEntityDistanceReturnConditionParams(
					distance=5.0, comparison_type=enums.EComparisonType.Less
					)
			)


@dataclass
class scnCheckPlayerTargetNodeDistanceReturnCondition(scnIReturnCondition):
	params: scnCheckPlayerTargetNodeDistanceReturnConditionParams = field(
			default_factory=lambda: scnCheckPlayerTargetNodeDistanceReturnConditionParams(
					distance=5.0, comparison_type=enums.EComparisonType.Less
					)
			)


@dataclass
class scnCheckTriggerReturnCondition(scnIReturnCondition):
	params: scnCheckTriggerReturnConditionParams = field(default_factory=scnCheckTriggerReturnConditionParams)


@dataclass
class scnDummyAlwaysTrueReturnCondition(scnIReturnCondition):
	pass


@dataclass
class scnOverrideReturnConditions_InterruptionScenarioOperation(scnIInterruptionScenarioOperation):
	return_conditions: list[scnIReturnCondition] = field(default_factory=list)


@dataclass
class scnOverrideReturnConditions_Operation(scnIInterruptManager_Operation):
	return_conditions: list[scnIReturnCondition] = field(default_factory=list)


@dataclass
class scnInterruptionScenario(Chunk):
	id: scnInterruptionScenarioId = field(default_factory=scnInterruptionScenarioId)
	name: str = ''
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
	node_id: scnNodeId = field(default_factory=scnNodeId)
	ff_strategy: enums.scnFastForwardStrategy = enums.scnFastForwardStrategy.automatic
	output_sockets: list[scnOutputSocket] = field(default_factory=list)


@dataclass
class scnStartNode(scnSceneGraphNode):
	pass


@dataclass
class scnEndNode(scnSceneGraphNode):
	type: enums.scnEndNodeNsType = enums.scnEndNodeNsType.Terminating


@dataclass
class scnAndNode(scnSceneGraphNode):
	num_in_sockets: int = 0


@dataclass
class scnCutControlNode(scnSceneGraphNode):
	pass


@dataclass
class scnDeletionMarkerNode(scnSceneGraphNode):
	pass


@dataclass
class scnFlowControlNode(scnSceneGraphNode):
	is_open: bool = True
	opens_at: int = 0
	closes_at: int = 0


@dataclass
class scnHubNode(scnSceneGraphNode):
	pass


@dataclass
class scnInterruptManagerNode(scnSceneGraphNode):
	interruption_operations: list[scnIInterruptionOperation] = field(default_factory=list)


@dataclass
class scnQuestNode(scnSceneGraphNode):
	quest_node: questNodeDefinition = field(default_factory=questNodeDefinition)
	isock_mappings: list[str] = field(default_factory=list)
	osock_mappings: list[str] = field(default_factory=list)


@dataclass
class scnRandomizerNode(scnSceneGraphNode):
	mode: enums.scnRandomizerMode = enums.scnRandomizerMode.Random
	num_out_sockets: int = 0
	weights: list[int] = field(default_factory=list)


@dataclass
class scnXorNode(scnSceneGraphNode):
	pass


@dataclass
class scnSceneTime(Chunk):
	stu: int = 0


@dataclass
class scnChoiceNodeNsActorReminderParams(Chunk):
	use_custom_reminder: bool = False
	reminder_actor: scnActorId = field(default_factory=scnActorId)
	wait_time_for_reminder_a: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_b: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_c: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_looping: scnSceneTime = field(default_factory=scnSceneTime)
	cut_reminder_enabled: bool = False
	wait_time_to_cut_reminder: float = 0.0


@dataclass
class scnChoiceNodeNsReminderParams(Chunk):
	reminder_enabled: bool = False
	use_custom_reminder: bool = False
	reminder_actor: scnActorId = field(default_factory=scnActorId)
	wait_time_for_reminder_a: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_b: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_c: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_looping: scnSceneTime = field(default_factory=scnSceneTime)


@dataclass
class scnChoiceNodeNsTimedParams(Chunk):
	action: enums.scnChoiceNodeNsTimedAction = enums.scnChoiceNodeNsTimedAction.appear
	time_limited_finish: bool = False
	duration: scnSceneTime = field(default_factory=scnSceneTime)


@dataclass
class scnTimedCondition(Chunk):
	duration: scnSceneTime = field(default_factory=scnSceneTime)
	action: enums.scnChoiceNodeNsTimedAction = enums.scnChoiceNodeNsTimedAction.appear
	time_limited_finish: bool = False


@dataclass
class scnReminderCondition(Chunk):
	use_custom_reminder: bool = False
	reminder_actor: scnActorId = field(default_factory=scnActorId)
	wait_time_for_reminder_a: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_b: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_reminder_c: scnSceneTime = field(default_factory=scnSceneTime)
	wait_time_for_looping: scnSceneTime = field(default_factory=scnSceneTime)
	start_time: scnSceneTime = field(default_factory=scnSceneTime)
	process_step: enums.scnReminderConditionProcessStep = enums.scnReminderConditionProcessStep.ReminderA
	playing: bool = False
	running: bool = False
	reminder_params: scnChoiceNodeNsReminderParams = field(default_factory=scnChoiceNodeNsReminderParams)


class scnChoiceNodeNsLookAtParams(Chunk):
	pass


@dataclass
class scnChoiceNodeNsBasicLookAtParams(scnChoiceNodeNsLookAtParams):
	slot_name: str = ''
	offset: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class scnChoiceNodeNsDeprecatedParams(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	prop_id: scnPropId = field(default_factory=scnPropId)


@dataclass
class scnScalingData_KeepRelationWithOtherEvents(scnIScalingData):
	group_rfrnc_ndspace_starttime: scnSceneTime = field(default_factory=scnSceneTime)
	group_rfrnc_ndspace_endtime: scnSceneTime = field(default_factory=scnSceneTime)


@dataclass
class scnSectionInternalsActorBehavior(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	behavior_mode: enums.scnSectionInternalsActorBehaviorMode = enums.scnSectionInternalsActorBehaviorMode.OnlyIfAlive


@dataclass
class scnRewindableSectionNode(scnSceneGraphNode):
	events: list[HandleData[scnSceneEvent]] = field(default_factory=list)
	section_duration: scnSceneTime = field(default_factory=scnSceneTime)
	actor_behaviors: list[scnSectionInternalsActorBehavior] = field(default_factory=list)
	play_speed_modifiers: scnRewindableSectionPlaySpeedModifiers = field(
			default_factory=scnRewindableSectionPlaySpeedModifiers
			)


@dataclass
class scnSectionNode(scnSceneGraphNode):
	events: list[HandleData[scnSceneEvent]] = field(default_factory=list)
	section_duration: scnSceneTime = field(default_factory=scnSceneTime)
	actor_behaviors: list[scnSectionInternalsActorBehavior] = field(default_factory=list)
	is_focus_clue: bool = False


@dataclass
class scnSceneGraph(Chunk):
	graph: list[HandleData[scnSceneGraphNode]] = field(default_factory=list)
	start_nodes: list[scnNodeId] = field(default_factory=list)
	end_nodes: list[scnNodeId] = field(default_factory=list)


@dataclass
class scnLocalMarker(Chunk):
	transform_ls: Transform = field(default_factory=Transform)
	name: str = ''


@dataclass
class scnPropOwnershipTransferOptions(Chunk):
	type: enums.scnPropOwnershipTransferOptionsType = enums.scnPropOwnershipTransferOptionsType.TransferToWorkspotSystem_Automatic
	dettach_from_slot: bool = True
	remove_from_inventory: bool = True


@dataclass
class scnFindEntityInEntityParams(Chunk):
	actor_id: scnActorId = field(default_factory=scnActorId)
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	item_id: int = 0
	slot_id: int = 0
	force_max_visibility: bool = False
	ownership_transfer_options: scnPropOwnershipTransferOptions = field(
			default_factory=scnPropOwnershipTransferOptions
			)


@dataclass
class scnPropDef(Chunk):
	prop_id: scnPropId = field(default_factory=scnPropId)
	prop_name: str = ''
	spec_prop_record_id: int = 0
	anim_sets: list[scnRidAnimSetSRRefId] = field(default_factory=list)
	cinematic_anim_sets: list[scnCinematicAnimSetSRRefId] = field(default_factory=list)
	dynamic_anim_sets: list[scnDynamicAnimSetSRRefId] = field(default_factory=list)
	entity_acquisition_plan: enums.scnEntityAcquisitionPlan = enums.scnEntityAcquisitionPlan.findInContext
	find_entity_in_entity_params: scnFindEntityInEntityParams = field(default_factory=scnFindEntityInEntityParams)
	spawn_despawn_params: scnSpawnDespawnEntityParams = field(default_factory=scnSpawnDespawnEntityParams)
	spawn_set_params: scnSpawnSetParams = field(default_factory=scnSpawnSetParams)
	community_params: scnCommunityParams = field(default_factory=scnCommunityParams)
	spawner_params: scnSpawnerParams = field(default_factory=scnSpawnerParams)
	find_entity_in_node_params: scnFindEntityInNodeParams = field(default_factory=scnFindEntityInNodeParams)
	find_entity_in_world_params: scnFindEntityInWorldParams = field(default_factory=scnFindEntityInWorldParams)


@dataclass
class scnWorkspotData(Chunk):
	data_id: scnSceneWorkspotDataId = field(default_factory=scnSceneWorkspotDataId)


@dataclass
class scnWorkspotData_EmbeddedWorkspotTree(scnWorkspotData):
	workspot_tree: workWorkspotTree = field(default_factory=workWorkspotTree)


@dataclass
class scnWorkspotData_ExternalWorkspotResource(scnWorkspotData):
	pass
	# TODO: workspot_resource: CResourceReference<workWorkspotResource> = field(default_factory=CResourceReference<workWorkspotResource>)


@dataclass
class scnMarker(Chunk):
	type: enums.scnMarkerType = enums.scnMarkerType.Global
	local_marker_id: str = ''
	node_ref: str = ''
	entity_ref: gameEntityReference = field(default_factory=gameEntityReference)
	slot_name: str = ''
	is_mounted: bool = True


@dataclass
class scnPlaySkAnimRootMotionData(Chunk):
	enabled: bool = False
	placement_mode: enums.scnRootMotionAnimPlacementMode = enums.scnRootMotionAnimPlacementMode.Blend
	origin_marker: scnMarker = field(default_factory=scnMarker)
	origin_offset: Transform = field(default_factory=Transform)
	custom_blend_in_time: float = -1.0
	custom_blend_in_curve: enums.scnEasingType = enums.scnEasingType.SinusoidalEaseInOut
	remove_pitch_roll_rotation: bool = True
	mesh_dissolving_enabled: bool = True
	snap_to_ground_start: float = 0.0
	snap_to_ground_end: float = 0.0
	snap_to_ground: bool = False
	vehicle_change_physics_state: bool = True
	vehicle_enabled_physics_on_end: bool = True
	trajectory_lod: list[scnAnimationMotionSample] = field(default_factory=list)


# @dataclass
# class scnVehicleMoveOnSpline_Overrides(questIVehicleMoveOnSpline_Overrides):
# 	use_entry: bool = False
# 	use_exit: bool = False
# 	entry_speed: float = -1.0
# 	exit_speed: float = -1.0
# 	entry_transform: Transform = field(default_factory=Transform)
# 	exit_transform: Transform = field(default_factory=Transform)
# 	entry_marker: scnMarker = field(default_factory=scnMarker)
# 	exit_marker: scnMarker = field(default_factory=scnMarker)


@dataclass
class scneventsPlayRidCameraAnimEvent(scnSceneEvent):
	camera_ref: str = ''
	camera_placement: enums.scneventsRidCameraPlacement = enums.scneventsRidCameraPlacement.SceneOrigin
	anim_data: scneventsPlayAnimEventData = field(default_factory=scneventsPlayAnimEventData)
	anim_srref_id: scnRidCameraAnimationSRRefId = field(default_factory=scnRidCameraAnimationSRRefId)
	anim_origin_marker: scnMarker = field(default_factory=scnMarker)
	activate_as_game_camera: bool = True
	control_render_to_texture_state: bool = False
	mark_camer_cut: bool = True


class scnPlacementEvent(scnSceneEvent):
	actor_id: scnActorId = field(default_factory=scnActorId)
	target_waypoint: scnMarker = field(default_factory=scnMarker)


@dataclass
class scnWorkspotInstance(Chunk):
	workspot_instance_id: scnSceneWorkspotInstanceId = field(default_factory=scnSceneWorkspotInstanceId)
	data_id: scnSceneWorkspotDataId = field(default_factory=scnSceneWorkspotDataId)
	local_transform: Transform = field(default_factory=Transform)
	play_at_actor_location: bool = False
	origin_marker: scnMarker = field(default_factory=scnMarker)


@dataclass
class scnRidSerialNumber(Chunk):
	serial_number: int = sys.maxsize


@dataclass
class scnRidTag(Chunk):
	signature: str = ''
	serial_number: scnRidSerialNumber = field(default_factory=scnRidSerialNumber)


@dataclass
class scnCameraAnimationRid(Chunk):
	tag: scnRidTag = field(default_factory=scnRidTag)
	animation: animIAnimationBuffer = field(default_factory=animIAnimationBuffer)
	camera_animation_lod: scnCameraAnimationLOD = field(default_factory=scnCameraAnimationLOD)


@dataclass
class scnCameraRid(Chunk):
	tag: scnRidTag = field(default_factory=scnRidTag)
	animations: list[scnCameraAnimationRid] = field(default_factory=list)


@dataclass
class scnAnimationRid(Chunk):
	tag: scnRidTag = field(default_factory=scnRidTag)
	animation: animAnimation = field(default_factory=animAnimation)
	events: animEventsContainer = field(default_factory=animEventsContainer)
	motion_extracted: bool = False
	offset: Transform = field(default_factory=Transform)
	bones_count: int = 0
	trajectory_bone_index: int = -1


@dataclass
class scnActorRid(Chunk):
	tag: scnRidTag = field(default_factory=scnRidTag)
	animations: list[scnAnimationRid] = field(default_factory=list)
	facial_animations: list[scnAnimationRid] = field(default_factory=list)
	cyberware_animations: list[scnAnimationRid] = field(default_factory=list)


@dataclass
class scnRidResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	actors: list[scnActorRid] = field(default_factory=list)
	cameras: list[scnCameraRid] = field(default_factory=list)
	next_serial_number: scnRidSerialNumber = field(default_factory=scnRidSerialNumber)
	version: int = 0


@dataclass
class scnRidResourceHandler(Chunk):
	id: scnRidResourceId = field(default_factory=scnRidResourceId)
	rid_resource: scnRidResource = field(default_factory=scnRidResource)  # TODO: CResourceReference


@dataclass
class scnAddIdleAnimEvent(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	actor_component: str = "body"
	weight: float = 1.0


@dataclass
class scnAddIdleWithBlendAnimEvent(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	actor_component: str = "body"
	target_weight: float = 1.0


@dataclass
class scnRidAnimationSRRef(Chunk):
	resource_id: scnRidResourceId = field(default_factory=scnRidResourceId)
	animation_sn: scnRidSerialNumber = field(default_factory=scnRidSerialNumber)


@dataclass
class scnRidAnimSetSRRef(Chunk):
	animations: list[scnSRRefId] = field(default_factory=list)


@dataclass
class scnLipsyncAnimSetSRRef(Chunk):
	lipsync_anim_set: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceReference
	async_ref_lipsync_anim_set: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceAsyncReference


@dataclass
class scnRidCameraAnimationSRRef(Chunk):
	resource_id: scnRidResourceId = field(default_factory=scnRidResourceId)
	animation_sn: scnRidSerialNumber = field(default_factory=scnRidSerialNumber)


@dataclass
class scnCinematicAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceAsyncReference
	priority: int = 128
	is_override: bool = False


@dataclass
class scnGameplayAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceAsyncReference


@dataclass
class scnDynamicAnimSetSRRef(Chunk):
	async_anim_set: Any  # TODO: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceAsyncReference


@dataclass
class scnAnimSetAnimNames(Chunk):
	animation_names: list[str] = field(default_factory=list)


@dataclass
class scnGenderMask(Chunk):
	mask: int = 128


@dataclass
class scnfppGenderSpecificParams(Chunk):
	gender_mask: scnGenderMask = field(default_factory=lambda: scnGenderMask(4))
	transition_blend_in_trajectory_space_angles: list[EulerAngles] = field(default_factory=list)
	transition_blend_in_camera_space: list[float] = field(default_factory=list)
	transition_end_input_angles: list[EulerAngles] = field(default_factory=list)
	idle_camera_ls: EulerAngles = field(default_factory=EulerAngles)
	idle_control_camera_ms: EulerAngles = field(default_factory=EulerAngles)


@dataclass
class scnPlayFPPControlAnimEvent(scnPlayAnimEvent):
	# TODO: duration: int = 1000
	# TODO: neck_weight = 1.0
	# TODO: upper_face_blend_additive = True
	# TODO: lower_face_blend_additive = True
	# TODO: eyes_blend_additive = True
	# TODO: fpp_control_active = True
	gameplay_anim_name: scnAnimName = field(default_factory=scnAnimName)
	fppcontrol_active: bool = False
	blend_override: enums.scnfppBlendOverride = enums.scnfppBlendOverride.Centering
	camera_use_trajectory_space: bool = True
	camera_blend_in_duration: float = 0.5
	camera_blend_out_duration: float = 0.5
	stay_in_scene: bool = False
	idle_is_mounted_workspot: bool = False
	enable_world_space_smoothing: bool = True
	is_scene_carrying: bool = False
	camera_parallax_weight: float = 0.0
	camera_parallax_space: enums.scnfppParallaxSpace = enums.scnfppParallaxSpace.Trajectory
	vehicle_procedural_camera_weight: float = 0.0
	yaw_limit_left: float = 0.0
	yaw_limit_right: float = 0.0
	pitch_limit_top: float = 0.0
	pitch_limit_bottom: float = 0.0
	gender_specific_params: list[scnfppGenderSpecificParams] = field(default_factory=list)


@dataclass
class scnPlayRidAnimEvent(scnPlayFPPControlAnimEvent):
	rid_versinon: int = 0
	anim_res_ref_id: scnRidAnimationSRRefId = field(default_factory=scnRidAnimationSRRefId)
	anim_origin_marker: scnMarker = field(default_factory=scnMarker)
	actor_placement: enums.scnRidActorPlacement = enums.scnRidActorPlacement.SceneOrigin
	actor_has_collision: bool = True
	blend_in_trajectory_bone: float = 0.0


@dataclass
class scnPlaySkAnimEvent(scnPlayFPPControlAnimEvent):
	anim_name: scnAnimName = field(default_factory=scnAnimName)
	pose_blend_out_workspot: scnEventBlendWorkspotSetupParameters = field(
			default_factory=scnEventBlendWorkspotSetupParameters
			)
	root_motion_data: scnPlaySkAnimRootMotionData = field(default_factory=scnPlaySkAnimRootMotionData)
	player_data: scnPlayerAnimData = field(default_factory=scnPlayerAnimData)


@dataclass
class scnRidAnimationContainerSRRefAnimContainerContext(Chunk):
	gender_mask: scnGenderMask = field(default_factory=scnGenderMask)


@dataclass
class scnRidAnimationContainerSRRefAnimContainer(Chunk):
	animation: scnRidAnimationSRRefId = field(default_factory=scnRidAnimationSRRefId)
	context: scnRidAnimationContainerSRRefAnimContainerContext = field(
			default_factory=scnRidAnimationContainerSRRefAnimContainerContext
			)


@dataclass
class scnRidAnimationContainerSRRef(Chunk):
	animations: list[scnRidAnimationContainerSRRefAnimContainer] = field(default_factory=list)


@dataclass
class scnRidAnimationContainerSRRefId(Chunk):
	pass


@dataclass
class scnAnimSetDynAnimNames(Chunk):
	anim_variable: str = ''
	anim_names: list[str] = field(default_factory=list)


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
	player_gender_mask: scnGenderMask = field(default_factory=scnGenderMask)


@dataclass
class scnscreenplayOptionUsage(Chunk):
	player_gender_mask: scnGenderMask = field(default_factory=scnGenderMask)


@dataclass
class scnscreenplayDialogLine(Chunk):
	item_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	speaker: scnActorId = field(default_factory=scnActorId)
	addressee: scnActorId = field(default_factory=scnActorId)
	usage: scnscreenplayLineUsage = field(default_factory=scnscreenplayLineUsage)
	locstring_id: scnlocLocstringId = field(default_factory=scnlocLocstringId)
	male_lipsync_animation_name: bytes = b''
	female_lipsync_animation_name: bytes = b''


@dataclass
class scnscreenplayChoiceOption(Chunk):
	item_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	usage: scnscreenplayOptionUsage = field(default_factory=scnscreenplayOptionUsage)
	locstring_id: scnlocLocstringId = field(default_factory=scnlocLocstringId)


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
	variant_id: scnlocVariantId = field(default_factory=scnlocVariantId)
	content: str = ''


@dataclass
class scnlocLocStoreEmbedded(Chunk):
	vd_entries: list[scnlocLocStoreEmbeddedVariantDescriptorEntry] = field(default_factory=list)
	vp_entries: list[scnlocLocStoreEmbeddedVariantPayloadEntry] = field(default_factory=list)


@dataclass
class scnSceneVOInfo(Chunk):
	in_vo_trigger: str = ''
	out_vo_trigger: str = ''
	duration: float = 0.0
	id: int = 0


@dataclass
class scnWorkspotSymbol(Chunk):
	ws_instance: scnSceneWorkspotInstanceId = field(default_factory=scnSceneWorkspotInstanceId)
	ws_node_id: scnNodeId = field(default_factory=scnNodeId)
	ws_editor_event_id: int = sys.maxsize


@dataclass
class scnSceneEventSymbol(Chunk):
	editor_event_id: int = sys.maxsize
	origin_node_id: scnNodeId = field(default_factory=scnNodeId)
	scene_event_ids: list[scnSceneEventId] = field(default_factory=list)


@dataclass
class scnNodeSymbol(Chunk):
	node_id: scnNodeId = field(default_factory=scnNodeId)
	editor_node_id: scnNodeId = field(default_factory=scnNodeId)
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
	id: scnEffectId = field(default_factory=scnEffectId)
	# TODO: effect: CResourceAsyncReference<worldEffect> = field(default_factory=CResourceAsyncReference<worldEffect>)


@dataclass
class scnEffectInstanceId(Chunk):
	effect_id: scnEffectId = field(default_factory=scnEffectId)
	id: int = sys.maxsize


@dataclass
class scnEffectEntry(Chunk):
	effect_instance_id: scnEffectInstanceId = field(default_factory=scnEffectInstanceId)
	effect_name: str = ''


@dataclass
class scneventsVFXBraindanceEvent(scnSceneEvent):
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''
	effect_entry: scnEffectEntry = field(default_factory=scnEffectEntry)
	sequence_shift: int = 0
	glitch_effect_entry: scnEffectEntry = field(default_factory=scnEffectEntry)
	glitch_sequence_shift: int = 0
	fully_rewindable: bool = False


@dataclass
class scneventsVFXDurationEvent(scnSceneEvent):
	effect_entry: scnEffectEntry = field(default_factory=scnEffectEntry)
	start_action: enums.scneventsVFXActionType = enums.scneventsVFXActionType.Play
	end_action: enums.scneventsVFXActionType = enums.scneventsVFXActionType.Kill
	sequence_shift: int = 0
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''
	mute_sound: bool = False


@dataclass
class scneventsVFXEvent(scnSceneEvent):
	effect_entry: scnEffectEntry = field(default_factory=scnEffectEntry)
	action: enums.scneventsVFXActionType = enums.scneventsVFXActionType.Play
	sequence_shift: int = 0
	performer_id: scnPerformerId = field(default_factory=scnPerformerId)
	node_ref: str = ''
	mute_sound: bool = False


@dataclass
class scnEffectInstance(Chunk):
	effect_instance_id: scnEffectInstanceId = field(default_factory=scnEffectInstanceId)
	compiled_effect: worldCompiledEffectInfo = field(default_factory=worldCompiledEffectInfo)


@dataclass
class scnExecutionTag(Chunk):
	flags: int = 0


@dataclass
class scnReferencePointId(Chunk):
	id: int = sys.maxsize


@dataclass
class scnChoiceNodeNsAdaptiveLookAtReferencePoint(Chunk):
	reference_point: scnReferencePointId = field(default_factory=scnReferencePointId)
	constant_weight: float = 0.0


@dataclass
class scnChoiceNodeNsAdaptiveLookAtParams(scnChoiceNodeNsLookAtParams):
	nearby_slot_name: str = ''
	distant_slot_name: str = ''
	blend_limit: float = 0.0
	reference_point_full_effect_angle: float = 0.0
	reference_point_no_effect_angle: float = 63.0
	reference_point_full_effect_distance: float = 5.0
	reference_point_no_effect_distance: float = 0.0
	reference_points: list[scnChoiceNodeNsAdaptiveLookAtReferencePoint] = field(default_factory=list)
	auxiliary_relative_point: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class scnChoiceNodeOption(Chunk):
	screenplay_option_id: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	caption: str = ''
	blueline: bool = False
	is_fixed_as_read: bool = False
	is_single_choice: bool = False
	type: gameinteractionsChoiceTypeWrapper = field(default_factory=gameinteractionsChoiceTypeWrapper)
	timed_params: scnChoiceNodeNsTimedParams = field(default_factory=scnChoiceNodeNsTimedParams)
	quest_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	trigger_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	blueline_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	emphasis_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	icon_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	gameplay_action: int = 0
	icon_tag_ids: list[int] = field(default_factory=list)
	ex_data_flags: int = 0
	mappin_reference_point_id: scnReferencePointId = field(default_factory=scnReferencePointId)
	timed_condition: scnTimedCondition = field(default_factory=scnTimedCondition)


@dataclass
class scnChoiceNode(scnSceneGraphNode):
	# TODO: localized_display_name_override = new() { Unk1 = 0, Value = "" };
	# TODO: ata_params = new scnChoiceNodeNsAttachToActorParams { ActorId = new scnActorId { Id = sys.maxsize } };
	# TODO: atp_params = new scnChoiceNodeNsAttachToPropParams { PropId = new scnPropId { Id = sys.maxsize }, VisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.inWorld };
	# TODO: atgo_params = new scnChoiceNodeNsAttachToGameObjectParams { VisualizerStyle = enums.scnChoiceNodeNsVisualizerStyle.inWorld };
	# TODO: atw_params = new scnChoiceNodeNsAttachToWorldParams { EntityPosition = new Vector3(), EntityOrientation =  };
	display_name_override: str = ''
	localized_display_name_override: LocalizationString = field(default_factory=LocalizationString)
	options: list[scnChoiceNodeOption] = field(default_factory=list)
	mode: enums.scnChoiceNodeNsOperationMode = enums.scnChoiceNodeNsOperationMode.attachToScreen
	persistent_line_events: list[scnSceneEventId] = field(default_factory=list)
	custom_persistent_line: scnscreenplayItemId = field(default_factory=scnscreenplayItemId)
	timed_params: scnChoiceNodeNsTimedParams = field(default_factory=scnChoiceNodeNsTimedParams)
	reminder_params: scnChoiceNodeNsActorReminderParams = field(default_factory=scnChoiceNodeNsActorReminderParams)
	shape_params: scnInteractionShapeParams = field(default_factory=scnInteractionShapeParams)
	look_at_params: scnChoiceNodeNsLookAtParams = field(default_factory=scnChoiceNodeNsLookAtParams)
	force_attach_to_screen_condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	choice_group: str = ''
	cpo_hold_input_action_section: bool = False
	do_not_turn_off_prevention_system: bool = False
	ata_params: scnChoiceNodeNsAttachToActorParams = field(default_factory=scnChoiceNodeNsAttachToActorParams)
	atp_params: scnChoiceNodeNsAttachToPropParams = field(default_factory=scnChoiceNodeNsAttachToPropParams)
	atgo_params: scnChoiceNodeNsAttachToGameObjectParams = field(
			default_factory=scnChoiceNodeNsAttachToGameObjectParams
			)
	ats_params: scnChoiceNodeNsAttachToScreenParams = field(default_factory=scnChoiceNodeNsAttachToScreenParams)
	atw_params: scnChoiceNodeNsAttachToWorldParams = field(default_factory=scnChoiceNodeNsAttachToWorldParams)
	choice_priority: int = 0
	hub_priority: int = 0
	mappin_params: scnChoiceNodeNsMappinParams = field(default_factory=scnChoiceNodeNsMappinParams)
	interrupt_capability: enums.scnInterruptCapability = enums.scnInterruptCapability.Interruptable
	interruption_speaker_override: scnActorId = field(default_factory=scnActorId)
	# TODO: choice_flags: CBitField<scnChoiceNodeNsChoiceNodeBitFlags> = field(default_factory=CBitField<scnChoiceNodeNsChoiceNodeBitFlags>)
	always_use_brain_gender: bool = False
	timed_section_condition: scnTimedCondition = field(default_factory=scnTimedCondition)
	reminder_condition: scnReminderCondition = field(default_factory=scnReminderCondition)


@dataclass
class scnReferencePointDef(Chunk):
	id: scnReferencePointId = field(default_factory=scnReferencePointId)
	offset: tuple[float, float, float] = (0.0, 0.0, 0.0)
	origin_marker: scnMarker = field(default_factory=scnMarker)


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
	scene_graph: HandleData[scnSceneGraph] = field(default_factory=dict)  # type: ignore[assignment]
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
class scnBraindanceJumpInProgress_ConditionType(scnIBraindanceConditionType):
	in_progress: bool = True
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindanceLayer_ConditionType(scnIBraindanceConditionType):
	layer: enums.scnBraindanceLayer
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindancePaused_ConditionType(scnIBraindanceConditionType):
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindancePerspective_ConditionType(scnIBraindanceConditionType):
	perspective: enums.scnBraindancePerspective
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindancePlaying_ConditionType(scnIBraindanceConditionType):
	speed: enums.scnBraindanceSpeed
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindanceResetting_ConditionType(scnIBraindanceConditionType):
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnBraindanceRewinding_ConditionType(scnIBraindanceConditionType):
	speed: enums.scnBraindanceSpeed = enums.scnBraindanceSpeed.Any
	scene_file: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_version: enums.scnSceneVersionCheck = enums.scnSceneVersionCheck.OlderOrEqual


@dataclass
class scnInterestingConversation_DEPRECATED(Chunk):
	scene_filename: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference


@dataclass
class scnInterestingConversationData(Chunk):
	scene_filename: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	interruption_operations: list[scnIInterruptionOperation] = field(default_factory=list)


@dataclass
class scnInterestingConversationsGroup(Chunk):
	condition: questIBaseCondition = field(default_factory=questIBaseCondition)
	conversations: list[scnInterestingConversationData] = field(default_factory=list)


@dataclass
class scnInterestingConversationsResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	conversation_groups: list[scnInterestingConversationsGroup] = field(default_factory=list)


@dataclass
class scnScenesVersionsChangedRecord(Chunk):
	change_in_version: int = 0
	scene_before_change: scnSceneResource = field(
			default_factory=scnSceneResource
			)  # TODO: CResourceAsyncReference


@dataclass
class scnScenesVersionsSceneChanges(Chunk):
	scene: scnSceneResource = field(default_factory=scnSceneResource)  # TODO: CResourceAsyncReference
	scene_changes: list[scnScenesVersionsChangedRecord] = field(default_factory=list)


@dataclass
class scnCheckSpeakersDistanceInterruptConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnCheckSpeakersDistanceReturnConditionParams(Chunk):
	distance: float = 0.0
	comparison_type: enums.EComparisonType = enums.EComparisonType.Greater


@dataclass
class scnCheckSpeakersDistanceInterruptCondition(scnIInterruptCondition):
	params: scnCheckSpeakersDistanceInterruptConditionParams = field(
			default_factory=lambda: scnCheckSpeakersDistanceInterruptConditionParams(distance=6.0)
			)


@dataclass
class scnCheckSpeakersDistanceReturnCondition(scnIReturnCondition):
	params: scnCheckSpeakersDistanceReturnConditionParams = field(
			default_factory=scnCheckSpeakersDistanceReturnConditionParams
			)
