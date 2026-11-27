"""The progression S1 -> S2 -> FT-0 -> FT-1 -> FT-1V as parts arrive: one build path, with its schedule and spend.

fast_track.py schedules FT-0, FT-1 and FT-1V as three separate machines, each started on day 0. This script
schedules them as one machine that grows: every order goes out on day 0 (except the cube in path B), and each
state starts as soon as its parts are in and the state before it has done its job. The durations are
fast_track.py's (vendor statements read 2026-11-25/26, or estimates where marked), plus the upgrade steps.

    python desktop-lpbf/fast-track/cad/ft_progression.py   # out/progression.csv, out/progression.md, img/progression-gantt.png
"""
from __future__ import annotations

import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import fast_track as F  # noqa: E402

OUT, IMG = HERE / "out", HERE.parent / "img"

STATE_OF_TASK = {}


def T(state, dur, deps, basis):
    return (dur, deps, basis, state)


ORDERS = {
    "used optics chain arrives": T("orders", *F.COMMON["used optics chain arrives"]),
    "McMaster stock and hardware": T("orders", *F.COMMON["McMaster stock and hardware"]),
    "safety parts and eyewear": T("orders", *F.COMMON["safety parts and eyewear"]),
    "window, cover slides, beam dump (Edmund, Thorlabs)": T("orders", (2, 5), [], "Edmund 38-990 '5 In Stock'; Thorlabs in-stock items"),
    "O2 analyzer (used)": T("orders", *F.COMMON["O2 analyzer (used)"]),
    "argon cylinder and regulator": T("orders", *F.COMMON["argon cylinder and regulator"]),
    "PC + RTC5 software": T("orders", *F.COMMON["PC + RTC5 software"]),
    "enclosure arrives": T("orders", (3, 8), [], "estimate: distributor stock, ground (fast_track.py)"),
    "LSO registration and SOP": T("approvals", *F.COMMON["LSO registration and SOP"]),
    "EHS review (Al powder)": T("approvals", *F.COMMON["EHS review (Al powder)"]),
}

