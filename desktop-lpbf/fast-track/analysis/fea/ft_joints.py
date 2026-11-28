"""Joint compliance of the g3 gantry (#260, PR 294 round 3): the frame of ft_struct.py case 4c_model with bolted joints
modelled as springs instead of bonded, the head's rotary inertia, and a mesh check.

The bonded model (ft_struct.gantry_model_case, P['gantry'] = 'four_post_braced_front_g3', 62.0 / 100.6 / 179.4 Hz at 10 mm)
fragments every member into one conformal mesh, so each joint is as stiff as solid metal. Here each member is meshed on
its own instead (posts, cross-beams and braces one group each; the head mount on the entrance side, flange plate + angle
brackets + top flange + gussets, bonded inside itself; the far-side plate + its brackets likewise). Wherever two groups
touch or overlap, each side's nodes in the contact zone are tied to a rigid patch (*RIGID BODY), and the two patches'
reference nodes are joined by springs: three translational (kt, N/mm) and three rotational (kr, N mm/rad; in CalculiX a
rigid body's rotations are its ROT node's translations, so a SPRING2 between two ROT nodes is a moment spring). The post
feet (and the diagonals' held lower ends) are either fixed, as in the bonded model, or rigid patches on springs to ground
(the bench mounting). Very stiff springs reproduce the bonded model (rigid patches stiffen it a little); that run is the
reference for the sweep.

The head (5.8 kg housing, 206.9 x 140 x 180 mm) and the LINOS objective (1.34 kg, Ø119.8 x 48.6 mm) are one rigid body on
both support plates, as in ft_struct. 'point': all the mass at the centre of mass (ft_struct's model); 'inertia': the
housing as 8 points of m/8 at (+-a, +-b, +-c)/(2 sqrt 3) about its centre and the lens as two rings of 4 points at radius
R/sqrt 2 and +-h/(2 sqrt 3), which give a uniform box's and a uniform cylinder's mass, centre and inertia (estimates:
the real mass distribution is not published).

Run:  cd <repo> && OMP_NUM_THREADS=2 /tmp/tools/capmem 4 /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/fea/ft_joints.py <cmd>
  bonded <hmax> <point|inertia>     the bonded g3 model (mesh check, inertia check)
  sweep <hmax>                      the joint model on one mesh, every stiffness case in SWEEP
  variant <name> <hmax>             a geometric option (extra braces), with the joint model
  plot                              struct-joints-mode1.png from struct-joints.json
Scratch goes to /tmp/r3-fea-joints/struct (env FT_STRUCT_RUN); results to analysis/out/fea/struct-joints.json.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import sys
import time

os.environ.setdefault("FT_STRUCT_RUN", "/tmp/r3-fea-joints/struct")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
import cadquery as cq  # noqa: E402
import ft_struct as S  # noqa: E402

M, P = S.M, S.P
OUT = S.OUT
RUN = S.RUN
JSON = OUT / "struct-joints.json"
D_TOL = 0.05          # mm: a node within this of the other member's (filled) envelope is in the contact zone

# Stiffness cases for the sweep. kr in N mm/rad, kt in N/mm; 'frame' = beam-post, brace ends, head mount to beams;
# 'base' = the post feet and the diagonals' lower ends on the bench (None = fixed, as in the bonded model).
STIFF = 1.0e12        # "rigid" rotational spring, N mm/rad
STIFF_T = 1.0e7       # "rigid" translational spring, N/mm


def case(kr, kt, kr_base=None, kt_base=None, kr_by=None, kt_by=None):
    return dict(kr=kr, kt=kt, kr_base=kr_base, kt_base=kt_base, kr_by=kr_by or {}, kt_by=kt_by or {})


SWEEP = {
    "stiff": case(STIFF, STIFF_T),
    "kr1e8_kt2e4": case(1e8, 2e4),
    "kr3e7_kt2e4": case(3e7, 2e4),
    "kr1e7_kt2e4": case(1e7, 2e4),
    "kr3e6_kt2e4": case(3e6, 2e4),
    "kr1e6_kt2e4": case(1e6, 2e4),
    "kr3e5_kt2e4": case(3e5, 2e4),
    "kr1e7_kt5e3": case(1e7, 5e3),
    "kr1e7_kt1e5": case(1e7, 1e5),
    "kr1e7_ktstiff": case(1e7, STIFF_T),
    "krstiff_kt2e4": case(STIFF, 2e4),
    "kr1e7_kt2e4_base1e7": case(1e7, 2e4, 1e7, 2e4),
    "kr3e6_kt2e4_base3e6": case(3e6, 2e4, 3e6, 2e4),
    "kr1e6_kt2e4_base1e6": case(1e6, 2e4, 1e6, 2e4),
    # hardware options at the realistic baseline (kr 3e6, kt 2e4): stiffer joints where they matter
    "kr3e6_beampost1e8": case(3e6, 2e4, kr_by={"beam-post": 1e8}),
    "kr3e6_braces1e8": case(3e6, 2e4, kr_by={"brace": 1e8}, kt_by={"brace": 1e5}),
    "kr3e6_mount1e8": case(3e6, 2e4, kr_by={"mount": 1e8}, kt_by={"mount": 1e5}),
    # the translational stiffness turned out to matter most (the braces work axially through their end joints)
    "kr3e6_kt1e5": case(3e6, 1e5),
    "kr3e6_bracekt1e5": case(3e6, 2e4, kt_by={"brace": 1e5}),
    "kr3e6_braces_rigid": case(3e6, 2e4, kr_by={"brace": STIFF}, kt_by={"brace": STIFF_T}),
    "kr3e6_braces1e8_beampost1e8": case(3e6, 2e4, kr_by={"brace": 1e8, "beam-post": 1e8}, kt_by={"brace": 1e5, "beam-post": 1e5}),
    "krstiff_kt5e4": case(STIFF, 5e4),
    "krstiff_kt1e5": case(STIFF, 1e5),
}


# --------------------------------------------------------------------------------------------
# geometry: the g3 frame as ft_struct.gantry_model_case builds it, in groups
# --------------------------------------------------------------------------------------------
def rtube(p0, p1, r_in):
    A_, B_ = cq.Vector(*p0), cq.Vector(*p1)
    dd = B_ - A_
    return cq.Solid.makeCylinder(15.0, dd.Length, A_, dd.normalized()).cut(cq.Solid.makeCylinder(r_in, dd.Length, A_, dd.normalized()))


def g3_geometry(extra_braces=()):
    parts = M.build("FT-1")
    if M.P.get("gantry") != "four_post_braced_front_g3":
        raise RuntimeError(f"model gantry is {M.P.get('gantry')!r}, expected 'four_post_braced_front_g3'")
    L = M.levels("FT-1")
    sec = S.tslot_section()
    eq = S.equivalent_tube(sec["Ixx"], sec["A"])
    eq45 = S.equivalent_tube(S.I_TSLOT45, S.A_TSLOT45, s=45.0)
    al = S.MAT["al6061"]
    frame30 = dict(al, rho=al["rho"] * eq["rho_scale"])
    frame45 = dict(al, rho=al["rho"] * eq45["rho_scale"])
    posts = []
    for s_ in S.part(parts, "Gantry uprights").shape.Solids():
        bb = s_.BoundingBox()
        c = ((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2)
        for g_ in posts:
            if abs(g_["c"][0] - c[0]) < 40 and abs(g_["c"][1] - c[1]) < 40:
                b_ = g_["bb"]
                g_["bb"] = [min(b_[0], bb.xmin), max(b_[1], bb.xmax), min(b_[2], bb.ymin), max(b_[3], bb.ymax), min(b_[4], bb.zmin), max(b_[5], bb.zmax)]
                break
        else:
            posts.append(dict(c=c, bb=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]))
    assert len(posts) == 4, len(posts)
    G = []
    for k, g_ in enumerate(posts):
        G.append(dict(name=f"post {k} ({'back' if g_['c'][1] > 0 else 'front'} {'left' if g_['c'][0] < 0 else 'right'})", kind="post",
                      bodies=[(f"post {k}", S.tube_box(*g_["bb"], eq45["t"], "z"))], mats=[frame45], env=("box", tuple(g_["bb"]))))
    for nm, tag in (("Gantry cross-beam (clamped", "back beam"), ("Gantry cross-beam, front", "front beam")):
        bb = S.part(parts, nm).shape.BoundingBox()
        bbl = (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
        G.append(dict(name=tag, kind="beam", bodies=[(tag, S.tube_box(*bbl, eq["t"], "x"))], mats=[frame30], env=("box", bbl)))
    r_in = (30.0 ** 4 - 64 * S.I_TSLOT / math.pi) ** 0.25 / 2
    held = []
    back_front_face = min(g_["bb"][2] for g_ in posts if g_["c"][1] > 0)
    brace_solids = list(S.part(parts, "Gantry braces").shape.Solids())
    if any(p_.name.startswith("Gantry knee braces, front") for p_ in parts):
        brace_solids += list(S.part(parts, "Gantry knee braces, front").shape.Solids())
    for k, s_ in enumerate(brace_solids):
        V = np.array([v.toTuple() for v in s_.Vertices()])
        C = np.array(s_.Center().toTuple())
        d = np.linalg.svd(V - V.mean(0))[2][0]
        pr = (V - C) @ d
        e0, e1 = C + pr.min() * d, C + pr.max() * d
        if e0[2] > e1[2]:
            e0, e1 = e1, e0
        d = (e1 - e0) / np.linalg.norm(e1 - e0)
        diag = np.linalg.norm(e1 - e0) > 400
        if diag:
            t_ = (back_front_face - e0[1]) / d[1] if abs(d[1]) > 1e-6 else 0.0
            p0 = e0 + min(t_, 0.0) * d if t_ < 0 else e0 - 20.0 * d
            held.append((p0.copy(), d.copy()))
        else:
            p0 = e0 - 20.0 * d
        p1 = e1 + 20.0 * d
        G.append(dict(name=f"{'diagonal' if diag else 'knee brace'} {k}", kind="brace", bodies=[(f"brace {k}", rtube(p0, p1, r_in))],
                      mats=[frame30], env=("cyl", (p0, p1, 15.0)), ends=(p0.round(1).tolist(), p1.round(1).tolist())))
    for k, (p0, p1) in enumerate(extra_braces):
        p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
        G.append(dict(name=f"added brace {k}", kind="brace", bodies=[(f"added brace {k}", rtube(p0, p1, r_in))], mats=[frame30],
                      env=("cyl", (p0, p1, 15.0)), ends=(p0.round(1).tolist(), p1.round(1).tolist())))
    fl = S.part(parts, "Scan-head flange plate (MK-09)").shape
    near = [("flange plate", fl), ("angle brackets", S.part(parts, "Flange-to-beam angle brackets (MK-09)").shape)]
    for nm in ("Head-plate top flange", "Head-plate gussets"):
        near.append((nm, S.part(parts, nm).shape))
    far = [(nm, S.part(parts, nm).shape) for nm in ("Head far-side support plate", "Far-side support angle brackets")]
    G.append(dict(name="head mount, entrance side (MK-09 flange plate, brackets, top flange, gussets)", kind="mount", bodies=near,
                  mats=[al] * len(near), env=("mesh", None)))
    G.append(dict(name="head mount, far side (support plate and brackets)", kind="mount", bodies=far, mats=[al] * len(far), env=("mesh", None)))
    hbb = S.part(parts, "SCANLAB hurrySCAN").shape.BoundingBox()
    fbb = fl.BoundingBox()
    xbb = S.part(parts, "Head far-side support plate").shape.BoundingBox()
    ax_xy = P["axis_off"]
    c_head = np.array([(hbb.xmin + hbb.xmax) / 2, (hbb.ymin + hbb.ymax) / 2, (hbb.zmin + hbb.zmax) / 2])
    c_lens = np.array([ax_xy[0], ax_xy[1], (S.LENS["flange_z"] + L["lens_bot"]) / 2])
    head = dict(hbb=(hbb.xmin, hbb.xmax, hbb.ymin, hbb.ymax, hbb.zmin, hbb.zmax), fbb=(fbb.xmin, fbb.xmax, fbb.ymin, fbb.ymax, fbb.zmin, fbb.zmax),
                xbb=(xbb.xmin, xbb.xmax, xbb.ymin, xbb.ymax, xbb.zmin, xbb.zmax), c_head=c_head, c_lens=c_lens,
                lens_h=S.LENS["flange_z"] - L["lens_bot"], lens_r=P["lens_d"] / 2)
    return dict(G=G, held=held, posts=posts, head=head)


# --------------------------------------------------------------------------------------------
# meshes
# --------------------------------------------------------------------------------------------
def merge(meshes):
    ntags, xyz, tets, body, ngroup, surfs = [], [], [], [], [], {}
    off = boff = soff = 0
    for gi, m in enumerate(meshes):
        new = np.arange(1, len(m["ntags"]) + 1, dtype=np.int64) + off
        remap = np.zeros(int(m["ntags"].max()) + 1, dtype=np.int64)
        remap[m["ntags"]] = new
        ntags.append(new)
        xyz.append(m["xyz"])
        tets.append(remap[m["tets"]])
        body.append(m["body"] + boff)
        ngroup.append(np.full(len(new), gi, dtype=np.int64))
        for t, s in m["surfs"].items():
            surfs[soff + t] = dict(bb=s["bb"], tri=remap[s["tri"]], nvol=s["nvol"], group=gi)
        off += len(new)
        boff += int(m["body"].max()) + 1
        soff += max(m["surfs"]) + 1
    ntags = np.concatenate(ntags)
    idx = np.full(off + 1, -1, dtype=np.int64)
    idx[ntags] = np.arange(len(ntags))
    m = dict(name="merged", ntags=ntags, xyz=np.vstack(xyz), idx=idx, tets=np.vstack(tets), body=np.concatenate(body),
             ngroup=np.concatenate(ngroup), surfs=surfs)
    m["faces"] = S.face_index(m)
    return m


def mesh_model(geo, hmax, bonded, tag):
    G = geo["G"]
    mats = [mt for g in G for mt in g["mats"]]
    if bonded:
        bodies = [b for g in G for b in g["bodies"]]
        m = S.mesh_bodies(bodies, f"j_bonded_{tag}", hmax=hmax, hmin=1.5, curv=8)
    else:
        meshes = []
        for gi, g in enumerate(G):
            meshes.append(S.mesh_bodies(g["bodies"], f"j_{tag}_g{gi}", hmax=hmax, hmin=1.5, curv=8))
        m = merge(meshes)
        print(f"  merged: {len(m['ntags'])} nodes, {len(m['tets'])} C3D10, {len(G)} groups")
    return m, mats


def head_nodes(m, geo):
    """FOOT: the flange plate's +x face and the far plate's -x face under the head's footprint (as ft_struct)."""
    h = geo["head"]
    hb, fb, xb = h["hbb"], h["fbb"], h["xbb"]
    foot = S.nodes_on(m, S.surfaces(m, S.planar("x", fb[1])), lambda q: (q[:, 1] >= hb[2]) & (q[:, 1] <= hb[3]) & (q[:, 2] >= max(hb[4], fb[4])))
    foot = np.union1d(foot, S.nodes_on(m, S.surfaces(m, S.planar("x", xb[0])),
                                       lambda q: (q[:, 1] >= hb[2]) & (q[:, 1] <= hb[3]) & (q[:, 2] >= max(hb[4], xb[4]))))
    return foot


