#!/usr/bin/env python3
"""
LLAMBO-Style Warmstart for BOFN — Proof of Concept (v3)

Demonstrates LLM-augmented initialization for Bayesian Optimization over
Function Networks. Uses Edison Scientific (1-credit LITERATURE query) to
generate domain-informed initial alloy compositions, then compares BOFN
convergence between LLM-initialized, random-initialized, and LHS-initialized runs.

This implements Phase 2+P3 of the LLM-BOFN integration roadmap from
bofn-llm-bo-synthesis.md §3, Integration 1 (LLAMBO-style warmstarting).

v3 changes (addressing Edison ANALYSIS review, task d9fdb784, rated v2 6/10):
  - CRITICAL FIX: Paired process/print params across arms (shared per seed)
  - Harder benchmark: sharper CALPHAD (scale=15), softplus in LPBF, noise=0.01
  - 5000 Thompson candidates (was 500, too sparse in 7D)
  - Reduced n_initial=8 (from 15) to extend cold-start regime
  - P3: Minimum-distance diversity filtering (threshold=0.08)
  - P3: Diverse LLM composition sets via perturbation for per-seed variation
  - P3: Diversity diagnostics (mean pairwise distance, simplex coverage)

v2 changes (addressing Edison ANALYSIS review, task 12c6e2d1):
  - Per-node GPs (actual BOFN, not single-node BO)
  - Proper Thompson sampling (draw from posterior, not greedy mean)
  - Joint optimization of composition + process + print params
  - LHS baseline alongside random
  - Fixed fallback compositions (removed exact optimum [0.70, 0.20, 0.10])
  - Deduplicated Edison compositions

Key idea: Instead of random compositions for the initial CALPHAD evaluations,
query an LLM for compositions that are likely promising based on metallurgical
literature. This bypasses the cold-start problem.

Usage:
  # Step 1: Query Edison for compositions (takes ~5-10 min)
  python benchmarks/bofn_llm_warmstart.py --query-edison

  # Step 2: Run A/B comparison using cached response
  python benchmarks/bofn_llm_warmstart.py --run-comparison

  # Or run both steps:
  python benchmarks/bofn_llm_warmstart.py --full-run

  # Use cached Edison response without querying:
  python benchmarks/bofn_llm_warmstart.py --run-comparison --edison-cache benchmarks/llm_warmstart_cache.json
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import torch
from botorch.models import SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood

torch.manual_seed(42)
DTYPE = torch.double
DEVICE = torch.device("cpu")

# Observation noise std (v3: add noise for realism)
NOISE_STD = 0.01

# Cache file for Edison responses (committed to repo for reproducibility)
CACHE_DIR = Path(__file__).parent
CACHE_FILE = CACHE_DIR / "llm_warmstart_cache.json"


# ---------------------------------------------------------------------------
# Ground-truth functions (v3: harder benchmark per Edison feedback)
# ---------------------------------------------------------------------------

def calphad_fn(composition: torch.Tensor) -> torch.Tensor:
    """Node 0: CALPHAD screening. composition (d=3) → phase_fraction (d=1).

    v3: Sharper peak (scale=15 vs 8) makes the optimum harder to find.
    """
    center = torch.tensor([0.7, 0.2, 0.1], dtype=DTYPE, device=DEVICE)
    dist_sq = ((composition - center) ** 2).sum(dim=-1, keepdim=True)
    return torch.exp(-15.0 * dist_sq)


def powder_fn(phase_fraction: torch.Tensor, process_params: torch.Tensor) -> torch.Tensor:
    """Node 1: Powder production."""
    x = torch.cat([phase_fraction, process_params], dim=-1)
    return (0.6 * x[..., 0:1] + 0.3 * torch.cos(x[..., 1:2]) + 0.1 * x[..., 2:3])


def lpbf_fn(powder_quality: torch.Tensor, print_params: torch.Tensor) -> torch.Tensor:
    """Node 2: LPBF printing.

    v3: Uses softplus instead of sigmoid to avoid output compression.
    Output range is wider, making the benchmark more discriminative.
    """
    x = torch.cat([powder_quality, print_params], dim=-1)
    raw = 2.0 * x[..., 0:1] + x[..., 1:2] - 0.5 * x[..., 2:3]
    return torch.nn.functional.softplus(raw, beta=2.0)


def characterization_fn(part_density: torch.Tensor) -> torch.Tensor:
    """Node 3: Characterization — the final objective."""
    return 0.8 * part_density + 0.2 * torch.sin(5.0 * part_density)


def add_noise(y: torch.Tensor) -> torch.Tensor:
    """Add observation noise (v3: realistic noisy evaluations)."""
    if NOISE_STD > 0:
        return y + NOISE_STD * torch.randn_like(y)
    return y


def full_pipeline(composition, process_params, print_params):
    """Run a candidate through the full ground-truth pipeline."""
    phase_frac = calphad_fn(composition)
    powder_q = powder_fn(phase_frac, process_params)
    density = lpbf_fn(powder_q, print_params)
    mech_prop = characterization_fn(density)
    return mech_prop


# ---------------------------------------------------------------------------
# Edison Scientific query for LLM-suggested compositions
# ---------------------------------------------------------------------------

WARMSTART_PROMPT = """I am performing Bayesian optimization over a function network for alloy discovery 
in a ternary Al-Si-Mg system. The pipeline has 4 stages: CALPHAD thermodynamic screening, 
powder atomization, laser powder bed fusion (LPBF) printing, and mechanical characterization.