PATH = {
    # S1: optics on the frame, guide laser onto a target on the deck plate
    "deck plate and target stand made": T("S1", (1, 2), ["McMaster stock and hardware"], "estimate: two plates, ~3 shop hours"),
    "S1 optics bench assembled": T("S1", (1, 1), ["used optics chain arrives", "PC + RTC5 software",
                                                  "deck plate and target stand made"], "estimate"),
    "S1 guide-laser and scanner checks": T("S1", (2, 4), ["S1 optics bench assembled", "LSO registration and SOP",
                                                          "safety parts and eyewear"], "fast_track.py's bench check"),
    # S2: the box round the beam, full power into the dump
    "window stack and beam tube made": T("S2", (2, 3), ["McMaster stock and hardware"], "estimate: MK-02, MK-10, ~8 shop hours"),
    "box cut and fitted": T("S2", (1, 2), ["enclosure arrives", "window stack and beam tube made",
                                          "window, cover slides, beam dump (Edmund, Thorlabs)"],
                            "estimate: window bore, bulkheads, glands, rod hole"),
    "S2 interlocks wired and proven": T("S2", (1, 2), ["box cut and fitted", "safety parts and eyewear"], "estimate"),
    "S2 FULL POWER INTO THE DUMP": T("S2", (1, 2), ["S1 guide-laser and scanner checks", "S2 interlocks wired and proven"],
                                     "milestone: calorimetry, focus ladder; inside the laser's return window"),
    # FT-0
    "FT-0 parts made": T("FT-0", (3, 5), ["window stack and beam tube made"],
                         "estimate: MK-03..07, 11, 16, 17, ~12 shop hours after the window parts"),
    "FT-0 assembled in the box": T("FT-0", (1, 2), ["FT-0 parts made", "box cut and fitted"], "estimate"),
    "FT-0 purge and heat (O2 log)": T("FT-0", (1, 2), ["FT-0 assembled in the box", "O2 analyzer (used)",
                                                     "argon cylinder and regulator"], "estimate"),
    "FT-0 FIRST TRACKS": T("FT-0", (1, 2), ["S2 FULL POWER INTO THE DUMP", "FT-0 purge and heat (O2 log)",
                                           "EHS review (Al powder)"], "milestone"),
    "FT-0 hand-spread layers and pads": T("FT-0", (2, 4), ["FT-0 FIRST TRACKS"], "estimate"),
    # FT-1
    "FT-1 parts made": T("FT-1", (3, 5), ["FT-0 parts made"], "estimate: MK-08, 12, 15, ~12 shop hours"),
    "FT-0 -> FT-1 upgrade": T("FT-1", (1, 2), ["FT-1 parts made", "stages arrive", "FT-0 purge and heat (O2 log)"],
                              "estimate: collar off, rod to the stage, recoater on the deck, block heaters in"),
    "FT-1 re-commission": T("FT-1", (1, 2), ["FT-0 -> FT-1 upgrade"], "estimate: purge, heat both, home stages, interlocks"),
    "FT-1 powder layers: dose, spread, pads": T("FT-1", (3, 5), ["FT-1 re-commission", "FT-0 FIRST TRACKS"], "estimate"),
    "FT-1 FIRST COUPONS": T("FT-1", (2, 5), ["FT-1 powder layers: dose, spread, pads"], "milestone"),
    # FT-1V
    "pump, KF parts, Pirani, feedthroughs": T("FT-1V", (2, 7), [], "fast_track.py (McMaster next day, or used IDP-3)"),
    "cube plates machined": T("FT-1V", (2, 3), ["cube frame and plates arrive (PO)"], "estimate: MK-13, MK-14"),
    "FT-1 -> FT-1V transfer": T("FT-1V", (1, 2), ["cube plates machined", "pump, KF parts, Pirani, feedthroughs",
                                                "FT-1 powder layers: dose, spread, pads"],
                                "estimate: cassette, gland, window stack, stages across; optics up 21 mm"),
    "FT-1V leak check and pump-purge": T("FT-1V", (2, 4), ["FT-1 -> FT-1V transfer"], "fast_track.py"),
    "FT-1V FIRST COUPONS (< 100 ppm)": T("FT-1V", (2, 5), ["FT-1V leak check and pump-purge"], "milestone"),
}

STAGES = {
    "PCard": T("orders", (3, 10), [], "Zaber X-LSM100B 'Lead Time 1-5 Days' (read 2026-11-27) + Thorlabs MTS50/M-Z8 "
                                     "'Available Today'; each vendor under $3,500"),
    "PO": T("orders", (11, 20), [], "both Zaber stages (X-VSR20A, X-LSM100B) on one PO: BYU PO 10-14 days + 1-5 days "
                                  "+ transit"),
}
CUBE = {
    "day 0": T("orders", (11, 16), [], "Ideal Vacuum 'Available now' (2026-11-25) + BYU PO + LTL (fast_track.py)"),
    "after the O2 log": T("orders", (11, 16), ["FT-0 purge and heat (O2 log)"],
                          "ordered only if FT-0's first purge stalls above the target"),
}

SCENARIOS = {
    "A: stages on PCards, cube ordered on day 0": ("PCard", "day 0"),
    "B: stages on PCards, cube ordered after FT-0's O2 log": ("PCard", "after the O2 log"),
    "C: both stages on one Zaber PO, cube after the O2 log": ("PO", "after the O2 log"),
}

MILESTONES = ("S1 guide-laser and scanner checks", "S2 FULL POWER INTO THE DUMP", "FT-0 FIRST TRACKS",
              "FT-1 FIRST COUPONS", "FT-1V FIRST COUPONS (< 100 ppm)")
