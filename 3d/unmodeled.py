"""Mapa do que a foto mostra e o modelo não tem (vermelho) e do que o modelo tem e a foto não (azul)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, bpy
import scene
def load(p):
    im = bpy.data.images.load(p, check_existing=False); w, h = im.size
    a = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(a); return a.reshape(h, w, 4)
d = load(os.path.join(scene.OUT, "proj_depth.exr"))[..., 0]
d = d[::2, ::2][:667, :1000] if d.shape[0] >= 1334 else d
photo = load(os.path.abspath(os.path.join(scene.HERE, "..", "public", "media", "drone-cutout.png")))
pa = photo[..., 3]
has = (d > 0).astype(np.float32)
out = np.ones((667, 1000, 4), dtype=np.float32)
gray = photo[..., :3].mean(-1) * 0.35 + 0.65
for c in range(3):
    out[..., c] = gray
miss = (pa > 0.5) & (has < 0.5)
extra = (pa < 0.2) & (has > 0.5)
out[miss] = (0.9, 0.1, 0.1, 1)
out[extra] = (0.1, 0.35, 0.95, 1)
print("MISSING px", int(miss.sum()), "of photo", int((pa > 0.5).sum()), " EXTRA px", int(extra.sum()))
img = bpy.data.images.new("um", 1000, 667, alpha=True)
img.pixels.foreach_set(out.ravel())
img.filepath_raw = os.path.join(scene.OUT, "_unmodeled.png"); img.file_format = "PNG"; img.save()