def feet_nodes(m, geo):
    """Fixed nodes of the bonded model: each post's bottom face, and the end ring of each diagonal's held lower end.
    Returns {post index: tags} so that each foot can be one patch."""
    out = {}
    for k, g_ in enumerate(geo["posts"]):
        x0, x1, y0, y1, z0, _ = g_["bb"]
        ids = S.nodes_on(m, S.surfaces(m, S.planar("z", z0)), lambda q: (q[:, 0] >= x0 - 0.1) & (q[:, 0] <= x1 + 0.1) & (q[:, 1] >= y0 - 0.1) & (q[:, 1] <= y1 + 0.1))
        out[k] = ids
    for bp, bd in geo["held"]:
        rel = m["xyz"] - bp
        s_ax = rel @ bd
        rad = np.linalg.norm(rel - np.outer(s_ax, bd), axis=1)
        ring = m["ntags"][(np.abs(s_ax) < 0.3) & (rad < 15.2)]
        k = int(np.argmin([math.hypot(g_["c"][0] - bp[0], g_["c"][1] - bp[1]) for g_ in geo["posts"]]))
        out[k] = np.union1d(out[k], ring)
    return out


# --------------------------------------------------------------------------------------------
# joints: contact zones between groups
# --------------------------------------------------------------------------------------------
def group_trimesh(m, gi):
    import trimesh
    tri = np.vstack([s["tri"][:, :3] for s in m["surfs"].values() if s.get("group") == gi and s["nvol"] == 1])
    rows = m["idx"][tri]
    used, inv = np.unique(rows, return_inverse=True)
    return trimesh.Trimesh(vertices=m["xyz"][used], faces=inv.reshape(-1, 3), process=False)


