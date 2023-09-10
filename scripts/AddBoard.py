import bpy
import re
import os


def get_current_folder_path():
    # Get the full path of the currently opened Blender scene
    scene_path = bpy.data.filepath

    # Extract the folder path without the scene name
    folder_path = os.path.dirname(scene_path)

    # Strip the trailing slash if it exists
    if folder_path.endswith(os.path.sep):
        folder_path = folder_path[:-1]

    return folder_path

def AddBoard():
    # User needs to select the skateboard or the part of the skateboard 
    # that has the animation on it so that the skateboard rig can be brought in 
    # and bake the animation down on
    selection = bpy.context.selected_objects
    scripts_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_riggingObjects")
    # Bring in the board rig (FBX import)
    folder_path = get_current_folder_path()  # Get the folder path
    fbx_file_path = os.path.join(scripts_folder, "board_socket.fbx")
    bpy.ops.import_scene.fbx(filepath=fbx_file_path, use_image_search=False, axis_forward='Y', axis_up='Z')
    
    filepath=bpy.data.filepath
    
    if os.path.exists(filepath):
        os.remove(filepath)
    bpy.ops.wm.save_mainfile(filepath=filepath)  # Save the file to keep the board rig

    # Parent constraint the skateboard to the board rig

    #bpy.context.view_layer.objects.active = bpy.data.objects["Armature.001"]
    #bpy.ops.object.parent_set(type='OBJECT')

    # Bake down the animation
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, only_selected=True, visual_keying=True, clear_constraints=True)

    # Delete all objects except the board rig
    bpy.ops.object.select_all(action='DESELECT')
    #bpy.data.objects["Armature.001"].select_set(True)

    # Step 2: Group select ['pCube1', 'Armature.001']

    # Replace 'pCube1' and 'Armature.001' with the actual names of your objects
    objects_to_group_select = ['pCube1', 'Armature.001']

    for obj_name in objects_to_group_select:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.select_set(True)
        else:
            print(f"Object '{obj_name}' not found.")

    bpy.ops.object.select_all(action='INVERT')
    bpy.ops.object.delete()

    # Replace 'Armature' with the name of your armature object
    armature_name = 'Armature'

    # Check if the armature object exists
    armature_obj = bpy.data.objects.get(armature_name)

    if armature_obj:
        # Make sure the armature object is active
        bpy.context.view_layer.objects.active = armature_obj
        
        # Switch to Pose Mode
        bpy.ops.object.mode_set(mode='POSE')
    else:
        print(f"Armature '{armature_name}' not found.")

    # Extract the folder path without the scene name
    # Modify the scene name to include "_char" at the end
    scene_name = bpy.path.basename(bpy.data.filepath).rpartition('.')[0]
    new_scene_name = f"{scene_name}_board"
    print(f"Scene name: {scene_name}")

    # Save the file out with the folder name
    path = bpy.data.filepath
    directory = os.path.dirname(path)
    blend_export_path = os.path.join(directory, f"{new_scene_name}.blend")
    
    # Update the scene view    
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=blend_export_path)

    # Export the FBX file with the same name as the scene plus "_char"
    # Specify the name of the parent armature
    parent_armature_name = "Armature.001"

    # Get the parent armature object
    parent_armature = bpy.data.objects.get(parent_armature_name)
    fbx_export_path = os.path.join(directory, f"{new_scene_name}.fbx")
    bpy.ops.export_scene.fbx(filepath=fbx_export_path, use_selection=False)

    # Report the export path
    print(f"FBX file saved to: {fbx_export_path}")
    print(f"Blender file saved to: {blend_export_path}")   
    
    # Reload the original Blender file
    bpy.ops.wm.open_mainfile(filepath=filepath)

# Call the function to add the board
#add_board(bpy.context, "C:/Users/cryptox/AppData/Roaming/Blender Foundation/Blender/3.6/scripts/addons/Blender_Scripts/scripts/")
