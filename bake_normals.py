# Bakes normal in blender
#
# What it does:
#
# 1) Temporarily switch to cycles.
# 2) Temporarily select normal texture of the shader.
# 3) Temporarily disable all non-multires modifiers
# 4) Cycles bake normal
# 5) Revert to the original state
# 6) Reload all affected images
#
# Errors
#
# If no valid normal texture is found. 
#
# We look for an image that's input to the normal map node.

import bpy

def select_normal_image(node_tree):
    normal_map_node = next((n for n in node_tree.nodes if n.type == 'NORMAL_MAP'), None)
    if not normal_map_node:
        raise Exception("Requires a normal map node.")

    color_input = normal_map_node.inputs.get("Color")
    if not color_input or not color_input.is_linked:
        raise Exception("Requires a normal map node with image input.")

    from_node = color_input.links[0].from_node
    if from_node.type == 'TEX_IMAGE':
        return from_node
    raise Exception("Requires a normal map node with image input.")


def main():
    deferred_actions = []
    changed_images = []

    prev_engine = bpy.context.scene.render.engine
    bpy.context.scene.render.engine = 'CYCLES'

    def revert(engine=prev_engine):
        bpy.context.scene.render.engine = engine
    deferred_actions.append(revert)

    for mesh in bpy.context.selected_objects:
        if mesh.type != 'MESH':
            continue
        # Get the first material
        mat = mesh.material_slots[0].material

        if not mat or not mat.use_nodes:
            continue

        node_tree = mat.node_tree
        image = select_normal_image(node_tree)
        changed_images.append(image.image)
        prev = node_tree.nodes.active
        node_tree.nodes.active = image

        def revert(node_tree=node_tree, prev=prev):
            if prev:
                node_tree.nodes.active = prev

        deferred_actions.append(revert)

        for mod in mesh.modifiers:
            if mod.type != 'MULTIRES':
                prev = mod.show_viewport
                mod.show_viewport = False

                def revert(mod=mod, prev=prev):
                    mod.show_viewport = prev

                deferred_actions.append(revert)

    # set baking parameters
    bake_type = bpy.context.scene.render.bake_type
    multires = bpy.context.scene.render.use_bake_multires
    margin = bpy.context.scene.render.bake_margin

    def revert(bake_type=bake_type, multires=multires, margin=margin):
        bpy.context.scene.render.bake_type = bake_type
        bpy.context.scene.render.use_bake_multires = multires
        bpy.context.scene.render.bake_margin = margin

    bpy.context.scene.render.bake_type = 'NORMALS'
    bpy.context.scene.render.use_bake_multires = True
    bpy.context.scene.render.bake_margin = 16
    deferred_actions.append(revert)

    bpy.ops.object.bake_image()

    for image in changed_images:
        image.update()

    for action in deferred_actions:
        action()


# Define the operator
class OBJECT_OT_bake_multires_normal(bpy.types.Operator):
    """Run custom function"""
    bl_idname = "object.bake_multires_normal"
    bl_label = "Bake Multires Normal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Your custom function logic goes here
        obj = context.active_object
        if obj:
            self.report({'INFO'}, f"Baked multires normal ran on {obj.name}")
            main()
        else:
            self.report({'WARNING'}, "No active object")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_bake_multires_normal.bl_idname, icon='MODIFIER')

def register():
    bpy.utils.register_class(OBJECT_OT_bake_multires_normal)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_bake_multires_normal)


if __name__ == "__main__":
    register()
