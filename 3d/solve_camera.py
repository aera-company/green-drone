"""Resolve a câmera do master a partir de pontos físicos (cubos e parafusos das proteções).
Projeção pinhole equivalente à câmera do Blender (sensor 36 mm, ajuste horizontal)."""
import json, math
import numpy as np
from scipy.optimize import least_squares

W, H = 1000, 667
D = 0.30
OBS = {
    "FL": {"hub": (510, 410), "screws": [(405, 342), (567, 310), (657, 415), (552, 532), (382, 472)], "c": (-1, 1)},
    "BL": {"hub": (732, 230), "screws": [(647, 192), (755, 177), (850, 240), (792, 310), (645, 282)], "c": (-1, -1)},
    "FR": {"hub": (305, 210), "screws": [(327, 161), (210, 195), (407, 194)], "c": (1, 1)},
}

def cam_basis(az, el, dist, tx, ty, tz, roll):
    a, e = math.radians(az), math.radians(el)
    t = np.array([tx, ty, tz])
    pos = t + dist * np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    f = t - pos; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    r2 = cr * r + sr * u; u2 = -sr * r + cr * u
    return pos, f, r2, u2

def project(P, cam):
    az, el, dist, focal, tx, ty, tz, roll = cam
    pos, f, r, u = cam_basis(az, el, dist, tx, ty, tz, roll)
    d = P - pos
    z = d @ f
    x = d @ r / z; y = d @ u / z
    k = focal / 36.0 * W
    return np.stack([W / 2 + x * k, H / 2 - y * k], -1)

def model_points(s, phase):
    out = {}
    rr = D / 2 - 0.035 * D / 2
    for g, o in OBS.items():
        cx, cy = o["c"][0] * s * D, o["c"][1] * s * D
        arm = math.atan2(-cy, -cx)
        ends = [(cx + rr * math.cos(arm + math.radians(phase) + k * math.pi / 3),
                 cy + rr * math.sin(arm + math.radians(phase) + k * math.pi / 3), 0.0) for k in range(6)]
        out[g] = (np.array([cx, cy, 0.0]), np.array(ends))
    return out

def residuals(x):
    cam, s, phase = x[:8], x[8], x[9]
    res = []
    mp = model_points(s, phase)
    for g, o in OBS.items():
        hub, ends = mp[g]
        ph = project(hub[None], cam)[0]
        res += list(ph - np.array(o["hub"]))
        pe = project(ends, cam)
        for sc in o["screws"]:
            dd = np.linalg.norm(pe - np.array(sc), axis=1)
            j = int(np.argmin(dd))
            res += list(pe[j] - np.array(sc))
    return np.array(res)

best = None
for az0 in (110, 125, 140, 155):
    for el0 in (25, 35, 45):
        for f0 in (35, 50, 70):
            x0 = [az0, el0, 1.3, f0, 0, 0, -0.03, 0, 0.62, 0]
            r = least_squares(residuals, x0, bounds=([60, 5, 0.4, 15, -.3, -.3, -.3, -20, 0.45, -30],
                                                     [200, 80, 5, 200, .3, .3, .3, 20, 1.0, 30]))
            if best is None or r.cost < best.cost:
                best = r
x = best.x
rms = math.sqrt(np.mean(residuals(x) ** 2))
names = ["az", "el", "dist", "focal", "tx", "ty", "tz", "roll", "s", "phase"]
sol = dict(zip(names, map(float, x)))
print("RMS px", round(rms, 2)); print({k: round(v, 3) for k, v in sol.items()})
json.dump({"cam": sol, "rms_px": rms}, open("renders/camera_solve.json", "w"), indent=1)
