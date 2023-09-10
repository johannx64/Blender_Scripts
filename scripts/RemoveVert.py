import bpy

def draw(self, context):
    self.layout.label(text="Error!")

class MessageBoxOperator(bpy.types.Operator):
    bl_idname = "ui.show_message_box"
    bl_label = "Show Message Box"

    def execute(self, context):
        # Check if the file has been saved
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please select the skateboard")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MessageBoxOperator)

def unregister():
    bpy.utils.unregister_class(MessageBoxOperator)

def RemoveVert():
    # Select the board object
    # If nothing is selected, display an error
    selection = bpy.context.selected_objects
    counter = len(selection)
    if counter == 0:
        bpy.context.window_manager.popup_menu(draw, title="Please select the skateboard", icon='ERROR')
        print("Nothing selected")
        return

    # Query the connection
    board_object = selection[0]
    constraint = None
    for constraint in board_object.constraints:
        if constraint.type == 'LIMIT_LOCATION':
            break
    if constraint:
        board_object.constraints.remove(constraint)

    # Bake the animation
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    bpy.context.scene.frame_set(start_frame)
    bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, only_selected=True, visual_keying=True)

    # Select the 'Hips' object
    # Select the 'Hips' bone inside the 'Armature' armature
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Armature'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='POSE')  # Switch to Pose Mode
    bpy.context.object.data.bones.active = bpy.context.object.data.bones['Hips']  # Select the 'Hips' bone
    bpy.ops.pose.select_all(action='SELECT')  # Select the bone
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode
    #bpy.data.objects['Hips'].select_set(True)
    board_object = selection[0]
    constraint = None
    for constraint in board_object.constraints:
        board_object.constraints.remove(constraint)  # Remove each constraint

#   bpy.ops.object.delete(use_global=False)
#RemoveVert()