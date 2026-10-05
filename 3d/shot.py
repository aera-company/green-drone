"""PASS 01 · Motion proof: REVEAL → APPROACH → TURN → ENTRY → DARK, uma tomada contínua.

Uso:
  blender -b --factory-startup --python shot.py -- <formato> <frames> <samples> <saida>
  formato: desktop (1600x900) | mobile (720x1280) | preview (800x450)
  frames:  "0-159" ou "0,20,40"
Status: MOTION_SIMULATION. Drone reconstruído + foto projetada; ambiente modelado (não é operação real).
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Euler
import scene, drone_model, projection

argv = scene.args()
FMT = argv[0] if argv else "preview"
FR = argv[1] if len(argv) > 1 else "0,24,56,88,104,118,132,159"
SAMPLES = int(argv[2]) if len(argv) > 2 else 16
OUTDIR = argv[3] if len(argv) > 3 else os.path.join(scene.OUT, "shot_" + FMT)
os.makedirs(OUTDIR, exist_ok=True)
frames = []
for part in FR.split(","):
    if "-" in part:
        a, b = part.split("-"); frames += list(range(int(a), int(b) + 1))
    else:
        frames.append(int(part))

cam = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]
_ga = os.path.join(scene.OUT, "guard_adj.json")
GADJ = {k: tuple(v) for k, v in json.load(open(_ga)).items()} if os.path.exists(_ga) else {}

scene.reset()
sc = bpy.context.scene
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "METAL"
sc.cycles.device = "GPU"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.frame_start, sc.frame_end = 0, 159
sc.render.fps = 24

# ------------------------------------------------------------------ drone + projeção (na pose da foto)
root, p = drone_model.build({"s": cam["s"], "spoke_phase": cam["phase"], "guard_adj": GADJ})
M = drone_model.MAT
proj, proj_cam = projection.make_projector(root, cam)
dpath = os.path.join(scene.OUT, "proj_depth_shot.exr")
projection.render_depth(proj_cam, dpath)
lit = [m for k, m in M.items() if k not in ("silhouette", "led", "prop")]
projection.apply_albedo(lit, proj, cam["focal"], dpath, strength=0.75)
projection.apply(lit, proj, cam["focal"], dpath)
bpy.data.objects.remove(proj_cam, do_unlink=True)

# ------------------------------------------------------------------ coreografia
F_REVEAL, F_APPROACH, F_TURN, F_ENTRY, F_END = 24, 56, 88, 124, 159
YAW_TURN = -40.0
fwd = Vector((math.sin(math.radians(-YAW_TURN)), math.cos(math.radians(-YAW_TURN)), 0))   # frente após o giro
WALL_S = 3.4
D = p["D"]

def smooth(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

def interp(keys, f):
    """keys: lista (frame, valor ou tupla); interpolação suave entre chaves."""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            t = smooth((f - f0) / (f1 - f0))
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * t for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * t
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]

# drone: avanço ao longo da frente (s), altura, giro e inclinação
K_S = [(0, 0.0), (F_TURN, 0.15), (104, 1.8), (116, 3.2), (124, 3.75), (136, 4.3), (F_END, 4.9)]
K_Z = [(0, 0.0), (F_TURN, 0.02), (118, -0.04), (F_END, -0.12)]
K_YAW = [(0, 0.0), (F_APPROACH, 0.0), (F_TURN, YAW_TURN), (F_END, YAW_TURN - 6)]
K_BANK = [(0, 0.0), (F_APPROACH, 0.0), (72, 9.0), (F_TURN, 3.0), (110, -4.0), (136, 0.0), (F_END, 0.0)]
K_PITCH = [(0, 0.0), (F_TURN, 0.0), (100, 7.0), (124, 4.0), (F_END, 1.0)]   # inclina para frente ao acelerar

# câmera: azimute/elevação/distância em torno do drone, alvo relativo, deslocamento de lente
MA = cam["az"]; ME = cam["el"]; MD = cam["dist"]
K_CAM = [
    (0,          (MA, ME, MD * 1.55, 0.0, -0.20)),
    (F_REVEAL,   (MA, ME, MD * 1.48, 0.0, -0.20)),
    (F_APPROACH, (MA - 2, ME - 5, MD * 0.86, 0.0, -0.05)),
    (F_TURN,     (MA + 10, ME - 13, MD * 1.18, 0.0, 0.0)),
    (104,        (MA + 20, ME - 22, MD * 1.50, 0.0, 0.0)),   # abre: antepara inteira de lado
    (116,        (MA + 28, ME - 34, MD * 2.10, 0.0, 0.0)),   # câmera ao lado da chapa: drone some atrás dela
    (124,        (MA + 55, ME - 34, MD * 1.55, 0.0, 0.0)),   # contorna; drone reaparece no fundo pela abertura
    (136,        (MA + 88, ME - 34, MD * 0.98, 0.0, 0.0)),   # atravessa a abertura
    (F_END,      (MA + 80, ME - 36, MD * 1.30, 0.0, 0.0)),
]
if FMT == "mobile":
    # quadro vertical: mesmo trajeto do desktop (a abertura precisa ser lida de frente);
    # câmera um pouco mais longe e deslocamento vertical de lente para o texto
    DIST = [1.62, 1.55, 1.12, 1.45, 1.65, 2.1, 1.55, 1.0, 1.3]
    SHY = [0.17, 0.17, 0.06, 0.10, 0.06, 0.0, 0.0, 0.0, 0.0]
    K_CAM = [(f, (v[0], v[1], MD * DIST[i], 0.0, SHY[i])) for i, (f, v) in enumerate(K_CAM)]
TGT = Vector((cam["tx"], cam["ty"], cam["tz"]))   # alvo da foto (relativo ao drone)

def drone_pos(f):
    return fwd * interp(K_S, f) + Vector((0, 0, interp(K_Z, f)))

SIDE = Vector((fwd.y, -fwd.x, 0))
F_SWITCH = 104
# ENTRY por posições explícitas (s ao longo do voo, lateral, altura): câmera rente à chapa,
# ao lado da abertura, para o drone sumir atrás da borda e reaparecer no fundo.
K_ENTRY = [(112, (2.85, -1.75, 0.22)), (118, (3.04, -1.68, 0.18)), (122, (3.02, -1.35, 0.15)),
           (128, (2.72, -0.45, 0.12)), (136, (3.42, -0.12, 0.08)), (F_END, (3.78, 0.12, 0.10))]

if FMT == "mobile":
    K_ENTRY = [(112, (2.85, -1.75, 0.22)), (118, (3.04, -1.68, 0.18)), (122, (3.02, -1.35, 0.15)),
               (128, (2.62, -0.45, 0.14)), (136, (3.30, -0.10, 0.12)), (F_END, (3.48, 0.08, 0.14))]

def _orbit(f):
    az, el, dist, _, shift = interp(K_CAM, f)
    t = drone_pos(f) + TGT
    a, e = math.radians(az), math.radians(el)
    return t + Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist, t, shift

def cam_pose(f):
    if f <= F_SWITCH:
        return _orbit(f)
    p0, _, shift0 = _orbit(F_SWITCH)
    k0 = (F_SWITCH, (p0.dot(fwd), p0.dot(SIDE), p0.z))
    sv, lv, zv = interp([k0] + K_ENTRY, f)
    pos = fwd * sv + SIDE * lv + Vector((0, 0, zv))
    return pos, drone_pos(f) + TGT, interp([(F_SWITCH, shift0), (120, 0.0)], f)

# ------------------------------------------------------------------ ambiente
def mat_principled(name, color, rough, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m

def noisy(m, scale, c0, c1, bump=0.2):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = 10
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].color = (*c0, 1); r.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump
    nt.links.new(n.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

# antepara externa: aço pintado claro (combina com a abertura clara), interior: aço escuro oxidado
paint = noisy(mat_principled("paint", (0.42, 0.44, 0.43), 0.6, 0.0), 2.2, (0.30, 0.31, 0.30), (0.47, 0.49, 0.48), 0.08)
rust = noisy(mat_principled("rust", (0.05, 0.04, 0.035), 0.65, 0.3), 6.0, (0.025, 0.022, 0.02), (0.12, 0.06, 0.03), 0.3)

def oriented_box(name, center_s, lateral, z, size, mat):
    """Caixa alinhada à frente do voo: size = (lateral, profundidade ao longo de fwd, altura)."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object; o.name = name
    o.scale = size
    side = Vector((fwd.y, -fwd.x, 0))
    o.location = fwd * center_s + side * lateral + Vector((0, 0, z))
    o.rotation_euler = (0, 0, math.atan2(-fwd.x, fwd.y))
    if mat:
        o.data.materials.append(mat)
    return o

