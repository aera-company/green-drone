"""Modelo paramétrico do drone protagonista (p04_drone_recortado_x139).

Reconstrução a partir de fotos. Status: MOTION_SIMULATION até validação da Gávea.
Unidades: D = diâmetro externo da proteção. Tudo é multiplicado por P["D"] (m).
Eixos: +Y = frente do drone (direção da ferramenta), +X = direita, +Z = cima.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

P = {
    "D": 0.30,            # diâmetro externo da proteção em metros (REQUIRES_GAVEA_VALIDATION)
    "s": 0.665,            # deslocamento do centro de cada proteção em X e Y (D)
    "ring_w": 0.035,      # largura radial do anel
    "ring_t": 0.010,      # espessura do anel
    "cage_h": 0.18,       # distância entre anel superior e inferior
    "spokes": 6,
    "spoke_phase": 0.0,   # rotação dos raios (graus) relativa ao braço
    "spoke_w": 0.028,
    "arm_w": 0.10,
    "body": (0.50, 0.90, 0.50),   # largura X, profundidade Y, altura Z
    "body_top": -0.015,
    "lidar_r": 0.12,
    "lidar_h": 0.21,
    "lidar_pos": (-0.02, -0.60, 0.45),
    "lidar_tilt": 38.0,   # graus, topo inclinado para trás
    "tool_reach": 1.30,   # Y da ponta da ferramenta
    "rods": True,
    "guard_adj": {},      # ajuste fino por proteção: nome -> (dx, dy, dz, escala_raio, cage_h)
}

MAT = {}


# ---------------------------------------------------------------- materiais

def _principled(name, color, rough, metal=0.0, coat=0.0, trans=0.0, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = trans
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


def _carbon():
    m = _principled("carbon", (0.02, 0.02, 0.022), 0.32, coat=0.15)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(45))
    mp.inputs["Scale"].default_value = (260, 260, 260)
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Color1"].default_value = (0.03, 0.03, 0.033, 1)
    br.inputs["Color2"].default_value = (0.012, 0.012, 0.014, 1)
    br.inputs["Mortar Size"].default_value = 0.0
    br.offset = 0.5
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.08
    nt.links.new(br.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def materials():
    if MAT:
        return MAT
    MAT["carbon"] = _carbon()
    MAT["plastic"] = _principled("plastic_black", (0.008, 0.008, 0.009), 0.5)
    MAT["rubber"] = _principled("rubber", (0.01, 0.01, 0.01), 0.8)
    MAT["alu"] = _principled("alu", (0.75, 0.75, 0.76), 0.25, metal=1.0)
    MAT["white"] = _principled("white_plastic", (0.85, 0.85, 0.84), 0.35)
    MAT["lidar_glass"] = _principled("lidar_glass", (0.01, 0.01, 0.012), 0.08, coat=1.0)
    MAT["red"] = _principled("red_anod", (0.55, 0.03, 0.03), 0.3, metal=0.6)
    MAT["blue_anod"] = _principled("blue_anod", (0.03, 0.12, 0.6), 0.3, metal=0.6)
    MAT["tube"] = _principled("tube_blue", (0.05, 0.35, 0.95), 0.12, trans=0.55)
    MAT["led"] = _principled("led", (1, 0.9, 0.6), 0.2, emit=(1, 0.86, 0.6), emit_strength=0.0)
    MAT["prop"] = _principled("prop", (0.01, 0.01, 0.011), 0.35)
    MAT["silhouette"] = _principled("silhouette", (1, 1, 1), 1.0)
    return MAT


# ---------------------------------------------------------------- geometria

def _obj(name, mesh, mat, parent):
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    if mat:
        o.data.materials.append(mat)
    o.parent = parent
    return o


def annulus(name, r_out, r_in, t, z, parent, mat, segs=96, center=(0, 0)):
    bm = bmesh.new()
    cx, cy = center
    outer_b, inner_b, outer_t, inner_t = [], [], [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        c, s = math.cos(a), math.sin(a)
        outer_b.append(bm.verts.new((cx + r_out * c, cy + r_out * s, z - t / 2)))
        inner_b.append(bm.verts.new((cx + r_in * c, cy + r_in * s, z - t / 2)))
        outer_t.append(bm.verts.new((cx + r_out * c, cy + r_out * s, z + t / 2)))
        inner_t.append(bm.verts.new((cx + r_in * c, cy + r_in * s, z + t / 2)))
    for i in range(segs):
        j = (i + 1) % segs
        bm.faces.new((outer_t[i], outer_t[j], inner_t[j], inner_t[i]))
        bm.faces.new((outer_b[j], outer_b[i], inner_b[i], inner_b[j]))
        bm.faces.new((outer_b[i], outer_b[j], outer_t[j], outer_t[i]))
        bm.faces.new((inner_b[j], inner_b[i], inner_t[i], inner_t[j]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _obj(name, me, mat, parent)


def plate(name, pts, t, parent, mat, z=0.0):
    """Placa extrudada a partir de polígono 2D (x, y) no plano z."""
    bm = bmesh.new()
    vb = [bm.verts.new((x, y, z - t / 2)) for x, y in pts]
    vt = [bm.verts.new((x, y, z + t / 2)) for x, y in pts]
    bm.faces.new(vt)
    bm.faces.new(list(reversed(vb)))
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((vb[i], vb[j], vt[j], vt[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return _obj(name, me, mat, parent)


def box(name, center, size, parent, mat, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = _obj(name, me, mat, parent)
    o.location = center
    o.rotation_euler = [math.radians(r) for r in rot]
    return o


def bar(name, p1, p2, w, h, parent, mat, up=(0, 0, 1)):
    """Barra retangular de p1 a p2. w = largura (perpendicular a 'up'), h = altura (ao longo de 'up')."""
    p1, p2, up = Vector(p1), Vector(p2), Vector(up)
    d = p2 - p1
    L = d.length
    x = d.normalized()
    z = (up - up.dot(x) * x)
    if z.length < 1e-6:
        z = Vector((0, 0, 1)) if abs(x.z) < 0.9 else Vector((1, 0, 0))
        z = (z - z.dot(x) * x)
    z.normalize()
    y = z.cross(x)
    o = box(name, (0, 0, 0), (L, w, h), parent, mat)
    m = Matrix((x, y, z)).transposed().to_4x4()
    m.translation = (p1 + p2) / 2
    o.matrix_basis = m
    return o


def cyl(name, p1, p2, r, parent, mat, segs=48):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=d.length)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = _obj(name, me, mat, parent)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    o.matrix_basis = Matrix.Translation((p1 + p2) / 2) @ q.to_matrix().to_4x4()
    for f in o.data.polygons:
        f.use_smooth = abs(f.normal.z) < 0.5
    return o


def tube(name, points, r, parent, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    cu.bevel_resolution = 6
    cu.resolution_u = 24
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(points) - 1)
    for bp, p in zip(sp.bezier_points, points):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    o.parent = parent
    return o


# ---------------------------------------------------------------- partes

def guard(idx, cx, cy, root, p, with_light=False, light_dir=None):
    D = p["D"]
    adj = p["guard_adj"].get(idx, (0, 0, 0, 1.0, p["cage_h"]))
    p = dict(p)
    p["cage_h"] = adj[4]
    cx, cy = cx + adj[0] * D, cy + adj[1] * D
    M = materials()
    g = bpy.data.objects.new(f"guard_{idx}", None)
    bpy.context.collection.objects.link(g)
    g.parent = root
    g.location = (cx, cy, adj[2] * D)
    R = D / 2 * adj[3]
    rw, rt, ch = p["ring_w"] * D, p["ring_t"] * D, p["cage_h"] * D
    annulus(f"ring_top_{idx}", R, R - rw, rt, 0, g, M["carbon"])
    annulus(f"ring_bot_{idx}", R, R - rw, rt, -ch, g, M["carbon"])
    # direção do braço (aponta para o centro do drone)
    arm_ang = math.atan2(-cy, -cx)
    hub_r = 0.07 * D
    cyl(f"hub_{idx}", (0, 0, -rt / 2), (0, 0, rt / 2), hub_r, g, M["carbon"])
    n = p["spokes"]
    rr = R - rw / 2
    for k in range(n):
        a = arm_ang + math.radians(p["spoke_phase"]) + 2 * math.pi * k / n
        c, s = math.cos(a), math.sin(a)
        if k != 0:
            bar(f"spoke_{idx}_{k}", (c * hub_r * 0.6, s * hub_r * 0.6, 0), (c * rr, s * rr, 0),
                p["spoke_w"] * D, rt, g, M["carbon"])
        # poste vertical na ponta de cada raio
        pc = (c * rr, s * rr)
        bar(f"post_{idx}_{k}", (pc[0], pc[1], -ch), (pc[0], pc[1], 0), 0.016 * D, 0.016 * D, g,
            M["carbon"], up=(c, s, 0))
        # parafuso
        cyl(f"screw_{idx}_{k}", (pc[0], pc[1], rt / 2), (pc[0], pc[1], rt / 2 + 0.008 * D), 0.011 * D, g, M["alu"])
    # estrela de raios também no anel inferior (vista através da gaiola na foto)
    cyl(f"hub_bot_{idx}", (0, 0, -ch - rt / 2), (0, 0, -ch + rt / 2), hub_r * 0.8, g, M["carbon"])
    for k in range(n):
        a = arm_ang + math.radians(p["spoke_phase"]) + 2 * math.pi * k / n
        c, s_ = math.cos(a), math.sin(a)
        bar(f"spoke_bot_{idx}_{k}", (c * hub_r * 0.5, s_ * hub_r * 0.5, -ch), (c * rr, s_ * rr, -ch),
            p["spoke_w"] * D * 0.9, rt, g, M["carbon"])
    # motor invertido + hélice
    cyl(f"motor_{idx}", (0, 0, -rt / 2), (0, 0, -0.075 * D), 0.05 * D, g, M["plastic"])
    prop = bpy.data.objects.new(f"prop_{idx}", None)
    bpy.context.collection.objects.link(prop)
    prop.parent = g
    prop.location = (0, 0, -0.088 * D)
    for side in (1, -1):
        b = bar(f"blade_{idx}_{side}", (0, 0, 0), (side * 0.43 * D, 0, 0), 0.07 * D, 0.006 * D, prop, M["prop"])
        b.rotation_euler.x = math.radians(14 * side)
    # ângulo das pás medido na foto (FL, BL); FR e BR não aparecem, ângulo arbitrário
    PROP = {"FL": 126.0, "BL": 162.0, "FR": 77.0, "BR": 171.0}
    prop.rotation_euler.z = math.radians(PROP[idx])
    # varetas diagonais para baixo (estrutura inferior)
    if p["rods"]:
        out = math.atan2(cy, cx)
        for da in (-50, 50):
            a = out + math.radians(da)
            bar(f"rod_{idx}_{da}", (math.cos(a) * rr, math.sin(a) * rr, -ch),
                (-cx * 0.85, -cy * 0.85, -0.60 * D), 0.008 * D, 0.008 * D, g, M["carbon"])
    if with_light:
        # posição medida na foto: (ângulo em graus no anel, altura em D)
        LIGHT = {"FL": (132.8, -0.253), "FR": (32.8, -0.024)}
        ang, lz = LIGHT.get(idx, (math.degrees(math.atan2(light_dir[1], light_dir[0])), -0.09))
        a = math.radians(ang)
        lp = (math.cos(a) * (R + 0.02 * D), math.sin(a) * (R + 0.02 * D), lz * D - adj[2] * D)
        lm = box(f"light_{idx}", lp, (0.10 * D, 0.08 * D, 0.10 * D), g, M["red"], rot=(0, 0, math.degrees(a) - 90))
        if lz * D < -ch:   # suporte até o anel inferior quando a luz fica pendurada
            bar(f"light_post_{idx}", (math.cos(a) * (R - rw / 2), math.sin(a) * (R - rw / 2), -ch),
                (lp[0], lp[1], lp[2] + 0.04 * D), 0.03 * D, 0.012 * D, g, M["carbon"])
        box(f"led_{idx}", (0, 0.041 * D, 0), (0.045 * D, 0.004 * D, 0.045 * D), lm, M["led"])
        box(f"lens_{idx}", (0, 0.04 * D, 0), (0.085 * D, 0.002 * D, 0.085 * D), lm, M["white"])
    return g


def build(params=None, silhouette=False):
    p = dict(P)
    if params:
        p.update(params)
    D = p["D"]
    M = materials()
    root = bpy.data.objects.new("DRONE", None)
    bpy.context.collection.objects.link(root)
    t = p["ring_t"] * D
    s = p["s"] * D
    G = {"FL": (-s, s), "FR": (s, s), "BL": (-s, -s), "BR": (s, -s)}
    for name, (gx, gy) in G.items():
        light = name in ("FL", "FR")
        guard(name, gx, gy, root, p, with_light=light, light_dir=(gx, gy))

    bx, by, bz = [v * D for v in p["body"]]
    top = p["body_top"] * D

    G = {n: (gx + p["guard_adj"].get(n, (0, 0))[0] * D, gy + p["guard_adj"].get(n, (0, 0))[1] * D)
         for n, (gx, gy) in G.items()}
    # placa central + braços em gusset (largos no corpo, estreitos no cubo)
    plate("center_plate", [(-bx * 0.62, -by * 0.52), (bx * 0.62, -by * 0.52), (bx * 0.62, by * 0.52),
                           (-bx * 0.62, by * 0.52)], t, root, M["carbon"])
    for name, (gx, gy) in G.items():
        d = Vector((gx, gy)).normalized()
        n = Vector((-d.y, d.x))
        base = Vector((gx, gy)) * 0.30
        hub = Vector((gx, gy))
        wb, wh = (0.16 if name in ('FL', 'FR') else 0.07) * D, 0.06 * D
        pts = [base + n * wb, hub + n * wh, hub - n * wh, base - n * wb]
        if name in ("FL", "FR"):
            # gusset vazado: contorno de carbono com recorte triangular, como na foto
            bw = 0.045 * D
            for i in range(4):
                a3 = Vector((pts[i].x, pts[i].y, 0)); b3 = Vector((pts[(i + 1) % 4].x, pts[(i + 1) % 4].y, 0))
                bar(f"arm_{name}_e{i}", a3, b3, bw, t, root, M["carbon"])
            mid = base + (hub - base) * 0.55
            bar(f"arm_{name}_x", Vector((base.x + n.x * wb, base.y + n.y * wb, 0)), Vector((mid.x - n.x * wh, mid.y - n.y * wh, 0)),
                bw, t, root, M["carbon"])
            plate(f"arm_{name}_hubplate", [(v.x, v.y) for v in [hub + n * wh - d * 0.1 * D, hub + n * wh, hub - n * wh,
                                                              hub - n * wh - d * 0.1 * D]], t, root, M["carbon"])
        else:
            plate(f"arm_{name}", [(v.x, v.y) for v in pts], t, root, M["carbon"])

    # corpo (eletrônica) pendurado abaixo da placa
    box("body", (0, 0, top - bz / 2), (bx, by, bz), root, M["plastic"])
    for side in (-1, 1):
        for k in range(14):
            y = by * 0.05 + k * by * 0.03
            box(f"fin_{side}_{k}", (side * (bx / 2 + 0.01 * D), y, top - bz * 0.55),
                (0.02 * D, 0.012 * D, bz * 0.62), root, M["plastic"])
    plate("bottom_plate", [(-bx * 0.45, -by * 0.45), (bx * 0.45, -by * 0.45), (bx * 0.45, by * 0.45),
                           (-bx * 0.45, by * 0.45)], t, root, M["carbon"], z=top - bz - t)

    # selim: bloco preto inclinado subindo da frente para trás, até o berço do LiDAR
    sp = bpy.data.objects.new("saddle", None)
    bpy.context.collection.objects.link(sp)
    sp.parent = root
    box("saddle_core", (-0.02 * D, 0.0, 0.11 * D), (0.22 * D, 0.62 * D, 0.20 * D), sp, M["plastic"], rot=(-16, 0, 0))
    box("saddle_tower", (-0.04 * D, -0.30 * D, 0.20 * D), (0.24 * D, 0.24 * D, 0.30 * D), sp, M["plastic"], rot=(-20, 0, 0))
    # arco de carbono (moldura trapezoidal) por cima do selim
    hoop = [(-0.30, 0.30, 0.02), (-0.24, 0.24, 0.30), (0.08, 0.02, 0.44), (0.30, -0.22, 0.30), (0.33, -0.25, 0.04)]
    for i in range(len(hoop) - 1):
        bar(f"hoop_{i}", [v * D for v in hoop[i]], [v * D for v in hoop[i + 1]], 0.035 * D, 0.012 * D, root,
            M["carbon"], up=(0.4, 0.6, 0.6))

    # LiDAR inclinado
    lx, ly, lz = [v * D for v in p["lidar_pos"]]
    tilt = math.radians(p["lidar_tilt"])
    axis = Vector((0, -math.sin(tilt), math.cos(tilt)))
    h = p["lidar_h"] * D
    r = p["lidar_r"] * D
    base = Vector((lx, ly, lz)) - axis * h / 2
    cyl("lidar_base", base, base + axis * h * 0.25, r * 0.96, root, M["plastic"])
    cyl("lidar_band", base + axis * h * 0.25, base + axis * h * 0.45, r, root, M["white"])
    cyl("lidar_glass", base + axis * h * 0.45, base + axis * h * 0.92, r * 0.98, root, M["lidar_glass"])
    cyl("lidar_cap", base + axis * h * 0.92, base + axis * h, r, root, M["alu"])
    cyl("lidar_cradle", base - axis * 0.10 * D, base, r * 0.75, root, M["plastic"])
    bar("lidar_post", (lx, ly + 0.1 * D, 0.0), tuple(base - axis * 0.08 * D), 0.12 * D, 0.10 * D, root, M["plastic"])
    # gaiola do LiDAR: octógono grande de carbono no plano lateral (YZ), medido na foto (lado da câmera);
    # o lado oposto é espelhado por suposição (REQUIRES_GAVEA_VALIDATION)
    cage = [(-0.08, 0.68), (-0.29, 0.77), (-0.48, 0.71), (-0.91, 0.40), (-1.02, 0.24), (-0.92, 0.15),
            (-0.70, 0.09), (-0.42, 0.28)]
    for side in (-1,):
        for i in range(len(cage)):
            y1, z1 = cage[i]; y2, z2 = cage[(i + 1) % len(cage)]
            bar(f"lidar_cage_{side}_{i}", (side * 0.14 * D, y1 * D, z1 * D), (side * 0.14 * D, y2 * D, z2 * D),
                0.04 * D, 0.012 * D, root, M["carbon"], up=(1, 0, 0))
    # apoio da gaiola no selim
    bar("lidar_cage_strut", (-0.14 * D, -0.42 * D, 0.28 * D), (-0.04 * D, -0.30 * D, 0.22 * D), 0.03 * D, 0.02 * D, root, M["carbon"])
    cyl("blue_conn", (-0.02 * D, -0.05 * D, 0.30 * D), (-0.02 * D, -0.05 * D, 0.40 * D), 0.03 * D, root, M["blue_anod"])
    cyl("conn_alu", (-0.13 * D, -0.30 * D, 0.14 * D), (-0.13 * D, -0.30 * D, 0.26 * D), 0.014 * D, root, M["alu"])
    # molduras laterais de carbono do selim (contorno trapezoidal)
    for side in (-1, 1):
        fr = [(0.36, 0.02), (0.22, 0.34), (-0.22, 0.44), (-0.40, 0.06)]
        for i in range(4):
            y1, z1 = fr[i]
            y2, z2 = fr[(i + 1) % 4]
            bar(f"saddle_frame_{side}_{i}", (side * 0.13 * D, y1 * D, z1 * D), (side * 0.13 * D, y2 * D, z2 * D),
                0.045 * D, 0.012 * D, root, M["carbon"], up=(1, 0, 0))

    # ferramenta frontal: medidas por projeção inversa no plano central (x = TX), em D.
    # Módulo da escova fica ALTO (z ~ +0.25), confirmado pela foto de perfil.
    TX = 0.04
    def P3(y, z, x=TX):
        return Vector((x * D, y * D, z * D))
    tr = p["tool_reach"] * D
    # par de placas de carbono que leva o módulo da escova até o corpo
    for side in (-0.05, 0.05):
        plate_pts = [(0.42, 0.02), (0.42, 0.14), (1.18, 0.34), (1.30, 0.20), (1.22, 0.08)]
        for i in range(len(plate_pts)):
            y1, z1 = plate_pts[i]; y2, z2 = plate_pts[(i + 1) % len(plate_pts)]
            bar(f"tool_plate_{side}_{i}", P3(y1, z1, TX + side), P3(y2, z2, TX + side), 0.05 * D, 0.012 * D, root,
                M["carbon"], up=(1, 0, 0))
    box("tool_bracket", tuple(P3(1.10, 0.20)), (0.13 * D, 0.16 * D, 0.12 * D), root, M["plastic"], rot=(-15, 0, 0))
    bc = P3(1.36, 0.25)
    cyl("brush", bc + Vector((-0.07 * D, 0, 0)), bc + Vector((0.06 * D, 0, 0)), 0.115 * D, root, M["rubber"])
    cyl("brush_hub", bc + Vector((-0.078 * D, 0, 0)), bc + Vector((-0.07 * D, 0, 0)), 0.04 * D, root, M["alu"])
    cyl("brush_housing", bc + Vector((-0.02 * D, -0.02 * D, 0.03 * D)), bc + Vector((0.11 * D, -0.02 * D, 0.03 * D)),
        0.135 * D, root, M["plastic"])
    box("tool_tip_block", tuple(P3(1.48, 0.40)), (0.09 * D, 0.10 * D, 0.08 * D), root, M["plastic"], rot=(-20, 0, 0))
    cyl("spring", P3(1.11, 0.39, TX - 0.02), P3(0.94, 0.24, TX - 0.02), 0.016 * D, root, M["alu"])
    # braço inferior de carbono e sondas
    bar("tool_arm_low", P3(0.80, -0.12), P3(1.27, -0.39), 0.10 * D, 0.012 * D, root, M["carbon"], up=(1, 0, 0))
    bar("tool_arm_low2", P3(0.45, -0.05), P3(0.82, -0.12), 0.10 * D, 0.012 * D, root, M["carbon"], up=(1, 0, 0))
    bar("probe_a", P3(1.25, -0.14), P3(1.54, 0.01), 0.075 * D, 0.07 * D, root, M["plastic"], up=(1, 0, 0))
    bar("probe_b", P3(1.22, -0.37), P3(1.55, -0.30), 0.08 * D, 0.075 * D, root, M["plastic"], up=(1, 0, 0))
    cyl("probe_pin", P3(1.55, -0.30), P3(1.60, -0.29), 0.013 * D, root, M["alu"])
    box("probe_conn", tuple(P3(1.55, 0.14)), (0.05 * D, 0.06 * D, 0.06 * D), root, M["plastic"])
    bar("probe_link", P3(1.27, -0.39), P3(1.25, -0.14), 0.03 * D, 0.03 * D, root, M["carbon"], up=(1, 0, 0))
    # cabos pretos
    for i, pts in enumerate([
        [(0.05, 0.1, 0.25), (0.12, 0.35, 0.18), (0.08, 0.6, 0.10), (0.02, 0.9, 0.05), (0.06, 1.15, 0.02)],
        [(-0.10, -0.2, 0.30), (-0.18, 0.05, 0.22), (-0.12, 0.3, 0.12), (-0.2, 0.55, 0.05), (-0.08, 0.85, -0.05), (0.0, 1.2, -0.25)],
        [(0.10, -0.35, 0.25), (0.16, -0.1, 0.20), (0.14, 0.2, 0.06), (0.10, 0.5, -0.06), (0.05, 0.9, -0.12)],
        [(-0.05, 0.75, 0.10), (-0.12, 0.82, 0.18), (-0.02, 0.95, 0.14), (0.05, 1.05, 0.06)],
    ]):
        tube(f"cable_{i}", [Vector(p) * D for p in pts], 0.007 * D, root, M["rubber"])

    # tubo azul: caminho extraído da foto (trace_tube.py); sem o arquivo, usa o traçado manual
    import json as _json, os as _os
    tp = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "renders", "tube_path.json")
    if p.get("tube_from_photo", True) and _os.path.exists(tp):
        tpts = [Vector(v) for v in _json.load(open(tp))]
    else:
        tpts = [Vector(v) * D for v in [(-0.02, -0.05, 0.36), (-0.10, 0.10, 0.30), (-0.04, 0.30, 0.16),
                                         (-0.20, 0.42, 0.10), (-0.12, 0.62, 0.02), (0.0, 0.95, -0.02),
                                         (0.05, tr / D * 1.02, -0.18)]]
    tube("tube_main", tpts, 0.018 * D, root, M["tube"])

    # chanfro fino em todas as peças: devolve os brilhos de borda que a foto tem
    for o in root.children_recursive:
        if o.type == "MESH":
            bv = o.modifiers.new("bevel", "BEVEL")
            bv.width = 0.0007
            bv.segments = 2
            bv.limit_method = "ANGLE"
            bv.harden_normals = False
    if silhouette:
        for o in root.children_recursive:
            if o.type in ("MESH", "CURVE"):
                o.data.materials.clear()
                o.data.materials.append(M["silhouette"])
    return root, p
