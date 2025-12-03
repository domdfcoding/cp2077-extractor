#!/usr/bin/env python3
#
#  ent.py
"""
Classes to represent datatypes within CR2W/W2RC files (prefixed ``ent``).
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
from cp2077_extractor.cr2w.datatypes.appearance import appearanceAppearanceResource
from cp2077_extractor.cr2w.datatypes.base import CColor, Chunk, Plane, Quaternion, Transform, redTagList
from cp2077_extractor.cr2w.datatypes.mesh import CMesh
from cp2077_extractor.cr2w.datatypes.rend import rendSLightFlickering

if TYPE_CHECKING:
	# this package
	from cp2077_extractor.cr2w.datatypes.world import WorldTransform, worldEffect

__all__ = [
		"CIESDataResource",
		"entBaseCameraComponent",
		"entEntity",
		"entEntityID",
		"entEntityParametersBuffer",
		"entEntityTemplate",
		"entFallbackSlot",
		"entGameEntity",
		"entIAttachment",
		"entIBinding",
		"entIComponent",
		"entIPlacedComponent",
		"entIPositionProvider",
		"entISourceBinding",
		"entITransformBinding",
		"entIVisualComponent",
		"entLightComponent",
		"entSlot",
		"entSlotComponent",
		"entTagMask",
		"entTemplateAppearance",
		"entTemplateBindingOverride",
		"entTemplateComponentBackendDataOverrideInfo",
		"entTemplateComponentResolveSettings",
		"entTemplateInclude",
		"entVisualTagsSchema",
		"entVoicesetInputToBlock",
		"entdismembermentAppearanceMatch",
		"entdismembermentCullObject",
		"entdismembermentDangleInfo",
		"entdismembermentEffectResource",
		"entdismembermentFillMeshInfo",
		"entdismembermentMeshInfo",
		"entdismembermentPhysicsInfo",
		"entdismembermentWoundConfig",
		"entdismembermentWoundConfigContainer",
		"entdismembermentWoundDecal",
		"entdismembermentWoundMeshes",
		"entdismembermentWoundResource",
		"entdismembermentWoundsConfigSet",
		]


@dataclass
class entVisualTagsSchema(Chunk):
	visual_tags: redTagList = field(default_factory=redTagList)
	schema: str = ''


@dataclass
class entTemplateComponentResolveSettings(Chunk):
	component_name: str = ''
	name_param: str = ''
	mode: enums.entTemplateComponentResolveMode = enums.entTemplateComponentResolveMode.AutoSelect


@dataclass
class entTagMask(Chunk):
	hard_tags: redTagList = field(default_factory=redTagList)
	soft_tags: redTagList = field(default_factory=redTagList)
	excluded_tags: redTagList = field(default_factory=redTagList)


@dataclass
class entdismembermentCullObject(Chunk):
	plane: Plane = field(default_factory=lambda: Plane(normal_distance=(0.0, 0.0, 1.0, -0.0)))
	plane1: Plane = field(default_factory=lambda: Plane(normal_distance=(0.0, 0.0, 1.0, -0.0)))
	capsule_point_a: tuple[float, float, float] = (0.0, 0.0, 0.0)
	capsule_point_b: tuple[float, float, float] = (0.0, 0.0, 0.0)
	capsule_radius: float = 0.1
	nearest_anim_bone_name: str = ''
	nearest_anim_index: int = -1
	ragdoll_body_index: int = sys.maxsize


@dataclass
class entdismembermentAppearanceMatch(Chunk):
	character: str = ''
	mesh: str = ''
	set_by_user: bool = False


@dataclass
class entdismembermentPhysicsInfo(Chunk):
	density_scale: float = 1.0


@dataclass
class entdismembermentMeshInfo(Chunk):
	mesh: CMesh = field(default_factory=CMesh)  # TODO: CResourceAsyncReference
	mesh_appearance: str = "default"
	appearance_map: list[entdismembermentAppearanceMatch] = field(default_factory=list)
	should_receive_decal: bool = False
	body_part_mask: enums.physicsRagdollBodyPartE = enums.physicsRagdollBodyPartE.HEAD  # TODO: CBitField
	wound_type: enums.entdismembermentWoundTypeE = enums.entdismembermentWoundTypeE.CLEAN | enums.entdismembermentWoundTypeE.COARSE  # TODO: CBitField
	cull_mesh: enums.entdismembermentWoundTypeE = enums.entdismembermentWoundTypeE.CLEAN  # TODO: CBitField
	offset: Transform = field(default_factory=Transform)
	scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
	physics: entdismembermentPhysicsInfo = field(default_factory=entdismembermentPhysicsInfo)


@dataclass
class entdismembermentDangleInfo(Chunk):
	dangle_segment_lenght: float = 0.1
	dangle_velocity_damping: float = 0.4
	dangle_bend_stiffness: float = 0.6
	dangle_segment_stiffness: float = 0.0
	dangle_collision_sphere_radius: float = 0.25


@dataclass
class entdismembermentFillMeshInfo(entdismembermentMeshInfo):
	placement: enums.entdismembermentPlacementE = enums.entdismembermentPlacementE.MAIN_MESH  # TODO: CBitField
	simulation: enums.entdismembermentSimulationTypeE = enums.entdismembermentSimulationTypeE.NONE
	dangle: entdismembermentDangleInfo = field(default_factory=entdismembermentDangleInfo)


@dataclass
class entdismembermentWoundMeshes(Chunk):
	resource_set: enums.entdismembermentResourceSetE = enums.entdismembermentResourceSetE.NONE
	meshes: list[entdismembermentMeshInfo] = field(default_factory=list)
	fill_meshes: list[entdismembermentFillMeshInfo] = field(default_factory=list)


@dataclass
class entdismembermentWoundDecal(Chunk):
	offset_a: tuple[float, float, float] = (0.0, 0.0, 0.0)
	offset_b: tuple[float, float, float] = (0.0, 0.0, 0.0)
	scale: float = 1.0
	fade_origin: float = 0.7
	fade_power: float = 1.0
	resource_sets: enums.entdismembermentResourceSetMask = enums.entdismembermentResourceSetMask.BARE  # TODO: CBitField
	material: Any = None  # TODO: CResourceAsyncReference<IMaterial> = field(default_factory=CResourceAsyncReference<IMaterial>)


@dataclass
class entdismembermentWoundResource(Chunk):
	name: str = ''
	wound_type: enums.entdismembermentWoundTypeE = enums.entdismembermentWoundTypeE.CLEAN | enums.entdismembermentWoundTypeE.COARSE  # TODO: CBitField
	body_part: enums.physicsRagdollBodyPartE = enums.physicsRagdollBodyPartE.HEAD  # TODO: CBitField
	cull_object: entdismembermentCullObject = field(default_factory=entdismembermentCullObject)
	garment_morph_strength: float = 1.0
	use_procedural_cut: bool = False
	use_single_mesh_for_ragdoll: bool = False
	is_critical: bool = False
	resources: list[entdismembermentWoundMeshes] = field(default_factory=list)
	decals: list[entdismembermentWoundDecal] = field(default_factory=list)
	censored_paths: list[int] = field(default_factory=list)
	censored_cooked_paths: list[Chunk] = field(default_factory=list)  # TODO: CResourceAsyncReference
	censorship_valid: bool = False


@dataclass
class entdismembermentEffectResource(Chunk):
	name: str = ''
	appearance_names: list[str] = field(default_factory=list)
	body_part_mask: enums.physicsRagdollBodyPartE = enums.physicsRagdollBodyPartE.HEAD  # TODO: CBitField
	offset: Transform = field(default_factory=Transform)
	placement: enums.entdismembermentPlacementE = enums.entdismembermentPlacementE.MAIN_MESH  # TODO: CBitField
	resource_sets: enums.entdismembermentResourceSetMask = enums.entdismembermentResourceSetMask.BARE | enums.entdismembermentResourceSetMask.BARE1 | enums.entdismembermentResourceSetMask.BARE2 | enums.entdismembermentResourceSetMask.BARE3 | enums.entdismembermentResourceSetMask.GARMENT | enums.entdismembermentResourceSetMask.GARMENT1 | enums.entdismembermentResourceSetMask.GARMENT2 | enums.entdismembermentResourceSetMask.GARMENT3  # TODO: CBitField
	wound_type: enums.entdismembermentWoundTypeE = enums.entdismembermentWoundTypeE.COARSE  # TODO: CBitField
	effect: "worldEffect" = field(
			default_factory=lambda: worldEffect()
			)  # TODO: resolve default class (circular import)    # TODO: CResourceAsyncReference
	match_to_wound_by_name: bool = False


@dataclass
class entdismembermentWoundConfig(Chunk):
	wound_name: str = ''
	resource_set: enums.entdismembermentResourceSetE = enums.entdismembermentResourceSetE.BARE


@dataclass
class entdismembermentWoundConfigContainer(Chunk):
	appearance_name: str = ''
	wounds: list[entdismembermentWoundConfig] = field(default_factory=list)


@dataclass
class entdismembermentWoundsConfigSet(Chunk):
	configs: list[entdismembermentWoundConfigContainer] = field(default_factory=list)


@dataclass
class entIBinding(Chunk):
	enabled: bool = False
	enable_mask: entTagMask = field(default_factory=entTagMask)
	bind_name: str = ''


@dataclass
class entTemplateBindingOverride(Chunk):
	component_name: str = ''
	property_name: str = ''
	binding: entIBinding = field(default_factory=entIBinding)


@dataclass
class entTemplateComponentBackendDataOverrideInfo(Chunk):
	component_name: str
	offset: tuple[int, int]


@dataclass
class entEntityParametersBuffer(Chunk):
	parameter_buffers: list[Any] = field(default_factory=list)  # TODO: SerializationDeferredDataBuffer


@dataclass
class entEntityTemplate(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	includes: list["entTemplateInclude"] = field(default_factory=list)
	appearances: list["entTemplateAppearance"] = field(default_factory=list)
	default_appearance: str = "default"
	visual_tags_schema: entVisualTagsSchema = field(default_factory=entVisualTagsSchema)
	component_resolve_settings: list[entTemplateComponentResolveSettings] = field(default_factory=list)
	binding_overrides: list[entTemplateBindingOverride] = field(default_factory=list)
	backend_data_overrides: list[entTemplateComponentBackendDataOverrideInfo] = field(default_factory=list)
	local_data: Any = None  # TODO: DataBuffer = field(default_factory=DataBuffer)
	include_instance_buffer: Any = None  # TODO: DataBuffer = field(default_factory=DataBuffer)
	compiled_data: Any = None  # TODO: DataBuffer = field(default_factory=DataBuffer)
	resolved_dependencies: list[Chunk] = field(default_factory=list)  # TODO: CResourceAsyncReference
	inplace_resources: list[Chunk] = field(default_factory=list)  # TODO: CResourceReference
	compiled_entity_lodflags: int = 0


@dataclass
class entTemplateAppearance(Chunk):
	name: str = ''
	appearance_resource: appearanceAppearanceResource = field(
			default_factory=appearanceAppearanceResource
			)  # TODO: CResourceAsyncReference
	appearance_name: str = ''


@dataclass
class entTemplateInclude(Chunk):
	name: str = ''
	template: entEntityTemplate = field(default_factory=entEntityTemplate)  # TODO: CResourceAsyncReference


@dataclass
class entEntity(Chunk):
	custom_camera_target: enums.ECustomCameraTarget = enums.ECustomCameraTarget.ECCTV_All
	render_scene_layer_mask: enums.RenderSceneLayerMask = enums.RenderSceneLayerMask.Default  # CBitField


@dataclass
class entGameEntity(entEntity):
	pass


@dataclass
class entIComponent(Chunk):
	name: str = ''
	is_replicable: bool = False
	id: int = 0


@dataclass
class entISourceBinding(entIBinding):
	pass


@dataclass
class entITransformBinding(entISourceBinding):
	pass


@dataclass
class entIPlacedComponent(entIComponent):
	local_transform: "WorldTransform" = field(
			default_factory=lambda: WorldTransform()
			)  # TODO: resolve default class (circular import)
	parent_transform: entITransformBinding = field(default_factory=entITransformBinding)


@dataclass
class entSlot(Chunk):
	slot_name: str = ''
	relative_position: tuple[float, float, float] = (0.0, 0.0, 0.0)
	relative_rotation: Quaternion = field(default_factory=Quaternion)
	bone_name: str = ''


@dataclass
class entFallbackSlot(Chunk):
	slot_name: str = ''
	bone_name: str = ''


@dataclass
class entSlotComponent(entIPlacedComponent):
	# TODO: name = "Component";
	# TODO: local_transform = new WorldTransform { Position = new WorldPosition { X = new FixedPoint(), Y = new FixedPoint(), Z = new FixedPoint() }, Orientation = new Quaternion { R = 1.000000F } };
	slots: list[entSlot] = field(default_factory=list)
	fallback_slots: list[entFallbackSlot] = field(default_factory=list)


@dataclass
class entVoicesetInputToBlock(Chunk):
	input: str = ''
	block_specific_variation: bool = False
	variation_number: int = 0


@dataclass
class entIPositionProvider(Chunk):
	pass


@dataclass
class entIVisualComponent(entIPlacedComponent):
	auto_hide_distance: float = 0.0
	render_scene_layer_mask: enums.RenderSceneLayerMask = enums.RenderSceneLayerMask.Default  # TODO: CBitField
	force_lodlevel: int = 0


@dataclass
class CIESDataResource(Chunk):
	cooking_platform: enums.ECookingPlatform = enums.ECookingPlatform.PLATFORM_None
	samples: list[int] = field(default_factory=list)  # new(128)


@dataclass
class entLightComponent(entIVisualComponent):
	# TODO: name = "Component";
	# TODO: local_transform = new WorldTransform { Position = new WorldPosition { X = new FixedPoint(), Y = new FixedPoint(), Z = new FixedPoint() }, Orientation = new Quaternion { R = 1.000000F } };
	# TODO: auto_hide_distance = 15.00
	# TODO: render_scene_layer_mask = Enums.RenderSceneLayerMask.Default;
	# TODO: force_lod_level = -1;
	# TODO: light_channel = Enums.rendLightChannel.LC_Channel1 | Enums.rendLightChannel.LC_Channel2 | Enums.rendLightChannel.LC_Channel3 | Enums.rendLightChannel.LC_Channel4 | Enums.rendLightChannel.LC_Channel5 | Enums.rendLightChannel.LC_Channel6 | Enums.rendLightChannel.LC_Channel7 | Enums.rendLightChannel.LC_Channel8 | Enums.rendLightChannel.LC_ChannelWorld;
	type: enums.ELightType = enums.ELightType.LT_Point
	color: CColor = field(default_factory=CColor)
	radius: float = 5.0
	unit: enums.ELightUnit = enums.ELightUnit.LU_Lumen
	intensity: float = 100.0
	ev: float = 0.0
	temperature: float = -1.0
	light_channel: enums.rendLightChannel = enums.rendLightChannel.LC_Channel1  # TODO: CBitField
	scene_diffuse: bool = True
	scene_specular_scale: int = 100
	directional: bool = False
	roughness_bias: int = 0
	scale_gi: int = 100
	scale_env_probes: int = 100
	use_in_transparents: bool = True
	scale_vol_fog: int = 0
	use_in_particles: bool = True
	attenuation: enums.rendLightAttenuation = enums.rendLightAttenuation.LA_InverseSquare
	clamp_attenuation: bool = False
	group: enums.rendLightGroup = enums.rendLightGroup.LG_Group0
	area_shape: enums.EAreaLightShape = enums.EAreaLightShape.ALS_Capsule
	area_two_sided: bool = True
	spot_capsule: bool = False
	source_radius: float = 0.05
	capsule_length: float = 1.0
	area_rect_side_a: float = 1.0
	area_rect_side_b: float = 1.0
	inner_angle: float = 30.0
	outer_angle: float = 45.0
	softness: float = 2.0
	enable_local_shadows: bool = False
	enable_local_shadows_force_statics_only: bool = False
	contact_shadows: enums.rendContactShadowReciever = enums.rendContactShadowReciever.CSR_None
	shadow_angle: float = -10.0
	shadow_radius: float = -10.0
	shadow_fade_distance: float = 10.0
	shadow_fade_range: float = 5.0
	shadow_softness_mode: enums.ELightShadowSoftnessMode = enums.ELightShadowSoftnessMode.LSSM_Default
	ray_traced_shadows_platform: enums.rendRayTracedShadowsPlatform = enums.rendRayTracedShadowsPlatform.RLSP_All
	ray_tracing_light_source_radius: float = -1.0
	ray_tracing_contact_shadow_range: float = -1.0
	ies_profile: CIESDataResource = field(default_factory=CIESDataResource)  # TODO: CResourceAsyncReference
	flicker: rendSLightFlickering = field(default_factory=rendSLightFlickering)
	env_color_group: enums.EEnvColorGroup = enums.EEnvColorGroup.ECG_Default
	color_group_saturation: int = 100
	portal_angle_cutoff: int = 0
	allow_distant_light: bool = True
	ray_tracing_intensity_scale: float = 1.0
	path_tracing_light_usage: enums.rendEPathTracingLightUsage = enums.rendEPathTracingLightUsage.PTLU_Everywhere
	path_tracing_override_scale_gi: bool = True
	rtxdi_shadow_starting_distance: float = -1.0
	is_enabled: bool = True


@dataclass
class entEntityID(Chunk):
	hash: int = 0


@dataclass
class entIAttachment(Chunk):
	source: entIComponent = field(default_factory=entIComponent)
	destination: entIComponent = field(default_factory=entIComponent)


@dataclass
class entBaseCameraComponent(entIPlacedComponent):
	# TODO: name = "Component";
	# TODO: local_transform = new WorldTransform { Position = new WorldPosition { X = new FixedPoint(), Y = new FixedPoint(), Z = new FixedPoint() }, Orientation = new Quaternion { R = 1.000000F } };
	fov: float = 60.0
	zoom: float = 1.0
	near_plane_override: float = 0.0
	far_plane_override: float = 0.0
	motion_blur_scale: float = 1.0
