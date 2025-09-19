bl_info = {
    "name": "Misc Blender Utilies",
    "author": "Mincong Lu",
    "version": (0, 1),
    "blender": (4, 5, 0),
    "location": "3D View > Right-Click Menu",
    "description": "Adds some utilities.",
    "warning": "",
    "category": "Object",
}

import importlib
from . import bake_normals

# Reload for development (so Blender updates without restart)
importlib.reload(bake_normals)

def register():
    bake_normals.register()

def unregister():
    bake_normals.unregister()