OW, OH, OZ = 1.30, 1.00, 0.02          # abertura (m) e altura do centro
T = 0.06                               # espessura da antepara
BIG_W, BIG_H = 9.0, 6.0
# antepara em 4 peças em volta da abertura; curta do lado oposto à câmera (fica fora do quadro no REVEAL)
NEAR_W, FAR_W = 1.6, 0.6
TOPZ, BOTZ = 3.3, -1.15
oriented_box("wall_L", WALL_S, -(OW / 2 + NEAR_W / 2), (TOPZ + BOTZ) / 2, (NEAR_W, T, TOPZ - BOTZ), paint)
oriented_box("wall_R", WALL_S, (OW / 2 + FAR_W / 2), (TOPZ + BOTZ) / 2, (FAR_W, T, TOPZ - BOTZ), paint)
oriented_box("wall_T", WALL_S, 0, (OZ + OH / 2 + TOPZ) / 2, (OW, T, TOPZ - (OZ + OH / 2)), paint)
oriented_box("wall_B", WALL_S, 0, (OZ - OH / 2 + BOTZ) / 2, (OW, T, (OZ - OH / 2) - BOTZ), paint)
# cordões de solda e emendas de chapa (lado externo)
seam = mat_principled("seam", (0.22, 0.22, 0.21), 0.7, 0.2)
for z in (-1.3, 1.25, 2.6):
    oriented_box(f"seam_h_{z}", WALL_S - T / 2 - 0.006, -(NEAR_W - FAR_W) / 2, z, (NEAR_W + FAR_W + OW, 0.012, 0.025), seam)
