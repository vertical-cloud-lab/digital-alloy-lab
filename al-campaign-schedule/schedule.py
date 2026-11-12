"""Al-family alloy discovery campaign: schedule from Nov 12, 2026 to the Feb 28, 2027 paper deadline.

Single source of truth for the dates in README.md (issue #256). Running it:

* checks the plan (36 Al + 4 Cu atomizer runs, no runs on weekends or BYU holidays,
  everything done before the deadline, gates in order);
* writes runs.csv and tasks.csv, the table view of the two charts;
* renders gantt.png, runs-cumulative.png and their -dark variants;
* prints the weekly run counts and the "flat 3 runs a week" comparison quoted in README.md.

    python schedule.py

Needs matplotlib (already in the repo's requirements.txt).
"""

from __future__ import annotations

import csv
import datetime as dt
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = dt.date
ONE = dt.timedelta(days=1)

# --------------------------------------------------------------------------------------
# Calendar
# --------------------------------------------------------------------------------------
TODAY = D(2026, 11, 12)
DEADLINE = D(2027, 2, 28)  # Sunday
SUBMIT = D(2027, 2, 25)  # target: Thursday, three days of buffer
DATA_FREEZE = D(2027, 2, 12)
VALIDATION_CUTOFF = D(2027, 2, 19)

# BYU 2026-27 dates and deadlines (catalog): Thanksgiving Nov 26-27, last class Dec 10,
# finals Dec 12-17, Christmas Dec 25, New Year Dec 31-Jan 1, winter classes start Jan 6,
# MLK Day Jan 18, Presidents' Day Feb 15.
HOLIDAYS = {
    D(2026, 11, 26): "Thanksgiving",
    D(2026, 11, 27): "Thanksgiving",
    D(2026, 12, 25): "Christmas",
    D(2026, 12, 31): "New Year",
    D(2027, 1, 1): "New Year",
    D(2027, 1, 18): "MLK Day",
    D(2027, 2, 15): "Presidents' Day",
}
FINALS = (D(2026, 12, 12), D(2026, 12, 17))
WINTER_BREAK = (D(2026, 12, 18), D(2027, 1, 5))  # finals end -> first day of winter classes

# Week n starts on the Monday below. W0 is the rest of this week.
W1 = D(2026, 11, 16)


def week_of(day: dt.date) -> int:
    return (day - W1).days // 7 + 1


def week_start(n: int) -> dt.date:
    return W1 + dt.timedelta(weeks=n - 1)


# --------------------------------------------------------------------------------------
# Atomizer runs: (date, family, code, block, what it is for)
# Mon-Thu are run days; Friday is maintenance, the weekly decision and Cu runs.
# --------------------------------------------------------------------------------------
BLOCKS = OrderedDict(
    [
        ("A", "Baseline repeats: 6063, 250 g, fixed settings (repeatability bar)"),
        ("D", "Benchmarks made in-house: AlSi10Mg-type and Scalmalloy-type"),
        ("B", "Dosing check: 4047 powder in 6063 cups (known Si)"),
        ("S", "Seed compositions picked from the CALPHAD screen"),
        ("R", "Optimizer rounds: batch chosen each Friday"),
        ("F", "Finalists: extra powder for tensile repeats, DED and outside checks"),
        ("X", "Flex slot: redo a failed run, or A6-A8, or one more candidate"),
        ("Cu", "Copper runs for the ONR work (not part of the Al paper)"),
    ]
)

