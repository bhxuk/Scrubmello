"""Scrubmello product models and renders (Blender / Cycles).
Units: metres. Products are modelled lying flat on the floor (XY plane),
bristles facing up (+Z), handle running towards -Y from the click collar at Y=0.
Usage: python sm.py <shot> [<shot> ...]   (or 'all')"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
QUICK = os.environ.get('SM_QUICK') == '1'

HEX = {
    'pink': '#f4b9c8', 'blue': '#a9d3ee', 'yellow': '#f7e08c', 'black': '#4a4a54',
    'white': '#f2f0ec', 'lilac': '#cfc2ef', 'mint': '#bfe5c7',
}
RAINBOW = ['#f6bfcd', '#f9d2ae', '#f8e59a', '#bfe5c7', '#b3d8f0', '#cfc2ef']
AXIS = 0.008  # centre line height: everything is coaxial, back of head sits on the floor


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


# ---------------------------------------------------------------- materials
_mats = {}


def _colour_input(nt, bsdf, col, axis='Y'):
    """Plain colour, or a rainbow gradient along the object's own length."""
    if col != 'rainbow':
        bsdf.inputs['Base Color'].default_value = lin(HEX[col]); return
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs[axis], ramp.inputs[0])
    els = ramp.color_ramp.elements
    while len(els) < len(RAINBOW): els.new(0.5)
    for i, hx in enumerate(RAINBOW):
        els[i].position = i / (len(RAINBOW) - 1); els[i].color = lin(hx)
    nt.links.new(ramp.outputs[0], bsdf.inputs['Base Color'])


def mat(kind, col):
    key = (kind, col)
    if key in _mats: return _mats[key]
    m = bpy.data.materials.new(f'{kind}-{col}'); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    if kind == 'soft':      # soft-touch matte silicone
        _colour_input(nt, b, col)
        b.inputs['Roughness'].default_value = 0.62
        b.inputs['Subsurface Weight'].default_value = 0.25
        b.inputs['Subsurface Scale'].default_value = 0.002
        b.inputs['Sheen Weight'].default_value = 0.25
        b.inputs['Sheen Roughness'].default_value = 0.4
        b.inputs['Coat Weight'].default_value = 0.08
        b.inputs['Coat Roughness'].default_value = 0.5
    elif kind == 'bristle':  # slightly glossier silicone for bristles
        _colour_input(nt, b, col, 'Y')
        b.inputs['Roughness'].default_value = 0.42
        b.inputs['Subsurface Weight'].default_value = 0.35
        b.inputs['Subsurface Scale'].default_value = 0.0015
    elif kind == 'clear':    # frosted see-through silicone, faint tint
        c = lin(HEX[col]) if col != 'rainbow' else lin('#f4f0ff')
        tint = tuple(0.82 + 0.18 * v for v in c[:3]) + (1,)
        b.inputs['Base Color'].default_value = tint
        b.inputs['Transmission Weight'].default_value = 1.0
        b.inputs['Roughness'].default_value = 0.16
        b.inputs['IOR'].default_value = 1.41
        b.inputs['Coat Weight'].default_value = 0.3
        b.inputs['Coat Roughness'].default_value = 0.05
    elif kind == 'fabric':
        _colour_input(nt, b, col)
        b.inputs['Roughness'].default_value = 0.95
        b.inputs['Sheen Weight'].default_value = 0.9
        b.inputs['Sheen Roughness'].default_value = 0.35
        # waffle weave bump
        tc = nt.nodes.new('ShaderNodeTexCoord'); w1 = nt.nodes.new('ShaderNodeTexWave'); w2 = nt.nodes.new('ShaderNodeTexWave')
        for w, d in ((w1, 'X'), (w2, 'Y')):
            w.wave_type = 'BANDS'; w.bands_direction = d; w.inputs['Scale'].default_value = 220
            w.inputs['Distortion'].default_value = 0.4
            nt.links.new(tc.outputs['Object'], w.inputs['Vector'])
        mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
        nt.links.new(w1.outputs['Fac'], mx.inputs[0]); nt.links.new(w2.outputs['Fac'], mx.inputs[1])
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 1.0
        bump.inputs['Distance'].default_value = 0.0015
        nt.links.new(mx.outputs[0], bump.inputs['Height']); nt.links.new(bump.outputs[0], b.inputs['Normal'])
    elif kind == 'ripple':   # ultra smooth silicone with soft concentric ripples
        _colour_input(nt, b, col)
        b.inputs['Roughness'].default_value = 0.35
        b.inputs['Subsurface Weight'].default_value = 0.3
        b.inputs['Subsurface Scale'].default_value = 0.002
        tc = nt.nodes.new('ShaderNodeTexCoord'); w = nt.nodes.new('ShaderNodeTexWave')
        w.wave_type = 'RINGS'; w.inputs['Scale'].default_value = 60; w.wave_profile = 'SIN'
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 0.85, 1)
        nt.links.new(tc.outputs['Object'], mp.inputs[0]); nt.links.new(mp.outputs[0], w.inputs['Vector'])
        bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35
        bump.inputs['Distance'].default_value = 0.0008
        nt.links.new(w.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs[0], b.inputs['Normal'])
    elif kind == 'mesh':
        _colour_input(nt, b, col)
        b.inputs['Roughness'].default_value = 0.5
        b.inputs['Sheen Weight'].default_value = 0.5
    if col == 'black' and 'Subsurface Weight' in b.inputs: b.inputs['Subsurface Weight'].default_value = 0.0
    _mats[key] = m
    return m


