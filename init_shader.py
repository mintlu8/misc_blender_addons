import bpy

def main():
    for obj in bpy.context.selected_objects:
        if obj.type != 'MESH':
            continue
        obj.data.materials.clear()
        # Create material
        mat = bpy.data.materials.new("PbrMaterial")
        mat.use_nodes = True
        obj.data.materials.append(mat)

        # Get node tree
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear default nodes
        for n in nodes:
            nodes.remove(n)

        # Add nodes
        output = nodes.new("ShaderNodeOutputMaterial")
        output.location = (400, 0)

        principled = nodes.new("ShaderNodeBsdfPrincipled")
        principled.location = (0, 0)

        links.new(principled.outputs["BSDF"], output.inputs["Surface"])

        # Create color image (8-bit int precision)
        color_img = bpy.data.images.new(
            "PbrColor",
            width=1024,
            height=1024,
            alpha=True,
            float_buffer=False  # 8-bit per channel
        )
        color_img.pixels = [1.0, 1.0, 1.0, 1.0] * (1024 * 1024)
        color_img.update()
        color_tex = nodes.new("ShaderNodeTexImage")
        color_tex.image = color_img
        color_tex.location = (-400, 200)
        links.new(color_tex.outputs["Color"], principled.inputs["Base Color"])

        # Create normal map image (32-bit float precision)
        normal_img = bpy.data.images.new(
            "PbrNormal",
            width=1024,
            height=1024,
            alpha=False,
            float_buffer=True  # 32-bit float
        )
        normal_img.pixels = [0.5, 0.5, 1.0, 1.0] * (1024 * 1024)
        normal_img.update()
        normal_tex = nodes.new("ShaderNodeTexImage")
        normal_tex.image = normal_img
        normal_tex.location = (-800, -200)

        # Add normal map node
        normal_map = nodes.new("ShaderNodeNormalMap")
        normal_map.location = (-400, -200)

        links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"])
        links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])

        nodes.active = color_tex


class OBJECT_OT_init_pbr_shader(bpy.types.Operator):
    """Initialize pbr shader for an object."""
    bl_idname = "object.init_pbr_shader"
    bl_label = "Initialize pbr shader"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Your custom function logic goes here
        obj = context.active_object
        if obj:
            self.report({'INFO'}, f"Initialized pbr shader on {obj.name}")
            main()
        else:
            self.report({'WARNING'}, "No active object")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_init_pbr_shader.bl_idname, icon='MODIFIER')

def register():
    bpy.utils.register_class(OBJECT_OT_init_pbr_shader)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_init_pbr_shader)


if __name__ == "__main__":
    register()
