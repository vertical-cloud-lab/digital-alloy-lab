# Local minimum approximation of the BOFN benchmark surface

Probes the noiseless `ExtendedManufacturingGPNetwork` (6-node DAG, seed=0,
coupling=0.3, node_costs=[1,10,10,45,20,30]) used by
`benchmarks/bofn_actions_benchmark.py` and the SLURM sweep
`hpc/bofn_benchmark/`. The benchmark *maximizes* y5; this script reports the
*minimum* of y5 for context (gives a sense of how hard the floor is to escape
and the spread of the surface response).

Reproduce:

    python benchmarks/figures/local_min_approx/min_sobol.py

## Results (n=65,536 Sobol samples over [-1,1]^5, seed=0)

| stat   | y5 value |
|--------|----------|
| min    | 0.2100   |
| p01    | 0.2335   |
| p05    | 0.2689   |
| median | 0.5856   |
| mean   | 0.6055   |
| p95    | 1.0388   |
| p99    | 1.1885   |
| max    | 1.3698   |
| std    | 0.2405   |

L-BFGS-B multi-start (32 best Sobol seeds) refined the minimum to
**y5 ≈ 0.2079** at x* ≈ [0.584, 0.521, -0.276, -0.189, 1.000] — only ~0.002
below the Sobol grid floor, indicating the surface is reasonably well
covered by 65k Sobol points and the basin is broad.

For comparison, the benchmark's `compute_true_max(n_samples=16384)` reports
y5_max ≈ 1.37 (matches Sobol max here at 65,536). So the BOFN benchmark's
"true" optimum gap is ~1.16 units of y5 — well-spread, not a needle-in-a-
haystack landscape.

See `sobol_y5_distribution.png` for the y5 histogram and per-node
distributions; the surface is unimodal-ish with a right-skewed tail toward
the maximum, so easy fractional-cost gains are concentrated near the median
and the last ~10% of progress carries most of the optimization difficulty.
