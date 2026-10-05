"""Ajusta câmera para reproduzir a pose do master. Saída: renders/camera_fit.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import scene, drone_model

W, H = 300, 200
scene.reset()
root, p = drone_model.build(silhouette=True)
scene.workbench_silhouette()
scene.size(W, H)

def blur(a, r=2):
    k = np.ones(2 * r + 1) / (2 * r + 1)
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)

master = scene.load_alpha(os.path.join(scene.OUT, "master_alpha_small.png"))
# master_alpha_small tem só canal L salvo como RGBA? usamos luminância do alpha salvo
mb = blur(master)

tmp = os.path.join(scene.OUT, "_fit.png")
def score(c):
    scene.camera(c["az"], c["el"], c["dist"], c["focal"], (c["tx"], c["ty"], c["tz"]), c["roll"])
    scene.render_to(tmp)
    a = blur(scene.load_alpha(tmp))
    inter = np.minimum(a, mb).sum(); uni = np.maximum(a, mb).sum()
    return inter / uni

init = json.loads(scene.args()[0]) if scene.args() else {}
c = {"az": 135, "el": 35, "dist": 1.25, "focal": 50, "tx": 0.0, "ty": 0.03, "tz": -0.03, "roll": 0}
c.update(init)
steps = {"az": 8, "el": 6, "dist": 0.15, "focal": 10, "tx": 0.03, "ty": 0.03, "tz": 0.03, "roll": 4}
best = score(c)
print("INIT", best, flush=True)
for it in range(6):
    improved = False
    for k in steps:
        for sgn in (1, -1):
            t = dict(c); t[k] += sgn * steps[k]
            sc = score(t)
            if sc > best:
                best, c, improved = sc, t, True
                break
    print("IT", it, round(best, 4), {k: round(v, 3) for k, v in c.items()}, flush=True)
    if not improved:
        steps = {k: v / 2 for k, v in steps.items()}
json.dump({"cam": c, "score": best}, open(os.path.join(scene.OUT, "camera_fit.json"), "w"), indent=1)
