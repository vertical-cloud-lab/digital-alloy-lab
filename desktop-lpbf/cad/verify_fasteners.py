"""Check every part in fasteners.CATALOG against McMaster-Carr's own CAD, by volume and bounding box.

McMaster's files are not committed (they are McMaster's copyrighted content). Fetch them through the lab Pi into
/tmp/mcm_cad as <PN>_full.STEP ("3-D STEP", helical threads) and <PN>_simple.STEP ("3-D STEP simplified", plain
shanks); fastener-cad-manifest.csv lists the files used here with their sha256. Parts whose files are absent are
reported as not checked.

    python desktop-lpbf/cad/verify_fasteners.py            # -> cad/out/fastener-check.md and .json
    python desktop-lpbf/cad/verify_fasteners.py --manifest /tmp/work/cadlog*.jsonl   # also rewrite the manifest

Light shapes (detail=False) are compared with McMaster's simplified model; detailed shapes (detail=True: threads as
revolved rings, inserts as coils) with the full model. Bounding boxes are compared as sorted extents.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fasteners as F  # noqa: E402

CAD = pathlib.Path("/tmp/mcm_cad")
OUT = HERE / "out"


def load(path):
    vals = cq.importers.importStep(str(path)).vals()
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)


def ext(s):
    b = s.BoundingBox()
    return sorted([round(b.xlen, 3), round(b.ylen, 3), round(b.zlen, 3)])


def pct(a, b):
    return None if (a is None or b is None) else 100.0 * (a - b) / b


def check(pn):
    c = F.CATALOG[pn]
    row = dict(pn=pn, kind=c["kind"], desc=c["desc"], price_usd=c["price_usd"], sold_as=c["sold_as"], url=c["url"])
    full, simple = CAD / f"{pn}_full.STEP", CAD / f"{pn}_simple.STEP"
    light, det = F.shape(pn, False), F.shape(pn, True)
    row["ours_light_mm3"], row["ours_detail_mm3"] = light.Volume(), det.Volume()
    row["ours_light_ext"], row["ours_detail_ext"] = ext(light), ext(det)
    row["mcm_full_mm3"] = row["mcm_simple_mm3"] = None
    if simple.exists():
        m = load(simple)
        row["mcm_simple_mm3"], row["mcm_simple_ext"] = m.Volume(), ext(m)
    if full.exists():
        m = load(full)
        row["mcm_full_mm3"], row["mcm_full_ext"] = m.Volume(), ext(m)
    row["light_vs_simple_pct"] = pct(row["ours_light_mm3"], row["mcm_simple_mm3"])
    row["detail_vs_full_pct"] = pct(row["ours_detail_mm3"], row["mcm_full_mm3"])
    if row.get("mcm_simple_ext"):
        row["light_ext_ok"] = all(abs(a - b) < 0.01 for a, b in zip(row["ours_light_ext"], row["mcm_simple_ext"]))
    if row.get("mcm_full_ext"):
        row["detail_ext_maxdiff_mm"] = max(abs(a - b) for a, b in zip(row["ours_detail_ext"], row["mcm_full_ext"]))
    row["mass_g"] = F.mass_g(pn)
    return row


def write_manifest(logs):
    rows = []
    for lg in logs:
        for line in pathlib.Path(lg).read_text().splitlines():
            r = json.loads(line)
            for f in r.get("files", []):
                if f.get("file"):
                    rows.append(["McMaster-Carr", r["pn"], f["fmt"], f["suggested"], f["bytes"], f["sha256"], f["url"], f["utc"]])
    seen, out = set(), []
    for r in rows:                       # keep the last download of each (pn, format)
        seen.discard((r[1], r[2]))
    for r in reversed(rows):
        if (r[1], r[2]) not in seen:
            seen.add((r[1], r[2]))
            out.append(r)
    out.sort(key=lambda r: (r[1], r[2]))
    with open(HERE / "fastener-cad-manifest.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["vendor", "part_number", "kind", "file", "bytes", "sha256", "source_url", "fetched_utc"])
        w.writerows(out)
    print("manifest rows:", len(out))


def main():
    if "--manifest" in sys.argv:
        write_manifest(sys.argv[sys.argv.index("--manifest") + 1:])
    OUT.mkdir(exist_ok=True)
    rows = []
    for pn in F.CATALOG:
        try:
            r = check(pn)
        except Exception as e:  # report and carry on
            r = dict(pn=pn, kind=F.CATALOG[pn]["kind"], desc=F.CATALOG[pn]["desc"], error=f"{type(e).__name__}: {e}")
        rows.append(r)
        print(pn, r.get("light_vs_simple_pct"), r.get("detail_vs_full_pct"), r.get("error", ""), flush=True)
    (OUT / "fastener-check.json").write_text(json.dumps(rows, indent=1, default=float))

    def f(x, n=4):
        return "–" if x is None else f"{x:.{n}f}"

    lines = ["# Fasteners: our CadQuery parts against McMaster-Carr's CAD", "",
             "Written by [`verify_fasteners.py`](../verify_fasteners.py). Volumes in mm³. *Light* is the shape used in the",
             "model (plain shank at the major diameter), compared with McMaster's \"3-D STEP simplified\". *Detailed* adds the",
             "thread as revolved rings with McMaster's axial profile (same volume per length as a helix), compared with",
             "McMaster's full \"3-D STEP\". Helical inserts: light is the installed envelope (not comparable, so no figure);",
             "detailed is the coil without its prong, against McMaster's coil *with* its prong, so it reads low by the prong.",
             "McMaster's files are not committed; [`../fastener-cad-manifest.csv`](../fastener-cad-manifest.csv) lists them.", "",
             "| Part | Kind | Description | Price | McMaster simplified | Ours, light | Δ light | McMaster full | Ours, detailed | Δ detailed | Extents match (light) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if "error" in r:
            lines.append(f"| [{r['pn']}](https://www.mcmaster.com/{r['pn']}/) | {r['kind']} | {r['desc']} | | error: {r['error']} | | | | | | |")
            continue
        lv = "–" if r["kind"] == "insert" else f(r["ours_light_mm3"], 3)
        dl = "–" if r["kind"] == "insert" else (f(r["light_vs_simple_pct"], 4) + " %" if r["light_vs_simple_pct"] is not None else "–")
        dd = (f(r["detail_vs_full_pct"], 3) + " %") if r["detail_vs_full_pct"] is not None else "–"
        ok = {True: "yes", False: "**no**", None: "–"}[r.get("light_ext_ok")]
        lines.append(f"| [{r['pn']}]({r['url']}) | {r['kind']} | {r['desc']} | ${r['price_usd']:.2f} / {r['sold_as']} | "
                     f"{f(r['mcm_simple_mm3'], 3)} | {lv} | {dl} | {f(r['mcm_full_mm3'], 3)} | {f(r['ours_detail_mm3'], 3)} | {dd} | {ok} |")
    (OUT / "fastener-check.md").write_text("\n".join(lines) + "\n")
    print("wrote", OUT / "fastener-check.md")


if __name__ == "__main__":
    main()
