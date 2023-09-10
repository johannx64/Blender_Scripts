import bpy
import os

def DrippyRigObject():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    for obj in mesh_objects:
        obj.select_set(True)
        bpy.ops.object.delete(use_global=False)

    bpy.ops.wm.link(filename='../_rigObjects/DrippyBaseRig.blend', directory=os.path.dirname(bpy.data.filepath), link=False, relative_path=False)

    for mesh in mesh_objects:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Hips'].select_set(True)
        mesh.select_set(True)
        bpy.ops.object.parent_set(type='ARMATURE_NAME')

    bpy.ops.wm.link(filename='../_rigObjects/DrippyWeightedMesh.blend', directory=os.path.dirname(bpy.data.filepath), link=False, relative_path=False)

    source_cluster = bpy.data.objects['sourceCluster']
    clusters = [obj for obj in bpy.data.objects if obj.type == 'MESH' and 'Cluster' in obj.name]

    for cluster in clusters:
        bpy.ops.object.select_all(action='DESELECT')
        source_cluster.select_set(True)
        cluster.select_set(True)
        bpy.ops.object.data_transfer(data_type='VGROUP_WEIGHTS', use_create=True, use_auto_transform=False, layers_select_src='NAME')
        cluster.name = cluster.name.replace('Cluster', '')

    bpy.data.objects.remove(source_cluster)

    path = bpy.data.filepath
    directory = os.path.dirname(path)
    name = os.path.basename(path)
    p = os.path.join(directory, name)

    bpy.ops.export_scene.fbx(filepath=p, use_selection=True, global_scale=1.0)

