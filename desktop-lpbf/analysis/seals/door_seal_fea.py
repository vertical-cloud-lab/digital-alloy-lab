"""CalculiX check of the drop-down door as a seal carrier (issue #260, PR #266).

The door FEA in analysis/fea/fea.py (case 3) loads the door with the atmosphere at vacuum and puts it on its land.
What it leaves out is the O-ring itself: at +20 mbar during a build only the two draw latches hold the door against its
own cord, and the door bends between them.

Since 2026-11-23 (round 5) each McMaster 1807A61 draw latch sits on a 6061 bracket bolted to the front face of a door
ear and points forward; its hook pulls a strike on the chamber's side face straight back (+y), along a line outboard of
the ear (x = +/-158 as drawn). Everything below is read from cad/lpbf_low.py (round 6, 2026-11-25; until then this
script held fixed x 128-156, z 40-68 patches on the ears and took the latch line at z 54):
  - the door's mesh includes the two brackets, their feet bonded to the ears' front faces (the brackets' screws are
    not drawn);
  - each latch is a rigid body on its base's footprint on the bracket's outer face, with its reference node on the
    pull line (the latch base's face + LATCH_PULL_E);
  - the hinges are the leaves' footprints on the door's front face. Their pin holes are slotted +/-0.6 mm in y, so the
    door floats on its cord and the hinges hold z only, unless a pin reaches the end of its slot;
  - the O-ring: its reaction (Lindley, FKM 75A) as a uniform pressure on the groove floor, plus linear springs on the
    groove floor's nodes at Lindley's tangent stiffness, so the cord pushes less where the door bows away; +20 mbar on
    the door's back face inside the seal.
Cases:
  A  the latch hooks held in y where the squeeze would be 25 % with a rigid door; hinges floating;
  B  as A with the hinge pins at the ends of their slots (y and z held);
  C  the boundary conditions used up to round 5, for comparison: the door alone, the brackets' feet's footprints held in
     y, the hinges in y and z, no cord stiffness;
  D  the round-5 design: each latch preloaded to 0.75, 1.2 or 1.78 kN (a force on its reference node), hinges floating,
     and the door's land (its back face where the frame or the floor plate is behind it) in contact with the chamber's
     front face. Contact is solved by an active set of penalty springs: on where the door presses, off where it would
     pull, re-solved until the set stops changing. The squeeze is then measured from the land's metal-to-metal 25.8 %.
     The latches pull 12 mm outboard of the ears' tips, so the door pivots on them and opens in the middle (D1200);
  E  the fix drawn since 2026-11-25: as D, with the hinge holding the door's bottom edge where its land touches
     (round pin holes, the chamber's knuckle blocks shimmed at assembly; the FEA takes the hinge as rigid);
  F  a what-if, not drawn: E plus a rib along the door's top edge (DOOR_FEA_RIB="h,d,half-length").
Results: squeeze, line load and contact pressure along the gland (also at the gland's worst tolerance, from seals.py's
gland check), the land gap, the latch and hinge loads against the latch's rating, and von Mises in the door, ears and
brackets against 6061-T6's yield.

Run:  FEA_RUN=/tmp/<you>/fea OMP_NUM_THREADS=2 /tmp/capmem 4 python desktop-lpbf/analysis/seals/door_seal_fea.py [--cases=A,D1200] [--md-only]
      ->  analysis/out/seals/door_seal_fea.{json,md}, door_seal_A.png, door_seal_D1200.png
      (~50k nodes at hmin 1.5 mm, SPOOLES; ~100 s per solve; cases D take 3-6 solves each)
"""
from __future__ import annotations

import gc
import json
import math
import os
import pathlib
import re
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "fea"))
sys.path.insert(0, str(HERE))
import fea as F          # noqa: E402  (meshing, CalculiX I/O and rendering helpers; imports cad/lpbf_low as F.M)
import seals as SE       # noqa: E402  (Lindley load per length, Gent modulus)

OUT = ROOT / "analysis" / "out" / "seals"
LATCH_PULL_E = 12.0      # mm, the hook's pull line above the latch base (lpbf_low: base on the bracket face at x 146, pull at x 158)
P_BUILD = 0.002          # MPa, +20 mbar during a build
SQUEEZE = 0.25           # design squeeze at the latch line
SLOT = 0.6               # mm, the hinge pin holes' slot half-length in y (lpbf_low section 8)
HMAX = float(os.environ.get("DOOR_FEA_HMAX", "5.0"))   # mm, largest element
HMIN = float(os.environ.get("DOOR_FEA_HMIN", "1.5"))   # mm, smallest (at the groove's curves; the mesh check is in door_seal_fea.md)


def bbox(s):
    b = s.BoundingBox()
    return np.array([b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax])