# ---------------------------------------------------------------- helpers
def link(ob, parent):
    bpy.context.collection.objects.link(ob)
    if parent: ob.parent = parent
    return ob


def new_mesh(name, verts, faces, m, parent=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); me.materials.append(m)
    return link(ob, parent)


def tube(name, pts, m, parent=None, squash=0.78, ring=24, cap=True):
    """Sweep a circle along pts [(x,y,r)] lying in the XY plane at the axis height.
    The section is squashed in Z so handles are wider than they are thick."""
    verts, faces = [], []
    n = len(pts)
    for i, (x, y, r) in enumerate(pts):
        a = Vector((pts[min(i + 1, n - 1)][0] - pts[max(i - 1, 0)][0], pts[min(i + 1, n - 1)][1] - pts[max(i - 1, 0)][1], 0)).normalized()
        side = Vector((-a.y, a.x, 0))
        for k in range(ring):
            t = 2 * math.pi * k / ring
            p = Vector((x, y, AXIS)) + side * (r * math.cos(t)) + Vector((0, 0, 1)) * (r * squash * math.sin(t))
            verts.append(tuple(p))
    for i in range(n - 1):
        for k in range(ring):
            a, b2 = i * ring + k, i * ring + (k + 1) % ring
            faces.append((a, b2, b2 + ring, a + ring))
    if cap:
        for end, idx in ((0, 0), (1, n - 1)):
            c = len(verts); x, y, _ = pts[idx]; verts.append((x, y, AXIS))
            for k in range(ring):
                a, b2 = idx * ring + k, idx * ring + (k + 1) % ring
                faces.append((c, b2, a) if end == 0 else (c, a, b2))
    return new_mesh(name, verts, faces, m, parent)


def path_profile(path, radius, n=90):
    """path(t)->(x,y), radius(t)->r for t in [0,1]"""
    return [(*path(i / (n - 1)), radius(i / (n - 1))) for i in range(n)]


def round_ends(r, t, a=0.06, b=0.06, r0=None):
    """Make a radius function close with round caps at both ends."""
    v = r(t)
    if t < a: v *= math.sqrt(max(1 - ((a - t) / a) ** 2, 0.02)) if r0 is None else 1
    if t > 1 - b: v *= math.sqrt(max(1 - ((t - (1 - b)) / b) ** 2, 0.0))
    return max(v, 0.0004)