for lat in (-1.5, -2.0):
    oriented_box(f"seam_v_{lat}", WALL_S - T / 2 - 0.006, lat, 0.5, (0.025, 0.012, BIG_H), seam)
# placa de identificação lisa ao lado da abertura (sem texto)
oriented_box("plate", WALL_S - T / 2 - 0.01, -OW / 2 - 0.45, OZ + 0.25, (0.32, 0.01, 0.2), seam)
# moldura reforçada da abertura (perfil em L), escurecida pelo uso
frame_m = noisy(mat_principled("frame", (0.3, 0.3, 0.3), 0.5, 0.4), 8.0, (0.18, 0.18, 0.17), (0.32, 0.30, 0.27), 0.15)
for nm, lat, z, sz in [("fr_L", -OW / 2 - 0.04, OZ, (0.08, 0.16, OH + 0.16)), ("fr_R", OW / 2 + 0.04, OZ, (0.08, 0.16, OH + 0.16)),
                       ("fr_T", 0, OZ + OH / 2 + 0.04, (OW + 0.16, 0.16, 0.08)), ("fr_B", 0, OZ - OH / 2 - 0.04, (OW + 0.16, 0.16, 0.08))]:
    oriented_box(nm, WALL_S, lat, z, sz, frame_m)
# interior do tanque
DEPTH = 7.0
TW = 2.4
oriented_box("tank_floor", WALL_S + DEPTH / 2, 0, -1.12, (TW, DEPTH, 0.05), rust)
oriented_box("tank_ceil", WALL_S + DEPTH / 2, 0, 3.2, (TW, DEPTH, 0.05), rust)
oriented_box("tank_back", WALL_S + DEPTH, 0, 1.075, (TW, 0.05, 4.45), rust)
oriented_box("tank_L", WALL_S + DEPTH / 2, -TW / 2, 1.075, (0.05, DEPTH, 4.45), rust)
oriented_box("tank_R", WALL_S + DEPTH / 2, TW / 2, 1.075, (0.05, DEPTH, 4.45), rust)
# reforços verticais (cavernas) dentro do tanque
for i in range(6):
    oriented_box(f"rib_{i}", WALL_S + 1.0 + i * 1.0, -TW / 2 + 0.09, 1.075, (0.18, 0.08, 4.45), rust)
    oriented_box(f"ribr_{i}", WALL_S + 1.0 + i * 1.0, TW / 2 - 0.09, 1.075, (0.18, 0.08, 4.45), rust)
