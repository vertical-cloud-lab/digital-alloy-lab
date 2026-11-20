"""Machine cost under five buying strategies, from the BOM and the two sourcing tables next to this script.

Scenarios
  baseline     bom.csv as it stands (low = cheapest listed option per line, high = premium option)
  used         the big lines bought used or new-surplus (used-options.csv, rows with a `pick`)
  cheaper      McMaster/DigiKey/Thorlabs catalogue parts swapped for same-spec parts from other sources
               (cheaper-equivalents.csv, rows with counted = yes)
  both         used + cheaper; where both offer the same component, the cheaper one wins
  engraver     buy the Monport GT 200 W split MOPA engraver (~$7,500 academic, pulsed only) as a testbed and
               defer the CW optics chain (L1, L2, L3, L5, L6, C1); printed as "phase 0" spend and as the
               eventual total once the CW chain is bought too

How a replacement is applied. Each row of the two CSVs names the component it replaces (`replaces`, e.g.
"G7:3861N11" or "L1:laser") and what that component contributes to the BOM line's low and high totals
(`base_low_usd`, `base_high_usd`; 0 means the component is not in that end of the range). For each component
and each end, the scenario uses min(base, alternative): an alternative never makes a line dearer, and a
BOM option that is already cheaper (e.g. the $60 open-source scan controller at C1's low end) stays.
So the low end of every scenario still contains the BOM's under-spec low options (a PRC laser, a marking
galvo, OPAL). The at-spec table, always printed, is the like-for-like comparison: the CW optics chain at the
design's spec (new = the BOM's high end for L1, L3, L5, L6, C1; used = the used picks) with the cheapest listed
option on every other line. Lead times are not computed here; see ../cost-scenarios.md section 4.

Re-run (standard library only), from the repo root:
    python desktop-lpbf/cost/cost_scenarios.py            # totals table
    python desktop-lpbf/cost/cost_scenarios.py --lines    # plus every BOM line that changes
    python desktop-lpbf/cost/cost_scenarios.py --at-spec  # plus the CW chain's lines, new vs used, at spec
"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BOM = HERE.parent / "bom.csv"
USED = HERE / "used-options.csv"
CHEAP = HERE / "cheaper-equivalents.csv"
ENGRAVER_USD = 7500.0  # Monport GT 200 W split MOPA, academic price reported in the issue thread (not fetched here)
CW_CHAIN = ["L1", "L2", "L3", "L5", "L6", "C1"]


def num(x):
    try:
        return float(str(x).replace(",", "").replace("$", ""))
    except ValueError:
        return None


def read_bom():
    lines = {}
    for r in csv.DictReader(open(BOM)):
        q = float(r["qty"])
        lines[r["id"]] = {"item": r["item"], "low": q * float(r["unit_low_usd"]), "high": q * float(r["unit_high_usd"])}
    return lines


def read_used():
    """component -> {line, base_low, base_high, low, high}; low/high are None when no listing is picked for that end."""
    comp = {}
    for r in csv.DictReader(open(USED)):
        pick = r["pick"].strip()
        if not pick or not r["replaces"]:
            continue
        c = comp.setdefault(r["replaces"], {"line": r["bom_line"], "base_low": num(r["base_low_usd"]) or 0.0,
                                            "base_high": num(r["base_high_usd"]) or 0.0, "low": None, "high": None})
        cost = sum(num(r[k]) or 0.0 for k in ("price_usd", "shipping_usd", "extra_usd"))
        for end in ("low", "high"):
            if end in pick:
                c[end] = (c[end] or 0.0) + cost
    return comp


def read_cheaper():
    """component -> {line, base_low, base_high, low, high}: the cheapest counted alternative for each component."""
    comp = {}
    if not CHEAP.exists():
        return comp
    for r in csv.DictReader(open(CHEAP)):
        if r.get("counted", "").strip().lower() != "yes":
            continue
        alt = num(r["alt_line_usd"])
        if alt is None:
            continue
        c = comp.setdefault(r["replaces"], {"line": r["bom_line"], "base_low": num(r["base_low_usd"]) or 0.0,
                                            "base_high": num(r["base_high_usd"]) or 0.0, "low": None, "high": None})
        for end in ("low", "high"):
            c[end] = alt if c[end] is None else min(c[end], alt)
    return comp


def apply(lines, *sources):
    """Return {line: [low, high]} after applying every component replacement in `sources` (min wins)."""
    out = {k: [v["low"], v["high"]] for k, v in lines.items()}
    keys = set().union(*[s.keys() for s in sources])
    for key in keys:
        entries = [s[key] for s in sources if key in s]
        line = entries[0]["line"]
        if line not in out:
            continue
        for i, end in enumerate(("low", "high")):
            base = entries[0]["base_" + end]
            if base <= 0:
                continue  # component not in this end of the BOM range
            alts = [e[end] for e in entries if e[end] is not None]
            if alts:
                out[line][i] += min([base] + alts) - base
    return out


def totals(t):
    return sum(v[0] for v in t.values()), sum(v[1] for v in t.values())


def main():
    lines = read_bom()
    used, cheap = read_used(), read_cheaper()
    sc = {
        "Baseline, all new (bom.csv)": apply(lines),
        "Used majors": apply(lines, used),
        "Cheaper same-spec equivalents": apply(lines, cheap),
        "Both (used majors + cheaper equivalents)": apply(lines, used, cheap),
    }
    base_lo, base_hi = totals(sc["Baseline, all new (bom.csv)"])
    print("| Scenario | Low (USD) | High (USD) | vs baseline low | vs baseline high |")
    print("|---|---:|---:|---:|---:|")
    for name, t in sc.items():
        lo, hi = totals(t)
        print(f"| {name} | {lo:,.0f} | {hi:,.0f} | {lo - base_lo:+,.0f} | {hi - base_hi:+,.0f} |")
    for name in ("Baseline, all new (bom.csv)", "Both (used majors + cheaper equivalents)"):
        t = sc[name]
        lo, hi = totals(t)
        cw_lo = sum(t[k][0] for k in CW_CHAIN if k in t)
        cw_hi = sum(t[k][1] for k in CW_CHAIN if k in t)
        short = "baseline" if name.startswith("Baseline") else "both"
        print(f"| Engraver testbed first, phase 0 ({short} prices, CW chain deferred) | {lo - cw_lo + ENGRAVER_USD:,.0f} "
              f"| {hi - cw_hi + ENGRAVER_USD:,.0f} | {lo - cw_lo + ENGRAVER_USD - base_lo:+,.0f} | {hi - cw_hi + ENGRAVER_USD - base_hi:+,.0f} |")
        print(f"| Engraver testbed first, then the CW chain ({short} prices) | {lo + ENGRAVER_USD:,.0f} | {hi + ENGRAVER_USD:,.0f} "
              f"| {lo + ENGRAVER_USD - base_lo:+,.0f} | {hi + ENGRAVER_USD - base_hi:+,.0f} |")
    print(f"\nCounted replacements: {len(used)} used-market components, {len(cheap)} cheaper-equivalent components.")

    if "--lines" in sys.argv:
        print("\n| Line | Item | Baseline | Used | Cheaper | Both |")
        print("|---|---|---:|---:|---:|---:|")
        names = list(sc)
        for k, v in lines.items():
            cells = [sc[n][k] for n in names]
            if all(abs(c[0] - cells[0][0]) < 0.005 and abs(c[1] - cells[0][1]) < 0.005 for c in cells):
                continue
            fmt = lambda c: f"{c[0]:,.0f}–{c[1]:,.0f}"
            print(f"| {k} | {v['item'][:48]} | " + " | ".join(fmt(c) for c in cells) + " |")

    # Like-for-like: the CW optics chain at the design's spec. New = the BOM's high end for L1, L3, L5, L6 and C1
    # (IPG quote, Thorlabs expander, SCANLAB basiCube quote, high-power lens, RTC6 estimate; L2 = 0 for the
    # air-cooled IPG). Used = the used picks for the same lines, without the min() rule (a SCANLAB card, not OPAL).
    keymap = {"L1": "L1:laser", "L3": "L3:collimator", "L5": "L5:head", "L6": "L6:lens", "C1": "C1:controller"}
    rows, new_chain, used_lo, used_hi = [], 0.0, 0.0, 0.0
    for ln, key in keymap.items():
        u = used.get(key, {})
        ulo = u.get("low") if u.get("low") is not None else 0.0  # e.g. the laser's own collimator: $0
        uhi = u.get("high") if u.get("high") is not None else ulo
        if u.get("low") is None and ln != "L3":
            ulo = uhi
        rows.append((ln, lines[ln]["high"], ulo, uhi))
        new_chain += lines[ln]["high"]; used_lo += ulo; used_hi += uhi
    print("\nAt spec: the CW optics chain (L1 laser, L3 collimator, L5 scan head, L6 lens, C1 scan card) at the design's"
          " spec, with the cheapest listed option on every other line.\n")
    print("| Build | CW chain (USD) | Machine total (USD) |")
    print("|---|---:|---:|")
    for name, label, chain in (("Baseline, all new (bom.csv)", "All new (IPG quote, SCANLAB quotes)", (new_chain, new_chain)),
                               ("Cheaper same-spec equivalents", "All new chain + cheaper equivalents elsewhere", (new_chain, new_chain)),
                               ("Used majors", "Used CW chain + other used majors", (used_lo, used_hi)),
                               ("Both (used majors + cheaper equivalents)", "Used CW chain + used majors + cheaper equivalents", (used_lo, used_hi))):
        t = sc[name]
        rest = totals(t)[0] - sum(t[k][0] for k in CW_CHAIN if k in t)
        c = f"{chain[0]:,.0f}" if chain[0] == chain[1] else f"{chain[0]:,.0f}–{chain[1]:,.0f}"
        m = f"{rest + chain[0]:,.0f}" if chain[0] == chain[1] else f"{rest + chain[0]:,.0f}–{rest + chain[1]:,.0f}"
        print(f"| {label} | {c} | {m} |")
    if "--at-spec" in sys.argv:
        print("\n| CW chain line | New at spec (BOM high) | Used low pick | Used high pick |")
        print("|---|---:|---:|---:|")
        for ln, n, lo, hi in rows:
            print(f"| {ln} | {n:,.0f} | {lo:,.0f} | {hi:,.0f} |")
        print(f"| **Total** | **{new_chain:,.0f}** | **{used_lo:,.0f}** | **{used_hi:,.0f}** |")

if __name__ == "__main__":
    main()
