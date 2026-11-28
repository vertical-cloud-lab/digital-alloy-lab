"""Scale references for the build animation (render_build.py): things everyone knows the size of, and dimension lines.

A machinist watching the first animation couldn't tell how big the chamber was ("the size and scale aren't immediately
apparent from the video"). Every chapter now puts one of these next to the work:

  soda can     a US 12 fl oz (355 mL) can: Ø66 x 122 mm (the "211" body; the "202" end is Ø54)
  steel rule   a 300 mm (12 in.) rule, 25 mm wide, ticks every 10 mm, longer every 50 and 100 mm
  person       a 1.75 m man (MakeHuman's CC0 base mesh, clothes and rig, built by human/build_person.py), for the tray
               and the kit layout
  dims         dimension lines with extension lines, end ticks and a label in mm and inches

The meshes are plain pyvista; colours are neutral so nothing reads as a brand.
"""
from __future__ import annotations

import math
import pathlib

import numpy as np
import pyvista as pv

INCH = 25.4
INK = "#1d2733"
CAN = dict(d=66.0, h=122.0, end_d=54.0, neck=9.0)
RULE = dict(L=300.0, w=25.0, t=1.0)


def soda_can(at=(0.0, 0.0, 0.0)):
    """[(mesh, colour)]: a 12 fl oz can standing on `at` (its base centre)."""
    x, y, z = map(float, at)
    r, h, re, nk = CAN["d"] / 2, CAN["h"], CAN["end_d"] / 2, CAN["neck"]
    body = pv.Cylinder(center=(x, y, z + nk + (h - 2 * nk) / 2), direction=(0, 0, 1), radius=r, height=h - 2 * nk, resolution=48)
    top = pv.Cylinder(center=(x, y, z + h - nk / 2), direction=(0, 0, 1), radius=(r + re) / 2, height=nk, resolution=48)
    bot = pv.Cylinder(center=(x, y, z + nk / 2), direction=(0, 0, 1), radius=(r + re) / 2, height=nk, resolution=48)
    lid = pv.Disc(center=(x, y, z + h + 0.2), inner=0.0, outer=re, normal=(0, 0, 1), c_res=48)
    band = pv.Cylinder(center=(x, y, z + h * 0.52), direction=(0, 0, 1), radius=r + 0.3, height=h * 0.34, resolution=48)
    return [(body, "#c8323a"), (top, "#c9ced3"), (bot, "#c9ced3"), (lid, "#aeb4ba"), (band, "#f2f2f2")]


def steel_rule(at=(0.0, 0.0, 0.0), axis=(1.0, 0.0, 0.0), L=RULE["L"]):
    """([(mesh, colour)], [(point, label)]): a steel rule lying flat from `at` along `axis` (in the xy plane)."""
    a = np.asarray(axis, float)
    a /= np.linalg.norm(a)
    n = np.array([-a[1], a[0], 0.0])               # across the rule
    p0 = np.asarray(at, float)
    w, t = RULE["w"], RULE["t"]
    corners = [p0, p0 + a * L, p0 + a * L + n * w, p0 + n * w]
    base = pv.PolyData(np.array(corners), faces=[4, 0, 1, 2, 3]).extrude((0, 0, t), capping=True)
    ticks = []
    for mm in range(0, int(L) + 1, 10):
        ln = 12.0 if mm % 100 == 0 else 8.0 if mm % 50 == 0 else 5.0
        q = p0 + a * mm + np.array([0, 0, t + 0.05])
        ticks.append(pv.Line(q, q + n * ln))
    labels = [(p0 + a * mm + n * (w * 0.75) + np.array([0, 0, t + 1]), "0" if mm == 0 else f"{mm // 10} cm") for mm in (0, 100, 200, 300) if mm <= L]
    tick = ticks[0].merge(ticks[1:]) if len(ticks) > 1 else ticks[0]
    return [(base, "#d5d9dd"), (tick.tube(radius=0.45), INK)], labels