def inside_env(env, pts, d, tm=None):
    kind, data = env
    if kind == "box":
        x0, x1, y0, y1, z0, z1 = data
        return ((pts[:, 0] >= x0 - d) & (pts[:, 0] <= x1 + d) & (pts[:, 1] >= y0 - d) & (pts[:, 1] <= y1 + d)
                & (pts[:, 2] >= z0 - d) & (pts[:, 2] <= z1 + d))
    if kind == "cyl":
        p0, p1, r = data
        p0, p1 = np.asarray(p0), np.asarray(p1)
        ax = p1 - p0
        Lx = np.linalg.norm(ax)
        u = ax / Lx
        rel = pts - p0
        s = rel @ u
        rad = np.linalg.norm(rel - np.outer(s, u), axis=1)
        return (s >= -d) & (s <= Lx + d) & (rad <= r + d)
    import trimesh
    lo, hi = tm.bounds[0] - 1.0, tm.bounds[1] + 1.0
    cand = np.all((pts >= lo) & (pts <= hi), axis=1)
    out = np.zeros(len(pts), dtype=bool)
    if cand.any():
        sd = trimesh.proximity.signed_distance(tm, pts[cand])      # > 0 inside
        out[cand] = sd >= -d
    return out


def joint_class(ka, kb):
    s = {ka, kb}
    if s == {"beam", "post"}:
        return "beam-post"
    if "brace" in s:
        return "brace"
    if "mount" in s:
        return "mount"
    return "other"


