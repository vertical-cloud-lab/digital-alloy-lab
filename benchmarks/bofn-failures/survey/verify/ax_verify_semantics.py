#!/usr/bin/env python3
"""Empirically check how Ax (installed 1.3.1; same logic as main for these paths)
treats trial statuses in (a) model training data, (b) pending features,
(c) the X_pending actually passed to the acquisition function, and
(d) the AddExecutionViability transform. Two-"stage" toy: s1 = stage-1
measurement (outcome constraint), y = final objective."""
import logging
import warnings

import numpy as np

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)

import ax
import ax.generators.torch.botorch_modular.acquisition as acq_mod
from ax.adapter.registry import Generators, MBM_X_trans, Y_trans
from ax.adapter.transforms.add_execution_viability import AddExecutionViability
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from ax.core.utils import (
    extract_pending_observations,
    get_pending_observation_features,
    get_pending_observation_features_based_on_trial_status,
)

print("ax version", ax.__version__)
rng = np.random.default_rng(0)

client = Client(random_seed=0)
client.configure_experiment(
    parameters=[
        RangeParameterConfig(name="x1", parameter_type="float", bounds=(0.0, 1.0)),
        RangeParameterConfig(name="x2", parameter_type="float", bounds=(0.0, 1.0)),
    ]
)
client.configure_optimization(objective="y", outcome_constraints=["s1 >= 0.2"])
exp = client._experiment

pts = rng.uniform(size=(14, 2)).round(4)
label = {}


def attach(i):
    idx = client.attach_trial(parameters={"x1": float(pts[i, 0]), "x2": float(pts[i, 1])})
    return idx


for i in range(6):  # fully observed
    t = attach(i)
    client.complete_trial(t, raw_data={"s1": 0.5 + 0.1 * i, "y": 1.0 + i})
    label[t] = "COMPLETED(s1,y)"
t = attach(6)
st = client.complete_trial(t, raw_data={"s1": 0.45})  # stage 2 never measured
label[t] = f"complete_trial(s1 only)->{st.name}"
t = attach(7)
client.attach_data(t, raw_data={"s1": 0.41})
client.mark_trial_failed(t, failed_reason="stage-2 printer jam")
label[t] = "FAILED(after s1 attached)"
t = attach(8)
client.attach_data(t, raw_data={"s1": 0.05})
client.mark_trial_abandoned(t)
label[t] = "ABANDONED(after s1 attached)"
for i in (9, 10, 11):
    t = attach(i)
    client.mark_trial_abandoned(t)
    label[t] = "ABANDONED(no data)"
t = attach(12)
label[t] = "RUNNING(no data)"
t = attach(13)
client.attach_data(t, raw_data={"s1": 0.3})
client.mark_trial_early_stopped(t)
label[t] = "EARLY_STOPPED(s1 only)"

print("\n== trials ==")
for idx, tr in exp.trials.items():
    print(f"  {idx:2d} {tr.status.name:13s} reason={tr.status_reason!r:24s} {label[idx]}")

arm2idx = {}
for idx, tr in exp.trials.items():
    p = tr.arm.parameters
    arm2idx[(round(p["x1"], 4), round(p["x2"], 4))] = idx


def rows_to_idx(X):
    out = []
    for r in X.tolist():
        out.append(arm2idx.get((round(r[0], 4), round(r[1], 4)), "?"))
    return sorted(out, key=str)


print("\n== (b) pending features per metric ==")
for fn in (get_pending_observation_features, get_pending_observation_features_based_on_trial_status):
    pend = fn(experiment=exp) or {}
    print(" ", fn.__name__)
    for m, feats in sorted(pend.items()):
        print(f"    {m}: trials {sorted({f.trial_index for f in feats})}")

captured = {}
orig = acq_mod._get_X_pending_and_observed


def spy(**kw):
    Xp, Xo = orig(**kw)
    captured["X_pending"] = Xp
    captured["outcome_constraints"] = kw.get("outcome_constraints")
    captured["n_outcomes"] = len(kw["Xs"])
    return Xp, Xo


acq_mod._get_X_pending_and_observed = spy


def run(transforms, configs, tag, pending=None):
    captured.clear()
    adapter = Generators.BOTORCH_MODULAR(
        experiment=exp, transforms=transforms, transform_configs=configs
    )
    pend = extract_pending_observations(exp) if pending is None else pending
    adapter.gen(n=1, pending_observations=pend)
    print(f"\n== {tag} ==")
    print("  adapter.outcomes:", adapter.outcomes)
    od = adapter.get_training_data().observation_data["mean"]
    for m in od.columns:
        tri = sorted(set(od[m].dropna().index.get_level_values("trial_index")))
        print(f"  (a) training rows for {m}: trials {tri}")
    try:
        for ds in adapter.generator.surrogate.training_data:
            print(f"  surrogate dataset outcomes={ds.outcome_names} n={ds.X.shape[0]} Y={ds.Y.view(-1).round(decimals=2).tolist() if ds.outcome_names==['execution_viable'] else '...'}")
    except Exception as e:  # noqa
        print("  (could not read surrogate datasets)", type(e).__name__, e)
    Xp = captured.get("X_pending")
    print("  (c) X_pending rows -> trials:", None if Xp is None else rows_to_idx(Xp))
    oc = captured.get("outcome_constraints")
    print("  outcome constraint matrix A:", None if oc is None else oc[0].tolist(), "b:", None if oc is None else oc[1].view(-1).tolist())


run(MBM_X_trans + Y_trans, {}, "default MBM transforms")
VCFG = {"AddExecutionViability": {"feasibility_threshold": 0.8, "min_abandoned_trials": 3}}
try:
    run(MBM_X_trans + Y_trans + [AddExecutionViability], VCFG,
        "MBM + AddExecutionViability (appended after Y transforms), no metric registered")
except Exception as e:
    print("\n== MBM + AddExecutionViability, no metric registered ==\n  ERROR:", type(e).__name__, e)

from ax.core.metric import Metric
exp.add_tracking_metric(Metric(name="execution_viable"))
for tag, tlist in [
    ("after Y transforms", MBM_X_trans + Y_trans + [AddExecutionViability]),
    ("before Y transforms", MBM_X_trans + [AddExecutionViability] + Y_trans),
]:
    try:
        run(tlist, VCFG, f"WORKAROUND (tracking metric 'execution_viable' registered), viability {tag}")
    except Exception as e:
        print(f"\n== WORKAROUND viability {tag} ==\n  ERROR:", type(e).__name__, str(e)[:300])

# (e) legacy AxClient: complete_trial with a missing opt-config metric
from ax.service.ax_client import AxClient, ObjectiveProperties

axc = AxClient(verbose_logging=False)
axc.create_experiment(
    parameters=[{"name": "x1", "type": "range", "bounds": [0.0, 1.0]}],
    objectives={"y": ObjectiveProperties(minimize=False)},
    outcome_constraints=["s1 >= 0.2"],
)
_, ti = axc.attach_trial(parameters={"x1": 0.3})
axc.complete_trial(ti, raw_data={"s1": (0.5, 0.0)})
print("\n== (e) legacy AxClient.complete_trial with s1 only ->", axc.experiment.trials[ti].status.name)

# (f) X_pending under the fast path used when >=100 single-arm trials
fast = get_pending_observation_features_based_on_trial_status(experiment=exp)
run(MBM_X_trans + Y_trans, {}, "default MBM transforms, fast-path pending (>=100-trial branch)", pending=fast)
