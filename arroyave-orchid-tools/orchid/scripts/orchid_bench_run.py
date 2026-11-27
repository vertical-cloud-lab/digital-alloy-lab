#!/usr/bin/env python3
"""Driver for orchid-bench (ORCHID synthetic-papers extraction benchmark), offline, no LLM calls.

Run (through the scrubbed-environment wrapper) as:
    /tmp/sbx/clean /tmp/arroyave/venvs/orchid-bench/bin/python -I orchid_bench_run.py <step> [...]

Steps (each writes a JSON summary under /tmp/arroyave/results/orchid/data/):
  rescore   re-run bench/score.py on every shipped bench/outputs/<extractor>/ and compare with the shipped scores.json
  oracle    run baselines/oracle.py (truth written as extractor output), compare its files with the shipped ones,
            score it and list every aggregate ratio metric that is not 1.0
  baselines run the deterministic baselines that need neither the private orchid-pipeline nor Tesseract
            (text_regex, tables_pdfplumber), compare outputs with the shipped ones and re-score
  generate  regenerate the 20 synthetic papers (generate.py, cache already filled) and compare every docs/ and truth/
            file byte-for-byte (sha256) with the shipped files
  results   rebuild results/RESULTS.md + results.json from the shipped scores and diff them against the shipped copies
The shipped repository is SRC (read-only); every step writes only in WORK (a copy) or OUTDIR.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SRC = Path("/tmp/arroyave/src/orchid-calphad__orchid-bench")
WORK = Path("/tmp/arroyave/work/orchid-bench")
PY = "/tmp/arroyave/venvs/orchid-bench/bin/python"
OUTDIR = Path("/tmp/arroyave/results/orchid/data")
SCRATCH = Path("/tmp/arroyave/work/bench_scratch")
ENV = dict(os.environ)
ENV.update({
    "ORCHID_TDB_DIR": "/tmp/arroyave/src/orchid-calphad__orchid-project.org/data/databases/sgte-binary",
    "ORCHID_PD_DIR": "/tmp/arroyave/src/orchid-calphad__orchid-data/phase-diagrams/sgte",
    "OPEN_TDB": "/tmp/arroyave/src/orchid-calphad__orchid-project.org/data/databases",
    "ORCHID_PIPELINE": "/nonexistent/orchid-pipeline",   # private; deliberately absent
    "OMP_NUM_THREADS": "1", "MPLBACKEND": "Agg",
})


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(cmd, cwd=WORK, timeout=900):
    t0 = time.time()
    r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    return r, time.time() - t0


def leaves(o, prefix=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{prefix}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{prefix}[{i}]")
    else:
        yield prefix, o


def diff_json(a, b):
    la, lb = dict(leaves(a)), dict(leaves(b))
    keys = set(la) | set(lb)
    nd, maxd = 0, 0.0
    ex = []
    for k in sorted(keys):
        x, y = la.get(k, "<missing>"), lb.get(k, "<missing>")
        if x == y:
            continue
        nd += 1
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            maxd = max(maxd, abs(float(x) - float(y)))
        if len(ex) < 8:
            ex.append([k, x, y])
    return nd, maxd, ex


def step_rescore():
    out = SCRATCH / "rescore"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for d in sorted((SRC / "bench" / "outputs").iterdir()):
        shipped = d / "scores.json"
        if not shipped.exists():
            continue
        n = sum(1 for _ in d.glob("*/*.json"))
        r, dt = run([PY, "bench/score.py", "--outputs", str(d), "--out", str(out / f"{d.name}.json")], timeout=600)
        row = {"extractor": d.name, "n_output_files": n, "exit": r.returncode, "seconds": round(dt, 2)}
        if r.returncode == 0:
            new = out / f"{d.name}.json"
            row["byte_identical"] = sha(new) == sha(shipped)
            nd, maxd, ex = diff_json(json.loads(shipped.read_text()), json.loads(new.read_text()))
            row.update({"n_differing_leaves": nd, "max_abs_numeric_diff": maxd, "examples": ex})
        else:
            row["stderr_tail"] = r.stderr[-600:]
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "examples"}), flush=True)
    (OUTDIR / "orchid-bench-rescore.json").write_text(json.dumps(rows, indent=1) + "\n")


def step_oracle():
    r, dt = run([PY, "bench/baselines/oracle.py"])
    res = {"oracle_exit": r.returncode, "oracle_seconds": round(dt, 2), "stderr_tail": r.stderr[-600:]}
    new_dir, old_dir = WORK / "bench/outputs/oracle", SRC / "bench/outputs/oracle"
    files = sorted(p.relative_to(old_dir) for p in old_dir.glob("*/*.json"))
    same = [f for f in files if (new_dir / f).exists() and sha(new_dir / f) == sha(old_dir / f)]
    res.update({"oracle_files_shipped": len(files), "oracle_files_identical": len(same)})
    r2, dt2 = run([PY, "bench/score.py", "--outputs", str(new_dir), "--out", str(SCRATCH / "oracle_scores.json")])
    res.update({"score_exit": r2.returncode, "score_seconds": round(dt2, 2)})
    if r2.returncode == 0:
        agg = json.loads((SCRATCH / "oracle_scores.json").read_text())["aggregate"]
        ratio_words = ("recall", "precision", "exact", "accuracy", "acc", "within", "match")
        not_one = []
        n_ratio = 0
        for k, v in leaves(agg):
            leaf = k.rsplit("/", 1)[-1].lower()
            if isinstance(v, (int, float)) and not isinstance(v, bool) and any(w in leaf for w in ratio_words) \
                    and "err" not in leaf and not leaf.startswith("n_"):
                n_ratio += 1
                if abs(v - 1.0) > 1e-12:
                    not_one.append([k, v])
        res.update({"n_ratio_metrics": n_ratio, "ratio_metrics_not_1": not_one[:60], "n_not_1": len(not_one)})
        nd, maxd, ex = diff_json(json.loads((old_dir / "scores.json").read_text()),
                                 json.loads((SCRATCH / "oracle_scores.json").read_text()))
        res.update({"vs_shipped_scores_differing_leaves": nd, "vs_shipped_max_abs_diff": maxd, "examples": ex})
    (OUTDIR / "orchid-bench-oracle.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("ratio_metrics_not_1", "examples")}), flush=True)


def step_baselines():
    res = {}
    import shutil
    for name, ext in (("text_regex.py", "text_regex"), ("tables_pdfplumber.py", "tables_pdfplumber")):
        shutil.rmtree(WORK / "bench/outputs" / ext, ignore_errors=True)   # so "identical" means regenerated
        r, dt = run([PY, f"bench/baselines/{name}"], timeout=900)
        row = {"exit": r.returncode, "seconds": round(dt, 2), "stderr_tail": r.stderr[-1200:]}
        new_dir, old_dir = WORK / "bench/outputs" / ext, SRC / "bench/outputs" / ext
        per_r = {}
        for f in sorted(old_dir.glob("*/*.json")):
            rel = f.relative_to(old_dir)
            g = new_dir / rel
            k = rel.parts[0]
            per_r.setdefault(k, [0, 0])
            per_r[k][0] += 1
            if g.exists() and sha(g) == sha(f):
                per_r[k][1] += 1
        row["identical_files_by_rendering"] = {k: f"{v[1]}/{v[0]}" for k, v in per_r.items()}
        if r.returncode == 0:
            r2, dt2 = run([PY, "bench/score.py", "--outputs", str(new_dir), "--out", str(SCRATCH / f"{ext}_rerun.json")])
            if r2.returncode == 0:
                nd, maxd, ex = diff_json(json.loads((old_dir / "scores.json").read_text()),
                                         json.loads((SCRATCH / f"{ext}_rerun.json").read_text()))
                row.update({"rescore_vs_shipped_differing_leaves": nd, "max_abs_diff": maxd, "examples": ex})
        res[ext] = row
        shutil.rmtree(new_dir, ignore_errors=True)        # restore the shipped outputs (incl. scores.json) for later steps
        shutil.copytree(old_dir, new_dir)
        print(ext, json.dumps({k: v for k, v in row.items() if k != "examples"}, ensure_ascii=False)[:1500], flush=True)
    (OUTDIR / "orchid-bench-baselines.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")


def step_generate(jobs="2", systems=None):
    cmd = [PY, "bench/generate.py", "--jobs", jobs] + (["--systems", *systems] if systems else [])
    r, dt = run(cmd, timeout=1500)
    res = {"cmd": " ".join(cmd[1:]), "exit": r.returncode, "seconds": round(dt, 1),
           "stdout_tail": r.stdout[-1500:], "stderr_tail": r.stderr[-2500:]}
    by_kind = {}
    mism = []
    for f in sorted(list((SRC / "bench/docs").rglob("*")) + list((SRC / "bench/truth").glob("*.json"))):
        if not f.is_file():
            continue
        rel = f.relative_to(SRC / "bench")
        kind = rel.parts[0] if rel.parts[0] == "truth" else (rel.parts[2] if len(rel.parts) > 3 else rel.name)
        g = WORK / "bench" / rel
        by_kind.setdefault(kind, [0, 0])
        by_kind[kind][0] += 1
        if g.exists() and sha(g) == sha(f):
            by_kind[kind][1] += 1
        else:
            mism.append(str(rel))
    res["identical_by_kind"] = {k: f"{v[1]}/{v[0]}" for k, v in sorted(by_kind.items())}
    res["mismatched_examples"] = mism[:40]
    res["n_mismatched"] = len(mism)
    (OUTDIR / "orchid-bench-generate.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "mismatched_examples"}, ensure_ascii=False, indent=1), flush=True)


def step_provenance():
    """Check the SGTE TDB and ORCHID diagram SHA-256 recorded in every truth key against local copies."""
    rows = []
    for tf in sorted((SRC / "bench/truth").glob("*.json")):
        t = json.loads(tf.read_text())
        st = t["source_tdb"]
        tdb = Path(ENV["ORCHID_TDB_DIR"]) / st["file"]
        row = {"doc": t["doc_id"], "tdb": st["file"], "tdb_present": tdb.exists(),
               "tdb_sha_match": tdb.exists() and sha(tdb) == st["sha256"]}
        ds = t.get("diagram_source") or {}
        f = ds.get("file") or ds.get("path") or ""
        pdj = Path(ENV["ORCHID_PD_DIR"]) / Path(f).name if f else None
        if pdj is not None:
            row.update({"diagram": Path(f).name, "diagram_present": pdj.exists(),
                        "diagram_sha_match": pdj.exists() and sha(pdj) == ds.get("sha256")})
        rows.append(row)
    (OUTDIR / "orchid-bench-provenance.json").write_text(json.dumps(rows, indent=1) + "\n")
    print(json.dumps(rows, indent=0)[:4000], flush=True)


def step_results(with_ledger=False):
    """build_results.py reads the Gemini ledger from work/ai/ (git-ignored); the repo ships it as results/."""
    import shutil
    led = WORK / "bench/work/ai/gemini_ledger.jsonl"
    if with_ledger:
        led.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / "bench/results/gemini_ledger.jsonl", led)
    elif led.exists():
        led.unlink()
    r, dt = run([PY, "bench/results/build_results.py"])
    res = {"ledger_copied_to_work_ai": with_ledger, "exit": r.returncode, "seconds": round(dt, 2),
           "stderr_tail": r.stderr[-1500:]}
    for f in ("results/RESULTS.md", "results/results.json"):
        a, b = SRC / "bench" / f, WORK / "bench" / f
        res[f] = "identical" if b.exists() and sha(a) == sha(b) else "differs"
    tag = "with-ledger" if with_ledger else "fresh-clone"
    (OUTDIR / f"orchid-bench-results-rebuild-{tag}.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1), flush=True)


if __name__ == "__main__":
    SCRATCH.mkdir(parents=True, exist_ok=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    step = sys.argv[1]
    if step == "generate":
        step_generate(*(sys.argv[2:3] or ["2"]), systems=sys.argv[3:] or None)
    else:
        {"rescore": step_rescore, "oracle": step_oracle, "baselines": step_baselines, "results": step_results,
         "results-ledger": lambda: step_results(True), "provenance": step_provenance}[step]()
