import bpy
import os

def DrippyAnimExport():
    # This will rename the file to the same as the folder it's in
    path = bpy.data.filepath
    directory = os.path.dirname(path)
    nameBase = os.path.basename(directory)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(directory, nameBase + ".blend"))

    # This is going to rename everything without the prefix
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    selection = bpy.context.selected_objects
    for sel in selection:
        selName = sel.name
        index = selName.find(":")
        if selName in bpy.data.objects and index >= 0:
            object = selName
            x = object.split(":")
            bpy.data.objects[selName].name = x[1]

    # Bake down the animation just in case
    start = bpy.context.scene.frame_start
    end = bpy.context.scene.frame_end
    bpy.ops.nla.bake(frame_start=start, frame_end=end, step=1, only_selected=False, visual_keying=True, clear_constraints=False, use_current_action=False, bake_types={'POSE'})

    # Delete everything that isn't the armature
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["Armature"].select_set(True)
    bpy.ops.object.delete()

    # Export the FBX version
    p = os.path.join(directory, nameBase + ".fbx")
    bpy.ops.export_scene.fbx(filepath=p, use_scene_name=True, bake_anim_use_all_actions=True, bake_anim_use_nla_strips=True)

