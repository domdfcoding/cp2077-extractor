#!/usr/bin/env python3
#
#  game.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``game``).
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
from cp2077_extractor.cr2w.datatypes.base import CColor, Chunk, CMatrix, Sphere
from cp2077_extractor.cr2w.datatypes.ent import (
		entBaseCameraComponent,
		entEntityID,
		entGameEntity,
		entIAttachment,
		entIComponent,
		entIPlacedComponent,
		entLightComponent,
		entSlotComponent
		)
from cp2077_extractor.cr2w.datatypes.ink import inkanimDefinition, inkanimProxy, inkWidget
from cp2077_extractor.cr2w.datatypes.world import (
		worldAreaShapeNode,
		worldAreaShapeNodeInstance,
		worldEffectBlackboard,
		worldIRuntimeSystem,
		worlduiIWidgetGameController
		)

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.datatypes.physics import (
			physicsFilterData,
			physicsMaterialReference,
			physicsQueryPreset
			)
	from cp2077_extractor.cr2w.datatypes.work import WorkspotMapperComponent

# TODO: some classes belong in new modules

__all__ = [
		"AuthorizationData",
		"BackDoorObjectiveData",
		"BaseScriptableAction",
		"BaseSkillCheckContainer",
		"ClueRecordData",
		"ConditionGroupData",
		"ControlPanelObjectiveData",
		"DamageStatListener",
		"DemolitionSkillCheck",
		"DestructionData",
		"DeviceActionQueue",
		"DeviceOperationBase",
		"DeviceOperationsContainer",
		"DeviceOperationsTrigger",
		"DisassembleOptions",
		"ElectricLightController",
		"ElectricLightControllerPS",
		"EngineeringSkillCheck",
		"FocusClueDefinition",
		"FocusForcedHighlightData",
		"GameLoadedFactReset",
		"GameObjectListener",
		"GameplayConditionBase",
		"GameplayConditionContainer",
		"GameplayLightController",
		"GameplayLightControllerPS",
		"GameplaySkillCondition",
		"GemplayObjectiveData",
		"HackingSkillCheck",
		"HighlightInstance",
		"IllegalActionTypes",
		"ModuleInstance",
		"ObjectScanningDescription",
		"OverheatStatListener",
		"SActionWidgetPackage",
		"SFactOperationData",
		"SHitFlag",
		"SHitStatusEffect",
		"SPerformedActions",
		"SToggleDeviceOperationData",
		"SWeaponPlaneParams",
		"SWidgetPackage",
		"SWidgetPackageBase",
		"ScriptableDeviceAction",
		"ScriptableDeviceComponent",
		"ScriptableDeviceComponentPS",
		"SecurityAccessLevelEntry",
		"SecurityAccessLevelEntryClient",
		"SecuritySystemClearanceEntry",
		"SharedGameplayPS",
		"SkillCheckBase",
		"SpiderbotScavengeOptions",
		"StartOverheatEffectEvent",
		"UpdateDamageChangeEvent",
		"UpdateOverheatEvent",
		"WeaponChargeStatListener",
		"WidgetCustomData",
		"gameAttackComputed",
		"gameBaseGameSession",
		"gameBaseTimer",
		"gameCameraComponent",
		"gameComponent",
		"gameComponentPS",
		"gameCooldownSystemEvent",
		"gameCustomValueStatPoolsListener",
		"gameDeactivateTPPRepresentationEvent",
		"gameDeactivateTriggerDestructionComponentEvent",
		"gameDebugCheatsSystem",
		"gameDebugContextPtr",
		"gameDebugContextUserData",
		"gameDebugDrawHistorySystem",
		"gameDebugFreeCamera",
		"gameDebugPerformanceSystem",
		"gameDebugPlayerBreadcrumbs",
		"gameDebugTimeState",
		"gameDebugVisualizerSystem",
		"gameDelayID",
		"gameDelaySystem",
		"gameDelaySystemCallbackInfo",
		"gameDelaySystemDelayStruct",
		"gameDelaySystemEventStruct",
		"gameDelaySystemPSEventStruct",
		"gameDelaySystemScriptableSysRequestStruct",
		"gameDelaySystemScriptedDelayCallbackWrapper",
		"gameDelaySystemTickOnEventStruct",
		"gameDelaySystemTickStruct",
		"gameDelaySystemTickWithCallbackStruct",
		"gameDependentWorkspotData",
		"gameDeprecated_GameplayEvent",
		"gameDestructibleSpotsSystem",
		"gameDestructionPersistencySystem",
		"gameDeviceCameraControlComponent",
		"gameDeviceComponent",
		"gameDeviceComponentPS",
		"gameDeviceDynamicConnectionChange",
		"gameDeviceInteractionManager",
		"gameDeviceLoaded",
		"gameDevicePSChanged",
		"gameDeviceReplicatedState",
		"gameDeviceSystem",
		"gameDisableAimAssist",
		"gameDynamicEntityHandler",
		"gameDynamicEntityIDSystem",
		"gameDynamicEventNodeInstance",
		"gameDynamicSpawnSystem",
		"gameEffectAction",
		"gameEffectAttachment",
		"gameEffectData",
		"gameEffectData_MeleeTireHit",
		"gameEffectData_MeleeWaterFx",
		"gameEffectData_Pierce",
		"gameEffectData_PiercePreview",
		"gameEffectData_Splatter",
		"gameEffectData_SplatterList",
		"gameEffectDebugSettings",
		"gameEffectDefinition",
		"gameEffectDurationModifier",
		"gameEffectDurationModifierScriptContext",
		"gameEffectDurationModifier_Scripted",
		"gameEffectDuration_Duration_Blackboard",
		"gameEffectDuration_Infinite",
		"gameEffectDuration_Instant",
		"gameEffectExecutionScriptContext",
		"gameEffectExecutor",
		"gameEffectExecutor_DamageProjection",
		"gameEffectExecutor_LandingFX",
		"gameEffectExecutor_NewEffect",
		"gameEffectExecutor_NewEffect_CopyData",
		"gameEffectExecutor_NewEffect_ReflectedVector",
		"gameEffectExecutor_PhysicalImpulseFromInstigator",
		"gameEffectExecutor_Scripted",
		"gameEffectExecutor_SendStatusEffect",
		"gameEffectExecutor_SendStimuli",
		"gameEffectExecutor_TriggerDestruction",
		"gameEffectExecutor_UpdateMeleeTireHit",
		"gameEffectInfo",
		"gameEffectInstance",
		"gameEffectNode",
		"gameEffectObjectFilter",
		"gameEffectObjectFilter_Cone",
		"gameEffectObjectFilter_HitRepresentation",
		"gameEffectObjectFilter_HitRepresentation_Quickhack",
		"gameEffectObjectFilter_HitRepresentation_Sphere",
		"gameEffectObjectFilter_HitRepresentation_SweepOverTime_Box",
		"gameEffectObjectFilter_HitRepresentation_Sweep_Box",
		"gameEffectObjectFilter_IgnoreMountedVehicle",
		"gameEffectObjectFilter_NearestWeakspotIfAny",
		"gameEffectObjectFilter_NoDuplicates",
		"gameEffectObjectFilter_NoInstigator",
		"gameEffectObjectFilter_NoInstigatorIfPlayerControlled",
		"gameEffectObjectFilter_NoPlayer",
		"gameEffectObjectFilter_NoPuppet",
		"gameEffectObjectFilter_NoSource",
		"gameEffectObjectFilter_NoWeapon",
		"gameEffectObjectFilter_NotAlive",
		"gameEffectObjectFilter_TechPreview",
		"gameEffectObjectFilter_Unique",
		"gameEffectObjectGroupFilter",
		"gameEffectObjectGroupFilter_Cone",
		"gameEffectObjectGroupFilter_Scripted",
		"gameEffectObjectProvider",
		"gameEffectObjectProvider_ProjectileHitEvent",
		"gameEffectObjectProvider_QueryCapsule",
		"gameEffectObjectProvider_QueryCapsule_GrowOverTime",
		"gameEffectObjectProvider_QueryShockwave",
		"gameEffectObjectProvider_QuerySphere",
		"gameEffectObjectProvider_QuerySphere_GrowOverTime",
		"gameEffectObjectProvider_Scripted",
		"gameEffectObjectProvider_SingleEntity",
		"gameEffectObjectProvider_Stimuli_EntitiesInRange",
		"gameEffectObjectProvider_SweepMelee_Box",
		"gameEffectObjectProvider_SweepMelee_MantisBlades",
		"gameEffectObjectProvider_SweepOverTime",
		"gameEffectObjectSingleFilter",
		"gameEffectObjectSingleFilter_Scripted",
		"gameEffectPostAction",
		"gameEffectPostAction_BeamVFX",
		"gameEffectPostAction_BulletTrace",
		"gameEffectPostAction_MeleeTireHit",
		"gameEffectPostAction_MeleeWaterEffects",
		"gameEffectPostAction_ProcessNearlyHitAgents",
		"gameEffectPostAction_Scripted",
		"gameEffectPostAction_UpdateActiveVehicleUIData",
		"gameEffectPostAction_WaterImpulse",
		"gameEffectPreAction",
		"gameEffectPreAction_Scripted",
		"gameEffectPreAction_SpreadingEffect",
		"gameEffectPreloadScriptContext",
		"gameEffectProviderScriptContext",
		"gameEffectScriptContext",
		"gameEffectSet",
		"gameEffectSettings",
		"gameEffectSingleFilterScriptContext",
		"gameEffectSpawnerSaveSystem",
		"gameEffectSystem",
		"gameEffectTriggerNodeInstance",
		"gameEffectTriggerSystem",
		"gameEffector",
		"gameEffectorObject",
		"gameEffectorSystem",
		"gameEnableAimAssist",
		"gameEngineTurnedOffEvent",
		"gameEngineTurnedOnEvent",
		"gameEntitiesWithStatusEffectPrereq",
		"gameEntitiesWithStatusEffectPrereqState",
		"gameEntityIDArrayPrereq",
		"gameEntityIDArrayPrereqState",
		"gameEntityIDPool",
		"gameEntityReference",
		"gameEntitySpawnerEventsBroadcasterImpl",
		"gameEntityStubSystem",
		"gameEnumNameToIndexCache",
		"gameEnvironmentDamageSystem",
		"gameEquippedPrereqListener",
		"gameEquippedPrereqState",
		"gameEthnicityPicker",
		"gameExternalMovementCameraDataEvent",
		"gameExtraStatPoolDataModifierStatListener",
		"gameFinalTimeState",
		"gameFinalizeActivationTPPRepresentationEvent",
		"gameFinalizeDeactivationTPPRepresentationEvent",
		"gameFootstepEvent",
		"gameFootstepSystem",
		"gameForceResetAmmoEvent",
		"gameFreeCameraComponent",
		"gameFriendlyFireSystem",
		"gameFxInstance",
		"gameFxSystem",
		"gameGOGRewardsSystem",
		"gameGameFeatureManager",
		"gameGameRulesSystem",
		"gameGameSession",
		"gameGameSessionDesc",
		"gameGameTagSystem",
		"gameGameplayLogicPackageSystem",
		"gameGarmentItemObject",
		"gameGeometryDescriptionSystem",
		"gameGodModeSystem",
		"gameGrenadeThrowQuery",
		"gameHalloweenEvent",
		"gameHasDialogVisualizerVisiblePrereq",
		"gameHasDialogVisualizerVisiblePrereqState",
		"gameHitRepresentationOverride",
		"gameHitRepresentationSystem",
		"gameHitResult",
		"gameHitShapeContainer",
		"gameHitShapeUserData",
		"gameIAIDirectorSystem",
		"gameIAchievementSystem",
		"gameIActionsFactory",
		"gameIActivityCardsSystem",
		"gameIActivityLogSystem",
		"gameIAreaManager",
		"gameIAttachmentSlotsListener",
		"gameIAttack",
		"gameIAttitudeManager",
		"gameIAutoSaveSystem",
		"gameIBlackboard",
		"gameIBlackboardSystem",
		"gameIBlackboardUpdateProxy",
		"gameIBreachSystem",
		"gameICameraSystem",
		"gameIClientEntitySpawnSystem",
		"gameICollisionQueriesSystem",
		"gameICombatQueriesSystem",
		"gameICommunitySystem",
		"gameICompanionSystem",
		"gameIComparisonPrereq",
		"gameIComponentsStateSystem",
		"gameIContainerManager",
		"gameICooldownSystem",
		"gameIDamageSystem",
		"gameIDamageSystemListener",
		"gameIDebugCheatsSystem",
		"gameIDebugDrawHistorySystem",
		"gameIDebugPlayerBreadcrumbs",
		"gameIDebugSystem",
		"gameIDebugVisualizerSystem",
		"gameIDelaySystem",
		"gameIDestructionPersistencySystem",
		"gameIDeviceInteractionManager",
		"gameIDeviceSystem",
		"gameIDynamicEntityIDSystem",
		"gameIDynamicSpawnSystem",
		"gameIEffect",
		"gameIEffectInputParameter",
		"gameIEffectOutputParameter",
		"gameIEffectParameter_BoolEvaluator",
		"gameIEffectParameter_CNameEvaluator",
		"gameIEffectParameter_FloatEvaluator",
		"gameIEffectParameter_IntEvaluator",
		"gameIEffectParameter_QuatEvaluator",
		"gameIEffectParameter_StringEvaluator",
		"gameIEffectParameter_VectorEvaluator",
		"gameIEffectSpawnerSaveSystem",
		"gameIEffectSystem",
		"gameIEffectTriggerSystem",
		"gameIEffectorSystem",
		"gameIEntitySpawnerEventsBroadcaster",
		"gameIEntityStubSystem",
		"gameIEnvironmentDamageSystem",
		"gameIEquipmentSystem",
		"gameIFinisherScenario",
		"gameIFootstepSystem",
		"gameIFriendlyFireSystem",
		"gameIFxSystem",
		"gameIGameAudioSystem",
		"gameIGameRulesSystem",
		"gameIGameSystem",
		"gameIGameSystemReplicatedState",
		"gameIGameplayLogicPackageSystem",
		"gameIGlobalTvSystem",
		"gameIGodModeSystem",
		"gameIHitRepresentationSystem",
		"gameIHitShape",
		"gameIInventoryListener",
		"gameIInventoryManager",
		"gameIItemFactorySystem",
		"gameIJournalManager",
		"gameILevelAssignmentSystem",
		"gameILocationManager",
		"gameILootManager",
		"gameIMarketSystem",
		"gameIMinimapSystem",
		"gameIMovingPlatformMovement",
		"gameIMovingPlatformMovementInitData",
		"gameIMovingPlatformMovementPointToPoint",
		"gameIMovingPlatformSystem",
		"gameIMuppetInputAction",
		"gameIObjectCarrySystem",
		"gameIObjectPoolSystem",
		"gameIOnlineSystem",
		"gameIPersistencySystem",
		"gameIPhantomEntitySystem",
		"gameIPhotoModeSystem",
		"gameIPingSystem",
		"gameIPlayerHandicapSystem",
		"gameIPlayerManager",
		"gameIPlayerSystem",
		"gameIPoliceRadioSystem",
		"gameIPopulationSystem",
		"gameIPrereq",
		"gameIPrereqManager",
		"gameIPreventionSpawnSystem",
		"gameIProjectileSystem",
		"gameIPuppetUpdaterSystem",
		"gameIRPGPrereq",
		"gameIRazerChromaEffectsSystem",
		"gameIRealTimeEventSystem",
		"gameIRenderGameplayEffectsManagerSystem",
		"gameIReplicatedGameSystem",
		"gameIRichPresenceSystem",
		"gameISaveSanitizationForbiddenAreaSystem",
		"gameISceneSystem",
		"gameISchematicSystem",
		"gameIScriptablePrereq",
		"gameIScriptableSystem",
		"gameIScriptableSystemsContainer",
		"gameIScriptsDebugOverlaySystem",
		"gameIShootingAccuracySystem",
		"gameISpatialQueriesSystem",
		"gameIStatPoolsListener",
		"gameIStatPoolsSystem",
		"gameIStatsDataSystem",
		"gameIStatsListener",
		"gameIStatsSystem",
		"gameIStatusComboSystem",
		"gameIStatusEffectListener",
		"gameIStatusEffectSystem",
		"gameIStimuliSystem",
		"gameIStreamingMonitorSystem",
		"gameISubtitleHandlerSystem",
		"gameITargetingSystem",
		"gameITelemetrySystem",
		"gameITeleportationFacility",
		"gameITierSystem",
		"gameITimeState",
		"gameITimeSystem",
		"gameITransactionSystem",
		"gameITransformAnimatorSaveSystem",
		"gameITransformsHistorySystem",
		"gameIVehicleSystem",
		"gameIVisionModeSystem",
		"gameIWardrobeSystem",
		"gameIWatchdogSystem",
		"gameIWorkspotGameSystem",
		"gameIWorldBoundarySystem",
		"gameImpostorComponentAttachEvent",
		"gameImpostorComponentSlotListener",
		"gameInCrowd",
		"gameInnerItemData",
		"gameInputTriggerState",
		"gameIntervalTimer",
		"gameInventoryChangedEvent",
		"gameInventoryListenerData_Base",
		"gameInventoryListenerData_InventoryEmpty",
		"gameInventoryListenerData_ItemAdded",
		"gameInventoryListenerData_ItemExtracted",
		"gameInventoryListenerData_ItemNotification",
		"gameInventoryListenerData_ItemQuantityChanged",
		"gameInventoryListenerData_ItemRemoved",
		"gameInventoryListenerData_PartAdded",
		"gameInventoryListenerData_PartRemoved",
		"gameInventoryManager",
		"gameInventoryPrereqState",
		"gameInventoryScriptListener",
		"gameIsQuickhackPanelOpenedPrereqState",
		"gameIsVisualizerActivePrereq",
		"gameIsVisualizerActivePrereqState",
		"gameItemCreationPrereqDataWrapper",
		"gameItemData",
		"gameItemDecorationEvent",
		"gameItemDropStorageInventoryListener",
		"gameItemDropStorageManager",
		"gameItemEventsEquippedToObject",
		"gameItemEventsPropagateRenderingPlane",
		"gameItemEventsRemoveActiveItem",
		"gameItemEventsUnequipStarted",
		"gameItemEventsUnequippedFromObject",
		"gameItemFactorySystem",
		"gameItemFactorySystemPool",
		"gameItemObject",
		"gameItemsMeshesLoaded",
		"gameJoinTrafficSettings",
		"gameJournalBriefingBaseSection",
		"gameJournalContainerEntry",
		"gameJournalEntry",
		"gameJournalEntryOverrideData",
		"gameJournalFileEntry",
		"gameJournalFolderEntry",
		"gameJournalManager",
		"gameJournalOnscreensStructuredGroup",
		"gameJournalPrimaryFolderEntry",
		"gameKillTriggerNode",
		"gameKillTriggerNodeInstance",
		"gameLazyDevice",
		"gameLevelAssignmentSystem",
		"gameLoSFinderParams",
		"gameLoSFinderSystem",
		"gameLoSIFinderSystem",
		"gameLocationManager",
		"gameLookAtFacingPositionProvider",
		"gameLootBagInventoryListener",
		"gameLootContainerBase",
		"gameLootManager",
		"gameLootSlot",
		"gameLootSlotSingleItem",
		"gameLootSlotSingleItemLongStreaming",
		"gameMakeInventoryShareableEvent",
		"gameMappinUtils",
		"gameMinimapSystem",
		"gameModdingSystem",
		"gameMovingPlatformBeforeArrivedAt",
		"gameMovingPlatformMoveTo",
		"gameMovingPlatformRestoreMoveTo",
		"gameMovingPlatformSystem",
		"gameMuppetComponent",
		"gameMuppetInputActionActivateScanning",
		"gameMuppetInputActionAimDownSight",
		"gameMuppetInputActionCrouch",
		"gameMuppetInputActionJump",
		"gameMuppetInputActionMeleeAttack",
		"gameMuppetInputActionQuickMelee",
		"gameMuppetInputActionReloadWeapon",
		"gameMuppetInputActionUseConsumable",
		"gameMuppetInventoryGameController",
		"gameMuppetLoadoutsGameController",
		"gameMuppetStates",
		"gameNPCHealthStatPoolsListener",
		"gameNPCQuickHackUploadStatPoolsListener",
		"gameNPCStatsListener",
		"gameNarrationPlateBlackboardUpdater",
		"gameNativeAutodriveSystem",
		"gameNativeHudManager",
		"gameNetrunnerPrototypeDespawnEvent",
		"gameNotPrereqState",
		"gameObject",
		"gameObjectActionRefreshEvent",
		"gameObjectActionsCallbackController",
		"gameObjectCarrierComponentAttached",
		"gameObjectCarrierComponentDetached",
		"gameObjectCarrySystem",
		"gameObjectDeathListener",
		"gameObjectPS",
		"gameObjectPoolSystem",
		"gameObjectSpawnParameter",
		"gameOffPavement",
		"gameOnExecutionContext",
		"gameOnInventoryEmptyEvent",
		"gameOnLootAllEvent",
		"gameOnLootEvent",
		"gameOnPavement",
		"gameOnScannableBraindanceClueDisabledEvent",
		"gameOnScannableBraindanceClueEnabledEvent",
		"gameOutOfCrowd",
		"gamePSChangedEvent",
		"gamePatrolSplineControlPoint",
		"gamePersistencySystem",
		"gamePersistentID",
		"gamePersistentState",
		"gamePhantomEntitySystem",
		"gamePhotoModeAttachmentSlotsListener",
		"gamePhotoModeAutoFocusPositionProvider",
		"gamePhotoModeCameraObject",
		"gamePhotoModeEnableEvent",
		"gamePhotoModeObjectPositionProvider",
		"gamePhotoModeSystem",
		"gamePhotoModeUtils",
		"gamePhotomodeLightComponent",
		"gamePhotomodeLightObject",
		"gamePingSystem",
		"gamePlayerArmorStatPoolsListener",
		"gamePlayerAttachRequest",
		"gamePlayerCoverInfo",
		"gamePlayerHealthStatPoolsListener",
		"gamePlayerManager",
		"gamePlayerObstacleSystem",
		"gamePlayerProximityPrereqState",
		"gamePlayerReleaseControlAsChild",
		"gamePlayerScriptableSystemRequest",
		"gamePlayerSocket",
		"gamePlayerStatsListener",
		"gamePlayerSystem",
		"gamePlayerTakeControlAsChild",
		"gamePlayerTakeControlAsParent",
		"gamePopulationSystem",
		"gamePrepareTPPRepresentationEvent",
		"gamePrereqManager",
		"gamePrereqState",
		"gamePrereqStateChangedEvent",
		"gamePreventionSpawnSystem",
		"gamePreviewItemData",
		"gameProjectileSystem",
		"gamePuppet",
		"gamePuppetBase",
		"gamePuppetBlackboardUpdater",
		"gamePuppetStatPoolsListener",
		"gamePuppetStatsListener",
		"gamePuppetStatusEffectListener",
		"gamePuppetUpdaterSystem",
		"gameQueryResult",
		"gameQuestOrSceneSetVehiclePhysicsActive",
		"gameRPGManager",
		"gameRPGPrereqState",
		"gameRandomStatModifier",
		"gameRazerChromaEffectsSystem",
		"gameRealTimeEventSystem",
		"gameRecordIdSpawnModifier",
		"gameRegenerateLootEvent",
		"gameRemains",
		"gameRemoveCooldownEvent",
		"gameRenderGameplayEffectsManagerSystem",
		"gameReplAnimTransformRequestBase",
		"gameReplAnimTransformSyncAnimRequest",
		"gameRequestStats",
		"gameResetContainerEvent",
		"gameRichPresenceSystem",
		"gameRicochetData",
		"gameRuntimeSystemLights",
		"gameSaveSanitizationForbiddenAreaSystem",
		"gameScanningActionFinishedEvent",
		"gameScanningComponent",
		"gameScanningController",
		"gameScanningEvent",
		"gameScanningEventForInstigator",
		"gameScanningInternalEvent",
		"gameScanningPulseEvent",
		"gameScanningTooltipElementDef",
		"gameScenePlayerAnimationParams",
		"gameSceneTier",
		"gameSceneTierData",
		"gameScreenshot360CameraComponent",
		"gameScriptStatPoolsListener",
		"gameScriptStatsListener",
		"gameScriptableComponent",
		"gameScriptableSystem",
		"gameScriptableSystemRequest",
		"gameScriptableSystemsContainer",
		"gameScriptedDamageSystemListener",
		"gameScriptedPrereqAttitudeListenerWrapper",
		"gameScriptedPrereqMountingListenerWrapper",
		"gameShapeData",
		"gameStatModifierBase",
		"gameStatPoolDataModifierStatListener",
		"gameStatusEffectComponent",
		"gameTargetShootComponent",
		"gameTier3CameraSettings",
		"gameTimeDilatable",
		"gameUniqueItemData",
		"gameVisionModeComponent",
		"gameVisionModeSystemRevealIdentifier",
		"gamedamageAttackData",
		"gamedataAccuracy_Record",
		"gamedataArcadeCollidableObject_Record",
		"gamedataArcadeGameplay_Record",
		"gamedataArcadeObject_Record",
		"gamedataBaseObject_Record",
		"gamedataBaseSign_Record",
		"gamedataBase_MappinDefinition_Record",
		"gamedataCharacter_Record",
		"gamedataConstantStatModifier_Record",
		"gamedataContentAssignment_Record",
		"gamedataCoverSelectionParameters_Record",
		"gamedataDamageType_Record",
		"gamedataDataNode",
		"gamedataDeviceScreenType_Record",
		"gamedataDevice_Record",
		"gamedataDriveHelper_Record",
		"gamedataEffectorTimeDilationDriver_Record",
		"gamedataEffector_Record",
		"gamedataEnvLight_Record",
		"gamedataEquipSlot_Record",
		"gamedataEquipmentArea_Record",
		"gamedataEquipmentMovementSound_Record",
		"gamedataEthnicNames_Record",
		"gamedataEthnicity_Record",
		"gamedataFacialPreset_Record",
		"gamedataFastTravelBinkData_Record",
		"gamedataFastTravelBinksGroup_Record",
		"gamedataFastTravelPoint_Record",
		"gamedataFastTravelScreenDataGroup_Record",
		"gamedataFastTravelScreenData_Record",
		"gamedataFastTravelSystem_Record",
		"gamedataFocusClue_Record",
		"gamedataFootstep_Record",
		"gamedataForceDismembermentEffector_Record",
		"gamedataFriendlyTargetAngleDistanceCoverSelectionParameters_Record",
		"gamedataFriendlyTargetDistanceCoverSelectionParameters_Record",
		"gamedataFxActionType_Record",
		"gamedataFxAction_Record",
		"gamedataGOGReward_Record",
		"gamedataGadget_Record",
		"gamedataGameplayAbilityGroup_Record",
		"gamedataGameplayAbility_Record",
		"gamedataGameplayLogicPackageUIData_Record",
		"gamedataGameplayLogicPackage_Record",
		"gamedataGameplayRestrictionStatusEffect_Record",
		"gamedataGameplayTagsPrereq_Record",
		"gamedataGenderEntity_Record",
		"gamedataGender_Record",
		"gamedataGenericHighwaySign_Record",
		"gamedataGenericMetroSign_Record",
		"gamedataGenericStreetNameSign_Record",
		"gamedataGrenadeDeliveryMethodType_Record",
		"gamedataGrenadeDeliveryMethod_Record",
		"gamedataGrenade_Record",
		"gamedataHUD_Preset_Entry_Record",
		"gamedataHackCategory_Record",
		"gamedataHackingMiniGame_Record",
		"gamedataHandbrakeFrictionModifier_Record",
		"gamedataHandicapLootList_Record",
		"gamedataHandicapLootPreset_Record",
		"gamedataHitPrereqConditionType_Record",
		"gamedataHitPrereqCondition_Record",
		"gamedataHitPrereq_Record",
		"gamedataHomingGDM_Record",
		"gamedataHomingParameters_Record",
		"gamedataHudEnhancer_Record",
		"gamedataIPrereq_Record",
		"gamedataIconsGeneratorContext_Record",
		"gamedataImprovementRelation_Record",
		"gamedataInAirGravityModifier_Record",
		"gamedataInitLoadingScreen_Record",
		"gamedataInteractionBase_Record",
		"gamedataInteractionMountBase_Record",
		"gamedataInventoryItemGroup_Record",
		"gamedataInventoryItemSet_Record",
		"gamedataInventoryItem_Record",
		"gamedataIsHackable_Record",
		"gamedataItemAction_Record",
		"gamedataItemArrayQuery_Record",
		"gamedataItemBlueprintElement_Record",
		"gamedataItemBlueprint_Record",
		"gamedataItemCategory_Record",
		"gamedataItemCost_Record",
		"gamedataItemCreationPrereq_Record",
		"gamedataItemDropSettings_Record",
		"gamedataItemList_Record",
		"gamedataItemPartConnection_Record",
		"gamedataItemPartListElement_Record",
		"gamedataItemQueryElement_Record",
		"gamedataItemQuery_Record",
		"gamedataItemRecipe_Record",
		"gamedataItemRequiredSlot_Record",
		"gamedataItemStructure_Record",
		"gamedataItemType_Record",
		"gamedataItem_Record",
		"gamedataItemsFactoryAppearanceSuffixBase_Record",
		"gamedataItemsFactoryAppearanceSuffixOrder_Record",
		"gamedataJournalIcon_Record",
		"gamedataKeepCurrentCoverCoverSelectionParameters_Record",
		"gamedataKnifeThrowDelivery_Record",
		"gamedataLCDScreen_Record",
		"gamedataLandingFxMaterial_Record",
		"gamedataLandingFxPackage_Record",
		"gamedataLayout_Record",
		"gamedataLifePath_Record",
		"gamedataLightPreset_Record",
		"gamedataLinearAccuracy_Record",
		"gamedataLoadingTipsGroup_Record",
		"gamedataLocomotionMode_Record",
		"gamedataLookAtPart_Record",
		"gamedataLookAtPreset_Record",
		"gamedataLootInjectionSettings_Record",
		"gamedataLootItem_Record",
		"gamedataLootTableElement_Record",
		"gamedataLootTable_Record",
		"gamedataMappinClampingSettings_Record",
		"gamedataMappinDefinition_Record",
		"gamedataMappinPhaseDefinition_Record",
		"gamedataMappinPhase_Record",
		"gamedataMappinUICustomOpacityParams_Record",
		"gamedataMappinUIFilterGroup_Record",
		"gamedataMappinUIGlobalProfile_Record",
		"gamedataMappinUIParamGroup_Record",
		"gamedataMappinUIPreventionSettings_Record",
		"gamedataMappinUIRuntimeProfile_Record",
		"gamedataMappinUISettings_Record",
		"gamedataMappinUISpawnProfile_Record",
		"gamedataMappinVariant_Record",
		"gamedataMappinsGroup_Record",
		"gamedataMaterialFx_Record",
		"gamedataMaterial_Record",
		"gamedataMeleeAttackDirection_Record",
		"gamedataMetaQuest_Record",
		"gamedataMiniGame_AllSymbols_Record",
		"gamedataMiniGame_AllSymbols_inline0_Record",
		"gamedataMiniGame_AllSymbols_inline1_Record",
		"gamedataMiniGame_AllSymbols_inline2_Record",
		"gamedataMiniGame_AllSymbols_inline3_Record",
		"gamedataMiniGame_AllSymbols_inline4_Record",
		"gamedataMiniGame_SymbolsWithRarity_Record",
		"gamedataMiniGame_Trap_Record",
		"gamedataMinigameActionType_Record",
		"gamedataMinigameAction_Record",
		"gamedataMinigameCategory_Record",
		"gamedataMinigameTrapType_Record",
		"gamedataMinigame_Def_Record",
		"gamedataModifyAttackCritChanceEffector_Record",
		"gamedataModifyStaminaHandlerEffector_Record",
		"gamedataModifyStatPoolCustomLimitEffector_Record",
		"gamedataModifyStatPoolModifierEffector_Record",
		"gamedataModifyStatPoolValueEffector_Record",
		"gamedataMovementParam_Record",
		"gamedataMovementParams_Record",
		"gamedataMovementPolicyTagList_Record",
		"gamedataMovementPolicy_Record",
		"gamedataMultiPrereq_Record",
		"gamedataMutablePoolValueModifier_Record",
		"gamedataNPCBehaviorState_Record",
		"gamedataNPCEquipmentGroupEntry_Record",
		"gamedataNPCEquipmentGroup_Record",
		"gamedataNPCEquipmentItemPool_Record",
		"gamedataNPCEquipmentItem_Record",
		"gamedataNPCEquipmentItemsPoolEntry_Record",
		"gamedataNPCHighLevelState_Record",
		"gamedataNPCQuestAffiliation_Record",
		"gamedataNPCRarity_Record",
		"gamedataNPCStanceState_Record",
		"gamedataNPCTypePrereq_Record",
		"gamedataNPCType_Record",
		"gamedataNPCUpperBodyState_Record",
		"gamedataNetworkPingingParameteres_Record",
		"gamedataNetworkPresetBinderParameters_Record",
		"gamedataNewPerkCategory_Record",
		"gamedataNewPerkLevelData_Record",
		"gamedataNewPerkLevelUIData_Record",
		"gamedataNewPerkSlot_Record",
		"gamedataNewPerkTier_Record",
		"gamedataNewPerk_Record",
		"gamedataNewSkillsProficiency_Record",
		"gamedataNewsFeedTitle_Record",
		"gamedataNonLinearAccuracy_Record",
		"gamedataNumberPlate_Record",
		"gamedataObjectActionCost_Record",
		"gamedataObjectActionEffect_Record",
		"gamedataObjectActionGameplayCategory_Record",
		"gamedataObjectActionPrereq_Record",
		"gamedataObjectActionReference_Record",
		"gamedataObjectActionType_Record",
		"gamedataObjectAction_Record",
		"gamedataOffMeshLinkTag_Record",
		"gamedataOutput_Record",
		"gamedataOverrideRangedAttackPackageEffector_Record",
		"gamedataOwnerAngleCoverSelectionParameters_Record",
		"gamedataOwnerDistanceCoverSelectionParameters_Record",
		"gamedataOwnerThreatCoverSelectionParameters_Record",
		"gamedataParentAttachmentType_Record",
		"gamedataParticleDamage_Record",
		"gamedataPassiveProficiencyBonusUIData_Record",
		"gamedataPassiveProficiencyBonus_Record",
		"gamedataPathLengthCoverSelectionParameters_Record",
		"gamedataPathSecurityCoverSelectionParameters_Record",
		"gamedataPerkArea_Record",
		"gamedataPerkLevelData_Record",
		"gamedataPerkLevelUIData_Record",
		"gamedataPerkPrereq_Record",
		"gamedataPerkUtility_Record",
		"gamedataPerkWeaponGroup_Record",
		"gamedataPerk_Record",
		"gamedataPersistentLootTable_Record",
		"gamedataPhotoModeBackground_Record",
		"gamedataPhotoModeEffect_Record",
		"gamedataPhotoModeFace_Record",
		"gamedataPhotoModeFrame_Record",
		"gamedataPhotoModeItem_Record",
		"gamedataPhotoModePoseCategory_Record",
		"gamedataPhotoModePose_Record",
		"gamedataPhotoModeSticker_Record",
		"gamedataPierce_Record",
		"gamedataPing_Record",
		"gamedataPlayerBuild_Record",
		"gamedataPlayerIsNewPerkBoughtPrereq_Record",
		"gamedataPlayerPossesion_Record",
		"gamedataPlayerVehicleDisplayOverride_Record",
		"gamedataPoolValueModifier_Record",
		"gamedataPrereqCheck_Record",
		"gamedataPrereq_Record",
		"gamedataPresetMapper_Record",
		"gamedataPreventionAttackTypeData_Record",
		"gamedataPreventionFallbackUnitData_Record",
		"gamedataPreventionHeatDataMatrix_Record",
		"gamedataPreventionHeatData_Record",
		"gamedataPreventionHeatTable_Record",
		"gamedataPreventionMinimapData_Record",
		"gamedataPreventionUnitPoolData_Record",
		"gamedataPreventionVehiclePoolData_Record",
		"gamedataProficiency_Record",
		"gamedataProgram_Record",
		"gamedataProgressionBuild_Record",
		"gamedataProjectileCollision_Record",
		"gamedataProjectileLaunchMode_Record",
		"gamedataProjectileLaunch_Record",
		"gamedataProjectileOnCollisionAction_Record",
		"gamedataProp_Record",
		"gamedataPropagateStatusEffectInAreaEffector_Record",
		"gamedataPurchaseOffer_Record",
		"gamedataQuality_Record",
		"gamedataQuery_Record",
		"gamedataQuestRestrictionMode_Record",
		"gamedataQuestSystemSetup_Record",
		"gamedataRPGAction_Record",
		"gamedataRPGDataPackage_Record",
		"gamedataRaceCheckpoint_Record",
		"gamedataRacingMappin_Record",
		"gamedataRadioStation_Record",
		"gamedataRandomNewsFeedBatch_Record",
		"gamedataRandomPassengerEntry_Record",
		"gamedataRandomRatioCoverSelectionParameters_Record",
		"gamedataRandomStatModifier_Record",
		"gamedataRandomVariant_Record",
		"gamedataRangedAttackPackage_Record",
		"gamedataRangedAttack_Record",
		"gamedataReactionLimit_Record",
		"gamedataReactionPresetCivilian_Record",
		"gamedataReactionPresetCorpo_Record",
		"gamedataReactionPresetGanger_Record",
		"gamedataReactionPresetMechanical_Record",
		"gamedataReactionPresetNoReaction_Record",
		"gamedataReactionPresetPolice_Record",
		"gamedataReactionPreset_Record",
		"gamedataRearWheelsFrictionModifier_Record",
		"gamedataRecipeElement_Record",
		"gamedataRecipeItem_Record",
		"gamedataRegularGDM_Record",
		"gamedataRegular_Record",
		"gamedataRemoveAllModifiersEffector_Record",
		"gamedataRewardBase_Record",
		"gamedataRewardBase_inline0_Record",
		"gamedataRewardSet_Record",
		"gamedataRigs_Record",
		"gamedataRipperdocMappin_Record",
		"gamedataRoachRaceBackgroundObject_Record",
		"gamedataRoachRaceBackground_Record",
		"gamedataRoachRaceLevelList_Record",
		"gamedataRoachRaceLevel_Record",
		"gamedataRoachRaceMovement_Record",
		"gamedataRoachRaceObject_Record",
		"gamedataRoachRaceObstacleTexturePartPair_Record",
		"gamedataRoachRaceObstacle_Record",
		"gamedataRoachRacePowerUpList_Record",
		"gamedataRotationLimiter_Record",
		"gamedataRowSymbols_Record",
		"gamedataRowTraps_Record",
		"gamedataRule_Record",
		"gamedataScannableData_Record",
		"gamedataScannerModuleVisibilityPreset_Record",
		"gamedataSceneCameraDoF_Record",
		"gamedataSceneInterruptionScenarios_Record",
		"gamedataSceneResources_Record",
		"gamedataScreenMessageData_Record",
		"gamedataScreenMessagesList_Record",
		"gamedataSearchFilterMaskTypeCond_Record",
		"gamedataSearchFilterMaskTypeCondition_Record",
		"gamedataSearchFilterMaskTypeValue_Record",
		"gamedataSearchFilterMaskType_Record",
		"gamedataSeatState_Record",
		"gamedataSectorSelector_Record",
		"gamedataSenseObjectType_Record",
		"gamedataSensePreset_Record",
		"gamedataSenseShape_Record",
		"gamedataSetAttackHitTypeEffector_Record",
		"gamedataShooterAI_Record",
		"gamedataShooterBackground_Record",
		"gamedataShooterBasilisk_Record",
		"gamedataShooterBossAI_Record",
		"gamedataShooterBulletList_Record",
		"gamedataShooterBullet_Record",
		"gamedataShooterFlyingDrone_Record",
		"gamedataShooterGameplay_Record",
		"gamedataShooterLayerInfo_Record",
		"gamedataShooterLevelList_Record",
		"gamedataShooterLevel_Record",
		"gamedataShooterMeathead_Record",
		"gamedataShooterMelee_Record",
		"gamedataShooterNPCDrone_Record",
		"gamedataShooterNinja_Record",
		"gamedataShooterObject_Record",
		"gamedataShooterPickUpTransporter_Record",
		"gamedataShooterPlayerData_Record",
		"gamedataShooterPowerUpList_Record",
		"gamedataShooterPowerup_Record",
		"gamedataShooterProjectileAI_Record",
		"gamedataShooterProp_Record",
		"gamedataShooterRangeGrenade_Record",
		"gamedataShooterRange_Record",
		"gamedataShooterRescueTransporter_Record",
		"gamedataShooterSpiderDrone_Record",
		"gamedataShooterTransporter_Record",
		"gamedataShooterVFXList_Record",
		"gamedataShooterVFX_Record",
		"gamedataShooterVIP_Record",
		"gamedataShooterWeaponData_Record",
		"gamedataShooterWeaponList_Record",
		"gamedataSlotItemPartElement_Record",
		"gamedataSlotItemPartListElement_Record",
		"gamedataSlotItemPartPreset_Record",
		"gamedataSmartGunHandlerParams_Record",
		"gamedataSmartGunMissParams_Record",
		"gamedataSmartGunTargetSortConfigurations_Record",
		"gamedataSmartGunTargetSortData_Record",
		"gamedataSpawnableObjectPriority_Record",
		"gamedataSpawnableObject_Record",
		"gamedataSpreadAreaEffector_Record",
		"gamedataSpreadEffector_Record",
		"gamedataSpreadInitEffector_Record",
		"gamedataSquadBackyardBase_Record",
		"gamedataSquadBase_Record",
		"gamedataSquadFenceBase_Record",
		"gamedataSquadInstance_Record",
		"gamedataStatChangedPrereq_Record",
		"gamedataStatDistributionData_Record",
		"gamedataStatModifierGroup_Record",
		"gamedataStatModifier_Record",
		"gamedataStatPoolCost_Record",
		"gamedataStatPoolDistributionData_Record",
		"gamedataStatPoolPrereq_Record",
		"gamedataStatPoolUpdate_Record",
		"gamedataStatPool_Record",
		"gamedataStatPrereq_Record",
		"gamedataStat_Record",
		"gamedataStatsArray_Record",
		"gamedataStatsFolder_Record",
		"gamedataStatsList_Record",
		"gamedataStatusEffectAIBehaviorFlag_Record",
		"gamedataStatusEffectAIBehaviorType_Record",
		"gamedataStatusEffectAIData_Record",
		"gamedataStatusEffectAttackData_Record",
		"gamedataStatusEffectFX_Record",
		"gamedataStatusEffectPlayerData_Record",
		"gamedataStatusEffectPrereq_Record",
		"gamedataStatusEffectType_Record",
		"gamedataStatusEffectUIData_Record",
		"gamedataStatusEffectVariation_Record",
		"gamedataStatusEffect_Record",
		"gamedataStatusEffect_inline0_Record",
		"gamedataStatusEffect_inline1_Record",
		"gamedataStickyGDM_Record",
		"gamedataStimPriority_Record",
		"gamedataStimPropagation_Record",
		"gamedataStimTargets_Record",
		"gamedataStimType_Record",
		"gamedataStim_Record",
		"gamedataStopAndStickPerpendicular_Record",
		"gamedataStopAndStick_Record",
		"gamedataStop_Record",
		"gamedataStrategyData_Record",
		"gamedataStreetCredTier_Record",
		"gamedataStreetSign_Record",
		"gamedataSubCharacter_Record",
		"gamedataSubStatModifier_Record",
		"gamedataSubstat_Record",
		"gamedataTDBIDHelper",
		"gamedataTPPCameraSetup_Record",
		"gamedataTPPLookAtPresets_Record",
		"gamedataTVBase_Record",
		"gamedataTacticLimiterCoverSelectionParameters_Record",
		"gamedataTankArrangement_Record",
		"gamedataTankBackgroundData_Record",
		"gamedataTankDecorationSpawnerData_Record",
		"gamedataTankDestroyableObject_Record",
		"gamedataTankDriveModelData_Record",
		"gamedataTankEnemySpawnerData_Record",
		"gamedataTankEnemy_Record",
		"gamedataTankGameplayData_Record",
		"gamedataTankGameplay_Record",
		"gamedataTankLevelGameplay_Record",
		"gamedataTankLevelObjectID_Record",
		"gamedataTankLevelObject_Record",
		"gamedataTankLevelSpawnableArrangement_Record",
		"gamedataTankObstacleSpawnerData_Record",
		"gamedataTankPickupSpawnerData_Record",
		"gamedataTankPickup_Record",
		"gamedataTankPlayerData_Record",
		"gamedataTankPlayerWeaponLevel_Record",
		"gamedataTankProjectileSpawnerData_Record",
		"gamedataTankProjectile_Record",
		"gamedataTankScoreMultiplierBreakpoint_Record",
		"gamedataTankSpawnableArrangement_Record",
		"gamedataTankWeapon_Record",
		"gamedataTemporalPrereq_Record",
		"gamedataTerminalScreenType_Record",
		"gamedataThreatDistanceCoverSelectionParameters_Record",
		"gamedataThreatTrackingPresetBase_Record",
		"gamedataThumbnailWidgetDefinition_Record",
		"gamedataTime_Record",
		"gamedataTrackingMode_Record",
		"gamedataTracking_Record",
		"gamedataTraitData_Record",
		"gamedataTrait_Record",
		"gamedataTransgression_Record",
		"gamedataTrapType_Record",
		"gamedataTrap_Record",
		"gamedataTriggerAttackEffector_Record",
		"gamedataTriggerHackingMinigameEffector_Record",
		"gamedataTriggerMode_Record",
		"gamedataTweakDBInterface",
		"gamedataTweakDBRecord",
		"gamedataUIAnimation_Record",
		"gamedataUICharacterCreationAttribute_Record",
		"gamedataUICharacterCreationAttributesPreset_Record",
		"gamedataUICharacterCustomizationResourcePaths_Record",
		"gamedataUICondition_Record",
		"gamedataUIElement_Record",
		"gamedataUIIconCensorFlag_Record",
		"gamedataUIIconCensorship_Record",
		"gamedataUIIconPool_Record",
		"gamedataUIIcon_Record",
		"gamedataUINameplateDisplayType_Record",
		"gamedataUINameplate_Record",
		"gamedataUIStatsMap_Record",
		"gamedataUncontrolledMovementEffector_Record",
		"gamedataUpgradingData_Record",
		"gamedataUphillDriveHelper_Record",
		"gamedataUseConsumableEffector_Record",
		"gamedataUtilityLossCoverSelectionParameters_Record",
		"gamedataValueAssignment_Record",
		"gamedataValueDataNode",
		"gamedataVehicleAIBoostSettings_Record",
		"gamedataVehicleAIPanicDrivingSettings_Record",
		"gamedataVehicleAITractionEstimation_Record",
		"gamedataVehicleAIVisionSettings_Record",
		"gamedataVehicleAirControlAxis_Record",
		"gamedataVehicleAirControl_Record",
		"gamedataVehicleAppearancesToColorTemplate_Record",
		"gamedataVehicleBehaviorData_Record",
		"gamedataVehicleBurnOut_Record",
		"gamedataVehicleCameraManager_Record",
		"gamedataVehicleClearCoatOverrides_Record",
		"gamedataVehicleColorTemplate_Record",
		"gamedataVehicleCustomMultilayer_Record",
		"gamedataVehicleDataPackage_Record",
		"gamedataVehicleDecalAttachment_Record",
		"gamedataVehicleDefaultState_Record",
		"gamedataVehicleDeformablePart_Record",
		"gamedataVehicleDeformableZone_Record",
		"gamedataVehicleDestructibleGlass_Record",
		"gamedataVehicleDestructibleLight_Record",
		"gamedataVehicleDestructibleWheel_Record",
		"gamedataVehicleDestructionPointDamper_Record",
		"gamedataVehicleDestruction_Record",
		"gamedataVehicleDetachablePart_Record",
		"gamedataVehicleDiscountSettings_Record",
		"gamedataVehicleDoorDetachRule_Record",
		"gamedataVehicleDriveModelData_Record",
		"gamedataVehicleEngineData_Record",
		"gamedataVehicleFPPCameraParams_Record",
		"gamedataVehicleFlatTireSimParams_Record",
		"gamedataVehicleFlatTireSimulation_Record",
		"gamedataVehicleFxCollisionMaterial_Record",
		"gamedataVehicleFxCollision_Record",
		"gamedataVehicleFxWheelsDecalsMaterialSmear_Record",
		"gamedataVehicleFxWheelsDecalsMaterial_Record",
		"gamedataVehicleFxWheelsDecals_Record",
		"gamedataVehicleFxWheelsParticlesMaterial_Record",
		"gamedataVehicleFxWheelsParticles_Record",
		"gamedataVehicleGear_Record",
		"gamedataVehicleImpactTraffic_Record",
		"gamedataVehicleManufacturer_Record",
		"gamedataVehicleModel_Record",
		"gamedataVehicleOffer_Record",
		"gamedataVehiclePIDSettings_Record",
		"gamedataVehiclePartsClearCoatOverrides_Record",
		"gamedataVehicleProceduralFPPCameraParams_Record",
		"gamedataVehicleSeatSet_Record",
		"gamedataVehicleSeat_Record",
		"gamedataVehicleSteeringSettings_Record",
		"gamedataVehicleStoppingSettings_Record",
		"gamedataVehicleSurfaceBinding_Record",
		"gamedataVehicleSurfaceType_Record",
		"gamedataVehicleTPPCameraParams_Record",
		"gamedataVehicleTPPCameraPresetParams_Record",
		"gamedataVehicleTrafficSuspension_Record",
		"gamedataVehicleType_Record",
		"gamedataVehicleUIData_Record",
		"gamedataVehicleUnlockType_Record",
		"gamedataVehicleVisualCustomizationPreviewGlowSetup_Record",
		"gamedataVehicleVisualCustomizationPreviewSetup_Record",
		"gamedataVehicleVisualDestruction_Record",
		"gamedataVehicleWater_Record",
		"gamedataVehicleWeapon_Record",
		"gamedataVehicleWheelDimensionsPreset_Record",
		"gamedataVehicleWheelDimensionsSetup_Record",
		"gamedataVehicleWheelDrivingPreset_Record",
		"gamedataVehicleWheelDrivingSetup_2_Record",
		"gamedataVehicleWheelDrivingSetup_4_Record",
		"gamedataVehicleWheelDrivingSetup_Record",
		"gamedataVehicleWheelRole_Record",
		"gamedataVehicleWheelsFrictionMap_Record",
		"gamedataVehicleWheelsFrictionPreset_Record",
		"gamedataVehicle_Record",
		"gamedataVendorCraftable_Record",
		"gamedataVendorExperience_Record",
		"gamedataVendorItemQuery_Record",
		"gamedataVendorItem_Record",
		"gamedataVendorProgressionBasedStock_Record",
		"gamedataVendorType_Record",
		"gamedataVendorWare_Record",
		"gamedataVendor_Record",
		"gamedataVirtualNetworkPath_Record",
		"gamedataVirtualNetwork_Record",
		"gamedataVisionGroup_Record",
		"gamedataVisionModuleBase_Record",
		"gamedataVisualTagsPrereq_Record",
		"gamedataWeakspot_Record",
		"gamedataWeaponEvolution_Record",
		"gamedataWeaponFxPackage_Record",
		"gamedataWeaponItem_Record",
		"gamedataWeaponManufacturer_Record",
		"gamedataWeaponSafeModeBound_Record",
		"gamedataWeaponSafeModeBounds_Record",
		"gamedataWeaponVFXAction_Record",
		"gamedataWeaponVFXSet_Record",
		"gamedataWeaponsTooltipData_Record",
		"gamedataWeatherPreset_Record",
		"gamedataWeather_Record",
		"gamedataWebsite_Record",
		"gamedataWeightedCharacter_Record",
		"gamedataWidgetDefinition_Record",
		"gamedataWidgetRatio_Record",
		"gamedataWidgetStyle_Record",
		"gamedataWorkspotActionType_Record",
		"gamedataWorkspotCategory_Record",
		"gamedataWorkspotReactionType_Record",
		"gamedataWorkspotStatusEffect_Record",
		"gamedataWorldMapFilter_Record",
		"gamedataWorldMapFiltersList_Record",
		"gamedataWorldMapFreeCameraSettings_Record",
		"gamedataWorldMapSettings_Record",
		"gamedataWorldMapZoomLevel_Record",
		"gamedataXPPoints_Record",
		"gamedataXPPoints_inline0_Record",
		"gamedatanpc_scanning_data_Record",
		"gamedeviceAction",
		"gamedeviceActionProperty",
		"gameeventsAttitudeGroupChangedEvent",
		"gameeventsDefeatedEvent",
		"gameeventsDeviceEndPlayerCameraControlEvent",
		"gameeventsEndTakedownEvent",
		"gameeventsEvaluateLootQualityEvent",
		"gameeventsHitEvent",
		"gameeventsProjectedHitEvent",
		"gameeventsProperlySeenByPlayerEvent",
		"gameeventsRefreshVisibility",
		"gameeventsReloadLootEvent",
		"gameeventsResurrectEvent",
		"gameeventsStealthMappinCheckLootEvent",
		"gameeventsTargetHitEvent",
		"gameeventsUnconsciousEvent",
		"gameeventsUserLeftCoverEvent",
		"gamegpsGPSSystem",
		"gamegpsIGPSSystem",
		"gamegraphCNode",
		"gamehelperGameObjectEffectHelper",
		"gamehelperStimBroadcasterComponentHelper",
		"gamehitRepresentationEventsResetAllScaleMultipliers",
		"gameinfluenceBumpAgent",
		"gameinfluenceIAgent",
		"gameinfluenceISystem",
		"gameinfluenceSystem",
		"gameinputScriptListenerAction",
		"gameinputScriptListenerActionConsumer",
		"gameinteractionsCManager",
		"gameinteractionsChoice",
		"gameinteractionsChoiceCaption",
		"gameinteractionsChoiceCaptionPart",
		"gameinteractionsChoiceCaptionScriptPart",
		"gameinteractionsChoiceLookAtDescriptor",
		"gameinteractionsChoiceMetaData",
		"gameinteractionsChoiceTypeWrapper",
		"gameinteractionsEnableClientSideInteractionEvent",
		"gameinteractionsIFunctorDefinition",
		"gameinteractionsIManager",
		"gameinteractionsIPredicateType",
		"gameinteractionsIShapeDefinition",
		"gameinteractionsInteractionScriptedCondition",
		"gameinteractionsLootVisualiserControlWrapper",
		"gameinteractionsNodeDefinition",
		"gameinteractionsOnScreenTestPredicate",
		"gameinteractionsOrbActivationPredicate",
		"gameinteractionsOrbID",
		"gameinteractionsPublisherActivationEvent",
		"gameinteractionsPublisherBaseEvent",
		"gameinteractionsPublisherChoiceEvent",
		"gameinteractionsSuppressedPredicate",
		"gameinteractionsTargetFilterResult_Logical",
		"gameinteractionsTargetFilter_Logical",
		"gameinteractionsvisDeviceVisualizerFamily",
		"gameinteractionsvisDeviceVisualizerLogic",
		"gameinteractionsvisDialogVisualizerFamily",
		"gameinteractionsvisDialogVisualizerLogic",
		"gameinteractionsvisFamilyBase",
		"gameinteractionsvisIGroupedVisualizerLogic",
		"gameinteractionsvisIVisualizerDefinition",
		"gameinteractionsvisIVisualizerLogicInterface",
		"gameinteractionsvisIVisualizerTimeProvider",
		"gameinteractionsvisLootVisualizerDefinition",
		"gameinteractionsvisLootVisualizerFamily",
		"gameinteractionsvisLootVisualizerLogic",
		"gamemappinsCustomPositionMappin",
		"gamemappinsFastTravelMappin",
		"gamemappinsGrenadeMappin",
		"gamemappinsIArea",
		"gamemappinsIMappin",
		"gamemappinsIMappinData",
		"gamemappinsIMappinSystem",
		"gamemappinsIMappinUpdateData",
		"gamemappinsIMappinVolume",
		"gamemappinsIPointOfInterestVariant",
		"gamemappinsIRuntimeMappinData",
		"gamemappinsIVisualObject",
		"gamemappinsInteractionMappin",
		"gamemappinsInteractionMappinInitialData",
		"gamemappinsInteractionMappinUpdateData",
		"gamemappinsMappinData",
		"gamemappinsMappinScriptData",
		"gamemappinsMappinSystem",
		"gamemappinsOutlineArea",
		"gamemappinsPointOfInterestMappin",
		"gamemappinsQuestMappin",
		"gamemappinsRuntimeGenericMappinData",
		"gamemappinsRuntimeInteractionMappinData",
		"gamemappinsRuntimeMappin",
		"gamemappinsRuntimePointOfInterestMappinData",
		"gamemappinsRuntimeQuestMappinData",
		"gamemappinsRuntimeStubMappinData",
		"gamemappinsStealthMappin",
		"gamemappinsStealthMappinStatsListener",
		"gamemappinsStubMappin",
		"gamemappinsStubMappinData",
		"gamemappinsVehicleMappin",
		"gamemountingIMountingFacility",
		"gamemountingIMountingPublisher",
		"gamemountingMountableComponent",
		"gamemountingMountingFacility",
		"gamemountingMountingPublisher",
		"gameplayeractionsAttachSlotListener",
		"gameprojectileAcceleratedMovementEvent",
		"gameprojectileCollisionEvaluator",
		"gameprojectileForceActivationEvent",
		"gameprojectileLinearMovementEvent",
		"gameprojectileParabolicTrajectoryParams",
		"gameprojectileScriptCollisionEvaluator",
		"gameprojectileSetUpEvent",
		"gameprojectileShootEvent",
		"gameprojectileShootTargetEvent",
		"gameprojectileTrajectoryParams",
		"gameprojectileWeaponParams",
		"gametargetingSystemTargetFilter",
		"gametargetingSystemTargetFilterResult",
		"gametargetingSystemTargetFilter_Closest",
		"gameuiHUDGameController",
		"gameuiWidgetGameController",
		"gameweaponObject",
		"netTime",
		"populationModifier",
		"redResourceReferenceScriptToken",
		"senseStimuliData",
		"textTextParameterSet",
		"worldIDestructibleSpotsSystem",
		]
