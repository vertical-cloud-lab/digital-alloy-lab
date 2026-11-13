
# FLAIME Gantt Schedule — Round 2 Review Report

## Overall Grade: B+ (82/100), up from C+ (58/100)

| Category | R1 Grade | R2 Grade | Change |
|---|---|---|---|
| Scheduling Engine Logic | D (40) | B+ (85) | +45 |
| Task Duration Realism | C (60) | B+ (85) | +25 |
| Visual Design | C+ (62) | B- (72) | +10 |
| Code Quality | B- (72) | B (80) | +8 |
| Throughput Claim Validity | D+ (45) | B (82) | +37 |
| Documentation | B+ (82) | A- (88) | +6 |
| **Overall** | **C+ (58)** | **B+ (82)** | **+24** |

---

## 1. Has the scheduling engine been fixed correctly?

**Mostly yes — all Priority 1 critical bugs from R1 are resolved.** The scheduling engine is fundamentally sound now:

- ✅ **Zero resource conflicts** across all 4 shared resources (LPBF, Atomizer, AutoTrickler, SEM). R1 found 16 overlapping resource-usage pairs; R2 has 0.
- ✅ **All 12 compositions have unique start times** — the Comp 9-12 collapse (all starting Tue 07:00) is fully resolved via `_advance_work_hours()`.
- ✅ **Working-hours arithmetic** correctly staggers compositions by 4 work-hours, properly counting only staffed shift hours and skipping overnight/Sunday.
- ✅ **ResourceTracker** now tracks all 4 shared resources with event-driven scheduling.

**However, 5 residual issues remain:**

**BUG 1 (MODERATE — 3 tasks):** `_earliest_manual_start()` line 421 uses `<=` for the morning_end boundary (`if dt <= morning_end` where morning_end = 12:00). When a resource frees at exactly 12:00, this returns 12:00 as valid, but 12:00 is the start of lunch. Combined with `_schedule_task()` line 505 using strict `<` in `if t < lunch_s`, the lunch-crossing check fails when t == lunch_s. Result: 3 manual tasks scheduled during the 12:00-13:00 lunch break:
  - Comp 3 Setup: Tue 12:00-13:00 (spans entire lunch)
  - Comp 7 Extract: Thu 12:00-12:30 (during lunch)
  - Comp 10 Setup: Fri 12:00-13:00 (spans entire lunch)

**Fix:** Change line 421 from `if dt <= morning_end` to `if dt < morning_end`, OR change line 505 from `if t < lunch_s` to `if t <= lunch_s`. Two-line fix.

**BUG 2 (MINOR — 2 tasks):** Transit tasks (lines 491-493) bypass the shift-end check, directly returning `t + dur` after `_earliest_manual_start()` without verifying against `_manual_end()`. Result: 2 transit blocks end at 18:15 (Comp 1 and Comp 8). Impact is minimal — a 15-minute campus walk at 6 PM is physically realistic.

**BUG 3 (MINOR — 1 day):** `SEM_DAILY_LIMIT_H = 4.0` is declared (line 95) but never enforced. The `ResourceTracker` only tracks `sem_free` (sequential availability), not daily cumulative usage. Wednesday has 6.0h of SEM use (Comp 3: 2h + Comp 4: 2h + Comp 5: 2h), exceeding the declared 4h limit by 50%.

**BUG 4 (COSMETIC):** `_task_fits_in_day()` function (lines 447-468) appears to be dead code — it's defined but never called after refactoring. Its lunch-break logic also differs subtly from `_schedule_task()`, creating potential confusion.

---

## 2. Is the throughput of 1.71 comps/day realistic and defensible for a proposal?

**Yes, with caveats — it is slightly optimistic but defensible.**

The claimed 1.71 compositions/working day (12 compositions across 7 working days, Mon Sep 7 – Mon Sep 14) is a major improvement over the R1 claim of 2.4/day and is within reasonable bounds:

