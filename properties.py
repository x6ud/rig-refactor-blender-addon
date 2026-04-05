import bpy


class RigRefactorProperties(bpy.types.PropertyGroup):
    auto_connect_bones_selected_only: bpy.props.BoolProperty(default=False)

    correct_bone_length_selected_only: bpy.props.BoolProperty(default=False)
    correct_bone_length_limit_max: bpy.props.BoolProperty(default=False)
    correct_bone_length_limit_min: bpy.props.BoolProperty(default=True)
    correct_bone_length_max: bpy.props.FloatProperty(name="Max Bone Length", min=0, default=30)
    correct_bone_length_min: bpy.props.FloatProperty(name="Min Bone Length", min=0, default=0.05)
    correct_bone_length_min_to_avg: bpy.props.BoolProperty(default=True)

    rename_bones_number_prefix: bpy.props.StringProperty(name="Suffix Separator", default="_")

    rename_bones_mirror_mode: bpy.props.EnumProperty(
        items=[("any_match", "any match", "any match"),
               ("start_with", "starts with", "starts with"),
               ("end_with", "ends with", "ends with")
               ],
        default="any_match"
    )
    rename_bones_search_lf: bpy.props.StringProperty(default="_L_")
    rename_bones_search_rt: bpy.props.StringProperty(default="_R_")
    rename_bones_lf_suffix: bpy.props.StringProperty(default="_L")
    rename_bones_rt_suffix: bpy.props.StringProperty(default="_R")