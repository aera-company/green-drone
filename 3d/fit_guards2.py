"""Ajuste por proteção com IoU numa região, modelo inteiro presente (sem 'esconder' anéis no corpo)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, bpy
import scene, drone_model
cam = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]
W, H = 500, 333
ROI = {"FL": (350, 290, 680, 600), "BL": (615, 150, 885, 385), "FR": (150, 140, 420, 340), "BR": (420, 70, 670, 210)}
master = scene.load_alpha(os.path.join(scene.OUT, "master_alpha_500.png"))
tmp = os.path.join(scene.OUT, "_fg2.png")
scene.reset(); scene.workbench_silhouette(); scene.size(W, H)
adj = {k: tuple(v) for k, v in json.load(open(os.path.join(scene.OUT, "guard_adj.json"))).items()} if len(sys.argv) > 0 and "--" in sys.argv else {}
ONLY = scene.args()
def score(name, a):
    for o in list(bpy.data.objects):
        if o.type != "CAMERA":
            bpy.data.objects.remove(o, do_unlink=True)
    drone_model.MAT.clear()
    ad = dict(adj); ad[name] = tuple(a)
    drone_model.build({"s": cam["s"], "spoke_phase": 0.0, "guard_adj": ad, "tube_from_photo": True}, silhouette=True)
    scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"])
    scene.render_to(tmp)
    r = scene.load_alpha(tmp)
    x0, y0, x1, y1 = [v // 2 for v in ROI[name]]
    R = r[y0:y1, x0:x1]; M = master[y0:y1, x0:x1]
    return float(np.minimum(R, M).sum() / np.maximum(R, M).sum())
for name in (ONLY or ["FL", "BL", "FR", "BR"]):
    a = [0.0, 0.0, 0.0, 1.0, 0.18]
    st = [0.03, 0.03, 0.03, 0.03, 0.03]
    lo = [-0.15, -0.15, -0.15, 0.85, 0.08]; hi = [0.15, 0.15, 0.15, 1.15, 0.32]
    best = score(name, a); print(name, "INIT", round(best, 4), flush=True)
    for it in range(8):
        imp = False
        for i in range(5):
            for sg in (1, -1):
                t = list(a); t[i] = min(hi[i], max(lo[i], t[i] + sg * st[i]))
                v = score(name, t)
                if v > best + 1e-4:
                    best, a, imp = v, t, True
        if not imp:
            st = [x / 2 for x in st]
    adj[name] = tuple(round(x, 4) for x in a)
    print(name, "BEST", round(best, 4), adj[name], flush=True)
json.dump(adj, open(os.path.join(scene.OUT, "guard_adj.json"), "w"), indent=1)
print("DONE", flush=True)
