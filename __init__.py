bl_info = {
    "name": "Misc Blender Utilies",
    "author": "Mincong Lu",
    "version": (0, 1),
    # "blender": (4, 5, 0),
    "location": "3D View > Right-Click Menu",
    "description": "Adds some utilities.",
    "warning": "",
    "category": "Object",
}

import importlib
from . import bake_normals, init_shader, parenting

# Reload for development (so Blender updates without restart)
importlib.reload(bake_normals)
importlib.reload(init_shader)
importlib.reload(parenting)

def register():
    bake_normals.register()
    init_shader.register()
    parenting.register()

def unregister():
    bake_normals.unregister()
    init_shader.unregister()
    parenting.unregister()