RUNS = [
    # W1 (Nov 16-20): the machine is still set up for copper after the Nov 10 run
    (D(2026, 11, 16), "Cu", "Cu1", "Cu", "630 bronze; then the full clean (~1 h) and switch to the Al set-up"),
    (D(2026, 11, 17), "Al", "A1", "A", "first run counted toward the repeatability bar"),
    (D(2026, 11, 18), "Al", "A2", "A", "repeat"),
    (D(2026, 11, 19), "Al", "A3", "A", "repeat"),
    # W2 (Nov 23-25; Thanksgiving Thu-Fri)
    (D(2026, 11, 23), "Al", "A4", "A", "repeat"),
    (D(2026, 11, 24), "Al", "A5", "A", "n = 5: check the bar"),
    # W3
    (D(2026, 11, 30), "Al", "D1", "D", "AlSi10Mg-type from 4047 + Mg (the 'beat this' alloy)"),
    (D(2026, 12, 1), "Al", "B30", "B", "30 wt% 4047 powder in thin cups (Si about 3.9 wt%)"),
    (D(2026, 12, 2), "Al", "D2", "D", "Scalmalloy-type Al-Mg-Sc-Zr (the mineral-burden reference)"),
    (D(2026, 12, 3), "Al", "B15", "B", "15 wt% 4047 powder (Si about 2.1 wt%)"),
    # W4 (last day of classes Thu Dec 10)
    (D(2026, 12, 7), "Al", "S1", "S", "seed 1"),
    (D(2026, 12, 8), "Al", "S2", "S", "seed 2"),
    (D(2026, 12, 9), "Al", "S3", "S", "seed 3"),
    (D(2026, 12, 10), "Al", "S4", "S", "seed 4"),
    # W5 (finals)
    (D(2026, 12, 14), "Al", "X1", "X", "flex"),
    (D(2026, 12, 15), "Al", "X2", "X", "flex"),
    (D(2026, 12, 16), "Al", "X3", "X", "flex (move to Dec 21-22 or drop if finals get in the way)"),
    (D(2026, 12, 18), "Cu", "Cu2", "Cu", "copper; clean over the break"),
    # W6-W7: winter break, no runs planned
    # W8 (classes start Wed Jan 6)
    (D(2027, 1, 5), "Al", "R1-1", "R", "round 1 (batch chosen Dec 18, charges made Jan 4)"),
    (D(2027, 1, 6), "Al", "R1-2", "R", "round 1"),
    (D(2027, 1, 7), "Al", "R1-3", "R", "round 1"),
    # W9
    (D(2027, 1, 11), "Al", "X4", "X", "flex"),
    (D(2027, 1, 12), "Al", "R2-1", "R", "round 2 (chosen Fri Jan 8)"),
    (D(2027, 1, 13), "Al", "R2-2", "R", "round 2"),
    (D(2027, 1, 14), "Al", "R2-3", "R", "round 2"),
    (D(2027, 1, 15), "Cu", "Cu3", "Cu", "copper"),
    # W10 (MLK Day Mon Jan 18)
    (D(2027, 1, 19), "Al", "R3-1", "R", "round 3 (chosen Fri Jan 15)"),
    (D(2027, 1, 20), "Al", "R3-2", "R", "round 3"),
    (D(2027, 1, 21), "Al", "R3-3", "R", "round 3"),
    # W11 (finalists picked Fri Jan 22)
    (D(2027, 1, 25), "Al", "F1-a", "F", "finalist 1"),
    (D(2027, 1, 26), "Al", "F1-b", "F", "finalist 1"),
    (D(2027, 1, 27), "Al", "F2-a", "F", "finalist 2"),
    (D(2027, 1, 28), "Al", "F2-b", "F", "finalist 2"),
    # W12
    (D(2027, 2, 1), "Al", "R4-1", "R", "round 4 (chosen Fri Jan 29; powder data only)"),
    (D(2027, 2, 2), "Al", "R4-2", "R", "round 4"),
    (D(2027, 2, 3), "Al", "R4-3", "R", "round 4"),
    (D(2027, 2, 4), "Al", "X5", "X", "flex"),
    # W13: last Al runs; powder data only, frozen Fri Feb 12
    (D(2027, 2, 8), "Al", "D1-r", "D", "AlSi10Mg-type repeat, for the benchmark's own run-to-run spread"),
    (D(2027, 2, 9), "Al", "X6", "X", "flex"),
    # W14: after the data freeze
    (D(2027, 2, 19), "Cu", "Cu4", "Cu", "copper"),
]

# Short-week capacity used for the "flat 3 runs a week" comparison: 3 a week, fewer in
# Thanksgiving week (2) and finals week (2), none over the winter break.
FLAT3 = {1: 3, 2: 2, 3: 3, 4: 3, 5: 2, 6: 0, 7: 0, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3, 13: 3}

# --------------------------------------------------------------------------------------
# Tasks for the Gantt chart: (stream, row label, [(start, end inclusive, tag)], owner, notes)
# --------------------------------------------------------------------------------------
STREAMS = OrderedDict(
    [
        ("atom", "Atomizer and powder"),
        ("print", "Printing (LPBF and DED)"),
        ("test", "Metallography and testing"),
        ("sim", "Simulation and optimizer"),
        ("val", "Independent validation"),
        ("write", "Writing"),
    ]
)