def torus(name, centre, R, r, m, parent=None, normal='Z', seg=48, rs=16):
    verts, faces = [], []
    for i in range(seg):
        u = 2 * math.pi * i / seg
        for j in range(rs):
            v = 2 * math.pi * j / rs
            p = Vector(((R + r * math.cos(v)) * math.cos(u), (R + r * math.cos(v)) * math.sin(u), r * math.sin(v)))
            if normal == 'X': p = Vector((p.z, p.x, p.y))
            elif normal == 'Y': p = Vector((p.x, p.z, p.y))
            verts.append(tuple(p + Vector(centre)))
    for i in range(seg):
        for j in range(rs):
            a = i * rs + j; b2 = ((i + 1) % seg) * rs + j
            faces.append((a, b2, ((i + 1) % seg) * rs + (j + 1) % rs, i * rs + (j + 1) % rs))
    return new_mesh(name, verts, faces, m, parent)


def cyl_y(name, y0, y1, r, m, parent=None, squash=1.0, x=0.0):
    return tube(name, [(x, y0, r), (x, y1, r)], m, parent, squash=squash, ring=32)


# ---------------------------------------------------------------- heads
EGG_A, EGG_B, EGG_K = 0.036, 0.044, 0.14   # half width, half height, egg-ness (wider at top)


def egg_pts(a=EGG_A, b=EGG_B, k=EGG_K, n=96, shrink=1.0):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = a * math.cos(t) * (1 + k * math.sin(t)); y = b * math.sin(t)
        pts.append((x * shrink, y * shrink))
    return pts


def inside(px, py, a, b, k, s):
    yn = py / (b * s)
    if abs(yn) >= 1: return False
    w = a * s * (1 + k * yn) * math.sqrt(1 - yn * yn)
    return abs(px) < w


def puck(name, a, b, k, thick, m, cy, parent=None, bevel=0.0045):
    """Rounded egg-shaped slab, back on the floor, top face at z=thick."""
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '2D'; cu.fill_mode = 'BOTH'
    sp = cu.splines.new('POLY'); pts = egg_pts(a - bevel, b - bevel, k)
    sp.points.add(len(pts) - 1)
    for i, (x, y) in enumerate(pts): sp.points[i].co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    cu.extrude = max(thick / 2 - bevel, 0.0002); cu.bevel_depth = bevel; cu.bevel_resolution = 6
    ob = bpy.data.objects.new(name, cu); link(ob, parent)
    ob.location = (0, cy, thick / 2)
    ob.data.materials.append(m)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects: o.select_set(False)
    ob.select_set(True); bpy.ops.object.convert(target='MESH')
    for p in ob.data.polygons: p.use_smooth = True
    return ob


def bristle_field(name, a, b, k, cy, z0, L, r0, r1, step, m, parent=None, shrink=0.86, seg=8, tipround=True, jitter=0.0, lean=0.0):
    tmpl_v, tmpl_f = [], []
    rings = 6
    for i in range(rings + 1):
        s = i / rings
        r = r0 + (r1 - r0) * s
        z = L * s
        if tipround and i == rings: r *= 0.55
        for j in range(seg):
            t = 2 * math.pi * j / seg; tmpl_v.append((r * math.cos(t), r * math.sin(t), z))
    for i in range(rings):
        for j in range(seg):
            a1, b1 = i * seg + j, i * seg + (j + 1) % seg
            tmpl_f.append((a1, b1, b1 + seg, a1 + seg))
    top = len(tmpl_v); tmpl_v.append((0, 0, L + r1 * 0.45))
    for j in range(seg): tmpl_f.append((rings * seg + j, rings * seg + (j + 1) % seg, top))
    verts, faces = [], []
    rnd = random.Random(7)
    row = 0; y = -b
    while y < b:
        x0 = -a + (step / 2 if row % 2 else 0)
        x = x0
        while x < a:
            if inside(x, y, a, b, k, shrink):
                jx, jy = (rnd.uniform(-jitter, jitter), rnd.uniform(-jitter, jitter))
                off = len(verts)
                ln = 1 + rnd.uniform(-0.04, 0.04)
                for (vx, vy, vz) in tmpl_v:
                    verts.append((x + jx + vx + lean * vz * (x / a), cy + y + jy + vy + lean * vz * (y / b), z0 + vz * ln))
                faces += [tuple(i + off for i in f) for f in tmpl_f]
            x += step
        y += step * 0.866; row += 1
    return new_mesh(name, verts, faces, m, parent)