def find_joints(m, geo, exclude):
    G = geo["G"]
    tms = {gi: group_trimesh(m, gi) for gi, g in enumerate(G) if g["env"][0] == "mesh"}
    used = set(map(int, exclude))
    joints = []
    for a in range(len(G)):
        for b in range(a + 1, len(G)):
            na = m["ntags"][m["ngroup"] == a]
            nb = m["ntags"][m["ngroup"] == b]
            pa = m["xyz"][m["idx"][na]]
            pb = m["xyz"][m["idx"][nb]]
            ina = inside_env(G[b]["env"], pa, D_TOL, tms.get(b))
            inb = inside_env(G[a]["env"], pb, D_TOL, tms.get(a))
            A = [int(t) for t in na[ina] if int(t) not in used]
            B = [int(t) for t in nb[inb] if int(t) not in used]
            if len(A) < 3 or len(B) < 3:
                if len(A) or len(B):
                    print(f"  pair {G[a]['name']} / {G[b]['name']}: {len(A)} / {len(B)} nodes, not a joint")
                continue
            used.update(A)
            used.update(B)
            c = np.vstack([m["xyz"][m["idx"][A]], m["xyz"][m["idx"][B]]]).mean(0)
            cls = joint_class(G[a]["kind"], G[b]["kind"])
            joints.append(dict(a=a, b=b, A=np.array(A), B=np.array(B), c=c, cls=cls, name=f"{G[a]['name']} / {G[b]['name']}"))
            print(f"  joint {cls:9s} {G[a]['name'][:28]:28s} / {G[b]['name'][:28]:28s}: {len(A)} + {len(B)} nodes at {c.round(0).tolist()}")
    return joints


