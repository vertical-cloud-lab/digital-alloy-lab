import logging, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.WARNING)
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from ax.core.utils import compute_metric_availability
c = Client(random_seed=0)
c.configure_experiment(parameters=[RangeParameterConfig(name="x1", parameter_type="float", bounds=(0.0, 1.0))])
c.configure_optimization(objective="y", outcome_constraints=["s1 >= 0.2"])
a = c.attach_trial(parameters={"x1": 0.3})
c.attach_data(a, {"s1": 0.4})
c.mark_trial_failed(a, failed_reason="stage2: printer jam")
b = c.attach_trial(parameters={"x1": 0.3})
c.complete_trial(b, {"s1": 0.4, "y": 1.2})
e = c._experiment
print("trial", a, e.trials[a].status.name, e.trials[a].arm.name, "| retry", b, e.trials[b].status.name, e.trials[b].arm.name)
print("availability:", {k: v.name for k, v in compute_metric_availability(e).items()})
print("dedup set excludes FAILED arm only if not reused:", sorted(e.arms_by_signature_for_deduplication.keys())[:3])