# TODO
LocalizationString = str


class DeviceOperationsTrigger(Chunk):
	pass


class gameAttackComputed(Chunk):
	pass


class gameBaseGameSession(Chunk):
	pass


class gameBaseTimer(Chunk):
	pass


class gameCooldownSystemEvent(Chunk):
	pass


class gamedataTDBIDHelper(Chunk):
	pass


class gamedataTweakDBInterface(Chunk):
	pass


class gamedataTweakDBRecord(Chunk):
	pass


class gameDeactivateTPPRepresentationEvent(Chunk):
	pass


class gameDeactivateTriggerDestructionComponentEvent(Chunk):
	pass


class gameDebugContextPtr(Chunk):
	pass


class gameDebugContextUserData(Chunk):
	pass


class gameDelayID(Chunk):
	pass


class gameDelaySystemDelayStruct(Chunk):
	pass


class gameDelaySystemScriptedDelayCallbackWrapper(Chunk):
	pass


class gameDelaySystemTickStruct(Chunk):
	pass


class gameDependentWorkspotData(Chunk):
	pass


class gameDeprecated_GameplayEvent(Chunk):
	pass


class gameDeviceDynamicConnectionChange(Chunk):
	pass


class gameDeviceLoaded(Chunk):
	pass


class gameDevicePSChanged(Chunk):
	pass


