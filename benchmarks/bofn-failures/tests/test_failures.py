"""Checks for the failure benchmark (run: python -m pytest tests/ -q; about 2 minutes).

1. The vendored networks are byte-identical to their sources (sha256 from vendor/SOURCES.md).
2. With failures off, a campaign reproduces the source `eifn_reuse` run action for action, on both
   networks (short budget).
3. The failure model: transient rates, input-caused regions, label noise, and that every cell's
   optimum is viable.
4. The strategies' data rules, on a short campaign with failures.

Each network runs in its own subprocess, because both vendored modules are called `bofn_alloy`.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def _py(code: str) -> dict:
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=HERE, check=True)
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_vendor_sha256():
    table = (HERE / "vendor" / "SOURCES.md").read_text()
    rows = re.findall(r"\| `([^`]+)` \| .*? \| `([0-9a-f]{64})` \|", table)
    assert len(rows) == 7
    for rel, sha in rows:
        assert hashlib.sha256((HERE / "vendor" / rel).read_bytes()).hexdigest() == sha, rel


REPRO = """
import json, os, sys, warnings
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(1)
sys.path.insert(0, ".")
from netload import load
net = load({name!r})
if net.family == "al":
    os.environ["BOFN_NO_REC"] = "1"
    ref = net.POL.run("eifn_reuse", 1.0, 3, 20000)
else:
    ref = net.POL.run("eifn_reuse", 1.0, 1.0, 3, 20000)
from policy import run
mine = run(net, "drop", "nofail", 1.0, 3, budget=20000)
a = [[r["spent"], r["best_validated"]] for r in ref["rows"]]
b = [[c["spent"], c["best"]] for c in mine["curve"]]
print(json.dumps(dict(a=a, b=b)))
"""


def _same(a, b):
    return len(a) == len(b) and all(abs(x[0] - y[0]) < 1e-9 and abs(x[1] - y[1]) < 1e-12 for x, y in zip(a, b))


def test_nofail_reproduces_source_al():
    out = _py(REPRO.format(name="al"))
    assert len(out["a"]) > 3 and _same(out["a"], out["b"])


def test_nofail_reproduces_source_cu():
    out = _py(REPRO.format(name="cu-toy"))
    assert len(out["a"]) > 3 and _same(out["a"], out["b"])


def test_failure_model():
    sys.path.insert(0, str(HERE))
    from failmodel import P_TRANSIENT, FailureModel, p_input_ded, p_input_lpbf

    fm = FailureModel("al", "mixed", 0, 1.0)
    outs = [fm.attempt("A", {}) for _ in range(4000)]
    rate = sum(o[0] == "FAILED" for o in outs) / len(outs)
    assert abs(rate - P_TRANSIENT["al"]["A"]) < 0.02
    assert all(o[1] == o[2] for o in outs if o[0] == "FAILED")  # no label noise in "mixed"
    fm = FailureModel("al", "mislabel", 0, 1.0)
    outs = [fm.attempt("L", dict(P=0.3, v=0.1, f=0.7, g=0.38)) for _ in range(4000)]
    fails = [o for o in outs if o[0] == "FAILED"]
    flipped = sum(o[1] != o[2] for o in fails) / len(fails)
    assert abs(flipped - 0.3) < 0.06
    # the aluminum optimum at kappa = 1 prints; the same alloy without Zr cracks and may crash; far below the ridge it can't fuse
    assert p_input_lpbf(0.336, 0.110, 0.70, 0.377, 1.0)[0] < 1e-3
    assert p_input_lpbf(0.336, 0.110, 0.70, 0.0, 1.0)[0] > 0.5
    assert p_input_lpbf(0.10, 0.90, 0.30, 0.0, 1.0)[0] > 0.99
    # copper: pure copper can't be fused at Utah's power cap at low power; Mines at full power can
    assert p_input_ded(0.3, 0.1, 0.0, 0.0, 0.6, 1.0, 0.56, True, 0.5)[0] > 0.95
    assert p_input_ded(0.75, 0.5, 0.0, 0.0, 0.6, 1.0, 0.56, False, 0.5)[0] < 0.05
    # transient-only and no-failure scenarios never produce input-caused failures
    for scen in ("transient", "nofail"):
        fm = FailureModel("cu", scen, 0, 1.0)
        assert all(fm.attempt("M", dict(P=0.3, v=0.1, f=0.0, g=0.0, h=0.6))[1] != "input" for _ in range(200))


def test_optima_viable():
    opt = json.loads((HERE / "optima.json").read_text())
    assert len(opt) == 4
    for cell in opt.values():
        assert cell["viable_opt_pct"] > 99.0
        assert cell["share_within_60pct_viable"] > 0.99


RULES = """
import json, sys, warnings
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(1)
sys.path.insert(0, ".")
from netload import load
import policy as PO
net = load("al")
out = {}
for strategy in PO.STRATEGIES:
    BA, POL = net.BA, net.POL
    truth = net.truth(1.0)
    torch.manual_seed(0)
    d, lab = POL.initial_data(truth, 0)
    fm = PO.FailureModel("al", "mixed", 0, 1.0)
    fl = PO.FailLab(net, truth, d, lab, fm)
    g = torch.Generator().manual_seed(5)
    for k in range(40):  # random designs and reprints, to get failures of every kind
        x = torch.rand(7, generator=g)
        if k % 3 == 2 and d.lots:
            fl.run_reuse(x, int(torch.randint(len(d.lots), (1,), generator=g)))
        else:
            fl.run_new(x)
    v = PO.DataView(fl, strategy)
    blocked = [t for t in fl.trials if t["blocked"] is not None]
    blocked_obs = {(n, i) for t in blocked for r in t["rows"] for n, i in fl.rows[r]["obs"]}
    kept = {(n, i) for n in net.ORDER for i in v.keep[n]}
    out[strategy] = dict(
        n_blocked=len(blocked),
        n_input=sum(t["blocked"]["label"] == "input" for t in blocked),
        blocked_obs=len(blocked_obs), blocked_obs_kept=len(blocked_obs & kept),
        pending=len(v.pending), imputed=sum(len(v.imputed[n][0]) for n in net.ORDER),
        vx_zeros=v.vx[1].count(0.0), vnode_zeros={st: y.count(0.0) for st, (Z, y) in v.vnode.items()},
        n_input_rows={st: sum(1 for r in fl.rows if r["stage"] == st and r["status"] == "FAILED" and r["label"] == "input") for st in ("A", "L")},
    )
