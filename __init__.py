bl_info = {
    "name": "Allerion",
    "blender": (2, 80, 0),  # Blender version required
    "category": "Object",  # The category under which your addon will appear
    "author": "johann9616@gmail.com",
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > MyApp",
    "description": "Description of your addon",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy
import os
from .scripts.PrepScene import PrepScene
from .scripts.CleanAnim import CleanAnim
from .scripts.RemoveVert import RemoveVert
from .scripts.AddBoard import AddBoard

# Set the absolute path to the "scripts" folder
scripts_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")

# List all script files in the "scripts" folder
script_files = [f for f in os.listdir(scripts_folder) if f.endswith(".py")]

class ALLERION_PT_ScriptsPanel(bpy.types.Panel):
    bl_label = "Scripts"
    bl_idname = "ALLERION_PT_ScriptsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scripts'

    def draw(self, context):
        layout = self.layout

        for script_file in script_files:
            script_file=script_file.replace(".py", "")            
            layout.operator("allerion.run_script", text=script_file).script_name = script_file

class ALLERION_OT_RunScript(bpy.types.Operator):
    bl_idname = "allerion.run_script"
    bl_label = "Run Script"
    script_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            self.report({'INFO'}, self.script_name)           
            if "PrepScene" in self.script_name:
                PrepScene()
            elif "CleanAnim" in self.script_name:
                CleanAnim()
            elif "AddBoard" in self.script_name:
                AddBoard()
            elif "RemoveVert" in self.script_name:
                RemoveVert()
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error running script '{self.script_name}': {str(e)}")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(ALLERION_PT_ScriptsPanel)
    bpy.utils.register_class(ALLERION_OT_RunScript)

def unregister():
    bpy.utils.unregister_class(ALLERION_PT_ScriptsPanel)
    bpy.utils.unregister_class(ALLERION_OT_RunScript)

if __name__ == "__main__":
    register()
