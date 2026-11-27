"""Coarse CFD of the laser guard's air with the drawn cooling (issue #260, PR 281; monitoring/cooling.md §4.2).

cooling.py treats the guard's air as one well-mixed volume. This case checks the drawn flow path instead: steady buoyant RANS
(OpenFOAM v2406 buoyantSimpleFoam, k-epsilon, perfect gas) in the guard's inside, with the parts from the CAD model as blocked
cells of a Cartesian mesh.

  dump      build the model (cad/lpbf_low.build(monitoring=True), no fasteners, no tray) and write an STL and the bounding box of
            every part inside the guard to --stl (~1 GB, 15 s)
  case      voxelise those parts on a Cartesian grid (cell size --h, mm), write the polyMesh directly (no blockMesh), and the
            fields and dictionaries for one load case into --out
  post      read the solved case(s) and write analysis/out/monitoring/cooling/guard_cfd.json, guard_cfd.md and the figures

What is modelled (each an assumption, stated again in cooling.md §4.2):
  * Domain: the guard's inside, x -420..310, y -265..215, z -160 (base plate) .. 366.1 (top panel), less every part's cells.
    Thin sheet (the Chronos hood) is a zero-thickness wall (baffle) on mesh planes. The chamber's KF-25 hoses, the fibre, the
    argon and O2 lines and the screws are left out (thin or not watertight in the export).
  * Inlet: the inlet trap's inner face (y = 181.5), left of the hood plenum (x -394..-283, z -118..202), at the supply
    temperature, a uniform velocity carrying the exhaust flow less the hood's. The trap's last leg points the air down at
    62 deg (atan(A / (D/n)) = atan(10 / 5.33)), so the velocity has that direction. The plenum, the two ducts and the trap
    blocks are solid; the hood fan is a fixed-flow inlet where the duct drops into the hood (x -392..-336, z 127), at the supply
    temperature + 0.5 K (cooling.py's allowance; the fan's own 2.2 W is ~0.35 K of it).
  * Exhaust: the exhaust trap's inner face (y = 181.5, x 40..284, z 108..338) at a fixed pressure; the flow out equals the flow
    in. 118 m3/h and the hood's 20.4 m3/h are cooling.py's operating point (cooling.json operating_point, hood).
  * Heat: cooling.py's SOURCES for the load case, as a fixed power on each device's surfaces: the galvo 30 % of its heat, the
    optics bridge 70 % of it plus the beam path (cooling.py T_bridge), the servos, the stepper, PB2 (with its 40 mm fan), the
    LP camera's Pi, the Chronos, the photodiodes, the IMX296 boards, the LED, the AE preamp and the layer camera. The exhaust
    fans sit outside the guard, so their 13.4 W is not in the guard's air (cooling.py counts it). The chamber's outside (body,
    floor plate, lid, door, build module) is held at 60 C (cooling.py's bound); the half of its legs' conduction that
    cooling.py gives the guard's air goes in as a uniform flux on the base plate's top. No radiation.
  * Panels: the CFD resolves the inside film; the outside is a fixed coefficient to the Shuttle's air (cooling.py's formulas:
    vertical bare panel 2.6, top 3.3, the polycarbonate window 6.5, the base plate's underside 1.9 W/m2K).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[2]                                            # desktop-lpbf/
OUT = D / "analysis" / "out" / "monitoring" / "cooling"
sys.path.insert(0, str(D / "cad"))
import monitoring_cooling as MC  # noqa: E402

G = MC.GUARD
RHO, CP = 1.13, 1007.0
PHI_TRAP = math.degrees(math.atan2(MC.LOUVRE["A"], MC.LOUVRE["D"] / MC.LOUVRE["n"]))     # 61.9 deg: the trap's last leg

# ------------------------------------------------------------------------------------------------ parts -> patches
# patch name: (name prefixes, what); the heat for each load case is in heat_inputs()
GROUPS = {
    "galvo": (["2-axis galvo scan head"], "basiCube 20 galvo"),
    "bridge": (["Optics bridge (6061", "Galvo riser plate"], "optics bridge and the galvo's riser"),
    "chamber": (["Process chamber body", "Chamber floor plate", "Chamber lid", "Chamber door (6061", "Build module M50:"],
                "chamber outside, held at 60 C"),
    "servoR": (["Recoater servo (ClearPath"], "recoater servo"),
    "servoZ": (["Z servo (ClearPath"], "Z servo (its part above the base plate)"),
    "stepper": (["Dosing stepper"], "dosing stepper"),
    "pb2": (["PB2 process-module box", "PB2 vent fan"], "PB2 (Pi 5, boards, DC-DC, 40 mm fan)"),
    "piLP": (["LP camera's Pi"], "the LP camera's Pi in its heat-sink case"),
    "chronos": (["Side high-speed camera"], "Chronos 2.1-HD"),
    "pdA": (["Photodiode A (Thorlabs"], "PDA36A2, photodiode A"),
    "pdB": (["Photodiode B (Thorlabs"], "PDA36A2, photodiode B"),
    "camLP": (["LP camera (monochrome"], "LP camera (IMX296)"),
    "camCoax": (["Coaxial camera (monochrome"], "coaxial camera (IMX296)"),
    "led": (["BW LED heat sink", "BW LED (Thorlabs"], "BW 850 nm LED and heat sink"),
    "aePre": (["AE preamplifier"], "AE preamp"),
    "camLayer": (["Layer camera (Pi HQ"], "layer camera"),
    "cage": (["Coaxial cube", "Coaxial lens tubes", "Coaxial camera arm", "Photodiode A arm", "Photodiode B arm", "Cage rods",
              "Coaxial-monitoring dichroic", "Beam trap on cube 1", "Fold mirror", "Safety shutter", "Collimator"],
             "coaxial cage, its cubes and arms, the dichroic, shutter, fold mirror and collimator (unheated)"),
}
SKIP = ["Laser guard panels", "Process fiber", "Guard inlet light trap", "Guard exhaust light trap", "Hood duct", "Side camera hood",
        "Hood fan in the duct", "Base plate", "Leveling mounts", "Guard frame", "Gas-loop + vacuum hoses", "Argon line",
        "O2 sample line"]
# devices whose surrounding air is reported (patch groups), with cooling.md §1's rating and what it is checked on
REPORT = [
    ("chronos", "Chronos 2.1-HD, in its hood", 40, "air"),
    ("cage", "coaxial cage", None, "air"),
    ("camCoax", "coaxial camera (IMX296)", 50, "board"),
    ("pdA", "photodiode PD-A (PDA36A2)", 40, "air"),
    ("pdB", "photodiode PD-B (PDA36A2)", 40, "air"),
    ("pb2", "PB2 (Pi 5)", 70, "box air"),
    ("camLP", "LP camera (IMX296)", 50, "board"),
    ("piLP", "LP camera's Pi 5", 80, "SoC"),
    ("galvo", "galvo (basiCube 20)", 35, "air"),
    ("led", "BW 850 nm LED", 40, "air"),
    ("aePre", "AE preamp", 65, "case"),
    ("camLayer", "layer camera (Pi HQ)", 50, "air"),
]


def load_cooling():
    return json.load(open(OUT / "cooling.json"))


def heat_inputs(load, T_s, cj):
    """W per patch, from cooling.py's SOURCES (cooling.json 'sources'), and the legs' share to the base plate"""
    i = "W_typical" if load == "typical" else "W_worst"
    S = {k: v[i] for k, v in cj["sources"].items()}
    galvo = S["galvo (basiCube 20)"]
    beam = S["beam path (collimator, shutter coil, dichroic, beam trap, f-theta)"]
    Q = dict(galvo=0.3 * galvo, bridge=0.7 * galvo + beam,
             servoR=0.5 * S["Z and recoater servos"], servoZ=0.5 * S["Z and recoater servos"],
             stepper=S["dosing stepper"], pb2=S["PB2 (Pi 5, lid sensors, DC-DC)"] + 1.08,
             piLP=S["LP camera's Pi 5 (second Pi)"], chronos=S["Chronos 2.1-HD"],
             pdA=0.5 * S["two PDA36A2"], pdB=0.5 * S["two PDA36A2"],
             camLP=0.5 * S["IMX296 boards (LP, coaxial)"], camCoax=0.5 * S["IMX296 boards (LP, coaxial)"],
             led=S["BW 850 nm LED"], aePre=S["AE preamp"], camLayer=S["layer camera (Pi HQ)"])
    # cooling.py: the legs conduct G_LEGS (60 - T_g) and half of it is given to the guard's air through the base plate. T_g is
    # the well-mixed guard air of the same case (cooling.json), so the total heat matches cooling.py's
    case = "typical" if abs(T_s - cj["cases"]["typical"]["T_s"]) < 0.05 else "busy"
    Tg = cj["results"][f"{case}/vent_shuttle"]["guard"]["T_g"]
    legs = 0.5 * cj["chamber"]["G_legs_W_per_K"] * (60.0 - Tg)
    return Q, legs, Tg


# ------------------------------------------------------------------------------------------------ dump (CAD)
def dump(stl_dir):
    import time
    stl_dir = pathlib.Path(stl_dir)
    stl_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(D / "cad")
    import lpbf_low as L
    from cadquery import exporters
    t0 = time.time()
    parts = L.build(include_tray=False, module="M50", fasteners=False, monitoring=True)
    rows = []
    for i, p in enumerate(parts):
        bb = p.shape.BoundingBox()
        try:
            vol = p.shape.Volume()
        except Exception:
            vol = None
        inside = not (bb.xmax < G["x0"] or bb.xmin > G["x1"] or bb.ymax < G["y0"] or bb.ymin > G["y1"] or bb.zmax < G["z0"] - 40
                      or bb.zmin > G["z1"])
        r = dict(i=i, name=p.name, bbox=[bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax], vol_mm3=vol, inside=inside)
        if inside:
            fn = stl_dir / f"p{i:03d}.stl"
            exporters.export(p.shape, str(fn), tolerance=0.5, angularTolerance=0.3)
            r["stl"] = fn.name
        rows.append(r)
    json.dump(dict(parts=rows), open(stl_dir / "parts.json", "w"), indent=1)
    print(f"{len(parts)} parts, {sum(1 for r in rows if r['inside'])} inside the guard, {time.time() - t0:.0f} s")


# ------------------------------------------------------------------------------------------------ grid
def grid_lines(h):
    """non-uniform tensor grid: the lines that must be exact (domain, traps, hood, ducts, bridge and its posts, chamber), each
    interval split into equal cells no longer than h. The back posts' faces at y 175 keep the 6.5 mm gap in front of the inlet
    trap open"""
    I, E, P, D1, D2, H = MC.INLET, MC.EXHAUST, MC.PLENUM, MC.DUCT1, MC.DUCT2, MC.HOOD
    yt = MC.Y_TRAP[0]
    must = [
        [G["x0"], G["x1"], H["x"][0], H["x"][1], I["x"][0], P["x"][0], I["x"][1], E["x"][0], E["x"][1], -360.0, 245.0, -156.0, 156.0,
         H["floor_opening_x"][0], H["floor_opening_x"][1], -345.0, -285.0, 180.0, 240.0],
        [G["y0"], G["y1"], yt, H["y"][0], H["y"][1], P["y"][0], -190.0, -111.0, 111.0, -185.0, -125.0, 115.0, 175.0],
        [G["z0"], G["z1"], I["z"][0], I["z"][1], E["z"][0], E["z"][1], H["z"][0], H["z"][1], D2["z"][1], 211.1, 236.1, -20.0, 136.0],
    ]
    out = []
    for a in range(3):
        L = sorted(set(round(v, 2) for v in must[a]))
        merged = [L[0]]
        for v in L[1:]:
            if v - merged[-1] < 3.0:
                continue
            merged.append(v)
        lines = [merged[0]]
        for v0, v1 in zip(merged[:-1], merged[1:]):
            n = max(1, math.ceil((v1 - v0) / h - 1e-9))
            lines += list(np.linspace(v0, v1, n + 1)[1:])
        out.append(np.array(lines))
    return out


def voxelise(tri, xc, yc, zc):
    """cells whose centre is inside a closed triangle mesh: rays along x through every (y, z) centre, parity of the crossings"""
    jit_y, jit_z = 1.234567e-4, 2.345678e-4                    # off any vertex or edge
    ys, zs = yc + jit_y, zc + jit_z
    mask = np.zeros((len(xc), len(yc), len(zc)), bool)
    p0, p1, p2 = tri[:, 0], tri[:, 1], tri[:, 2]
    ymin, ymax = tri[:, :, 1].min(1), tri[:, :, 1].max(1)
    zmin, zmax = tri[:, :, 2].min(1), tri[:, :, 2].max(1)
    j0, j1 = np.searchsorted(ys, ymin), np.searchsorted(ys, ymax, "right")
    k0, k1 = np.searchsorted(zs, zmin), np.searchsorted(zs, zmax, "right")
    nj, nk = np.maximum(j1 - j0, 0), np.maximum(k1 - k0, 0)
    cnt = nj * nk
    keep = cnt > 0
    if not keep.any():
        return mask
    t_idx = np.repeat(np.nonzero(keep)[0], cnt[keep])
    off = np.arange(cnt[keep].sum()) - np.repeat(np.cumsum(cnt[keep]) - cnt[keep], cnt[keep])
    jj = j0[t_idx] + off // nk[t_idx]
    kk = k0[t_idx] + off % nk[t_idx]
    py, pz = ys[jj], zs[kk]
    a, b, c = p0[t_idx], p1[t_idx], p2[t_idx]
    d = (b[:, 1] - a[:, 1]) * (c[:, 2] - a[:, 2]) - (c[:, 1] - a[:, 1]) * (b[:, 2] - a[:, 2])
    ok = np.abs(d) > 1e-12
    d = np.where(ok, d, 1.0)
    l1 = ((py - a[:, 1]) * (c[:, 2] - a[:, 2]) - (c[:, 1] - a[:, 1]) * (pz - a[:, 2])) / d
    l2 = ((b[:, 1] - a[:, 1]) * (pz - a[:, 2]) - (py - a[:, 1]) * (b[:, 2] - a[:, 2])) / d
    inside = ok & (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
    xh = a[:, 0] + l1 * (b[:, 0] - a[:, 0]) + l2 * (c[:, 0] - a[:, 0])
    jj, kk, xh = jj[inside], kk[inside], xh[inside]
    if len(xh) == 0:
        return mask
    key = jj * len(zc) + kk
    order = np.lexsort((xh, key))
    key, xh = key[order], xh[order]
    starts = np.nonzero(np.r_[True, key[1:] != key[:-1]])[0]
    ends = np.r_[starts[1:], len(key)]
    for s, e in zip(starts, ends):
        if (e - s) % 2:
            continue                                            # odd crossings: an open edge; leave the row empty
        j, k = divmod(int(key[s]), len(zc))
        for m in range(s, e, 2):
            i0, i1 = np.searchsorted(xc, xh[m]), np.searchsorted(xc, xh[m + 1])
            mask[i0:i1, j, k] = True
    return mask


def box_mask(b, xc, yc, zc):
    x0, y0, z0, x1, y1, z1 = b
    return ((xc[:, None, None] > x0) & (xc[:, None, None] < x1) & (yc[None, :, None] > y0) & (yc[None, :, None] < y1)
            & (zc[None, None, :] > z0) & (zc[None, None, :] < z1))


def build_solid(stl_dir, X, Y, Z):
    """label array over the cells: 0 fluid, else 1 + index into names. Explicit blocks for the traps, plenum, ducts and frame"""
    import trimesh
    stl_dir = pathlib.Path(stl_dir)
    xc, yc, zc = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1]), 0.5 * (Z[1:] + Z[:-1])
    lab = np.zeros((len(xc), len(yc), len(zc)), np.int16)
    names = []

    def put(mask, name):
        if name not in names:
            names.append(name)
        lab[mask & (lab == 0)] = names.index(name) + 1

    rows = json.load(open(stl_dir / "parts.json"))["parts"]
    used, skipped = [], []
    # explicit blocks first (they win where they overlap a part)
    yt = MC.Y_TRAP[0]
    I, E, P, D1, D2 = MC.INLET, MC.EXHAUST, MC.PLENUM, MC.DUCT1, MC.DUCT2
    put(box_mask((I["x"][0] - 2, yt, I["z"][0] - 2, I["x"][1] + 2, G["y1"] + 1, I["z"][1] + 2), xc, yc, zc), "trapIn")
    put(box_mask((E["x"][0] - 2, yt, E["z"][0] - 2, E["x"][1] + 2, G["y1"] + 1, E["z"][1] + 2), xc, yc, zc), "trapEx")
    for b in (P, D1, D2):
        put(box_mask((b["x"][0], b["y"][0], b["z"][0], b["x"][1], b["y"][1], b["z"][1]), xc, yc, zc), "duct")
    # the chamber as one block (its floor plate, frame and lid: x +-156, y +-111, z -20..136), so the argon inside it, which the
    # grid would otherwise join to the guard through the window and viewport bores, is not counted as guard air
    put(box_mask((-156.0, -111.0, -20.0, 156.0, 111.0, 136.0), xc, yc, zc), "chamber")
    fr = []                                                     # guard frame: 20 mm T-slot along the 12 edges
    x0, x1, y0, y1, z0, z1 = G["x0"], G["x1"], G["y0"], G["y1"], G["z0"], G["z1"]
    for x in (x0, x1 - 20):
        for y in (y0, y1 - 20):
            fr.append((x, y, z0, x + 20, y + 20, z1))
    for z in (z0, z1 - 20):
        for y in (y0, y1 - 20):
            fr.append((x0, y, z, x1, y + 20, z + 20))
        for x in (x0, x1 - 20):
            fr.append((x, y0, z, x + 20, y1, z + 20))
    for b in fr:
        put(box_mask(b, xc, yc, zc), "frame")
    for r in rows:
        if not r["inside"] or any(r["name"].startswith(s) for s in SKIP):
            continue
        grp = next((g for g, (pre, _) in GROUPS.items() if any(r["name"].startswith(p) for p in pre)), "walls")
        b = r["bbox"]
        bv = max(1e-9, (b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2]))
        fill = (r["vol_mm3"] or 0.0) / bv
        m = None
        if "stl" in r:
            mesh = trimesh.load(stl_dir / r["stl"], process=True)
            if mesh.is_watertight:
                m = voxelise(np.asarray(mesh.triangles), xc, yc, zc)
            elif fill > 0.3:
                m = box_mask(b, xc, yc, zc)
        if m is None or not m.any():
            # small parts the grid misses: the cell holding the bbox centre if the part fills its bbox well
            if fill > 0.3 and grp != "walls":
                c = [0.5 * (b[0] + b[3]), 0.5 * (b[1] + b[4]), 0.5 * (b[2] + b[5])]
                m = np.zeros_like(lab, bool)
                m[np.searchsorted(X, c[0]) - 1, np.searchsorted(Y, c[1]) - 1, np.searchsorted(Z, c[2]) - 1] = True
            else:
                skipped.append(r["name"][:60])
                continue
        put(m, grp)
        used.append((r["name"][:60], grp, int(m.sum())))
    # pockets the parts close off (the chamber's own gas volume, gaps inside assemblies) are not the guard's air: fill them
    from scipy import ndimage
    reg, nreg = ndimage.label(lab == 0)
    sizes = np.bincount(reg.ravel())
    sizes[0] = 0
    main = int(np.argmax(sizes))
    pockets = (reg > 0) & (reg != main)
    if pockets.any():
        put(pockets, "walls")
    used.append((f"{nreg - 1} closed pockets filled", "walls", int(pockets.sum())))
    return lab, names, used, skipped


# ------------------------------------------------------------------------------------------------ polyMesh writer
def write_polymesh(case, X, Y, Z, lab, names, baffles, special):
    """Cartesian cells, the solid ones removed. Faces between a fluid cell and a solid cell go to the solid's patch, faces on the
    domain's sides to the panel patches, baffle faces (sheet on a mesh plane) to 'hood' twice. special(face centre, normal axis,
    solid name) can rename a face's patch (inlet, exhaust, hoodIn, window)."""
    nx, ny, nz = lab.shape
    F = lab == 0
    cid = np.full(lab.shape, -1, np.int64)
    flat = F.flatten("F")
    cid_f = np.cumsum(flat) - 1
    cid_f[~flat] = -1
    cid = cid_f.reshape(lab.shape, order="F")
    nc = int(flat.sum())

    def vid(i, j, k):
        return i + (nx + 1) * (j + (ny + 1) * k)

    def quad(axis, i, j, k):
        """vertices of the face on the + side of cell (i, j, k) normal to axis, ordered so the normal points +axis"""
        if axis == 0:
            return np.stack([vid(i + 1, j, k), vid(i + 1, j + 1, k), vid(i + 1, j + 1, k + 1), vid(i + 1, j, k + 1)], -1)
        if axis == 1:
            return np.stack([vid(i, j + 1, k), vid(i, j + 1, k + 1), vid(i + 1, j + 1, k + 1), vid(i + 1, j + 1, k)], -1)
        return np.stack([vid(i, j, k + 1), vid(i + 1, j, k + 1), vid(i + 1, j + 1, k + 1), vid(i, j + 1, k + 1)], -1)

    xc, yc, zc = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1]), 0.5 * (Z[1:] + Z[:-1])
    cent = (xc, yc, zc)
    L = (X, Y, Z)
    internal = []                                               # (owner, axis, faces)
    bnd = {}                                                    # patch -> list of (owner, faces)

    def add_b(patch, owner, faces):
        bnd.setdefault(patch, []).append((owner, faces))

    for a in range(3):
        sl0 = [slice(None)] * 3
        sl1 = [slice(None)] * 3
        sl0[a] = slice(0, lab.shape[a] - 1)
        sl1[a] = slice(1, lab.shape[a])
        A, B = lab[tuple(sl0)], lab[tuple(sl1)]
        i, j, k = [v.reshape(A.shape) for v in np.indices(A.shape)]
        base = np.zeros(A.shape, bool) if baffles is None else baffles[a][tuple(sl0)]
        ff = (A == 0) & (B == 0)
        # internal faces
        m = ff & ~base
        ii, jj, kk = i[m], j[m], k[m]
        q = quad(a, ii, jj, kk)
        internal.append((cid[ii, jj, kk], a, q))
        # baffles: two boundary faces
        m = ff & base
        ii, jj, kk = i[m], j[m], k[m]
        q = quad(a, ii, jj, kk)
        add_b("hood", cid[ii, jj, kk], q)
        nb = [ii.copy(), jj.copy(), kk.copy()]
        nb[a] = nb[a] + 1
        add_b("hood", cid[nb[0], nb[1], nb[2]], q[:, ::-1])
        # fluid (-) | solid (+): owner on the - side, normal +a
        for fl_side in (0, 1):
            if fl_side == 0:
                m = (A == 0) & (B > 0)
                sol = B[m]
            else:
                m = (A > 0) & (B == 0)
                sol = A[m]
            ii, jj, kk = i[m], j[m], k[m]
            q = quad(a, ii, jj, kk)
            own = [ii.copy(), jj.copy(), kk.copy()]
            if fl_side == 1:
                own[a] = own[a] + 1
                q = q[:, ::-1]
            fc = [cent[0][own[0]].copy(), cent[1][own[1]].copy(), cent[2][own[2]].copy()]
            fc[a] = L[a][ii + 1 if a == 0 else (jj + 1 if a == 1 else kk + 1)]
            for s in np.unique(sol):
                sm = sol == s
                nm = names[s - 1]
                pn = special(np.stack([fc[0][sm], fc[1][sm], fc[2][sm]], -1), a, +1 if fl_side == 0 else -1, nm)
                for p in np.unique(pn):
                    pm = pn == p
                    add_b(p, cid[own[0][sm][pm], own[1][sm][pm], own[2][sm][pm]], q[sm][pm])
    # domain sides
    for a in range(3):
        for side in (0, 1):
            sl = [slice(None)] * 3
            sl[a] = 0 if side == 0 else lab.shape[a] - 1
            m = F[tuple(sl)]
            g = np.indices(m.shape)
            ii = [None] * 3
            others = [b for b in range(3) if b != a]
            ii[others[0]], ii[others[1]] = g[0][m], g[1][m]
            ii[a] = np.full(ii[others[0]].shape, sl[a])
            if side == 1:
                q = quad(a, ii[0], ii[1], ii[2])
            else:
                qi = [v.copy() for v in ii]
                qi[a] = qi[a] - 1
                q = quad(a, qi[0], qi[1], qi[2])[:, ::-1]
            fc = [cent[0][ii[0]], cent[1][ii[1]], cent[2][ii[2]]]
            fc = [v.copy() for v in fc]
            fc[a] = np.full(fc[0].shape, L[a][0] if side == 0 else L[a][-1])
            pname = {(0, 0): "panelL", (0, 1): "panelR", (1, 0): "panelF", (1, 1): "panelB", (2, 0): "floor", (2, 1): "panelTop"}[(a, side)]
            pn = special(np.stack(fc, -1), a, -1 if side == 0 else +1, pname)
            for p in np.unique(pn):
                pm = pn == p
                add_b(p, cid[ii[0][pm], ii[1][pm], ii[2][pm]], q[pm])
    # order internal faces by owner then neighbour (+x, +y, +z neighbours are increasing in this numbering)
    own = np.concatenate([o for o, a, q in internal])
    ax = np.concatenate([np.full(len(o), a) for o, a, q in internal])
    qs = np.concatenate([q for o, a, q in internal])
    order = np.lexsort((ax, own))
    own, ax, qs = own[order], ax[order], qs[order]
    # neighbour from the vertex ids: recompute from owner index + axis via the label grid
    ijk = np.argwhere(F.transpose(2, 1, 0))[:, ::-1]           # fluid cells in cid order (i fastest)
    oi = ijk[own]
    ni = oi.copy()
    ni[np.arange(len(ni)), ax] += 1
    nei = cid[ni[:, 0], ni[:, 1], ni[:, 2]]
    assert (nei > own).all()
    patches = [(p, np.concatenate([o for o, q in v]), np.concatenate([q for o, q in v])) for p, v in bnd.items()]
    # keep the used points only
    allq = np.concatenate([qs] + [q for _, _, q in patches])
    used = np.unique(allq)
    remap = np.full((nx + 1) * (ny + 1) * (nz + 1), -1, np.int64)
    remap[used] = np.arange(len(used))
    gi = used % (nx + 1)
    gj = (used // (nx + 1)) % (ny + 1)
    gk = used // ((nx + 1) * (ny + 1))
    pts = np.stack([X[gi], Y[gj], Z[gk]], -1) * 1e-3
    pm = case / "constant" / "polyMesh"
    pm.mkdir(parents=True, exist_ok=True)

    def hdr(cls, obj, note=""):
        return ("FoamFile\n{\n    version 2.0;\n    format ascii;\n    class %s;\n%s    location \"constant/polyMesh\";\n    object %s;\n}\n"
                % (cls, ('    note "%s";\n' % note) if note else "", obj))

    with open(pm / "points", "w") as f:
        f.write(hdr("vectorField", "points") + f"{len(pts)}\n(\n")
        f.write("\n".join("(%.6g %.6g %.6g)" % tuple(p) for p in pts))
        f.write("\n)\n")
    faces = [remap[qs]] + [remap[q] for _, _, q in patches]
    owners = [own] + [o for _, o, _ in patches]
    nf = sum(len(x) for x in faces)
    with open(pm / "faces", "w") as f:
        f.write(hdr("faceList", "faces") + f"{nf}\n(\n")
        for fa in faces:
            f.write("\n".join("4(%d %d %d %d)" % tuple(r) for r in fa))
            f.write("\n")
        f.write(")\n")
    note = f"nPoints:{len(pts)} nCells:{nc} nFaces:{nf} nInternalFaces:{len(own)}"
    with open(pm / "owner", "w") as f:
        f.write(hdr("labelList", "owner", note) + f"{nf}\n(\n")
        f.write("\n".join(str(int(v)) for v in np.concatenate(owners)))
        f.write("\n)\n")
    with open(pm / "neighbour", "w") as f:
        f.write(hdr("labelList", "neighbour", note) + f"{len(nei)}\n(\n")
        f.write("\n".join(str(int(v)) for v in nei))
        f.write("\n)\n")
    start = len(own)
    with open(pm / "boundary", "w") as f:
        f.write(hdr("polyBoundaryMesh", "boundary") + f"{len(patches)}\n(\n")
        for p, o, q in patches:
            typ = "patch" if p in ("inlet", "hoodIn", "exhaust") else "wall"
            f.write(f"    {p}\n    {{\n        type {typ};\n        nFaces {len(o)};\n        startFace {start};\n    }}\n")
            start += len(o)
        f.write(")\n")
    area = {}
    for p, o, q in patches:
        P0, P1, P2 = pts[remap[q[:, 0]]], pts[remap[q[:, 1]]], pts[remap[q[:, 2]]]
        area[p] = float(np.linalg.norm(np.cross(P1 - P0, P2 - P0), axis=1).sum())
    return dict(cells=nc, faces=nf, internal=len(own), points=len(pts), patches={p: len(o) for p, o, _ in patches}, area_m2=area,
                ijk=ijk)


# ------------------------------------------------------------------------------------------------ case
def write_case(args):
    cj = load_cooling()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    X, Y, Z = grid_lines(args.h)
    lab, names, used, skipped = build_solid(args.stl, X, Y, Z)
    nx, ny, nz = lab.shape
    # hood sheets as baffles on mesh planes (faces between two fluid cells on the plane, within the sheet's extent)
    H = MC.HOOD
    xc, yc, zc = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1]), 0.5 * (Z[1:] + Z[:-1])
    baff = [np.zeros((nx, ny, nz), bool) for _ in range(3)]

    def on(Lines, v):
        i = int(np.argmin(np.abs(Lines - v)))
        assert abs(Lines[i] - v) < 1e-6, (v, Lines[i])
        return i - 1                                            # cell index on the - side of the plane

    def inr(c, lo, hi):
        return (c > lo) & (c < hi)

    for yv in H["y"]:                                           # the hood's -y and +y sides
        j = on(Y, yv)
        baff[1][:, j, :] |= inr(xc, *H["x"])[:, None] & inr(zc, *H["z"])[None, :]
    i = on(X, H["x"][0])                                        # its back (-x end)
    baff[0][i, :, :] |= inr(yc, *H["y"])[:, None] & inr(zc, *H["z"])[None, :]
    k = on(Z, H["z"][0])                                        # its floor (the bracket plate fills the cut-out)
    baff[2][:, :, k] |= inr(xc, *H["x"])[:, None] & inr(yc, *H["y"])[None, :]
    I, E = MC.INLET, MC.EXHAUST
    fo = H["floor_opening_x"]
    yt = MC.Y_TRAP[0]
    win = G["door_window"]

    def special(fc, axis, sgn, nm):
        x, y, z = fc[:, 0], fc[:, 1], fc[:, 2]
        p = np.full(len(fc), nm, dtype=object)
        if nm == "trapIn" and axis == 1:
            p[inr(x, I["x"][0], MC.PLENUM["x"][0]) & inr(z, *I["z"]) & (np.abs(y - yt) < 1e-6)] = "inlet"
        if nm == "trapEx" and axis == 1:
            p[inr(x, *E["x"]) & inr(z, *E["z"]) & (np.abs(y - yt) < 1e-6)] = "exhaust"
        if nm == "duct" and axis == 2:
            p[inr(x, *fo) & inr(y, H["y"][0] + 1, H["y"][1] - 1) & (np.abs(z - H["z"][1]) < 1e-6)] = "hoodIn"
        if nm == "panelF":
            p[inr(x, win[0], win[1]) & inr(z, win[2], win[3])] = "window"
        if nm in ("trapIn", "trapEx", "duct", "frame", "cage"):
            p[p == nm] = "walls" if nm != "cage" else "cage"
        return p

    mesh = write_polymesh(out, X, Y, Z, lab, names, baff, special)
    ijk = mesh.pop("ijk")
    np.savez_compressed(out / "grid.npz", X=X, Y=Y, Z=Z, lab=lab, ijk=ijk, names=np.array(names))
    # ---------------------------------------------------------------- loads and boundary values
    T_s = args.supply_c
    Q, legs, Tg_wm = heat_inputs(args.load, T_s, cj)
    q_ex = args.q_exhaust if args.q_exhaust else cj["operating_point"]["q_m3h"]
    q_hood = args.q_hood if args.q_hood is not None else cj["hood"]["q_m3h"]
    q_in = q_ex - q_hood
    A_in, A_hood = mesh["area_m2"]["inlet"], mesh["area_m2"]["hoodIn"]
    vn = q_in / 3600 / A_in
    ang = math.radians(args.inlet_angle)
    U_in = (0.0, -vn, -vn * math.tan(ang))
    v_hood = q_hood / 3600 / A_hood
    Tk = lambda c: c + 273.15
    A_floor = mesh["area_m2"]["floor"]
    q_floor = legs / A_floor
    k_in, eps_in = 1.5 * (0.1 * 1.6) ** 2, 0.09 ** 0.75 * (1.5 * (0.1 * 1.6) ** 2) ** 1.5 / 0.003
    hdr = lambda cls, obj: "FoamFile\n{\n    version 2.0;\n    format ascii;\n    class %s;\n    object %s;\n}\n" % (cls, obj)
    heated = {p: Q[p] for p in Q if p in mesh["patches"]}
    missing = [p for p in Q if p not in mesh["patches"]]
    assert not missing, f"heated parts the grid lost: {missing}"
    walls_adiabatic = [p for p in mesh["patches"] if p not in heated and p not in ("inlet", "hoodIn", "exhaust", "chamber", "floor", "window")
                       and not p.startswith("panel")]
    h_out = dict(panelL=2.6, panelR=2.6, panelF=2.6, panelB=2.6, panelTop=3.3, window=6.5)

    def T_bc():
        s = []
        s.append(f"    inlet {{ type fixedValue; value uniform {Tk(T_s):.3f}; }}")
        s.append(f"    hoodIn {{ type fixedValue; value uniform {Tk(T_s + args.hood_pickup):.3f}; }}")
        s.append(f"    exhaust {{ type inletOutlet; inletValue uniform {Tk(T_s):.3f}; value uniform {Tk(T_s):.3f}; }}")
        s.append(f"    chamber {{ type fixedValue; value uniform {Tk(60.0):.3f}; }}")
        s.append(f"    floor {{ type externalWallHeatFluxTemperature; mode flux; q uniform {q_floor:.4f}; kappaMethod fluidThermo; "
                 f"value uniform {Tk(T_s + 5):.3f}; }}")
        for p, h in h_out.items():
            if p in mesh["patches"]:
                s.append(f"    {p} {{ type externalWallHeatFluxTemperature; mode coefficient; h uniform {h}; Ta constant {Tk(T_s):.3f}; "
                         f"kappaMethod fluidThermo; value uniform {Tk(T_s + 5):.3f}; }}")
        for p, w in heated.items():
            s.append(f"    {p} {{ type externalWallHeatFluxTemperature; mode power; Q constant {w:.4f}; kappaMethod fluidThermo; "
                     f"value uniform {Tk(T_s + 5):.3f}; }}")
        s.append(f"    \"({'|'.join(walls_adiabatic)})\" {{ type zeroGradient; }}")
        return "\n".join(s)

    allwalls = [p for p in mesh["patches"] if p not in ("inlet", "hoodIn", "exhaust")]
    W = "|".join(allwalls)
    files = {
        "0/U": hdr("volVectorField", "U") + f"""dimensions [0 1 -1 0 0 0 0];
internalField uniform (0 0 0);
boundaryField
{{
    inlet {{ type fixedValue; value uniform ({U_in[0]:.5f} {U_in[1]:.5f} {U_in[2]:.5f}); }}
    hoodIn {{ type fixedValue; value uniform (0 0 {-v_hood:.5f}); }}
    exhaust {{ type pressureInletOutletVelocity; value uniform (0 0 0); }}
    "({W})" {{ type noSlip; }}
}}
""",
        "0/T": hdr("volScalarField", "T") + f"""dimensions [0 0 0 1 0 0 0];
internalField uniform {Tk(T_s + 5):.3f};
boundaryField
{{
{T_bc()}
}}
""",
        "0/p": hdr("volScalarField", "p") + f"""dimensions [1 -1 -2 0 0 0 0];
internalField uniform 1e5;
boundaryField
{{
    ".*" {{ type calculated; value uniform 1e5; }}
}}
""",
        "0/p_rgh": hdr("volScalarField", "p_rgh") + f"""dimensions [1 -1 -2 0 0 0 0];
internalField uniform 1e5;
boundaryField
{{
    exhaust {{ type prghPressure; p uniform 1e5; value uniform 1e5; }}
    "(inlet|hoodIn|{W})" {{ type fixedFluxPressure; value uniform 1e5; }}
}}
""",
        "0/k": hdr("volScalarField", "k") + f"""dimensions [0 2 -2 0 0 0 0];
internalField uniform 1e-3;
boundaryField
{{
    "(inlet|hoodIn)" {{ type fixedValue; value uniform {k_in:.4g}; }}
    exhaust {{ type inletOutlet; inletValue uniform 1e-3; value uniform 1e-3; }}
    "({W})" {{ type kqRWallFunction; value uniform 1e-3; }}
}}
""",
        "0/epsilon": hdr("volScalarField", "epsilon") + f"""dimensions [0 2 -3 0 0 0 0];
internalField uniform 1e-4;
boundaryField
{{
    "(inlet|hoodIn)" {{ type fixedValue; value uniform {eps_in:.4g}; }}
    exhaust {{ type inletOutlet; inletValue uniform 1e-4; value uniform 1e-4; }}
    "({W})" {{ type epsilonWallFunction; value uniform 1e-4; }}
}}
""",
        "0/nut": hdr("volScalarField", "nut") + f"""dimensions [0 2 -1 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "(inlet|hoodIn|exhaust)" {{ type calculated; value uniform 0; }}
    "({W})" {{ type nutkWallFunction; value uniform 0; }}
}}
""",
        "0/alphat": hdr("volScalarField", "alphat") + f"""dimensions [1 -1 -1 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "(inlet|hoodIn|exhaust)" {{ type calculated; value uniform 0; }}
    "({W})" {{ type compressible::alphatJayatillekeWallFunction; Prt 0.85; value uniform 0; }}
}}
""",
        "constant/g": hdr("uniformDimensionedVectorField", "g") + "dimensions [0 1 -2 0 0 0 0];\nvalue (0 0 -9.81);\n",
        "constant/thermophysicalProperties": hdr("dictionary", "thermophysicalProperties") + """thermoType
{
    type            heRhoThermo;
    mixture         pureMixture;
    transport       const;
    thermo          hConst;
    equationOfState perfectGas;
    specie          specie;
    energy          sensibleEnthalpy;
}
mixture
{
    specie { molWeight 28.96; }
    thermodynamics { Cp 1007; Hf 0; }
    transport { mu 1.9e-05; Pr 0.71; }
}
""",
        "constant/turbulenceProperties": hdr("dictionary", "turbulenceProperties")
        + "simulationType RAS;\nRAS\n{\n    RASModel kEpsilon;\n    turbulence on;\n    printCoeffs on;\n}\n",
        "system/controlDict": hdr("dictionary", "controlDict") + f"""application buoyantSimpleFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime {args.iters};
deltaT 1;
writeControl timeStep;
writeInterval {args.iters};
purgeWrite 1;
writeFormat ascii;
writePrecision 7;
writeCompression off;
timeFormat general;
runTimeModifiable true;
functions
{{
    wallHeatFlux {{ type wallHeatFlux; libs (fieldFunctionObjects); writeControl timeStep; writeInterval 50; log false; }}
    exhaustFlow {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name exhaust; operation sum; fields (phi);
                  writeFields false; writeControl timeStep; writeInterval 10; log false; }}
    exhaustT {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name exhaust; operation weightedAverage;
               weightField phi; fields (T); writeFields false; writeControl timeStep; writeInterval 10; log false; }}
    volT {{ type volFieldValue; libs (fieldFunctionObjects); operation volAverage; fields (T); writeFields false;
           writeControl timeStep; writeInterval 10; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 10; fields (T U);
             probeLocations ((-0.300 -0.040 0.070) (-0.215 -0.190 0.300) (0.020 -0.100 0.330) (0.050 0.120 0.320) (-0.380 0.0 0.330)); }}
}}
""",
        "system/fvSchemes": hdr("dictionary", "fvSchemes") + """ddtSchemes { default steadyState; }
gradSchemes { default Gauss linear; }
divSchemes
{
    default none;
    div(phi,U) bounded Gauss linearUpwind grad(U);
    div(phi,h) bounded Gauss limitedLinear 1;
    div(phi,K) bounded Gauss linear;
    div(phi,k) bounded Gauss upwind;
    div(phi,epsilon) bounded Gauss upwind;
    div(phi,age) bounded Gauss upwind;
    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}
laplacianSchemes { default Gauss linear corrected; }
interpolationSchemes { default linear; }
snGradSchemes { default corrected; }
wallDist { method meshWave; }
""",
        "system/fvSolution": hdr("dictionary", "fvSolution") + """solvers
{
    p_rgh { solver GAMG; smoother DIC; tolerance 1e-8; relTol 0.01; }
    "(U|h|k|epsilon)" { solver PBiCGStab; preconditioner DILU; tolerance 1e-8; relTol 0.1; }
    age { solver PBiCGStab; preconditioner DILU; tolerance 1e-8; relTol 0; }
}
SIMPLE
{
    momentumPredictor yes;
    nNonOrthogonalCorrectors 0;
    residualControl { p_rgh 1e-5; U 1e-5; h 1e-6; "(k|epsilon)" 1e-5; }
}
relaxationFactors
{
    fields { rho 1.0; p_rgh 0.7; }
    equations { U 0.3; h 0.3; "(k|epsilon)" 0.5; }
}
""",
        "system/decomposeParDict": hdr("dictionary", "decomposeParDict") + "numberOfSubdomains 2;\nmethod scotch;\n",
        "system/ageDict": hdr("dictionary", "ageDict") + """functions
{
    age
    {
        type            age;
        libs            (fieldFunctionObjects);
        phi             phi;
        rho             rho;
        schemesField    age;
        tolerance       1e-6;
        nCorr           2000;
        diffusion       on;
    }
}
""",
    }
    for name, txt in files.items():
        (out / name).parent.mkdir(parents=True, exist_ok=True)
        (out / name).write_text(txt)
    (out / "case.foam").write_text("")
    meta = dict(h_mm=args.h, load=args.load, supply_c=T_s, hood_pickup_k=args.hood_pickup, q_exhaust_m3h=q_ex, q_hood_m3h=q_hood,
                q_inlet_m3h=q_in, inlet_angle_deg=args.inlet_angle, U_inlet=U_in, v_hood=v_hood, heat_W=heated, legs_to_floor_W=legs,
                floor_flux_W_m2=q_floor, wellmixed_guard_c=Tg_wm, mesh={k: v for k, v in mesh.items()}, n=[nx, ny, nz],
                names=names, parts_used=used, parts_skipped=skipped, h_out=h_out, variant=args.variant)
    (out / "case_meta.json").write_text(json.dumps(meta, indent=1, default=float))
    print(f"{out}: {nx} x {ny} x {nz} grid, {mesh['cells']} fluid cells, {mesh['faces']} faces; inlet {q_in:.1f} m3/h over "
          f"{A_in:.4f} m2 (v_n {vn:.3f} m/s), hood {q_hood:.1f} m3/h over {A_hood:.4f} m2; heat {sum(heated.values()):.1f} W + legs "
          f"{legs:.1f} W; skipped {len(skipped)}")
    print("patches:", {p: (n, round(mesh['area_m2'][p], 4)) for p, n in mesh["patches"].items()})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("dump")
    a.add_argument("--stl", default="/tmp/guard-cfd/stl")
    a = sub.add_parser("case")
    a.add_argument("--stl", default="/tmp/guard-cfd/stl")
    a.add_argument("--out", required=True)
    a.add_argument("--h", type=float, default=12.0, help="largest cell size, mm")
    a.add_argument("--load", choices=("typical", "worst"), default="typical")
    a.add_argument("--supply-c", type=float, default=30.2, help="supply (Shuttle) air, C: 30.2 typical, 38.0 busy")
    a.add_argument("--hood-pickup", type=float, default=0.5)
    a.add_argument("--q-exhaust", type=float, default=None)
    a.add_argument("--q-hood", type=float, default=None)
    a.add_argument("--inlet-angle", type=float, default=PHI_TRAP, help="downward angle of the inlet air, deg (trap's last leg)")
    a.add_argument("--iters", type=int, default=1500)
    a.add_argument("--variant", default="as drawn")
    a = sub.add_parser("post")
    a.add_argument("cases", nargs="+")
    args = ap.parse_args()
    if args.cmd == "dump":
        dump(args.stl)
    elif args.cmd == "case":
        write_case(args)
    else:
        import guard_cfd_post
        guard_cfd_post.main(args.cases)