print(json.dumps(out))
"""


def test_strategy_rules():
    o = _py(RULES)
    nb, ni = o["drop"]["n_blocked"], o["drop"]["n_input"]
    assert nb > 5 and ni > 2 and o["drop"]["blocked_obs"] > 0
    assert o["drop"]["blocked_obs_kept"] == 0 and o["drop"]["pending"] == 0
    assert o["abandon"]["blocked_obs_kept"] == 0 and o["abandon"]["pending"] == nb
    assert o["partial"]["blocked_obs_kept"] == o["partial"]["blocked_obs"] and o["partial"]["pending"] == nb
    assert o["impute"]["blocked_obs_kept"] == o["impute"]["blocked_obs"] and o["impute"]["pending"] == 0
    assert o["impute"]["imputed"] == sum(o["impute"]["n_input_rows"].values())
    assert o["viab_x"]["blocked_obs_kept"] == 0 and o["viab_x"]["pending"] == ni and o["viab_x"]["vx_zeros"] == ni
    assert o["viab_x_partial"]["blocked_obs_kept"] == o["viab_x_partial"]["blocked_obs"]
    assert o["viab_x_partial"]["pending"] == ni and o["viab_x_partial"]["vx_zeros"] == ni
    assert o["viab_node"]["blocked_obs_kept"] == o["viab_node"]["blocked_obs"] and o["viab_node"]["pending"] == 0
    assert o["viab_node"]["vnode_zeros"] == o["viab_node"]["n_input_rows"]