def head(kind, col, parent=None, collar_col=None):
    """Build a head with its stem and Mello Click collar. Collar sits at Y=0..0.008."""
    collar_col = collar_col or col
    a, b, k = EGG_A, EGG_B, EGG_K
    thick = 0.016
    if kind == 'crease': a, b, k, thick = 0.019, 0.05, 0.05, 0.011
    cy = 0.008 + 0.006 + b - 0.002          # head centre Y
    soft = mat('soft', col)
    # Mello Click collar: clear ring round a coloured core
    cyl_y('collar', 0.0, 0.0085, 0.0088, mat('clear', collar_col), parent)
    cyl_y('core', -0.002, 0.0105, 0.0062, mat('soft', collar_col), parent)
    torus('lock', (0, 0.0042, AXIS), 0.0089, 0.0009, mat('soft', collar_col), parent, normal='Y')
    # stem
    tube('stem', [(0, 0.0082, 0.0074), (0, 0.016, 0.0074), (0, 0.022, 0.0095)], soft, parent, squash=1.0, cap=False)
    base = puck('head', a, b, k, thick, soft, cy, parent)
    z0 = thick - 0.0004
    if kind == 'body':
        bristle_field('bristles', a, b, k, cy, z0, 0.0085, 0.0011, 0.0007, 0.0042, mat('bristle', col), parent, lean=0.05)
    elif kind == 'soft':
        bristle_field('bristles', a, b, k, cy, z0, 0.0042, 0.0007, 0.00045, 0.0026, mat('bristle', col), parent)
    elif kind == 'scalp':
        bristle_field('nubs', a, b, k, cy, z0, 0.0055, 0.0026, 0.0018, 0.0088, mat('bristle', col), parent, shrink=0.82, seg=12)
    elif kind == 'face':
        bristle_field('bristles', a, b, k, cy, z0, 0.0022, 0.0004, 0.0003, 0.0017, mat('bristle', col), parent, shrink=0.88, seg=6)
    elif kind == 'crease':
        bristle_field('bristles', a, b, k, cy, z0, 0.004, 0.0006, 0.0004, 0.0023, mat('bristle', col), parent, shrink=0.84)
    elif kind == 'intimate':
        base.data.materials[0] = mat('ripple', col)
        dome(a * 0.9, b * 0.9, k, cy, z0 - 0.002, 0.004, mat('ripple', col), parent)
    elif kind == 'cloth':
        dome(a * 0.95, b * 0.95, k, cy, z0 - 0.003, 0.013, mat('fabric', col), parent)
        piping(a * 0.95, b * 0.95, k, cy, z0, mat('fabric', col), parent)
    elif kind == 'mesh':
        pouf(a, b, k, cy, z0, col, parent)
    return cy


def dome(a, b, k, cy, z0, h, m, parent=None, n=64, rings=24):
    verts, faces = [], []
    for i in range(rings + 1):
        s = 1 - i / rings
        z = z0 + h * math.sqrt(max(1 - s * s, 0))
        for j in range(n):
            t = 2 * math.pi * j / n
            x = a * s * math.cos(t) * (1 + k * math.sin(t)); y = b * s * math.sin(t)
            verts.append((x, cy + y, z))
    for i in range(rings):
        for j in range(n):
            a1, b1 = i * n + j, i * n + (j + 1) % n
            faces.append((a1, b1, b1 + n, a1 + n))
    c = len(verts); verts.append((0, cy, z0 + h))
    for j in range(n): faces.append((rings * n + j, rings * n + (j + 1) % n, c))
    return new_mesh('dome', verts, faces, m, parent)