# --------------------------------------------------------------------------------------------
# CalculiX input
# --------------------------------------------------------------------------------------------
def head_mass_lines(geo, ref, first_node, first_el, inertia):
    """Extra nodes and MASS elements for the head. Returns (node lines, element+mass lines, node tags, cm)."""
    h = geo["head"]
    mh, ml = S.HEAD["mass"], S.LENS["mass"]
    cm = (mh * h["c_head"] + ml * h["c_lens"]) / (mh + ml)
    nodes, els, tags = [], [], []
    if not inertia:
        els.append(f"*ELEMENT, TYPE=MASS, ELSET=MHEAD\n{first_el},{ref}\n*MASS, ELSET=MHEAD\n{(mh + ml) * 1e-3:.6E}\n")
        return "", "".join(els), [], cm
    a, b, c = S.HEAD["size"]
    k = first_node
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                pts.append((h["c_head"] + np.array([sx * a, sy * b, sz * c]) / (2 * math.sqrt(3)), mh / 8))
    R, hh = h["lens_r"], h["lens_h"]
    for sz in (-1, 1):
        for q in range(4):
            ang = q * math.pi / 2 + math.pi / 4
            pts.append((h["c_lens"] + np.array([R / math.sqrt(2) * math.cos(ang), R / math.sqrt(2) * math.sin(ang), sz * hh / (2 * math.sqrt(3))]), ml / 8))
    e = first_el
    ml_lines = []
    for p, mass in pts:
        nodes.append(f"{k},{p[0]:.6f},{p[1]:.6f},{p[2]:.6f}\n")
        tags.append(k)
        ml_lines.append(f"*ELEMENT, TYPE=MASS, ELSET=MH{e}\n{e},{k}\n*MASS, ELSET=MH{e}\n{mass * 1e-3:.6E}\n")
        k += 1
        e += 1
    return "".join(nodes), "".join(ml_lines), tags, cm


def write_inp(job, m, mats, foot, feet, joints, stiff, inertia):
    """stiff: None for the bonded model (no joints), else a case() dict."""
    RUN.mkdir(parents=True, exist_ok=True)
    ne = len(m["tets"])
    nmax = int(m["ntags"].max())
    nxt = nmax + 1
    lines_nodes, lines_extra, lines_bc = [], [], []
    ref, rot = nxt, nxt + 1
    nxt += 2
    hn, hm, htags, cm = head_mass_lines(geo_cache["geo"], ref, nxt + 100, ne + 1, inertia)
    nxt += 100 + 16
    el = ne + 1 + 16
    lines_nodes.append(f"{ref},{cm[0]:.6f},{cm[1]:.6f},{cm[2]:.6f}\n{rot},{cm[0]:.6f},{cm[1]:.6f},{cm[2]:.6f}\n")
    lines_nodes.append(hn)
    lines_extra.append(S.nset("FOOT", list(foot) + htags))
    lines_extra.append(f"*RIGID BODY, NSET=FOOT, REF NODE={ref}, ROT NODE={rot}\n")
    lines_extra.append(hm)
    springs = {}       # (elset) -> (dof, k, [(n1, n2)]) for SPRING2; SPRING1 keyed separately

    def add_spring(name, dof, k, n1, n2=None):
        key = (name, dof, k, n2 is None)
        springs.setdefault(key, []).append((n1, n2))
    if stiff is None or stiff.get("kr_base") is None:
        allfeet = np.unique(np.concatenate(list(feet.values())))
        lines_extra.append(S.nset("FEET", allfeet))
        lines_bc.append("FEET,1,3\n")
    else:
        for k_, ids in feet.items():
            c = m["xyz"][m["idx"][ids]].mean(0)
            r1, r2 = nxt, nxt + 1
            nxt += 2
            lines_nodes.append(f"{r1},{c[0]:.6f},{c[1]:.6f},{c[2]:.6f}\n{r2},{c[0]:.6f},{c[1]:.6f},{c[2]:.6f}\n")
            lines_extra.append(S.nset(f"FT{k_}", ids) + f"*RIGID BODY, NSET=FT{k_}, REF NODE={r1}, ROT NODE={r2}\n")
            for d in (1, 2, 3):
                add_spring("BT", d, stiff["kt_base"], r1)
                add_spring("BR", d, stiff["kr_base"], r2)
    if stiff is not None:
        for j, jt in enumerate(joints):
            refs = []
            for side in ("A", "B"):
                r1, r2 = nxt, nxt + 1
                nxt += 2
                c = jt["c"]
                lines_nodes.append(f"{r1},{c[0]:.6f},{c[1]:.6f},{c[2]:.6f}\n{r2},{c[0]:.6f},{c[1]:.6f},{c[2]:.6f}\n")
                lines_extra.append(S.nset(f"J{j}{side}", jt[side]) + f"*RIGID BODY, NSET=J{j}{side}, REF NODE={r1}, ROT NODE={r2}\n")
                refs.append((r1, r2))
            kr = stiff["kr_by"].get(jt["cls"], stiff["kr"])
            kt = stiff["kt_by"].get(jt["cls"], stiff["kt"])
            for d in (1, 2, 3):
                add_spring("JT", d, kt, refs[0][0], refs[1][0])
                add_spring("JR", d, kr, refs[0][1], refs[1][1])
    for i, ((name, dof, k, one), pairs) in enumerate(sorted(springs.items(), key=lambda kv: str(kv[0]))):
        es = f"S{name}{dof}_{i}"
        typ = "SPRING1" if one else "SPRING2"
        lines_extra.append(f"*ELEMENT, TYPE={typ}, ELSET={es}\n")
        for n1, n2 in pairs:
            lines_extra.append(f"{el},{n1}\n" if one else f"{el},{n1},{n2}\n")
            el += 1
        lines_extra.append(f"*SPRING, ELSET={es}\n{dof}\n{k:.6E}\n" if one else f"*SPRING, ELSET={es}\n{dof},{dof}\n{k:.6E}\n")
    eids = np.arange(1, ne + 1)
    with open(RUN / f"{job}.inp", "w") as f:
        f.write("*HEADING\nFT " + job + "\n*NODE, NSET=NALL\n")
        np.savetxt(f, np.column_stack([m["ntags"], m["xyz"]]), fmt=["%d", "%.6f", "%.6f", "%.6f"], delimiter=",")
        f.write("".join(lines_nodes))
        for k in np.unique(m["body"]):
            sel = m["body"] == k
            f.write(f"*ELEMENT, TYPE=C3D10, ELSET=B{k}\n")
            np.savetxt(f, np.column_stack([eids[sel], m["tets"][sel]]), fmt="%d", delimiter=",")
        f.write("".join(lines_extra))
        for k in np.unique(m["body"]):
            mat = mats[int(k)]
            f.write(f"*MATERIAL, NAME=M{k}\n*ELASTIC\n{mat['E']},{mat['nu']}\n*DENSITY\n{mat['rho'] * 1e-12:.5e}\n")
            f.write(f"*SOLID SECTION, ELSET=B{k}, MATERIAL=M{k}\n")
        if lines_bc:
            f.write("*BOUNDARY\n" + "".join(lines_bc))
        f.write("*STEP\n*FREQUENCY, SOLVER=SPOOLES\n6\n*NODE FILE\nU\n*END STEP\n")
    return cm


