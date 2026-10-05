"""Refina câmera + espaçamento das proteções por silhueta (IoU suavizado), partindo do solve por pontos."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import scene, drone_model

W, H = 500, 333
sol = json.load(open(os.path.join(scene.OUT, "camera_solve.json")))["cam"]

def blur(a, r=2):
    k = np.ones(2 * r + 1) / (2 * r + 1)
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)

master = blur(scene.load_alpha(os.path.join(scene.OUT, "master_alpha_500.png")))
tmp = os.path.join(scene.OUT, "_rf.png")
scene.reset()
scene.workbench_silhouette()
scene.size(W, H)
state = {"s": None}

def rebuild(s):
    if state["s"] == s:
        return
    for o in list(bpy.data.objects):
        if o.type != "CAMERA":
            bpy.data.objects.remove(o, do_unlink=True)
    drone_model.MAT.clear()
    drone_model.build({"s": s, "spoke_phase": sol["phase"]}, silhouette=True)
    state["s"] = s

def score(c):
    rebuild(round(c["s"], 4))
    scene.camera(c["az"], c["el"], c["dist"], c["focal"], (c["tx"], c["ty"], c["tz"]), c["roll"])
    scene.render_to(tmp)
    a = blur(scene.load_alpha(tmp))
    return np.minimum(a, master).sum() / np.maximum(a, master).sum()

c = {k: sol[k] for k in ["az", "el", "dist", "focal", "tx", "ty", "tz", "roll", "s"]}
steps = {"az": 2, "el": 2, "dist": 0.04, "focal": 2, "tx": 0.01, "ty": 0.01, "tz": 0.01, "roll": 1, "s": 0.02}
best = score(c)
print("INIT", round(best, 4), flush=True)
for it in range(14):
    improved = False
    for k in steps:
        for sgn in (1, -1):
            t = dict(c); t[k] += sgn * steps[k]
            v = score(t)
            if v > best + 1e-4:
                best, c, improved = v, t, True
    print("IT", it, round(best, 4), {k: round(v, 3) for k, v in c.items()}, flush=True)
    if not improved:
        steps = {k: v / 2 for k, v in steps.items()}
out = dict(sol); out.update(c)
json.dump({"cam": out, "iou": best}, open(os.path.join(scene.OUT, "camera_refined.json"), "w"), indent=1)