def piping(a, b, k, cy, z, m, parent=None):
    pts = egg_pts(a, b, k, 120)
    verts, faces = [], []; ring = 12; r = 0.0016
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        nx, ny = pts[(i + 1) % n][0] - pts[i - 1][0], pts[(i + 1) % n][1] - pts[i - 1][1]
        d = Vector((ny, -nx, 0)).normalized()
        for j in range(ring):
            t = 2 * math.pi * j / ring
            p = Vector((x, cy + y, z)) + d * r * math.cos(t) + Vector((0, 0, r * math.sin(t)))
            verts.append(tuple(p))
    for i in range(n):
        for j in range(ring):
            a1 = i * ring + j; b1 = i * ring + (j + 1) % ring; i2 = ((i + 1) % n) * ring
            faces.append((a1, b1, i2 + (j + 1) % ring, i2 + j))
    return new_mesh('piping', verts, faces, m, parent)


def pouf(a, b, k, cy, z0, col, parent):
    """Puffy net mesh: three overlapping jittered spheres turned into wire nets."""
    rnd = random.Random(3)
    for layer, (dx, dy, sc, rot) in enumerate(((0, 0, 1.0, 0.0), (0.004, 0.003, 0.9, 0.5), (-0.004, -0.002, 0.82, 1.1))):
        bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
        me = bpy.data.meshes.new('pouf'); bm.to_mesh(me); bm.free()
        cr, sr = math.cos(rot), math.sin(rot)
        for v in me.vertices:
            x, y, z = v.co
            x, y = x * cr - y * sr, x * sr + y * cr
            x *= a * 0.92 * sc; y *= b * 0.9 * sc; z = z * 0.013 * sc
            if z < 0: z *= 0.3
            v.co = (x + dx + rnd.uniform(-0.001, 0.001), cy + y + dy + rnd.uniform(-0.001, 0.001), z0 + 0.004 + z + rnd.uniform(-0.0008, 0.0008))
        ob = bpy.data.objects.new('pouf', me); me.materials.append(mat('mesh', col)); link(ob, parent)
        mod = ob.modifiers.new('net', 'WIREFRAME'); mod.thickness = 0.0005; mod.use_relative_offset = False
        ob.modifiers.new('sub', 'SUBSURF').levels = 1


# ---------------------------------------------------------------- handles
def handle(kind, col, parent=None):
    soft = mat('soft', col); clear = mat('clear', col)
    if kind in ('pebble', 'mini'):
        L = 0.112 if kind == 'pebble' else 0.072
        W = 0.0115 if kind == 'pebble' else 0.008
        rf = lambda t: (0.0066 + (W - 0.0066) * math.sin(math.pi * min(t / 0.62, 1) / 2) ** 1.4) if t < 0.62 else W - (W - 0.0055) * ((t - 0.62) / 0.38) ** 2
        pts = path_profile(lambda t: (0, -L * t), lambda t: round_ends(rf, t, a=0.0001, b=0.12))
        tube('grip', pts[:], soft, parent)
        # clear hang tab with a hole
        torus('loop', (0, -L - 0.006, AXIS - 0.0005), 0.0058, 0.0019, clear, parent)
        # clear thumb window: a frosted inlay along the top of the grip
        win = path_profile(lambda t: (0, -L * (0.28 + 0.4 * t)), lambda t: round_ends(lambda u: W * 0.5, t, 0.2, 0.2))
        w = tube('window', win, clear, parent, squash=0.5)
        w.location.z = W * 0.78 - 0.0025
        return L + 0.014
    if kind == 'reach':
        L = 0.40
        path = lambda t: (0.03 * math.sin(math.pi * t * 0.9) * (1 - t) - 0.012 * t * t, -L * t)
        rf = lambda t: 0.0068 + 0.0026 * max(0, (t - 0.55) / 0.45) ** 0.8 - 0.0008 * math.sin(math.pi * min(t / 0.55, 1))
        allp = path_profile(path, lambda t: round_ends(rf, t, a=0.0001, b=0.035), 160)
        # clear shaft (upper part) with a slim coloured spine inside, coloured grip (lower part)
        cut = 100
        tube('shaft', allp[:cut + 1], clear, parent, squash=0.85, cap=False)
        tube('spine', [(x, y, 0.0026) for x, y, r in allp[:cut + 1]], soft, parent, squash=1.0)
        tube('grip', allp[cut - 1:], soft, parent, squash=0.85)
        ex, ey, _ = allp[-1]
        torus('loop', (ex - 0.001, ey - 0.007, AXIS - 0.0008), 0.0065, 0.002, clear, parent)
        return L + 0.016
    if kind == 'easy':
        L = 0.17
        bend = 0.32  # radians, angled grip
        def path(t):
            s = L * t
            if s < 0.05: return (0, -s)
            u = s - 0.05
            return (math.sin(bend) * u, -0.05 - math.cos(bend) * u)
        rf = lambda t: 0.0085 + 0.0040 * math.sin(math.pi * min(max((t - 0.15) / 0.85, 0), 1) * 0.85)
        pts = path_profile(path, lambda t: round_ends(rf, t, a=0.0001, b=0.07), 140)
        tube('grip', pts, soft, parent, squash=0.8)
        # clear soft-grip rings
        for i in range(6):
            t = 0.42 + i * 0.085
            j = int(t * (len(pts) - 1))
            seg = pts[j - 2:j + 3]
            tube(f'ring{i}', [(x, y, r + 0.0016) for x, y, r in seg], clear, parent, squash=0.82)
        ex, ey, _ = pts[-1]
        torus('loop', (ex + 0.004, ey - 0.006, AXIS - 0.0008), 0.0062, 0.0019, clear, parent)
        return L + 0.014