class gameDeviceReplicatedState(Chunk):
	pass


class gameDisableAimAssist(Chunk):
	pass


class gameDynamicEntityHandler(Chunk):
	pass


class gameEffectAction(Chunk):
	pass


class gameEffectData_MeleeTireHit(Chunk):
	pass


class gameEffectData_MeleeWaterFx(Chunk):
	pass


class gameEffectData_Pierce(Chunk):
	pass


class gameEffectData_PiercePreview(Chunk):
	pass


class gameEffectData_Splatter(Chunk):
	pass


class gameEffectData_SplatterList(Chunk):
	pass


class gameEffectData(Chunk):
	pass


class gameEffectDurationModifier(Chunk):
	pass


class gameEffectDurationModifierScriptContext(Chunk):
	pass


class gameEffectExecutionScriptContext(Chunk):
	pass


class gameEffectInfo(Chunk):
	pass


class gameEffectNode(Chunk):
	pass


class gameEffector(Chunk):
	pass


class gameEffectorObject(Chunk):
	pass


class gameEffectPreloadScriptContext(Chunk):
	pass


class gameEffectProviderScriptContext(Chunk):
	pass


class gameEffectScriptContext(Chunk):
	pass


class gameEffectSingleFilterScriptContext(Chunk):
	pass


class gameEnableAimAssist(Chunk):
	pass


class gameEngineTurnedOffEvent(Chunk):
	pass


class gameEngineTurnedOnEvent(Chunk):
	pass


class gameEntityIDPool(Chunk):
	pass


class gameEnumNameToIndexCache(Chunk):
	pass


class gameEthnicityPicker(Chunk):
	pass


class gameeventsAttitudeGroupChangedEvent(Chunk):
	pass


class gameeventsDefeatedEvent(Chunk):
	pass


class gameeventsDeviceEndPlayerCameraControlEvent(Chunk):
	pass


class gameeventsEndTakedownEvent(Chunk):
	pass


class gameeventsEvaluateLootQualityEvent(Chunk):
	pass


class gameeventsProperlySeenByPlayerEvent(Chunk):
	pass


class gameeventsRefreshVisibility(Chunk):
	pass


class gameeventsReloadLootEvent(Chunk):
	pass


class gameeventsResurrectEvent(Chunk):
	pass


class gameeventsStealthMappinCheckLootEvent(Chunk):
	pass


class gameeventsUnconsciousEvent(Chunk):
	pass


class gameeventsUserLeftCoverEvent(Chunk):
	pass


class gameExternalMovementCameraDataEvent(Chunk):
	pass


class gameFinalizeActivationTPPRepresentationEvent(Chunk):
	pass


class gameFinalizeDeactivationTPPRepresentationEvent(Chunk):
	pass


class gameFootstepEvent(Chunk):
	pass


class gameForceResetAmmoEvent(Chunk):
	pass


class gameFxInstance(Chunk):
	pass


class gameGameFeatureManager(Chunk):
	pass


class gameGameSessionDesc(Chunk):
	pass


class gameGeometryDescriptionSystem(Chunk):
	pass


class gamegraphCNode(Chunk):
	pass


class gameGrenadeThrowQuery(Chunk):
	pass


class gameHalloweenEvent(Chunk):
	pass


class gamehelperGameObjectEffectHelper(Chunk):
	pass


class gamehelperStimBroadcasterComponentHelper(Chunk):
	pass


class gamehitRepresentationEventsResetAllScaleMultipliers(Chunk):
	pass


class gameHitShapeUserData(Chunk):
	pass


class gameIAttachmentSlotsListener(Chunk):
	pass


class gameIAttack(Chunk):
	pass


class gameIBlackboard(Chunk):
	pass


class gameIDamageSystemListener(Chunk):
	pass


class gameIEffect(Chunk):
	pass


class gameIEffectInputParameter(Chunk):
	pass


class gameIEffectOutputParameter(Chunk):
	pass


class gameIEffectParameter_BoolEvaluator(Chunk):
	pass


class gameIEffectParameter_CNameEvaluator(Chunk):
	pass


class gameIEffectParameter_FloatEvaluator(Chunk):
	pass


class gameIEffectParameter_IntEvaluator(Chunk):
	pass


class gameIEffectParameter_QuatEvaluator(Chunk):
	pass


class gameIEffectParameter_StringEvaluator(Chunk):
	pass


class gameIEffectParameter_VectorEvaluator(Chunk):
	pass


class gameIFinisherScenario(Chunk):
	pass


class gameIGameSystem(Chunk):
	pass


class gameIGameSystemReplicatedState(Chunk):
	pass


class gameIHitShape(Chunk):
	pass


class gameIInventoryListener(Chunk):
	pass


class gameImpostorComponentAttachEvent(Chunk):
	pass


class gameIMuppetInputAction(Chunk):
	pass


class gameInCrowd(Chunk):
	pass


class gameinfluenceBumpAgent(Chunk):
	pass


class gameinfluenceIAgent(Chunk):
	pass


class gameInnerItemData(Chunk):
	pass


class gameinputScriptListenerAction(Chunk):
	pass


class gameinputScriptListenerActionConsumer(Chunk):
	pass


class gameInputTriggerState(Chunk):
	pass


class gameinteractionsChoiceCaptionPart(Chunk):
	pass


class gameinteractionsEnableClientSideInteractionEvent(Chunk):
	pass


class gameinteractionsIFunctorDefinition(Chunk):
	pass


class gameinteractionsInteractionScriptedCondition(Chunk):
	pass


class gameinteractionsIPredicateType(Chunk):
	pass