geo_cache = {}


def modal(job, m, mats, foot, feet, joints, stiff, inertia):
    cm = write_inp(job, m, mats, foot, feet, joints, stiff, inertia)
    t = S.run_ccx(job)
    f = S.read_freqs(job)
    modes = []
    names = ("x (along the cross-beams)", "y (fore-aft)", "z (vertical)")
    G = geo_cache["geo"]["G"]
    ng = m.get("ngroup")
    for k, blk in enumerate([x for x in S.read_frd(job) if x["name"] == "DISP"][:6]):
        Um = S.field(m, blk, 3)
        ur, tr = S.rigid_fit(m, Um, foot, cm)
        mag = np.linalg.norm(Um, axis=1)
        j = int(np.argmax(mag))
        md = dict(f_hz=f[k] if k < len(f) else None, head_translation_dir=(np.asarray(ur) / (np.linalg.norm(ur) + 1e-30)).round(2).tolist(),
                  head_rotation_dir=(np.asarray(tr) / (np.linalg.norm(tr) + 1e-30)).round(2).tolist(),
                  max_at=m["xyz"][j].round(0).tolist(), dominant_head_axis=names[int(np.argmax(np.abs(ur)))],
                  head_share=float(np.linalg.norm(ur) / (mag.max() + 1e-30)))
        if ng is not None:
            md["max_in"] = G[int(ng[j])]["name"]
        modes.append(md)
    return dict(freqs_hz=[round(x, 2) for x in f], modes=modes, ccx_s=round(t), nodes=int(len(m["ntags"])), elements=int(len(m["tets"])))


def load_json():
    return json.loads(JSON.read_text()) if JSON.exists() else {"runs": {}}


def save_run(key, r):
    R = load_json()
    R["runs"][key] = r
    R["meta"] = dict(
        model="CAD v2, P['gantry'] = 'four_post_braced_front_g3' (ft_struct.py case 4c_model geometry)",
        method="members meshed separately; contact zones tied to rigid patches joined by 3 translational (kt, N/mm) and 3 rotational "
               "(kr, N mm/rad) springs; feet fixed or on springs to ground; head + lens one rigid body on both support plates",
        head=S.HEAD, lens=S.LENS, sweep_cases={k: v for k, v in SWEEP.items()})
    JSON.write_text(json.dumps(R, indent=1, default=float))