# ---------------------------------------------------------------- products
def product(name, hkind, head_kind, head_col, handle_col, loc=(0, 0, 0), rotz=0.0, gap=0.0):
    root = bpy.data.objects.new(name, None); link(root, None)
    hp = bpy.data.objects.new(name + '-head', None); link(hp, root)
    head(head_kind, head_col, hp, collar_col=handle_col)
    hp.location.y = gap
    handle(hkind, handle_col, root)
    if hkind == 'mini': root.scale = (0.82, 0.82, 0.82)
    root.location = loc; root.rotation_euler.z = rotz
    return root


def lone_head(name, kind, col, loc=(0, 0, 0), rotz=0.0):
    root = bpy.data.objects.new(name, None); link(root, None)
    head(kind, col, root)
    root.location = loc; root.rotation_euler.z = rotz
    return root


def hooks(loc=(0, 0, 0), rotz=0.0):
    root = bpy.data.objects.new('hooks', None); link(root, None)
    clear = mat('clear', 'white'); white = mat('soft', 'white')
    # suction cup: clear disc, white hook
    d = dome(0.022, 0.022, 0.0, 0.0, 0.0, 0.007, clear, root, n=48, rings=12)
    tube('cupstem', [(0, 0.0, 0.0045), (0, 0.0, 0.0045)], white, root)
    hk = [(0.0, -0.002 + 0.03 * t, 0.0035) for t in (0, 0.5, 1)]
    tube('arm', [(0, 0.0, 0.0034), (0, 0.032, 0.0034), (0, 0.04, 0.0026)], white, root, squash=0.9)
    torus('hookend', (0, 0.036, 0.004), 0.0045, 0.0022, white, root, normal='X')
    # screw plate: white egg plate, clear hook, two screws
    p = bpy.data.objects.new('plate', None); link(p, root); p.location = (0.06, 0.0, 0)
    puck('plate', 0.011, 0.016, 0.1, 0.006, white, 0.0, p, bevel=0.002)
    for sy in (-0.008, 0.008):
        torus('screw', (0, sy, 0.0062), 0.0012, 0.0011, mat('soft', 'black'), p)
    tube('parm', [(0, 0.0, 0.0035), (0, 0.03, 0.0035), (0, 0.036, 0.003)], clear, p, squash=0.9)
    torus('pend', (0, 0.033, 0.0042), 0.0042, 0.0022, clear, p, normal='X')
    root.location = loc; root.rotation_euler.z = rotz
    return root


