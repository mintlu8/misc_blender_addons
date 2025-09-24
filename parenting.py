import bpy
import mathutils

def center_of_mass(obj):
    if not obj.data.vertices:
        return obj.matrix_world.translation.copy()
    total = mathutils.Vector((0.0, 0.0, 0.0))
    for v in obj.data.vertices:
        total += v.co
    return obj.matrix_world @ total

def distance_to_line_segment(a, x, y):
    d1 = a - x
    d = y - x
    len2 = d.length_squared
    if len2 == 0.0:
        return d1.length
    t = d1.dot(d) / len2
    if t <= 0.0:
        return (a - x).length
    elif t >= 1.0:
        return (a - y).length
    else:
        return (x + t * d).length

def find_best_bone(armature, position):
    if armature.type != 'ARMATURE':
        raise Exception("Expected active object armature.")

    mat = armature.matrix_world
    best_fit = 999999999
    result = None
    for bone in armature.data.bones:
        if not bone.use_deform:
            continue
        head = mat @ bone.head_local
        tail = mat @ bone.tail_local
        d = distance_to_line_segment(position, head, tail)
        if d < best_fit:
            best_fit = d
            result = bone
    if not result:
        raise Exception("Expected at least one deforming bone.")
    return result


def set_vertex_group_weight(obj, group_name, weight_value):
    if obj.type != 'MESH':
        raise Exception("Expected mesh.")

    vg = obj.vertex_groups.get(group_name)
    if vg is None:
        vg = obj.vertex_groups.new(name=group_name)

    verts = range(len(obj.data.vertices))
    vg.add(verts, weight_value, 'REPLACE')

def main():
    armature = bpy.context.active_object
    bpy.ops.object.parent_set(type='ARMATURE_NAME')
    for obj in bpy.context.selected_objects:
        if obj.type != 'MESH':
            continue
        center = center_of_mass(obj)
        bone = find_best_bone(armature, center)
        set_vertex_group_weight(obj, bone.name, 1.0)


class OBJECT_OT_parent_single_bone(bpy.types.Operator):
    """Parent to armature controlled by the nearest bone."""
    bl_idname = "object.parent_single_bone"
    bl_label = "Armature Parent to Single Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj:
            self.report({'INFO'}, f"Parent to single bone on {obj.name}.")
            try:
                main()
            except Exception as e:
                self.report({'WARNING'}, f"{e}")
        else:
            self.report({'WARNING'}, "No active object")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_parent_single_bone.bl_idname, icon='MODIFIER')

def register():
    bpy.utils.register_class(OBJECT_OT_parent_single_bone)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_parent_single_bone)


if __name__ == "__main__":
    register()
