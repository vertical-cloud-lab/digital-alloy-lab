"""Structural FEA (CalculiX, axisymmetric CAX6) of option B's welded vessel and option C's glass, with the
temperature fields from thermal.py, plus the closed-form checks in handcalcs.py.

    python analysis/structural.py          # needs analysis/out/thermal/<case>/pass2.frd from thermal.py

B vessel (the whole 316L weldment: KF stub flange, reducer, body, 8 mm floor), held axially on the
flange's back taper where the clamp bears. Load cases:
  B_pressure   +1.2 bar gauge inside (1.5 x the chamber's relief setting), 25 C
  B_vacuum     full vacuum: 1.0 bar outside, 25 C (Provo's room is ~0.86 bar, so this is ~16 % high)
  B_hot_<t>    the B_816 temperature field at t = 10 ... 3600 s, plus the run pressure (+0.15 bar)
Glass (C): the tube alone, standing on its bottom gasket, 3 MPa of tie-rod clamping on its top end, with
the C_400 (fused quartz) and C_400_boro (borosilicate) temperature fields at each saved time.

Output: analysis/out/structural/<case>/ and analysis/out/structural_summary.{json,md}; field plots in
analysis/img/.
"""

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.tri as mtri  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cad"))
import axifea as F  # noqa: E402
import params as P  # noqa: E402
import thermal as TH  # noqa: E402

OUT = HERE / "out" / "structural"
IMG = HERE / "img"
OUT.mkdir(parents=True, exist_ok=True)

# 316L: E (GPa), mean expansion from 20 C (1e-6/K), and minimum yield (MPa), ASME II-D style values
T_TAB = [20, 100, 200, 300, 400, 500, 600, 700, 800]
E_316 = [193, 187, 180, 173, 166, 159, 152, 145, 138]
A_316 = [15.9, 16.0, 16.5, 17.0, 17.5, 17.8, 18.1, 18.4, 18.7]
SY_316L = [172, 145, 121, 108, 99, 93, 88, 84, 80]
GLASS = {  # E MPa, nu, alpha 1/K, design tensile MPa (long-term), short-term fracture MPa
    "QUARTZ": dict(E=72000, nu=0.17, alpha=0.55e-6, design=7.0, short=50.0),
    "BORO": dict(E=64000, nu=0.20, alpha=3.3e-6, design=6.0, short=40.0),
}


def temp_interpolator(case, region_names):
    """Linear interpolator of the thermal result (CAX3 mesh of thermal.py) over the given regions."""
    spec = TH.CASES[case]
    regs, cavity, probes, info = TH.DESIGNS[spec[0]](spec[1], **spec[2])
    for r in regs:
        r.size *= TH.MESH_SCALE
    m = F.build_mesh(regs, order=1)
    frd = [(t, v) for t, v in F.read_frd(TH.OUT / case / "pass2.frd")
           if t is not None and min(abs(t - ft) for ft in TH.FIELD_TIMES) < 1e-3]
    els = [e for e in m.elems if m.elem_region[e] in region_names]
    used = sorted({n for e in els for n in m.elems[e]})
    idx = {n: i for i, n in enumerate(used)}
    xy = np.array([m.nodes[n] for n in used])
    tri = mtri.Triangulation(xy[:, 0], xy[:, 1], np.array([[idx[n] for n in m.elems[e]] for e in els]))
    fields = []
    for t, vals in frd:
        if len(vals) != len(m.nodes):
            raise RuntimeError(f"{case}: thermal mesh rebuilt with {len(m.nodes)} nodes, frd has {len(vals)}")
        T = np.array([vals[n][0] for n in used])
        fields.append((t, mtri.LinearTriInterpolator(tri, T)))
    return fields


def nearest_fill(interp, pts):
    v = np.asarray(interp(pts[:, 0], pts[:, 1]).filled(np.nan))
    bad = np.isnan(v)
    if bad.any():   # points a hair outside the thermal triangulation: nudge inward
        for k in np.where(bad)[0]:
            for d in (0.05, 0.1, 0.2, 0.4):
                for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                    vv = interp(pts[k, 0] + dx, pts[k, 1] + dy)
                    if not np.ma.is_masked(vv):
                        v[k] = float(vv)
                        break
                if not np.isnan(v[k]):
                    break
    return v