# névoa só dentro
fog = oriented_box("fog", WALL_S + DEPTH / 2 + 0.05, 0, 1.075, (TW - 0.1, DEPTH - 0.1, 4.3), None)
mf = bpy.data.materials.new("fog"); mf.use_nodes = True
nf = mf.node_tree; nf.nodes.remove(nf.nodes["Principled BSDF"])
vol = nf.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 0.14; vol.inputs["Anisotropy"].default_value = 0.4
nf.links.new(vol.outputs["Volume"], nf.nodes["Material Output"].inputs["Volume"])
fog.data.materials.append(mf)
fog.visible_shadow = False

# mundo: fundo #F7F7F8 para raios de câmera, ambiente suave para iluminação
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
bg.inputs["Strength"].default_value = 0.22
lp = nt.nodes.new("ShaderNodeLightPath")
bg2 = nt.nodes.new("ShaderNodeBackground")
srgb = 0.930   # #F7F7F8 em linear ~0.930
bg2.inputs["Color"].default_value = (0.930, 0.930, 0.937, 1); bg2.inputs["Strength"].default_value = 1.0
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
nt.links.new(bg.outputs[0], mx.inputs[1]); nt.links.new(bg2.outputs[0], mx.inputs[2])
nt.links.new(mx.outputs[0], nt.nodes["World Output"].inputs["Surface"])

def area(name, loc, target, size, power, color=(1, 1, 1)):
    ld = bpy.data.lights.new(name, "AREA"); ld.size = size; ld.energy = power; ld.color = color
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o
area("key", (-0.6, 0.5, 1.4), (0, 0, 0), 1.6, 110)
area("fill", (0.9, 0.9, 0.4), (0, 0, -0.05), 1.2, 25)
area("rim", (0.5, -1.0, 0.6), (0, 0, 0.05), 0.8, 55)
# luz de serviço fria e fraca dentro do tanque (último fio de luz pela abertura)
area("spill", tuple(fwd * (WALL_S + 0.3) + Vector((0, 0, 1.6))), tuple(fwd * (WALL_S + 1.2) + Vector((0, 0, -1.6))), 0.8, 6,
     color=(0.8, 0.88, 1.0))

# lanternas: spots presos aos módulos de luz, apontando para a frente do voo
spots = []
for o in list(bpy.data.objects):
    if o.name.startswith("light_") and o.type == "MESH" and not o.name.startswith("light_post"):
        ld = bpy.data.lights.new("spot_" + o.name, "SPOT")
        ld.spot_size = math.radians(55); ld.spot_blend = 0.5; ld.shadow_soft_size = 0.015
        ld.color = (1.0, 0.88, 0.72); ld.energy = 0.0
        s = bpy.data.objects.new("spot_" + o.name, ld); sc.collection.objects.link(s)
        s.parent = root
        bpy.context.view_layer.update()
        s.location = o.matrix_world.translation + Vector((0, 0.03, 0))
        s.rotation_euler = Vector((0, 1, -0.12)).to_track_quat("-Z", "Y").to_euler()   # frente do drone (+Y local)
        spots.append(s)
