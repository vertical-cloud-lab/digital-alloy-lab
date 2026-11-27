"""Summary, derived limits and plots from every thermal case in analysis/out/thermal/*/result.json.

    python analysis/thermal_report.py

Writes analysis/out/thermal_summary.{md,json} and analysis/img/thermal_{seals,mass,alarms}.png:
- peak temperature of every seal, the thermocouple spots and the glass, with times;
- the largest shot mass each design takes before its hottest seal reaches 150 C (a working limit with margin)
  and 200 C (FKM's continuous rating), by linear interpolation between the mass cases;
- when each thermocouple would cross its alarm (top 120 C, bottom 150 C) in a bad run, a good run and a hang-up;
- the field plots for the main cases (analysis/out/thermal/<case>/field.png) copied next to the summary.
"""

import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
IMG = HERE / "img"
LIMITS = {"EPDM": (150, 175), "FKM": (200, 230), "FFKM": (240, 325)}
ALARM = {"TC_TOP": 120.0, "TC_BOTTOM": 150.0}


def load():
    res = {}
    for p in sorted((OUT / "thermal").glob("*/result.json")):
        res[p.parent.name] = json.loads(p.read_text())
    return res


def first_cross(ser, lim):
    t, T = np.array(ser["t"]), np.array(ser["T"])
    i = np.where(T >= lim)[0]
    if not len(i):
        return None
    k = i[0]
    if k == 0:
        return float(t[0])
    return float(t[k - 1] + (lim - T[k - 1]) * (t[k] - t[k - 1]) / (T[k] - T[k - 1]))


def hottest_seal(r):
    best = None
    for s in ("N_ORING", "N_BORING", "N_SEAT", "N_SEAL_TOP", "N_SEAL_BOT"):
        if s in r["peaks"]:
            v = r["peaks"][s]["T_max"]
            if best is None or v > best[1]:
                best = (s, v)
    return best


def safe_mass(res, design, seal):
    pts = sorted((r["mass_g"], r["peaks"][seal]["T_max"]) for n, r in res.items()
                 if r["design"] == design and not r["options"] and not r["extra"] and seal in r["peaks"])
    out = {}
    for lim in (150.0, 200.0):
        m = None
        for (m0, t0), (m1, t1) in zip(pts, pts[1:]):
            if t0 <= lim <= t1:
                m = m0 + (lim - t0) * (m1 - m0) / (t1 - t0)
                break
        if m is None and pts and pts[-1][1] < lim:
            m = f"> {pts[-1][0]} (largest case run)"
        if m is None and pts and pts[0][1] > lim:
            m = f"< {pts[0][0]}"
        out[f"to_{int(lim)}C"] = round(m) if isinstance(m, float) else m
    return dict(seal=seal, points=pts, **out)