def span(a, b, tag=""):
    return (a, b, tag)


TASKS = [
    # Atomizer and powder
    ("atom", "Settings, SOP (#253), consumables count, G0", [span(D(2026, 11, 12), D(2026, 11, 20))], "Gage, Ronnie", "fixed settings and the five SOP questions settled before A1"),
    ("atom", "Al runs (36)", "RUNS-Al", "Gage, Ronnie + a 3rd operator", "one marker per run day"),
    ("atom", "Cu runs (4)", "RUNS-Cu", "Gage", "Fridays at block boundaries, each followed by the full clean"),
    ("atom", "Cups and plugs in bulk, then weekly charge kits", [span(D(2026, 11, 13), D(2026, 12, 4), ""), span(D(2026, 12, 7), D(2027, 2, 5), "")], "Paul, doser team", "or sawn bar + master-alloy pieces where possible (#250)"),
    ("atom", "Sieve, weigh, seal 5 g for O (within 48 h)", [span(D(2026, 11, 17), D(2027, 2, 10))], "powder team", "two splits per run at 250/63/45 um"),
    ("atom", "Weekly SEM/EDS session (all of the week's powders)", [span(D(2026, 11, 19), D(2027, 2, 12))], "Ronnie + 1-2 more trained users", "PSD >=1000 particles, shape >=400, EDS top/mid/bottom"),
    # Printing
    ("print", "Book Utah MIDI and U of U DED (Carl's visit)", [span(D(2026, 11, 13), D(2026, 11, 25))], "Carl, Sterling", "reduced-build kit? powder per build? groove plates? dates"),
    ("print", "LPBF sessions, Utah MIDI (P1-P5)", [span(D(2026, 12, 2), D(2026, 12, 3), "P1"), span(D(2026, 12, 16), D(2026, 12, 17), "P2"), span(D(2027, 1, 12), D(2027, 1, 13), "P3"), span(D(2027, 1, 20), D(2027, 1, 21), "P4"), span(D(2027, 2, 2), D(2027, 2, 3), "P5")], "Ronnie, Carl", "see README for what each session prints"),
    ("print", "DED sessions, U of U (coarse 63-150 um powder)", [span(D(2026, 12, 15), D(2026, 12, 15), "DED1"), span(D(2027, 1, 14), D(2027, 1, 14), "DED2"), span(D(2027, 2, 4), D(2027, 2, 4), "DED3")], "Carl", "uses the fraction LPBF can't"),
    ("print", "Part removal, heat treatment, specimen prep", [span(D(2026, 12, 4), D(2026, 12, 11)), span(D(2026, 12, 17), D(2026, 12, 23)), span(D(2027, 1, 13), D(2027, 1, 19)), span(D(2027, 1, 21), D(2027, 1, 27)), span(D(2027, 2, 3), D(2027, 2, 9))], "printing team", "about a week after each session"),
    # Metallography and testing
    ("test", "Archimedes density set-up (#144)", [span(D(2026, 11, 16), D(2026, 12, 4))], "Seth or volunteer", "needed for P1 cubes"),
    ("test", "Polishing batches (powder and print sections)", [span(D(2026, 11, 30), D(2027, 2, 11))], "polishing team", "one batch a week on the PX500"),
    ("test", "Hardness and density on every print", [span(D(2026, 12, 7), D(2027, 2, 12))], "testing team", "the fast strength screen the optimizer uses"),
    ("test", "Tensile: dry run, baseline, seeds, finalists", [span(D(2026, 12, 2), D(2026, 12, 4), "dry run"), span(D(2026, 12, 14), D(2026, 12, 16), "AlSi10Mg"), span(D(2027, 1, 19), D(2027, 1, 22), "seeds"), span(D(2027, 2, 9), D(2027, 2, 12), "finalists")], "testing team", ">=3 specimens per alloy for the finalists"),
    ("test", "Corrosion: electrodes, method check, baselines, finalists", [span(D(2026, 11, 16), D(2026, 11, 20), "order"), span(D(2026, 12, 7), D(2026, 12, 18), "method"), span(D(2027, 1, 11), D(2027, 1, 15), "baselines"), span(D(2027, 1, 25), D(2027, 2, 12), "campaign")], "Ben, Jarrett", "EZstat-Pro on the CubXL; 3.5 wt% NaCl"),
    # Simulation and optimizer
    ("sim", "Freeze design space and mineral-burden metric", [span(D(2026, 11, 12), D(2026, 11, 20))], "Xavier, Sterling", "elements on hand, bounds, Al >= 80 wt%, liquidus limit"),
    ("sim", "CALPHAD screen, then pick seeds S1-S4", [span(D(2026, 11, 16), D(2026, 12, 4))], "Xavier", "pycalphad now; Thermo-Calc if licensed"),
    ("sim", "Pre-register the AI benchmark", [span(D(2026, 11, 30), D(2026, 12, 4))], "Xavier, Sterling", "committed before the first optimizer round"),
    ("sim", "Printability maps before each print session", [span(D(2026, 11, 23), D(2027, 2, 1))], "Xavier", "Eagar-Tsai (#238) or AM Module"),
    ("sim", "Optimizer: batch chosen every Friday", [span(D(2026, 12, 14), D(2027, 1, 29))], "Xavier", "R1 Dec 18, R2 Jan 8, R3 Jan 15, F Jan 22, R4 Jan 29"),
    ("sim", "Benchmark replay (>=20 seeds), Thermo-Calc re-check", [span(D(2027, 2, 1), D(2027, 2, 17))], "Xavier", "acceleration factor with bootstrap CIs"),
    # Independent validation
    ("val", "Line up outside chemistry, tensile, 2nd print", [span(D(2026, 12, 14), D(2027, 1, 8))], "Sterling, Gage", "accounts and POs ready before samples exist"),
    ("val", "O and ICP batch 1 (A, B, D, S powders)", [span(D(2027, 1, 8), D(2027, 1, 29), "")], "Gage", "sealed 5 g splits"),
    ("val", "Finalists out, results back", [span(D(2027, 1, 29), D(2027, 2, 19))], "Sterling", "anything late goes to the SI as pending, or is cut"),
    # Writing
    ("write", "Journal, authors, section owners, figure scripts", [span(D(2026, 11, 13), D(2026, 11, 25))], "Sterling", "Adv. Mater. collection article (#120)"),
    ("write", "Methods (from the SOPs) and introduction", [span(D(2026, 11, 30), D(2027, 1, 4))], "section owners", "finals and break weeks are writing weeks"),
    ("write", "Results figures, refreshed weekly", [span(D(2026, 12, 7), D(2027, 2, 12))], "everyone", "scripts re-run every Friday"),
    ("write", "Full draft (version A or B)", [span(D(2027, 1, 29), D(2027, 2, 15))], "Sterling + leads", "version decided Jan 29"),
    ("write", "Co-author review, revise, submit", [span(D(2027, 2, 16), D(2027, 2, 25))], "all authors", "submit Thu Feb 25; deadline Sun Feb 28"),
]