# ------------------------------------------------------------------ the person
HUMAN = pathlib.Path(__file__).resolve().parent / "human" / "person.npz"     # built by human/build_person.py
# a slate shirt rather than a bright blue one: the build GIFs share one 160-colour palette per file, mostly greys, and a
# saturated shirt broke up into blotches in it
PERSON_COLOURS = {"skin": "#c49a7e", "shirt": "#5f7186", "jeans": "#39465a", "shoe": "#2f3237", "sole": "#1d1f22",
                  "hair": "#3b2c22", "eye_white": "#dcd8d2", "iris": "#3a2a20", "brow": "#33261d"}
POSES = {   # arm_out / arm_fwd: the upper arm's angle out from vertical to the side / forward (deg); elbow: forearm bend
    "stand": dict(arm_out=7.0, arm_fwd=4.0, elbow=12.0),          # arms hanging, hands beside the thighs
    "reach": dict(arm_out=3.0, arm_fwd=24.0, elbow=62.0),         # both hands forward at about waist height
}
_HUMAN = {}


def _human():
    """person.npz, loaded once: rest-pose vertices (mm, z up, facing -y, soles on z = 0), triangles and their materials,
    23 bones (joint, parent) and four skin weights per vertex."""
    if not _HUMAN:
        d = np.load(HUMAN)
        _HUMAN.update({k: d[k] for k in d.files})
        _HUMAN["bi"] = {str(b): k for k, b in enumerate(_HUMAN["bones"])}
        _HUMAN["mk"] = {str(n): p.astype(float) for n, p in zip(_HUMAN["mark_names"], _HUMAN["mark_pos"])}
    return _HUMAN


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _rot_axis(axis, deg):
    a = _unit(axis)
    t = math.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def _rot_between(a, b):
    """The smallest rotation taking direction a to direction b."""
    a, b = _unit(a), _unit(b)
    v, c = np.cross(a, b), float(np.dot(a, b))
    if np.linalg.norm(v) < 1e-9:
        return np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K / (1 + c)


def _pair(v):
    """A value for both sides, or (left, right)."""
    return (float(v), float(v)) if np.isscalar(v) else (float(v[0]), float(v[1]))


def person_pose(arm_out=7.0, arm_fwd=4.0, elbow=12.0, stance=260.0, curl=(14.0, 24.0), bend=0.0, head_down=0.0):
    """{bone: rotation about its joint, in the rest frame} for a figure standing with its ankles `stance` mm apart; the
    trunk bent `bend` deg forward (half at the waist, half at the chest) and the head bowed `head_down` deg more; each
    upper arm `arm_out` deg out to the side and `arm_fwd` deg forward of hanging straight down (measured from the room's
    vertical, so bending over leaves the arms hanging), the elbows bent `elbow` deg forward; the four fingers curled
    curl[0] deg at the knuckles and curl[1] deg at the middle joints. arm_out, arm_fwd and elbow take one value for both
    arms or a (left, right) pair. The rest pose (MakeHuman's A-pose) has the arms ~45 deg out, the forearms forward,
    the fingers straight and the ankles ~400 mm apart."""
    H = _human()
    J = lambda b: H["head"][H["bi"][b]].astype(float)                      # noqa: E731
    ex = np.array([1.0, 0.0, 0.0])                                         # the figure's left: bending forward turns about +x
    pose = {"spine_low": _rot_axis(ex, bend / 2), "spine_up": _rot_axis(ex, bend / 2),
            "neck": _rot_axis(ex, 0.4 * head_down), "head": _rot_axis(ex, 0.6 * head_down)}
    trunk = pose["spine_low"] @ pose["spine_up"]                           # the arms' parent frame
    outs, fwds, elbows = _pair(arm_out), _pair(arm_fwd), _pair(elbow)
    for k, (S, sg) in enumerate((("L", 1.0), ("R", -1.0))):
        sh, el, wr = J(f"upperarm.{S}"), J(f"lowerarm.{S}"), J(f"hand.{S}")
        down = _unit([sg * math.tan(math.radians(outs[k])), -math.tan(math.radians(fwds[k])), -1.0])
        Ru = _rot_between(el - sh, trunk.T @ down)
        pose[f"upperarm.{S}"] = Ru
        side = np.cross(down, [0.0, -1.0, 0.0])                             # the elbow's hinge, across the arm
        if np.linalg.norm(side) < 1e-6:                                    # arm straight ahead: bend the forearm down
            side = np.array([1.0, 0.0, 0.0])
        pose[f"lowerarm.{S}"] = _rot_between(_unit(wr - el), (trunk @ Ru).T @ (_rot_axis(side, elbows[k]) @ down))
        # fingers: curled toward the palm about the knuckle line (index finger's knuckle to the little finger's)
        ax = H["mk"][f"knuckle5.{S}"] - H["mk"][f"knuckle2.{S}"]
        pose[f"fingers.{S}"] = _rot_axis(ax, sg * curl[0])
        pose[f"fingertips.{S}"] = _rot_axis(ax, sg * curl[1])
        # legs: swing each leg in about the hip so the ankles are `stance` apart, the foot turned back level
        hip, an = J(f"upperleg.{S}"), J(f"foot.{S}")
        want = np.array([sg * stance / 2, an[1], an[2]])
        Rl = _rot_between((an - hip) * [1, 0, 1], (want - hip) * [1, 0, 1])
        pose[f"upperleg.{S}"] = Rl
        pose[f"foot.{S}"] = Rl.T
    return pose