COLORS = {"orders": "#8c96a0", "approvals": "#b9b9b9", "S1": "#5b7fb5", "S2": "#8e6bbf", "FT-0": "#e08a3c",
          "FT-1": "#3a9a5b", "FT-1V": "#2a9fb0"}


def tasks_for(scn):
    st, cube = SCENARIOS[scn]
    t = {**ORDERS, **PATH}
    t["stages arrive"] = STAGES[st]
    t["cube frame and plates arrive (PO)"] = CUBE[cube]
    return t


def run():
    res = {}
    for scn in SCENARIOS:
        tasks = tasks_for(scn)
        f = F.forward({k: (v[0], v[1], v[2]) for k, v in tasks.items()})
        res[scn] = (tasks, f)
    return res


# Parts.csv lines by the first state that needs them (S1 = the optics bench)
FIRST_STATE = {
    "S1": ["L1", "L2", "L3", "L4", "L5", "L5b", "L6", "L7", "L10", "C1", "E4", "S2", "MON4"],
    "S2": ["L8", "L9", "E1", "S1", "MON6"],
    "FT-0": ["H1", "H2", "H3", "H4", "G1", "G2", "G3", "G4", "G5", "M4", "C2", "S3", "S4", "F1", "F2a", "P1", "MON1",
             "MON2", "MON3", "MON7", "MON8"],
    "FT-1": ["M1b", "M1c", "M2", "M3", "F2b", "MON5"],
    "FT-1V": ["E2", "E3", "E5", "F2c"],
}


def spend():
    rows = {r["id"]: r for r in csv.DictReader(open(HERE.parent / "parts.csv"))}
    out, lo_c, hi_c = [], 0.0, 0.0
    for st, ids in FIRST_STATE.items():
        lo = hi = 0.0
        for i in ids:
            r = rows.get(i)
            if r is None:
                continue
            q = float(r["FT1V"] if st == "FT-1V" else r["FT1"] if st == "FT-1" else r["FT0"] or 0) or float(r["FT1"] or 0)
            if i == "H1":
                q = 2.0          # two plate heaters in FT-0; the block's four come with FT-1
            if i in ("F2b",):    # FT-1's shop time less FT-0's, already counted
                lo += float(r["unit_low"]) - float(rows["F2a"]["unit_low"])
                hi += float(r["unit_high"]) - float(rows["F2a"]["unit_high"])
                continue
            if i in ("F2c",):
                lo += float(r["unit_low"]) - float(rows["F2b"]["unit_low"])
                hi += float(r["unit_high"]) - float(rows["F2b"]["unit_high"])
                continue
            lo += q * float(r["unit_low"])
            hi += q * float(r["unit_high"])
        if st == "FT-1":                                  # the well block's 4 cartridges (H1: FT-0 2, FT-1 6)
            lo += 4 * float(rows["H1"]["unit_low"])
            hi += 4 * float(rows["H1"]["unit_high"])
        lo_c += lo
        hi_c += hi
        out.append(dict(state=st, adds=", ".join(ids), added_low=round(lo), added_high=round(hi),
                        cumulative_low=round(lo_c), cumulative_high=round(hi_c)))
    return out