class gameinteractionsIShapeDefinition(Chunk):
	pass


class gameinteractionsLootVisualiserControlWrapper(Chunk):
	pass


class gameinteractionsNodeDefinition(Chunk):
	pass


class gameinteractionsPublisherBaseEvent(Chunk):
	pass


class gameinteractionsvisFamilyBase(Chunk):
	pass


class gameinteractionsvisIVisualizerLogicInterface(Chunk):
	pass


class gameinteractionsvisIVisualizerTimeProvider(Chunk):
	pass


class gameInventoryChangedEvent(Chunk):
	pass


class gameInventoryListenerData_Base(Chunk):
	pass


class gameIPrereq(Chunk):
	pass


class gameIScriptableSystem(Chunk):
	pass


class gameIsQuickhackPanelOpenedPrereqState(Chunk):
	pass


class gameIStatPoolsListener(Chunk):
	pass


class gameIStatsListener(Chunk):
	pass


class gameIStatusEffectListener(Chunk):
	pass


class gameItemCreationPrereqDataWrapper(Chunk):
	pass


class gameItemData(Chunk):
	pass


class gameItemDecorationEvent(Chunk):
	pass


class gameItemDropStorageInventoryListener(Chunk):
	pass


class gameItemDropStorageManager(Chunk):
	pass


class gameItemEventsEquippedToObject(Chunk):
	pass


class gameItemEventsPropagateRenderingPlane(Chunk):
	pass


class gameItemEventsRemoveActiveItem(Chunk):
	pass


class gameItemEventsUnequippedFromObject(Chunk):
	pass


class gameItemEventsUnequipStarted(Chunk):
	pass


class gameItemFactorySystemPool(Chunk):
	pass


class gameItemsMeshesLoaded(Chunk):
	pass


class gameITimeState(Chunk):
	pass


class gameJoinTrafficSettings(Chunk):
	pass


class gameJournalOnscreensStructuredGroup(Chunk):
	pass


class gameLazyDevice(Chunk):
	pass


class GameLoadedFactReset(Chunk):
	pass


class gameLookAtFacingPositionProvider(Chunk):
	pass


class gameLoSFinderParams(Chunk):
	pass


class gameMakeInventoryShareableEvent(Chunk):
	pass


class gamemappinsIMappinData(Chunk):
	pass


class gamemappinsIMappinUpdateData(Chunk):
	pass


class gamemappinsIMappinVolume(Chunk):
	pass


class gamemappinsIPointOfInterestVariant(Chunk):
	pass


class gamemappinsIRuntimeMappinData(Chunk):
	pass


class gamemappinsIVisualObject(Chunk):
	pass


class gameMappinUtils(Chunk):
	pass


class gameMovingPlatformBeforeArrivedAt(Chunk):
	pass


class gameMuppetStates(Chunk):
	pass


class gameNarrationPlateBlackboardUpdater(Chunk):
	pass


class gameNetrunnerPrototypeDespawnEvent(Chunk):
	pass


class gameObjectActionRefreshEvent(Chunk):
	pass


class gameObjectActionsCallbackController(Chunk):
	pass


class gameObjectCarrierComponentAttached(Chunk):
	pass


class gameObjectCarrierComponentDetached(Chunk):
	pass


class gameObjectSpawnParameter(Chunk):
	pass


class gameOffPavement(Chunk):
	pass


class gameOnExecutionContext(Chunk):
	pass


class gameOnInventoryEmptyEvent(Chunk):
	pass


class gameOnLootAllEvent(Chunk):
	pass


class gameOnLootEvent(Chunk):
	pass


class gameOnPavement(Chunk):
	pass


class gameOnScannableBraindanceClueDisabledEvent(Chunk):
	pass


class gameOnScannableBraindanceClueEnabledEvent(Chunk):
	pass


class gameOutOfCrowd(Chunk):
	pass


class gamePatrolSplineControlPoint(Chunk):
	pass


class gamePersistentState(Chunk):
	pass


class gamePhotoModeAutoFocusPositionProvider(Chunk):
	pass


class gamePhotoModeEnableEvent(Chunk):
	pass


class gamePhotoModeObjectPositionProvider(Chunk):
	pass


class gamePhotoModeUtils(Chunk):
	pass


class gamePlayerCoverInfo(Chunk):
	pass


class gamePlayerObstacleSystem(Chunk):
	pass


class gamePlayerReleaseControlAsChild(Chunk):
	pass


class gamePlayerSocket(Chunk):
	pass


class gamePlayerTakeControlAsChild(Chunk):
	pass


class gamePlayerTakeControlAsParent(Chunk):
	pass


class gamePrepareTPPRepresentationEvent(Chunk):
	pass


class gamePrereqState(Chunk):
	pass


class gamePrereqStateChangedEvent(Chunk):
	pass


class gameprojectileCollisionEvaluator(Chunk):
	pass


class gameprojectileForceActivationEvent(Chunk):
	pass


class gameprojectileTrajectoryParams(Chunk):
	pass


class gamePSChangedEvent(Chunk):
	pass


class gamePuppetBlackboardUpdater(Chunk):
	pass


class gameQuestOrSceneSetVehiclePhysicsActive(Chunk):
	pass


class gameRegenerateLootEvent(Chunk):
	pass


class gameRequestStats(Chunk):
	pass


class gameResetContainerEvent(Chunk):
	pass


class gameRPGManager(Chunk):
	pass


class gameScanningActionFinishedEvent(Chunk):
	pass


class gameScanningController(Chunk):
	pass


class gameScanningInternalEvent(Chunk):
	pass


class gameScanningPulseEvent(Chunk):
	pass


class gameScenePlayerAnimationParams(Chunk):
	pass


class gameScriptableSystemRequest(Chunk):
	pass


class gameScriptedPrereqAttitudeListenerWrapper(Chunk):
	pass


class gameScriptedPrereqMountingListenerWrapper(Chunk):
	pass


class gameStatModifierBase(Chunk):
	pass


class gametargetingSystemTargetFilter(Chunk):
	pass


class ObjectScanningDescription(Chunk):
	pass


class populationModifier(Chunk):
	pass


class senseStimuliData(Chunk):
	pass


class StartOverheatEffectEvent(Chunk):
	pass


class textTextParameterSet(Chunk):
	pass


class UpdateDamageChangeEvent(Chunk):
	pass


class WidgetCustomData(Chunk):
	pass


@dataclass
class netTime(Chunk):
	milli_secs: int = 0


@dataclass
class gameReplAnimTransformRequestBase(Chunk):
	apply_server_time: netTime = field(default_factory=lambda: netTime(sys.maxsize))


@dataclass
class gameEntityReference(Chunk):
	type: enums.gameEntityReferenceType = enums.gameEntityReferenceType.EntityRef
	reference: str = ''
	names: list[str] = field(default_factory=list)
	slot_name: str = ''
	scene_actor_context_name: str = ''
	dynamic_entity_unique_name: str = ''


@dataclass
class gameTier3CameraSettings(Chunk):
	yaw_left_limit: float = 60.0
	yaw_right_limit: float = 60.0
	pitch_top_limit: float = 60.0
	pitch_bottom_limit: float = 45.0
	pitch_speed_multiplier: float = 1.0
	yaw_speed_multiplier: float = 1.0


@dataclass
class SToggleDeviceOperationData(Chunk):
	operation_name: str = ''
	enable: bool = False


@dataclass
class DeviceOperationBase(Chunk):
	operation_name: str = ''
	execute_once: bool = False
	is_enabled: bool = False
	toggle_operations: list[SToggleDeviceOperationData] = field(default_factory=list)
	disable_device: bool = False


@dataclass
class DeviceOperationsContainer(Chunk):
	operations: list[DeviceOperationBase] = field(default_factory=list)
	triggers: list[DeviceOperationsTrigger] = field(default_factory=list)


@dataclass
class gamedeviceActionProperty(Chunk):
	name: str = ''
	type_name: str = ''
	first: Any = None  # TODO: CVariant = field(default_factory=CVariant)
	second: Any = None  # TODO: CVariant = field(default_factory=CVariant)
	third: Any = None  # TODO: CVariant = field(default_factory=CVariant)
	flags: enums.gamedeviceActionPropertyFlags = enums.gamedeviceActionPropertyFlags._None


@dataclass
class gamedeviceAction(Chunk):
	action_name: str = ''
	clearance_level: int = 0
	localized_object_name: str = ''
	payment_quantity: int = 0


@dataclass
class gameinteractionsChoiceCaption(Chunk):
	parts: list[gameinteractionsChoiceCaptionPart] = field(default_factory=list)


@dataclass
class gameinteractionsChoiceTypeWrapper(Chunk):
	properties: int = 0


@dataclass
class gameinteractionsChoiceMetaData(Chunk):
	tweak_dbname: str = ''
	tweak_dbid: int = 0
	type: gameinteractionsChoiceTypeWrapper = field(default_factory=gameinteractionsChoiceTypeWrapper)


@dataclass
class gameinteractionsOrbID(Chunk):
	id: int = 0


@dataclass
class gameinteractionsChoiceLookAtDescriptor(Chunk):
	type: enums.gameinteractionsChoiceLookAtType = enums.gameinteractionsChoiceLookAtType.Root
	slot_name: str = ''
	offset: tuple[float, float, float] = (0.0, 0.0, 0.0)
	orb_id: gameinteractionsOrbID = field(default_factory=gameinteractionsOrbID)


@dataclass
class gameinteractionsChoice(Chunk):
	caption: str = ''
	caption_parts: gameinteractionsChoiceCaption = field(default_factory=gameinteractionsChoiceCaption)
	data: list[Any] = field(default_factory=list)  # TODO: CVariant
	choice_meta_data: gameinteractionsChoiceMetaData = field(default_factory=gameinteractionsChoiceMetaData)
	look_at_descriptor: gameinteractionsChoiceLookAtDescriptor = field(
			default_factory=gameinteractionsChoiceLookAtDescriptor
			)
	do_not_turn_off_prevention_system: bool = False


@dataclass
class DeviceActionQueue(Chunk):
	actions_in_queue: list[gamedeviceAction] = field(default_factory=list)
	max_queue_size: int = 1
	locked: bool = False


class gamedataBaseObject_Record(gamedataTweakDBRecord):
	pass


class gamedataItem_Record(gamedataBaseObject_Record):
	pass


class gamedataWeaponItem_Record(gamedataItem_Record):
	pass


class gamedataSpawnableObject_Record(gamedataBaseObject_Record):
	pass


class gamedataCharacter_Record(gamedataSpawnableObject_Record):
	pass


class gamedataSlotItemPartElement_Record(gamedataTweakDBRecord):
	pass


class gamedataSlotItemPartListElement_Record(gamedataTweakDBRecord):
	pass


class gamedataSlotItemPartPreset_Record(gamedataTweakDBRecord):
	pass


class gamedataSmartGunHandlerParams_Record(gamedataTweakDBRecord):
	pass


class gamedataSmartGunMissParams_Record(gamedataTweakDBRecord):
	pass


class gamedataSmartGunTargetSortConfigurations_Record(gamedataTweakDBRecord):
	pass


class gamedataSmartGunTargetSortData_Record(gamedataTweakDBRecord):
	pass


class gamedataSpawnableObjectPriority_Record(gamedataTweakDBRecord):
	pass


class gamedataEffector_Record(gamedataTweakDBRecord):
	pass


class gamedataEffectorTimeDilationDriver_Record(gamedataTweakDBRecord):
	pass


class gamedataEnvLight_Record(gamedataTweakDBRecord):
	pass


class gamedataEquipmentArea_Record(gamedataTweakDBRecord):
	pass


class gamedataEquipmentMovementSound_Record(gamedataTweakDBRecord):
	pass


class gamedataEquipSlot_Record(gamedataTweakDBRecord):
	pass


class gamedataEthnicity_Record(gamedataTweakDBRecord):
	pass


class gamedataEthnicNames_Record(gamedataTweakDBRecord):
	pass


class gamedataFacialPreset_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelBinkData_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelBinksGroup_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelPoint_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelScreenData_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelScreenDataGroup_Record(gamedataTweakDBRecord):
	pass


class gamedataFastTravelSystem_Record(gamedataTweakDBRecord):
	pass


class gamedataFootstep_Record(gamedataTweakDBRecord):
	pass


class gamedataForceDismembermentEffector_Record(gamedataEffector_Record):
	pass


class gamedataCoverSelectionParameters_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gameScanningTooltipElementDef(Chunk):
	record_id: int = 0
	time_pct: float = 0.0


@dataclass
class gameComponent(entIComponent):
	# TODO: name = "Component"
	persistent_state: gamePersistentState = field(default_factory=gamePersistentState)


@dataclass
class ModuleInstance(Chunk):
	is_looked_at: bool = False
	is_revealed: bool = False
	was_processed: bool = False
	entity_id: entEntityID = field(default_factory=entEntityID)
	state: enums.InstanceState = enums.InstanceState.DISABLED
	previous_instance: "ModuleInstance" = field(default_factory=lambda: ModuleInstance())


@dataclass
class HighlightInstance(ModuleInstance):
	context: enums.HighlightContext = enums.HighlightContext.DEFAULT
	instant: bool = False


@dataclass
class FocusForcedHighlightData(Chunk):
	source_id: entEntityID = field(default_factory=entEntityID)
	source_name: str = ''
	highlight_type: enums.EFocusForcedHighlightType = enums.EFocusForcedHighlightType.INTERACTION
	outline_type: enums.EFocusOutlineType = enums.EFocusOutlineType.INVALID
	priority: enums.EPriority = enums.EPriority.VeryLow
	in_transition_time: float = 0.5
	out_transition_time: float = 2.0
	hud_data: HighlightInstance = field(default_factory=HighlightInstance)
	is_revealed: bool = False
	is_savable: bool = False
	pattern_type: enums.gameVisionModePatternType = enums.gameVisionModePatternType.Default


@dataclass
class SFactOperationData(Chunk):
	fact_name: str = ''
	fact_value: int = 0
	operation_type: enums.EMathOperationType = enums.EMathOperationType.Add


@dataclass
class ClueRecordData(Chunk):
	clue_record: int = 0
	percentage: float = 0.0
	facts: list[SFactOperationData] = field(default_factory=list)
	was_inspected: bool = False


@dataclass
class FocusClueDefinition(Chunk):
	extended_clue_records: list[ClueRecordData] = field(default_factory=list)
	clue_record: int = 0
	fact_to_activate: str = ''
	facts: list[SFactOperationData] = field(default_factory=list)
	use_auto_inspect: bool = False
	is_enabled: bool = False
	is_progressing: bool = True
	clue_group_id: str = ''
	was_inspected: bool = False
	qdb_callback_id: int = 0
	conclusion_quest_state: enums.EConclusionQuestState = enums.EConclusionQuestState.Undefined


@dataclass
class gameScanningComponent(gameComponent):
	# TODO: name = "scanning";
	# TODO: bounding_sphere = new Sphere { CenterRadius2 = new Vector4 { W = -1.000000F } };
	scannable_data: list[gameScanningTooltipElementDef] = field(default_factory=list)
	time_needed: float = 0.0
	auto_generate_bounding_sphere: bool = True
	bounding_sphere: Sphere = field(default_factory=Sphere)
	ignores_scanning_distance_limit: bool = False
	cpo_enable_multiple_players_scanning_modifier: bool = True
	is_braindance_clue: bool = False
	braindance_layer: enums.braindanceVisionMode = enums.braindanceVisionMode.Default
	is_braindance_blocked: bool = False
	is_braindance_layer_unlocked: bool = False
	is_braindance_timeline_unlocked: bool = False
	is_braindance_active: bool = False
	current_braindance_layer: int = 0
	clues: list[FocusClueDefinition] = field(default_factory=list)
	object_description: ObjectScanningDescription = field(default_factory=ObjectScanningDescription)
	scanning_bar_text: int = 0
	is_focus_mode_active: bool = False
	current_highlight: FocusForcedHighlightData = field(default_factory=FocusForcedHighlightData)
	is_hud_manager_initialized: bool = False
	is_being_scanned: bool = False
	is_scanning_clues_blocked: bool = False
	is_entity_visible: bool = True
	on_braindance_vision_mode_change_callback: Chunk = field(default_factory=Chunk)
	on_braindance_fpp_change_callback: Chunk = field(default_factory=Chunk)


@dataclass
class GameObjectListener(Chunk):
	prereq_owner: gamePrereqState = field(default_factory=gamePrereqState)
	e3hack_block: bool = False


@dataclass
class gamedataFriendlyTargetAngleDistanceCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataFriendlyTargetDistanceCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


class gamedataFxAction_Record(gamedataTweakDBRecord):
	pass


class gamedataFxActionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataGadget_Record(gamedataWeaponItem_Record):
	pass


class gamedataGameplayAbility_Record(gamedataTweakDBRecord):
	pass


class gamedataGameplayAbilityGroup_Record(gamedataTweakDBRecord):
	pass


class gamedataGameplayLogicPackage_Record(gamedataTweakDBRecord):
	pass


class gamedataGameplayLogicPackageUIData_Record(gamedataTweakDBRecord):
	pass


class gamedataIPrereq_Record(gamedataTweakDBRecord):
	pass


class gamedataGameplayTagsPrereq_Record(gamedataIPrereq_Record):
	pass


class gamedataGender_Record(gamedataTweakDBRecord):
	pass


class gamedataGenderEntity_Record(gamedataTweakDBRecord):
	pass


class gamedataBaseSign_Record(gamedataTweakDBRecord):
	pass


class gamedataStreetSign_Record(gamedataBaseSign_Record):
	pass


class gamedataGenericHighwaySign_Record(gamedataBaseSign_Record):
	pass


class gamedataGenericMetroSign_Record(gamedataBaseSign_Record):
	pass


class gamedataGenericStreetNameSign_Record(gamedataBaseSign_Record):
	pass


class gamedataGOGReward_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataGrenade_Record(gamedataGadget_Record):
	pass


class gamedataGrenadeDeliveryMethod_Record(gamedataTweakDBRecord):
	pass


class gamedataGrenadeDeliveryMethodType_Record(gamedataTweakDBRecord):
	pass


class gamedataHackCategory_Record(gamedataTweakDBRecord):
	pass


class gamedataHackingMiniGame_Record(gamedataTweakDBRecord):
	pass


class gamedataDriveHelper_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataDevice_Record(gamedataBaseObject_Record):
	pass


class gamedataDeviceScreenType_Record(gamedataTweakDBRecord):
	pass


class gamedataArcadeObject_Record(gamedataTweakDBRecord):
	pass


class gamedataArcadeCollidableObject_Record(gamedataArcadeObject_Record):
	pass


class gamedataStatModifier_Record(gamedataTweakDBRecord):
	pass


class gamedataConstantStatModifier_Record(gamedataStatModifier_Record):
	pass


@dataclass
class gamedataHandbrakeFrictionModifier_Record(gamedataDriveHelper_Record):
	pass


@dataclass
class gamedataHandicapLootList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHandicapLootPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHitPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataHitPrereqCondition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHitPrereqConditionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHomingGDM_Record(gamedataGrenadeDeliveryMethod_Record):
	pass


@dataclass
class gamedataHomingParameters_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHUD_Preset_Entry_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataHudEnhancer_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataIconsGeneratorContext_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataImprovementRelation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataInAirGravityModifier_Record(gamedataDriveHelper_Record):
	pass


@dataclass
class gamedataInitLoadingScreen_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataInteractionBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataInteractionMountBase_Record(gamedataInteractionBase_Record):
	pass


@dataclass
class gamedataInventoryItem_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataInventoryItemGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataInventoryItemSet_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataIsHackable_Record(gamedataTweakDBRecord):
	pass


class gamedataObjectAction_Record(gamedataTweakDBRecord):
	pass


class gamedataItemAction_Record(gamedataObjectAction_Record):
	pass


@dataclass
class gamedataQuery_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemQuery_Record(gamedataQuery_Record):
	pass


@dataclass
class gamedataItemArrayQuery_Record(gamedataItemQuery_Record):
	pass


@dataclass
class gamedataItemBlueprint_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemBlueprintElement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemCategory_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataObjectActionCost_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemCost_Record(gamedataObjectActionCost_Record):
	pass


@dataclass
class gamedataStatPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataItemCreationPrereq_Record(gamedataStatPrereq_Record):
	pass


@dataclass
class gamedataItemDropSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemPartConnection_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemPartListElement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemRecipe_Record(gamedataItem_Record):
	pass


@dataclass
class gamedataItemRequiredSlot_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemsFactoryAppearanceSuffixBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemsFactoryAppearanceSuffixOrder_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemStructure_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIIcon_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataJournalIcon_Record(gamedataUIIcon_Record):
	pass


@dataclass
class gamedataKeepCurrentCoverCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataKnifeThrowDelivery_Record(gamedataGrenadeDeliveryMethod_Record):
	pass


@dataclass
class gamedataLandingFxMaterial_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLandingFxPackage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLayout_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLCDScreen_Record(gamedataBaseSign_Record):
	pass


@dataclass
class gamedataLifePath_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLightPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataAccuracy_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLinearAccuracy_Record(gamedataAccuracy_Record):
	pass


class gamedataLoadingTipsGroup_Record(gamedataTweakDBRecord):
	pass


class gamedataBase_MappinDefinition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLocomotionMode_Record(gamedataTweakDBRecord):
	pass


class gamedataLookAtPart_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLookAtPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLootInjectionSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataLootTableElement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataItemQueryElement_Record(gamedataLootTableElement_Record):
	pass


@dataclass
class gamedataLootItem_Record(gamedataLootTableElement_Record):
	pass


@dataclass
class gamedataLootTable_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinClampingSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinDefinition_Record(gamedataBase_MappinDefinition_Record):
	pass


@dataclass
class gamedataMappinPhase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinPhaseDefinition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinsGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUICustomOpacityParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUIFilterGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUIGlobalProfile_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUIParamGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUIPreventionSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUIRuntimeProfile_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinUISettings_Record(gamedataMappinUIRuntimeProfile_Record):
	pass