def geometry(parts):
    """Latch, bracket and hinge positions from the built model (one entry per side, right first)."""
    P = F.P
    dy1 = -P["cy"]
    dy0 = dy1 - 15.0
    lat = F.part(parts, "Draw latches on the door")
    brk = F.part(parts, "Draw-latch brackets on the door")
    hng = F.part(parts, "Door hinge leaves")
    door = F.part(parts, "Chamber door")
    bd = bbox(door.shape)
    import cadquery as cq
    sides = []
    for s in sorted(lat.shape.Solids(), key=lambda s: -s.Center().x):
        b = bbox(s)
        sx = 1.0 if b[0] + b[3] > 0 else -1.0
        x_base = b[0] if sx > 0 else b[3]                       # the latch base's face on the bracket's outer face
        br = [t for t in brk.shape.Solids() if np.sign(t.Center().x) == sx][0]
        bb = bbox(br)
        foot = bbox(br.intersect(door.shape.translate(cq.Vector(0.0, -0.4, 0.0))))   # where the foot touches the ear's front face
        sides.append(dict(sx=sx, x_base=float(x_base), x_pull=float(x_base + sx * LATCH_PULL_E), z_pull=float((b[2] + b[5]) / 2),
                          latch_y=(float(b[1]), float(b[4])), latch_z=(float(max(b[2], bb[2])), float(min(b[5], bb[5]))),
                          bracket_bbox=bb.tolist(), plate_t=float(min(bb[3] - bb[0], 6.0)), foot_x=(float(foot[0]), float(foot[3])),
                          foot_z=(float(foot[2]), float(foot[5]))))
    leaves = []
    for s in hng.shape.Solids():
        b = bbox(s)
        if abs(b[4] - dy0) < 0.05 and b[4] - b[1] < 4.0:        # the flat leaves screwed to the door's front face
            leaves.append(dict(x=(float(b[0]), float(b[3])), z=(float(max(b[2], bd[2])), float(min(b[5], bd[5])))))
    if len(sides) != 2 or len(leaves) != 2:
        raise RuntimeError(f"expected 2 latches and 2 hinge leaves, found {len(sides)} and {len(leaves)}")
    return dict(dy0=dy0, dy1=dy1, door_bbox=bd.tolist(), latches=sides, hinge_leaves=leaves, hinge_axis=list(F.M.DOOR_HINGE),
                latch_pn="McMaster 1807A61", latch_rating_N=F.M.LATCH_1807A61["rating_N"], latch_pos=dict(F.M.LATCH_POS))


def clearances(parts):
    """Closest distances (OpenCascade, exact) from the latches and brackets to their neighbours, door shut."""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    out = {}
    pairs = (("Draw latches on the door", "Optics bridge posts"), ("Draw-latch brackets on the door", "Optics bridge posts"),
             ("Draw-latch actuators", "Optics bridge posts"))
    for a, b in pairs:
        try:
            d = BRepExtrema_DistShapeShape(F.part(parts, a).shape.wrapped, F.part(parts, b).shape.wrapped)
            d.Perform()
            out[f"{a} | {b}"] = float(d.Value()) if d.IsDone() else None
        except KeyError:
            continue
    return out


def lumped(m, fs):
    """Node ids and lumped areas (HRZ weights of the 6-node triangle: corners 0.0526, mid-sides 0.2807) of a face set."""
    w = np.array([1 / 30, 1 / 30, 1 / 30, 32 / 180, 32 / 180, 32 / 180])
    w = w / w.sum()
    ids, inv = np.unique(fs["tri"].ravel(), return_inverse=True)
    a = np.zeros(len(ids))
    np.add.at(a, inv, (fs["area"][:, None] * w[None, :]).ravel())
    return ids, a


def springs(eid0, ids, k):
    """SPRING1 elements (y) on nodes `ids` with stiffnesses `k` (N/mm), binned into 40 stiffness groups."""
    edges = np.quantile(k, np.linspace(0, 1, 41))
    grp = np.clip(np.searchsorted(edges, k, side="right") - 1, 0, 39)
    s, e = "", eid0
    for g in range(40):
        sel = grp == g
        if not sel.any():
            continue
        s += f"*ELEMENT, TYPE=SPRING1, ELSET=SPR{g}\n" + "".join(f"{e + i},{int(n)}\n" for i, n in enumerate(ids[sel]))
        e += int(sel.sum())
        s += f"*SPRING, ELSET=SPR{g}\n2\n{k[sel].mean():.6f}\n"
    return s


def dat_totals(job):
    """Total forces per node set from the .dat file (*NODE PRINT, TOTALS=ONLY)."""
    txt = (F.RUN / f"{job}.dat").read_text().splitlines()
    out = {}
    for i, l in enumerate(txt):
        mm = re.match(r"\s*total force \(fx,fy,fz\) for set (\S+)", l)
        if mm:
            for l2 in txt[i + 1:i + 4]:
                p = l2.split()
                if len(p) == 3:
                    out[mm.group(1)] = [float(v) for v in p]
                    break
    return out


def hertz(w_line, cs, E):
    """Contact half-width and mean / peak pressure of a cord pressed on a flat (Hertz line contact, rubber nu = 0.5)."""
    Es = E / (1 - 0.5 ** 2)
    a = math.sqrt(4 * w_line * (cs / 2) / (math.pi * Es))
    return a, w_line / (2 * a), 2 * w_line / (math.pi * a)


def where(p):
    x, z = p[0], p[2]
    if z > 95:
        v = "top"
    elif z < 13:
        v = "bottom"
    else:
        v = "side"
    return f"{v} (x {x:.0f}, z {z:.0f})"


