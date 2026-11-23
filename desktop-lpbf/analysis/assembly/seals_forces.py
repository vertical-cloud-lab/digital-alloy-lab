"""Installing every O-ring of the M50 desktop LPBF by robot, and the forces of every press, push and screw against what a
UR12e and its tools can give (issue #260, PR #266). Writes analysis/out/assembly/seals.json, forces.json and seals_forces.md.

Seals (every gland lpbf_low.GLANDS registers, plus the lid cord):
  installed stretch      ring ID against the groove's inner wall (face glands, vacuum pushes the ring inward), the groove
                         root (external radial groove) or the rod (internal rod groove); Parker ORD 5700 §3.3: <= 5 %
  install stretch        the most the ring is stretched while going in (mandrel, internal two-point grip, fold), against
                         Parker's 25-50 % ceiling; folding a ring through a throat is bending strain, (CS/2)/(r_fold + CS/2)
  moulded vs cord        for the lid's 300 x 210 mm rounded rectangle: the AS568 2-2xx whose ID circumference matches the
                         inner wall, and the bending strain at the groove's corners against Parker §4.3 (corner radius >= 3 x CS)
  lead-in chamfers       Trelleborg's Table 16 lengths (Parker gives only "15-20 deg, X > Y")
  dovetail insertion     the cord squeezed through the half-dovetail's face opening, Lindley's relation with Gent's modulus
  friction               Parker §5.11.2: F = fc x L (fc read from Fig. 5-9, 70A and 80A lines, interpolated to 75A), break-out 3x
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parents[1] / "cad"
sys.path.insert(0, str(CAD))
sys.path.insert(0, str(HERE.parent / "seals"))
OUT = HERE.parent / "out" / "assembly"

IN = 25.4
LBF = 4.44822
# Parker Fig. 5-9 (fc, lb per inch of seal contact, vs % compression; read from the chart, 2026-11-20 22:18 UTC)
FC = {70: [(10, 0.7), (15, 1.0), (20, 1.33), (25, 1.65)], 80: [(10, 1.2), (15, 1.8), (20, 2.4), (25, 3.05)]}
# Trelleborg Table 16, lead-in chamfer length Z min (mm) at 15 deg / 20 deg, by cross-section
CHAMFER = {1.78: (2.5, 1.5), 2.62: (3.0, 2.0), 3.53: (3.5, 2.5)}
# UR12e and tools (datasheets read 2026-11-20; assembly-tooling.csv)
UR = dict(ft_range_N=100.0, ft_acc_N=5.5, payload=12.5, force_limit_N=(50.0, 250.0))
SD = dict(torque=(0.15, 5.0), axial_stop_N=40.0)
NR = dict(torque=(1.5, 10.0))
AS568_2XX = {"2-276": 278.99, "2-277": 291.69, "2-278": 304.39, "2-279": 329.79}      # ID mm, CS 3.53 (Parker Table 9-1)


def gent_E(shore=75.0):
    return 0.0981 * (56 + 7.62336 * shore) / (0.137505 * (254 - 2.54 * shore))


def lindley(cs, e, shore=75.0):
    return cs * gent_E(shore) * (1.25 * e ** 1.5 + 50 * e ** 6)


def fc_75(squeeze_pct):
    def interp(t):
        xs, ys = [a for a, _ in t], [b for _, b in t]
        if squeeze_pct <= xs[0]:
            return ys[0] * squeeze_pct / xs[0]
        for (x0, y0), (x1, y1) in zip(t[:-1], t[1:]):
            if squeeze_pct <= x1:
                return y0 + (y1 - y0) * (squeeze_pct - x0) / (x1 - x0)
        return ys[-1] + (ys[-1] - ys[-2]) * (squeeze_pct - xs[-1]) / (xs[-1] - xs[-2])
    return 0.5 * (interp(FC[70]) + interp(FC[80]))


def main():
    import lpbf_low as M
    import module_params as MP
    M.build(module="M50", reservoir="M")
    G = {k: dict(v) for k, v in M.GLANDS.items()}
    P = M.P
    rows = []
    for k, g in G.items():
        ring = g.get("ring")
        cs = float(g["cs"])
        rid = MP.AS568[ring][0] if ring in MP.AS568 else None
        n = int(g.get("n", 1))
        r = dict(gland=k, ring=ring, n=n, cs=cs, ring_id=rid, kind=g["kind"], closure=g.get("closure"), dovetail=bool(g.get("dovetail")))
        if g["kind"] == "face":
            if "groove_id" in g and rid:
                r["installed_stretch_pct"] = round(100 * (g["groove_id"] / rid - 1), 1)
                r["install_stretch_pct"] = round(100 * ((g["groove_id"] + 1.0) / rid - 1), 1)
            elif "inner_perimeter" in g and rid:
                r["installed_stretch_pct"] = round(100 * (g["inner_perimeter"] / (math.pi * rid) - 1), 1)
                r["install_stretch_pct"] = round(100 * ((g["inner_perimeter"] + math.pi) / (math.pi * rid) - 1), 1)
            r["method"] = ("cord: vulcanized ring rolled into the half-dovetail (roller_n), arm B tensioning the free loop"
                           if ring == "cord" else
                           ("2F-85 pin caps open inside the ring (2-point internal grip), lay it on the groove, roller_n presses it under "
                            "the dovetail lip" if g.get("dovetail") else
                            "2F-85 pin caps open inside the ring, lay it in the groove; PFPE film if the groove faces down when closed"))
            r["chamfer_needed"] = "none (axial face seal)"
        elif g["kind"] == "radial":
            r["installed_stretch_pct"] = round(100 * (g["groove_d"] / rid - 1), 1)
            mand = 96.7
            r["install_stretch_pct"] = round(100 * (mand / rid - 1), 1)
            sq = 100 * (cs - (MP.PORT_D - g["groove_d"]) / 2) / cs
            fc = fc_75(sq)
            Lp = math.pi * MP.PORT_D / IN
            r.update(squeeze_pct=round(sq, 1), fc_lb_in=round(fc, 2), running_N=round(fc * Lp * LBF, 0), breakout_N=round(3 * fc * Lp * LBF, 0),
                     method="stretched over the acetal spigot mandrel (cone + 0.45 mm sleeve) and pushed off into the groove by the pusher",
                     chamfer_needed=("floor port's lower edge: 20 deg x 2.5 mm, now in the model (FP-04), = Trelleborg's minimum for 3.53 mm"
                                     if "lead-in chamfer on its lower edge" in (CAD / "lpbf_low.py").read_text() else
                                     f"floor port's lower edge: >= {CHAMFER[3.53][0]} mm at 15 deg or {CHAMFER[3.53][1]} mm at 20 deg")
                                    + "; the spigot's top edge is covered by the mandrel's sleeve")
        elif g["kind"] == "rod":
            ring_od = rid + 2 * cs
            r["installed_stretch_pct"] = round(100 * (g["rod_d"] / rid - 1), 1)
            r["ring_od_vs_groove_pct"] = round(100 * (g["groove_d"] / ring_od - 1), 1)
            sq = 100 * (cs - g["depth"]) / cs
            fc = fc_75(sq)
            Lr = math.pi * g["rod_d"] / IN
            # folding a 2-114 through the Ø15.93 throat inside a Ø12.4 loader tube: kidney fold, fold radius ~2.5 mm
            r_fold = 2.5
            r.update(squeeze_pct=round(sq, 1), fc_lb_in=round(fc, 2), running_N=round(n * fc * Lr * LBF, 0), breakout_N=round(3 * n * fc * Lr * LBF, 0),
                     fold_strain_pct=round(100 * (cs / 2) / (r_fold + cs / 2), 0),
                     method="folded into the slotted loader tube (kidney fold), pushed through the Ø15.93 throat and released into "
                            "the groove, the deeper groove first; then the rod enters on the PEEK bullet",
                     chamfer_needed=f"rod end: the bullet's 15 deg nose (>= {CHAMFER[2.62][0]} mm at 15 deg); the throat's edges "
                                    "rounded R0.2-0.4 and polished")
        elif g["kind"] == "sae":
            r["method"] = "comes fitted on the transducer and relief valve; turned in with the part"
            r["chamfer_needed"] = "SAE J1926 port's 12 deg chamfer (part of the port standard)"
        rows.append(r)
    # the lid cord, and the moulded alternative: the gland's inner wall read from the model (lpbf_low.py: rbox(-ix - 3, ix + 3,
    # -iy - 3, iy + 3, ..., r) cut into the frame's top face; r read from the source so a change there flows through)
    import re as _re
    src = (CAD / "lpbf_low.py").read_text()
    mm = _re.search(r"lid_gland = rbox\(.*?, (\d+(?:\.\d+)?) \+ gw\)\.cut\(rbox\(-ix - (\d+(?:\.\d+)?), ix \+ \d+(?:\.\d+)?, -iy - \d+(?:\.\d+)?, iy \+ \d+(?:\.\d+)?, [^,]+, [^,]+, (\d+(?:\.\d+)?)\)\)", src)
    off, r_in = (float(mm.group(2)), float(mm.group(3))) if mm else (3.3, 4.3)
    lid_in_hw, lid_in_hy = P["ix"] + off, P["iy"] + off
    per_in = 2 * (2 * lid_in_hw + 2 * lid_in_hy) - (8 - 2 * math.pi) * r_in
    cands = {k: v for k, v in AS568_2XX.items() if 0.0 <= per_in / (math.pi * v) - 1 <= 0.05}
    best = min(cands.items(), key=lambda kv: abs(per_in / (math.pi * kv[1]) - 1.02)) if cands else \
        min(AS568_2XX.items(), key=lambda kv: abs(per_in / (math.pi * kv[1]) - 1.02))
    cs = 3.53
    rc = r_in + cs / 2
    lid = dict(gland="lid", ring="3.53 mm cord (vulcanized splice)", n=1, cs=cs, kind="face", closure="chamber lid (20 x M5)",
               inner_perimeter_mm=round(per_in, 1), centreline_mm=round(per_in + math.pi * P["gland_w"], 1),
               moulded_alternative=best[0], moulded_id=best[1],
               moulded_installed_stretch_pct=round(100 * (per_in / (math.pi * best[1]) - 1), 2),
               moulded_stretch_range_pct=[round(100 * (per_in / (math.pi * (best[1] + 1.65)) - 1), 2), round(100 * (per_in / (math.pi * (best[1] - 1.65)) - 1), 2)],
               corner_r_inner_mm=r_in, corner_r_parker_min_mm=round(3 * cs, 1), corner_bend_strain_pct=round(100 * (cs / 2) / rc, 0),
               corner_bend_strain_at_3cs_pct=round(100 * (cs / 2) / (3 * cs + cs / 2), 0), gland_from_model=bool(mm),
               method="cord laid in by arm B at the midpoints, ends, quarter points (Adebola et al. 2024), rolled home by arm A's 3.2 mm "
                      "PTFE wheel at 10-20 N; the splice at a straight run",
               chamfer_needed="none (axial face seal)")
    rows.insert(0, lid)
    # the floor cord (chamber-construction.md: frame + bolted floor plate), same treatment as the lid
    if "floor" in G and getattr(M, "FRAME", None):
        g = G["floor"]
        per_f = float(g["inner_perimeter"])
        r_f = M.FRAME["r_in"] + M.FRAME["gland_t"]
        bf = min(AS568_2XX.items(), key=lambda kv: abs(per_f / (math.pi * kv[1]) - 1.005))
        for r in rows:
            if r["gland"] == "floor":
                r.update(ring="3.53 mm cord (vulcanized splice)", inner_perimeter_mm=round(per_f, 1), moulded_alternative=bf[0], moulded_id=bf[1],
                         moulded_installed_stretch_pct=round(100 * (per_f / (math.pi * bf[1]) - 1), 2),
                         moulded_stretch_range_pct=[round(100 * (per_f / (math.pi * (bf[1] + 1.65)) - 1), 2),
                                                    round(100 * (per_f / (math.pi * (bf[1] - 1.65)) - 1), 2)],
                         corner_r_inner_mm=round(r_f, 1), corner_r_parker_min_mm=round(3 * cs, 1),
                         corner_bend_strain_pct=round(100 * (cs / 2) / (r_f + cs / 2), 0),
                         method="floor plate face up on Fixture P: cord laid in by arm B, rolled home by arm A's 3.2 mm wheel; nothing above "
                                "the plate yet, so the roller has the whole gland to itself",
                         chamfer_needed="none (axial face seal)")
    # dovetail insertion (door, drawer): cord through the face opening
    w_face = 2.3 - 1.32 * math.tan(math.radians(MP.DOVETAIL_DEG))
    for r in rows:
        if r.get("dovetail"):
            e_nom = max(0.0, (r["cs"] - w_face) / r["cs"])
            e_max = max(0.0, (r["cs"] + 0.076 - w_face) / (r["cs"] + 0.076))
            r.update(face_opening_mm=round(w_face, 2), lateral_squeeze_pct=[round(100 * e_nom, 1), round(100 * e_max, 1)],
                     insert_N_per_mm=[round(lindley(r["cs"], e_nom), 3), round(lindley(r["cs"] + 0.076, e_max), 3)],
                     roller_force_N=round(max(5.0, lindley(r["cs"] + 0.076, e_max) * 6.0 * 2.0), 1))
    seals = dict(rows=rows, lubricant=dict(name="Krytox LVP (PFPE grease)", vapour_pressure_torr_20C=1e-13, fkm="compatible (Chemours lists Viton A)",
                                           use="a film wiped on with a lint-free swab; holds face rings in grooves that face down when closed"),
                 verification=[
                     "D405 RGB at 70-120 mm before each closure: ring present, unbroken, in the groove all round, no twist mark "
                     "(about 0.1-0.15 mm per pixel at 100 mm, 87 deg x 58 deg); its depth (+-2 % at 50 cm, roughly +-1.4 % at 20 cm) is too "
                     "coarse to see a 0.5-0.9 mm proud cord, so seating is checked by force",
                     "force signature in UR force mode (F/T +-100 N range, +-5.5 N accuracy): the roller's 10-20 N press stays flat round the "
                     "groove (a dip is a gap, a spike an overlap); rod and spigot insertions follow a reference curve (double peak = pinched ring)",
                     "leak test after assembly: rate of rise from <= 1 mbar and O2 drift at +20 mbar argon (seals.md), plus a helium sniff of "
                     "each new joint if the rate of rise fails"])
    # ---------------------------------------------------------------- forces
    d_pin, L_eng, mu = 6.0, 10.0, 0.15
    delta = 0.008                                   # m6 dowel in an H7 hole: 0 to 0.012 mm interference, mid value
    p = delta / (d_pin * ((1 + 0.33) / 68.9e3 + (1 - 0.30) / 193e3))
    dowel_N = mu * p * math.pi * d_pin * L_eng
    spig = next(r for r in rows if r["gland"] == "spigot")
    rod = next(r for r in rows if r["gland"] == "rod_M50")
    forces = [
        dict(step="C02", what="Ø6 m6 dowel and diamond pin pressed 10 mm into the 6061 floor (H7)", need_N=round(dowel_N, 0),
             basis=f"Lame press fit, 0.008 mm diametral interference, mu {mu}: p = {p:.0f} MPa",
             robot="NO: 16x the F/T range; a UR pushing this hard is past its force limit. Arbor press by a person, or a slip fit (g6) "
                   "with retaining compound so the robot only inserts it"),
        dict(step="C10", what="spigot's 2-238 entering the Ø96 floor port", need_N=spig["running_N"], peak_N=spig["breakout_N"],
             basis=f"Parker 5.11.2: fc {spig['fc_lb_in']} lb/in at {spig['squeeze_pct']} % over pi x 96 mm; break-out 3x",
             robot="robot starts it on the lead-in chamfer (<= 50 N in force mode), the two captive M6 screws pull it home"),
        dict(step="M13", what="hollow rod, top end first, through the two 2-114 rod O-rings", need_N=rod["running_N"], peak_N=rod["breakout_N"],
             basis=f"Parker 5.11.2: fc {rod['fc_lb_in']} lb/in at {rod['squeeze_pct']} % over pi x 15.875 mm, two rings",
             robot="yes in force mode with a PFPE film (lubricated, about half); dry break-out is at the F/T range"),
        dict(step="M26", what="build plate into the honed bore (0.15 mm radial clearance) and onto the bayonet", need_N=10.0,
             basis="sliding fit; 10 N contact for a spiral search", robot="yes: force-guided spiral search; positioning alone (AprilTag + D405, "
                                                                          "about +-0.4 mm) is coarser than the clearance"),
        dict(step="F39", what="drawer against its 2-033 (358 N to squeeze, seals.md)", need_N=50.0, peak_N=358.0,
             basis="the two quarter-turn latches pull it the last 0.4 mm", robot="robot pushes to first contact only"),
        dict(step="F46", what="reservoir onto the dock O-ring along its 2 deg ramps (seals.md)", need_N=94.0,
             basis="seals.md: 94 N push home, 58 N pull-out", robot="yes, but at the F/T range's edge (100 N): set the push to 94 N +- 5.5 N"),
        dict(step="F51", what="door draw latches, 725 N preload each (seals.md)", need_N=725.0,
             basis="1807A61 over-centre latches", robot="NO: a person closes them (or pneumatic clamps, seals.md (b))"),
        dict(step="screws", what="M3 / M4 / M5 / M6 A2-70 in A2 inserts, mu 0.14 (MoS2 paste)", need_N=None,
             torque_Nm={"M3": 1.1, "M4": 2.2, "M5": 4.2, "M6": 7.4},
             basis="Pfeiffer Vacuum's A2-70 table (90 % of Rp0.2): M4 2.2, M5 4.2, M6 7.4 N m at mu 0.14; M3 from TR Fastenings",
             robot="OnRobot Screwdriver 0.15-5 N m covers M3-M5; M6 needs the inline nutrunner (1.5-10 N m)"),
        dict(step="M02/C01", what="helical inserts (M3-M6)", need_N=None, torque_Nm={"insert": "0.45-3 (Bollhoff's powered tools)"},
             basis="Bollhoff HELICOIL power tools E-S 206 (0.45-0.95 N m), E-PSG (0.9-3 N m)", robot="machine shop, with the tang broken off"),
    ]
    tip = []
    from run_assembly import tipover  # noqa: E402
    for what, kg, F, reach, h in (("chamber assembly, two arms (15.5 kg / 2)", 7.75, 0.0, 900.0, 1000.0),
                                  ("optics bridge, two arms (13.3 kg / 2)", 6.65, 0.0, 1000.0, 1300.0),
                                  ("chamber body on the vacuum gripper (7.3 kg + 0.8 kg)", 8.1, 0.0, 700.0, 900.0),
                                  ("12.5 kg at 1300 mm (rated payload at full reach)", 12.5, 0.0, 1300.0, 900.0),
                                  ("reservoir push home 94 N, sideways at 1.25 m", 0.5, 94.0, 800.0, 1250.0),
                                  ("dowel press 1.6 kN (if a robot tried)", 0.0, dowel_N, 600.0, 1000.0)):
        tip.append(dict(case=what, payload_kg=kg, push_N=round(F, 0), margin=tipover(kg, F, reach, h)))
    out = dict(seals=seals, forces=forces, tipover=tip, sources=dict(
        parker="Parker O-Ring Handbook ORD 5700, https://nfc.arizona.edu/sites/default/files/2022-02/parker_o-ring_handbook.pdf, read 2026-11-20 22:18 UTC: "
               "Sec. 3.3 (stretch), 4.3 (non-circular grooves, corner radius >= 3x CS), 5.11 (friction, Fig. 5-9), Design Charts 4-3..4-5, Table 9-1",
        trelleborg="Trelleborg O-ring catalogue Table 16 (lead-in chamfers), read 2026-11-20 22:41 UTC",
        pfeiffer="Pfeiffer Vacuum knowledge base, A2-70 tightening torques, read 2026-11-20 22:35 UTC",
        krytox="Chemours Krytox LVP data sheet, read 2026-11-20 22:36 UTC",
        adebola="Adebola et al. (2024), Automating deformable gasket assembly, IEEE CASE, doi:10.48550/arxiv.2408.12593 (via Edison r3)"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "seals_forces.json").write_text(json.dumps(out, indent=1, default=str))
    return out


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    o = main()
    print(json.dumps(o["seals"]["rows"][:3], indent=1, default=str)[:3000])
    print(json.dumps(o["tipover"], indent=1))