**Evidence supporting defensibility:**
- Steady-state completions average ~2/day (Tue-Thu each have 2 completions), which aligns with the LPBF bottleneck (5h/comp × 2 comps = 10h of 15h available)
- All 4 shared resources show zero conflicts — the schedule is physically realizable
- Per-composition pipeline time of 16.0h is realistic (up from R1's 12.5h)
- The 4h work-hour stagger enables effective pipelining (Comp N's LPBF runs while N+1 atomizes while N-1 characterizes)

**Factors causing slight inflation (~0.1-0.2 comps/day):**
- 3 tasks during lunch break add ~2-3h of phantom capacity
- Wednesday's SEM overuse (6h vs. 4h limit) — enforcing this would push Comp 5's SEM to Thursday
- The "7 working days" denominator includes the spill Monday with only 2 compositions finishing

**Corrected estimate:** With lunch-break and SEM fixes, throughput would drop to approximately **1.5-1.6 comps/day**, still well above the R1 estimate of 1.0-1.5 and appropriate for a proposal claiming "~1.5 compositions per day." R1's estimate of 1.0-1.5 was slightly conservative; the actual schedule demonstrates that effective pipelining pushes the upper bound of that range.

**Bottleneck analysis:**
- LPBF printer: 5.0h/comp, 15h available/day → theoretical max 3.0 comps/day
- Atomizer: 2.5h/comp, 10h staffed → theoretical max 4.0 comps/day
- SEM facility: 2.0h/comp, 4h daily limit → theoretical max 2.0 comps/day (binding if enforced)
- The SEM daily limit (if enforced) and LPBF together constrain to ~2 comps/day theoretical, ~1.5-1.7 achieved with overhead

**Recommendation for proposal:** Claim "~1.5 compositions per day" or "8-9 compositions per week" rather than 1.71. This rounds conservatively and accounts for real-world disruptions (equipment downtime, failed builds, scheduling friction).

---

## 3. Are there remaining visual improvements needed for publication quality?

**Yes — the figure is adequate for internal review but not yet publication-ready.** Key issues:

1. **Label overlap (HIGHEST PRIORITY):** Text labels for adjacent short tasks merge into illegible strings ("DispAtomize", "SetPrint", "PrepSEMech"). This is the most significant visual defect. Fix: increase label threshold to ≥1h tasks only, use abbreviated labels, or alternate above/below positioning.

2. **Font size too small:** Bar labels at 6.5pt are below the R1 recommendation of 8-9pt and will be illegible in print at standard figure reduction (most journals reduce to ~80% of column width).

3. **Non-working hours not compressed (R1 P4.4):** The x-axis shows all 24 hours including the 22:00-07:00 overnight gap, making the chart very wide (~8 day-widths) and individual task bars appear as thin slivers. Compressing non-working hours would reduce chart width by ~60% and dramatically improve readability.

4. **Legend density:** 15 entries in 5 columns. The two cooling entries (Powder cooling, Build-plate cool-down) look identical. Could merge to "Passive/cooling (dashed)" and reduce to ≤10 entries.

5. **Transit blocks invisible:** The thin gray slivers are informative in principle but invisible in practice.

6. **X-axis clutter:** ~24+ tick labels at 6-hour intervals spanning 8+ days create a dense, hard-to-read axis.

**Improvements achieved:** Figure size (14"×9.8" at 300 DPI), black text above bars, Okabe-Ito colorblind-safe palette, dashed outlines for cooling — all good.

---

## 4. Are there any remaining resource conflicts or impossible overlaps?

**No resource conflicts exist.** All four shared resources (LPBF, Atomizer, AutoTrickler, SEM) are used sequentially with zero overlaps. This is verified programmatically across all 180 scheduled blocks.

**Personnel feasibility:** Maximum concurrent manual tasks is 5 (at Fri 07:00), requiring personnel at 3 different locations simultaneously. With PI + 2 MS students + ~5 available UGs, this is feasible. Maximum concurrent manual tasks at any single location is 2 (at BYU-VCL and BYU-Micro). No single-person double-booking is forced.

**The only "impossible" items are the 3 lunch-break tasks** (manual work during 12:00-13:00), which are edge-case bugs, not resource conflicts. Fixing them would push tasks to 13:00 with minimal cascade impact.

---

## 5. Grade: B+ (82/100)

This is a substantial improvement from C+ (58/100). The scoring breakdown:

- **Scheduling Engine Logic: B+ (85).** All R1 critical bugs fixed. Four shared resources tracked correctly. Working-hours arithmetic works. Deductions for lunch-break edge case (-10), transit shift-end bypass (-3), unenforced SEM limit (-2).

- **Task Duration Realism: B+ (85).** Pipeline expanded to 16.0h/comp with cooling, cleaning, transit, and revised durations. Deductions for optimistic Sieve+QC (-5), no explicit epoxy cure wait in Prep (-5), no SEM pump-down overhead (-5).

- **Visual Design: B- (72).** Good DPI, palette, text color, cooling distinction. Major label overlap issue (-12), font too small (-5), no time compression (-6), dense legend (-5).

- **Code Quality: B (80).** Clean structure maintained. New features well-implemented. Remaining bugs are edge cases. Dead code (`_task_fits_in_day`) and redundant lunch logic (-5 each).

- **Throughput Claim Validity: B (82).** 1.71/day is realistic within ~15% of corrected value. Properly accounts for most real-world constraints. Deductions for SEM overuse (-8), lunch violations (-5), no class schedule modeling (-5).

- **Documentation: A- (88).** Excellent docstrings, comprehensive module header, clean summary output. Missing: explicit statement of known limitations.

---

## 6. Prioritized Remaining Changes

### PRIORITY 1 — Bug Fixes (10 minutes total, do before any proposal submission)
- **P1.1:** Fix lunch-break boundary: line 421 `<=` → `<`, line 505 `<` → `<=` (fixes 3 tasks)
- **P1.2:** Add shift-end check for transit tasks in lines 491-493 (fixes 2 tasks)

### PRIORITY 2 — Enforcement (30-40 minutes)
- **P2.1:** Enforce SEM daily limit or remove the declared constant (fixes Wed 6h→4h)
- **P2.2:** Remove dead `_task_fits_in_day()` function

### PRIORITY 3 — Visual Polish (2-3 hours, needed for proposal figure)
- **P3.1:** Fix label overlap (highest visual priority) — threshold at ≥1h, abbreviate
- **P3.2:** Increase bar label font to ≥8pt
- **P3.3:** Compress non-working hours in time axis (most impactful visual change)
- **P3.4:** Simplify legend to ≤10 entries
- **P3.5:** Consider 10"×6" for two-column proposal layouts

### PRIORITY 4 — Nice-to-Have (for A-grade, ~4 hours)
- **P4.1:** Resource utilization timeline subplot
- **P4.2:** Critical path highlighting
- **P4.3:** Named personnel assignment model
- **P4.4:** Schedule resilience analysis (what if a build fails?)

---

## Discretionary Analytical Decisions

- Classified the lunch-break edge-case bug as MODERATE rather than CRITICAL, because it affects only 3 of 84 manual tasks and has minimal cascade impact on overall throughput (~0.1 comps/day)
- Classified transit tasks ending at 18:15 as MINOR rather than MODERATE, because a 15-minute campus walk at 6 PM is physically realistic even if it technically violates the shift model
- Used SEM_DAILY_LIMIT_H = 4.0h as the reference limit for evaluating SEM daily compliance, based on the code's own declared constant; actual BYU Microscopy facility availability may differ
- Estimated corrected throughput at 1.5-1.6 comps/day based on qualitative cascade analysis of the 3 lunch-break tasks and 1 SEM daily-limit violation, rather than running a fully corrected scheduler simulation
- Scored Visual Design at B- (72) rather than C+ despite significant label overlap, because the R1 improvements (DPI, palette, text color, cooling distinction) represent meaningful progress and the figure is usable for internal review
- Assessed personnel feasibility assuming ~50% UG daytime availability (5 of 10 UGs available at any time) based on the R1 estimate of 15-18 credit-hour course loads
- Treated the 7-working-day span as the correct denominator for throughput calculation, matching the code's own methodology, rather than using an alternative like "days with completions" (5 days, which would give 12/5 = 2.4)
- Graded Throughput Claim Validity at B (82) rather than B+ because the SEM daily limit violation and lunch-break tasks create a systematic ~15% inflation; for a proposal, ~1.5 would be more defensible than 1.71
- Classified _task_fits_in_day() as dead code based on grep-level analysis showing no call sites in the current code; it may have been used in an earlier version before the _schedule_task refactoring
