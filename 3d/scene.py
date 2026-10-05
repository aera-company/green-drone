"""Câmera, render e utilidades compartilhadas pelos testes."""
import math
import os
import sys
import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "renders")


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def camera(az, el, dist, focal, target=(0, 0, 0), roll=0.0, name="CAM"):
    cam = bpy.data.objects.get(name)
    if cam is None:
        cd = bpy.data.cameras.new(name)
        cam = bpy.data.objects.new(name, cd)
        bpy.context.collection.objects.link(cam)
    cam.data.lens = focal
    cam.data.sensor_width = 36
    t = Vector(target)
    a, e = math.radians(az), math.radians(el)
    pos = t + Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist
    cam.location = pos
    d = (t - pos).normalized()
    q = d.to_track_quat("-Z", "Y")
    cam.rotation_euler = q.to_euler()
    cam.rotation_euler.rotate_axis("Z", math.radians(roll))
    bpy.context.scene.camera = cam
    return cam


def size(w, h, pct=100):
    r = bpy.context.scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, pct


def workbench_silhouette():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "FLAT"
    sc.display.shading.color_type = "SINGLE"
    sc.display.shading.single_color = (1, 1, 1)
    sc.render.film_transparent = True
    sc.display.render_aa = "8"
    sc.view_settings.view_transform = "Standard"


def render_to(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def load_alpha(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    bpy.data.images.remove(img)
    a = px.reshape(h, w, 4)[::-1, :, 3]
    return a


def args():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
