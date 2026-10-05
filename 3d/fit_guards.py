"""Ajuste fino de cada proteção contra a foto (precisão da silhueta), com câmera fixa."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bpy
import scene, drone_model

cam = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]
W, H = 1000, 667
def blur(a, r=1):
    k = np.ones(2 * r + 1) / (2 * r + 1)
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)
master = scene.load_alpha(os.path.join(scene.OUT, "master_alpha_full.png"))
mb = np.clip(blur(master, 1) * 1.3, 0, 1)
tmp = os.path.join(scene.OUT, "_fg.png")
scene.reset(); scene.workbench_silhouette(); scene.size(W, H)
adj = {}
def build_and_score(name, a):
    for o in list(bpy.data.objects):
        if o.type != "CAMERA":
            bpy.data.objects.remove(o, do_unlink=True)
    drone_model.MAT.clear()
    adj2 = dict(adj); adj2[name] = tuple(a)
    drone_model.build({"s": cam["s"], "spoke_phase": 0.0, "guard_adj": adj2, "rods": False}, silhouette=True)
    g = bpy.data.objects[f"guard_{name}"]
    keep = set(o.name for o in g.children_recursive)
    for o in bpy.data.objects:
        if o.type in ("MESH", "CURVE"):
            o.hide_render = o.name not in keep or o.name.startswith(("motor", "blade", "light", "led", "lens", "rod"))
    scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"])
    scene.render_to(tmp)
    r = scene.load_alpha(tmp)
    return float((r * mb).sum() / max(r.sum(), 1))
for name in ["FL", "BL", "FR", "BR"]:
    a = [0.0, 0.0, 0.0, 1.0, 0.18]
    steps = [0.02, 0.02, 0.02, 0.02, 0.02]
    lo = [-0.12, -0.12, -0.12, 0.9, 0.12]; hi = [0.12, 0.12, 0.12, 1.1, 0.26]
    best = build_and_score(name, a)
    print(name, "INIT", round(best, 4), flush=True)
    for it in range(10):
        imp = False
        for i in range(5):
            for sg in (1, -1):
                t = list(a); t[i] = min(hi[i], max(lo[i], t[i] + sg * steps[i]))
                v = build_and_score(name, t)
                if v > best + 1e-4:
                    best, a, imp = v, t, True
        if not imp:
            steps = [x / 2 for x in steps]
    adj[name] = tuple(round(x, 4) for x in a)
    print(name, "BEST", round(best, 4), adj[name], flush=True)
json.dump(adj, open(os.path.join(scene.OUT, "guard_adj.json"), "w"), indent=1)
