"""Checks on the fast-track model (ft_model.py), state by state.

1. Interference: every pair of parts whose bounding boxes overlap is intersected with OpenCascade's exact boolean;
   shared volume above VOL_TOL is a clash unless the pair is a designed contact (JOINTS, reported separately).
2. Beam: the scanned-beam envelope (the Ø40 field from the f-theta lens) against every part, with the clearance to
   the nearest ones.
3. Travel: the hopper-blade swept over the recoater's travel, and the plate over the piston's, against the static
   parts; the travel the hopper actually needs; the gaps at the ends of the piston stroke.
4. Fit: the deck cassette in the box and through the cube's face opening; both recoater stages in the cube; the rod
   lengths; the window's height above the bed and the irradiance on it.
5. Gas: the enclosure's gas volume measured from the model, and what it means for a flow purge (box) and a
   pump-purge (cube); the enclosure's air temperature rise.

Run:  python desktop-lpbf/fast-track/cad/ft_checks.py     # writes out/checks.json and out/checks.md
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys
import time

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402

OUT = HERE / "out"
VOL_TOL = 0.5      # mm3
GAP_WARN = 2.0     # mm
P = M.P

JOINTS = [
    ("Gantry uprights", "Gantry cross-beam", "T-slot joint"),
    ("Gantry uprights", "T-slot base", "uprights stand on the support rail"),
    ("Process fibre", "IPG YLR", "fibre leaves the laser's front panel"),
    ("Process fibre", "Collimator", "fibre connector in the collimator"),
    ("Argon feed tube", "Slot nozzle", "tube fitting in the nozzle's feed boss"),
    ("Argon feed tube", "box, 16 x 12", "bulkhead fitting through the box wall"),
    ("Exhaust hose", "box, 16 x 12", "bulkhead fitting through the box wall"),
    ("Exhaust hose", "Exhaust collector", "hose on the collector's outlet"),
    ("Vibration motor", "Carriage bracket and arm", "motor clamped on the arm"),
    ("Plate heaters", "Heater plate", "heaters in their holes"),
    ("Well-block heaters", "Well block", "heaters in their holes"),
    ("Fibreglass rope wiper", "Heater plate", "rope in its groove"),
    ("Fibreglass rope wiper", "Well block", "rope compressed against the bore: the wiper"),
    ("Piston rod", "Heater plate", "rod in its socket"),
    ("Piston rod", "Rod clamp", "rod in the clamp"),
    ("Piston rod", "FT-0 rod collar", "rod in the collar"),
    ("Dump water lines", "Water-cooled beam dump", "hose on the dump"),
    ("Dump water lines", "box, 16 x 12", "lines through a cable gland"),
    ("KF-25 pump hose", "KF-25 ports", "hose on the pump port"),
    ("KF-25 pump hose", "Rotary-vane pump", "hose on the pump inlet"),
    ("Argon feed tube", "Cube left plate", "bulkhead fitting"),
    ("Exhaust hose", "Cube right plate", "bulkhead fitting"),
]


def joint(a, b):
    for x, y, why in JOINTS:
        if (x in a and y in b) or (x in b and y in a):
            return why
    return None


def bb_overlap(a, b, pad=0.0):
    return not (a.xmax + pad < b.xmin or b.xmax + pad < a.xmin or a.ymax + pad < b.ymin or b.ymax + pad < a.ymin
                or a.zmax + pad < b.zmin or b.zmax + pad < a.zmin)


def common_volume(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:          # noqa: BLE001  (an OCC failure is reported, not hidden)
        return float("nan")


def interference(parts):
    clashes, contacts = [], []
    bbs = [p.shape.BoundingBox() for p in parts]
    for i, j in itertools.combinations(range(len(parts)), 2):
        if not bb_overlap(bbs[i], bbs[j]):
            continue
        a, b = parts[i], parts[j]
        v = common_volume(a.shape, b.shape)
        if not (v > VOL_TOL or v != v):
            continue
        why = joint(a.name, b.name)
        row = dict(a=a.name, b=b.name, volume_mm3=round(v, 1) if v == v else "OCC failed")
        if why:
            contacts.append({**row, "why": why})
        else:
            clashes.append(row)
    return clashes, contacts


def beam_check(state, parts):
    cone = M.beam_cone(state, 0.0, P["lens_wd"])
    cbb = cone.BoundingBox()
    allowed = ("Window, ", "Cover slide", "f-theta lens")
    hits, near = [], []
    for p in parts:
        bb = p.shape.BoundingBox()
        if not bb_overlap(cbb, bb, pad=25.0):
            continue
        v = common_volume(cone, p.shape)
        if v > VOL_TOL and not any(k in p.name for k in allowed):
            hits.append(dict(part=p.name, volume_mm3=round(v, 1)))
        elif not any(k in p.name for k in allowed):
            try:
                d = cone.distance(p.shape)
            except Exception:  # noqa: BLE001
                d = float("nan")
            near.append(dict(part=p.name, clearance_mm=round(d, 2)))
    near.sort(key=lambda r: r["clearance_mm"])
    return hits, near


def recoater_sweep(state, n=13):
    """Move the hopper over its full travel; record clashes and the smallest gap to each static part."""
    half = P["rc_travel"] / 2
    statics = [p for p in M.build(state, hx=0.0) if p.group != "recoater"]
    gaps, clashes = {}, []
    sbbs = [s.shape.BoundingBox() for s in statics]
    for k in range(n):
        hx = -half + 2 * half * k / (n - 1)
        movers = [p for p in M.build(state, hx=hx) if p.group == "recoater"]
        for m_ in movers:
            mbb = m_.shape.BoundingBox()
            for s, sbb in zip(statics, sbbs):
                if not bb_overlap(mbb, sbb, pad=15.0):
                    continue
                if "Well block" in s.name and "cord" in m_.name:
                    continue       # the cord rides on the block top by design
                if "X-LSQ075B" in s.name and "carriage" in m_.name:
                    continue       # the carriage rides on the stage
                if "Substrate" in s.name and "cord" in m_.name:
                    continue       # the cord spreads over the substrate by design
                if "Stage shield" in s.name and "bracket" in m_.name:
                    pass
                v = common_volume(m_.shape, s.shape)
                if v > VOL_TOL:
                    clashes.append(dict(hx=round(hx, 1), mover=m_.name, part=s.name, volume_mm3=round(v, 1)))
                    continue
                d = m_.shape.distance(s.shape)
                key = (m_.name, s.name)
                if key not in gaps or d < gaps[key][0]:
                    gaps[key] = (d, hx)
    rows = [dict(mover=a, part=b, min_gap_mm=round(d, 2), at_hx=round(x, 1)) for (a, b), (d, x) in gaps.items()]
    rows.sort(key=lambda r: r["min_gap_mm"])
    return clashes, rows


def travel_needed():
    """Hopper centre positions at the two parks, from the beam envelope and the overflow slot (cassette frame)."""
    hl = P["hopper"][0]
    margin = 3.0
    z_top = P["hopper"][2] + 13.0                      # vibrator top above the bed
    r = M.beam_radius(z_top)
    # left park: hopper's +x face and the vibrator (radius 5 about hx) clear the beam
    left = -(r + margin + max(hl / 2, 5.0))
    # right park: the cord clamp's -x face clears the beam, and the cord has passed the overflow slot's near edge
    blade_x = lambda hx: hx - hl / 2 - 2.0             # noqa: E731  cord centre
    right = max(r + margin + hl / 2 + 4.0, P["ovf_x"][0] + 1.5 - blade_x(0.0))
    return dict(beam_r_at_hopper_top_mm=round(r, 2), left_park=round(left, 1), right_park=round(right, 1),
                travel_needed_mm=round(right - left, 1), X_LSQ075B_travel=75.0, X_LSQ150B_travel=150.0)


def piston_checks(state):
    L = M.levels(state)
    dz = L["dz"]
    res = {}
    for pz in (P["pz_bot"], P["pz_top"]):
        parts = M.build(state, pz=pz)
        by = {p.name: p for p in parts}
        movers = [p for p in parts if p.group == "piston"]
        statics = [p for p in parts if p.group != "piston"]
        clash = []
        for m_ in movers:
            mbb = m_.shape.BoundingBox()
            for s in statics:
                if not bb_overlap(mbb, s.shape.BoundingBox()):
                    continue
                if joint(m_.name, s.name):
                    continue
                v = common_volume(m_.shape, s.shape)
                if v > VOL_TOL:
                    clash.append(dict(mover=m_.name, part=s.name, volume_mm3=round(v, 1)))
        hp = by["Heater plate Ø39.8 x 28 (MK-04)"].shape.BoundingBox()
        deck = by["Deck plate (MK-01)"].shape.BoundingBox()
        clamp = by["Rod clamp (MK-15)"].shape.BoundingBox()
        gland = by["Rod gland plate, 2 O-rings (MK-07)"].shape.BoundingBox()
        res[f"pz={pz:+.0f}"] = dict(clashes=clash, plate_bottom_above_deck_mm=round(hp.zmin - deck.zmax, 2),
                                    clamp_top_below_gland_mm=round(gland.zmin - clamp.zmax, 2),
                                    rope_inside_bore=bool(pz - P["sub_t"] - 7 - P["rope"] > -P["well"][2]))
    rod = [p for p in M.build(state) if p.name.startswith("Piston rod")][0].shape.BoundingBox()
    res["rod_length_mm"] = round(rod.zlen, 1)
    res["stage_stroke_used_mm"] = P["pz_top"] - P["pz_bot"]
    res["X_VSR20A_travel_mm"] = P["vs_travel"]
    # vacuum load on the rod in the cube: 1 atm on the rod's section, against the stage's 100 N continuous thrust
    a_rod = math.pi / 4 * (P["rod_od"] / 1000) ** 2
    res["atm_force_on_rod_N"] = round(101325 * a_rod, 1)
    return res


def fit_checks():
    L_box, L_cube = M.levels("FT-1"), M.levels("FT-1V")
    stage_len = {"X-LSQ075B": P["rc_rail_l"] + P["rc_motor_l"], "X-LSQ150B": 150 + 110 + P["rc_motor_l"]}
    out = dict(deck_mm=P["deck"], cube_inside_mm=round(P["cube_in"], 1), cube_face_opening_mm_est=P["cube_open"],
               deck_through_opening_margin_mm=round(P["cube_open"] - max(P["deck"]), 1),
               box_inside_mm=[round(v, 1) for v in P["box_in"]],
               deck_in_box_margins_mm=[round((P["box_in"][0] - P["deck"][0]) / 2, 1),
                                        round((P["box_in"][1] - P["deck"][1]) / 2, 1)])
    for k, v in stage_len.items():
        out[f"{k}_length_mm_est"] = v
        out[f"{k}_fits_cube_square"] = v <= P["cube_in"] - 2 * 5.0
        out[f"{k}_fits_deck"] = v <= P["deck"][0]
    # window height and irradiance at 400 W for a 5 mm collimated beam focused at f = 254
    for name, st in (("box", "FT-1"), ("cube", "FT-1V")):
        parts = M.build(st)
        w = [p for p in parts if p.name.startswith("Window, ")][0].shape.BoundingBox()
        L = M.levels(st)
        h = w.zmin - L["dz"]
        d = P["beam_d"] * h / 254.0
        out[f"window_above_bed_{name}_mm"] = round(h, 1)
        out[f"beam_at_window_{name}_mm"] = round(d, 2)
        out[f"window_irradiance_{name}_kW_cm2_at_400W"] = round(400 / (math.pi / 4 * (d / 10) ** 2) / 1000, 1)
    # cassette height above the deck (to the hopper/arm/vibrator top) against the cube's inside height
    parts = M.build("FT-1V")
    cas = [p for p in parts if p.sub in ("cassette", "recoater") or p.name.startswith(("Slot nozzle", "Exhaust collector"))]
    top = max(p.shape.BoundingBox().zmax for p in cas)
    out["cassette_height_above_floor_mm"] = round(top - L_cube["floor_top"], 1)
    out["cube_inside_height_mm"] = round(L_cube["roof_in"] - L_cube["floor_top"], 1)
    out["box_inside_height_mm"] = round(L_box["roof_in"] - L_box["floor_top"], 1)
    # substrate screws: a countersunk head outside the Ø30 build area must stay inside the Ø39.8 disc
    for size, head in (("M3", 6.0), ("M2.5", 5.0), ("M2", 4.0)):
        r = 15.0 + head / 2
        out[f"substrate_{size}_head_outer_r_mm"] = round(r + head / 2, 2)
        out[f"substrate_{size}_fits"] = r + head / 2 <= P["plate_d"] / 2
    return out


def inside_volume(state, parts):
    """Gas volume: the enclosure's inside less the parts (or their parts) inside it."""
    L = M.levels(state)
    xc, yc = P["deck_c"]
    if state == "FT-1V":
        s = P["cube_in"] / 2
        region = M.box(xc - s, xc + s, yc - s, yc + s, L["floor_top"], L["roof_in"])
        frame = [p for p in parts if p.name.startswith("Ideal Vacuum 12")][0].shape
        v_in = region.cut(frame).Volume()
        vendor = 22.6e6
    else:
        bx, by, bz = P["box_in"]
        region = M.box(xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2, L["floor_top"], L["roof_in"])
        v_in = region.Volume()
        vendor = None
    rbb = region.BoundingBox()
    v_parts = 0.0
    skip = ("Ideal Vacuum 12", "box, 16 x 12", "Box lid", "Lid gasket", "Cube ")
    for p in parts:
        if any(k in p.name for k in skip):
            continue
        if not bb_overlap(rbb, p.shape.BoundingBox()):
            continue
        v_parts += common_volume(region, p.shape)
    return dict(inside_L=round(v_in / 1e6, 2), vendor_L=vendor and vendor / 1e6, parts_inside_L=round(v_parts / 1e6, 2),
                gas_L=round((v_in - v_parts) / 1e6, 2))


