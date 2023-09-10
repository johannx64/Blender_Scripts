bl_info = {
    "name": "Prep Scene",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os

def draw(self, context):
    self.layout.label(text="Error!")


class MessageBoxOperator(bpy.types.Operator):
    bl_idname = "ui.show_message_box"
    bl_label = "Show Message Box"

    def execute(self, context):
        # Check if the file has been saved
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save the file before running this script.")
        else:
            self.report({'INFO'}, "File has been saved.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MessageBoxOperator)

def unregister():
    bpy.utils.unregister_class(MessageBoxOperator)

def remove_prefix(name):
    # Split the name by ':' and take the last part
    parts = name.split(':')
    if len(parts) > 1:
        return parts[-1]
    return name
register()
def PrepScene():
    # Check if the file has been saved
    if not bpy.data.filepath:        
        # test call to the operator
        bpy.ops.ui.show_message_box()        
        return

    # User needs to select the skateboard model or models
    # If nothing is selected, display an error
    selection = bpy.context.selected_objects
    counter = len(selection)
    print(selection)
    if counter == 0:
        bpy.context.window_manager.popup_menu(draw, title="Please select the skateboard", icon='ERROR')
        return

    # Create an empty object to group the skateboard objects
    bpy.ops.object.empty_add(location=(0, 0, 0))
    skateboard_group = bpy.context.object
    skateboard_group.name = "skGroup"

    # Parent the skateboard objects to the group
    for obj in selection:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = skateboard_group
    bpy.ops.object.parent_set(type='OBJECT')
    
    # Set the rotation of the skateboard group (180 degrees around Y-axis, 90 degrees around X-axis)
    skateboard_group.rotation_euler = (0, 0, 3.14159)  # x = 90 degrees, y = 0 degrees, z = 180 degrees

    # Flip the character round via the armature (180 degrees around Z-axis)
    armature = bpy.data.objects['Armature']
    armature.rotation_euler[2] = 3.14159  # Rotate 180 degrees around Z-axis


    # Rename the head material to headMTL
    if "Head" in bpy.data.materials:
        bpy.data.materials["Head"].name = "HeadMtl"
    
    filepath=bpy.data.filepath
    print(f"Saving file as: {filepath}")
    # Check if the file exists and remove it
    if os.path.exists(filepath):
        os.remove(filepath)
        
    bpy.ops.wm.save_mainfile(filepath=filepath, check_existing=False)

    # This is the start of the process to remove excess joints
    # and remove any prefixes
    bpy.ops.object.select_all(action='DESELECT')
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    for bone in armature.pose.bones:
        bone.name = remove_prefix(bone.name)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a yTrans empty object
    bpy.ops.object.empty_add(location=(0, 0, 0))
    yTrans = bpy.context.object
    yTrans.name = 'yTrans'

    # Parent yTrans to the skGroup
    bpy.ops.object.select_all(action='DESELECT')
    yTrans.select_set(True)
    bpy.context.view_layer.objects.active = skateboard_group  # Set the active object to skGroup
    bpy.ops.object.parent_set(type='OBJECT')

    # Set the yTrans location relative to 'Hips' bone
    hips_bone = armature.pose.bones.get('Hips')
    if hips_bone:
        yTrans.location = hips_bone.head

    # Select yTrans directly
    yTrans = bpy.data.objects.get('yTrans')
    if yTrans:
        yTrans.select_set(True)
        bpy.context.view_layer.objects.active = yTrans

    # Create a Copy Location constraint from 'Hips' to yTrans
    bpy.ops.object.constraint_add(type='COPY_LOCATION')
    bpy.context.object.constraints["Copy Location"].target = armature
    bpy.context.object.constraints["Copy Location"].subtarget = 'Hips'
    bpy.context.object.constraints["Copy Location"].use_offset = True  # Set use_offset to True

    # Bake the animation
    # Check if the file exists and remove it
    if os.path.exists(filepath):
        os.remove(filepath)
    bpy.ops.wm.save_mainfile(filepath=filepath, check_existing=False)
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)
    bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start, frame_end=bpy.context.scene.frame_end, only_selected=True, visual_keying=True)

    # Save the file out with the folder name
    path = bpy.data.filepath
    directory = os.path.dirname(path)
    nameBase = os.path.basename(directory)
    # Check if the file exists and remove it
    if os.path.exists(filepath):
        os.remove(filepath)
    bpy.ops.wm.save_mainfile(filepath=filepath, check_existing=False)