@dataclass
class gamedataMappinUISpawnProfile_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMappinVariant_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMaterial_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMaterialFx_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMeleeAttackDirection_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMetaQuest_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMiniGame_SymbolsWithRarity_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_inline0_Record(gamedataMiniGame_SymbolsWithRarity_Record):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_inline1_Record(gamedataMiniGame_SymbolsWithRarity_Record):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_inline2_Record(gamedataMiniGame_SymbolsWithRarity_Record):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_inline3_Record(gamedataMiniGame_SymbolsWithRarity_Record):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_inline4_Record(gamedataMiniGame_SymbolsWithRarity_Record):
	pass


@dataclass
class gamedataMiniGame_AllSymbols_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMinigame_Def_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMiniGame_Trap_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMinigameAction_Record(gamedataObjectAction_Record):
	pass


@dataclass
class gamedataMinigameActionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMinigameCategory_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMinigameTrapType_Record(gamedataTweakDBRecord):
	pass


class gamedataModifyAttackCritChanceEffector_Record(gamedataEffector_Record):
	pass


class gamedataModifyStaminaHandlerEffector_Record(gamedataEffector_Record):
	pass


class gamedataModifyStatPoolCustomLimitEffector_Record(gamedataEffector_Record):
	pass


class gamedataModifyStatPoolModifierEffector_Record(gamedataEffector_Record):
	pass


class gamedataModifyStatPoolValueEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataMovementParam_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMovementParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMovementPolicy_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMovementPolicyTagList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMultiPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataPoolValueModifier_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataMutablePoolValueModifier_Record(gamedataPoolValueModifier_Record):
	pass


@dataclass
class gamedataNetworkPingingParameteres_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNetworkPresetBinderParameters_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerk_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerkCategory_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerkLevelData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerkLevelUIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerkSlot_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewPerkTier_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewsFeedTitle_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProficiency_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNewSkillsProficiency_Record(gamedataProficiency_Record):
	pass


@dataclass
class gamedataNonLinearAccuracy_Record(gamedataAccuracy_Record):
	pass


@dataclass
class gamedataNPCBehaviorState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCEquipmentGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCEquipmentGroupEntry_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCEquipmentItem_Record(gamedataNPCEquipmentGroupEntry_Record):
	pass


@dataclass
class gamedataNPCEquipmentItemPool_Record(gamedataNPCEquipmentGroupEntry_Record):
	pass


@dataclass
class gamedataNPCEquipmentItemsPoolEntry_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCHighLevelState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCQuestAffiliation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCRarity_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCStanceState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNPCTypePrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataNPCUpperBodyState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataNumberPlate_Record(gamedataLCDScreen_Record):
	pass


@dataclass
class gamedataObjectActionEffect_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataObjectActionPrereq_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataObjectActionReference_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataObjectActionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataOffMeshLinkTag_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataOutput_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataOverrideRangedAttackPackageEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataOwnerAngleCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataOwnerDistanceCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataOwnerThreatCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataParentAttachmentType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataParticleDamage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPassiveProficiencyBonus_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPassiveProficiencyBonusUIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPathLengthCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataPathSecurityCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataPerk_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPerkArea_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPerkLevelData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPerkLevelUIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPerkPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataPerkUtility_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPerkWeaponGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPersistentLootTable_Record(gamedataLootTable_Record):
	pass


@dataclass
class gamedataPhotoModeItem_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPhotoModeBackground_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataPhotoModeEffect_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataPhotoModeFace_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataPhotoModeFrame_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataPhotoModePose_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataPhotoModePoseCategory_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPhotoModeSticker_Record(gamedataPhotoModeItem_Record):
	pass


@dataclass
class gamedataProjectileCollision_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPierce_Record(gamedataProjectileCollision_Record):
	pass


@dataclass
class gamedataPing_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPlayerBuild_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPlayerIsNewPerkBoughtPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataPlayerPossesion_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPlayerVehicleDisplayOverride_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPrereq_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPrereqCheck_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPresetMapper_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionAttackTypeData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionFallbackUnitData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionHeatData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionHeatDataMatrix_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionHeatTable_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionMinimapData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionUnitPoolData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataPreventionVehiclePoolData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProgram_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProgressionBuild_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProjectileLaunch_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProjectileLaunchMode_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProjectileOnCollisionAction_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataProp_Record(gamedataSpawnableObject_Record):
	pass


@dataclass
class gamedataPropagateStatusEffectInAreaEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataPurchaseOffer_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataQuality_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataQuestRestrictionMode_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataQuestSystemSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRaceCheckpoint_Record(gamedataLCDScreen_Record):
	pass


@dataclass
class gamedataRacingMappin_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRadioStation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRandomNewsFeedBatch_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRandomPassengerEntry_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRandomRatioCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataRandomStatModifier_Record(gamedataStatModifier_Record):
	pass


@dataclass
class gamedataRandomVariant_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRangedAttack_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRangedAttackPackage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataReactionLimit_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataReactionPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataReactionPresetCivilian_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataReactionPresetCorpo_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataReactionPresetGanger_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataReactionPresetMechanical_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataReactionPresetNoReaction_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataReactionPresetPolice_Record(gamedataReactionPreset_Record):
	pass


@dataclass
class gamedataRearWheelsFrictionModifier_Record(gamedataDriveHelper_Record):
	pass


@dataclass
class gamedataRecipeElement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRecipeItem_Record(gamedataItem_Record):
	pass


@dataclass
class gamedataRegular_Record(gamedataProjectileLaunch_Record):
	pass


@dataclass
class gamedataRegularGDM_Record(gamedataGrenadeDeliveryMethod_Record):
	pass


@dataclass
class gamedataRemoveAllModifiersEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataRewardBase_inline0_Record(gamedataConstantStatModifier_Record):
	pass


@dataclass
class gamedataRewardBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRewardSet_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRigs_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRipperdocMappin_Record(gamedataUIIcon_Record):
	pass


@dataclass
class gamedataRoachRaceBackground_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRoachRaceBackgroundObject_Record(gamedataArcadeObject_Record):
	pass


@dataclass
class gamedataRoachRaceLevel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRoachRaceLevelList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRoachRaceMovement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRoachRaceObject_Record(gamedataArcadeObject_Record):
	pass


@dataclass
class gamedataRoachRaceObstacle_Record(gamedataRoachRaceObject_Record):
	pass


@dataclass
class gamedataRoachRaceObstacleTexturePartPair_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRoachRacePowerUpList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRotationLimiter_Record(gamedataDriveHelper_Record):
	pass


@dataclass
class gamedataRowSymbols_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRowTraps_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRPGAction_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRPGDataPackage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataRule_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataScannableData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataFocusClue_Record(gamedataScannableData_Record):
	pass


@dataclass
class gamedatanpc_scanning_data_Record(gamedataScannableData_Record):
	pass


@dataclass
class gamedataObjectActionGameplayCategory_Record(gamedataScannableData_Record):
	pass


@dataclass
class gamedataScannerModuleVisibilityPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSceneCameraDoF_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSceneInterruptionScenarios_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSceneResources_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataScreenMessageData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataScreenMessagesList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSearchFilterMaskType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSearchFilterMaskTypeCondition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSearchFilterMaskTypeCond_Record(gamedataSearchFilterMaskTypeCondition_Record):
	pass


@dataclass
class gamedataSearchFilterMaskTypeValue_Record(gamedataSearchFilterMaskTypeCondition_Record):
	pass


@dataclass
class gamedataSeatState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSectorSelector_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSenseObjectType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSensePreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSenseShape_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSetAttackHitTypeEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataShooterObject_Record(gamedataArcadeObject_Record):
	pass


@dataclass
class gamedataShooterAI_Record(gamedataShooterObject_Record):
	pass


@dataclass
class gamedataShooterBackground_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterBossAI_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterBasilisk_Record(gamedataShooterBossAI_Record):
	pass


@dataclass
class gamedataShooterBullet_Record(gamedataShooterObject_Record):
	pass


@dataclass
class gamedataShooterBulletList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterProjectileAI_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterFlyingDrone_Record(gamedataShooterProjectileAI_Record):
	pass


class gamedataArcadeGameplay_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterGameplay_Record(gamedataArcadeGameplay_Record):
	pass


@dataclass
class gamedataShooterLayerInfo_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterLevel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterLevelList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterMeathead_Record(gamedataShooterBossAI_Record):
	pass


@dataclass
class gamedataShooterMelee_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterNinja_Record(gamedataShooterBossAI_Record):
	pass


@dataclass
class gamedataShooterNPCDrone_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterPickUpTransporter_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterPlayerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterPowerup_Record(gamedataShooterObject_Record):
	pass


@dataclass
class gamedataShooterPowerUpList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterProp_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterRange_Record(gamedataShooterProjectileAI_Record):
	pass


@dataclass
class gamedataShooterRangeGrenade_Record(gamedataShooterProjectileAI_Record):
	pass


@dataclass
class gamedataShooterRescueTransporter_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterSpiderDrone_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterTransporter_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterVFX_Record(gamedataShooterObject_Record):
	pass


@dataclass
class gamedataShooterVFXList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterVIP_Record(gamedataShooterAI_Record):
	pass


@dataclass
class gamedataShooterWeaponData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataShooterWeaponList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicle_Record(gamedataSpawnableObject_Record):
	pass


@dataclass
class gamedataVehicleAIBoostSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAIPanicDrivingSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAirControl_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAirControlAxis_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAITractionEstimation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAIVisionSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleAppearancesToColorTemplate_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleBehaviorData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleBurnOut_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleCameraManager_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleClearCoatOverrides_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleColorTemplate_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleCustomMultilayer_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDataPackage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDecalAttachment_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDefaultState_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDeformablePart_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDeformableZone_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDestructibleGlass_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDestructibleLight_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDestructibleWheel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDestruction_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDestructionPointDamper_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDetachablePart_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDiscountSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDoorDetachRule_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleDriveModelData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleEngineData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFlatTireSimParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFlatTireSimulation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFPPCameraParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxCollision_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxCollisionMaterial_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxWheelsDecals_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxWheelsDecalsMaterial_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxWheelsDecalsMaterialSmear_Record(gamedataVehicleFxWheelsDecalsMaterial_Record):
	pass


@dataclass
class gamedataVehicleFxWheelsParticles_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleFxWheelsParticlesMaterial_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleGear_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleImpactTraffic_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleManufacturer_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleModel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleOffer_Record(gamedataPurchaseOffer_Record):
	pass


@dataclass
class gamedataVehiclePartsClearCoatOverrides_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehiclePIDSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleProceduralFPPCameraParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleSeat_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleSeatSet_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleSteeringSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleStoppingSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleSurfaceBinding_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleSurfaceType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleTPPCameraParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleTPPCameraPresetParams_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleTrafficSuspension_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleUIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleUnlockType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleVisualCustomizationPreviewGlowSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleVisualCustomizationPreviewSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleVisualDestruction_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWater_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWeapon_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelDimensionsPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelDimensionsSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelDrivingPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelDrivingSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
@dataclass
class gamedataVehicleWheelDrivingSetup_2_Record(gamedataVehicleWheelDrivingSetup_Record):
	pass


@dataclass
class gamedataVehicleWheelDrivingSetup_4_Record(gamedataVehicleWheelDrivingSetup_Record):
	pass


class gamedataVehicleWheelRole_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelsFrictionMap_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVehicleWheelsFrictionPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVendor_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVendorWare_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVendorCraftable_Record(gamedataVendorWare_Record):
	pass


@dataclass
class gamedataVendorExperience_Record(gamedataVendorWare_Record):
	pass


@dataclass
class gamedataVendorItem_Record(gamedataVendorWare_Record):
	pass


@dataclass
class gamedataVendorItemQuery_Record(gamedataVendorWare_Record):
	pass


@dataclass
class gamedataVendorProgressionBasedStock_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVendorType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVirtualNetwork_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVirtualNetworkPath_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVisionGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVisionModuleBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataVisualTagsPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataWeakspot_Record(gamedataSpawnableObject_Record):
	pass


@dataclass
class gamedataWeaponEvolution_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponFxPackage_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponManufacturer_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponSafeModeBound_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponSafeModeBounds_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponsTooltipData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponVFXAction_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeaponVFXSet_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeather_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeatherPreset_Record(gamedataSpawnableObject_Record):
	pass


@dataclass
class gamedataWebsite_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWeightedCharacter_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWidgetDefinition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWidgetRatio_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWidgetStyle_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorkspotActionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorkspotCategory_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorkspotReactionType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorldMapFilter_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorldMapFiltersList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorldMapFreeCameraSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorldMapSettings_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataWorldMapZoomLevel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataXPPoints_inline0_Record(gamedataConstantStatModifier_Record):
	pass


@dataclass
class gamedataXPPoints_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gameIReplicatedGameSystem(gameIGameSystem):
	pass


@dataclass
class gameIDebugCheatsSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gameDebugCheatsSystem(gameIDebugCheatsSystem):
	pass


@dataclass
class gameIDebugDrawHistorySystem(gameIGameSystem):
	pass


@dataclass
class gameDebugDrawHistorySystem(gameIDebugDrawHistorySystem):
	pass


class gameDebugPerformanceSystem(gameIGameSystem):
	pass


class gameIDebugPlayerBreadcrumbs(gameIGameSystem):
	pass


class gameDebugPlayerBreadcrumbs(gameIDebugPlayerBreadcrumbs):
	pass


class gameDebugTimeState(gameITimeState):
	pass


class gameIDebugVisualizerSystem(gameIGameSystem):
	pass


class gameDebugVisualizerSystem(gameIDebugVisualizerSystem):
	pass


class gameIDelaySystem(gameIGameSystem):
	pass


class gameDelaySystem(gameIDelaySystem):
	pass


class gameDelaySystemCallbackInfo(gameDelaySystemDelayStruct):
	pass


class gameDelaySystemEventStruct(gameDelaySystemDelayStruct):
	pass


class gameDelaySystemPSEventStruct(gameDelaySystemDelayStruct):
	pass


class gameDelaySystemScriptableSysRequestStruct(gameDelaySystemDelayStruct):
	pass


class gameDelaySystemTickOnEventStruct(gameDelaySystemTickStruct):
	pass


class gameDelaySystemTickWithCallbackStruct(gameDelaySystemTickStruct):
	pass


class worldIDestructibleSpotsSystem(gameIGameSystem):
	pass


class gameDestructibleSpotsSystem(worldIDestructibleSpotsSystem):
	pass


class gameIDestructionPersistencySystem(gameIGameSystem):
	pass


class gameDestructionPersistencySystem(gameIDestructionPersistencySystem):
	pass


@dataclass
class gameDeviceCameraControlComponent(gameComponent):
	pass


@dataclass
class gameDeviceComponent(gameComponent):
	pass


@dataclass
class gameIDeviceInteractionManager(gameIGameSystem):
	pass


@dataclass
class gameDeviceInteractionManager(gameIDeviceInteractionManager):
	pass


@dataclass
class gameIDeviceSystem(gameIGameSystem):
	pass


@dataclass
class gameDeviceSystem(gameIDeviceSystem):
	pass


@dataclass
class gameIDynamicEntityIDSystem(gameIGameSystem):
	pass


@dataclass
class gameDynamicEntityIDSystem(gameIDynamicEntityIDSystem):
	pass


@dataclass
class gameDynamicEventNodeInstance(worldAreaShapeNodeInstance):
	pass


@dataclass
class gameIDynamicSpawnSystem(gameIGameSystem):
	pass


@dataclass
class gameDynamicSpawnSystem(gameIDynamicSpawnSystem):
	pass


@dataclass
class gameEffectAttachment(entIAttachment):
	pass


@dataclass
class gameEffectDuration_Duration_Blackboard(gameEffectDurationModifier):
	pass


@dataclass
class gameEffectDuration_Infinite(gameEffectDurationModifier):
	pass


@dataclass
class gameEffectDuration_Instant(gameEffectDurationModifier):
	pass


@dataclass
class gameEffectDurationModifier_Scripted(gameEffectDurationModifier):
	pass


@dataclass
class gameEffectExecutor(gameEffectNode):
	uses_hit_cooldown: bool = False