GATES = [
    (D(2026, 11, 20), "G0", "Ready to run: settings fixed, consumables ordered, design space frozen, Utah and DED booked"),
    (D(2026, 12, 4), "G1", "Repeatability bar checked on A1-A5; seeds S1-S4 picked; benchmark pre-registered; P1 printed"),
    (D(2027, 1, 15), "G2", "One full loop shown (CALPHAD -> atomize -> print -> test -> optimizer); >=2 in-house powders print >=99% dense"),
    (D(2027, 1, 22), "G3", "Finalists F1, F2 picked; outside checks booked"),
    (D(2027, 1, 29), "G4", "Paper version A (new alloy) or B (feedstock + replay) decided"),
    (DATA_FREEZE, "Freeze", "Experimental data frozen"),
    (VALIDATION_CUTOFF, "Outside", "Cut-off for outside results"),
    (SUBMIT, "Submit", "Target submission (deadline Sun Feb 28)"),
]


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------
def check() -> None:
    fam = Counter(r[1] for r in RUNS)
    assert fam["Al"] == 36, fam
    assert fam["Cu"] == 4, fam
    days = [r[0] for r in RUNS]
    assert len(days) == len(set(days)), "two runs on one day"
    for day, family, code, block, _ in RUNS:
        assert day.weekday() < 5, f"{code} on a weekend"
        assert day not in HOLIDAYS, f"{code} on {HOLIDAYS[day]}"
        assert not (WINTER_BREAK[0] < day < WINTER_BREAK[1]), f"{code} in the winter break"
        if family == "Al":
            assert day <= DATA_FREEZE, f"{code} after the data freeze"
        assert block in BLOCKS, code
    codes = [r[2] for r in RUNS]
    assert len(codes) == len(set(codes)), "duplicate run code"
    for stream, label, spans, *_ in TASKS:
        assert stream in STREAMS, label
        if isinstance(spans, str):
            continue
        for a, b, _ in spans:
            assert a <= b, label
            assert TODAY <= a and b <= DEADLINE, label
    gate_days = [g[0] for g in GATES]
    assert gate_days == sorted(gate_days)
    assert SUBMIT < DEADLINE


