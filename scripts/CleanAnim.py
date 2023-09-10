import bpy
import os
import re

def CleanAnim():
    # Get the name of the currently opened Blender scene
    folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_riggingObjects")

    scene_path = bpy.data.filepath
    # Extract the folder path without the scene name
    folder_path = os.path.dirname(scene_path)
    
    # Import the FBX file containing the skeleton with the Blender rig in bind pose
    fbx_file_path = os.path.join(folder, "blenderRefRig.fbx")
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)

    # Select and store the animated skeleton
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="rigRef*")
    bpy.ops.object.duplicate()
    animated_skeleton = bpy.context.selected_objects[0]

    # Put the animated skeleton into the bind pose by using the origin skeleton as reference
    # Note: Autokeying needs to be off
    for bone in animated_skeleton.pose.bones:
        target_name = re.sub(r"rigRef/", "NewName/", bone.name)  # Change "NewName" to the desired name
        target_bone = bpy.data.objects.get(target_name)
        if target_bone:
            target_bone.location = bone.location
            target_bone.rotation_euler = bone.rotation_euler

    # Delete the reference skeleton
    bpy.data.objects.remove(animated_skeleton)
    
    # Import the clean skeleton with no rotation or joint orientation
    fbx_file_path = os.path.join(folder, "retargetSkel.fbx")
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)
    
    # Parent constrain the clean skeleton to the animated one with maintain offset on
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Armature*")
    bpy.ops.object.select_all(action='INVERT')
    
    bpy.ops.object.delete()

    # Bake down the animation
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    bpy.context.view_layer.objects.active = bpy.data.objects["Armature"]
    bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, bake_types={'POSE'})

    # Delete the constraints
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern="Armature.001*")

    # Find and delete the "Armature.001" object if it exists
    armature_001 = bpy.data.objects.get("Armature.001")
    if armature_001:
        bpy.data.objects.remove(armature_001)
    else:
        print("missing armature")
        return

    # Rename the final skeleton bones
    for bone in bpy.data.objects["Armature"].pose.bones:
        new_name = re.sub(r"target_", "", bone.name)
        bone.name = new_name

    # Modify the scene name to include "_char" at the end
    scene_name = bpy.path.basename(bpy.data.filepath).rpartition('.')[0]
    print(f"Scene name: {scene_name}")
    new_scene_name = f"{scene_name}_char"

    # Save the Blender scene with the modified name
    #new_scene_path = os.path.join(folder_path, f"{new_scene_name}.blend")

    # Save the file out with the folder name
    path = bpy.data.filepath
    directory = os.path.dirname(path)
    blend_export_path = os.path.join(directory, f"{new_scene_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_export_path)


    #bpy.ops.wm.save_as_mainfile(filepath=new_scene_path)

    # Export the FBX file with the same name as the scene plus "_char"
    fbx_export_path = os.path.join(directory, f"{new_scene_name}.fbx")
    bpy.ops.export_scene.fbx(filepath=fbx_export_path, use_selection=False)

    # Report the export path
    print(f"FBX file saved to: {fbx_export_path}")
    print(f"Blender file saved to: {blend_export_path}")

    # Reopen the original scene
    bpy.ops.wm.open_mainfile(filepath=scene_path)

#CleanAnim("C:/Users/cryptox/AppData/Roaming/Blender Foundation/Blender/3.6/scripts/addons/Blender_Scripts/scripts/_riggingObjects")
