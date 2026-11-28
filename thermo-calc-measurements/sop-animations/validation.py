"""One table of how well each instrument model is checked (#262, PR #263).

    python validation.py            # -> out/validation.json and out/validation.md

For every model the SOP videos use: the maker's published W x D x H against the model's own bounding box, and, where
it was registered to reference frames (fit.py; refs/<key>/fit.json), the RMS pixel error of every view before and
after the fit, and of any view held out of it. Also each SOP video's collision audit (out/collisions/).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

# which models each SOP uses (the scripts may use more; this is for the table's order)
ORDER = ["dsc_sta", "microbalance", "riffle_splitter", "lpbf_chamber", "precision_saw", "mount_press", "polisher",
         "fumehood", "vhx", "sem", "density_balance", "ultrasonic_bath", "drying_oven", "he_pycnometer", "furnace",
         "quench_tank", "hardness", "eddy_meter", "laser_flash", "aging_rack", "icp_oes", "onh_analyzer",
         "microwave_digester", "heat_sealer"]
REUSED = {"mount_press": "byu-vcl (LECO MX400, from the lab's own video)",
          "polisher": "byu-vcl (LECO PX500, fitted to the lab's SOP videos)",
          "fumehood": "byu-vcl (Labconco XStream)", "vhx": "byu-vcl (Keyence VHX-7000, fitted)",
          "sem": "byu-vcl (Hitachi TM4000PlusII, fitted)", "furnace": "byu-vcl (Nabertherm NAT 15/65, fitted)",
          "quench_tank": "byu-vcl (our design)", "hardness": "byu-vcl (Mitutoyo HM-220, catalogue)"}
VL_FITS = Path("/tmp/byu-vcl/vertical-lab/refs")      # byu-vcl's own fits of the reused models, when cloned


def _fit_rows(fit: dict) -> list[dict]:
    rows = []
    for name, v in fit.get("views", {}).items():
        rows.append(dict(view=name, holdout=bool(v.get("holdout")), before=v.get("rms_px_camera_only"),
                         after=v.get("rms_px"), picks=len(v.get("residual_px", {}))))
    return rows


def main() -> None:
    import stage
    keys = [k for k in ORDER]
    for f in sorted(HERE.glob("models_*.py")):
        import importlib
        mod = importlib.import_module(f.stem)
        keys += [k for k in getattr(mod, "REGISTRY", {}) if k not in keys]
    table = []
    for key in keys:
        try:
            inst, _ = stage.get(key)
        except KeyError:
            continue
        except Exception as e:                       # noqa: BLE001
            table.append(dict(key=key, error=f"{type(e).__name__}: {e}"))
            continue
        x0, x1, y0, y1, z0, z1 = inst.bbox()
        row = dict(key=key, model=inst.model, title=inst.title, published_mm=[round(v) for v in inst.size],
                   model_mm=[round(x1 - x0), round(y1 - y0), round(z1 - z0)], source=inst.source,
                   origin=REUSED.get(key, "this PR"))
        fp = HERE / "refs" / key / "fit.json"
        if not fp.exists() and key in REUSED and (VL_FITS / key / "fit.json").exists():
            fp = VL_FITS / key / "fit.json"
            row["fit_from"] = "byu-vcl"
        if fp.exists():
            row["fit"] = _fit_rows(json.loads(fp.read_text()))
        table.append(row)
    audits = {}
    for p in sorted((OUT / "collisions").glob("sop0*.json")):
        d = json.loads(p.read_text())
        audits[p.stem] = dict(frames_in_collision=d["frames_in_collision"], pairs=len(d["pairs"]),
                              every=d["checked_every"])
    OUT.mkdir(exist_ok=True)
    (OUT / "validation.json").write_text(json.dumps(dict(models=table, audits=audits), indent=1) + "\n")
    md = ["| Model | Key | Published W × D × H (mm) | Model (mm) | Registration: RMS px before → after (held out) | From |",
          "|---|---|---|---|---|---|"]
    for r in table:
        if "error" in r:
            md.append(f"| ? | `{r['key']}` | | | build failed: {r['error'][:80]} | |")
            continue
        fit = r.get("fit")
        if fit:
            parts = []
            for v in fit:
                s = f"{v['before']} → {v['after']}" if not v["holdout"] else f"held out: {v['after']}"
                parts.append(s)
            fits = "; ".join(parts) + (" (byu-vcl's fit)" if r.get("fit_from") else "")
        else:
            fits = "not registered"
        pw = " × ".join(str(v) for v in r["published_mm"])
        mw = " × ".join(str(v) for v in r["model_mm"])
        md.append(f"| {r['model']} | `{r['key']}` | {pw} | {mw} | {fits} | {r['origin']} |")
    if audits:
        md += ["", "| Chapter | Frames with a collision deeper than 1.5 mm | Pairs | Checked every |", "|---|---|---|---|"]
        for k, a in audits.items():
            md.append(f"| `{k}` | {a['frames_in_collision']} | {a['pairs']} | {a['every']} frames |")
    (OUT / "validation.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    sys.exit(main())