def weekly_counts():
    al = Counter(week_of(r[0]) for r in RUNS if r[1] == "Al")
    cu = Counter(week_of(r[0]) for r in RUNS if r[1] == "Cu")
    return al, cu


# --------------------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------------------
def write_csvs() -> None:
    with open(HERE / "runs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "weekday", "week", "family", "code", "block", "block_meaning", "purpose"])
        for day, family, code, block, purpose in RUNS:
            w.writerow([day.isoformat(), day.strftime("%a"), f"W{week_of(day)}", family, code, block, BLOCKS[block], purpose])
    with open(HERE / "tasks.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stream", "task", "start", "end", "tag", "suggested_lead", "notes"])
        for stream, label, spans, owner, notes in TASKS:
            if isinstance(spans, str):
                fam = spans.split("-")[1]
                rs = [r for r in RUNS if r[1] == fam]
                w.writerow([STREAMS[stream], label, rs[0][0].isoformat(), rs[-1][0].isoformat(), f"{len(rs)} run days (runs.csv)", owner, notes])
                continue
            for a, b, tag in spans:
                w.writerow([STREAMS[stream], label, a.isoformat(), b.isoformat(), tag, owner, notes])
        for day, tag, meaning in GATES:
            w.writerow(["Gates", tag, day.isoformat(), day.isoformat(), "gate", "", meaning])


# --------------------------------------------------------------------------------------
# Charts (dataviz skill: validated categorical slots 1-6, text in ink tokens, hairline grid)
# --------------------------------------------------------------------------------------
THEMES = {
    "light": dict(
        surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781", grid="#e1e0d9",
        axis="#c3c2b7", band="#f0efec", band_strong="#e6e5df", context="#a8a69f",
        series=["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"],
    ),
    "dark": dict(
        surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781", grid="#2c2c2a",
        axis="#383835", band="#262624", band_strong="#30302d", context="#6f6d68",
        series=["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"],
    ),
}


def _setup_mpl():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none"})
    return plt


