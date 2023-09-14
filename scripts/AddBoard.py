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

def draw(self, context):
    self.layout.label(text="Error!")

def AddBoard():
    # User needs to select the skateboard or the part of the skateboard 
    # that has the animation on it so that the skateboard rig can be brought in 
    # and bake the animation down on
    selection = bpy.context.selected_objects
    counter = len(selection)
    print(selection)
    if counter == 0:
        bpy.context.window_manager.popup_menu(draw, title="Please select the skateboard", icon='ERROR')
        return
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



    # Get references to the objects you want to work with
    selected_object_name = "Armature.001"
    target_object_name = "SkateboardMesh"

    # Get references to the selected object and the target object
    selected_object = bpy.data.objects.get(selected_object_name)
    target_object = bpy.data.objects.get(target_object_name)

    if selected_object and target_object:
        # Create a Copy Location constraint on the selected object
        constraint_location = selected_object.constraints.new(type='COPY_LOCATION')
        constraint_location.target = target_object
        constraint_location.use_offset = True  # Enable offset on location

        # Create a Copy Rotation constraint on the selected object
        constraint_rotation = selected_object.constraints.new(type='COPY_ROTATION')
        constraint_rotation.target = target_object
    else:
        print("One or both objects not found in the scene.")

    # You can further customize the constraint settings if needed.

    # Get a reference to the object you want to bake
    selected_object_name = "Armature.001"  # Replace with the actual object name
    selected_object = bpy.data.objects.get(selected_object_name)

    if selected_object:
        # Set the current frame to the start frame of the animation
        bpy.context.scene.frame_set(bpy.context.scene.frame_start)
        selected_object.location.z -= 0.050001
        
        # Create a keyframe for the selected object's location and rotation
        selected_object.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)
        selected_object.keyframe_insert(data_path="rotation_euler", frame=bpy.context.scene.frame_current)
        
        # Advance to the next frame and repeat until the end frame is reached
        for frame in range(bpy.context.scene.frame_start + 1, bpy.context.scene.frame_end + 1):
            bpy.context.scene.frame_set(frame)
            
            # Insert keyframes for location and rotation
            selected_object.keyframe_insert(data_path="location", frame=frame)
            selected_object.keyframe_insert(data_path="rotation_euler", frame=frame)
    else:
        print("Object not found in the scene.")
    
    # Bake the animation
    bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start,
                     frame_end=bpy.context.scene.frame_end,
                     only_selected=True,
                     visual_keying=True,
                     clear_constraints=True,
                     clear_parents=True,
                     use_current_action=True,
                     bake_types={'OBJECT'})
    
    
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
    if os.path.exists(blend_export_path):
        os.remove(blend_export_path)    
    bpy.ops.wm.save_as_mainfile(filepath=blend_export_path)

    # Export the FBX file with the same name as the scene plus "_char"
    # Specify the name of the parent armature
    parent_armature_name = "Armature.001"
    
    # Get the parent armature object
    parent_armature = bpy.data.objects.get(parent_armature_name)
    fbx_export_path = os.path.join(directory, f"{new_scene_name}.fbx")
    if os.path.exists(fbx_export_path):
        os.remove(fbx_export_path)  
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.export_scene.fbx(filepath=fbx_export_path, use_selection=False, add_leaf_bones=False)

    # Report the export path
    print(f"FBX file saved to: {fbx_export_path}")
    print(f"Blender file saved to: {blend_export_path}")   
    
    # Reload the original Blender file
    bpy.ops.wm.open_mainfile(filepath=filepath)