def main():
    res = load()
    rows = []
    md = ["# Thermal FEA summary (CalculiX, axisymmetric, transient)\n",
          "Every case: the shot (or powder) lands all at once at t = 0 and the run is followed for an hour. "
          "Shot: packed bed (60 % dense) at 1050 C, 70 % liquid, k_eff 5 W/m K unless the case says otherwise. "
          "Peaks are the hottest node of each part at any of the 180 output times. Seal ratings: FKM 200 C "
          "continuous / 230 C short; EPDM 150 / 175 C; FFKM 240 / 325 C. Cases: `analysis/thermal.py` (CASES).\n",
          "| Case | What lands, where | Joint O-ring max (C) [at s] | Other seal max (C) | TC top max | "
          "TC bottom max | Floor/plate max | Glass dT max (K) |",
          "|---|---|---|---|---:|---:|---:|---:|"]
    what = {
        "B_100": "100 g shot on the puck", "B_400": "400 g shot on the puck", "B_816": "816 g shot on the puck (Nov 13 charge)",
        "B_816_k2": "816 g, pile k 2 W/m K", "B_816_k20": "816 g, pile k 20 W/m K (fused)",
        "B_816_noliner": "816 g, no liner", "B_816_cupuck": "816 g, copper puck",
        "B_816_powder400": "816 g of powder at 400 C (a good run)", "B_hangup_25": "25 g of shot fused in the bore just under the joint",
        "B_hangup_100": "100 g of shot fused in the bore just under the joint",
        "A_100": "100 g shot on the puck", "A_250": "250 g shot on the puck", "A_400": "400 g shot on the puck",
        "C_400": "400 g shot in the pan, fused quartz", "C_816": "816 g shot in the pan, fused quartz",
        "C_400_boro": "400 g shot in the pan, borosilicate", "S_seat_120": "stock cup: 120 g of shot against the EPDM seat (Nov 13)",
        "S_glass_300": "stock cup: 300 g of shot fallen into the glass, against its wall (Nov 13)"}
    order = ["B_100", "B_400", "B_816", "B_816_k2", "B_816_k20", "B_816_noliner", "B_816_cupuck", "B_816_powder400",
             "B_hangup_25", "B_hangup_100", "A_100", "A_250", "A_400", "C_400", "C_816", "C_400_boro", "S_seat_120", "S_glass_300"]
    for name in order:
        if name not in res:
            continue
        r = res[name]
        pk = r["peaks"]
        o = pk.get("N_ORING", {})
        others = []
        for s in ("N_BORING", "N_SEAT", "N_SEAL_TOP", "N_SEAL_BOT"):
            if s in pk:
                others.append(f"{s[2:].lower().replace('boring', 'bottom O-ring')} {pk[s]['T_max']:.0f} [{pk[s]['t_at_max_s']:.0f}]")
        floor = pk.get("BOTTOM_CENTRE", pk.get("PLATE_RIM", {})).get("T_max", float("nan"))
        md.append(f"| {name} | {what.get(name, '')} | {o.get('T_max', float('nan')):.0f} [{o.get('t_at_max_s', 0):.0f}] | "
                  f"{'; '.join(others)} | {pk.get('TC_TOP', {}).get('T_max', float('nan')):.0f} | "
                  f"{pk.get('TC_BOTTOM', {}).get('T_max', float('nan')):.0f} | {floor:.0f} | "
                  f"{pk.get('glass_dT', {}).get('dT_max', '')} |")
    limits = {"B (joint O-ring)": safe_mass(res, "B", "N_ORING"), "A (bottom O-ring)": safe_mass(res, "A", "N_BORING"),
              "C (bottom glass seal)": safe_mass(res, "C", "N_SEAL_BOT")}
    md += ["\n## Largest shot mass before the hottest seal reaches 150 C / 200 C\n",
           "Linear interpolation between the mass cases (base cases only).\n", "| Design | Seal | to 150 C (g) | to 200 C (g) | "
           "cases (mass g, seal peak C) |", "|---|---|---|---|---|"]
    for k, v in limits.items():
        md.append(f"| {k} | {v['seal'][2:].lower()} | {v['to_150C']} | {v['to_200C']} | "
                  f"{', '.join(f'{m:.0f}: {t:.0f}' for m, t in v['points'])} |")
    alarms = {}
    for name in ("B_400", "B_816", "B_816_powder400", "B_hangup_25", "B_hangup_100", "A_100", "A_250"):
        if name not in res:
            continue
        r = res[name]
        a = {}
        for tc, lim in ALARM.items():
            if tc in r["series"]:
                a[f"{tc.lower()}_{int(lim)}C_s"] = first_cross(r["series"][tc], lim)
        if "N_ORING" in r["series"]:
            a["oring_150C_s"] = first_cross(r["series"]["N_ORING"], 150.0)
            a["oring_200C_s"] = first_cross(r["series"]["N_ORING"], 200.0)
        if "TC_BOTTOM" in r["series"]:
            t, T = np.array(r["series"]["TC_BOTTOM"]["t"]), np.array(r["series"]["TC_BOTTOM"]["T"])
            a["tc_bottom_at_60s"] = round(float(np.interp(60, t, T)), 0)
            a["tc_bottom_at_3600s"] = round(float(T[-1]), 0)
        alarms[name] = {k: (round(v, 0) if isinstance(v, float) else v) for k, v in a.items()}
    md += ["\n## When the alarms would sound (s after the metal lands)\n",
           "Top thermocouple alarm 120 C, bottom 150 C; blank = never within the hour.\n",
           "| Case | top TC >= 120 C | bottom TC >= 150 C | O-ring >= 150 C | O-ring >= 200 C | bottom TC at 60 s | at 1 h |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for k, a in alarms.items():
        f = lambda x: "" if x is None else f"{x:.0f}"  # noqa: E731
        md.append(f"| {k} | {f(a.get('tc_top_120C_s'))} | {f(a.get('tc_bottom_150C_s'))} | {f(a.get('oring_150C_s'))} | "
                  f"{f(a.get('oring_200C_s'))} | {a.get('tc_bottom_at_60s', '')} | {a.get('tc_bottom_at_3600s', '')} |")
    md += ["\n## Checks on the model\n",
           "- `analysis/verify_axifea.py`: steady film, radiation and surface-flux cases match closed-form answers to "
           "0.001 K; a lumped transient is within 0.8 %.",
           "- Sensitivity of B_816 to the pile's conductivity (2, 5, 20 W/m K), the liner and a copper puck: see the table "
           "(the joint O-ring moves by about 2 K).",
           "- Not modelled: wall-to-wall radiation and argon convection inside (the pile's radiation is put on the "
           "first wall it reaches, all absorbed: conservative for the walls near the pile); the clamp (it would carry "
           "heat from the cup's flange to the cooled cone: conservative); the shot arriving over 30-90 s instead of at "
           "once (conservative for peaks)."]
    (OUT / "thermal_summary.md").write_text("\n".join(md) + "\n")
    (OUT / "thermal_summary.json").write_text(json.dumps({"cases": {k: {kk: vv for kk, vv in v.items() if kk != "series"}
                                                                    for k, v in res.items()},
                                                          "safe_mass": limits, "alarms": alarms}, indent=1) + "\n")
    plots(res, limits)
    for name in ("B_816", "A_250", "C_400", "B_hangup_100", "S_seat_120", "S_glass_300", "B_816_powder400"):
        src = OUT / "thermal" / name / "field.png"
        if src.exists():
            shutil.copy(src, IMG / f"thermal_field_{name}.png")
    print("\n".join(md))


def plots(res, limits):
    IMG.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    groups = {"B: welded 316L": ["B_100", "B_400", "B_816", "B_hangup_25", "B_hangup_100", "B_816_powder400"],
              "A: KF nipple + blank": ["A_100", "A_250", "A_400"],
              "C: quartz rebuild / stock (Nov 13)": ["C_400", "C_816", "C_400_boro", "S_seat_120", "S_glass_300"]}
    cmap = plt.get_cmap("tab10")
    for ax, (title, names) in zip(axes, groups.items()):
        k = 0
        for n in names:
            if n not in res:
                continue
            r = res[n]
            for s, ls in (("N_ORING", "-"), ("N_BORING", "--"), ("N_SEAT", "-."), ("N_SEAL_BOT", ":")):
                if s in r["series"]:
                    ser = r["series"][s]
                    ax.plot(ser["t"], ser["T"], ls, color=cmap(k % 10), lw=1.4,
                            label=f"{n}: {s[2:].lower().replace('boring', 'bottom O-ring')}")
            k += 1
        for lab, (lo, hi) in LIMITS.items():
            ax.axhline(lo, color="0.5", lw=0.8, ls=(0, (6, 3)))
            ax.text(1.05, lo + 4, f"{lab} {lo} C", fontsize=7, color="0.35")
        ax.set_xscale("log")
        ax.set_xlim(1, 3600)
        ax.set_ylim(0, 700 if "C:" in title else 400)
        ax.set_xlabel("time after the metal lands (s)")
        ax.set_ylabel("seal temperature, hottest node (C)")
        ax.set_title(title)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=6.3, loc="upper left")
    fig.tight_layout()
    fig.savefig(IMG / "thermal_seals.png", dpi=125)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6.5, 4.3))
    for (lab, v), c in zip(limits.items(), ("tab:blue", "tab:orange", "tab:green")):
        if v["points"]:
            m, t = zip(*v["points"])
            ax.plot(m, t, "o-", color=c, label=lab)
    for lab, (lo, hi) in LIMITS.items():
        ax.axhline(lo, color="0.5", lw=0.8, ls=(0, (6, 3)))
        ax.text(20, lo + 4, f"{lab} {lo} C", fontsize=7, color="0.35")
    ax.set_xlabel("shot that reaches the cup (g, at 1050 C, all at once)")
    ax.set_ylabel("hottest seal, peak (C)")
    ax.set_title("How much shot each design takes")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(IMG / "thermal_mass.png", dpi=130)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
    for ax, tc in zip(axes, ("TC_TOP", "TC_BOTTOM")):
        for n, c in (("B_816", "tab:red"), ("B_400", "tab:orange"), ("B_816_powder400", "tab:green"),
                     ("B_hangup_25", "tab:purple"), ("B_hangup_100", "tab:brown")):
            if n in res and tc in res[n]["series"]:
                ser = res[n]["series"][tc]
                ax.plot(ser["t"], ser["T"], color=c, label=n)
        ax.axhline(ALARM[tc], color="k", lw=0.8, ls="--")
        ax.text(1.1, ALARM[tc] + 4, f"alarm {ALARM[tc]:.0f} C", fontsize=8)
        ax.set_xscale("log")
        ax.set_xlim(1, 3600)
        ax.set_xlabel("time (s)")
        ax.set_ylabel("thermocouple spot (C)")
        ax.set_title({"TC_TOP": "Top thermocouple (stub, under the flange)", "TC_BOTTOM": "Bottom thermocouple (6 mm above the floor)"}[tc])
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(IMG / "thermal_alarms.png", dpi=125)
    plt.close(fig)


if __name__ == "__main__":
    main()