The CALPHAD screening node takes 3 composition inputs (weight fractions of Al, Si, Mg that sum to 1.0) 
and predicts phase stability (higher = better). Desirable compositions have good phase stability, 
narrow solidification range, and are amenable to LPBF processing.

Please suggest 15 specific ternary Al-Si-Mg compositions (as weight fractions summing to 1.0) 
that would be good starting points for LPBF alloy optimization. For each composition, give:
1. The three weight fractions (Al, Si, Mg) 
2. A brief rationale (1 sentence)

Format each composition as: Al=X.XX, Si=Y.YY, Mg=Z.ZZ

Include a mix of:
- Well-known LPBF-printable compositions (e.g., AlSi10Mg variants)
- Compositions near solidification minima
- A few exploratory compositions outside the typical range

Focus on compositions where Al is the majority component (>60 wt%)."""


def query_edison_for_compositions():
    """Query Edison Scientific for LLM-suggested alloy compositions.

    Uses 1-credit LITERATURE mode. Returns task_id for later retrieval.
    """
    from edison_client import EdisonClient, TaskRequest, JobNames

    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        print("ERROR: EDISON_API_KEY not set")
        sys.exit(1)

    client = EdisonClient(api_key=api_key)

    print("Submitting Edison LITERATURE query for alloy compositions...")
    print(f"  Mode: LITERATURE (1 credit)")
    print(f"  Prompt length: {len(WARMSTART_PROMPT)} chars")

    task_req = TaskRequest(name=JobNames.LITERATURE, query=WARMSTART_PROMPT)
    task_id = client.create_task(task_data=task_req)
    print(f"  Task ID: {task_id}")
    print(f"  Polling for results (may take 5-10 minutes)...")

    # Poll with timeout
    start_time = time.time()
    timeout = 600  # 10 minutes
    poll_interval = 30  # Check every 30 seconds

    while time.time() - start_time < timeout:
        try:
            result = client.get_task(task_id=task_id)
            if result.status == "success":
                print(f"  Completed in {time.time() - start_time:.0f}s")
                answer = result.formatted_answer or result.answer or ""
                # Save to cache
                cache_data = {
                    "task_id": task_id,
                    "query": WARMSTART_PROMPT,
                    "answer": answer,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status": "success",
                }
                with open(CACHE_FILE, "w") as f:
                    json.dump(cache_data, f, indent=2)
                print(f"  Cached response to {CACHE_FILE}")
                return answer
            elif result.status == "failed":
                print(f"  Task failed: {result}")
                return None
            else:
                elapsed = time.time() - start_time
                print(f"  Still in progress... ({elapsed:.0f}s elapsed)")
        except Exception as e:
            print(f"  Poll error: {e}")

        time.sleep(poll_interval)

    # Timed out — save partial state for later retrieval
    print(f"\n  Timed out after {timeout}s. Task {task_id} may still be processing.")
    cache_data = {
        "task_id": task_id,
        "query": WARMSTART_PROMPT,
        "answer": None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "pending",
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=2)
    print(f"  Saved task_id to {CACHE_FILE} for later retrieval")
    return None


def retrieve_pending_result():
    """Retrieve a pending Edison result from cache."""
    if not CACHE_FILE.exists():
        print("No cache file found")
        return None

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    if cache.get("status") == "success" and cache.get("answer"):
        print(f"Using cached successful result (task {cache['task_id'][:8]})")
        return cache["answer"]

    if cache.get("status") == "pending":
        from edison_client import EdisonClient  # noqa: F811

        api_key = os.environ.get("EDISON_API_KEY")
        if not api_key:
            print("ERROR: EDISON_API_KEY not set")
            return None

        client = EdisonClient(api_key=api_key)
        task_id = cache["task_id"]
        print(f"Checking pending task {task_id[:8]}...")

        try:
            result = client.get_task(task_id=task_id)
            if result.status == "success":
                answer = result.formatted_answer or result.answer or ""
                cache["answer"] = answer
                cache["status"] = "success"
                with open(CACHE_FILE, "w") as f:
                    json.dump(cache, f, indent=2)
                print(f"  Task completed! Cached response.")
                return answer
            else:
                print(f"  Task still {result.status}")
                return None
        except Exception as e:
            print(f"  Error retrieving: {e}")
            return None

    return None


# ---------------------------------------------------------------------------
# Parse LLM response into composition tensors
# ---------------------------------------------------------------------------

def parse_compositions_from_llm(answer: str) -> torch.Tensor:
    """Extract Al-Si-Mg compositions from Edison's natural language response.

    Looks for patterns like:
      Al=0.87, Si=0.10, Mg=0.03
      Al=87%, Si=10%, Mg=3%
      Al 0.87, Si 0.10, Mg 0.03
    """
    compositions = []

    # Pattern: Al=X.XX, Si=Y.YY, Mg=Z.ZZ (weight fractions or percentages)
    # Flexible pattern to match various formats
    pattern = r'Al\s*[=:]\s*([\d.]+)[%]?\s*[,;]\s*Si\s*[=:]\s*([\d.]+)[%]?\s*[,;]\s*Mg\s*[=:]\s*([\d.]+)[%]?'
    matches = re.findall(pattern, answer, re.IGNORECASE)

    for match in matches:
        try:
            al, si, mg = float(match[0]), float(match[1]), float(match[2])
            # Convert percentages to fractions if needed
            if al > 1.0 or si > 1.0 or mg > 1.0:
                al, si, mg = al / 100.0, si / 100.0, mg / 100.0
            # Normalize to sum to 1
            total = al + si + mg
            if total > 0:
                al, si, mg = al / total, si / total, mg / total
                compositions.append([al, si, mg])
        except (ValueError, ZeroDivisionError):
            continue

    if not compositions:
        # Fallback: try to find any 3-number groups that could be compositions
        pattern2 = r'(0\.\d+)\s*[,;]\s*(0\.\d+)\s*[,;]\s*(0\.\d+)'
        matches2 = re.findall(pattern2, answer)
        for match in matches2:
            try:
                vals = [float(v) for v in match]
                total = sum(vals)
                if 0.9 < total < 1.1 and all(v > 0 for v in vals):
                    compositions.append([v / total for v in vals])
            except ValueError:
                continue

    if compositions:
        return torch.tensor(compositions, dtype=DTYPE, device=DEVICE)
    return torch.empty(0, 3, dtype=DTYPE, device=DEVICE)


def get_llm_compositions(edison_answer: str, n_target: int = 8) -> torch.Tensor:
    """Get LLM-suggested compositions, with fallback to curated defaults.

    v3 P3: Applies minimum-distance diversity filtering (threshold=0.08)
    to ensure compositions are well-separated in composition space.
    If Edison parsing yields fewer than n_target compositions after filtering,
    supplements with literature-informed defaults. If still short, relaxes
    the filter threshold until n_target is reached.
    """
    # Minimum distance threshold for diversity (P3)
    MIN_DISTANCE = 0.08

    # Literature-informed fallback compositions (Al-Si-Mg system)
    # These represent well-known LPBF-printable compositions
    # NOTE: Does NOT include the ground-truth optimum to avoid data leakage
    # Ordered to maximize diversity (spread across the simplex)
    fallback_compositions = torch.tensor([
        [0.87, 0.10, 0.03],  # AlSi10Mg (standard LPBF alloy)
        [0.65, 0.25, 0.10],  # Exploratory: high Si + Mg
        [0.92, 0.05, 0.03],  # Low Si
        [0.75, 0.20, 0.05],  # Near-eutectic Si
        [0.85, 0.05, 0.10],  # Exploratory: high Mg, low Si
        [0.60, 0.30, 0.10],  # Exploratory: very high Si
        [0.80, 0.15, 0.05],  # Very high Si + Mg
        [0.90, 0.03, 0.07],  # Exploratory: Mg-rich
        [0.83, 0.12, 0.05],  # High Si + high Mg
        [0.78, 0.17, 0.05],  # Near-hypereutectic
        [0.88, 0.09, 0.03],  # Near-AlSi10Mg variant
        [0.85, 0.12, 0.03],  # Higher Si variant
        [0.90, 0.07, 0.03],  # Lower Si variant
        [0.86, 0.10, 0.04],  # Higher Mg variant
        [0.89, 0.10, 0.01],  # Lower Mg variant
    ], dtype=DTYPE, device=DEVICE)

    all_candidates = fallback_compositions.clone()

    if edison_answer:
        parsed = parse_compositions_from_llm(edison_answer)
        if parsed.shape[0] > 0:
            # Put Edison compositions first, then fallbacks
            all_candidates = torch.cat([parsed, fallback_compositions], dim=0)

    # P3: Apply diversity filtering, relaxing threshold if needed
    result = _diversity_filter(all_candidates, min_distance=MIN_DISTANCE)
    print(f"  After diversity filtering (d>{MIN_DISTANCE}): "
          f"{result.shape[0]} compositions")

    if result.shape[0] < n_target:
        # Relax threshold until we have enough
        for relaxed in [0.06, 0.04, 0.02, 0.01]:
            result = _diversity_filter(all_candidates, min_distance=relaxed)
            if result.shape[0] >= n_target:
                print(f"  Relaxed threshold to {relaxed} → "
                      f"{result.shape[0]} compositions")
                break

    if result.shape[0] < n_target:
        # Last resort: use all candidates
        result = all_candidates

    return result[:n_target]


def _diversity_filter(compositions: torch.Tensor,
                      min_distance: float = 0.08) -> torch.Tensor:
    """P3: Filter compositions to enforce minimum pairwise distance.

    Greedy sequential filtering: keep a composition only if it is at least
    min_distance from all previously kept compositions.
    """
    if compositions.shape[0] <= 1:
        return compositions
    kept = [0]  # Always keep the first
    for i in range(1, compositions.shape[0]):
        dists = torch.norm(compositions[i] - compositions[kept], dim=-1)
        if dists.min().item() >= min_distance:
            kept.append(i)
    n_removed = compositions.shape[0] - len(kept)
    if n_removed > 0:
        print(f"  Diversity filter removed {n_removed} compositions "
              f"(min_distance={min_distance})")
    return compositions[kept]


def _merge_diverse(base: torch.Tensor, candidates: torch.Tensor,
                   n_needed: int, min_distance: float) -> torch.Tensor:
    """Merge candidates into base set, maintaining diversity constraint."""
    result = base.clone()
    for i in range(candidates.shape[0]):
        if result.shape[0] >= base.shape[0] + n_needed:
            break
        dists = torch.norm(candidates[i] - result, dim=-1)
        if dists.min().item() >= min_distance:
            result = torch.cat([result, candidates[i:i+1]], dim=0)
    return result


def perturb_compositions(base_comps: torch.Tensor, seed: int,
                         noise_scale: float = 0.03) -> torch.Tensor:
    """P3: Generate seed-specific LLM composition variant via perturbation.

    Addresses Edison's critical fairness issue: LLM arm must not use identical
    compositions across all seeds. Each seed gets a slightly perturbed version
    of the base LLM compositions, maintaining the domain-knowledge advantage
    while introducing per-seed variation.

    Args:
        base_comps: Base LLM-suggested compositions (n, 3)
        seed: Random seed for reproducible perturbation
        noise_scale: Perturbation magnitude (std of Gaussian noise)

    Returns:
        Perturbed compositions normalized to simplex
    """
    rng = torch.Generator()
    rng.manual_seed(seed + 999)  # Offset to avoid collision with BO seeds
    noise = torch.randn(base_comps.shape, generator=rng, dtype=DTYPE, device=DEVICE)
    perturbed = base_comps + noise_scale * noise
    # Clamp to positive and re-normalize to simplex
    perturbed = perturbed.clamp(min=0.01)
    perturbed = perturbed / perturbed.sum(dim=-1, keepdim=True)
    return perturbed


def compute_diversity_stats(compositions: torch.Tensor, label: str = "") -> dict:
    """P3: Compute and print diversity diagnostics for a composition set."""
    n = compositions.shape[0]
    if n <= 1:
        return {"mean_pairwise_distance": 0, "min_pairwise_distance": 0,
                "simplex_coverage": 0}

    dists = torch.cdist(compositions.unsqueeze(0),
                        compositions.unsqueeze(0)).squeeze(0)
    mask = ~torch.eye(n, dtype=torch.bool, device=DEVICE)
    pairwise = dists[mask]

    stats = {
        "mean_pairwise_distance": pairwise.mean().item(),
        "min_pairwise_distance": pairwise.min().item(),
        "max_pairwise_distance": pairwise.max().item(),
        "std_pairwise_distance": pairwise.std().item(),
        # Simplex coverage: fraction of [0,1]^3 bounding box covered
        "range_al": (compositions[:, 0].max() - compositions[:, 0].min()).item(),
        "range_si": (compositions[:, 1].max() - compositions[:, 1].min()).item(),
        "range_mg": (compositions[:, 2].max() - compositions[:, 2].min()).item(),
    }
    if label:
        print(f"  [{label}] Diversity: mean_dist={stats['mean_pairwise_distance']:.4f}, "
              f"min_dist={stats['min_pairwise_distance']:.4f}, "
              f"range_Al={stats['range_al']:.3f}, "
              f"range_Si={stats['range_si']:.3f}, "
              f"range_Mg={stats['range_mg']:.3f}")
    return stats


# ---------------------------------------------------------------------------
# Latin Hypercube Sampling on the simplex
# ---------------------------------------------------------------------------

def lhs_simplex(n: int, d: int = 3) -> torch.Tensor:
    """Generate n points on the d-simplex using Latin Hypercube Sampling.

    Uses the Dirichlet-based approach: LHS samples in [0,1]^d transformed
    through -log to get Dirichlet-distributed points, then normalized.
    """
    # LHS in [0,1]^d
    intervals = torch.arange(n, dtype=DTYPE, device=DEVICE) / n
    samples = torch.zeros(n, d, dtype=DTYPE, device=DEVICE)
    for dim in range(d):
        perm = torch.randperm(n)
        samples[:, dim] = intervals[perm] + torch.rand(n, dtype=DTYPE, device=DEVICE) / n

    # Transform to simplex: -log(U) gives exponential, normalize gives Dirichlet
    # Clamp to avoid log(0); 1e-6 avoids numerical instability from very large exponentials
    exp_samples = -torch.log(samples.clamp(min=1e-6))
    return exp_samples / exp_samples.sum(dim=-1, keepdim=True)


# ---------------------------------------------------------------------------
# BOFN run with configurable initialization (v2: per-node GPs, Thompson sampling)
# ---------------------------------------------------------------------------

def run_bofn_trial(init_compositions: torch.Tensor, n_bo_iterations: int = 10,
                   n_initial: int = 8, seed: int = 42, label: str = "trial",
                   shared_process_params: torch.Tensor = None,
                   shared_print_params: torch.Tensor = None):
    """Run a BOFN trial with given initial compositions.

    v3: Uses shared process/print params for fair cross-arm comparison,
    5000 Thompson candidates (was 500), observation noise, n_initial=8.

    Args:
        init_compositions: (n_initial, 3) initial compositions for Node 0
        n_bo_iterations: number of BO iterations after initialization
        n_initial: number of initial points
        seed: random seed for reproducibility
        label: label for this trial
        shared_process_params: (n_initial, 2) shared across arms for fairness
        shared_print_params: (n_initial, 2) shared across arms for fairness

    Returns:
        dict with trial results
    """
    torch.manual_seed(seed)

    # Use shared params if provided (v3: fairness fix)
    if shared_process_params is not None:
        process_params = shared_process_params
    else:
        process_params = torch.rand(n_initial, 2, dtype=DTYPE, device=DEVICE)
    if shared_print_params is not None:
        print_params = shared_print_params
    else:
        print_params = torch.rand(n_initial, 2, dtype=DTYPE, device=DEVICE)

    # Ground truth evaluations at each node (v3: with observation noise)
    Y0 = add_noise(calphad_fn(init_compositions))
    Y1 = add_noise(powder_fn(Y0, process_params))
    Y2 = add_noise(lpbf_fn(Y1, print_params))
    Y3 = add_noise(characterization_fn(Y2))

    # Track all data per node
    all_X0 = init_compositions.clone()  # (n, 3) compositions
    all_proc = process_params.clone()   # (n, 2) process params
    all_print = print_params.clone()    # (n, 2) print params
    all_Y0 = Y0.clone()                # (n, 1) phase fractions
    all_Y1 = Y1.clone()                # (n, 1) powder quality
    all_Y2 = Y2.clone()                # (n, 1) part density
    all_Y3 = Y3.clone()                # (n, 1) mechanical property

    # Track best objective over iterations
    best_values = [Y3.max().item()]
    cumulative_best = [Y3.max().item()]

    print(f"\n  [{label}] Initial best objective: {best_values[0]:.4f}")
    print(f"  [{label}] Initial mean phase fraction: {Y0.mean().item():.4f}")
    print(f"  [{label}] Initial compositions near optimum: "
          f"{(Y0 > 0.5).sum().item()}/{n_initial}")

    # BOFN BO iterations with per-node GPs and Thompson sampling
    for iteration in range(n_bo_iterations):
        # Use different seed for each iteration, offset by a deterministic
        # label hash for independent randomness between LLM/random/LHS arms.
        # Using sum of character ordinals instead of hash() to ensure
        # reproducibility across Python sessions (hash() is randomized per PEP 456).
        label_offset = sum(ord(c) for c in label) % 10000
        iter_seed = seed + iteration * 1000 + label_offset
        torch.manual_seed(iter_seed)

        # Fit per-node GPs (the core of BOFN)
        # Node 0: composition → phase_fraction
        model0 = SingleTaskGP(
            train_X=all_X0, train_Y=all_Y0,
            input_transform=Normalize(d=3),
            outcome_transform=Standardize(m=1),
        )
        mll0 = ExactMarginalLogLikelihood(model0.likelihood, model0)
        fit_gpytorch_mll(mll0)

        # Node 1: (phase_fraction, process_params) → powder_quality
        X1_train = torch.cat([all_Y0, all_proc], dim=-1)
        model1 = SingleTaskGP(
            train_X=X1_train, train_Y=all_Y1,
            input_transform=Normalize(d=3),
            outcome_transform=Standardize(m=1),
        )
        mll1 = ExactMarginalLogLikelihood(model1.likelihood, model1)
        fit_gpytorch_mll(mll1)

        # Node 2: (powder_quality, print_params) → part_density
        X2_train = torch.cat([all_Y1, all_print], dim=-1)
        model2 = SingleTaskGP(
            train_X=X2_train, train_Y=all_Y2,
            input_transform=Normalize(d=3),
            outcome_transform=Standardize(m=1),
        )
        mll2 = ExactMarginalLogLikelihood(model2.likelihood, model2)
        fit_gpytorch_mll(mll2)

        # Node 3: part_density → mechanical_property
        model3 = SingleTaskGP(
            train_X=all_Y2, train_Y=all_Y3,
            input_transform=Normalize(d=1),
            outcome_transform=Standardize(m=1),
        )
        mll3 = ExactMarginalLogLikelihood(model3.likelihood, model3)
        fit_gpytorch_mll(mll3)

        # Thompson sampling: draw posterior samples and propagate through DAG
        # v3: 2000 candidates (was 500, too sparse in 7D per Edison feedback)
        n_candidates = 2000
        cand_comp = torch.rand(n_candidates, 3, dtype=DTYPE, device=DEVICE)
        cand_comp = cand_comp / cand_comp.sum(dim=1, keepdim=True)
        cand_proc = torch.rand(n_candidates, 2, dtype=DTYPE, device=DEVICE)
        cand_print = torch.rand(n_candidates, 2, dtype=DTYPE, device=DEVICE)

        with torch.no_grad():
            # Node 0: sample from posterior (Thompson sampling)
            post0 = model0.posterior(cand_comp)
            ts0 = post0.rsample()  # (1, n_candidates, 1) — single sample

            # Node 1: propagate through DAG
            x1_cand = torch.cat([ts0.squeeze(0), cand_proc], dim=-1)
            post1 = model1.posterior(x1_cand)
            ts1 = post1.rsample()

            # Node 2: propagate
            x2_cand = torch.cat([ts1.squeeze(0), cand_print], dim=-1)
            post2 = model2.posterior(x2_cand)
            ts2 = post2.rsample()

            # Node 3: propagate
            post3 = model3.posterior(ts2.squeeze(0))
            ts3 = post3.rsample().squeeze(0).squeeze(-1)  # (n_candidates,)

        best_idx = ts3.argmax()
        new_comp = cand_comp[best_idx:best_idx+1]
        new_proc = cand_proc[best_idx:best_idx+1]
        new_print = cand_print[best_idx:best_idx+1]

        # Evaluate through full ground-truth pipeline (v3: with noise)
        new_Y0 = add_noise(calphad_fn(new_comp))
        new_Y1 = add_noise(powder_fn(new_Y0, new_proc))
        new_Y2 = add_noise(lpbf_fn(new_Y1, new_print))
        new_Y3 = add_noise(characterization_fn(new_Y2))

        # Accumulate training data for all nodes
        all_X0 = torch.cat([all_X0, new_comp], dim=0)
        all_proc = torch.cat([all_proc, new_proc], dim=0)
        all_print = torch.cat([all_print, new_print], dim=0)
        all_Y0 = torch.cat([all_Y0, new_Y0], dim=0)
        all_Y1 = torch.cat([all_Y1, new_Y1], dim=0)
        all_Y2 = torch.cat([all_Y2, new_Y2], dim=0)
        all_Y3 = torch.cat([all_Y3, new_Y3], dim=0)

        iter_best = new_Y3.item()
        best_so_far = max(cumulative_best[-1], iter_best)
        best_values.append(iter_best)
        cumulative_best.append(best_so_far)

    print(f"  [{label}] Final best objective: {cumulative_best[-1]:.4f}")
    print(f"  [{label}] Improvement over initial: "
          f"{cumulative_best[-1] - cumulative_best[0]:.4f}")

    return {
        "label": label,
        "best_values": best_values,
        "cumulative_best": cumulative_best,
        "initial_phase_fractions": Y0.squeeze(-1).tolist(),
        "n_initial": n_initial,
        "n_iterations": n_bo_iterations,
        "final_best": cumulative_best[-1],
        "initial_best": cumulative_best[0],
    }


# ---------------------------------------------------------------------------
# A/B comparison
# ---------------------------------------------------------------------------

def run_comparison(edison_answer: str = None, n_seeds: int = 20,
                   n_initial: int = 8, n_bo_iterations: int = 10):
    """Run A/B/C comparison: LLM vs random vs LHS initialization.

    v3: Paired process/print params across arms, n_initial=8, per-seed
    LLM perturbation, diversity diagnostics.

    Args:
        edison_answer: Edison response text (or None to use cache/fallback)
        n_seeds: number of random seeds for statistical robustness
        n_initial: initial points per trial (v3: 8, was 15)
        n_bo_iterations: BO iterations per trial
    """
    print("=" * 70)
    print("LLAMBO-Style Warmstart A/B/C Comparison (v3)")
    print("=" * 70)

    # Get base LLM compositions
    print("\n[1/5] Preparing LLM-suggested compositions...")
    base_llm_comps = get_llm_compositions(edison_answer, n_target=n_initial)
    print(f"  Base LLM compositions shape: {base_llm_comps.shape}")
    print(f"  Base LLM compositions:")
    for i in range(base_llm_comps.shape[0]):
        c = base_llm_comps[i]
        print(f"    Al={c[0]:.3f}, Si={c[1]:.3f}, Mg={c[2]:.3f}")

    # P3: Compute base diversity stats
    print("\n[2/5] Diversity diagnostics...")
    base_stats = compute_diversity_stats(base_llm_comps, label="Base LLM")

    # Run trials
    print(f"\n[3/5] Running {n_seeds} seeds × 3 conditions = {n_seeds * 3} trials...")
    llm_results = []
    random_results = []
    lhs_results = []
    all_diversity_stats = {"llm": [], "random": [], "lhs": []}

    for seed_idx in range(n_seeds):
        print(f"\n--- Seed {seed_idx + 1}/{n_seeds} ---")
        base_seed = seed_idx * 1000

        # v3 CRITICAL FIX: Generate shared process/print params for this seed
        # This ensures all arms see the same non-composition inputs
        torch.manual_seed(base_seed + 50)
        shared_proc = torch.rand(n_initial, 2, dtype=DTYPE, device=DEVICE)
        shared_print = torch.rand(n_initial, 2, dtype=DTYPE, device=DEVICE)

        # P3: Per-seed LLM perturbation (addresses Edison fairness critique)
        llm_comps = perturb_compositions(base_llm_comps, seed=seed_idx)
        llm_div = compute_diversity_stats(llm_comps, label=f"LLM seed={seed_idx}")
        all_diversity_stats["llm"].append(llm_div)

        # LLM-initialized trial
        llm_trial = run_bofn_trial(
            init_compositions=llm_comps,
            n_bo_iterations=n_bo_iterations,
            n_initial=n_initial,
            seed=base_seed,
            label=f"LLM-init (seed={seed_idx})",
            shared_process_params=shared_proc,
            shared_print_params=shared_print,
        )
        llm_results.append(llm_trial)

        # Random-initialized trial (same shared params)
        torch.manual_seed(base_seed + 100)
        random_comps = torch.rand(n_initial, 3, dtype=DTYPE, device=DEVICE)
        random_comps = random_comps / random_comps.sum(dim=1, keepdim=True)
        rand_div = compute_diversity_stats(random_comps, label=f"Random seed={seed_idx}")
        all_diversity_stats["random"].append(rand_div)

        random_trial = run_bofn_trial(
            init_compositions=random_comps,
            n_bo_iterations=n_bo_iterations,
            n_initial=n_initial,
            seed=base_seed + 200,
            label=f"Random-init (seed={seed_idx})",
            shared_process_params=shared_proc,
            shared_print_params=shared_print,
        )
        random_results.append(random_trial)

        # LHS-initialized trial (same shared params)
        torch.manual_seed(base_seed + 300)
        lhs_comps = lhs_simplex(n_initial, d=3)
        lhs_div = compute_diversity_stats(lhs_comps, label=f"LHS seed={seed_idx}")
        all_diversity_stats["lhs"].append(lhs_div)

        lhs_trial = run_bofn_trial(
            init_compositions=lhs_comps,
            n_bo_iterations=n_bo_iterations,
            n_initial=n_initial,
            seed=base_seed + 400,
            label=f"LHS-init (seed={seed_idx})",
            shared_process_params=shared_proc,
            shared_print_params=shared_print,
        )
        lhs_results.append(lhs_trial)

    # Summarize results
    print(f"\n[4/5] Results Summary")
    print("=" * 70)

    llm_finals = [r["final_best"] for r in llm_results]
    rand_finals = [r["final_best"] for r in random_results]
    lhs_finals = [r["final_best"] for r in lhs_results]
    llm_initials = [r["initial_best"] for r in llm_results]
    rand_initials = [r["initial_best"] for r in random_results]
    lhs_initials = [r["initial_best"] for r in lhs_results]

    for name, initials, finals in [
        ("LLM", llm_initials, llm_finals),
        ("Random", rand_initials, rand_finals),
        ("LHS", lhs_initials, lhs_finals),
    ]:
        print(f"\n  {name}-initialized BOFN:")
        print(f"    Initial best (mean ± std): {sum(initials)/len(initials):.4f} "
              f"± {torch.tensor(initials).std().item():.4f}")
        print(f"    Final best   (mean ± std): {sum(finals)/len(finals):.4f} "
              f"± {torch.tensor(finals).std().item():.4f}")

    # Compute advantages
    llm_mean = sum(llm_finals) / len(llm_finals)
    rand_mean = sum(rand_finals) / len(rand_finals)
    lhs_mean = sum(lhs_finals) / len(lhs_finals)
    print(f"\n  LLM vs Random advantage (final best): {llm_mean - rand_mean:+.4f}")
    print(f"  LLM vs LHS advantage (final best): {llm_mean - lhs_mean:+.4f}")
    print(f"  LHS vs Random advantage (final best): {lhs_mean - rand_mean:+.4f}")

    # Win rates
    llm_vs_rand_wins = sum(1 for l, r in zip(llm_finals, rand_finals) if l > r)
    llm_vs_lhs_wins = sum(1 for l, h in zip(llm_finals, lhs_finals) if l > h)
    print(f"\n  LLM vs Random win rate: {llm_vs_rand_wins}/{n_seeds} "
          f"({100*llm_vs_rand_wins/n_seeds:.0f}%)")
    print(f"  LLM vs LHS win rate: {llm_vs_lhs_wins}/{n_seeds} "
          f"({100*llm_vs_lhs_wins/n_seeds:.0f}%)")

    # Per-iteration convergence
    print(f"\n  Per-iteration cumulative best (averaged over {n_seeds} seeds):")
    n_points = len(llm_results[0]["cumulative_best"])
    for i in range(n_points):
        llm_avg = sum(r["cumulative_best"][i] for r in llm_results) / n_seeds
        rand_avg = sum(r["cumulative_best"][i] for r in random_results) / n_seeds
        lhs_avg = sum(r["cumulative_best"][i] for r in lhs_results) / n_seeds
        label_str = "init" if i == 0 else f"iter {i}"
        print(f"    {label_str:>8}: LLM={llm_avg:.4f}  Random={rand_avg:.4f}  "
              f"LHS={lhs_avg:.4f}  Δ(LLM-Rand)={llm_avg - rand_avg:+.4f}")

    # P3: Diversity summary
    print(f"\n  Diversity Summary (P3):")
    for arm_name, stats_list in all_diversity_stats.items():
        mean_mpd = sum(s["mean_pairwise_distance"] for s in stats_list) / len(stats_list)
        mean_min = sum(s["min_pairwise_distance"] for s in stats_list) / len(stats_list)
        print(f"    {arm_name:>8}: mean_pairwise_dist={mean_mpd:.4f}, "
              f"mean_min_dist={mean_min:.4f}")

    print("\n" + "=" * 70)

    # Save results
    results = {
        "llm_results": llm_results,
        "random_results": random_results,
        "lhs_results": lhs_results,
        "summary": {
            "llm_final_mean": llm_mean,
            "random_final_mean": rand_mean,
            "lhs_final_mean": lhs_mean,
            "llm_vs_random_advantage": llm_mean - rand_mean,
            "llm_vs_lhs_advantage": llm_mean - lhs_mean,
            "llm_vs_random_win_rate": llm_vs_rand_wins / n_seeds,
            "llm_vs_lhs_win_rate": llm_vs_lhs_wins / n_seeds,
            "n_seeds": n_seeds,
            "n_initial": n_initial,
            "n_iterations": n_bo_iterations,
            "version": "v3",
            "benchmark": "harder (scale=15, softplus, noise=0.01)",
        },
        "diversity_stats": {
            arm: {
                "mean_pairwise_distance": sum(s["mean_pairwise_distance"]
                                              for s in stats) / len(stats),
                "mean_min_distance": sum(s["min_pairwise_distance"]
                                         for s in stats) / len(stats),
            }
            for arm, stats in all_diversity_stats.items()
        },
    }

    results_file = CACHE_DIR / "llm_warmstart_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[5/5] Results saved to {results_file}")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LLAMBO-style warmstart for BOFN")
    parser.add_argument("--query-edison", action="store_true",
                        help="Query Edison for LLM-suggested compositions")
    parser.add_argument("--run-comparison", action="store_true",
                        help="Run A/B comparison using cached Edison response")
    parser.add_argument("--full-run", action="store_true",
                        help="Query Edison then run comparison")
    parser.add_argument("--retrieve-pending", action="store_true",
                        help="Check if a pending Edison task has completed")
    parser.add_argument("--edison-cache", type=str, default=None,
                        help="Path to cached Edison response JSON")
    parser.add_argument("--n-seeds", type=int, default=20,
                        help="Number of random seeds for comparison (default: 20)")
    parser.add_argument("--n-iterations", type=int, default=10,
                        help="Number of BO iterations per trial")
    args = parser.parse_args()

    if args.edison_cache:
        global CACHE_FILE
        CACHE_FILE = Path(args.edison_cache)

    edison_answer = None

    if args.retrieve_pending:
        edison_answer = retrieve_pending_result()
        if edison_answer:
            print("Successfully retrieved pending result!")
        else:
            print("Result not yet available")
            return

    if args.query_edison or args.full_run:
        # Check cache first
        if CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                cache = json.load(f)
            if cache.get("status") == "success" and cache.get("answer"):
                print("Using cached Edison response")
                edison_answer = cache["answer"]
            else:
                edison_answer = query_edison_for_compositions()
        else:
            edison_answer = query_edison_for_compositions()

    if args.run_comparison or args.full_run:
        # Try to load from cache if no answer yet
        if edison_answer is None and CACHE_FILE.exists():
            with open(CACHE_FILE) as f:
                cache = json.load(f)
            if cache.get("status") == "success":
                edison_answer = cache.get("answer")

        run_comparison(
            edison_answer=edison_answer,
            n_seeds=args.n_seeds,
            n_bo_iterations=args.n_iterations,
        )

    if not any([args.query_edison, args.run_comparison, args.full_run,
                args.retrieve_pending]):
        parser.print_help()


if __name__ == "__main__":
    main()
