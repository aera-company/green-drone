"""Leva o tubo azul da foto para 3D.

Os pontos 2D vêm da segmentação por cor (renders/_blue_mask.png) e são ordenados por waypoints
lidos na foto. Cada ponto é levantado para 3D pelo mapa de profundidade do projetor (superfície
embaixo do tubo), recuado um pouco em direção à câmera, já que o tubo passa por cima.
Saída: renders/tube_path.json (coordenadas no espaço do drone, metros).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
from mathutils import Vector
import scene

cam = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]
W, H = 1000, 667

WAYPOINTS = [(518, 128), (470, 168), (476, 192), (496, 213), (526, 229), (560, 242), (557, 259), (520, 267),
             (455, 270), (426, 281), (419, 296), (439, 320), (442, 346), (426, 364), (400, 366), (370, 353),
             (340, 346), (300, 356), (260, 376), (220, 399), (185, 414), (155, 424)]


def load(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    return px.reshape(h, w, 4)[::-1]


mask = load(os.path.join(scene.OUT, "_blue_mask.png"))[..., 0] > 0.5
depth = load(os.path.join(scene.OUT, "proj_depth.exr"))[..., 0]
dh, dw = depth.shape
sx, sy = dw / W, dh / H


def snap(x, y, r=7):
    ys, xs = np.nonzero(mask[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1])
    if len(xs) == 0:
        return float(x), float(y)
    return float(xs.mean() + max(0, x - r)), float(ys.mean() + max(0, y - r))


def depth_at(x, y, r=10):
    X, Y = int(x * sx), int(y * sy)
    win = depth[max(0, Y - r):Y + r + 1, max(0, X - r):X + r + 1]
    v = win[win > 0]
    return float(np.median(v)) if len(v) else None


scene.reset()
c = scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"])
bpy.context.view_layer.update()
mw = c.matrix_world.copy()
k = cam["focal"] / 36.0
xy, ds, last = [], [], None
for (x, y) in WAYPOINTS:
    x, y = snap(x, y)
    d = depth_at(x, y)
    if d is None:
        d = last
    last = d
    xy.append((x, y)); ds.append(d - 0.012)   # tubo por cima da superfície
# suaviza só a profundidade, ao longo dos raios: o tubo continua caindo sobre a foto
ds = np.array(ds)
for _ in range(3):
    ds[1:-1] = (ds[:-2] + 2 * ds[1:-1] + ds[2:]) / 4
pts = []
for (x, y), d in zip(xy, ds):
    u, v = x / W, 1 - y / H
    pc = Vector(((u - 0.5) / k * d, (v - 0.5) / (k * W / H) * d, -d))
    pts.append(list(mw @ pc))
# na região da ferramenta (esquerda da foto) o mapa pega superfícies do fundo: o tubo corre
# junto à ferramenta, então prendemos esses pontos ao plano lateral dela (x = TOOL_X)
TOOL_X = 0.03 * 0.30
cam_pos = mw.translation
for i, ((x, y), d) in enumerate(zip(xy, ds)):
    if x < 330:
        u, v = x / W, 1 - y / H
        ray = (mw.to_3x3() @ Vector(((u - 0.5) / k, (v - 0.5) / (k * W / H), -1.0))).normalized()
        t = (TOOL_X - cam_pos.x) / ray.x
        pts[i] = list(cam_pos + ray * t)
sm = np.array(pts)
json.dump(sm.tolist(), open(os.path.join(scene.OUT, "tube_path.json"), "w"), indent=1)
print("TUBE", len(sm), np.round(sm[[0, len(sm) // 2, -1]] / 0.3, 2).tolist())
