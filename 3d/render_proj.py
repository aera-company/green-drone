"""Testes da projeção da foto sobre o modelo.

Uso: blender -b --factory-startup --python render_proj.py -- <ângulos separados por vírgula> [samples] [residual 0/1]
Ex.: -- 0,10,20,35 128 1
Saída: renders/proj_yawXX.png (fundo transparente)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import scene, drone_model, projection

argv = scene.args()
ANGLES = [float(a) for a in (argv[0] if argv else "0").split(",")]
SAMPLES = int(argv[1]) if len(argv) > 1 else 128
RESIDUAL = (argv[2] != "0") if len(argv) > 2 else True
DEPTH_ONLY = len(argv) > 3 and argv[3] == "depthonly"   # mapa sem o tubo, para o trace_tube.py
cam = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]

scene.reset()
sc = bpy.context.scene
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "METAL"
sc.cycles.device = "GPU"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"

_ga = os.path.join(scene.OUT, "guard_adj.json")
GADJ = {k: tuple(v) for k, v in json.load(open(_ga)).items()} if os.path.exists(_ga) else {}
root, p = drone_model.build({"s": cam["s"], "spoke_phase": cam["phase"], "guard_adj": GADJ,
                            "tube_from_photo": not DEPTH_ONLY})
mats = [m for k, m in drone_model.MAT.items() if k != "silhouette"]

proj, proj_cam = projection.make_projector(root, cam)
depth_path = os.path.join(scene.OUT, "proj_depth.exr")
projection.render_depth(proj_cam, depth_path)
if DEPTH_ONLY:
    raise SystemExit(0)
projection.apply(mats, proj, cam["focal"], depth_path)
card = None
if RESIDUAL:
    card = projection.residual_shell(proj, cam["focal"], depth_path)

# estúdio claro (mesmo do teste anterior)
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.22
from mathutils import Vector
def area(name, loc, target, size, power):
    ld = bpy.data.lights.new(name, "AREA"); ld.size = size; ld.energy = power
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
area("key", (-0.6, 0.5, 1.4), (0, 0, 0), 1.6, 110)
area("fill", (0.9, 0.9, 0.4), (0, 0, -0.05), 1.2, 25)
area("rim", (0.5, -1.0, 0.6), (0, 0, 0.05), 0.8, 55)

scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"])
sc.render.film_transparent = True
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
scene.size(1000, 667)
SEQ = os.environ.get("SEQ_DIR")
if SEQ:
    os.makedirs(SEQ, exist_ok=True)
for fi, a in enumerate(ANGLES):
    # giro em torno do eixo vertical do drone + inclinação de curva proporcional
    root.rotation_euler = (0, math.radians(-7 * min(1, abs(a) / 35)), math.radians(-a))
    # a casca de resíduo só vale perto da pose da foto; some até 12° de giro
    projection.set_shell(max(0.0, 1.0 - abs(a) / 12.0))
    sc.frame_set(sc.frame_current)   # reavalia os drivers da máscara de ângulo
    tag = (f"{int(a):02d}" if float(a).is_integer() else f"{a:05.2f}") + ("" if RESIDUAL else "_nores")
    scene.render_to(os.path.join(SEQ, f"f{fi:04d}.png") if SEQ else os.path.join(scene.OUT, f"proj_yaw{tag}.png"))