def gantt(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    keep_orders = ("used optics chain arrives", "enclosure arrives", "stages arrive", "cube frame and plates arrive (PO)",
                   "LSO registration and SOP", "EHS review (Al powder)")
    scns = list(res)[:2]
    shown = {s: [k for k in res[s][1] if res[s][0][k][3] not in ("orders", "approvals") or k in keep_orders] for s in scns}
    n = [len(shown[s]) for s in scns]
    fig, axes = plt.subplots(len(scns), 1, figsize=(12, 1.6 + 0.27 * sum(n)), gridspec_kw=dict(height_ratios=n))
    for ax, scn in zip(axes, scns):
        tasks, f = res[scn]
        names = sorted(shown[scn], key=lambda k: (f[k][2], f[k][3]))
        for i, k in enumerate(names):
            sl, sh, fl, fh = f[k]
            st = tasks[k][3]
            ms = k in MILESTONES
            col = "#b2182b" if ms else COLORS[st]
            ax.barh(i, fl - sl, left=sl, color=col, alpha=0.95, height=0.6)
            ax.barh(i, fh - fl, left=fl, color=col, alpha=0.3, height=0.6)
            if ms:
                ax.text(fh + 0.4, i, f"{fl / 5:.1f}-{fh / 5:.1f} wk", va="center", fontsize=7.5, color=col, weight="bold")
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=7)
        ax.invert_yaxis()
        ax.set_xlim(0, 56)
        ax.set_xticks(range(0, 56, 5))
        ax.set_xticklabels([f"{d // 5}" for d in range(0, 56, 5)], fontsize=8)
        ax.axvspan(15, 30, color="#4daf4a", alpha=0.06)
        ax.grid(axis="x", color="#dddddd", lw=0.6)
        ax.set_axisbelow(True)
        ax.set_title(scn, fontsize=9.5, loc="left")
    fig.legend(handles=[Patch(color=c, label=k) for k, c in COLORS.items()] + [Patch(color="#b2182b", label="milestone")],
               fontsize=7.5, ncol=8, loc="lower center")
    axes[-1].set_xlabel("weeks from the decision (5 working days); dark = earliest, light = to the late estimate; "
                        "green band = 3-6 weeks", fontsize=8)
    fig.suptitle("One machine that grows: S1 -> S2 -> FT-0 -> FT-1 -> FT-1V as the parts arrive (estimates; scenario C in out/progression.md)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0.035, 1, 0.975))
    fig.savefig(IMG / "progression-gantt.png", dpi=125)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    res = run()
    rows = []
    for scn, (tasks, f) in res.items():
        for k, (sl, sh, fl, fh) in f.items():
            rows.append(dict(scenario=scn, task=k, state=tasks[k][3], start_low_d=sl, start_high_d=sh, finish_low_d=fl,
                             finish_high_d=fh, basis=tasks[k][2]))
    with open(OUT / "progression.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    md = ["# Progression schedule (`ft_progression.py`)", "", "Milestones in weeks (5 working days), earliest to latest:", "",
          "| Milestone | " + " | ".join(s.split(":")[0] for s in res) + " |", "|---|" + "---|" * len(res)]
    for m in MILESTONES:
        md.append(f"| {m} | " + " | ".join(f"{res[s][1][m][2] / 5:.1f}-{res[s][1][m][3] / 5:.1f}" for s in res) + " |")
    md += ["", "Scenarios: " + "; ".join(res), "", "Spend by the state that first needs each parts.csv line:", ""]
    sp = spend()
    md += ["| State | Lines | Adds | Cumulative |", "|---|---|---:|---:|"]
    for r in sp:
        md.append(f"| {r['state']} | {r['adds']} | ${r['added_low']:,}-{r['added_high']:,} | "
                  f"${r['cumulative_low']:,}-{r['cumulative_high']:,} |")
    sys.path.insert(0, str(HERE))
    import ft_model as M
    md += ["", "What changes at each step (from the CAD model; moved = the part's bounding box shifted):", ""]
    for x, y in zip(M.STATES[:-1], M.STATES[1:]):
        d = M.diff_states(x, y)
        fmt = lambda lst: "; ".join(f"{n} [{pid}]" if pid else n for n, pid in lst) or "none"  # noqa: E731
        md += [f"**{x} -> {y}** ({len(d['added'])} added, {len(d['moved'])} moved, {len(d['removed'])} removed, "
               f"{d['kept']} unchanged)", "", f"- added: {fmt(d['added'])}", f"- moved: {fmt(d['moved'])}",
               f"- removed: {fmt(d['removed'])}", ""]
    (OUT / "progression.md").write_text("\n".join(md) + "\n")
    gantt(res)
    print("\n".join(md))


if __name__ == "__main__":
    main()
