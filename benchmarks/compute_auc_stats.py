"""Compute AUC statistics from warmstart results JSON."""

import json
import numpy as np
from scipy.stats import ttest_ind

with open("benchmarks/llm_warmstart_results.json") as f:
    data = json.load(f)


def get_aucs(results):
    return [sum(r["cumulative_best"]) for r in results]


def get_cold_starts(results):
    return [r["cumulative_best"][0] for r in results]


def get_iters_to_threshold(results, threshold=2.0):
    iters = []
    for r in results:
        found = False
        for i, v in enumerate(r["cumulative_best"]):
            if v >= threshold:
                iters.append(i)
                found = True
                break
        if not found:
            iters.append(len(r["cumulative_best"]))
    return iters


llm_aucs = np.array(get_aucs(data["llm_results"]))
rand_aucs = np.array(get_aucs(data["random_results"]))
lhs_aucs = np.array(get_aucs(data["lhs_results"]))

print(f"LLM AUC: mean={np.mean(llm_aucs):.2f}, std={np.std(llm_aucs, ddof=1):.2f}")
print(f"Random AUC: mean={np.mean(rand_aucs):.2f}, std={np.std(rand_aucs, ddof=1):.2f}")
print(f"LHS AUC: mean={np.mean(lhs_aucs):.2f}, std={np.std(lhs_aucs, ddof=1):.2f}")

pooled = np.sqrt(
    (
        (len(llm_aucs) - 1) * np.std(llm_aucs, ddof=1) ** 2
        + (len(rand_aucs) - 1) * np.std(rand_aucs, ddof=1) ** 2
    )
    / (len(llm_aucs) + len(rand_aucs) - 2)
)
d = (np.mean(llm_aucs) - np.mean(rand_aucs)) / pooled
t, p = ttest_ind(llm_aucs, rand_aucs)
pct = (np.mean(llm_aucs) - np.mean(rand_aucs)) / np.mean(rand_aucs) * 100
print(f"AUC: d={d:.2f}, t={t:.2f}, p={p:.6f}, +{pct:.1f}%")

llm_cold = np.array(get_cold_starts(data["llm_results"]))
rand_cold = np.array(get_cold_starts(data["random_results"]))
pooled_cold = np.sqrt(
    (
        (len(llm_cold) - 1) * np.std(llm_cold, ddof=1) ** 2
        + (len(rand_cold) - 1) * np.std(rand_cold, ddof=1) ** 2
    )
    / (len(llm_cold) + len(rand_cold) - 2)
)
d_cold = (np.mean(llm_cold) - np.mean(rand_cold)) / pooled_cold
t_cold, p_cold = ttest_ind(llm_cold, rand_cold)
print(
    f"Cold-start: LLM={np.mean(llm_cold):.3f}, Random={np.mean(rand_cold):.3f}, diff={np.mean(llm_cold)-np.mean(rand_cold):.3f}, d={d_cold:.2f}, p={p_cold:.6f}"
)

llm_iters = get_iters_to_threshold(data["llm_results"])
rand_iters = get_iters_to_threshold(data["random_results"])
lhs_iters = get_iters_to_threshold(data["lhs_results"])
print(
    f"Iters>=2.0: LLM={np.mean(llm_iters):.1f}, Random={np.mean(rand_iters):.1f}, LHS={np.mean(lhs_iters):.1f}"
)

n = len(data["llm_results"])
wins = sum(
    1
    for l, r in zip(data["llm_results"], data["random_results"])
    if l["final_best"] > r["final_best"]
)
print(f"Win rate: {wins}/{n}")


def phase_quality(results, threshold=0.5):
    fracs = []
    for r in results:
        fracs.extend(r["initial_phase_fractions"])
    return sum(1 for x in fracs if x > threshold) / len(fracs) * 100


print(
    f"Init quality>0.5: LLM={phase_quality(data['llm_results']):.1f}%, Random={phase_quality(data['random_results']):.1f}%, LHS={phase_quality(data['lhs_results']):.1f}%"
)