def gantt(mode: str, out: Path) -> None:
    plt = _setup_mpl()
    import matplotlib.dates as mdates
    from matplotlib.patches import FancyBboxPatch, Rectangle

    t = THEMES[mode]
    color = {k: t["series"][i] for i, k in enumerate(STREAMS)}

    # rows: header per stream, then its tasks
    rows = []  # (kind, stream, label, spans)
    rows.append(("gates", None, "Gates and deadlines", None))
    for s in STREAMS:
        rows.append(("header", s, STREAMS[s], None))
        for stream, label, spans, *_ in TASKS:
            if stream == s:
                rows.append(("task", s, label, spans))
    n = len(rows)

    x0, x1 = D(2026, 11, 9), D(2027, 3, 1)
    fig_w, row_in, top_in, bot_in, left_in, right_in = 13.0, 0.30, 1.35, 0.75, 4.35, 0.35
    fig_h = top_in + bot_in + n * row_in
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=150, facecolor=t["surface"])
    ax = fig.add_axes([left_in / fig_w, bot_in / fig_h, 1 - (left_in + right_in) / fig_w, n * row_in / fig_h])
    ax.set_facecolor(t["surface"])
    X0, X1 = mdates.date2num(x0), mdates.date2num(x1)
    ax.set_xlim(X0, X1)
    ax.set_ylim(n - 0.5, -0.5)

    # px conversions for 4 px rounded ends
    ax_w_px = (1 - (left_in + right_in) / fig_w) * fig_w * 150
    ax_h_px = n * row_in * 150
    px_day = ax_w_px / (X1 - X0)
    px_row = ax_h_px / n
    r_days = 4 / px_day
    aspect = (4 / px_row) / r_days

    # background bands: finals, winter break, holidays
    def band(a, b, fc, z=0):
        ax.add_patch(Rectangle((mdates.date2num(a), -0.5), mdates.date2num(b + ONE) - mdates.date2num(a), n, facecolor=fc, edgecolor="none", zorder=z))

    band(WINTER_BREAK[0], WINTER_BREAK[1], t["band"])
    band(FINALS[0], FINALS[1], t["band"])
    for h in HOLIDAYS:
        band(h, h, t["band_strong"])

    # week grid (Mondays) and month labels
    mondays = [W1 + dt.timedelta(weeks=k) for k in range(-1, 16)]
    for m in mondays:
        if x0 <= m <= x1:
            ax.axvline(mdates.date2num(m), color=t["grid"], lw=0.8, zorder=0.5)
    ax.set_xticks([mdates.date2num(m) for m in mondays if x0 <= m <= x1])
    ax.set_xticklabels([f"W{week_of(m)}\n{m.strftime('%b')} {m.day}" if week_of(m) >= 1 else f"W0\n{m.strftime('%b')} {m.day}" for m in mondays if x0 <= m <= x1], fontsize=9, color=t["ink2"])
    ax.tick_params(axis="x", length=0, pad=4)

    # stream separators
    for i, (kind, s, label, spans) in enumerate(rows):
        if kind == "header" and i > 0:
            ax.axhline(i - 0.5, color=t["axis"], lw=0.8, zorder=0.6)

    def bar(a, b, y, fc, h=0.56, z=3):
        xa = mdates.date2num(a)
        w = mdates.date2num(b + ONE) - xa
        ax.add_patch(FancyBboxPatch((xa + 0.08, y - h / 2), w - 0.16, h, boxstyle=f"round,pad=0,rounding_size={min(r_days, (w - 0.16) / 2):.4f}", mutation_aspect=aspect, facecolor=fc, edgecolor="none", zorder=z))

    ylabels = []
    for i, (kind, s, label, spans) in enumerate(rows):
        ylabels.append(label)
        if kind == "gates":
            align = {"Freeze": ("right", -0.5), "Submit": ("left", 0.5)}
            for day, tag, _ in GATES:
                xm = mdates.date2num(day) + 0.5
                ha, dx = align.get(tag, ("center", 0.0))
                ax.plot([xm], [i], marker="D", ms=8, color=t["ink"], mec=t["surface"], mew=2, zorder=5)
                ax.text(xm + dx, i - 0.36, tag, ha=ha, va="bottom", fontsize=8.5, color=t["ink"], zorder=6)
            dl = mdates.date2num(DEADLINE) + 0.5
            ax.axvline(dl, color=t["ink2"], lw=1.0, zorder=4)
        elif kind == "header":
            pass  # swatch drawn in the label column below
        elif isinstance(spans, str):
            fam = spans.split("-")[1]
            fc = color[s] if fam == "Al" else t["context"]
            for r in RUNS:
                if r[1] == fam:
                    bar(r[0], r[0], i, fc, h=0.6)
        else:
            for a, b, tag in spans:
                bar(a, b, i, color[s])
                if tag:
                    xa = mdates.date2num(a)
                    xb = mdates.date2num(b + ONE)
                    ax.text(xb + 0.4, i, tag, ha="left", va="center", fontsize=8.5, color=t["ink2"], zorder=6)
                    _ = xa

    ax.set_yticks(range(n))
    ax.set_yticklabels(ylabels, fontsize=10)
    for lab, (kind, *_rest) in zip(ax.get_yticklabels(), rows):
        lab.set_color(t["ink"] if kind in ("header", "gates") else t["ink2"])
        if kind in ("header", "gates"):
            lab.set_fontweight("bold")
    ax.tick_params(axis="y", length=0, pad=8)
    for tick, (kind, s, *_r) in zip(ax.yaxis.get_major_ticks(), rows):
        if kind == "header":
            tick.set_pad(30)
            # 14 x 10 px swatch, right edge 10 px left of the axes
            xr = (left_in * 150 - 10) / (fig_w * 150)
            yc = (bot_in + (n - 0.5 - ylabels.index(STREAMS[s])) * row_in) / fig_h
            fig.patches.append(FancyBboxPatch((xr - 14 / (fig_w * 150), yc - 5 / (fig_h * 150)), 14 / (fig_w * 150), 10 / (fig_h * 150), boxstyle="round,pad=0,rounding_size=0.0012", transform=fig.transFigure, facecolor=color[s], edgecolor="none"))
    for sp in ax.spines.values():
        sp.set_visible(False)

    # band labels along the top of the plot
    def top_label(a, b, text):
        xm = (mdates.date2num(a) + mdates.date2num(b + ONE)) / 2
        ax.text(xm, -0.95, text, ha="center", va="bottom", fontsize=8.5, color=t["muted"], clip_on=False)

    top_label(D(2026, 11, 26), D(2026, 11, 27), "Thanksgiving")
    top_label(FINALS[0], FINALS[1], "Finals")
    top_label(D(2026, 12, 21), D(2027, 1, 3), "Winter break (no runs)")
    top_label(D(2027, 1, 18), D(2027, 1, 18), "MLK")
    top_label(D(2027, 2, 15), D(2027, 2, 15), "Pres. Day")
    ax.text(mdates.date2num(DEADLINE) + 0.5, -0.95, "Deadline", ha="center", va="bottom", fontsize=8.5, color=t["ink2"], clip_on=False)

    # title + legend (legend: one swatch per stream, plus gate and Cu keys)
    mx = 0.25 / fig_w
    fig.text(mx, 1 - 0.25 / fig_h, "Al alloy discovery campaign, Nov 12, 2026 to the Feb 28, 2027 paper deadline", fontsize=14, fontweight="bold", color=t["ink"], va="top")
    fig.text(mx, 1 - 0.55 / fig_h, "36 Al + 4 Cu atomizer runs, one marker per run day. Diamonds are decision gates. Shaded columns are finals, the winter break and holidays.", fontsize=10, color=t["ink2"], va="top")
    lx, ly = mx, 1 - 0.92 / fig_h
    sw_w, sw_h = 14 / (fig_w * 150), 10 / (fig_h * 150)
    for key, name, fc in [(s, STREAMS[s], color[s]) for s in STREAMS] + [("cu", "Cu run (other project)", t["context"])]:
        fig.patches.append(FancyBboxPatch((lx, ly), sw_w, sw_h, boxstyle="round,pad=0,rounding_size=0.0012", transform=fig.transFigure, facecolor=fc, edgecolor="none"))
        txt = fig.text(lx + sw_w + 6 / (fig_w * 150), ly - 1 / (fig_h * 150), name, fontsize=9.5, color=t["ink2"], va="bottom")
        fig.canvas.draw()
        lx = txt.get_window_extent().x1 / (fig_w * 150) + 22 / (fig_w * 150)

    fig.savefig(out, dpi=150, facecolor=t["surface"])
    plt.close(fig)