def purge_table(gas):
    """Flow purge (box) and pump-purge (cube) from the measured gas volumes (estimates as marked)."""
    rows = []
    air = 209_000
    for st in ("FT-0", "FT-1"):
        V_ = gas[st]["gas_L"]
        for tgt in (1000, 100):
            n = math.log(air / tgt)
            ideal = n * V_ / 20.0
            rows.append(dict(state=st, method="flow purge at 20 L/min", target_ppm=tgt, minutes=f"{ideal:.1f} ideal, "
                             f"{2 * ideal:.0f}-{5 * ideal:.0f} expected", argon_L=f"{2 * n * V_:.0f}-{5 * n * V_:.0f}"))
    V_ = gas["FT-1V"]["gas_L"]
    S = 1.0            # L/s effective pump speed through the KF-25 hose (estimate: McMaster 4396K21 class)
    for pb_mbar in (1.0, 5.0):
        for tgt in (100, 10):
            n = math.ceil(math.log(air / tgt) / math.log(1013 / pb_mbar))
            t_pump = V_ / S * math.log(1013 / pb_mbar) / 60
            mins = n * (t_pump + 1.0)
            rows.append(dict(state="FT-1V", method=f"pump to {pb_mbar:g} mbar, backfill argon", target_ppm=tgt,
                             minutes=f"{n} cycles x ({t_pump:.1f} min pump + ~1 min fill) = {mins:.0f}",
                             argon_L=f"{n * V_:.0f}"))
    return rows