def _skin(pose):
    """Linear-blend skinning: each vertex moved by its four bones' joint rotations (each bone's rotation applied in the
    rest frame, then its parent's)."""
    H = _human()
    nb = len(H["bones"])
    G = np.zeros((nb, 4, 4))
    for k in range(nb):                                                  # parents come before their children
        R = pose.get(str(H["bones"][k]), np.eye(3))
        L = np.eye(4)
        L[:3, :3] = R
        L[:3, 3] = H["head"][k] - R @ H["head"][k]
        p = int(H["parent"][k])
        G[k] = G[p] @ L if p >= 0 else L
    V = H["V"].astype(float)
    Vh = np.c_[V, np.ones(len(V))]
    out = np.zeros_like(V)
    for j in range(4):
        out += H["sk_w"][:, j, None] * np.einsum("nij,nj->ni", G[H["sk_i"][:, j]][:, :3, :], Vh)
    return out


def person(at=(0.0, 0.0, 0.0), h=1750.0, facing=(0.0, -1.0, 0.0), pose="stand", colours=None, **kw):
    """[(mesh, colour)]: a 1.75 m man in a long-sleeved T-shirt, jeans and trainers, standing on `at` and facing `facing`
    (xy), scaled to stature `h` (barefoot crown to sole).

    pose: "stand" (arms hanging), "reach" (both hands forward at about waist height), or a dict of person_pose()'s
    arguments; keyword arguments override single values (e.g. elbow=30, bend=25, head_down=20, arm_fwd=(60, 10)).
    colours: overrides for PERSON_COLOURS by material (e.g. {"shirt": "#e67e22"} to pick one person out).

    The third figure: the 2026-11-20 one was a cylinder with a ball on top, the 2026-11-23 one was lofted from ellipses
    and tubes, and both looked wrong ("human looks weird", "the human still looks weird"). This is MakeHuman's anatomical
    base mesh with its CC0 clothes, hair and eyes, shaped, dressed and skinned by human/build_person.py into person.npz,
    and posed here with MakeHuman's skeleton and skin weights."""
    H = _human()
    args = dict(POSES[pose]) if isinstance(pose, str) else dict(pose)
    args.update(kw)
    V = _skin(person_pose(**args))
    cols = dict(PERSON_COLOURS, **(colours or {}))
    mats = [str(x) for x in H["mats"]]
    soles = np.unique(H["F"][H["fmat"] == mats.index("sole")])
    V[:, 2] -= V[soles, 2].min()                                          # stand on the soles after the legs moved
    V *= h / 1750.0
    f = np.asarray(facing, float).copy()
    f[2] = 0.0
    f /= np.linalg.norm(f)
    ang = math.atan2(f[1], f[0]) - math.atan2(-1.0, 0.0)
    c, s_ = math.cos(ang), math.sin(ang)
    V = V @ np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1.0]]).T + np.asarray(at, float)
    out = []
    for k, name in enumerate(mats):
        tri = H["F"][H["fmat"] == k]
        if not len(tri):
            continue
        used, inv = np.unique(tri, return_inverse=True)
        m = pv.PolyData(V[used], np.c_[np.full(len(tri), 3), inv.reshape(-1, 3)].ravel())
        out.append((m.compute_normals(auto_orient_normals=False, split_vertices=False, consistent_normals=False),
                    cols[name]))
    return out