def cmd_bonded(hmax, which):
    """which: 'point', 'inertia' or 'both' (one mesh)."""
    geo = g3_geometry()
    geo_cache["geo"] = geo
    m, mats = mesh_model(geo, hmax, True, f"h{hmax:g}")
    foot = head_nodes(m, geo)
    feet = feet_nodes(m, geo)
    for inertia in ((False, True) if which == "both" else (which == "inertia",)):
        key = f"bonded_h{hmax:g}_{'inertia' if inertia else 'point'}"
        r = modal(key, m, mats, foot, feet, [], None, inertia)
        r.update(kind="bonded", hmax=hmax, inertia=inertia, utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=S.model_commit())
        save_run(key, r)
        print(f"  {key}: {r['freqs_hz']}", flush=True)


def joint_model(hmax, extra_braces=(), tag="base"):
    geo = g3_geometry(extra_braces)
    geo_cache["geo"] = geo
    m, mats = mesh_model(geo, hmax, False, f"{tag}_h{hmax:g}")
    foot = head_nodes(m, geo)
    feet = feet_nodes(m, geo)
    excl = np.union1d(foot, np.concatenate(list(feet.values())))
    joints = find_joints(m, geo, excl)
    return geo, m, mats, foot, feet, joints


def describe_joints(geo, joints):
    return [dict(name=j["name"], cls=j["cls"], nodes=[int(len(j["A"])), int(len(j["B"]))], at=j["c"].round(1).tolist()) for j in joints]


def cmd_sweep(hmax, which=None):
    geo, m, mats, foot, feet, joints = joint_model(hmax)
    todo = which or list(SWEEP)
    for name in todo:
        st = SWEEP[name]
        key = f"joints_h{hmax:g}_{name}"
        r = modal(key, m, mats, foot, feet, joints, st, True)
        r.update(kind="joints", hmax=hmax, inertia=True, stiffness=st, n_joints=len(joints), joints=describe_joints(geo, joints),
                 utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=S.model_commit())
        save_run(key, r)
        print(f"  {key}: {r['freqs_hz']}", flush=True)


VARIANTS = {
    # a diagonal in the front portal (y = the front posts' centre plane), from the left post at z 160 to the right post at
    # z 285: under the front right knee brace (its lower end runs into the post at z 329), over MON3 (z <= 125 at x +-20)
    # and 60 mm over the latch (x -28); the box's front face is 43 mm behind the portal's centre plane
    "front_diagonal": lambda yf, yb, xl, xr: [((xl, yf, 160.0), (xr, yf, 285.0))],
}


def cmd_variant(name, hmax, cases=("kr3e6_kt2e4", "stiff")):
    geo0 = g3_geometry()
    posts = geo0["posts"]
    yf = np.mean([g_["c"][1] for g_ in posts if g_["c"][1] < 0])
    yb = np.mean([g_["c"][1] for g_ in posts if g_["c"][1] > 0])
    xl = np.mean([g_["c"][0] for g_ in posts if g_["c"][0] < 0])
    xr = np.mean([g_["c"][0] for g_ in posts if g_["c"][0] > 0])
    extra = VARIANTS[name](yf, yb, xl, xr)
    # the added braces end on the post axes, so they run into both posts
    geo, m, mats, foot, feet, joints = joint_model(hmax, extra, tag=name)
    for cname in cases:
        st = SWEEP[cname]
        key = f"variant_{name}_h{hmax:g}_{cname}"
        r = modal(key, m, mats, foot, feet, joints, st, True)
        r.update(kind="variant", variant=name, extra_braces=[[list(map(float, p0)), list(map(float, p1))] for p0, p1 in extra], hmax=hmax,
                 inertia=True, stiffness=st, n_joints=len(joints), joints=describe_joints(geo, joints),
                 utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=S.model_commit())
        save_run(key, r)
        print(f"  {key}: {r['freqs_hz']}", flush=True)