def mises_principal(s):
    """s: (n, 6) [rr, zz, tt, rz, rt, zt] -> von Mises and max principal."""
    rr, zz, tt, rz = s[:, 0], s[:, 1], s[:, 2], s[:, 3]
    vm = np.sqrt(0.5 * ((rr - zz) ** 2 + (zz - tt) ** 2 + (tt - rr) ** 2) + 3 * rz ** 2)
    c = (rr + zz) / 2
    rad = np.sqrt(((rr - zz) / 2) ** 2 + rz ** 2)
    p1 = np.maximum(np.maximum(c + rad, c - rad), tt)
    return vm, p1


def run_static(name, m, mat_cards, sections, bc_lines, load_lines, temps=None, elset_out="E_ALL"):
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "static.inp", "w") as f:
        f.write("*HEADING\nstructural\n")
        F.write_mesh(f, m)
        F.write_set(f, "ELSET", "E_ALL", sorted(m.elems))
        f.write(bc_lines["sets"])
        f.write(mat_cards)
        f.write(sections)
        f.write(f"*INITIAL CONDITIONS, TYPE=TEMPERATURE\nNALL, 25.\n")
        f.write("*STEP\n*STATIC\n")
        f.write(bc_lines["bc"])
        f.write(load_lines)
        f.write("*TEMPERATURE\n")
        if temps is None:
            f.write("NALL, 25.\n")
        else:
            for n, T in temps.items():
                f.write(f"{n}, {T:.2f}\n")
        f.write(f"*EL PRINT, ELSET={elset_out}\nS\n*NODE PRINT, NSET=NALL\nU\n*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    F.run_ccx("static", d, threads=1)
    blocks = F.read_dat_blocks(d / "static.dat")
    key = next(k for k in blocks if k[0].startswith("stresses"))
    t, vals = blocks[key][-1]
    # .dat stress lines: elem  ip  s11 s22 s33 s12 s13 s23 -> parsed as {elem: [ip, s...]} (last ip wins);
    # re-read all integration points directly
    rows = []
    txt = (d / "static.dat").read_text().splitlines()
    on = False
    for ln in txt:
        if ln.strip().startswith("stresses"):
            on = True
            continue
        if on:
            p = ln.split()
            if len(p) == 8:
                try:
                    rows.append([float(x) for x in p])
                except ValueError:
                    on = False
            elif p and not p[0].lstrip("-").replace(".", "").isdigit():
                on = False
    rows = np.array(rows)
    ukey = next(k for k in blocks if k[0].startswith("displacements"))
    _, uvals = blocks[ukey][-1]
    return rows, uvals


def b_vessel_mesh():
    import parts as PT
    prof, z = PT.option_b_vessel_profile()
    m = F.build_mesh([F.Region("vessel", "S316L", prof, 0.8)], order=2)
    return m, z


def steel_cards():
    s = "*MATERIAL, NAME=S316L\n*ELASTIC\n"
    s += "".join(f"{e * 1000:.0f}, 0.3, {t}\n" for e, t in zip(E_316, T_TAB))
    s += "*EXPANSION, ZERO=20.\n" + "".join(f"{a * 1e-6:.4e}, {t}\n" for a, t in zip(A_316, T_TAB))
    s += "*DENSITY\n7.95e-9\n"
    return s


def b_cases():
    kf = P.JOINT
    m, z = b_vessel_mesh()
    # clamp bearing: the flange's back taper (between the rim corner and the hub), outer boundary edges
    rf, rh = kf.flange_od / 2, kf.hub_od / 2
    g = kf.ring_thk / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    z_lo, z_hi = -g - kf.lip, -g - t_edge
    taper_nodes = sorted({n for e in m.edges for n in e["n"]
                          if rh - 0.01 <= e["mid"][0] <= rf - 0.5 and z_lo - 0.01 <= e["mid"][1] <= z_hi + 0.01
                          and e["normal"][1] < -0.1})
    # inside (cavity) faces: boundary edges whose outward normal points into the bore or up from the floor
    cav = TH.Polygon([(0, z["z_bot"] + 0.01), (z["R_i"] + 0.3, z["z_bot"] + 0.01), (z["R_i"] + 0.3, z["z_red"] + 8),
                      (kf.bore / 2 + 0.3, z["z_stub"] - 8), (kf.bore / 2 + 0.3, 5), (0, 5)])
    inside = [e for e in m.edges if e["mid"][0] > 1e-6 and cav.contains(TH.Point(*(e["mid"] - 0.2 * e["normal"])))
              and not cav.contains(TH.Point(*(e["mid"] + 0.2 * e["normal"]))) is False]
    inside = [e for e in m.edges if e["mid"][0] > 1e-6 and cav.contains(TH.Point(*(e["mid"] + 0.3 * e["normal"])))]
    outside = [e for e in m.edges if e["mid"][0] > 1e-6 and e not in inside and abs(e["mid"][1] - (-g)) > 1e-6]
    sets = ""
    import io
    buf = io.StringIO()
    F.write_set(buf, "NSET", "TAPER", taper_nodes)
    sets = buf.getvalue()
    bc = "*BOUNDARY\nTAPER, 2, 2, 0.\n"
    cards = steel_cards()
    sec = "*SOLID SECTION, ELSET=E_vessel, MATERIAL=S316L\n"

    def pressure(edges, p):
        return "*DLOAD\n" + "".join(f"{e['elem']}, P{e['face']}, {p}\n" for e in edges)

    res = {}
    for name, loads, temps in (("B_pressure", pressure(inside, 0.12), None),
                               ("B_vacuum", pressure(outside, 0.10), None)):
        rows, u = run_static(name, m, cards, sec, {"sets": sets, "bc": bc}, loads, temps)
        vm, p1 = mises_principal(rows[:, 2:8])
        umax = max(math.hypot(v[0], v[1]) for v in u.values())
        res[name] = dict(vm_max=round(float(vm.max()), 2), u_max_mm=round(umax, 4))
    # hot cases: the B_816 field at each saved time, plus the run pressure
    fields = temp_interpolator("B_816", ["vessel"])
    pts = np.array([m.nodes[n] for n in sorted(m.nodes)])
    allowable = []
    for t, interp in fields:
        T = nearest_fill(interp, pts)
        temps = {n: float(T[k]) for k, n in enumerate(sorted(m.nodes))}
        name = f"B_hot_{int(t)}s"
        rows, u = run_static(name, m, cards, sec, {"sets": sets, "bc": bc}, pressure(inside, 0.015), temps)
        vm, p1 = mises_principal(rows[:, 2:8])
        k = int(np.argmax(vm))
        e_max = int(rows[k, 0])
        # temperature at that element (mean of its corner nodes) and the yield there
        Te = float(np.mean([temps[n] for n in m.elems[e_max][:3]]))
        sy = float(np.interp(Te, T_TAB, SY_316L))
        cen = np.mean([m.nodes[n] for n in m.elems[e_max][:3]], axis=0)
        umax = max(math.hypot(v[0], v[1]) for v in u.values())
        res[name] = dict(t_s=t, vm_max=round(float(vm.max()), 1), at_rz=[round(float(cen[0]), 1), round(float(cen[1]), 1)],
                         T_there=round(Te, 0), Sy_there=round(sy, 0), vm_over_Sy=round(float(vm.max()) / sy, 2),
                         T_max=round(float(T.max()), 0), u_max_mm=round(umax, 3))
        allowable.append((t, vm, rows, temps))
    # plot the worst hot case
    worst = max((k for k in res if k.startswith("B_hot")), key=lambda k: res[k]["vm_max"])
    plot_vm(m, OUT / worst / "static.dat", worst, res[worst])
    return res


def read_stresses(dat):
    """Integration-point stresses from a .dat file: rows [elem, ip, s11, s22, s33, s12, s13, s23]."""
    rows = []
    on = False
    for ln in Path(dat).read_text().splitlines():
        if ln.strip().startswith("stresses"):
            on = True
            continue
        if on:
            p = ln.split()
            if not p:
                continue
            try:
                vals = [float(x) for x in p]
            except ValueError:
                on = False
                continue
            if len(vals) == 8:
                rows.append(vals)
    return np.array(rows)


def plot_vm(m, dat, name, r):
    rows = read_stresses(dat)
    vm, _ = mises_principal(rows[:, 2:8])
    per_el = {}
    for (e, ip), v in zip(rows[:, :2].astype(int), vm):
        per_el.setdefault(e, []).append(v)
    fig, ax = plt.subplots(figsize=(4.5, 8))
    from matplotlib.collections import PolyCollection
    polys, vals = [], []
    for e, ns in m.elems.items():
        polys.append([m.nodes[n] for n in ns[:3]])
        vals.append(np.mean(per_el.get(e, [0])))
    pc = PolyCollection(polys, array=np.array(vals), cmap="viridis", edgecolors="none")
    ax.add_collection(pc)
    ax.autoscale()
    ax.set_aspect("equal")
    fig.colorbar(pc, ax=ax, label="von Mises (MPa)", shrink=0.7)
    ax.set_title(f"{name}: max {r['vm_max']} MPa at r,z = {r['at_rz']}\n"
                 f"(T there {r['T_there']} C, 316L yield {r['Sy_there']} MPa)", fontsize=8)
    ax.set_xlabel("r (mm)")
    ax.set_ylabel("z (mm)")
    fig.savefig(IMG / f"structural_{name}.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


def glass_cases():
    s = P.STOCK
    ro, ri = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]
    out = {}
    for case, gname in (("C_400", "QUARTZ"), ("C_400_boro", "BORO"), ("C_816", "QUARTZ")):
        if not (TH.OUT / case / "pass2.frd").exists():
            continue
        spec = TH.CASES[case]
        regs, cav, probes, info = TH.DESIGNS["C"](spec[1], **spec[2])
        glass = next(r for r in regs if r.name == "glass")
        zb, zt = min(p[1] for p in glass.poly), max(p[1] for p in glass.poly)
        m = F.build_mesh([F.Region("glass", gname, F_rect(ri, ro, zb, zt), 0.6)], order=2)
        g = GLASS[gname]
        cards = (f"*MATERIAL, NAME={gname}\n*ELASTIC\n{g['E']}, {g['nu']}\n*EXPANSION, ZERO=20.\n{g['alpha']:.3e}\n"
                 f"*DENSITY\n2.2e-9\n")
        sec = f"*SOLID SECTION, ELSET=E_glass, MATERIAL={gname}\n"
        bottom = sorted({n for e in m.edges for n in e["n"] if abs(e["mid"][1] - zb) < 1e-6})
        top_edges = [e for e in m.edges if abs(e["mid"][1] - zt) < 1e-6]
        import io
        buf = io.StringIO()
        F.write_set(buf, "NSET", "BOT", bottom)
        bc = "*BOUNDARY\nBOT, 2, 2, 0.\n"
        loads = "*DLOAD\n" + "".join(f"{e['elem']}, P{e['face']}, 3.0\n" for e in top_edges)
        fields = temp_interpolator(case, ["glass"])
        pts = np.array([m.nodes[n] for n in sorted(m.nodes)])
        worst = None
        series = []
        for t, interp in fields:
            T = nearest_fill(interp, pts)
            temps = {n: float(T[k]) for k, n in enumerate(sorted(m.nodes))}
            rows, u = run_static(f"{case}_glass_{int(t)}s", m, cards, sec, {"sets": buf.getvalue(), "bc": bc}, loads, temps)
            vm, p1 = mises_principal(rows[:, 2:8])
            series.append(dict(t_s=t, p1_max=round(float(p1.max()), 2), T_max=round(float(T.max()), 0),
                               T_min=round(float(T.min()), 0)))
            if worst is None or p1.max() > worst[1]:
                worst = (t, float(p1.max()))
        out[case] = dict(glass=gname, series=series, p1_max=round(worst[1], 2), t_worst_s=worst[0],
                         design_tensile=g["design"], short_term=g["short"],
                         ratio_design=round(worst[1] / g["design"], 2))
    return out


def F_rect(r0, r1, z0, z1):
    return [(r0, z0), (r1, z0), (r1, z1), (r0, z1)]


def main(argv):
    path = HERE / "out" / "structural_summary.json"
    res = json.loads(path.read_text()) if path.exists() else {"B": {}, "glass": {}}
    what = argv or ["B", "glass"]
    if "B" in what:
        res["B"] = b_cases()
    if "glass" in what:
        res["glass"] = glass_cases()
    path.write_text(json.dumps(res, indent=1) + "\n")
    L = ["# Structural FEA summary (CalculiX, axisymmetric CAX6)\n",
         "## Option B vessel (316L weldment)\n", "| Case | max von Mises (MPa) | where (r, z mm) | T there (C) | "
         "316L yield there (MPa) | ratio | max displacement (mm) |", "|---|---:|---|---:|---:|---:|---:|"]
    for k, v in res["B"].items():
        L.append(f"| {k} | {v['vm_max']} | {v.get('at_rz', '')} | {v.get('T_there', 25)} | "
                 f"{v.get('Sy_there', SY_316L[0])} | {v.get('vm_over_Sy', round(v['vm_max'] / SY_316L[0], 3))} | "
                 f"{v['u_max_mm']} |")
    L += ["\n## Glass tube (option C), thermal stress from the hot pile\n",
          "| Case | Glass | worst max principal (MPa) | at t (s) | long-term design tensile (MPa) | "
          "short-term fracture (MPa) |", "|---|---|---:|---:|---:|---:|"]
    for k, v in res["glass"].items():
        L.append(f"| {k} | {v['glass']} | {v['p1_max']} | {v['t_worst_s']:.0f} | {v['design_tensile']} | {v['short_term']} |")
    (HERE / "out" / "structural_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1:])