def _fmt(mm):
    return f"{mm:.0f} mm ({mm / INCH:.1f} in.)"


def dim_line(p0, p1, off, text=None):
    """(mesh of the extension lines, dimension line and end ticks; label point; label) for the distance p0-p1, drawn
    displaced by the vector `off`."""
    p0, p1, off = (np.asarray(v, float) for v in (p0, p1, off))
    L = float(np.linalg.norm(p1 - p0))
    u = (p1 - p0) / max(L, 1e-9)
    o = off / max(np.linalg.norm(off), 1e-9)
    q0, q1 = p0 + off, p1 + off
    tk = 0.04 * max(L, 120.0)
    segs = [(p0 + o * 4.0, q0 + o * tk * 0.4), (p1 + o * 4.0, q1 + o * tk * 0.4), (q0, q1)]
    d45 = (u + o) / math.sqrt(2)
    segs += [(q0 - d45 * tk / 2, q0 + d45 * tk / 2), (q1 - d45 * tk / 2, q1 + d45 * tk / 2)]
    lines = [pv.Line(a, b) for a, b in segs]
    mesh = lines[0].merge(lines[1:])
    return mesh, (q0 + q1) / 2 + o * tk * 0.6, text or _fmt(L)


def add_dims(st, key, dims, font_size=12, color=INK):
    """dims: [(p0, p1, off, text-or-None)]; draws them on the Stage `st` under `key` (remove with remove_dims)."""
    meshes, pts, labs = [], [], []
    for p0, p1, off, text in dims:
        m, q, lab = dim_line(p0, p1, off, text)
        meshes.append(m)
        pts.append(q)
        labs.append(lab)
    mesh = meshes[0].merge(meshes[1:]) if len(meshes) > 1 else meshes[0]
    st.add(key, mesh.tube(radius=0.0035 * max(np.ptp(mesh.points, axis=0).max(), 100.0), n_sides=8), color, ambient=0.8)
    st.pl.add_point_labels(np.array(pts), labs, font_size=font_size, text_color=color, shape="rounded_rect",
                           shape_color="white", shape_opacity=0.75, show_points=False, always_visible=True, name=key + "-lab")


def remove_dims(st, key):
    st.remove(key)
    try:
        st.pl.remove_actor(key + "-lab")
    except Exception:  # noqa: BLE001
        pass


def box_dims(b, which="xyz", pad=None):
    """Dimension lines for an axis-aligned box b = (x0, x1, y0, y1, z0, z1): x along the front-bottom edge, y along the
    right-bottom edge, z up the front-left edge (so the three labels don't crowd one corner)."""
    x0, x1, y0, y1, z0, z1 = map(float, b)
    pad = pad or 0.18 * max(x1 - x0, y1 - y0, z1 - z0, 60.0)
    out = []
    if "x" in which:
        out.append(((x0, y0, z0), (x1, y0, z0), (0, -pad, 0), None))
    if "y" in which:
        out.append(((x1, y0, z0), (x1, y1, z0), (pad, 0, 0), None))
    if "z" in which:
        out.append(((x0, y0, z0), (x0, y0, z1), (-pad * 0.7, -pad * 0.7, 0), None))
    return out


def add_refs(st, key, pieces, labels=()):
    """Draw [(mesh, colour)] as one group under `key`, plus point labels."""
    st.add_multi(key, pieces)
    if labels:
        st.pl.add_point_labels(np.array([p for p, _ in labels]), [t for _, t in labels], font_size=10, text_color=INK, shape=None,
                               show_points=False, always_visible=True, name=key + "-lab")


def remove_refs(st, key):
    st.remove(key)
    try:
        st.pl.remove_actor(key + "-lab")
    except Exception:  # noqa: BLE001
        pass