led_em = M["led"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]

# câmera
cd = bpy.data.cameras.new("CAM"); camo = bpy.data.objects.new("CAM", cd); sc.collection.objects.link(camo)
sc.camera = camo
cd.lens = cam["focal"]; cd.sensor_width = 36
cd.dof.use_dof = True
cd.dof.aperture_fstop = 4.0

# hélices: giro rápido por quadro (com motion blur viram disco)
props = [o for o in bpy.data.objects if o.name.startswith("prop_")]
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.5

# ------------------------------------------------------------------ chaves por quadro
K_PROJ = [(0, 1.0), (106, 1.0), (124, 0.0), (F_END, 0.0)]           # foto como emissão só na luz de fora
K_LAMP = [(0, 0.0), (117, 0.0), (126, 1.0), (F_END, 1.0)]
K_FSTOP = [(0, 5.6), (F_APPROACH, 2.8), (F_TURN, 4.0), (132, 2.8), (F_END, 2.2)]
proj_nodes = [m.node_tree.nodes["proj_amount"].outputs[0] for m in lit if "proj_amount" in m.node_tree.nodes]

for f in range(0, F_END + 1):
    # voo pairando: oscilação lenta e irregular, mínima
    hov = Vector((0.004 * math.sin(f * 0.21), 0.003 * math.sin(f * 0.17 + 1.3), 0.006 * math.sin(f * 0.26 + 0.4)))
    root.location = drone_pos(f) + hov
    root.rotation_euler = Euler((math.radians(interp(K_PITCH, f) + 0.4 * math.sin(f * 0.19)),
                                 math.radians(-interp(K_BANK, f) + 0.5 * math.sin(f * 0.23 + 2)),
                                 math.radians(interp(K_YAW, f))), "XYZ")
    root.keyframe_insert("location", frame=f); root.keyframe_insert("rotation_euler", frame=f)
    pos, tgt, shift = cam_pose(f)
    camo.location = pos
    camo.rotation_euler = (tgt - pos).to_track_quat("-Z", "Y").to_euler()
    camo.keyframe_insert("location", frame=f); camo.keyframe_insert("rotation_euler", frame=f)
    if FMT == "mobile":
        cd.shift_y = shift; cd.keyframe_insert("shift_y", frame=f)
    else:
        cd.shift_x = shift; cd.keyframe_insert("shift_x", frame=f)
    cd.dof.focus_distance = (drone_pos(f) - pos).length
    cd.dof.aperture_fstop = interp(K_FSTOP, f)
    cd.dof.keyframe_insert("focus_distance", frame=f); cd.dof.keyframe_insert("aperture_fstop", frame=f)
    for pr in props:
        pr.rotation_euler.z += math.radians(57)
        pr.keyframe_insert("rotation_euler", frame=f)
    for n in proj_nodes:
        n.default_value = interp(K_PROJ, f); n.keyframe_insert("default_value", frame=f)
    lamp = interp(K_LAMP, f)
    for s in spots:
        s.data.energy = 140.0 * lamp; s.data.keyframe_insert("energy", frame=f)
    led_em.default_value = 60.0 * lamp; led_em.keyframe_insert("default_value", frame=f)

for o in [root, camo] + props:
    if o.animation_data and o.animation_data.action:
        for fc in getattr(o.animation_data.action, "fcurves", []):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"

# ------------------------------------------------------------------ render
RES = {"desktop": (1280, 720), "mobile": (720, 1280), "preview": (800, 450)}[FMT]
scene.size(*RES)
sc.render.film_transparent = False
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.volume_step_rate = 2.0
sc.render.image_settings.file_format = "PNG"
for f in frames:
    sc.frame_set(f)
    scene.render_to(os.path.join(OUTDIR, f"f{f:04d}.png"))
print("SHOT_DONE", len(frames), flush=True)