def heat_table():
    """Enclosure air rise for the same heat load as fast_track.py (heater load + laser), by enclosure area."""
    sys.path.insert(0, str(HERE.parent))
    import fast_track as F
    h = F.heat()
    q = h["heater_load_W"]
    lo, hi = (float(x) for x in h["laser_avg_W"].split("-"))
    box_a = F.BOX_AREA_M2
    cube_a = 6 * ((P["cube_frame"] + 2 * (P["cube_plate_t"] - P["cube_boss"])) / 1000) ** 2
    rows = []
    for name, a in (("box (FT-0, FT-1)", box_a), ("cube (FT-1V)", cube_a)):
        for hb, lab in ((F.H_BOX_STILL, "still air"), (F.H_BOX_FAN, "fan")):
            r = [(q + w) / (hb * a) for w in (lo, hi)]
            rows.append(dict(enclosure=name, area_m2=round(a, 3), cooling=lab, rise_K=f"{r[0]:.0f}-{r[1]:.0f}",
                             air_C=f"{F.T_AMB + r[1]:.0f}", stage_limit_C=F.STAGE_MAX_C))
    return rows


def md_table(rows):
    if not rows:
        return "none\n"
    cols = list(rows[0])
    return ("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
            + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows))


def main():
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    res = dict(states={})
    gas = {}
    for st in M.STATES:
        parts = M.build(st)
        clashes, contacts = interference(parts)
        hits, near = beam_check(st, parts) if st != "S1" else ([], [])
        res["states"][st] = dict(n_parts=len(parts), clashes=clashes, contacts=contacts, beam_hits=hits,
                                 beam_nearest=near[:8])
        if st in ("FT-0", "FT-1", "FT-1V"):
            gas[st] = inside_volume(st, parts)
        print(f"{st}: {len(parts)} parts, {len(clashes)} clashes, {len(contacts)} designed contacts, "
              f"{len(hits)} beam hits ({time.time() - t0:.0f} s)")
    for st in ("FT-1", "FT-1V"):
        c, g = recoater_sweep(st)
        res["states"][st]["recoater_clashes"] = c
        res["states"][st]["recoater_gaps"] = g[:10]
        res["states"][st]["piston"] = piston_checks(st)
        print(f"{st}: recoater sweep {len(c)} clashes; piston {res['states'][st]['piston']}")
    res["travel"] = travel_needed()
    res["fit"] = fit_checks()
    res["gas"] = gas
    res["purge"] = purge_table(gas)
    res["heat"] = heat_table()
    (OUT / "checks.json").write_text(json.dumps(res, indent=1, default=str))

    md = ["# Checks on the fast-track model (`ft_checks.py`)", "",
          "Generated from `ft_model.py`. Bought parts are envelopes (some sizes are estimates, marked in `ft_model.P`), so a",
          "clash with a bought part's envelope means 'check against the maker's drawing', not a certain clash.", ""]
    md += ["## 1. Interference and the beam, by state", "",
           "| State | Parts | Clashes | Designed contacts | Beam envelope hits | Nearest parts to the beam (mm) |",
           "|---|---:|---:|---:|---:|---|"]
    for st, r in res["states"].items():
        near = ", ".join(f"{n['part'].split(' (')[0]} {n['clearance_mm']}" for n in r["beam_nearest"][:4]) or "-"
        md.append(f"| {st} | {r['n_parts']} | {len(r['clashes'])} | {len(r['contacts'])} | {len(r['beam_hits'])} | {near} |")
    for st, r in res["states"].items():
        if r["clashes"] or r["beam_hits"]:
            md += ["", f"**{st} clashes:**", "", md_table(r["clashes"] + [dict(a="beam envelope", b=h["part"],
                                                                               volume_mm3=h["volume_mm3"])
                                                                          for h in r["beam_hits"]])]
    md += ["", "Designed contacts (FT-1):", "", md_table(res["states"]["FT-1"]["contacts"])]
    md += ["## 2. Recoater and piston travel", "", "Hopper parks and the travel it needs (cassette frame, mm):", "",
           md_table([res["travel"]])]
    for st in ("FT-1", "FT-1V"):
        r = res["states"][st]
        md += [f"**{st}**: recoater swept over ±{P['rc_travel'] / 2:.1f} mm, {len(r['recoater_clashes'])} clashes. "
               "Smallest gaps:", "", md_table(r["recoater_gaps"][:6])]
        pc = r["piston"]
        md += [f"Piston ({st}): rod {pc['rod_length_mm']} mm; stroke {pc['stage_stroke_used_mm']} of "
               f"{pc['X_VSR20A_travel_mm']} mm; 1 atm on the rod = {pc['atm_force_on_rod_N']} N.", ""]
        md.append(md_table([dict(position=k, **{kk: (len(vv) if kk == "clashes" else vv) for kk, vv in v.items()})
                            for k, v in pc.items() if k.startswith("pz=")]))
    md += ["## 3. Fit", "", md_table([dict(check=k, value=v) for k, v in res["fit"].items()])]
    md += ["## 4. Gas volume from the model, and purging", "", md_table([dict(state=k, **v) for k, v in gas.items()]),
           md_table(res["purge"]),
           "Pump speed (1 L/s effective) and base pressures are estimates; the floor is set by leaks, outgassing and the "
           "argon's own O2, which the analyzer measures.", ""]
    md += ["## 5. Enclosure air temperature (same load as `fast_track.py`)", "", md_table(res["heat"])]
    (OUT / "checks.md").write_text("\n".join(md) + "\n")
    print(f"wrote out/checks.json, out/checks.md in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