def selections(m, G, gd, gl):
    """Groove floor, the face inside the seal, the hinge leaves' footprints and the bracket feet's footprints on mesh m."""
    dy0, dy1 = G["dy0"], G["dy1"]
    f_groove = F.faces_on(m, F.surfaces(m, F.planar("y", dy1 - gd)))
    gn = m["idx"][np.unique(f_groove["tri"].ravel())]
    xg, zg = m["xyz"][gn, 0], m["xyz"][gn, 2]
    w = gl["width"]
    in_x, in_z0, in_z1 = np.abs(xg).max() - w, zg.min() + w, zg.max() - w       # inner wall of the groove
    f_inside = F.faces_on(m, F.surfaces(m, F.planar("y", dy1)), lambda c: (np.abs(c[:, 0]) <= in_x) & (c[:, 2] >= in_z0) & (c[:, 2] <= in_z1))
    front = F.surfaces(m, F.planar("y", dy0))
    hinge = np.concatenate([F.nodes_on(m, front, lambda q, h=h: (q[:, 0] >= h["x"][0] - 0.01) & (q[:, 0] <= h["x"][1] + 0.01)
                                       & (q[:, 2] >= h["z"][0] - 0.01) & (q[:, 2] <= h["z"][1] + 0.01)) for h in G["hinge_leaves"]])
    feet = []
    for L in G["latches"]:
        x0, x1 = sorted(abs(v) for v in L["foot_x"])
        feet.append(F.nodes_on(m, front, lambda q, L=L, x0=x0, x1=x1: (q[:, 0] * L["sx"] >= x0 - 0.01) & (q[:, 0] * L["sx"] <= x1 + 0.01)
                               & (q[:, 2] >= L["foot_z"][0] - 0.01) & (q[:, 2] <= L["foot_z"][1] + 0.01)))
    h0 = G["hinge_leaves"][0]
    px = F.nearest(m, ((h0["x"][0] + h0["x"][1]) / 2, dy0, (h0["z"][0] + h0["z"][1]) / 2), hinge)
    return dict(f_groove=f_groove, gn=gn, f_inside=f_inside, hinge=hinge, feet=np.concatenate(feet), px=px)


def land_nodes(m, G, parts):
    """Door back-face nodes that have chamber material right behind them (the land: outside the door opening and the
    groove, on the frame or the floor plate), by testing a point 0.3 mm behind each node against those solids."""
    dy1 = G["dy1"]
    back = F.nodes_on(m, F.surfaces(m, F.planar("y", dy1)))
    solids = []
    for pre in ("Process chamber body", "Chamber floor plate"):
        try:
            solids += F.part(parts, pre).shape.Solids()
        except KeyError:
            pass
    import trimesh
    xyz = m["xyz"][m["idx"][back]].copy()
    xyz[:, 1] = dy1 + 0.3
    keep = np.zeros(len(xyz), bool)
    for s in solids:                                   # tessellated (0.05 mm) and tested by ray casting: OCC's classifier took minutes
        v, f = s.tessellate(0.05, 0.2)
        tm = trimesh.Trimesh(np.array([[p.x, p.y, p.z] for p in v]), np.array(f), process=True)
        bb = tm.bounds
        cand = np.all((xyz >= bb[0] - 1e-6) & (xyz <= bb[1] + 1e-6), axis=1) & ~keep
        if cand.any():
            keep[np.where(cand)[0][tm.contains(xyz[cand])]] = True
    return back[keep]


def latch_rigid_bodies(mm, G):
    """*RIGID BODY cards: each latch base's footprint on its bracket, reference node on the pull line."""
    nmax = int(mm["ntags"].max())
    extra, refs = "", []
    for k, L in enumerate(G["latches"]):
        face = F.surfaces(mm, F.planar("x", L["x_base"]))
        (y0, y1), (z0, z1) = L["latch_y"], L["latch_z"]
        ids = F.nodes_on(mm, face, lambda q, y0=y0, y1=y1, z0=z0, z1=z1: (q[:, 1] >= y0 - 0.01) & (q[:, 1] <= y1 + 0.01)
                         & (q[:, 2] >= z0 - 0.01) & (q[:, 2] <= z1 + 0.01))
        if len(ids) == 0:
            raise RuntimeError("latch patch empty")
        nr, nq = nmax + 1 + 2 * k, nmax + 2 + 2 * k
        refs.append(nr)
        yc = float(np.mean(L["latch_y"]))
        extra += (F.nset(f"LAT{k}", ids) + f"*NODE, NSET=REF{k}\n{nr},{L['x_pull']:.4f},{yc:.4f},{L['z_pull']:.4f}\n"
                  f"*NODE\n{nq},{L['x_pull']:.4f},{yc:.4f},{L['z_pull']:.4f}\n*RIGID BODY, NSET=LAT{k}, REF NODE={nr}, ROT NODE={nq}\n")
        L["patch_nodes"] = int(len(ids))
    return extra, refs


K_PEN = 1.0e5            # N/mm per land node in contact (penalty; ~E x 1.5 mm)
S_METAL = None           # squeeze with the land metal-to-metal: (cord - depth) / cord, set in main()