# ---------------------------------------------------------------- scene
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 16 if QUICK else 40
    sc.cycles.adaptive_threshold = 0.03
    sc.render.resolution_percentage = 40 if QUICK else 80
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 10; sc.cycles.transmission_bounces = 10
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = -0.6
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = lin('#f7f1ec'); bg.inputs[1].default_value = 0.35
    # shadow catcher floor
    bpy.ops.mesh.primitive_plane_add(size=6)
    fl = bpy.context.active_object; fl.is_shadow_catcher = True
    # soft studio lights
    def area(name, loc, size, power, col='#ffffff'):
        L = bpy.data.lights.new(name, 'AREA'); L.size = size; L.energy = power; L.color = lin(col)[:3]
        o = bpy.data.objects.new(name, L); bpy.context.collection.objects.link(o)
        o.location = loc; d = Vector((0, 0, 0)) - Vector(loc)
        o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    area('key', (-0.9, -0.6, 1.4), 1.4, 150, '#fff6ee')
    area('fill', (1.1, -0.3, 0.8), 1.6, 45, '#eef4ff')
    area('rim', (0.2, 1.2, 0.7), 0.9, 70)


def camera(target, dist, tilt_deg=38, yaw_deg=0, lens=85, res=(1000, 1250)):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    cam = bpy.data.cameras.new('cam'); cam.lens = lens
    o = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(o); sc.camera = o
    tilt = math.radians(tilt_deg); yaw = math.radians(yaw_deg)
    off = Vector((math.sin(yaw) * math.sin(tilt), -math.cos(yaw) * math.sin(tilt), math.cos(tilt))) * dist
    o.location = Vector(target) + off
    o.rotation_euler = (Vector(target) - o.location).to_track_quat('-Z', 'Y').to_euler()


def fit(tilt_deg=34, yaw_deg=0, lens=85, res=(1000, 1250), margin=1.14):
    """Point the camera from the given angle and frame every object in view."""
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    cam = bpy.data.cameras.new('cam'); cam.lens = lens
    o = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(o); sc.camera = o
    tilt = math.radians(tilt_deg); yaw = math.radians(yaw_deg)
    d = Vector((math.sin(yaw) * math.sin(tilt), -math.cos(yaw) * math.sin(tilt), math.cos(tilt)))
    o.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    coords = []
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH' or ob.is_shadow_catcher: continue
        ev = ob.evaluated_get(dg)
        for c in ev.bound_box: coords.extend(ev.matrix_world @ Vector(c))
    loc, _ = o.camera_fit_coords(dg, coords)
    o.location = loc
    cam.lens = lens / margin


def render(name):
    p = os.path.join(OUT, name + ('-q' if QUICK else '') + '.png')
    bpy.context.scene.render.filepath = p
    bpy.ops.render.render(write_still=True)
    print('WROTE', p, flush=True)


# ---------------------------------------------------------------- shots
def shot_hero():
    reset()
    product('reach', 'reach', 'body', 'yellow', 'white', loc=(-0.2, 0.16, 0), rotz=math.radians(26))
    product('pebble', 'pebble', 'face', 'pink', 'pink', loc=(0.04, 0.06, 0), rotz=math.radians(6))
    product('easy', 'easy', 'scalp', 'blue', 'white', loc=(0.14, 0.09, 0), rotz=math.radians(14))
    product('mini', 'mini', 'soft', 'rainbow', 'rainbow', loc=(0.26, 0.01, 0), rotz=math.radians(-8))
    fit(tilt_deg=24, lens=70, res=(1800, 1260), margin=1.06)
    render('hero')


def shot_handle(kind):
    reset()
    cfg = {'pebble': ('body', 'white', 'pink', -0.04, 0.42), 'reach': ('body', 'white', 'blue', -0.16, 0.95),
           'easy': ('scalp', 'white', 'yellow', -0.05, 0.52), 'mini': ('soft', 'white', 'rainbow', -0.02, 0.36)}[kind]
    hk, hc, gc, ty, dist = cfg
    rot = math.radians({'pebble': -18, 'reach': -10, 'easy': -26, 'mini': -18}[kind])
    product(kind, kind, hk, hc, gc, rotz=rot)
    fit(tilt_deg=34, lens=85, res=(1000, 1250))
    render('handle-' + kind)


HEAD_COL = {'body': 'pink', 'soft': 'blue', 'scalp': 'yellow', 'face': 'white', 'mesh': 'mint',
            'cloth': 'blue', 'crease': 'pink', 'intimate': 'lilac'}