def cumulative(mode: str, out: Path) -> None:
    plt = _setup_mpl()
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle

    t = THEMES[mode]
    al_days = sorted(r[0] for r in RUNS if r[1] == "Al")

    # proposed plan: step up on each run day
    xs, ys = [W1 - ONE], [0]
    for k, day in enumerate(al_days, 1):
        xs += [day, day]
        ys += [k - 1, k]
    xs.append(DATA_FREEZE)
    ys.append(len(al_days))

    # flat 3/week: runs on Mon/Tue/Wed of each week (fewer in short weeks)
    flat_days = []
    for wk, cap in FLAT3.items():
        cands = [week_start(wk) + dt.timedelta(days=d) for d in range(5)]
        cands = [c for c in cands if c not in HOLIDAYS]
        flat_days += cands[:cap]
    fx, fy = [W1 - ONE], [0]
    for k, day in enumerate(flat_days, 1):
        fx += [day, day]
        fy += [k - 1, k]
    fx.append(DATA_FREEZE)
    fy.append(len(flat_days))

    fig = plt.figure(figsize=(10.5, 4.6), dpi=150, facecolor=t["surface"])
    ax = fig.add_axes([0.07, 0.14, 0.80, 0.66])
    ax.set_facecolor(t["surface"])
    x0, x1 = D(2026, 11, 12), D(2027, 2, 28)
    ax.set_xlim(mdates.date2num(x0), mdates.date2num(x1))
    ax.set_ylim(0, 40)
    for a, b in [WINTER_BREAK, FINALS]:
        ax.add_patch(Rectangle((mdates.date2num(a), 0), mdates.date2num(b + ONE) - mdates.date2num(a), 40, facecolor=t["band"], edgecolor="none", zorder=0))
    for y in (10, 20, 30):
        ax.axhline(y, color=t["grid"], lw=0.8, zorder=0.5)
    ax.plot([mdates.date2num(x0), mdates.date2num(D(2027, 2, 7))], [36, 36], color=t["ink2"], lw=1.0, zorder=1)
    ax.text(mdates.date2num(D(2026, 11, 14)), 36.6, "36 Al runs needed", fontsize=9.5, color=t["ink2"], va="bottom")
    fz = mdates.date2num(DATA_FREEZE + ONE)
    ax.axvline(fz, color=t["axis"], lw=1.0, zorder=1)
    ax.text(fz + 0.6, 2, "data freeze\nFeb 12", fontsize=9, color=t["muted"], va="bottom")
    ax.text(mdates.date2num(D(2026, 12, 26)), 2, "finals and\nwinter break", fontsize=9, color=t["muted"], ha="center", va="bottom")

    ax.plot([mdates.date2num(x) for x in fx], fy, color=t["context"], lw=2, solid_joinstyle="round", solid_capstyle="round", zorder=2)
    ax.plot([mdates.date2num(x) for x in xs], ys, color=t["series"][0], lw=2, solid_joinstyle="round", solid_capstyle="round", zorder=3)
    for xx, yy, c, lab, dy in [(fx[-1], fy[-1], t["context"], f"{fy[-1]}: flat 3 a week", 0.0), (xs[-1], ys[-1], t["series"][0], f"{ys[-1]}: this plan", 1.8)]:
        ax.plot([mdates.date2num(xx)], [yy], marker="o", ms=8, color=c, mec=t["surface"], mew=2, zorder=4)
        ax.text(mdates.date2num(xx) + 1.2, yy + dy, lab, fontsize=10, color=t["ink"], va="center")

    mondays = [W1 + dt.timedelta(weeks=k) for k in range(0, 15, 2)]
    ax.set_xticks([mdates.date2num(m) for m in mondays])
    ax.set_xticklabels([f"{m.strftime('%b')} {m.day}" for m in mondays], fontsize=9, color=t["ink2"])
    ax.set_yticks([0, 10, 20, 30])
    ax.tick_params(axis="both", length=0, colors=t["ink2"], labelsize=9)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.axhline(0, color=t["axis"], lw=1.0, zorder=1)

    fig.text(0.07, 0.95, "Cumulative Al atomizer runs", fontsize=13, fontweight="bold", color=t["ink"], va="top")
    fig.text(0.07, 0.885, "Flat 3 runs a week (2 in Thanksgiving and finals weeks, none over the break) vs. this plan's 3-4 slots a week", fontsize=9.5, color=t["ink2"], va="top")
    # legend
    from matplotlib.lines import Line2D

    handles = [Line2D([0], [0], color=t["series"][0], lw=2), Line2D([0], [0], color=t["context"], lw=2)]
    leg = fig.legend(handles, ["This plan (3-4 slots a week)", "Flat 3 a week"], loc="upper right", bbox_to_anchor=(0.97, 0.99), frameon=False, fontsize=9.5, labelcolor=t["ink2"])
    _ = leg
    fig.savefig(out, dpi=150, facecolor=t["surface"])
    plt.close(fig)
    return len(flat_days), len(al_days)


def main() -> None:
    check()
    write_csvs()
    al, cu = weekly_counts()
    print("Week  starts      Al  Cu  flat-3")
    for wk in range(0, 16):
        print(f"W{wk:<4} {week_start(wk) if wk else TODAY}  {al.get(wk, 0):>2}  {cu.get(wk, 0):>2}  {FLAT3.get(wk, 0):>2}")
    print(f"Total Al {sum(al.values())}, Cu {sum(cu.values())}; flat 3/week through Feb 12: {sum(FLAT3.values())}")
    print("Al runs by block:", dict(Counter(r[3] for r in RUNS if r[1] == 'Al')))
    for mode in ("light", "dark"):
        suffix = "" if mode == "light" else "-dark"
        gantt(mode, HERE / f"gantt{suffix}.png")
        cumulative(mode, HERE / f"runs-cumulative{suffix}.png")
    print("wrote runs.csv, tasks.csv, gantt*.png, runs-cumulative*.png")


if __name__ == "__main__":
    main()