def solve(job, mm, sl, G, cfg, F_or_s0, k_line, w, active=None, land=None):
    """One linear CalculiX solve of a configuration; returns U, vm, the .dat totals and the cord springs' (ids, k)."""
    f_groove, f_inside, hinge, px = sl["f_groove"], sl["f_inside"], sl["hinge"], sl["px"]
    p_or = F_or_s0 / f_groove["area"].sum()
    ids_s, a_s = lumped(mm, f_groove)
    k_s = k_line / w * a_s
    extra, refs, prints = F.nset("HINGE", hinge), [], "*NODE PRINT, NSET=HINGE, TOTALS=ONLY\nRF\n"
    if cfg["latch"] == "ears":
        extra += F.nset("EAR", sl["feet"])
        bc = "EAR,2,2\n"
        prints += "*NODE PRINT, NSET=EAR, TOTALS=ONLY\nRF\n"
    else:
        rb, refs = latch_rigid_bodies(mm, G)
        extra += rb
        bc = "".join(f"{nr},2,2\n" for nr in refs) if cfg["latch"] == "hook" else ""
        prints += "".join(f"*NODE PRINT, NSET=REF{k}, TOTALS=ONLY\nRF\n" for k in range(len(refs)))
    eid = len(mm["tets"]) + 1
    if cfg["springs"]:
        extra += springs(eid, ids_s, k_s)
        eid += len(ids_s)
    if active is not None and len(active):
        extra += f"*ELEMENT, TYPE=SPRING1, ELSET=LAND\n" + "".join(f"{eid + i},{int(n)}\n" for i, n in enumerate(active)) + f"*SPRING, ELSET=LAND\n2\n{K_PEN:.1f}\n"
    F.write_model(job, mm, F.AL, extra)
    bc += ("HINGE,3,3\n" if cfg["hinge"] == "float" else "HINGE,2,3\n") + f"{px},1,1\n"
    loads = "*DLOAD\n" + F.dload_lines(f_groove, p_or) + F.dload_lines(f_inside, P_BUILD)
    if cfg["latch"] == "force":
        loads += "*CLOAD\n" + "".join(f"{nr},2,{cfg['P']:.6g}\n" for nr in refs)
    F.append(job, f"*STEP\n*STATIC\n*BOUNDARY\n{bc}" + loads + prints + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    F.run_ccx(job)
    U, S, vm = F.static_results(mm, job)
    return U, vm, dat_totals(job), refs, (ids_s, k_s)


def main(argv=()):
    global S_METAL
    want = next((a.split("=", 1)[1].split(",") for a in argv if a.startswith("--cases=")), None)
    if "--md-only" in argv:                                                       # re-write the note from the last results
        write_md(json.loads((OUT / "door_seal_fea.json").read_text()))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    parts = F.M.build()
    P = F.P
    G = geometry(parts)
    dy0 = G["dy0"]
    gd = P.get("door_gland_d", 2.8)
    gl = F.M.GLANDS["door"]
    cs = gl["cs"]
    w = gl["width"]
    S_METAL = (cs - gd) / cs
    E75 = SE.gent_E(SE.SHORE_FKM)
    door = F.part(parts, "Chamber door").shape
    brk = F.part(parts, "Draw-latch brackets on the door").shape
    clr = clearances(parts)
    # hmax 5 as fea.py's door case: at hmax 4 the rigid-body solve outgrew a 4 GB cap next to the built model
    meshes = dict(full=F.mesh_shape(door.fuse(brk).clean(), "door_seal", hmax=HMAX, hmin=HMIN),
                  door=F.mesh_shape(door, "door_seal_door", hmax=HMAX, hmin=HMIN))
    # what-if (cases F): a stiffening rib along the door's top edge on its front face, h (z) x d (y) x 2 xh (x), from DOOR_FEA_RIB
    rh, rd, rx = (float(v) for v in os.environ.get("DOOR_FEA_RIB", "12,20,112").split(","))
    zt = G["door_bbox"][5]
    import cadquery as cq
    rib = cq.Solid.makeBox(2 * rx, rd, rh, cq.Vector(-rx, dy0 - rd, zt - rh))
    G["rib"] = dict(h=rh, d=rd, x=rx, z=(zt - rh, zt), y=(dy0 - rd, dy0))
    if want is None or any(k.startswith("F") for k in want):
        meshes["rib"] = F.mesh_shape(door.fuse(brk).fuse(rib).clean(), "door_seal_rib", hmax=HMAX, hmin=HMIN)
    land = {k: land_nodes(meshes[k], G, parts) for k in meshes if k != "door"}
    del parts, door, brk                                                          # free the machine model before CalculiX runs
    gc.collect()
    sels = {k: selections(mm, G, gd, gl) for k, mm in meshes.items()}
    path = gl["inner_perimeter"] + np.pi * w                                      # centre line of the groove, as seals.py
    k_line = E75 * (1.875 * SQUEEZE ** 0.5 + 300 * SQUEEZE ** 5)                  # d(F/L)/d(delta) of Lindley's relation, N/mm per mm
    R = dict(geometry=G, path_mm=path, groove_depth_mm=gd, cord_mm=cs, E_fkm_MPa=E75, F_oring_N=SE.lindley(cs, SQUEEZE) * path,
             F_oring_metal_N=SE.lindley(cs, S_METAL) * path, squeeze_metal_pct=100 * S_METAL, k_line_N_per_mm2=k_line, hmax_mm=HMAX, hmin_mm=HMIN,
             nodes=len(meshes["full"]["ntags"]), nodes_door_only=len(meshes["door"]["ntags"]), land_nodes=int(len(land["full"])), clearances_mm=clr, cases=[])
    R["groove_floor_area_mm2"] = float(sels["full"]["f_groove"]["area"].sum())
    R["F_overpressure_N"] = P_BUILD * float(sels["full"]["f_inside"]["area"].sum())
    rating = G["latch_rating_N"]
    cases = [dict(key="A", label="hinges float in their slots (z only), latch hooks held on their pull lines at the 25 % position, cord stiffness",
                  mesh="full", latch="hook", hinge="float", springs=True, s0=SQUEEZE),
             dict(key="B", label="as A, with the hinge pins at the ends of their slots (y and z held)", mesh="full", latch="hook", hinge="held",
                  springs=True, s0=SQUEEZE),
             dict(key="C", label="round-5 boundary conditions: door alone, the brackets' feet's footprints held in y, hinges y and z, no cord stiffness",
                  mesh="door", latch="ears", hinge="held", springs=False, s0=SQUEEZE)]
    for Pk in (0.75, 1.2, 1.78):
        cases.append(dict(key=f"D{int(round(Pk * 1000))}", label=f"design: each latch preloaded to {Pk:.2f} kN ({100 * Pk * 1000 / rating:.0f} % of its rating), "
                          "hinges floating, the door's land in contact with the chamber's front face where pulled onto it, cord stiffness",
                          mesh="full", latch="force", hinge="float", springs=True, s0=S_METAL, contact=True, P=Pk * 1000.0))
    for Pk in (0.75, 1.2):
        cases.append(dict(key=f"E{int(round(Pk * 1000))}", label=f"as D at {Pk:.2f} kN, but the hinge pins hold the door's bottom edge where its land touches "
                          "(no float: the hinge set at assembly and locked)",
                          mesh="full", latch="force", hinge="held", springs=True, s0=S_METAL, contact=True, P=Pk * 1000.0))
    for Pk in (0.75, 1.2):
        cases.append(dict(key=f"F{int(round(Pk * 1000))}", label=f"as E at {Pk:.2f} kN, with a {G['rib']['h']:.0f} x {G['rib']['d']:.0f} mm rib along the door's top "
                          f"edge on its front face (x ±{G['rib']['x']:.0f})",
                          mesh="rib", latch="force", hinge="held", springs=True, s0=S_METAL, contact=True, P=Pk * 1000.0))
    order = [c["key"] for c in cases]
    if want:                                                                      # run some cases, in the order given; keep the others from the last run
        cases = sorted([c for c in cases if c["key"] in want], key=lambda c: want.index(c["key"]))
        jp = OUT / "door_seal_fea.json"
        if jp.exists():
            R["cases"] = [c for c in json.loads(jp.read_text()).get("cases", []) if c.get("case") not in want]
    vm_lim = F.AL["sy"]
    land_sets = {k: set(int(n) for n in v) for k, v in land.items()}
    for cfg in cases:
        key = cfg["key"]
        mm, sl = meshes[cfg["mesh"]], sels[cfg["mesh"]]
        xyz = mm["xyz"]
        gn = sl["gn"]
        lnd = land.get(cfg["mesh"])
        F_or_s0 = SE.lindley(cs, cfg["s0"]) * path
        job = f"door_seal_{key}"
        it_log = []
        if cfg.get("contact"):
            active = np.array(sorted(land_sets[cfg["mesh"]]), dtype=np.int64)
            for it in range(12):
                U, vm, tot, refs, (ids_s, k_s) = solve(job, mm, sl, G, cfg, F_or_s0, k_line, w, active=active, land=lnd)
                u_l = U[mm["idx"][lnd], 1]
                act = set(int(n) for n in active)
                inside = np.array([int(n) in act for n in lnd])
                new = lnd[(inside & (u_l > -1e-7)) | (~inside & (u_l > 1e-7))]
                it_log.append(dict(it=it, active=int(len(active)), next=int(len(new)), contact_N=float(K_PEN * u_l[inside].sum())))
                print(f"    {key} it {it}: {len(active)} land nodes in contact -> {len(new)}; contact force {it_log[-1]['contact_N']:.0f} N", flush=True)
                if set(int(n) for n in new) == act:
                    break
                active = new
        else:
            U, vm, tot, refs, (ids_s, k_s) = solve(job, mm, sl, G, cfg, F_or_s0, k_line, w)
            active = None
        uy = U[gn, 1]                                     # + toward the chamber (more squeeze), - away (squeeze lost)
        sq = cfg["s0"] + uy / cs
        i_lo, i_hi = int(np.argmin(uy)), int(np.argmax(uy))
        wl = SE.lindley(cs, np.clip(sq, 0, None))         # cord line load along the gland, N/mm
        a_lo, pm_lo, pk_lo = hertz(float(wl.min()), cs, E75)
        a_hi, pm_hi, pk_hi = hertz(float(wl.max()), cs, E75)
        if cfg["latch"] == "ears":
            latch = [abs(tot["EAR"][1]) / 2] * 2
        elif cfg["latch"] == "hook":
            latch = [abs(tot[f"REF{k}"][1]) for k in range(len(refs))]
        else:
            latch = [cfg["P"]] * len(refs)
        hinge_y = abs(tot["HINGE"][1]) / 2
        # land gap (the door's back face to the chamber's front face) on the land: from 0 in contact (case D) or from the nominal
        # gap at 25 % squeeze (A-C: the latches set the squeeze, the land never touches)
        if lnd is not None:
            ul = U[mm["idx"][lnd], 1]
            gap0 = 0.0 if cfg.get("contact") else cs * (1 - cfg["s0"]) - gd
            gaps = gap0 - ul
            j = int(np.argmax(gaps))
            land_gap = dict(max_um=1000 * float(gaps.max()), at=xyz[mm["idx"][lnd[j]]].tolist(), nominal_um=1000 * gap0,
                            in_contact=int(0 if active is None else len(active)), of=int(len(lnd)))
        else:
            land_gap = None
        near_patch = np.zeros(len(xyz), bool)             # the rigid patches' edges are stress raisers of the model, not of the part
        in_brk = np.zeros(len(xyz), bool)
        for L in G["latches"]:
            near_patch |= (np.abs(xyz[:, 0] - L["x_base"]) < 3.0) & (xyz[:, 1] >= L["latch_y"][0] - 3) & (xyz[:, 1] <= L["latch_y"][1] + 3)
            b = L["bracket_bbox"]
            in_brk |= (xyz[:, 0] >= b[0] - 0.01) & (xyz[:, 0] <= b[3] + 0.01) & (xyz[:, 1] <= dy0 + 0.01)
        in_ear = (np.abs(xyz[:, 0]) > 124.0) & (xyz[:, 1] >= dy0 - 0.01)
        in_door = ~in_brk & ~in_ear

        def vmax(sel):
            j = np.where(sel)[0]
            if len(j) == 0:
                return 0.0, [0.0, 0.0, 0.0]
            jj = j[int(np.argmax(vm[j]))]
            return float(vm[jj]), xyz[jj].tolist()
        st = {n: vmax(s) for n, s in (("door", in_door), ("ears", in_ear), ("brackets", in_brk & ~near_patch), ("brackets_at_patch", in_brk & near_patch))}
        hn = mm["idx"][sl["hinge"]]
        r = dict(case=key, label=label_of(cfg), cord=cs, nodes=len(mm["ntags"]), squeeze_ref_pct=100 * cfg["s0"],
                 F_oring_ref_N=F_or_s0, F_overpressure_N=P_BUILD * float(sl["f_inside"]["area"].sum()),
                 squeeze_min_pct=100 * float(sq.min()), squeeze_min_at=xyz[gn][i_lo].tolist(), squeeze_max_pct=100 * float(sq.max()),
                 squeeze_max_at=xyz[gn][i_hi].tolist(), lost_max_um=1000 * float(max(cs * SQUEEZE - cs * sq.min(), 0.0)), lost_at=xyz[gn][i_lo].tolist(),
                 margin_to_15pct_um=1000 * cs * (float(sq.min()) - 0.15),
                 line_load_N_per_mm=(float(wl.min()), float(wl.max())), contact_width_mm=(2 * a_lo, 2 * a_hi),
                 contact_mean_MPa=(pm_lo, pm_hi), contact_peak_MPa=(pk_lo, pk_hi), land_gap=land_gap,
                 cord_force_N=float(F_or_s0 + (k_s * U[mm["idx"][ids_s], 1]).sum()) if cfg["springs"] else F_or_s0,
                 latch_load_each_N=float(max(latch)), latch_loads_N=[float(v) for v in latch], hinge_load_each_N=float(hinge_y),
                 hinge_y_travel_um=(1000 * float(U[hn, 1].min()), 1000 * float(U[hn, 1].max())),
                 latch_rating_N=rating, latch_sf=rating / float(max(latch)),
                 vm=st, sf_yield=vm_lim / max(st["door"][0], st["ears"][0], st["brackets"][0]),
                 sf_yield_at_patch=vm_lim / st["brackets_at_patch"][0] if st["brackets_at_patch"][0] > 0 else None,
                 iterations=it_log or None, ok=bool(sq.min() > 0.15))
        # the squeeze along the gland, sampled for the note: top, bottom and sides, centre and corners
        r["profile"] = profile(xyz[gn], sq)
        R["cases"].append(r)
        R["cases"].sort(key=lambda c: order.index(c["case"]) if c["case"] in order else 99)
        if key in ("A", "D1200", "E750", "F750"):
            png = f"door_seal_{key}.png"
            F.render(mm, U, -U[:, 1] * 1000, OUT / png, f"Door at +20 mbar, case {key}: {label_of(cfg)[:90]}\n"
                     f"squeeze along the gland {100 * sq.min():.1f}-{100 * sq.max():.1f} %",
                     (-0.8, -1.5, 0.6), label="outward deflection (um)", mark=xyz[gn][i_lo])
            r["png"] = png
        print(f"  case {key}: squeeze {100 * sq.min():.2f}-{100 * sq.max():.2f} % (min at {np.round(xyz[gn][i_lo], 0)}), latch {latch[0]:.0f}/{latch[1]:.0f} N, "
              f"hinge {hinge_y:.0f} N each, vm door {st['door'][0]:.1f}, ears {st['ears'][0]:.1f}, brackets {st['brackets'][0]:.1f} "
              f"({st['brackets_at_patch'][0]:.1f} at the patch) MPa" + (f", land gap up to {land_gap['max_um']:.0f} um" if land_gap else ""), flush=True)
        (OUT / "door_seal_fea.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    write_md(R)


def label_of(cfg):
    return cfg["label"]


def profile(p, sq):
    """Squeeze (%) at named places along the gland: the nearest groove-floor nodes to each."""
    xs, zs = p[:, 0], p[:, 2]
    x1, z0, z1 = np.abs(xs).max(), zs.min(), zs.max()
    pts = {"top centre": (0, z1), "bottom centre": (0, z0), "top, x = +/-60": (60, z1), "bottom, x = +/-60": (60, z0),
           "corners, top": (x1, z1), "corners, bottom": (x1, z0), "sides, mid-height (latch line)": (x1, (z0 + z1) / 2)}
    out = {}
    for n, (x, z) in pts.items():
        vals = []
        for sx in ((1, -1) if x else (1,)):
            d = (xs - sx * x) ** 2 + (zs - z) ** 2
            vals.append(100 * float(sq[int(np.argmin(d))]))
        out[n] = min(vals)
    return out


def tolerance_drop(R):
    """Squeeze the door gland loses at worst tolerance (AS568 cord, +/-0.05 mm machining, 60 C), seals.py's gland check: nominal - min."""
    g = SE.gland_dovetail(R["cord_mm"], R["groove_depth_mm"], F.M.MP.FACE_1P78["width"], F.M.MP.DOVETAIL_DEG, T_service=60.0, groove_mat="al")
    return g["squeeze_nom"] - g["squeeze_min"], g


def write_md(R):
    G = R["geometry"]
    L0 = G["latches"][0]
    h = G["hinge_leaves"]
    cases = R["cases"]
    tol, gt = tolerance_drop(R)
    for r in cases:
        r["squeeze_min_worst_tol_pct"] = r["squeeze_min_pct"] - tol
        r["ok_worst_tol"] = bool(r["squeeze_min_worst_tol_pct"] >= 15.0)
    (OUT / "door_seal_fea.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    L = ["# Door as a seal carrier: CalculiX, held by its latches (round 6, 2026-11-25)", "",
         f"Door: 6061-T6, 15 mm, with the two latch brackets bonded to its ears, from `cad/lpbf_low.py`. C3D10 mesh, {R['nodes']} nodes "
         f"(hmax {R['hmax_mm']:g}, hmin {R['hmin_mm']:g} mm; case C: the door alone, {R['nodes_door_only']} nodes). "
         f"Seal centre line {R['path_mm']:.0f} mm; {R['cord_mm']} mm FKM 75A cord in a {R['groove_depth_mm']} mm deep half-dovetail, so the land "
         f"is metal-to-metal at {R['squeeze_metal_pct']:.1f} % squeeze. Cord reaction from Lindley (E = {R['E_fkm_MPa']:.2f} MPa from Gent): "
         f"{R['F_oring_N']:.0f} N at 25 %, {R['F_oring_metal_N']:.0f} N at {R['squeeze_metal_pct']:.1f} %, as a uniform pressure on the groove floor, plus "
         f"(all but C) springs at Lindley's tangent stiffness, {R['k_line_N_per_mm2']:.2f} N/mm per mm of squeeze per mm of seal, so the cord pushes less "
         f"where the door bows away. +20 mbar on the {R['F_overpressure_N'] / 0.002:.0f} mm² inside the seal ({R['F_overpressure_N']:.0f} N).", "",
         "Positions read from the model:",
         f"- latches ({G['latch_pn']}, rated {G['latch_rating_N']:.0f} N): base on the bracket's outer face at x ±{abs(L0['x_base']):.0f}, "
         f"y {L0['latch_y'][0]:.0f} to {L0['latch_y'][1]:.0f}, z {L0['latch_z'][0]:.1f}-{L0['latch_z'][1]:.1f}, modelled as a rigid body; "
         f"pull line x ±{abs(L0['x_pull']):.0f}, z {L0['z_pull']:.0f} (the hook {LATCH_PULL_E:.0f} mm off the base, assumed);",
         f"- brackets' feet on the ears' front faces: x ±{abs(L0['foot_x'][0]):.0f} to ±{abs(L0['foot_x'][1]):.0f}, z {L0['foot_z'][0]:.0f}-{L0['foot_z'][1]:.0f}; "
         f"the pull line is {abs(L0['x_pull']) - max(abs(L0['foot_x'][0]), abs(L0['foot_x'][1])):.0f} mm outboard of the feet's outer edge "
         f"and {abs(L0['x_pull']) - 116.0:.0f} mm outboard of the gland's side runs;",
         f"- hinge leaves on the door's front face: x {h[0]['x'][0]:.0f} to {h[0]['x'][1]:.0f} and {h[1]['x'][0]:.0f} to {h[1]['x'][1]:.0f}, "
         f"z {h[0]['z'][0]:.0f} to {h[0]['z'][1]:.0f}; pin axis (y, z) = ({G['hinge_axis'][0]:.0f}, {G['hinge_axis'][1]:.0f}); the pin holes were slotted ±{SLOT} mm in y until 2026-11-25 (A and D float on them, B and C hold the pins at the slots' ends) and are round since (E, F);",
         f"- the land: {R['land_nodes']} nodes of the door's back face with the frame or the floor plate behind them (outside the door opening).", "",
         f"The gland itself spans {gt['squeeze_min']:.1f}-{gt['squeeze_max']:.1f} % squeeze over its tolerances (nominal {gt['squeeze_nom']:.1f} %, seals.py), "
         f"so the fifth column takes {tol:.1f} % off the lowest squeeze; it should stay at or above 15 %.", "",
         "| Case | Squeeze along the gland | Lowest at | Margin to 15 % | Lowest at worst tolerance | Cord line load | Contact pressure, mean / peak (Hertz) | Land gap, largest | Each latch | Latch SF on rating | Each hinge (y) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in cases:
        lg = r.get("land_gap")
        lgt = (f"{lg['max_um']:.0f} µm at x {lg['at'][0]:.0f}, z {lg['at'][2]:.0f}" + (f"; {lg['in_contact']} of {lg['of']} land nodes touch" if r.get("iterations") else
                                                                                       f" (nominal {lg['nominal_um']:.0f})")) if lg else "–"
        L.append(f"| **{r['case']}**: {r['label']} | {r['squeeze_min_pct']:.1f}–{r['squeeze_max_pct']:.1f} % | {where(r['squeeze_min_at'])} | "
                 f"{r['margin_to_15pct_um']:.0f} µm | {'**' if not r['ok_worst_tol'] else ''}{r['squeeze_min_worst_tol_pct']:.1f} %{'**' if not r['ok_worst_tol'] else ''} | "
                 f"{r['line_load_N_per_mm'][0]:.2f}–{r['line_load_N_per_mm'][1]:.2f} N/mm | "
                 f"{r['contact_mean_MPa'][0]:.1f}–{r['contact_mean_MPa'][1]:.1f} / {r['contact_peak_MPa'][0]:.1f}–{r['contact_peak_MPa'][1]:.1f} MPa | "
                 f"{lgt} | {r['latch_load_each_N']:.0f} N | {r['latch_sf']:.1f} | {r['hinge_load_each_N']:.0f} N |")
    names = list(cases[0]["profile"].keys()) if cases else []
    L += ["", "Squeeze (%) at points along the gland (the lower of the two sides):", "",
          "| Case | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for r in cases:
        L.append(f"| {r['case']} | " + " | ".join(f"{r['profile'][n]:.1f}" for n in names) + " |")
    mpa = lambda v: f"{v:.1f} MPa" if v > 0 else "–"                                  # noqa: E731
    L += ["", "| Case | von Mises, door | ears | brackets | bracket at the latch patch (model edge) | SF on yield (276 MPa) | Hinge pins' y travel |",
          "|---|---|---|---|---|---|---|"]
    for r in cases:
        v = r["vm"]
        sfp = f" ({r['sf_yield_at_patch']:.1f} at the patch)" if r.get("sf_yield_at_patch") else ""
        L.append(f"| {r['case']} | {mpa(v['door'][0])} | {mpa(v['ears'][0])} | {mpa(v['brackets'][0])} | {mpa(v['brackets_at_patch'][0])} | "
                 f"{r['sf_yield']:.1f}{sfp} | {r['hinge_y_travel_um'][0]:.0f} to {r['hinge_y_travel_um'][1]:.0f} µm (slot ±{1000 * SLOT:.0f}) |")
    its = [r for r in cases if r.get("iterations")]
    if its:
        L += ["", "Contact (cases D-F): the land is a set of penalty springs (" + f"{K_PEN:.0e}" + " N/mm per node) switched on where the door presses on the "
              "chamber and off where it would pull; " + "; ".join(f"{r['case']}: {len(r['iterations'])} solves, {r['iterations'][-1]['active']} nodes touching, "
                                                                  f"{r['iterations'][-1]['contact_N']:.0f} N through the land" for r in its) + "."]
    if R.get("clearances_mm"):
        L += ["", "Clearances, door shut (exact OpenCascade distances): " + "; ".join(f"{k.replace(' | ', ' to ')} {v:.2f} mm" for k, v in R["clearances_mm"].items() if v is not None) + "."]
    L += ["", "What it means:",
          "- **The round-5 latches pry the door open (cases D).** Each pulls on a line 12 mm outboard of its ear's tip, and the ear's tip is the "
          "outermost place the door bears on the chamber (the chamber's front face ends at x ±156). So the door pivots on the ear tips: "
          "the preload goes through the tips, and the door's middle lifts off its land and its cord. More preload, more lift.",
          "- **The fix drawn since 2026-11-25 (cases E): the hinge holds the door's bottom edge.** Round pin holes in place of the ±0.6 mm "
          "slots, and the chamber's knuckle blocks shimmed at assembly so the shut door's land just touches. Set each latch to about 0.75 kN, "
          "and no more: that is the cord's force at metal-to-metal plus +20 mbar, over two latches. The hinge pins need a close fit; "
          "the FEA takes the hinge as rigid.",
          "- Case C repeats the round-4/5 boundary conditions on the new geometry: they hold the ears' front faces, so they can't show a pull "
          "outboard of the bearing.",
          "", "Notes:",
          "- Squeeze is read at the groove floor's nodes: the case's reference squeeze (25 % for A-C, metal-to-metal for D-F) plus the door's "
          "displacement toward the chamber over the cord's 1.78 mm. A-C hold the latch hooks (or the ears) where the squeeze would be 25 % with a "
          "rigid door; D-F apply the latch preload as a force and let the door find its place on the cord and the land.",
          "- Contact pressure: Hertz line contact of a cord on a flat (E* = E / 0.75), from the local line load. Rough at 20-30 % squeeze; the line load is the firmer number.",
          "- The latch is rigid from its base to its hook: the latch's own stretch, and how its preload changes with the +20 mbar increment, are not modelled.",
          "- The brackets' feet are bonded to the ears: their screws (not drawn in the model) carry the prying from the pull line's offset (mech.md §C)."]
    (OUT / "door_seal_fea.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
