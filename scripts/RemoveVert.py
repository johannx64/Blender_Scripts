import bpy

def find_and_delete_ty_fcurve():
    # Select the board object
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    # If nothing is selected, show an error message
    if bpy.context.selected_objects == []:
        print("Nothing selected")
        bpy.ops.wm.popup_menu_alert('INVOKE_DEFAULT')
        return

    # Query the connection
    obj = bpy.context.active_object
    conn = None
    
    # Check if there is a "ty" F-curve
    for fcurve in obj.animation_data.action.fcurves:
        if fcurve.data_path == 'location' and fcurve.array_index == 1:
            conn = fcurve
            break

    if conn is not None:
        print(f"Found 'ty' F-curve: {conn}")
        
        # Access keyframes of the F-curve
        keyframes = [(keyframe.co.x, keyframe.co.y) for keyframe in conn.keyframe_points]
        print("Keyframes:")
        for frame, value in keyframes:
            print(f"Frame: {frame}, Value: {value}")
        
        # Delete the found F-curve
        obj.animation_data.action.fcurves.remove(conn)
        print("Deleted 'ty' F-curve.")
    else:
        print("No 'ty' F-curve found")

def get_dopesheet_area():
    override_area = None
    for screen in bpy.context.workspace.screens:
        for area in screen.areas:
            if area.type == "DOPESHEET_EDITOR":
                return area
    return None

##add here, go to Armature Object, you must find in scene and disable/remove the Hips keyframes
"""add the code here for function cleanHips"""
def disableHipsKeyframes():
    # Find the armature object in the scene (assuming it's the parent of the skateboard)
    armature = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
            break

    if armature is not None:
        # Find the "Hips" bone
        target_bone_name = "Hips"  # Replace with the actual bone name
        target_bone = armature.pose.bones.get(target_bone_name)
        
        if target_bone is not None:
            # Get the Dopesheet area
            dopesheet_area = get_dopesheet_area()

            if dopesheet_area is not None:
                override = bpy.context.copy()
                override["area"] = dopesheet_area

                # Toggle the mute channels setting for the "Hips" bone
                bpy.ops.anim.channels_setting_enable(override, type='MUTE')

                print(f"Toggled visibility (mute) of '{target_bone_name}' bone's channels in the Dopesheet.")
            else:
                print("Dopesheet area not found.")
        else:
            print(f"'{target_bone_name}' bone not found in the armature.")
    else:
        print("Armature object not found in the scene.")

def remove_vertical_translation():
    # Check the selection
    selection = bpy.context.selected_objects
    counter = len(selection)
    
    if counter == 0:
        bpy.context.window_manager.popup_menu(draw, title="Please select the skateboard", icon='ERROR')
        return
    
    skateboard = bpy.context.active_object
    
    # Get the initial Z-location as reference
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    initial_location_z = skateboard.location.z
    
    # Remove the vertical translation by setting the Z-location relative to the initial frame
    for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        bpy.context.scene.frame_set(frame)
        skateboard.location.z = initial_location_z
        skateboard.keyframe_insert(data_path="location", index=2)
    
    # Reset the frame back to the start
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)

# Define the draw function for the popup menu
def draw(self, context):
    self.layout.label(text="No skateboard selected!")

def RemoveVert():
    # Ensure the skateboard object is selected before running the script
    if bpy.context.active_object:
        find_and_delete_ty_fcurve()
        #remove_vertical_translation()
        #disableHipsKeyframes()
        
    else:
        bpy.context.window_manager.popup_menu(draw, title="Please select the skateboard", icon='ERROR')
