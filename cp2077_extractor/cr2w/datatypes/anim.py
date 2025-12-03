#!/usr/bin/env python3
#
#  anim.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``anim``).
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
from typing import TYPE_CHECKING, Any

# this package
from cp2077_extractor.cr2w import enums
from cp2077_extractor.cr2w.datatypes.base import Chunk, QsTransform, Quaternion

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.datatypes.physics import physicsRagdollBodyInfo, physicsRagdollBodyNames

__all__ = [
		"animAdditionalFloatTrackContainer",
		"animAdditionalFloatTrackEntry",
		"animAdditionalTransformContainer",
		"animAdditionalTransformEntry",
		"animAnimDataChunk",
		"animAnimEvent",
		"animAnimFallbackFrameDesc",
		"animAnimFeature",
		"animAnimSet",
		"animAnimSetEntry",
		"animAnimSetup",
		"animAnimSetupEntry",
		"animAnimation",
		"animBoneCorrection",
		"animCompareBone",
		"animEventsContainer",
		"animFacialEmotionTransitionBaked",
		"animFloatTrackInfo",
		"animIAnimationBuffer",
		"animIKTargetRequest",
		"animIMotionExtraction",
		"animIRigIkSetup",
		"animLookAtLimits",
		"animLookAtPartRequest",
		"animLookAtRequest",
		"animLookAtRequestForPart",
		"animPoseCorrection",
		"animPoseCorrectionGroup",
		"animRig",
		"animRigPart",
		"animRigPartBone",
		"animRigPartBoneTree",
		"animRigRetarget",
		"animTransformInfo",
		"animTransformMask",
		]


class animIAnimationBuffer(Chunk):
	pass


@dataclass
class animTransformInfo(Chunk):
	name: str = ''
	parent_name: str = ''
	reference_transform_ls: QsTransform = field(
			default_factory=lambda: QsTransform(translation=(0.0, 0.0, 0.0, 1.0))
			)


@dataclass
class animAdditionalTransformEntry(Chunk):
	transform_info: animTransformInfo = field(default_factory=animTransformInfo)
	value: QsTransform = field(default_factory=QsTransform)


@dataclass
class animAdditionalTransformContainer(Chunk):
	entries: list[animAdditionalTransformEntry] = field(default_factory=list)


@dataclass
class animFloatTrackInfo(Chunk):
	name: str = ''
	reference_value: float = 0.0


@dataclass
class animAdditionalFloatTrackEntry(Chunk):
	name: str = ''
	track_info: animFloatTrackInfo = field(default_factory=animFloatTrackInfo)
	values: list[float] = field(default_factory=list)


@dataclass
class animAdditionalFloatTrackContainer(Chunk):
	entries: list[animAdditionalFloatTrackEntry] = field(default_factory=list)
	overwrite_existing_values: bool = True


class animIMotionExtraction(Chunk):
	pass


@dataclass
class animAnimation(Chunk):
	tags: list = field(default_factory=list)
	name: str = ''
	duration: float = 0.0
	animation_type: enums.animAnimationType = enums.animAnimationType.Normal
	anim_buffer: animIAnimationBuffer = field(default_factory=animIAnimationBuffer)
	additional_transforms: animAdditionalTransformContainer = field(
			default_factory=animAdditionalTransformContainer
			)
	additional_tracks: animAdditionalFloatTrackContainer = field(default_factory=animAdditionalFloatTrackContainer)
	motion_extraction: animIMotionExtraction = field(default_factory=animIMotionExtraction)
	frame_clamping: bool = False
	frame_clamping_start_frame: int = -1
	frame_clamping_end_frame: int = -1


@dataclass
class animAnimEvent(Chunk):
	start_frame: int = 0
	duration_in_frames: int = 0
	event_name: str = ''


@dataclass
class animEventsContainer(Chunk):
	events: list[animAnimEvent] = field(default_factory=list)


@dataclass
class animAnimSetEntry(Chunk):
	animation: animAnimation = field(default_factory=animAnimation)
	events: animEventsContainer = field(default_factory=animEventsContainer)


@dataclass
class animAnimDataChunk(Chunk):
	buffer: bytes = b''


@dataclass
class animAnimFallbackFrameDesc(Chunk):
	mpositions: int = 0
	mrotations: int = 0
	mfloat_tracks: int = 0


@dataclass
class animRigPartBone(Chunk):
	bone: str = ''
	weight: float = 1.0


@dataclass
class animRigPartBoneTree(Chunk):
	root_bone: str = ''
	weight: float = 1.0
	subtrees_to_change: list["animRigPartBoneTree"] = field(default_factory=list)


@dataclass
class animTransformMask(Chunk):
	index: int = -1
	weight: float = 0.0


@dataclass
class animRigPart(Chunk):
	name: str = ''
	single_bones: list[animRigPartBone] = field(default_factory=list)
	tree_bones: list[animRigPartBoneTree] = field(default_factory=list)
	bones_with_rotation_in_model_space: list[str] = field(default_factory=list)
	mask: list[animTransformMask] = field(default_factory=list)
	mask_rot_ms: list[int] = field(default_factory=list)


@dataclass
class animIRigIkSetup(Chunk):
	name: str = ''