def cmd_plot(hmax=12):
    """Two panels on one frequency scale: modes 1-3 against the frame joints' rotational stiffness (kt 20 kN/mm; mode 1
    with the feet on the same springs dashed), and against their translational stiffness (kr 10 kN m/rad); the 60 Hz
    minimum, the bonded model's mode 1, and the estimated ranges for bolted T-slot hardware."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    R = load_json()["runs"]
    ink, ink2, grid, band = "#191919", "#666666", "#e6e6e6", "#f0f0f0"
    cols = ["#257de0", "#f47230", "#00b894"]           # categorical slots 1-3 (validated, light mode)
    RIG = 1000.0                                         # where "rigid" is drawn on each log axis

    def sel(pred):
        out = []
        for r in R.values():
            st = r.get("stiffness")
            if r.get("kind") == "joints" and r.get("hmax") == hmax and st and pred(st):
                out.append((st, r["freqs_hz"][:3]))
        return out
    plain = lambda st: not st["kr_by"] and not st["kt_by"]
    pa = sorted(((RIG if st["kr"] >= STIFF else st["kr"] / 1e6), f) for st, f in sel(lambda st: plain(st) and st["kt"] == 2e4 and st["kr_base"] is None))
    pb = sorted(((RIG if st["kt"] >= STIFF_T else st["kt"] / 1e3), f) for st, f in sel(lambda st: plain(st) and st["kr"] == 1e7 and st["kr_base"] is None))
    base = sorted((st["kr"] / 1e6, f[0]) for st, f in sel(lambda st: plain(st) and st["kr_base"] is not None))
    bonded = R.get(f"bonded_h{hmax:g}_inertia", {}).get("freqs_hz", [None])[0]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.9), dpi=140, sharey=True)
    ymax = max(f[2] for _, f in pa + pb) * 1.12

    def panel(ax, pts, xlabel, ticks, labels, bandx, bandtxt):
        ax.axvspan(*bandx, color=band, zorder=0, lw=0)
        ax.text((bandx[0] * bandx[1]) ** 0.5, 6, bandtxt, ha="center", va="bottom", color=ink2, fontsize=8.5)
        ax.axhline(60.0, color=ink2, lw=1.0, ls=(0, (4, 3)), zorder=1)
        if bonded:
            ax.axhline(bonded, color="#bdbdbd", lw=1.0, ls=(0, (1, 2)), zorder=1)
        xs = [p[0] for p in pts]
        for k in range(3):
            ys = [p[1][k] for p in pts]
            fin = [i for i, x in enumerate(xs) if x < RIG]
            ax.plot([xs[i] for i in fin], [ys[i] for i in fin], color=cols[k], lw=2.0, zorder=3, solid_capstyle="round", label=f"mode {k + 1}")
            if xs and xs[-1] == RIG and fin:
                ax.plot([xs[fin[-1]], xs[-1]], [ys[fin[-1]], ys[-1]], color=cols[k], lw=1.2, ls=(0, (1, 2)), zorder=2)
            ax.plot(xs, ys, ls="none", marker="o", ms=6.5, mfc=cols[k], mec="white", mew=1.5, zorder=4)
            ax.text(xs[-1] * 1.3, ys[-1], f"mode {k + 1}", color=ink, fontsize=9, va="center")
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
        ax.minorticks_off()
        ax.set_xlim(ticks[0] * 0.7, RIG * 4.0)
        ax.set_ylim(0, ymax)
        ax.set_xlabel(xlabel, color=ink, fontsize=9.5)
        ax.grid(axis="y", color=grid, lw=0.8)
        ax.set_axisbelow(True)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
        for s_ in ("left", "bottom"):
            ax.spines[s_].set_color("#bdbdbd")
        ax.tick_params(colors=ink2, labelsize=8.5)
    a0, a1 = axes
    panel(a0, pa, "rotational stiffness of every frame joint, kN·m/rad\n(translational 20 kN/mm, feet fixed)",
          [0.3, 1, 3, 10, 30, 100, RIG], ["0.3", "1", "3", "10", "30", "100", "rigid"], (1.0, 10.0), "single corner brackets\n(estimate)")
    if base:
        a0.plot([b[0] for b in base], [b[1] for b in base], color=cols[0], lw=2.0, ls=(0, (5, 3)), zorder=3, label="mode 1, feet on the same springs")
        a0.plot([b[0] for b in base], [b[1] for b in base], ls="none", marker="o", ms=6.5, mfc="white", mec=cols[0], mew=1.8, zorder=4)
        a0.text(base[0][0] * 0.9, base[0][1] - 3, "mode 1, feet on\nthe same springs", color=ink, fontsize=8.5, ha="right", va="top")
    panel(a1, pb, "translational stiffness of every frame joint, kN/mm\n(rotational 10 kN·m/rad, feet fixed)",
          [5, 20, 100, RIG], ["5", "20", "100", "rigid"], (10.0, 50.0), "bolted T-nut joints\n(estimate)")
    a0.text(0.24, 58.5, "60 Hz minimum", color=ink2, fontsize=8.5, va="top")
    if bonded:
        a1.text(3.8, bonded + 1.5, f"bonded model, mode 1 ({bonded:.1f} Hz)", color=ink2, fontsize=8.5, va="bottom")
    a0.set_ylabel("frequency, Hz", color=ink, fontsize=9.5)
    a0.legend(loc="upper left", frameon=False, fontsize=8.5, labelcolor=ink, ncol=2)
    fig.suptitle("g3 gantry with its bolted joints as springs: the first three modes (12 mm mesh, head and lens inertia)",
                 color=ink, fontsize=11, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(OUT / "struct-joints-mode1.png")
    print("  wrote struct-joints-mode1.png")


def main():
    S.OUT.mkdir(parents=True, exist_ok=True)
    RUN.mkdir(parents=True, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "bonded":
        cmd_bonded(float(sys.argv[2]), sys.argv[3])
    elif cmd == "sweep":
        cmd_sweep(float(sys.argv[2]), sys.argv[3].split(",") if len(sys.argv) > 3 else None)
    elif cmd == "variant":
        cmd_variant(sys.argv[2], float(sys.argv[3]), tuple(sys.argv[4].split(",")) if len(sys.argv) > 4 else ("kr3e6_kt2e4", "stiff"))
    elif cmd == "plot":
        cmd_plot()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
