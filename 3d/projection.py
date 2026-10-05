"""Projeção da foto master sobre o modelo (camera projection mapping).

A foto é projetada a partir da câmera recuperada do master. O projetor fica preso ao drone,
então os pixels acompanham o objeto quando ele gira. Um mapa de profundidade renderizado do
ponto de vista do projetor decide quais superfícies a foto realmente enxerga; as demais
recebem o material procedural. Uma "placa de resíduo" segura o que a foto mostra e o modelo
ainda não tem (cabos, miudezas), só onde não há geometria.
"""
import math, os
import bpy
import scene

PHOTO = os.path.abspath(os.path.join(scene.HERE, "..", "public", "media", "drone-cutout.png"))
PW, PH = 1000, 667


def make_projector(root, cam):
    """Empty com a mesma pose da câmera do master, filho do drone (drone na pose original)."""
    c = scene.camera(cam["az"], cam["el"], cam["dist"], cam["focal"], (cam["tx"], cam["ty"], cam["tz"]), cam["roll"],
                     name="PROJ_CAM")
    bpy.context.view_layer.update()
    proj = bpy.data.objects.new("PROJ", None)
    bpy.context.collection.objects.link(proj)
    proj.matrix_world = c.matrix_world.copy()
    proj.parent = root
    proj.matrix_parent_inverse = root.matrix_world.inverted()
    return proj, c


def render_depth(proj_cam, path, scale=2, exclude=()):
    """Profundidade ao longo do eixo da câmera, em metros, EXR float. 0 = vazio."""
    sc = bpy.context.scene
    keep = (sc.camera, sc.render.resolution_x, sc.render.resolution_y, sc.render.film_transparent,
            sc.cycles.samples, sc.cycles.filter_width, sc.cycles.use_denoising, sc.world,
            sc.render.image_settings.file_format, sc.render.image_settings.color_depth,
            sc.view_settings.view_transform, sc.view_settings.look)
    m = bpy.data.materials.new("depth_override")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    cd = nt.nodes.new("ShaderNodeCameraData")
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(cd.outputs["View Z Depth"], em.inputs["Strength"])
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    hidden = []
    for o in exclude:
        hidden.append((o, o.hide_render))
        o.hide_render = True
    vl = bpy.context.view_layer
    vl.material_override = m
    w = bpy.data.worlds.new("black")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
    sc.world = w
    sc.camera = proj_cam
    sc.render.resolution_x, sc.render.resolution_y = PW * scale, PH * scale
    sc.render.film_transparent = False
    sc.cycles.samples = 1
    sc.cycles.filter_width = 0.01
    sc.cycles.use_denoising = False
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    sc.view_settings.view_transform = "Raw" if "Raw" in [i.identifier for i in sc.view_settings.bl_rna.properties["view_transform"].enum_items] else "Standard"
    sc.view_settings.look = "None"
    scene.render_to(path)
    vl.material_override = None
    for o, h in hidden:
        o.hide_render = h
    (sc.camera, sc.render.resolution_x, sc.render.resolution_y, sc.render.film_transparent, sc.cycles.samples,
     sc.cycles.filter_width, sc.cycles.use_denoising, sc.world, sc.render.image_settings.file_format,
     sc.render.image_settings.color_depth, sc.view_settings.view_transform, sc.view_settings.look) = keep
    return path


def _proj_uv(nt, proj, focal):
    """Nós que calculam (u, v, profundidade) da superfície vista pelo projetor."""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    tc.object = proj
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    negz = nt.nodes.new("ShaderNodeMath"); negz.operation = "MULTIPLY"; negz.inputs[1].default_value = -1
    nt.links.new(sep.outputs["Z"], negz.inputs[0])
    k = focal / 36.0

    def axis(out, mult):
        dv = nt.nodes.new("ShaderNodeMath"); dv.operation = "DIVIDE"
        nt.links.new(out, dv.inputs[0]); nt.links.new(negz.outputs[0], dv.inputs[1])
        ma = nt.nodes.new("ShaderNodeMath"); ma.operation = "MULTIPLY_ADD"
        ma.inputs[1].default_value = mult; ma.inputs[2].default_value = 0.5
        nt.links.new(dv.outputs[0], ma.inputs[0])
        return ma.outputs[0]

    u = axis(sep.outputs["X"], k)
    v = axis(sep.outputs["Y"], k * PW / PH)
    cmb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(u, cmb.inputs[0]); nt.links.new(v, cmb.inputs[1])
    return cmb.outputs[0], negz.outputs[0]


