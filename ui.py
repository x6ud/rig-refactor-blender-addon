import textwrap

import bpy


class RigRefactorPanelMain(bpy.types.Panel):
    bl_label = "Rig Refactor"
    bl_idname = "RIG_REFACTOR_PT_MAIN"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig Refactor"

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def draw(self, context):
        return


class RigRefactorPanelAutoConnectBones(bpy.types.Panel):
    bl_label = "Automatically Connect Bones"
    bl_idname = "RIG_REFACTOR_PT_AUTO_CONNECT_BONES"

    bl_parent_id = "RIG_REFACTOR_PT_MAIN"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        properties = context.scene.rig_refactor_properties
        layout = self.layout

        layout.prop(properties, "auto_connect_bones_selected_only", text="Selected Bones Only")
        layout.operator("rig_refactor.auto_connect_bones")


class RigRefactorPaneCorrectBoneLength(bpy.types.Panel):
    bl_label = "Correct Length of Bones"
    bl_idname = "RIG_REFACTOR_PT_CORRECT_BONE_LENGTH"

    bl_parent_id = "RIG_REFACTOR_PT_MAIN"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        properties = context.scene.rig_refactor_properties
        layout = self.layout

        layout.prop(properties, "correct_bone_length_limit_max", text="Limit Maximum Length")
        if properties.correct_bone_length_limit_max:
            layout.prop(properties, "correct_bone_length_max")
        layout.prop(properties, "correct_bone_length_limit_min", text="Limit Minimum Length")
        if properties.correct_bone_length_limit_min:
            layout.prop(properties, "correct_bone_length_min")
        layout.prop(properties, "correct_bone_length_min_to_avg", text="Set Small Bones to Average Length")
        layout.prop(properties, "correct_bone_length_selected_only", text="Selected Bones Only")
        layout.operator("rig_refactor.correct_bone_length")


class RigRefactorPaneRenameBones(bpy.types.Panel):
    bl_label = "Rename Bones"
    bl_idname = "RIG_REFACTOR_PT_RENAME_BONES"

    bl_parent_id = "RIG_REFACTOR_PT_MAIN"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        properties = context.scene.rig_refactor_properties
        layout = self.layout

        split = layout.split(factor=0.65)
        split.label(text="Suffix Separator")
        split.prop(properties, "rename_bones_number_prefix", text="")

        region_width = context.region.width
        chars = int(region_width / 7.5)
        text = "Remove the numeric suffix from bone names like \"bone_name" + properties.rename_bones_number_prefix + "01\"."
        for line in textwrap.wrap(text, width=chars):
            layout.label(text=line)
        layout.operator("rig_refactor.rename_bones_remove_numeric_suffix")

        layout.separator()

        layout.label(text="Replace in bone names that")
        layout.prop(properties, "rename_bones_mirror_mode", text="")
        row = layout.row()
        row.prop(properties, "rename_bones_search_lf", text="")
        row.label(text="with suffix")
        row.prop(properties, "rename_bones_lf_suffix", text="")
        row = layout.row()
        row.prop(properties, "rename_bones_search_rt", text="")
        row.label(text="with suffix")
        row.prop(properties, "rename_bones_rt_suffix", text="")
        layout.operator("rig_refactor.rename_bones_mirror")


class RigRefactorPaneClearUnused(bpy.types.Panel):
    bl_label = "Clear Unused"
    bl_idname = "RIG_REFACTOR_PT_CLEAR_UNUSED"

    bl_parent_id = "RIG_REFACTOR_PT_MAIN"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        properties = context.scene.rig_refactor_properties
        layout = self.layout
        layout.operator("rig_refactor.delete_unused_bones")
        layout.operator("rig_refactor.delete_unused_vertex_groups")