@dataclass
class gameEffectExecutor_DamageProjection(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_LandingFX(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_NewEffect(gameEffectExecutor):
	tag_in_this_file: str = ''
	forward_offset: float = 0.0
	child_effect: bool = False
	child_effect_tag: str = ''


@dataclass
class gameEffectExecutor_NewEffect_CopyData(gameEffectExecutor_NewEffect):
	pass


@dataclass
class gameEffectExecutor_NewEffect_ReflectedVector(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_PhysicalImpulseFromInstigator(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_Scripted(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_SendStatusEffect(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_SendStimuli(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_TriggerDestruction(gameEffectExecutor):
	pass


@dataclass
class gameEffectExecutor_UpdateMeleeTireHit(gameEffectExecutor):
	pass


class gameEffectInstance(gameIEffect):
	pass


@dataclass
class gameEffectObjectFilter(gameEffectNode):
	pass


@dataclass
class gameEffectObjectSingleFilter(gameEffectObjectFilter):
	pass


@dataclass
class gameEffectObjectSingleFilter_Scripted(gameEffectObjectSingleFilter):
	pass


@dataclass
class gameEffectObjectFilter_Cone(gameEffectObjectSingleFilter):
	pass


@dataclass
class gameEffectObjectGroupFilter(gameEffectObjectFilter):
	pass


@dataclass
class gameEffectObjectGroupFilter_Cone(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectGroupFilter_Scripted(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_HitRepresentation(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_HitRepresentation_Quickhack(gameEffectObjectFilter_HitRepresentation):
	pass


@dataclass
class gameEffectObjectFilter_HitRepresentation_Sphere(gameEffectObjectFilter_HitRepresentation):
	pass


@dataclass
class gameEffectObjectFilter_HitRepresentation_Sweep_Box(gameEffectObjectFilter_HitRepresentation):
	pass


@dataclass
class gameEffectObjectFilter_HitRepresentation_SweepOverTime_Box(gameEffectObjectFilter_HitRepresentation):
	pass


@dataclass
class gameEffectObjectFilter_IgnoreMountedVehicle(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NearestWeakspotIfAny(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoDuplicates(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoInstigator(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoInstigatorIfPlayerControlled(gameEffectObjectSingleFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoPlayer(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoPuppet(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoSource(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NotAlive(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_NoWeapon(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_TechPreview(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectFilter_Unique(gameEffectObjectGroupFilter):
	pass


@dataclass
class gameEffectObjectProvider(gameEffectNode):
	pass


@dataclass
class gameEffectObjectProvider_ProjectileHitEvent(gameEffectObjectProvider):
	pass


@dataclass
class gameEffectObjectProvider_QueryCapsule(gameEffectObjectProvider):
	gather_only_puppets: bool = False
	query_preset: "physicsQueryPreset" = field(
			default_factory=lambda: physicsQueryPreset()
			)  # TODO: resolve default class (circular import)


@dataclass
class gameEffectObjectProvider_QueryCapsule_GrowOverTime(gameEffectObjectProvider_QueryCapsule):
	pass


@dataclass
class gameEffectObjectProvider_QuerySphere(gameEffectObjectProvider):
	gather_only_puppets: bool = False
	filter_data: "physicsFilterData" = field(
			default_factory=lambda: physicsFilterData()
			)  # TODO: resolve default class (circular import)
	query_preset: "physicsQueryPreset" = field(
			default_factory=lambda: physicsQueryPreset()
			)  # TODO: resolve default class (circular import)


@dataclass
class gameEffectObjectProvider_QueryShockwave(gameEffectObjectProvider_QuerySphere):
	pass


@dataclass
class gameEffectObjectProvider_QuerySphere_GrowOverTime(gameEffectObjectProvider_QuerySphere):
	pass


@dataclass
class gameEffectObjectProvider_Scripted(gameEffectObjectProvider):
	pass


@dataclass
class gameEffectObjectProvider_SingleEntity(gameEffectObjectProvider):
	pass


@dataclass
class gameEffectObjectProvider_Stimuli_EntitiesInRange(gameEffectObjectProvider):
	pass


@dataclass
class gameEffectObjectProvider_SweepOverTime(gameEffectObjectProvider):
	filter_data: "physicsFilterData" = field(
			default_factory=lambda: physicsFilterData()
			)  # TODO: resolve default class (circular import)
	query_preset: "physicsQueryPreset" = field(
			default_factory=lambda: physicsQueryPreset()
			)  # TODO: resolve default class (circular import)


@dataclass
class gameEffectObjectProvider_SweepMelee_Box(gameEffectObjectProvider_SweepOverTime):
	player_static_detection_cone_distance: float = 2.0
	player_static_detection_cone_start_angle: float = 5.0
	player_static_detection_cone_end_angle: float = 18.0
	player_use_camera_for_obstruction_checks: bool = False
	check_melee_invulnerability: bool = True


@dataclass
class gameEffectObjectProvider_SweepMelee_MantisBlades(gameEffectObjectProvider_SweepMelee_Box):
	pass


@dataclass
class gameIEffectorSystem(gameIGameSystem):
	pass


@dataclass
class gameEffectorSystem(gameIEffectorSystem):
	pass


@dataclass
class gameEffectPostAction(gameEffectAction):
	pass


@dataclass
class gameEffectPostAction_BeamVFX(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_BulletTrace(gameEffectPostAction_BeamVFX):
	pass


@dataclass
class gameEffectPostAction_MeleeTireHit(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_MeleeWaterEffects(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_ProcessNearlyHitAgents(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_Scripted(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_UpdateActiveVehicleUIData(gameEffectPostAction):
	pass


@dataclass
class gameEffectPostAction_WaterImpulse(gameEffectPostAction):
	pass


@dataclass
class gameEffectPreAction(gameEffectAction):
	pass


@dataclass
class gameEffectPreAction_Scripted(gameEffectPreAction):
	pass


@dataclass
class gameEffectPreAction_SpreadingEffect(gameEffectPreAction):
	pass


@dataclass
class gameIEffectSpawnerSaveSystem(gameIGameSystem):
	pass


@dataclass
class gameEffectSpawnerSaveSystem(gameIEffectSpawnerSaveSystem):
	pass


@dataclass
class gameIEffectSystem(gameIGameSystem):
	pass


@dataclass
class gameEffectSystem(gameIEffectSystem):
	pass


@dataclass
class gameEffectTriggerNodeInstance(worldAreaShapeNodeInstance):
	pass


@dataclass
class gameIEffectTriggerSystem(gameIGameSystem):
	pass


@dataclass
class gameEffectTriggerSystem(gameIEffectTriggerSystem):
	pass


@dataclass
class gameIPrereqManager(gameIGameSystem):
	pass


@dataclass
class gameEntitiesWithStatusEffectPrereq(gameIPrereq):
	pass


@dataclass
class gameEntitiesWithStatusEffectPrereqState(gamePrereqState):
	pass


@dataclass
class gameEntityIDArrayPrereq(gameIPrereq):
	pass


@dataclass
class gameEntityIDArrayPrereqState(gamePrereqState):
	pass


@dataclass
class gameIEntitySpawnerEventsBroadcaster(gameIGameSystem):
	pass


@dataclass
class gameEntitySpawnerEventsBroadcasterImpl(gameIEntitySpawnerEventsBroadcaster):
	pass


@dataclass
class gameIEntityStubSystem(gameIGameSystem):
	pass


@dataclass
class gameEntityStubSystem(gameIEntityStubSystem):
	pass


@dataclass
class gameIEnvironmentDamageSystem(gameIGameSystem):
	pass


@dataclass
class gameEnvironmentDamageSystem(gameIEnvironmentDamageSystem):
	pass


@dataclass
class gameEquippedPrereqListener(gameIAttachmentSlotsListener):
	pass


@dataclass
class gameEquippedPrereqState(gamePrereqState):
	pass


@dataclass
class gameStatPoolDataModifierStatListener(gameIStatsListener):
	pass


@dataclass
class gameExtraStatPoolDataModifierStatListener(gameStatPoolDataModifierStatListener):
	pass


@dataclass
class gameFinalTimeState(gameITimeState):
	pass


@dataclass
class gameIFootstepSystem(gameIGameSystem):
	pass


@dataclass
class gameFootstepSystem(gameIFootstepSystem):
	pass


@dataclass
class gameScanningEvent(Chunk):
	state: enums.gameScanningState = enums.gameScanningState.Stopped


@dataclass
class SWeaponPlaneParams(Chunk):
	weapon_near_plane_cm: float = 0.0
	blur_intensity: float = 0.0


@dataclass
class gameCameraComponent(entBaseCameraComponent):
	anim_param_fov_override_weight: str = "fovOverride"
	anim_param_fov_override_value: str = "fovValue"
	anim_param_zoom_override_weight: str = "zoomOverride"
	anim_param_zoom_override_value: str = "zoomValue"
	anim_param_zoom_weapon_override_weight: str = "zoomWeaponOverride"
	anim_param_zoom_weapon_override_value: str = "zoomWeaponValue"
	anim_paramdof_intensity: str = "dofIntensity"
	anim_paramdof_near_blur: str = "dofNearBlur"
	anim_paramdof_near_focus: str = "dofNearFocus"
	anim_paramdof_far_blur: str = "dofFarBlur"
	anim_paramdof_far_focus: str = "dofFarFocus"
	fov_override_weight: float = 0.0
	fov_override_value: float = 0.0
	zoom_override_weight: float = 0.0
	zoom_override_value: float = 0.0
	zoom_weapon_override_weight: float = 0.0
	zoom_weapon_override_value: float = 0.0
	anim_param_weapon_near_plane_cm: str = "weaponNearPlane"
	anim_param_weapon_far_plane_cm: str = "weaponFarPlane"
	anim_param_weapon_edges_sharpness: str = "weaponEdgesSharpness"
	anim_param_weapon_vignette_intensity: str = "weaponVignetteIntensity"
	anim_param_weapon_vignette_radius: str = "weaponVignetteRadius"
	anim_param_weapon_vignette_circular: str = "weaponVignetteCircular"
	anim_param_weapon_blur_intensity: str = "weaponBlurIntensity"
	weapon_plane: SWeaponPlaneParams = field(default_factory=SWeaponPlaneParams)


@dataclass
class gameFreeCameraComponent(gameCameraComponent):
	pass


@dataclass
class gameIFriendlyFireSystem(gameIGameSystem):
	pass


@dataclass
class gameFriendlyFireSystem(gameIFriendlyFireSystem):
	pass


@dataclass
class gameIFxSystem(gameIGameSystem):
	pass


@dataclass
class gameFxSystem(gameIFxSystem):
	pass


@dataclass
class gameIGameplayLogicPackageSystem(gameIGameSystem):
	pass


@dataclass
class gameGameplayLogicPackageSystem(gameIGameplayLogicPackageSystem):
	pass


@dataclass
class gameIGameRulesSystem(gameIGameSystem):
	pass


@dataclass
class gameGameRulesSystem(gameIGameRulesSystem):
	pass


@dataclass
class gameGameSession(gameBaseGameSession):
	pass


@dataclass
class gameGameTagSystem(gameIGameSystem):
	pass


@dataclass
class gameIGodModeSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gameGodModeSystem(gameIGodModeSystem):
	pass


@dataclass
class gameIOnlineSystem(gameIGameSystem):
	pass


@dataclass
class gameGOGRewardsSystem(gameIOnlineSystem):
	pass


@dataclass
class gamegpsIGPSSystem(gameIGameSystem):
	pass


@dataclass
class gamegpsGPSSystem(gamegpsIGPSSystem):
	pass


@dataclass
class gameHasDialogVisualizerVisiblePrereq(gameIPrereq):
	pass


@dataclass
class gameHasDialogVisualizerVisiblePrereqState(gamePrereqState):
	pass


@dataclass
class gameIHitRepresentationSystem(gameIGameSystem):
	pass


@dataclass
class gameHitRepresentationSystem(gameIHitRepresentationSystem):
	pass


@dataclass
class gameIAchievementSystem(gameIGameSystem):
	pass


@dataclass
class gameIActionsFactory(gameIGameSystem):
	pass


@dataclass
class gameIActivityCardsSystem(gameIGameSystem):
	pass


@dataclass
class gameIActivityLogSystem(gameIGameSystem):
	pass


@dataclass
class gameIAIDirectorSystem(gameIGameSystem):
	pass


@dataclass
class gameIAreaManager(gameIGameSystem):
	pass


@dataclass
class gameIAttitudeManager(gameIGameSystem):
	pass


@dataclass
class gameIAutoSaveSystem(gameIGameSystem):
	pass


@dataclass
class gameIBlackboardSystem(gameIGameSystem):
	pass


@dataclass
class gameIBlackboardUpdateProxy(gameIGameSystem):
	pass


@dataclass
class gameIBreachSystem(gameIGameSystem):
	pass


@dataclass
class gameICameraSystem(gameIGameSystem):
	pass


@dataclass
class gameIClientEntitySpawnSystem(gameIGameSystem):
	pass


@dataclass
class gameICollisionQueriesSystem(gameIGameSystem):
	pass


@dataclass
class gameICombatQueriesSystem(gameIGameSystem):
	pass


@dataclass
class gameICommunitySystem(gameIGameSystem):
	pass


@dataclass
class gameICompanionSystem(gameIGameSystem):
	pass


@dataclass
class gameIComponentsStateSystem(gameIGameSystem):
	pass


@dataclass
class gameIContainerManager(gameIGameSystem):
	pass


@dataclass
class gameICooldownSystem(gameIGameSystem):
	pass


@dataclass
class gameIDamageSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gameIDebugSystem(gameIGameSystem):
	pass


@dataclass
class gameScriptableSystem(gameIScriptableSystem):
	pass


@dataclass
class gameIEquipmentSystem(gameScriptableSystem):
	pass


@dataclass
class gameIGameAudioSystem(gameIGameSystem):
	pass


class gameIGlobalTvSystem(gameIGameSystem):
	pass


@dataclass
class gameIInventoryManager(gameIGameSystem):
	pass


@dataclass
class gameIItemFactorySystem(gameIGameSystem):
	pass


@dataclass
class gameIJournalManager(gameIReplicatedGameSystem):
	pass


@dataclass
class gameILevelAssignmentSystem(gameIGameSystem):
	pass


@dataclass
class gameILocationManager(gameIGameSystem):
	pass


@dataclass
class gameILootManager(gameIGameSystem):
	pass


@dataclass
class gameIMarketSystem(gameScriptableSystem):
	pass


@dataclass
class gameIMinimapSystem(gameIGameSystem):
	pass


@dataclass
class gameIMovingPlatformMovementInitData(Chunk):
	init_type: enums.gameMovingPlatformMovementInitializationType = enums.gameMovingPlatformMovementInitializationType.Time
	init_value: float = 0.0


@dataclass
class gameIMovingPlatformMovement(Chunk):
	init_data: gameIMovingPlatformMovementInitData = field(default_factory=gameIMovingPlatformMovementInitData)
	end_node: str = ''


@dataclass
class gameIMovingPlatformMovementPointToPoint(gameIMovingPlatformMovement):
	pass


@dataclass
class gameIMovingPlatformSystem(gameIGameSystem):
	pass


@dataclass
class gameImpostorComponentSlotListener(gameIAttachmentSlotsListener):
	pass


@dataclass
class gameinfluenceISystem(gameIGameSystem):
	pass


@dataclass
class gameinfluenceSystem(gameinfluenceISystem):
	pass


@dataclass
class gameinteractionsChoiceCaptionScriptPart(gameinteractionsChoiceCaptionPart):
	pass


@dataclass
class gameinteractionsIManager(gameIGameSystem):
	pass


@dataclass
class gameinteractionsCManager(gameinteractionsIManager):
	pass


@dataclass
class gameinteractionsOnScreenTestPredicate(gameinteractionsIPredicateType):
	pass


@dataclass
class gameinteractionsOrbActivationPredicate(gameinteractionsIPredicateType):
	pass


@dataclass
class gameinteractionsPublisherActivationEvent(gameinteractionsPublisherBaseEvent):
	pass


@dataclass
class gameinteractionsPublisherChoiceEvent(gameinteractionsPublisherBaseEvent):
	pass


@dataclass
class gameinteractionsSuppressedPredicate(gameinteractionsIPredicateType):
	pass


@dataclass
class gametargetingSystemTargetFilter_Closest(gametargetingSystemTargetFilter):
	pass


@dataclass
class gameinteractionsTargetFilter_Logical(gametargetingSystemTargetFilter_Closest):
	pass


@dataclass
class gametargetingSystemTargetFilterResult(Chunk):
	hit_ent_id: entEntityID = field(default_factory=entEntityID)
	hit_component: entIComponent = field(default_factory=entIComponent)


@dataclass
class gameinteractionsTargetFilterResult_Logical(gametargetingSystemTargetFilterResult):
	pass


@dataclass
class gameinteractionsvisDeviceVisualizerFamily(gameinteractionsvisFamilyBase):
	pass


@dataclass
class gameinteractionsvisIGroupedVisualizerLogic(gameinteractionsvisIVisualizerLogicInterface):
	pass


@dataclass
class gameinteractionsvisDeviceVisualizerLogic(gameinteractionsvisIGroupedVisualizerLogic):
	pass


@dataclass
class gameinteractionsvisDialogVisualizerFamily(gameinteractionsvisFamilyBase):
	pass


@dataclass
class gameinteractionsvisDialogVisualizerLogic(gameinteractionsvisIGroupedVisualizerLogic):
	pass


@dataclass
class gameinteractionsvisIVisualizerDefinition(Chunk):
	flags: enums.gameinteractionsvisEVisualizerDefinitionFlags = enums.gameinteractionsvisEVisualizerDefinitionFlags._None


@dataclass
class gameinteractionsvisLootVisualizerDefinition(gameinteractionsvisIVisualizerDefinition):
	pass


@dataclass
class gameinteractionsvisLootVisualizerFamily(gameinteractionsvisFamilyBase):
	pass


@dataclass
class gameinteractionsvisLootVisualizerLogic(gameinteractionsvisIVisualizerLogicInterface):
	pass


@dataclass
class gameIntervalTimer(gameBaseTimer):
	pass


@dataclass
class gameInventoryListenerData_InventoryEmpty(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_ItemAdded(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_ItemExtracted(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_ItemNotification(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_ItemQuantityChanged(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_ItemRemoved(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_PartAdded(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryListenerData_PartRemoved(gameInventoryListenerData_Base):
	pass


@dataclass
class gameInventoryManager(gameIInventoryManager):
	pass


@dataclass
class gameInventoryPrereqState(gamePrereqState):
	pass


@dataclass
class gameInventoryScriptListener(gameIInventoryListener):
	pass


@dataclass
class gameIObjectCarrySystem(gameIGameSystem):
	pass


@dataclass
class gameIObjectPoolSystem(gameIGameSystem):
	pass


@dataclass
class gameIPersistencySystem(gameIGameSystem):
	pass


@dataclass
class gameIPhantomEntitySystem(gameIGameSystem):
	pass


@dataclass
class gameIPhotoModeSystem(gameIGameSystem):
	pass


@dataclass
class gameIPingSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gameIPlayerHandicapSystem(gameScriptableSystem):
	pass


@dataclass
class gameIPlayerManager(gameIGameSystem):
	pass


@dataclass
class gameIPlayerSystem(gameIGameSystem):
	pass


@dataclass
class gameIPoliceRadioSystem(gameIGameSystem):
	pass


@dataclass
class gameIPopulationSystem(gameIGameSystem):
	pass


@dataclass
class gameIPreventionSpawnSystem(gameIGameSystem):
	pass


@dataclass
class gameIProjectileSystem(gameIGameSystem):
	pass


@dataclass
class gameIPuppetUpdaterSystem(gameIGameSystem):
	pass


@dataclass
class gameIRazerChromaEffectsSystem(gameIGameSystem):
	pass


@dataclass
class gameIRealTimeEventSystem(gameIGameSystem):
	pass


@dataclass
class gameIRenderGameplayEffectsManagerSystem(gameIGameSystem):
	pass


@dataclass
class gameIRichPresenceSystem(gameIGameSystem):
	pass


@dataclass
class gameIComparisonPrereq(gameIPrereq):
	comparison_type: enums.gameComparisonType = enums.gameComparisonType.EQUAL


@dataclass
class gameIRPGPrereq(gameIComparisonPrereq):
	pass


@dataclass
class gameISaveSanitizationForbiddenAreaSystem(gameIGameSystem):
	pass


@dataclass
class gameISceneSystem(gameIGameSystem):
	pass


@dataclass
class gameISchematicSystem(gameIGameSystem):
	pass


@dataclass
class gameIScriptablePrereq(gameIPrereq):
	pass


@dataclass
class gameIScriptableSystemsContainer(gameIGameSystem):
	pass


@dataclass
class gameIScriptsDebugOverlaySystem(gameIGameSystem):
	pass


@dataclass
class gameIShootingAccuracySystem(gameIGameSystem):
	pass


@dataclass
class gameISpatialQueriesSystem(gameIGameSystem):
	pass


@dataclass
class gameIStatPoolsSystem(gameIGameSystem):
	pass


@dataclass
class gameIStatsDataSystem(gameIGameSystem):
	pass


@dataclass
class gameIStatsSystem(gameIGameSystem):
	pass


@dataclass
class gameIStatusComboSystem(gameIGameSystem):
	pass


@dataclass
class gameIStatusEffectSystem(gameIGameSystem):
	pass


@dataclass
class gameIStimuliSystem(gameIGameSystem):
	pass


@dataclass
class gameIStreamingMonitorSystem(gameIGameSystem):
	pass


@dataclass
class gameISubtitleHandlerSystem(gameIGameSystem):
	pass


@dataclass
class gameIsVisualizerActivePrereq(gameIPrereq):
	pass


@dataclass
class gameIsVisualizerActivePrereqState(gamePrereqState):
	pass


@dataclass
class gameITargetingSystem(gameIGameSystem):
	pass


@dataclass
class gameITelemetrySystem(gameIGameSystem):
	pass


@dataclass
class gameITeleportationFacility(gameIGameSystem):
	pass


@dataclass
class gameItemFactorySystem(gameIItemFactorySystem):
	pass


@dataclass
class gameITierSystem(gameIGameSystem):
	pass


@dataclass
class gameITimeSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gameITransactionSystem(gameIGameSystem):
	pass


@dataclass
class gameITransformAnimatorSaveSystem(gameIGameSystem):
	pass


@dataclass
class gameITransformsHistorySystem(gameIGameSystem):
	pass


@dataclass
class gameIVehicleSystem(gameIGameSystem):
	pass


@dataclass
class gameIVisionModeSystem(gameIGameSystem):
	pass


@dataclass
class gameIWardrobeSystem(gameIGameSystem):
	pass


@dataclass
class gameIWatchdogSystem(gameIGameSystem):
	pass


@dataclass
class gameIWorkspotGameSystem(gameIGameSystem):
	pass


@dataclass
class gameIWorldBoundarySystem(gameIGameSystem):
	pass


@dataclass
class gameJournalEntryOverrideData(Chunk):
	input_device: enums.inputESimplifiedInputDevice = enums.inputESimplifiedInputDevice.KBM
	input_scheme: enums.inputEInputScheme = enums.inputEInputScheme.LEGACY
	overridden_localization_string: LocalizationString = field(default_factory=LocalizationString)


@dataclass
class gameJournalEntry(Chunk):
	id: str = ''
	journal_entry_override_data_list: list[gameJournalEntryOverrideData] = field(default_factory=list)


@dataclass
class gameJournalBriefingBaseSection(gameJournalEntry):
	pass


@dataclass
class gameJournalContainerEntry(gameJournalEntry):
	entries: list[gameJournalEntry] = field(default_factory=list)


@dataclass
class gameJournalFileEntry(gameJournalContainerEntry):
	pass


@dataclass
class gameJournalManager(gameIJournalManager):
	pass


@dataclass
class gameJournalFolderEntry(gameJournalContainerEntry):
	pass


@dataclass
class gameJournalPrimaryFolderEntry(gameJournalFolderEntry):
	pass


@dataclass
class gameKillTriggerNode(worldAreaShapeNode):
	pass


@dataclass
class gameKillTriggerNodeInstance(worldAreaShapeNodeInstance):
	pass


@dataclass
class gameLevelAssignmentSystem(gameILevelAssignmentSystem):
	pass


@dataclass
class gameLocationManager(gameILocationManager):
	pass


@dataclass
class gameLootBagInventoryListener(gameIInventoryListener):
	pass


@dataclass
class gameLootManager(gameILootManager):
	pass


@dataclass
class gameLoSIFinderSystem(gameIGameSystem):
	pass


@dataclass
class gameLoSFinderSystem(gameLoSIFinderSystem):
	pass


@dataclass
class gamemappinsIMappin(gamemappinsIVisualObject):
	pass


@dataclass
class gamemappinsRuntimeMappin(gamemappinsIMappin):
	pass


@dataclass
class gamemappinsCustomPositionMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gamemappinsFastTravelMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gamemappinsGrenadeMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gamemappinsIArea(gamemappinsIVisualObject):
	pass


@dataclass
class gamemappinsIMappinSystem(gameIReplicatedGameSystem):
	pass


@dataclass
class gamemappinsInteractionMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gamemappinsMappinScriptData(Chunk):
	stat_pool_type: enums.gamedataStatPoolType = enums.gamedataStatPoolType.Invalid


@dataclass
class gamemappinsMappinData(gamemappinsIMappinData):
	mappin_type: int = 0
	variant: enums.gamedataMappinVariant = enums.gamedataMappinVariant.DefaultQuestVariant
	active: bool = True
	debug_caption: str = ''
	localized_caption: LocalizationString = field(default_factory=LocalizationString)
	visible_through_walls: bool = True
	script_data: gamemappinsMappinScriptData = field(default_factory=gamemappinsMappinScriptData)


@dataclass
class gamemappinsInteractionMappinInitialData(gamemappinsMappinData):
	pass


@dataclass
class gamemappinsInteractionMappinUpdateData(gamemappinsIMappinUpdateData):
	pass


@dataclass
class gamemappinsMappinSystem(gamemappinsIMappinSystem):
	pass


@dataclass
class gamemappinsOutlineArea(gamemappinsIArea):
	pass


@dataclass
class gamemappinsPointOfInterestMappin(gamemappinsIMappin):
	pass


@dataclass
class gamemappinsQuestMappin(gamemappinsIMappin):
	pass


@dataclass
class gamemappinsRuntimeGenericMappinData(gamemappinsIRuntimeMappinData):
	pass


@dataclass
class gamemappinsRuntimeInteractionMappinData(gamemappinsIRuntimeMappinData):
	pass


@dataclass
class gamemappinsRuntimePointOfInterestMappinData(gamemappinsIRuntimeMappinData):
	pass


@dataclass
class gamemappinsRuntimeQuestMappinData(gamemappinsIRuntimeMappinData):
	pass


@dataclass
class gamemappinsRuntimeStubMappinData(gamemappinsIRuntimeMappinData):
	pass


@dataclass
class gamemappinsStealthMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gamemappinsStealthMappinStatsListener(gameIStatsListener):
	pass


@dataclass
class gamemappinsStubMappin(gamemappinsIMappin):
	pass


@dataclass
class gamemappinsStubMappinData(gamemappinsMappinData):
	pass


@dataclass
class gamemappinsVehicleMappin(gamemappinsRuntimeMappin):
	pass


@dataclass
class gameMinimapSystem(gameIMinimapSystem):
	pass


@dataclass
class gameModdingSystem(gameIGameSystem):
	pass


@dataclass
class gamemountingIMountingFacility(gameIGameSystem):
	pass


@dataclass
class gamemountingIMountingPublisher(gameIGameSystem):
	pass


@dataclass
class gamemountingMountableComponent(entIComponent):
	pass


@dataclass
class gamemountingMountingFacility(gamemountingIMountingFacility):
	pass


@dataclass
class gamemountingMountingPublisher(gamemountingIMountingPublisher):
	pass


@dataclass
class gameMovingPlatformMoveTo(Chunk):
	movement: gameIMovingPlatformMovement = field(default_factory=gameIMovingPlatformMovement)
	destination_name: str = ''
	data: int = 0
	is_elevator: bool = False


@dataclass
class gameMovingPlatformRestoreMoveTo(gameMovingPlatformMoveTo):
	pass


@dataclass
class gameMovingPlatformSystem(gameIMovingPlatformSystem):
	pass


@dataclass
class gameMuppetComponent(entIComponent):
	pass


@dataclass
class gameMuppetInputActionActivateScanning(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionAimDownSight(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionCrouch(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionJump(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionMeleeAttack(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionQuickMelee(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionReloadWeapon(gameIMuppetInputAction):
	pass


@dataclass
class gameMuppetInputActionUseConsumable(gameIMuppetInputAction):
	pass


@dataclass
class gameuiWidgetGameController(worlduiIWidgetGameController):
	pass


@dataclass
class gameuiHUDGameController(gameuiWidgetGameController):
	show_anim_def: inkanimDefinition = field(default_factory=inkanimDefinition)
	hide_anim_def: inkanimDefinition = field(default_factory=inkanimDefinition)
	show_animation_name: str = "unfold"
	hide_animation_name: str = "fold"
	module_shown: bool = False
	show_anim_proxy: inkanimProxy = field(default_factory=inkanimProxy)
	hide_anim_proxy: inkanimProxy = field(default_factory=inkanimProxy)


@dataclass
class gameMuppetInventoryGameController(gameuiHUDGameController):
	pass


@dataclass
class gameMuppetLoadoutsGameController(gameuiHUDGameController):
	pass


@dataclass
class gameNativeAutodriveSystem(gameScriptableSystem):
	pass


@dataclass
class gameNativeHudManager(gameScriptableSystem):
	pass


@dataclass
class gameNotPrereqState(gamePrereqState):
	pass


@dataclass
class gamePuppetStatPoolsListener(gameIStatPoolsListener):
	pass


@dataclass
class gameNPCHealthStatPoolsListener(gamePuppetStatPoolsListener):
	pass


@dataclass
class gameNPCQuickHackUploadStatPoolsListener(gamePuppetStatPoolsListener):
	pass


@dataclass
class gamePuppetStatsListener(gameIStatsListener):
	pass


@dataclass
class gameNPCStatsListener(gamePuppetStatsListener):
	pass


@dataclass
class gameObjectCarrySystem(gameIObjectCarrySystem):
	pass


@dataclass
class gameObjectDeathListener(gameIStatPoolsListener):
	pass


@dataclass
class gameObjectPoolSystem(gameIObjectPoolSystem):
	pass


@dataclass
class gameObjectPS(gamePersistentState):
	pass


@dataclass
class gamePersistencySystem(gameIPersistencySystem):
	pass


@dataclass
class gamePhantomEntitySystem(gameIPhantomEntitySystem):
	pass


@dataclass
class gamePhotoModeAttachmentSlotsListener(gameIAttachmentSlotsListener):
	pass


@dataclass
class gamePhotomodeLightComponent(entLightComponent):
	pass


@dataclass
class gamePhotoModeSystem(gameIPhotoModeSystem):
	pass


@dataclass
class gamePingSystem(gameIPingSystem):
	pass


@dataclass
class gameplayeractionsAttachSlotListener(gameIAttachmentSlotsListener):
	pass


@dataclass
class gamePlayerArmorStatPoolsListener(gamePuppetStatPoolsListener):
	pass


@dataclass
class gamePlayerHealthStatPoolsListener(gamePuppetStatPoolsListener):
	pass


@dataclass
class gamePlayerManager(gameIPlayerManager):
	pass


@dataclass
class gamePlayerProximityPrereqState(gamePrereqState):
	pass


@dataclass
class gamePlayerStatsListener(gamePuppetStatsListener):
	pass


@dataclass
class gamePlayerSystem(gameIPlayerSystem):
	pass


@dataclass
class ScriptableDeviceComponent(gameDeviceComponent):
	pass


@dataclass
class redResourceReferenceScriptToken(Chunk):
	resource: Chunk = field(default_factory=Chunk)  # TODO: CResourceAsyncReference


@dataclass
class SWidgetPackageBase(Chunk):
	library_path: redResourceReferenceScriptToken = field(default_factory=redResourceReferenceScriptToken)
	library_id: str = ''
	widget_tweak_dbid: int = 0
	widget: inkWidget = field(default_factory=inkWidget)
	widget_name: str = ''
	placement: enums.EWidgetPlacementType = enums.EWidgetPlacementType.DOCKED
	orientation: enums.inkEOrientation = enums.inkEOrientation.Horizontal
	is_valid: bool = True


@dataclass
class gamePersistentID(Chunk):
	entity_hash: int = 0
	component_name: str = ''


@dataclass
class SWidgetPackage(SWidgetPackageBase):
	display_name: str = ''
	owner_id: gamePersistentID = field(default_factory=gamePersistentID)
	owner_idclass_name: str = ''
	custom_data: WidgetCustomData = field(default_factory=WidgetCustomData)
	is_widget_inactive: bool = False
	widget_state: enums.EWidgetState = enums.EWidgetState.DEFAULT
	icon_id: str = ''
	bckground_texture_id: int = 0
	icon_texture_id: int = 0
	text_data: textTextParameterSet = field(default_factory=textTextParameterSet)


@dataclass
class SActionWidgetPackage(SWidgetPackage):
	action: gamedeviceAction = field(default_factory=gamedeviceAction)
	was_initalized: bool = False
	dependend_actions: list[gamedeviceAction] = field(default_factory=list)


@dataclass
class IllegalActionTypes(Chunk):
	regular_actions: bool = False
	quick_hacks: bool = False
	skill_checks: bool = True


@dataclass
class SecuritySystemClearanceEntry(Chunk):
	user: entEntityID = field(default_factory=entEntityID)
	level: enums.ESecurityAccessLevel = enums.ESecurityAccessLevel.ESL_NONE


@dataclass
class SpiderbotScavengeOptions(Chunk):
	scavengable_by_spiderbot: bool = False


@dataclass
class SecurityAccessLevelEntry(Chunk):
	keycard: int = 0
	password: str = ''


@dataclass
class SecurityAccessLevelEntryClient(SecurityAccessLevelEntry):
	level: enums.ESecurityAccessLevel = enums.ESecurityAccessLevel.ESL_NONE


@dataclass
class AuthorizationData(Chunk):
	is_authorization_module_on: bool = True
	always_expose_actions: bool = False
	authorization_data_entry: SecurityAccessLevelEntryClient = field(
			default_factory=SecurityAccessLevelEntryClient
			)


@dataclass
class SPerformedActions(Chunk):
	id: str = ''
	action_context: list[enums.EActionContext] = field(default_factory=list)


@dataclass
class DisassembleOptions(Chunk):
	can_be_disassembled: bool = False


@dataclass
class ElectricLightController(ScriptableDeviceComponent):
	pass


@dataclass
class GameplayLightController(ElectricLightController):
	pass


@dataclass
class gamePopulationSystem(gameIPopulationSystem):
	pass


@dataclass
class gamePrereqManager(gameIPrereqManager):
	pass


@dataclass
class gamePreventionSpawnSystem(gameIPreventionSpawnSystem):
	pass


@dataclass
class gameUniqueItemData(gameItemData):
	pass


@dataclass
class gamePreviewItemData(gameUniqueItemData):
	pass


@dataclass
class gameprojectileLinearMovementEvent(Chunk):
	target_position: tuple[float, float, float, float] = (sys.maxsize, sys.maxsize, sys.maxsize, 1.0)


@dataclass
class gameprojectileAcceleratedMovementEvent(gameprojectileLinearMovementEvent):
	pass


@dataclass
class gameprojectileParabolicTrajectoryParams(gameprojectileTrajectoryParams):
	pass


@dataclass
class gameprojectileScriptCollisionEvaluator(gameprojectileCollisionEvaluator):
	pass


@dataclass
class gameRicochetData(Chunk):
	count: int = 0
	range: float = 0.0
	target_search_angle: float = 0.0
	min_angle: float = 0.0
	max_angle: float = 0.0
	chance: float = 0.0


@dataclass
class gameprojectileWeaponParams(Chunk):
	target_position: tuple[float, float, float, float] = (sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize)
	smart_gun_spread_on_hit_plane: tuple[float, float, float] = (0.0, 0.0, 0.0)
	charge: float = 0.0
	tracked_target_component: entIPlacedComponent = field(default_factory=entIPlacedComponent)
	smart_gun_accuracy: float = 1.0
	smart_gun_is_projectile_guided: bool = True
	hit_plane_offset: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	shooting_offset: float = 0.0
	ignore_weapon_owner_collision: bool = True
	ignore_mounted_vehicle_collision: bool = False
	ricochet_data: gameRicochetData = field(default_factory=gameRicochetData)
	range: float = -1.0


@dataclass
class gameProjectileSystem(gameIProjectileSystem):
	pass


@dataclass
class gamePuppetStatusEffectListener(gameIStatusEffectListener):
	pass


@dataclass
class gamePuppetUpdaterSystem(gameIPuppetUpdaterSystem):
	pass


@dataclass
class gameRandomStatModifier(gameStatModifierBase):
	pass


@dataclass
class gameRazerChromaEffectsSystem(gameIRazerChromaEffectsSystem):
	pass


@dataclass
class gameRealTimeEventSystem(gameIRealTimeEventSystem):
	pass


@dataclass
class gameRecordIdSpawnModifier(populationModifier):
	pass


@dataclass
class gameRemoveCooldownEvent(gameCooldownSystemEvent):
	pass


@dataclass
class gameRenderGameplayEffectsManagerSystem(gameIRenderGameplayEffectsManagerSystem):
	pass


@dataclass
class gameReplAnimTransformSyncAnimRequest(gameReplAnimTransformRequestBase):
	pass


@dataclass
class gameRichPresenceSystem(gameIRichPresenceSystem):
	pass


@dataclass
class gameRPGPrereqState(gamePrereqState):
	pass


@dataclass
class gameRuntimeSystemLights(worldIRuntimeSystem):
	pass


@dataclass
class gameSaveSanitizationForbiddenAreaSystem(gameISaveSanitizationForbiddenAreaSystem):
	pass


@dataclass
class gameScanningEventForInstigator(gameScanningEvent):
	pass


@dataclass
class gameSceneTier(senseStimuliData):
	pass


@dataclass
class gameScreenshot360CameraComponent(gameCameraComponent):
	pass


@dataclass
class gameScriptableSystemsContainer(gameIScriptableSystemsContainer):
	pass


@dataclass
class gameScriptedDamageSystemListener(gameIDamageSystemListener):
	pass


@dataclass
class gamedataSpreadAreaEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataSpreadEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataSpreadInitEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataSquadBackyardBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSquadBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSquadFenceBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSquadInstance_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStat_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatChangedPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataStatDistributionData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatModifierGroup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatPool_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatPoolCost_Record(gamedataObjectActionCost_Record):
	pass


@dataclass
class gamedataStatPoolDistributionData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatPoolPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataStatPoolUpdate_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatsArray_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatsFolder_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatsList_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffect_inline0_Record(gamedataStatModifierGroup_Record):
	pass


@dataclass
class gamedataStatusEffect_inline1_Record(gamedataConstantStatModifier_Record):
	pass


@dataclass
class gamedataStatusEffect_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataGameplayRestrictionStatusEffect_Record(gamedataStatusEffect_Record):
	pass


@dataclass
class gamedataWorkspotStatusEffect_Record(gamedataStatusEffect_Record):
	pass


@dataclass
class gamedataStatusEffectAIBehaviorFlag_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectAIBehaviorType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectAIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectAttackData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectFX_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectPlayerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataStatusEffectType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectUIData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStatusEffectVariation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStickyGDM_Record(gamedataGrenadeDeliveryMethod_Record):
	pass


@dataclass
class gamedataStim_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStimPriority_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStimPropagation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStimTargets_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStimType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStop_Record(gamedataProjectileCollision_Record):
	pass


@dataclass
class gamedataStopAndStick_Record(gamedataProjectileCollision_Record):
	pass


@dataclass
class gamedataStopAndStickPerpendicular_Record(gamedataProjectileCollision_Record):
	pass


@dataclass
class gamedataStrategyData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataStreetCredTier_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataSubCharacter_Record(gamedataCharacter_Record):
	pass


@dataclass
class gamedataSubstat_Record(gamedataStat_Record):
	pass


@dataclass
class gamedataSubStatModifier_Record(gamedataStatModifier_Record):
	pass


@dataclass
class gamedataTacticLimiterCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataTankArrangement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankBackgroundData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankDecorationSpawnerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankDriveModelData_Record(gamedataVehicleDriveModelData_Record):
	pass


@dataclass
class gamedataTankDestroyableObject_Record(gamedataArcadeCollidableObject_Record):
	pass


@dataclass
class gamedataTankEnemy_Record(gamedataTankDestroyableObject_Record):
	pass


@dataclass
class gamedataTankEnemySpawnerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankGameplay_Record(gamedataArcadeGameplay_Record):
	pass


@dataclass
class gamedataTankGameplayData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankLevelGameplay_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankLevelObject_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankLevelObjectID_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankLevelSpawnableArrangement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankObstacleSpawnerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankPickup_Record(gamedataArcadeCollidableObject_Record):
	pass


@dataclass
class gamedataTankPickupSpawnerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankPlayerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankPlayerWeaponLevel_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankProjectile_Record(gamedataArcadeCollidableObject_Record):
	pass


@dataclass
class gamedataTankProjectileSpawnerData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankScoreMultiplierBreakpoint_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankSpawnableArrangement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTankWeapon_Record(gamedataArcadeObject_Record):
	pass


@dataclass
class gamedataTemporalPrereq_Record(gamedataIPrereq_Record):
	pass


@dataclass
class gamedataTerminalScreenType_Record(gamedataDeviceScreenType_Record):
	pass


@dataclass
class gamedataThreatDistanceCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataThreatTrackingPresetBase_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataThumbnailWidgetDefinition_Record(gamedataWidgetDefinition_Record):
	pass


@dataclass
class gamedataTime_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTPPCameraSetup_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTPPLookAtPresets_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTracking_Record(gamedataProjectileLaunch_Record):
	pass


@dataclass
class gamedataTrackingMode_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTrait_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTraitData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTransgression_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTrap_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTrapType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTriggerAttackEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataTriggerHackingMinigameEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataTriggerMode_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataTVBase_Record(gamedataDevice_Record):
	pass


@dataclass
class gamedataUIAnimation_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUICharacterCreationAttribute_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUICharacterCreationAttributesPreset_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUICharacterCustomizationResourcePaths_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUICondition_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIElement_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIIconCensorFlag_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIIconCensorship_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIIconPool_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUINameplate_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUINameplateDisplayType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUIStatsMap_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUncontrolledMovementEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataUpgradingData_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataUphillDriveHelper_Record(gamedataDriveHelper_Record):
	pass


@dataclass
class gamedataUseConsumableEffector_Record(gamedataEffector_Record):
	pass


@dataclass
class gamedataUtilityLossCoverSelectionParameters_Record(gamedataCoverSelectionParameters_Record):
	pass


@dataclass
class gamedataDamageType_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataContentAssignment_Record(gamedataTweakDBRecord):
	pass


@dataclass
class gamedataValueAssignment_Record(gamedataContentAssignment_Record):
	pass


@dataclass
class gamedataDataNode(Chunk):
	node_type: enums.gamedataDataNodeType = enums.gamedataDataNodeType.File
	file_name: str = ''
	parent: "gamedataDataNode" = field(
			default_factory=lambda: gamedataDataNode()
			)  # TODO: resolve default class (circular import)


@dataclass
class gamedataValueDataNode(gamedataDataNode):
	pass


@dataclass
class gameTargetShootComponent(entIComponent):
	# TODO: name = "Component"
	weapon_record: gamedataWeaponItem_Record = field(default_factory=gamedataWeaponItem_Record)
	weapon_tdbid: int = 0
	character_record: gamedataCharacter_Record = field(default_factory=gamedataCharacter_Record)
	character_tdbid: int = 0


@dataclass
class gameVisionModeSystemRevealIdentifier(Chunk):
	source_entity_id: entEntityID = field(default_factory=entEntityID)
	reason: str = ''


@dataclass
class gameVisionModeComponent(gameComponent):
	# TODO: name = "vision";
	default_highlight_data: Any = None  # TODO: HighlightEditableData = field(default_factory=HighlightEditableData)
	forced_highlights: list[Any] = field(default_factory=list)  # TODO: FocusForcedHighlightData
	active_forced_highlight: Any = None  # TODO: FocusForcedHighlightData = field(default_factory=FocusForcedHighlightData)
	current_default_highlight: Any = None  # TODO: FocusForcedHighlightData = field(default_factory=FocusForcedHighlightData)
	active_reveal_requests: list[gameVisionModeSystemRevealIdentifier] = field(default_factory=list)
	is_focus_mode_active: bool = False
	was_cleaned_up: bool = False
	slave_objects_to_highlight: list[entEntityID] = field(default_factory=list)


@dataclass
class gameStatusEffectComponent(gameComponent):
	# TODO: name = "StatusEffect";
	pass


@dataclass
class gameObject(entGameEntity):
	persistent_state: gamePersistentState = field(default_factory=gamePersistentState)
	player_socket: gamePlayerSocket = field(default_factory=gamePlayerSocket)
	ui_slot_component: entSlotComponent = field(default_factory=entSlotComponent)
	tags: Chunk = field(default_factory=Chunk)
	display_name: LocalizationString = field(default_factory=LocalizationString)
	display_description: LocalizationString = field(default_factory=LocalizationString)
	audio_resource_name: str = ''
	visibility_check_distance: float = 16000.0
	force_register_in_hud_manager: bool = False
	prereq_listeners: list[GameObjectListener] = field(default_factory=list)
	status_effect_listeners: list[Any] = field(default_factory=list)  # TODO: StatusEffectTriggerListener
	last_engine_time: float = 0.0
	accumulated_time_passsed: float = 0.0
	scanning_component: gameScanningComponent = field(default_factory=gameScanningComponent)
	vision_component: gameVisionModeComponent = field(default_factory=gameVisionModeComponent)
	is_highlighted_in_focus_mode: bool = False
	status_effect_component: gameStatusEffectComponent = field(default_factory=gameStatusEffectComponent)
	mark_as_quest: bool = False
	e3object_revealed: bool = False
	workspot_mapper: "WorkspotMapperComponent" = field(
			default_factory=lambda: WorkspotMapperComponent()
			)  # TODO: resolve default class (circular import)
	stim_broadcaster: Any = None  # TODO: StimBroadcasterComponent = field(default_factory=StimBroadcasterComponent)
	squad_member_component: Any = None  # TODO: SquadMemberBaseComponent = field(default_factory=SquadMemberBaseComponent)
	source_shoot_component: Any = None  # TODO: gameSourceShootComponent = field(default_factory=gameSourceShootComponent)
	target_shoot_component: gameTargetShootComponent = field(default_factory=gameTargetShootComponent)
	received_damage_history: list[Any] = field(default_factory=list)  # TODO: DamageHistoryEntry
	force_defeat_reward: bool = False
	kill_reward_disabled: bool = False
	will_die_soon: bool = False
	is_scanner_data_dirty: bool = False
	has_visibility_forced_in_anim_system: bool = False
	is_dead: bool = False
	last_hit_instigator_id: entEntityID = field(default_factory=entEntityID)
	hit_instigator_cooldown_id: gameDelayID = field(default_factory=gameDelayID)
	is_targeted_with_smart_weapon: bool = False


@dataclass
class BaseScriptableAction(gamedeviceAction):
	requester_id: entEntityID = field(default_factory=entEntityID)
	executor: gameObject = field(default_factory=gameObject)
	proxy_executor: gameObject = field(default_factory=gameObject)
	cost_components: list[gamedataObjectActionCost_Record] = field(default_factory=list)
	object_action_id: int = 0
	object_action_record: gamedataObjectAction_Record = field(default_factory=gamedataObjectAction_Record)
	ink_widget_id: int = 0
	interaction_choice: gameinteractionsChoice = field(default_factory=gameinteractionsChoice)
	interaction_layer: str = ''
	is_action_rpgcheck_dissabled: bool = False
	can_skip_pay_cost: bool = False
	calculated_base_cost: int = 0
	device_action_queue: DeviceActionQueue = field(default_factory=DeviceActionQueue)
	is_action_queueing_used: bool = False
	is_queued_action: bool = False
	is_inactive: bool = False
	is_target_dead: bool = False
	activation_time_reduction: float = 0.0
	is_applied_by_monowire: bool = False


@dataclass
class ScriptableDeviceAction(BaseScriptableAction):
	prop: gamedeviceActionProperty = field(default_factory=gamedeviceActionProperty)
	action_widget_package: SActionWidgetPackage = field(default_factory=SActionWidgetPackage)
	spiderbot_action_location_override: str = ''
	duration: float = 0.0
	can_trigger_stim: bool = False
	was_performed_on_owner: bool = False
	should_activate_device: bool = False
	disable_spread: bool = False
	is_quick_hack: bool = False
	is_spiderbot_action: bool = False
	attached_program: int = 0
	active_status_effect: int = 0
	interaction_icon_type: int = 0
	has_interaction: bool = False
	inactive_reason: str = ''
	widget_style: enums.gamedataComputerUIStyle = enums.gamedataComputerUIStyle.DarkBlue


@dataclass
class gameprojectileSetUpEvent(Chunk):
	owner: gameObject = field(default_factory=gameObject)
	weapon: gameObject = field(default_factory=gameObject)
	trajectory_params: gameprojectileTrajectoryParams = field(default_factory=gameprojectileTrajectoryParams)
	lerp_multiplier: float = 5.00


@dataclass
class gameprojectileShootEvent(gameprojectileSetUpEvent):
	local_to_world: CMatrix = field(default_factory=CMatrix)
	start_point: tuple[float, float, float, float] = (sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize)
	start_velocity: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	weapon_velocity: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	params: gameprojectileWeaponParams = field(default_factory=gameprojectileWeaponParams)


@dataclass
class gameprojectileShootTargetEvent(gameprojectileShootEvent):
	pass


@dataclass
class gameDebugFreeCamera(gameObject):
	pass


@dataclass
class gameEffectDebugSettings(Chunk):
	override_global_settings: bool = False
	duration: float = 1.0
	color: CColor = field(default_factory=CColor)


@dataclass
class gameEffectSettings(Chunk):
	advanced_target_handling: bool = False
	synchronous_processing_for_player: bool = False
	force_synchronous_processing: bool = False
	temp_execute_only_once: bool = False
	tick_rate: float = 0.0
	use_sim_time_for_tick: bool = False


@dataclass
class gameEffectDefinition(Chunk):
	tag: str = ''
	object_providers: list[gameEffectObjectProvider] = field(default_factory=list)
	object_filters: list[gameEffectObjectFilter] = field(default_factory=list)
	effect_executors: list[gameEffectExecutor] = field(default_factory=list)
	duration_modifiers: list[gameEffectDurationModifier] = field(default_factory=list)
	pre_actions: list[gameEffectPreAction] = field(default_factory=list)
	post_actions: list[gameEffectPostAction] = field(default_factory=list)
	no_targets_actions: list[gameEffectAction] = field(default_factory=list)
	settings: gameEffectSettings = field(default_factory=gameEffectSettings)
	debug_settings: gameEffectDebugSettings = field(default_factory=gameEffectDebugSettings)


@dataclass
class gameEffectSet(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	effects: list[gameEffectDefinition] = field(default_factory=list)


class gameScriptStatsListener(gameIStatsListener):
	pass


@dataclass
class UpdateOverheatEvent(Chunk):
	value: float = 0.0


@dataclass
class gameScriptStatPoolsListener(gameIStatPoolsListener):
	pass


@dataclass
class gameCustomValueStatPoolsListener(gameScriptStatPoolsListener):
	pass


@dataclass
class SHitFlag(Chunk):
	flag: enums.hitFlag = enums.hitFlag._None
	source: str = ''


@dataclass
class SHitStatusEffect(Chunk):
	stacks: float = 0.0
	id: int = 0


@dataclass
class gameHitResult(Chunk):
	hit_position_enter: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
	hit_position_exit: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
	enter_distance_from_origin_sq: float = 0.0


@dataclass
class gameShapeData(Chunk):
	result: gameHitResult = field(default_factory=gameHitResult)
	user_data: gameHitShapeUserData = field(default_factory=gameHitShapeUserData)
	physics_material: str = ''
	hit_shape_name: str = ''


@dataclass
class gameQueryResult(Chunk):
	hit_shapes: list[gameShapeData] = field(default_factory=list)


@dataclass
class gameLootContainerBase(gameObject):
	use_area_loot: bool = True
	loot_tables: list[int] = field(default_factory=list)
	content_assignment: int = 0
	is_illegal: bool = False
	was_loot_initalized: bool = False
	container_type: enums.gamedataContainerType = enums.gamedataContainerType.AmmoCase
	loot_quality: enums.gamedataQuality = enums.gamedataQuality.Common
	has_quest_items: bool = False
	is_in_icon_forced_visibility_range: bool = False
	is_iconic: bool = False
	active_quality_range_interaction: str = ''


@dataclass
class gameLootSlot(gameLootContainerBase):

	immovable_after_drop: bool = False
	drop_chance: float = 1.0
	loot_state: enums.gameLootSlotState = enums.gameLootSlotState.Looted  # TODO: CBitField


@dataclass
class gameLootSlotSingleItem(gameLootSlot):
	# TODO: use_area_loot = False
	item_tdbid: int = 0


@dataclass
class gameLootSlotSingleItemLongStreaming(gameLootSlotSingleItem):
	pass


@dataclass
class gamePhotoModeCameraObject(gameObject):
	pass


@dataclass
class gamePhotomodeLightObject(gameObject):
	pass


@dataclass
class gameTimeDilatable(gameObject):
	pass


@dataclass
class gameItemObject(gameTimeDilatable):
	update_bucket: enums.UpdateBucketEnum = enums.UpdateBucketEnum.AttachedObject
	loot_quality: enums.gamedataQuality = enums.gamedataQuality.Common
	is_iconic: bool = False
	is_broken: bool = False


@dataclass
class gameweaponObject(gameItemObject):
	effect: gameEffectSet = field(default_factory=gameEffectSet)  # TODO: CResourceReference
	has_overheat: bool = False
	overheat_effect_blackboard: worldEffectBlackboard = field(default_factory=worldEffectBlackboard)
	overheat_listener: "OverheatStatListener" = field(
			default_factory=lambda: OverheatStatListener()
			)  # TODO: resolve default class (circular import)
	overheat_delay_sent: bool = False
	charge_effect_blackboard: worldEffectBlackboard = field(default_factory=worldEffectBlackboard)
	charge_stat_listener: "WeaponChargeStatListener" = field(
			default_factory=lambda: WeaponChargeStatListener()
			)  # TODO: resolve default class (circular import)
	trigger_effect_name: str = ''
	melee_hit_effect_blackboard: worldEffectBlackboard = field(default_factory=worldEffectBlackboard)
	melee_hit_effect_value: float = 0.0
	damage_type_listener: "DamageStatListener" = field(
			default_factory=lambda: DamageStatListener()
			)  # TODO: resolve default class (circular import)
	trail_name: str = ''
	max_charge_threshold: float = 100.0
	anim_owner: int = 0
	perfect_charge_started: bool = False
	perfect_charge_reached: bool = False
	perfect_charge_shot: bool = False
	low_ammo_effect_active: bool = False
	has_secondary_trigger_mode: bool = False
	weapon_record: gamedataWeaponItem_Record = field(default_factory=gamedataWeaponItem_Record)
	is_heavy_weapon: bool = False
	is_melee_weapon: bool = False
	is_ranged_weapon: bool = False
	is_shotgun_weapon: bool = False
	aiblackboard: gameIBlackboard = field(default_factory=gameIBlackboard)
	is_charged: bool = False


@dataclass
class gamedamageAttackData(Chunk):
	attack_type: enums.gamedataAttackType = enums.gamedataAttackType.ChargedWhipAttack
	instigator: gameObject = field(default_factory=gameObject)
	source: gameObject = field(default_factory=gameObject)
	weapon: gameweaponObject = field(default_factory=gameweaponObject)
	attack_definition: gameIAttack = field(default_factory=gameIAttack)
	attack_position: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	weapon_charge: float = 0.0
	num_ricochet_bounces: int = 0
	num_attack_spread: int = 0
	attack_time: float = 0.0
	trigger_mode: enums.gamedataTriggerMode = enums.gamedataTriggerMode.Burst
	flags: list[SHitFlag] = field(default_factory=list)
	status_effects: list[SHitStatusEffect] = field(default_factory=list)
	hit_type: enums.gameuiHitType = enums.gameuiHitType.Miss
	vehicle_impact_force: float = 0.0
	minimum_health_percent: float = 0.0
	additional_crit_chance: float = 0.0
	rand_roll: float = 0.0
	hit_reaction_min: int = 0
	hit_reaction_max: int = 0


@dataclass
class gameeventsHitEvent(Chunk):
	attack_data: gamedamageAttackData = field(default_factory=gamedamageAttackData)
	target: gameObject = field(default_factory=gameObject)
	hit_position: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
	hit_direction: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
	hit_component: entIPlacedComponent = field(default_factory=entIPlacedComponent)
	hit_collider_tag: str = ''
	hit_representation_result: gameQueryResult = field(default_factory=gameQueryResult)
	attack_pentration: float = 0.0
	has_pierced_tech_surface: bool = False
	attack_computed: gameAttackComputed = field(default_factory=gameAttackComputed)
	projection_pipeline: bool = False


@dataclass
class gameeventsProjectedHitEvent(gameeventsHitEvent):
	pass


@dataclass
class gameeventsTargetHitEvent(gameeventsHitEvent):
	pass


@dataclass
class OverheatStatListener(gameScriptStatPoolsListener):
	weapon: gameweaponObject = field(default_factory=gameweaponObject)
	update_evt: UpdateOverheatEvent = field(default_factory=UpdateOverheatEvent)
	start_evt: StartOverheatEffectEvent = field(default_factory=StartOverheatEffectEvent)


@dataclass
class WeaponChargeStatListener(gameCustomValueStatPoolsListener):
	weapon: gameweaponObject = field(default_factory=gameweaponObject)


@dataclass
class DamageStatListener(gameScriptStatsListener):
	weapon: gameweaponObject = field(default_factory=gameweaponObject)
	update_evt: UpdateDamageChangeEvent = field(default_factory=UpdateDamageChangeEvent)


@dataclass
class gamePuppetBase(gameTimeDilatable):
	pass


@dataclass
class gamePuppet(gamePuppetBase):
	pass


@dataclass
class gameGarmentItemObject(gameItemObject):
	pass


@dataclass
class gameRemains(gameObject):
	pass


@dataclass
class gamePlayerScriptableSystemRequest(gameScriptableSystemRequest):
	owner: gameObject = field(default_factory=gameObject)


@dataclass
class gamePlayerAttachRequest(gamePlayerScriptableSystemRequest):
	pass


@dataclass
class gameComponentPS(gamePersistentState):
	pass


@dataclass
class GemplayObjectiveData(Chunk):
	quest_unique_id: str = ''
	quest_title: str = ''
	objective_description: str = ''
	unique_id: str = ''
	owner_id: entEntityID = field(default_factory=entEntityID)
	objective_entry_id: str = ''
	unique_id_prefix: str = ''
	objective_state: enums.gameJournalEntryState = enums.gameJournalEntryState.Undefined


@dataclass
class BackDoorObjectiveData(GemplayObjectiveData):
	pass
	# TODO: quest_unique_id = "NETWORK";
	# TODO: quest_title = "NETWORK";
	# TODO: objective_description = "Hack backdoor in order to get access to the network";
	# TODO: unique_id_prefix = "backdoor";


@dataclass
class ControlPanelObjectiveData(GemplayObjectiveData):
	pass
	# TODO: quest_unique_id = "TECHNICAL_GRID";
	# TODO: quest_title = "TECHNICAL GRID";
	# TODO: objective_description = "Gain access to control panel in order to manipulate devices";
	# TODO: unique_id_prefix = "controlPanel";


@dataclass
class gameDeviceComponentPS(gameComponentPS):
	# TODO: device_ui_style = Enums.gamedataComputerUIStyle.LightBlue;
	mark_as_quest: bool = False
	auto_toggle_quest_mark: bool = True
	fact_to_disable_quest_mark: str = ''
	callback_to_disable_quest_mark_id: int = 0
	backdoor_objective_data: BackDoorObjectiveData = field(default_factory=BackDoorObjectiveData)
	control_panel_objective_data: ControlPanelObjectiveData = field(default_factory=ControlPanelObjectiveData)
	device_uistyle: enums.gamedataComputerUIStyle = enums.gamedataComputerUIStyle.DarkBlue
	blackboard: gameIBlackboard = field(default_factory=gameIBlackboard)
	is_scanned: bool = False
	is_being_scanned: bool = False
	expose_quick_hacks: bool = False
	is_attached_to_game: bool = False
	is_logic_ready: bool = False
	max_devices_to_extract_in_one_frame: int = 10


@dataclass
class GameplayConditionBase(Chunk):
	entity_id: entEntityID = field(default_factory=entEntityID)


@dataclass
class ConditionGroupData(Chunk):
	conditions: list[GameplayConditionBase] = field(default_factory=list)
	logic_operator: enums.ELogicOperator = enums.ELogicOperator.OR


@dataclass
class GameplayConditionContainer(Chunk):
	logic_operator: enums.ELogicOperator = enums.ELogicOperator.OR
	condition_groups: list[ConditionGroupData] = field(default_factory=list)


@dataclass
class GameplaySkillCondition(GameplayConditionBase):
	skill_to_check: int = 0
	difficulty: enums.EGameplayChallengeLevel = enums.EGameplayChallengeLevel.NONE
	skill_bonus: int = 0
	required_level: int = 0


@dataclass
class SkillCheckBase(Chunk):
	alternative_name: int = 0
	difficulty: enums.EGameplayChallengeLevel = enums.EGameplayChallengeLevel.NONE
	additional_requirements: GameplayConditionContainer = field(default_factory=GameplayConditionContainer)
	duration: float = 0.0
	is_active: bool = False
	was_passed: bool = False
	skill_check_performed: bool = False
	skill_to_check: enums.EDeviceChallengeSkill = enums.EDeviceChallengeSkill.Invalid
	base_skill: GameplaySkillCondition = field(default_factory=GameplaySkillCondition)
	is_dynamic: bool = False


@dataclass
class HackingSkillCheck(SkillCheckBase):
	# TODO: skill_to_check = Enums.EDeviceChallengeSkill.Hacking;
	pass


@dataclass
class EngineeringSkillCheck(SkillCheckBase):
	# TODO: skill_to_check = Enums.EDeviceChallengeSkill.Engineering;
	pass


@dataclass
class DemolitionSkillCheck(SkillCheckBase):
	# TODO: skill_to_check = Enums.EDeviceChallengeS
	pass


@dataclass
class BaseSkillCheckContainer(Chunk):
	hacking_check_slot: HackingSkillCheck = field(default_factory=HackingSkillCheck)
	engineering_check_slot: EngineeringSkillCheck = field(default_factory=EngineeringSkillCheck)
	demolition_check_slot: DemolitionSkillCheck = field(default_factory=DemolitionSkillCheck)
	is_initialized: bool = False


@dataclass
class SharedGameplayPS(gameDeviceComponentPS):
	device_state: enums.EDeviceStatus = enums.EDeviceStatus.OFF
	authorization_properties: AuthorizationData = field(default_factory=AuthorizationData)
	was_state_cached: bool = False
	was_state_set: bool = False
	cached_device_state: enums.EDeviceStatus = enums.EDeviceStatus.OFF
	reveal_devices_grid: bool = False
	reveal_devices_grid_when_unpowered: bool = False
	was_revealed_in_network_ping: bool = False
	has_network_backdoor: bool = False


@dataclass
class DestructionData(Chunk):
	durability_type: enums.EDeviceDurabilityType = enums.EDeviceDurabilityType.INVULNERABLE
	can_be_fixed: bool = False


@dataclass
class ScriptableDeviceComponentPS(SharedGameplayPS):
	# TODO: device_state = Enums.EDeviceStatus.ON;
	# TODO: reveal_devices_grid = true;
	# TODO: tweak_db_record = "Devices.GenericDevice";
	# TODO: backdoor_breach_difficulty = Enums.EGameplayChallengeLevel.EASY;
	# TODO: disassemble_properties = new DisassembleOptions();
	# TODO: flathead_scavenge_properties = new SpiderbotScavengeOptions();
	# TODO: destruction_properties = new DestructionData();
	# TODO: illegal_actions = new IllegalActionTypes { SkillChecks = true };
	is_initialized: bool = False
	force_resolve_state_on_attach: bool = False
	force_visibility_in_anim_system_on_logic_ready: bool = False
	masters: list[gameDeviceComponentPS] = field(default_factory=list)
	masters_cached: bool = False
	device_name: str = ''
	activation_state: enums.EActivationState = enums.EActivationState.NONE
	draw_grid_link: bool = False
	is_link_dynamic: bool = False
	full_depth: bool = True
	virtual_network_shape_id: int = 0
	tweak_dbrecord: int = 0
	tweak_dbdescription_record: int = 0
	content_scale: int = 0
	skill_check_container: BaseSkillCheckContainer = field(default_factory=BaseSkillCheckContainer)
	has_uicamera_zoom: bool = False
	allow_uicamera_zoom_dynamic_switch: bool = False
	has_full_screen_ui: bool = False
	has_authorization_module: bool = True
	has_personal_link_slot: bool = False
	backdoor_breach_difficulty: enums.EGameplayChallengeLevel = enums.EGameplayChallengeLevel.NONE
	should_skip_netrunner_minigame: bool = False
	minigame_definition: int = 0
	minigame_attempt: int = 1
	hacking_minigame_state: enums.gameuiHackingMinigameState = enums.gameuiHackingMinigameState.Unknown
	disable_personal_link_auto_disconnect: bool = False
	can_handle_advanced_interaction: bool = False
	can_be_trapped: bool = False
	disassemble_properties: DisassembleOptions = field(default_factory=DisassembleOptions)
	flathead_scavenge_properties: SpiderbotScavengeOptions = field(default_factory=SpiderbotScavengeOptions)
	destruction_properties: DestructionData = field(default_factory=DestructionData)
	can_player_take_over_control: bool = False
	can_be_in_device_chain: bool = False
	personal_link_forced: bool = False
	personal_link_custom_interaction: int = 0
	personal_link_status: enums.EPersonalLinkConnectionStatus = enums.EPersonalLinkConnectionStatus.NOT_CONNECTED
	is_advanced_interaction_mode_on: bool = False
	juryrig_trap_state: enums.EJuryrigTrapState = enums.EJuryrigTrapState.UNARMED
	is_controlled_by_the_player: bool = False
	is_highlighted_in_focus_mode: bool = False
	was_quick_hacked: bool = False
	was_quick_hack_attempt: bool = False
	last_performed_quick_hack: str = ''
	is_glitching: bool = False
	is_timed_turn_off: bool = False
	is_restarting: bool = False
	block_security_wake_up: bool = False
	is_locked_via_sequencer: bool = False
	distract_executed: bool = False
	distraction_time_completed: bool = False
	has_npcworkspot_kill_interaction: bool = False
	should_npcworkspot_finish_loop: bool = False
	durability_state: enums.EDeviceDurabilityState = enums.EDeviceDurabilityState.NOMINAL
	has_been_scavenged: bool = False
	currently_authorized_users: list[SecuritySystemClearanceEntry] = field(default_factory=list)
	performed_actions: list[SPerformedActions] = field(default_factory=list)
	is_initial_state_operation_performed: bool = False
	illegal_actions: IllegalActionTypes = field(default_factory=IllegalActionTypes)
	disable_quick_hacks: bool = False
	available_quick_hacks: list[str] = field(default_factory=list)
	is_keylogger_installed: bool = False
	actions_with_disabled_rpgchecks: list[int] = field(default_factory=list)
	available_spiderbot_actions: list[str] = field(default_factory=list)
	current_spiderbot_action_performed: ScriptableDeviceAction = field(default_factory=ScriptableDeviceAction)
	is_spiderbot_interaction_ordered: bool = False
	should_scanner_show_status: bool = True
	should_scanner_show_network: bool = True
	should_scanner_show_attitude: bool = False
	should_scanner_show_role: bool = False
	should_scanner_show_health: bool = False
	debug_device: bool = False
	debug_name: str = ''
	debug_expose_quick_hacks: bool = False
	debug_path: str = ''
	debug_id: int = 0
	is_under_empeffect: bool = False
	device_operations_setup: DeviceOperationsContainer = field(default_factory=DeviceOperationsContainer)
	connection_highlight_objects: list[str] = field(default_factory=list)
	active_contexts: list[enums.gamedeviceRequestType] = field(default_factory=list)
	playstyles: list[enums.EPlaystyle] = field(default_factory=list)
	quick_hack_vulnerabilties: list[int] = field(default_factory=list)
	quick_hack_vulnerabilties_initialized: bool = False
	willing_investigators: list[entEntityID] = field(default_factory=list)
	is_interactive: bool = True


@dataclass
class ElectricLightControllerPS(ScriptableDeviceComponentPS):
	# TODO: device_name = "LocKey#42165";
	# TODO: tweak_db_record = "Devices.ElectricLight";
	# TODO: tweak_db_description_record = 142476847136;
	is_connected_to_cls: bool = False
	was_clsinit_triggered: bool = False


#


@dataclass
class GameplayLightControllerPS(ElectricLightControllerPS):
	pass


@dataclass
class gameSceneTierData(Chunk):
	tier: enums.GameplayTier = enums.GameplayTier.Undefined
	empty_hands: bool = False
	user_debug_info: str = ''


@dataclass
class gameScriptableComponent(gameComponent):
	priority: int = 0


@dataclass
class gameHitShapeContainer(Chunk):
	name: str = ''
	slot_name: str = ''
	color: CColor = field(default_factory=CColor)
	shape: "gameIHitShape" = field(
			default_factory=lambda: gameIHitShape()
			)  # TODO: resolve default class (circular import)
	user_data: "gameHitShapeUserData" = field(
			default_factory=lambda: gameHitShapeUserData()
			)  # TODO: resolve default class (circular import)
	physics_material: "physicsMaterialReference" = field(
			default_factory=lambda: physicsMaterialReference()
			)  # TODO: resolve default class (circular import)


@dataclass
class gameHitRepresentationOverride(Chunk):
	represenation_override: gameHitShapeContainer = field(default_factory=gameHitShapeContainer)
