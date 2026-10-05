"""Renders do teste de viabilidade do modelo.

Uso: blender -b --factory-startup --python render_tests.py -- <modo> [samples]
Modos: master (pose do master, fundo transparente), turn (giro 35°), dark (interior escuro, luzes acesas)
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import scene, drone_model

argv = scene.args()
MODE = argv[0] if argv else "master"
SAMPLES = int(argv[1]) if len(argv) > 1 else 256
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
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Base Contrast"

_ga = os.path.join(scene.OUT, "guard_adj.json")
GADJ = {k: tuple(v) for k, v in json.load(open(_ga)).items()} if os.path.exists(_ga) else {}
root, p = drone_model.build({"s": cam["s"], "spoke_phase": cam["phase"], "guard_adj": GADJ})
D = p["D"]
M = drone_model.MAT


def area(name, loc, target, size, power, color=(1, 1, 1)):
    ld = bpy.data.lights.new(name, "AREA")
    ld.size = size
    ld.energy = power
    ld.color = color
    o = bpy.data.objects.new(name, ld)
    sc.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


def world(color, strength):
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*color, 1)
    bg.inputs["Strength"].default_value = strength


def cam_master():
    scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"])


def studio():
    # estúdio high-key como a foto do PDF: fundo branco, softbox grande em cima, rebatedor
    world((1, 1, 1), 0.22)
    area("key", (-0.6, 0.5, 1.4), (0, 0, 0), 1.6, 110)
    area("fill", (0.9, 0.9, 0.4), (0, 0, -0.05), 1.2, 25)
    area("rim", (0.5, -1.0, 0.6), (0, 0, 0.05), 0.8, 55)


def lights_on(power=14.0, spot_w=28.0):
    M["led"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 60.0
    for o in list(bpy.data.objects):
        if o.name.startswith("light_") and o.type == "MESH":
            mw = o.matrix_world
            fwd = (mw.to_3x3() @ Vector((0, 1, 0))).normalized()
            ld = bpy.data.lights.new("spot_" + o.name, "SPOT")
            ld.energy = spot_w
            ld.spot_size = math.radians(70)
            ld.spot_blend = 0.6
            ld.shadow_soft_size = 0.01
            ld.color = (1.0, 0.86, 0.66)
            s = bpy.data.objects.new("spot_" + o.name, ld)
            sc.collection.objects.link(s)
            s.location = mw.translation + fwd * 0.02
            s.rotation_euler = fwd.to_track_quat("-Z", "Y").to_euler()


if MODE == "master":
    studio()
    cam_master()
    sc.render.film_transparent = True
    scene.size(1000, 667)
    scene.render_to(os.path.join(scene.OUT, "test_01_master_pose.png"))

elif MODE == "turn":
    studio()
    cam_master()
    sc.render.film_transparent = True
    # giro de 35° em direção ao perfil esquerdo + inclinação de curva
    root.rotation_euler = (math.radians(0), math.radians(-7), math.radians(-35))
    scene.size(1000, 667)
    scene.render_to(os.path.join(scene.OUT, "test_02_turn35.png"))

elif MODE == "dark":
    import projection
    proj, proj_cam = projection.make_projector(root, cam)
    dpath = os.path.join(scene.OUT, "proj_depth_dark.exr")
    projection.render_depth(proj_cam, dpath)
    projection.apply_albedo([m for k, m in M.items() if k not in ("silhouette", "led")], proj, cam["focal"], dpath)
    world((0.004, 0.0045, 0.005), 1.0)
    sc.render.film_transparent = False
    # interior de tanque: casco cilíndrico de chapa com névoa leve
    R = 2.6
    bpy.ops.mesh.primitive_cylinder_add(vertices=160, radius=R, depth=4.0, location=(0, 0.2, 0.6))
    tank = bpy.context.active_object
    tank.name = "tank"
    mt = bpy.data.materials.new("steel_rust")
    mt.use_nodes = True
    nt = mt.node_tree
    b = nt.nodes["Principled BSDF"]
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 9.0
    noise.inputs["Detail"].default_value = 12.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.035, 0.03, 0.026, 1)
    ramp.color_ramp.elements[1].color = (0.16, 0.075, 0.035, 1)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.62
    b.inputs["Metallic"].default_value = 0.35
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.25
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    tank.data.materials.append(mt)
    # cordões de solda horizontais
    for z in (-0.6, 0.4, 1.4):
        bpy.ops.mesh.primitive_torus_add(major_radius=R - 0.005, minor_radius=0.012, location=(0, 0.2, z),
                                         major_segments=160)
        bpy.context.active_object.data.materials.append(mt)
    # névoa volumétrica
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, 0.6))
    fog = bpy.context.active_object
    fog.scale = (5.0, 5.0, 3.9)
    mf = bpy.data.materials.new("fog")
    mf.use_nodes = True
    nf = mf.node_tree
    nf.nodes.remove(nf.nodes["Principled BSDF"])
    vol = nf.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = 0.06
    vol.inputs["Anisotropy"].default_value = 0.35
    nf.links.new(vol.outputs["Volume"], nf.nodes["Material Output"].inputs["Volume"])
    fog.data.materials.append(mf)
    # drone em profundidade, levemente inclinado para frente, luzes acesas
    root.location = (0, 0.4, 0.15)
    root.rotation_euler = (math.radians(-5), 0, math.radians(-20))
    lights_on(spot_w=60.0)
    # luz fria muito fraca vinda da abertura acima (último fio de luz externa)
    area("hatch", (0.2, -0.4, 2.4), (0, 0.2, 0), 0.6, 18, color=(0.75, 0.85, 1.0))
    scene.camera(118, 12, 1.9, 40, (0.0, 0.42, 0.05), 0)
    sc.cycles.volume_step_rate = 2.0
    scene.size(1000, 667)
    scene.render_to(os.path.join(scene.OUT, "test_03_dark.png"))
