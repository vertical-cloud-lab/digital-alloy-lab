---
name: proposal-consistency-check
description: >
  Automated consistency checker for the FLAIME Genesis Mission proposal.
  Runs a Python script that cross-checks numerical claims, terminology,
  and key facts across the LaTeX source, population plan, and checklist.
  Use when asked to check proposal consistency, find inconsistencies,
  or audit the proposal before submission.
allowed-tools: shell
---

# Proposal Consistency Check Skill

This skill runs an automated consistency check across the FLAIME Genesis
Mission proposal documents. It catches numerical mismatches, terminology
drift, and missing required content.

## Usage

Run the checker script from the skill's directory:

```bash
python3 .github/skills/proposal-consistency-check/check_consistency.py
```

The script outputs a structured report with severity levels:
- **CRITICAL**: Must fix before submission
- **WARNING**: Should review
- **INFO**: Minor / stylistic

## What It Checks

1. **Numerical claims** — budget totals ($750K = BYU $650K + partner subawards
   ), personnel (2 MS + 10 UG), composition targets (100–200),
   sub-system count (22,803 = Σ C(15,k) for k=2..8), KPI thresholds, TRL levels
2. **Terminology** — FLAIME = "Fast Learning AI for Mineral Efficiency",
   TCAl10 (not TCAL8), AMAZEMET (all caps), consistent LPBF/Thermo-Calc/pycalphad
3. **Cross-references** — LaTeX `\ref`/`\label` pairs, unreferenced figures, placeholders
4. **FOA compliance** — Buy America, AI disclosure, abstract self-contained (no `\cite{}`),
   "Application Stage: Phase I" in abstract, team 2-of-3 categories
5. **Math validation** — combinatorics, budget arithmetic, throughput

## Key Design Note: Element Palette

The palette has 15 **non-Al** alloying elements. Al is always the base.
- k=2 → **ternary** system (2 chosen + Al = 3 components)
- k=3 → **quaternary** system (3 chosen + Al = 4 components)
- This is NOT a bug — do not "fix" ternary to binary for k=2.

## Canonical Parameters (update these when proposal changes)

The script header contains all canonical parameter values. When the proposal
evolves, update the constants at the top of `check_consistency.py` to match.

## After Running

Review the output and address findings in order of severity. The script
is conservative — it may flag items that are technically correct but worth
a human double-check.
