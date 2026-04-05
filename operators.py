import re

import bpy


class RigRefactorAutoConnectBones(bpy.types.Operator):
    bl_idname = "rig_refactor.auto_connect_bones"
    bl_label = "Automatically Connect Bones"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        bpy.ops.ed.undo_push()
        properties = context.scene.rig_refactor_properties

        if context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')

        obj = context.object
        arm = obj.data

        if not properties.auto_connect_bones_selected_only:
            for bone in arm.edit_bones:
                bone.select = True

        for eb in context.selected_editable_bones:
            parent = eb

            while len(parent.children) > 0:
                bone = parent.children[0]

                if len(parent.children) == 1:
                    parent.tail = bone.head
                    bone.use_connect = True

                parent = bone

        self.report({'INFO'}, "Done")
        return {'FINISHED'}


class RigRefactorCorrectBoneLength(bpy.types.Operator):
    bl_idname = "rig_refactor.correct_bone_length"
    bl_label = "Correct Length of Bones"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        bpy.ops.ed.undo_push()
        properties = context.scene.rig_refactor_properties

        if context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')

        obj = context.object
        arm = obj.data

        if not properties.correct_bone_length_selected_only:
            for bone in arm.edit_bones:
                bone.select = True

        if properties.correct_bone_length_limit_max:
            max_len = properties.correct_bone_length_max

            for bone in context.selected_editable_bones:
                has_connected_children = any(child.use_connect for child in bone.children)

                if not has_connected_children and bone.length > max_len:
                    direction = (bone.tail - bone.head).normalized()
                    new_tail = bone.head + direction * max_len

                    bone.tail = new_tail

        if properties.correct_bone_length_limit_min:
            min_len = properties.correct_bone_length_min
            avg_len = min_len

            if properties.correct_bone_length_min_to_avg:
                lengths = [b.length for b in arm.edit_bones if b.length > min_len]
                if lengths:
                    avg_len = sum(lengths) / len(lengths)

            for bone in context.selected_editable_bones:
                if bone.length <= min_len:
                    direction = (bone.tail - bone.head).normalized()
                    bone.tail = bone.head + direction * avg_len

        self.report({'INFO'}, "Done")
        return {'FINISHED'}


class RigRefactorRenameBonesRemoveNumericSuffix(bpy.types.Operator):
    bl_idname = "rig_refactor.rename_bones_remove_numeric_suffix"
    bl_label = "Remove Numeric Suffix"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        bpy.ops.ed.undo_push()
        properties = context.scene.rig_refactor_properties

        obj = context.object
        arm = obj.data

        sep = properties.rename_bones_number_prefix
        for bone in arm.bones:
            name = bone.name
            if sep:
                postfix = name.split(sep)[-1]
                if postfix.isdigit():
                    bone.name = name.rsplit(sep, 1)[0]
            else:
                new_name = re.sub(r'\d+$', '', name)
                if new_name != name:
                    bone.name = new_name

        self.report({'INFO'}, "Done")
        return {'FINISHED'}


class RigRefactorRenameBonesMirror(bpy.types.Operator):
    bl_idname = "rig_refactor.rename_bones_mirror"
    bl_label = "Rename Bones"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        bpy.ops.ed.undo_push()

        armature = context.object
        properties = context.scene.rig_refactor_properties

        mode = properties.rename_bones_mirror_mode
        search_lf = properties.rename_bones_search_lf
        search_rt = properties.rename_bones_search_rt
        suffix_lf = properties.rename_bones_lf_suffix
        suffix_rt = properties.rename_bones_rt_suffix

        def process_name(name, search, suffix):
            if mode == "any_match":
                if search in name:
                    return name.replace(search, "") + suffix

            elif mode == "start_with":
                if name.startswith(search):
                    return name[len(search):] + suffix

            elif mode == "end_with":
                if name.endswith(search):
                    return name[:-len(search)] + suffix

            return None

        if armature and armature.type == 'ARMATURE':
            for bone in armature.data.bones:
                name = bone.name

                new_name = process_name(name, search_lf, suffix_lf)

                if new_name is None:
                    new_name = process_name(name, search_rt, suffix_rt)

                if new_name:
                    bone.name = new_name

        self.report({'INFO'}, "Done")
        return {'FINISHED'}


class RigRefactorDeleteUnusedBones(bpy.types.Operator):
    bl_idname = "rig_refactor.delete_unused_bones"
    bl_label = "Delete Unused Bones"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == 'ARMATURE'

    def execute(self, context):
        bpy.ops.ed.undo_push()

        armature = context.object

        meshes = []
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for mod in obj.modifiers:
                    if mod.type == 'ARMATURE' and mod.object == armature:
                        meshes.append(obj)
                        break

        used_vg_names = set()
        for mesh in meshes:
            for vert in mesh.data.vertices:
                for g in vert.groups:
                    if g.weight > 0:
                        vg_name = mesh.vertex_groups[g.group].name
                        used_vg_names.add(vg_name)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = armature.data.edit_bones
        bones_to_remove = [b for b in edit_bones if b.name not in used_vg_names]
        for bone in bones_to_remove:
            edit_bones.remove(bone)

        self.report({'INFO'}, "Done")
        return {'FINISHED'}


class RigRefactorDeleteUnusedVertexGroups(bpy.types.Operator):
    bl_idname = "rig_refactor.delete_unused_vertex_groups"
    bl_label = "Delete Unused Vertex Groups"

    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        return objs and any(obj.type == 'MESH' for obj in objs)

    def execute(self, context):
        bpy.ops.ed.undo_push()

        def clean_vertex_groups(obj):
            if obj.type != 'MESH':
                return

            armature = None
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object and modifier.object.type == 'ARMATURE':
                    armature = modifier.object
                    break

            valid_bone_names = set()
            if armature:
                valid_bone_names = {bone.name for bone in armature.data.bones}

            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='OBJECT')

            groups_to_delete = []

            for vg in obj.vertex_groups:
                group_index = vg.index

                has_weight = any(group.group == group_index for v in obj.data.vertices for group in v.groups)

                bone_exists = (vg.name in valid_bone_names) if armature else True

                if not has_weight or not bone_exists:
                    groups_to_delete.append(vg.name)

            for name in groups_to_delete:
                obj.vertex_groups.remove(obj.vertex_groups[name])

        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for obj in selected_objects:
            clean_vertex_groups(obj)

        self.report({'INFO'}, "Done")
        return {'FINISHED'}
