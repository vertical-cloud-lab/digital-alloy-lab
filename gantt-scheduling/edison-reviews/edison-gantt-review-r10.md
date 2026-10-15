# R10 Review: FLAIME Experiment-Pipeline Gantt Chart

**Letter Grade: B**

This iteration successfully implements the R9 data-model fixes and R9 layout adjustments, bringing the utilization metrics into alignment with the caption and proposal. However, the PI’s feedback regarding shift coverage text overlap in the composite figure remains unresolved because the root cause was not addressed by the R9 layout tweaks. There is also a critical new inconsistency between the caption and the proposal narrative regarding undergraduate staffing numbers.

---

### 1. Per-Panel Text-Overlap Audit

**Composite Figure (`gantt_experiment_schedule.png`)**
*   **Panel (a) Shift coverage [P1 Severe]:** The PI is correct—the overlap persists at the bottom of the left strip. The bold x-axis label `"Shift coverage (≥2 UGs)"` collides heavily with three vertically staggered labels (`"Early 7-15"`, `"Mid 11-19"`, `"Late 14-22"`). 
    *   *Root cause:* The plotting loop evaluates `while d <= end_day` (where `end_day` is midnight the day *after* the schedule ends). This draws partial-day shift bars on the very last Tuesday whose time centers (e.g., 11:00, 15:00, 18:00) fall entirely outside the visible y-axis limit (`end_day = 00:00`). While the `Rectangle` patches are clipped, the `ax.text` annotations inside them default to `clip_on=False`, causing them to bleed directly into the x-axis label space below the spine. 
*   **Panel (b) Main compositions:** Clean. No collisions; gap-placed day labels render cleanly.
*   **Panel (c) Zoomed inlay:** Clean.
*   **Panel (d) Equipment hours:** Clean.
*   **Panel identifiers (a)–(d):** Clean.

**Standalone Subfigures**
*   **`shift_coverage.png` [P3 Minor]:** Borderline acceptable. Because the standalone figure has much more vertical headroom and suppresses the single-line x-tick labels (`show_xtick_labels=False`), the unclipped in-bar labels float staggered *below* the bold x-axis label. They don't overlap, but they look like a malformed or stray legend.
*   **All other subfigures** (`compositions_main`, `compositions_inlay`, `equipment_hours`, `legend`): Clean. No overlaps.

---

### 2. Caption ↔ Figure Consistency Check

**Status:** Mostly consistent, with one self-contradiction.
*   **Equipment utilization:** The caption accurately reflects the plotted 80h LPBF (24 on/56 off), 64h Atomizer (32 on/32 off), 32h SEM, and 16h AutoTrickler splits.
*   **Main panel throughput:** The caption correctly describes the 16 plotted compositions cascading at a rate of 3/weekday + 1 on Saturday.
*   **[P2] Staffing-concurrency contradiction:** The caption text for panel (a) states "≥3 are concurrent during peak shift overlap (14:00–15:00)", but the Headline Numbers section of the same file claims "≥4 concurrent during the 14:00–15:00 shift-overlap peak". Neither number makes sense mathematically: if all 3 shift bands (Early, Mid, Late) overlap between 14:00 and 15:00, and each requires ≥2 UGs, the true peak concurrency is ≥6.

---

### 3. Caption ↔ Proposal Consistency Check

**Status:** One critical contradiction and one minor framing discrepancy.
*   **[P1] Undergraduate staffing counts:** The proposal explicitly budgets for and describes "2 MS students, 10 undergraduate researchers" (PDF p. 2, p. 7, p. 30). The caption explicitly claims the team is "drawn from the 2 MS + 12 UG technician team" (line 74). This **10 vs. 12 UG mismatch** is a major inconsistency that reviewers will catch when cross-referencing the budget.
*   **[P3] Overall throughput ceiling:** The proposal (p. 4, p. 15) defines the Phase I target as "100–200 compositions." The caption (line 63) claims the schedule "supports ≥200 compositions." While technically true at steady-state, claiming a floor (≥200) that sits at the absolute ceiling of the proposal's range (100–200) may read as overpromising.

---

### 4. Status of R9 P1 (Atomizer split in data model)

**Status: RESOLVED.**
`schedule_data.json` now includes explicit `hands_on_h: 2.0` and `hands_off_h: 2.0` fields for all 16 `Atomization` tasks. The sum correctly yields 32 hours hands-on and 32 hours hands-off (64 hours total per week), perfectly matching the equipment hours panel and the caption text.

---

### 5. Recommended R11 Priority List (Ranked)

1.  **[P1] Fix panel (a) text bleed in `generate_gantt.py`:** Update the plotting loop to stop before the unplotted final day (`while d < end_day`), OR simply add `clip_on=True` to the `ax.text` call at line 1112 inside `_draw_shift_panel`. This will instantly resolve the PI's overlap complaint for both the composite and the standalone images.
2.  **[P1] Correct the UG staffing mismatch:** Change "12 UG technician team" to "10 UG technician team" in `gantt_figure_caption.md` to align with the proposal narrative and budget (pages 2, 7, 30).
3.  **[P2] Fix the concurrent-staffing math in the caption:** Reconcile the "≥3" and "≥4" concurrent staffing claims for the 14:00–15:00 peak overlap. If all three shift bands overlap at that hour with 2 UGs each, the number should be ≥6.
4.  **[P3] Soften the throughput framing:** Change "supports ≥200 compositions" to "supports the 100–200 composition Phase I target" in the caption to match the objective parameters on PDF pages 4 and 15.

***

*Discretionary analytical decisions:*
*   *Treated the stray staggered text at the bottom of the standalone `shift_coverage.png` as a P3 cosmetic issue rather than a P1 overlap, since it does not collide with other text elements in that specific rendering context.*
*   *Identified the "≥3" vs "≥4" concurrency claims as a P2 rather than P1 since they live purely in the unrendered caption markdown, but the underlying mathematical logic (3 shifts × 2 UGs = 6) suggests both numbers are fundamentally flawed.*