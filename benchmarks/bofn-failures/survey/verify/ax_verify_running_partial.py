#!/usr/bin/env python3
"""RUNNING trial with only stage-1 data attached: is it in X_pending? Can a COMPLETED
trial be re-labelled ABANDONED/FAILED via the public Client API?"""
import logging
import warnings

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)

import ax.generators.torch.botorch_modular.acquisition as acq_mod
from ax.adapter.registry import Generators
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from ax.core.utils import extract_pending_observations

client = Client(random_seed=1)
client.configure_experiment(
    parameters=[
        RangeParameterConfig(name="x1", parameter_type="float", bounds=(0.0, 1.0)),
        RangeParameterConfig(name="x2", parameter_type="float", bounds=(0.0, 1.0)),
    ]
)
client.configure_optimization(objective="y", outcome_constraints=["s1 >= 0.2"])
exp = client._experiment
pts = [(0.1, 0.2), (0.3, 0.9), (0.5, 0.5), (0.7, 0.1), (0.9, 0.8), (0.2, 0.6)]
for i, (a, b) in enumerate(pts[:5]):
    t = client.attach_trial(parameters={"x1": a, "x2": b})
    client.complete_trial(t, raw_data={"s1": 0.5 + 0.1 * i, "y": float(i)})
t_run = client.attach_trial(parameters={"x1": pts[5][0], "x2": pts[5][1]})
client.attach_data(t_run, raw_data={"s1": 0.33})  # stage 1 done, stage 2 in progress

cap = {}
orig = acq_mod._get_X_pending_and_observed


def spy(**kw):
    Xp, Xo = orig(**kw)
    cap["Xp"] = Xp
    return Xp, Xo


acq_mod._get_X_pending_and_observed = spy
pend = extract_pending_observations(exp)
print("pending per metric:", {m: sorted({f.trial_index for f in v}) for m, v in (pend or {}).items()})
Generators.BOTORCH_MODULAR(experiment=exp).gen(n=1, pending_observations=pend)
print("RUNNING trial", t_run, "status", exp.trials[t_run].status.name, "-> X_pending:", cap["Xp"])
ad = Generators.BOTORCH_MODULAR(experiment=exp)
od = ad.get_training_data().observation_data["mean"]
print("s1 training trials:", sorted(set(od["s1"].dropna().index.get_level_values("trial_index"))))

for meth in ("mark_trial_abandoned", "mark_trial_failed"):
    try:
        getattr(client, meth)(0)
        print(meth, "on COMPLETED trial 0 ->", exp.trials[0].status.name)
    except Exception as e:
        print(meth, "on COMPLETED trial 0 -> ERROR", type(e).__name__, str(e)[:120])