def _facing(nt, proj):
    """|cos| entre a normal da superfície e o raio vindo do projetor. A posição do projetor
    chega por drivers de transformação (sem expressão Python, roda em background)."""
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    pp = nt.nodes.new("ShaderNodeCombineXYZ")
    for i, ax in enumerate("XYZ"):
        fc = pp.inputs[i].driver_add("default_value")
        dr = fc.driver
        dr.type = "AVERAGE"
        var = dr.variables.new()
        var.type = "TRANSFORMS"
        var.targets[0].id = proj
        var.targets[0].transform_type = "LOC_" + ax
        var.targets[0].transform_space = "WORLD_SPACE"
    sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"
    nt.links.new(pp.outputs[0], sub.inputs[0]); nt.links.new(geo.outputs["Position"], sub.inputs[1])
    nrm = nt.nodes.new("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"
    nt.links.new(sub.outputs[0], nrm.inputs[0])
    dot = nt.nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    nt.links.new(nrm.outputs[0], dot.inputs[0]); nt.links.new(geo.outputs["True Normal"], dot.inputs[1])
    ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
    nt.links.new(dot.outputs["Value"], ab.inputs[0])
    return ab.outputs[0]


def _images(depth_path):
    photo = bpy.data.images.get("photo") or bpy.data.images.load(PHOTO)
    photo.name = "photo"
    photo.alpha_mode = "STRAIGHT"
    depth = bpy.data.images.load(depth_path, check_existing=False)
    depth.name = "proj_depth"
    depth.colorspace_settings.name = "Non-Color"
    return photo, depth


def apply(materials, proj, focal, depth_path, eps=0.006, gain=1.0, facing=(0.2, 0.45)):
    """Envolve cada material: foto onde o projetor enxerga, procedural no resto."""
    photo, depth = _images(depth_path)
    for m in materials:
        nt = m.node_tree
        out = nt.nodes["Material Output"]
        old = out.inputs["Surface"].links[0].from_socket
        uv, zdist = _proj_uv(nt, proj, focal)
        ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = photo; ti.extension = "CLIP"; ti.interpolation = "Cubic"
        nt.links.new(uv, ti.inputs["Vector"])
        td = nt.nodes.new("ShaderNodeTexImage"); td.image = depth; td.extension = "CLIP"; td.interpolation = "Closest"
        nt.links.new(uv, td.inputs["Vector"])
        # visível = profundidade da superfície <= profundidade do mapa + eps, e mapa > 0
        add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"; add.inputs[1].default_value = eps
        nt.links.new(td.outputs["Color"], add.inputs[0])
        vis = nt.nodes.new("ShaderNodeMath"); vis.operation = "LESS_THAN"
        nt.links.new(zdist, vis.inputs[0]); nt.links.new(add.outputs[0], vis.inputs[1])
        has = nt.nodes.new("ShaderNodeMath"); has.operation = "GREATER_THAN"; has.inputs[1].default_value = 0.0
        nt.links.new(td.outputs["Color"], has.inputs[0])
        m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
        nt.links.new(vis.outputs[0], m1.inputs[0]); nt.links.new(has.outputs[0], m1.inputs[1])
        # borda semitransparente da foto (franja do fundo branco) não entra
        al = nt.nodes.new("ShaderNodeMapRange"); al.interpolation_type = "SMOOTHSTEP"
        al.inputs["From Min"].default_value = 0.55; al.inputs["From Max"].default_value = 0.95
        nt.links.new(ti.outputs["Alpha"], al.inputs["Value"])
        # faces vistas de lado pelo projetor esticam a foto: entra o material do modelo
        fac = _facing(nt, proj)
        fm = nt.nodes.new("ShaderNodeMapRange"); fm.interpolation_type = "SMOOTHSTEP"
        fm.inputs["From Min"].default_value = facing[0]; fm.inputs["From Max"].default_value = facing[1]
        nt.links.new(fac, fm.inputs["Value"])
        m2a = nt.nodes.new("ShaderNodeMath"); m2a.operation = "MULTIPLY"
        nt.links.new(m1.outputs[0], m2a.inputs[0]); nt.links.new(al.outputs[0], m2a.inputs[1])
        m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
        nt.links.new(m2a.outputs[0], m2.inputs[0]); nt.links.new(fm.outputs[0], m2.inputs[1])
        # fator de mistura controlado de fora (0 = só procedural)
        amt = nt.nodes.new("ShaderNodeValue"); amt.name = "proj_amount"; amt.outputs[0].default_value = 1.0
        m3 = nt.nodes.new("ShaderNodeMath"); m3.operation = "MULTIPLY"
        nt.links.new(m2.outputs[0], m3.inputs[0]); nt.links.new(amt.outputs[0], m3.inputs[1])
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = gain
        nt.links.new(ti.outputs["Color"], em.inputs["Color"])
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(m3.outputs[0], mix.inputs[0])
        nt.links.new(old, mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs["Surface"])


def residual_card(root, proj, focal, depth_path, dist, size=1.4):
    """Placa perpendicular ao projetor, na profundidade do centro do drone, que mostra só os pixels
    da foto onde o modelo não tem geometria. Fica transparente no resto."""
    photo, depth = _images(depth_path)
    bpy.ops.mesh.primitive_plane_add(size=size)
    card = bpy.context.active_object
    card.name = "residual_card"
    card.parent = proj
    card.matrix_parent_inverse.identity()
    card.location = (0, 0, -dist)
    card.rotation_euler = (0, 0, 0)
    m = bpy.data.materials.new("residual")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    uv, _ = _proj_uv(nt, proj, focal)
    ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = photo; ti.extension = "CLIP"
    nt.links.new(uv, ti.inputs["Vector"])
    td = nt.nodes.new("ShaderNodeTexImage"); td.image = depth; td.extension = "CLIP"; td.interpolation = "Closest"
    nt.links.new(uv, td.inputs["Vector"])
    empty = nt.nodes.new("ShaderNodeMath"); empty.operation = "LESS_THAN"; empty.inputs[1].default_value = 1e-4
    nt.links.new(td.outputs["Color"], empty.inputs[0])
    mk = nt.nodes.new("ShaderNodeMath"); mk.operation = "MULTIPLY"
    nt.links.new(empty.outputs[0], mk.inputs[0]); nt.links.new(ti.outputs["Alpha"], mk.inputs[1])
    amt = nt.nodes.new("ShaderNodeValue"); amt.name = "shell_amount"; amt.outputs[0].default_value = 1.0
    m3 = nt.nodes.new("ShaderNodeMath"); m3.operation = "MULTIPLY"
    nt.links.new(mk.outputs[0], m3.inputs[0]); nt.links.new(amt.outputs[0], m3.inputs[1])
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(ti.outputs["Color"], em.inputs["Color"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(m3.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    card.data.materials.append(m)
    card.visible_shadow = False
    return card


def set_shell(value):
    for m in bpy.data.materials:
        if m.node_tree and "shell_amount" in m.node_tree.nodes:
            m.node_tree.nodes["shell_amount"].outputs[0].default_value = value


def set_amount(value):
    for m in bpy.data.materials:
        if m.node_tree and "proj_amount" in m.node_tree.nodes:
            m.node_tree.nodes["proj_amount"].outputs[0].default_value = value


def residual_shell(proj, focal, depth_path, res=(250, 167), offset=0.008):
    """Casca 2.5D: malha no espaço do projetor que segue o mapa de profundidade (buracos preenchidos
    pelos vizinhos). Mostra só os pixels da foto onde o modelo não tem geometria."""
    import numpy as np
    img = bpy.data.images.load(depth_path, check_existing=False)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    d = px.reshape(h, w, 4)[..., 0]          # linha 0 = base da imagem (v = 0)
    gw, gh = res
    # reduz pela mediana dos válidos em cada bloco
    bh, bw = h // gh, w // gw
    blk = d[:gh * bh, :gw * bw].reshape(gh, bh, gw, bw).transpose(0, 2, 1, 3).reshape(gh, gw, -1)
    blk = np.where(blk > 0, blk, np.nan)
    with np.errstate(all="ignore"):
        g = np.nanmedian(blk, axis=2)
    # preenche buracos com a média dos vizinhos válidos, iterando
    valid = ~np.isnan(g)
    g = np.where(valid, g, 0.0)
    for _ in range(400):
        if valid.all():
            break
        s = np.zeros_like(g); n = np.zeros_like(g)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                s += np.roll(np.roll(np.where(valid, g, 0), dy, 0), dx, 1)
                n += np.roll(np.roll(valid.astype(float), dy, 0), dx, 1)
        fill = (~valid) & (n > 0)
        g[fill] = s[fill] / n[fill]
        valid = valid | fill
    # suaviza (a casca não precisa de quinas)
    for _ in range(6):
        g = (g + np.roll(g, 1, 0) + np.roll(g, -1, 0) + np.roll(g, 1, 1) + np.roll(g, -1, 1)) / 5
    k = focal / 36.0
    verts, faces = [], []
    for j in range(gh):
        for i in range(gw):
            u = (i + 0.5) / gw; v = (j + 0.5) / gh
            z = float(g[j, i]) - offset
            verts.append(((u - 0.5) / k * z, (v - 0.5) / (k * PW / PH) * z, -z))
    for j in range(gh - 1):
        for i in range(gw - 1):
            a = j * gw + i
            faces.append((a, a + 1, a + gw + 1, a + gw))
    me = bpy.data.meshes.new("residual_shell")
    me.from_pydata(verts, [], faces)
    o = bpy.data.objects.new("residual_shell", me)
    bpy.context.collection.objects.link(o)
    o.parent = proj
    o.matrix_parent_inverse.identity()
    # material: mesmo do cartão de resíduo
    card = residual_card(None, proj, focal, depth_path, 1.0, size=0.01)
    o.data.materials.append(card.data.materials[0])
    bpy.data.objects.remove(card, do_unlink=True)
    o.visible_shadow = False
    return o


def apply_albedo(materials, proj, focal, depth_path, eps=0.006, facing=(0.2, 0.45), strength=0.8):
    """Variante para cenas com luz própria (escuro): a foto entra como cor base do material,
    então responde às lanternas e à névoa em vez de brilhar sozinha."""
    photo, depth = _images(depth_path)
    for m in materials:
        nt = m.node_tree
        b = nt.nodes.get("Principled BSDF")
        if b is None:
            continue
        sock = b.inputs["Base Color"]
        old = sock.links[0].from_socket if sock.links else None
        uv, zdist = _proj_uv(nt, proj, focal)
        ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = photo; ti.extension = "CLIP"; ti.interpolation = "Cubic"
        nt.links.new(uv, ti.inputs["Vector"])
        td = nt.nodes.new("ShaderNodeTexImage"); td.image = depth; td.extension = "CLIP"; td.interpolation = "Closest"
        nt.links.new(uv, td.inputs["Vector"])
        add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"; add.inputs[1].default_value = eps
        nt.links.new(td.outputs["Color"], add.inputs[0])
        vis = nt.nodes.new("ShaderNodeMath"); vis.operation = "LESS_THAN"
        nt.links.new(zdist, vis.inputs[0]); nt.links.new(add.outputs[0], vis.inputs[1])
        al = nt.nodes.new("ShaderNodeMapRange"); al.interpolation_type = "SMOOTHSTEP"
        al.inputs["From Min"].default_value = 0.55; al.inputs["From Max"].default_value = 0.95
        nt.links.new(ti.outputs["Alpha"], al.inputs["Value"])
        fm = nt.nodes.new("ShaderNodeMapRange"); fm.interpolation_type = "SMOOTHSTEP"
        fm.inputs["From Min"].default_value = facing[0]; fm.inputs["From Max"].default_value = facing[1]
        nt.links.new(_facing(nt, proj), fm.inputs["Value"])
        m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
        nt.links.new(vis.outputs[0], m1.inputs[0]); nt.links.new(al.outputs[0], m1.inputs[1])
        m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
        nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(fm.outputs[0], m2.inputs[1])
        m2.inputs[1].default_value = 1.0
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
        nt.links.new(m2.outputs[0], mx.inputs["Factor"])
        if old:
            nt.links.new(old, mx.inputs["A"])
        else:
            mx.inputs["A"].default_value = sock.default_value
        gain = nt.nodes.new("ShaderNodeMix"); gain.data_type = "RGBA"; gain.blend_type = "MULTIPLY"
        gain.inputs["Factor"].default_value = 1.0
        gain.inputs["B"].default_value = (strength, strength, strength, 1)
        nt.links.new(ti.outputs["Color"], gain.inputs["A"])
        nt.links.new(gain.outputs["Result"], mx.inputs["B"])
        nt.links.new(mx.outputs["Result"], sock)