def shot_head(kind):
    reset()
    lone_head(kind, kind, HEAD_COL[kind], rotz=math.radians(-20))
    c = Vector((0, 0.05 if kind != 'crease' else 0.055, 0)); c.rotate(Matrix.Rotation(math.radians(-20), 3, 'Z'))
    camera((c.x, c.y, 0.01), 0.42, tilt_deg=42, yaw_deg=-10, lens=85, res=(1000, 1250))
    render('head-' + kind)


def shot_click():
    reset()
    product('click', 'pebble', 'body', 'blue', 'white', rotz=math.radians(-62), gap=0.028)
    fit(tilt_deg=40, yaw_deg=-12, lens=85, res=(1600, 1000), margin=1.22)
    render('click')


def shot_hooks():
    reset()
    hooks(loc=(-0.03, -0.015, 0), rotz=math.radians(-15))
    fit(tilt_deg=40, lens=85, res=(1000, 1250), margin=1.3)
    render('hooks')


def shot_colours():
    reset()
    cols = ['pink', 'blue', 'yellow', 'black', 'white', 'rainbow']
    for i, c in enumerate(cols):
        product('c' + c, 'pebble', 'body', c, c, loc=(-0.2 + i * 0.08, 0.0, 0))
    fit(tilt_deg=36, lens=70, res=(2000, 1100), margin=1.08)
    render('colours')


def shot_set(name):
    reset()
    if name == 'starter':
        product('a', 'pebble', 'body', 'pink', 'pink', loc=(-0.05, 0.0, 0), rotz=math.radians(-10))
        lone_head('b', 'soft', 'pink', loc=(0.06, 0.02, 0), rotz=math.radians(15))
        hooks(loc=(0.03, -0.11, 0), rotz=math.radians(-80))
        fit(tilt_deg=32, lens=85, res=(1000, 1250))
    elif name == 'back':
        product('a', 'reach', 'body', 'blue', 'white', loc=(-0.02, 0.18, 0), rotz=math.radians(-18))
        lone_head('b', 'mesh', 'blue', loc=(0.09, 0.15, 0), rotz=math.radians(12))
        hooks(loc=(0.09, -0.06, 0), rotz=math.radians(-80))
        fit(tilt_deg=30, lens=85, res=(1000, 1250))
    elif name == 'family':
        product('a', 'pebble', 'body', 'pink', 'pink', loc=(-0.12, 0.0, 0))
        product('b', 'pebble', 'scalp', 'blue', 'blue', loc=(-0.04, 0.02, 0))
        product('c', 'reach', 'body', 'yellow', 'white', loc=(0.06, 0.2, 0), rotz=math.radians(-6))
        product('d', 'mini', 'soft', 'rainbow', 'rainbow', loc=(0.15, 0.0, 0))
        fit(tilt_deg=30, lens=85, res=(1000, 1250))
    elif name == 'care':
        product('a', 'easy', 'crease', 'mint', 'white', loc=(-0.06, 0.04, 0), rotz=math.radians(-12))
        product('b', 'reach', 'soft', 'lilac', 'white', loc=(0.07, 0.2, 0), rotz=math.radians(-6))
        lone_head('c', 'cloth', 'mint', loc=(0.12, -0.04, 0), rotz=math.radians(18))
        fit(tilt_deg=30, lens=85, res=(1000, 1250))
    render('set-' + name)


SHOTS = {'hero': shot_hero, 'click': shot_click, 'hooks': shot_hooks, 'colours': shot_colours}
for k in ('pebble', 'reach', 'easy', 'mini'): SHOTS['handle-' + k] = (lambda k=k: shot_handle(k))
for k in HEAD_COL: SHOTS['head-' + k] = (lambda k=k: shot_head(k))
for k in ('starter', 'back', 'family', 'care'): SHOTS['set-' + k] = (lambda k=k: shot_set(k))

if __name__ == '__main__':
    names = sys.argv[1:] or ['hero']
    if names == ['all']: names = list(SHOTS)
    for n in names: SHOTS[n]()