@dataclass
class animIKTargetRequest(Chunk):
	weight_position: float = 1.0
	weight_orientation: float = 1.0
	transition_in: float = 0.3
	transition_out: float = 0.3
	priority: int = 0


@dataclass
class animRig(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	bone_names: list[str] = field(default_factory=list)
	track_names: list[str] = field(default_factory=list)
	rig_extra_tracks: list[animFloatTrackInfo] = field(default_factory=list)
	level_of_detail_start_indices: list[int] = field(default_factory=list)
	distance_category_to_lod_map: list[int] = field(default_factory=list)
	turn_off_lod: int = -1
	turning_off_update_and_sample: bool = False
	reference_tracks: list[float] = field(default_factory=list)
	reference_pose_ms: list[QsTransform] = field(default_factory=list)
	apose_ls: list[QsTransform] = field(default_factory=list)
	apose_ms: list[QsTransform] = field(default_factory=list)
	tags: list = field(default_factory=list)
	parts: list[animRigPart] = field(default_factory=list)
	retargets: list["animRigRetarget"] = field(default_factory=list)
	ik_setups: list[animIRigIkSetup] = field(default_factory=list)
	ragdoll_desc: list["physicsRagdollBodyInfo"] = field(default_factory=list)
	ragdoll_names: list["physicsRagdollBodyNames"] = field(default_factory=list)


@dataclass
class animRigRetarget(Chunk):
	source_rig: animRig = field(default_factory=animRig)  # TODO: CResourceReference


@dataclass
class animAnimSet(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	animations: list[animAnimSetEntry] = field(default_factory=list)
	animation_data_chunks: list[animAnimDataChunk] = field(default_factory=list)
	fallback_data_addresses: list[int] = field(default_factory=list)
	fallback_data_address_indexes: list[int] = field(default_factory=list)
	fallback_anim_frame_descs: list[animAnimFallbackFrameDesc] = field(default_factory=list)
	fallback_anim_desc_indexes: list[int] = field(default_factory=list)
	fallback_anim_data_buffer: Any = None  # TODO: DataBuffer = field(default_factory=DataBuffer)
	fallback_num_position_data: int = 0
	fallback_num_rotation_data: int = 0
	fallback_num_float_track_data: int = 0
	rig: animRig = field(default_factory=animRig)  # TODO: CResourceReference
	tags: list = field(default_factory=list)
	version: int = 0


@dataclass
class animFacialEmotionTransitionBaked(Chunk):
	to_idle_male: str = ''
	facial_key_male: str = ''
	to_idle_female: str = ''
	facial_key_female: str = ''
	transition_type: enums.animFacialEmotionTransitionType = enums.animFacialEmotionTransitionType.Fast
	transition_duration: float = 0.0
	time_scale: float = 0.0
	to_idle_weight: float = 1.0
	to_idle_neck_weight: float = 0.0
	facial_key_weight: float = 0.0
	custom_transition_anim: str = ''


@dataclass
class animLookAtLimits(Chunk):
	soft_limit_degrees: float = 360.0
	hard_limit_degrees: float = 360.0
	hard_limit_distance: float = 1000000.0
	back_limit_degrees: float = 180.0


class animAnimFeature(Chunk):
	pass


@dataclass
class animLookAtPartRequest(Chunk):
	part_name: str = ''
	weight: float = 0.5
	suppress: float = 0.0
	mode: int = 0


@dataclass
class animLookAtRequest(Chunk):
	transition_speed: float = 60.0
	has_out_transition: bool = False
	out_transition_speed: float = 60.0
	following_speed_factor_override: float = -1.0
	limits: animLookAtLimits = field(default_factory=animLookAtLimits)
	suppress: float = 0.0
	mode: int = 0
	calculate_position_in_parent_space: bool = False
	priority: int = 0
	additional_parts: animLookAtPartRequest = field(default_factory=animLookAtPartRequest)
	invalid: bool = False


@dataclass
class animLookAtRequestForPart(Chunk):
	body_part: str = "Eyes"
	request: animLookAtRequest = field(default_factory=animLookAtRequest)
	attach_left_hand_to_right_hand: int = -1
	attach_right_hand_to_left_hand: int = -1


@dataclass
class animCompareBone(Chunk):
	bone_name: str = ''
	bone_rotation_ls: Quaternion = field(default_factory=Quaternion)


@dataclass
class animBoneCorrection(Chunk):
	bone_name: str = ''
	additive_correction: Quaternion = field(default_factory=Quaternion)


@dataclass
class animPoseCorrection(Chunk):
	rbf_coefficient: float = 3.5
	rbf_pow_value: float = 20.0
	compare_bones: animCompareBone = field(default_factory=animCompareBone)
	bone_corrections: animBoneCorrection = field(default_factory=animBoneCorrection)


@dataclass
class animPoseCorrectionGroup(Chunk):
	pose_corrections: animPoseCorrection = field(default_factory=animPoseCorrection)


@dataclass
class animAnimSetupEntry(Chunk):
	priority: int = 128
	anim_set: animAnimSet = field(default_factory=animAnimSet)  # TODO: CResourceAsyncReference
	variable_names: list[str] = field(default_factory=list)


@dataclass
class animAnimSetup(Chunk):
	cinematics: list[animAnimSetupEntry] = field(default_factory=list)
	gameplay: list[animAnimSetupEntry] = field(default_factory=list)
	hash: int = 0
