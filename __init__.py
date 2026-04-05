bl_info = {
    "name": "Rig Refactor",
    "description": "",
    "author": "x6ud",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "category": "Object"
}

import bpy

from .operators import \
    RigRefactorAutoConnectBones, \
    RigRefactorCorrectBoneLength, \
    RigRefactorRenameBonesRemoveNumericSuffix, \
    RigRefactorRenameBonesMirror, \
    RigRefactorDeleteUnusedBones, \
    RigRefactorDeleteUnusedVertexGroups
from .properties import RigRefactorProperties
from .ui import \
    RigRefactorPanelMain, \
    RigRefactorPanelAutoConnectBones, \
    RigRefactorPaneCorrectBoneLength, \
    RigRefactorPaneRenameBones, \
    RigRefactorPaneClearUnused

classes = [
    RigRefactorAutoConnectBones,
    RigRefactorCorrectBoneLength,
    RigRefactorRenameBonesRemoveNumericSuffix,
    RigRefactorRenameBonesMirror,
    RigRefactorDeleteUnusedBones,
    RigRefactorDeleteUnusedVertexGroups,

    RigRefactorProperties,

    RigRefactorPanelMain,
    RigRefactorPanelAutoConnectBones,
    RigRefactorPaneCorrectBoneLength,
    RigRefactorPaneRenameBones,
    RigRefactorPaneClearUnused,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rig_refactor_properties = bpy.props.PointerProperty(type=RigRefactorProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
