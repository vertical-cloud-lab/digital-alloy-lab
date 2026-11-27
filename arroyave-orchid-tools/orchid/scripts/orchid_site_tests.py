#!/usr/bin/env python3
"""Run every orchid-project.org release-tool test file (tools/tests/test_*.py) offline, one at a time.

The suite mixes pytest files (def test_*) and stand-alone scripts that print PASS/FAIL lines and read the release
from ORCHID_DATA / ~/projects/orchid-data. Each file runs with a per-file timeout; files with test functions run
under pytest, the others as scripts. HOME is a sandbox whose ~/projects/{orchid-data,open-tdb,...} are symlinks to the
local checkouts (orchid-data and the site's data/ are read-only inputs; the site tests run in a copy).

    HOME=/tmp/arroyave/work/site_home /tmp/sbx/clean /tmp/arroyave/venvs/orchid-site/bin/python -I orchid_site_tests.py [ci]
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SITE = Path(os.environ.get("ORCHID_SITE_DIR", "/tmp/arroyave/work/orchid-project.org"))
PY = "/tmp/arroyave/venvs/orchid-site/bin/python"
DATA = "/tmp/arroyave/src/orchid-calphad__orchid-data"
OUT = Path("/tmp/arroyave/results/orchid/data/orchid-project.org-tests.json")
LOGDIR = Path("/tmp/arroyave/work/site_test_logs")
ENV = dict(os.environ)
ENV.update({"ORCHID_DATA": DATA, "ORCHID_LITERATURE": f"{DATA}/literature/orchid-literature.jsonl.gz",
            "ORCHID_PARITY": f"{DATA}/literature/dft_parity.json",
            "OPEN_TDB": "/tmp/arroyave/src/orchid-calphad__orchid-project.org/data",
            "ORCHID_EXAMPLES": "/tmp/arroyave/src/orchid-calphad__orchid-examples",
            "ORCHID_EVAL_WORKERS": "1", "OMP_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg"})


def main():
    LOGDIR.mkdir(parents=True, exist_ok=True)
    ci = sys.argv[1:2] == ["ci"]
    only = [a for a in sys.argv[1:] if a.startswith("test_")]
    files = [SITE / "tools/tests/test_report_links.py"] if ci else sorted((SITE / "tools/tests").glob("test_*.py"))
    if only:
        files = [SITE / "tools/tests" / a for a in only]
    rows = []
    for f in files:
        src = f.read_text(encoding="utf-8")
        is_pytest = bool(re.search(r"^\s*def test_", src, re.M))
        cmd = ([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(f.relative_to(SITE))] if is_pytest
               else [PY, str(f.relative_to(SITE))])
        t0 = time.time()
        try:
            r = subprocess.run(cmd, cwd=SITE, env=ENV, capture_output=True, text=True, timeout=240)
            rc, so, se = r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired as e:
            rc, so, se = "timeout", (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), ""
        dt = time.time() - t0
        (LOGDIR / f"{f.stem}.log").write_text(f"$ {' '.join(cmd)}\n{so}\n--- stderr ---\n{se}", encoding="utf-8")
        text = so + "\n" + se
        n_pass = len(re.findall(r"^(PASS|ok)\b", so, re.M))
        n_fail = len(re.findall(r"^FAIL\b", so, re.M))
        m = re.search(r"(\d+) passed", so)
        summ = re.findall(r"^=*\s*(\d+ (?:passed|failed|error)[^\n]*)", so, re.M)
        err = [ln for ln in text.splitlines() if re.search(r"(Error|Exception|FAIL|failed|Traceback)", ln)]
        rows.append({"file": f.name, "runner": "pytest" if is_pytest else "script", "exit": rc,
                     "seconds": round(dt, 1), "pytest_summary": summ[-1] if summ else None,
                     "script_PASS_lines": n_pass, "script_FAIL_lines": n_fail,
                     "first_error_lines": err[:4], "last_stdout": so.strip().splitlines()[-1:] if so.strip() else []})
        print(json.dumps(rows[-1], ensure_ascii=False)[:700], flush=True)
    out = OUT.with_name(OUT.stem + ("-ci" if ci else "-siblings" if only else "") + ".json")
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
