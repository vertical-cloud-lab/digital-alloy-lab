### Edison Gantt Chart Review (R9)

**Grade: B−** (P2 caption fix confirmed; P1 atomizer data bug persists in schedule_data.json; P3 cannot be verified because image artifacts are absent from the workspace. A new caption-accuracy issue surfaces regarding the "≥3 people" staffing claim.)

---

#### 1. Verification of R8 Priorities

**[P1] Atomizer hands-on/hands-off split — NOT FIXED in data.**
`schedule_data.json` still contains 16 monolithic `Atomization` tasks, each 4.0 h with `is_automated: true`. Summing `requires_atomizer` tasks by automation flag yields **0 h hands-on + 64 h hands-off** — identical to R8. The caption (`gantt_figure_caption.md` line 50) and headline numbers (line 63) both correctly state "32 h hands-on melt prep / sieve + 32 h hands-off atomization & cool," but no data-level change supports this. Any figure generated from the current `schedule_data.json` will render the same 0+64 bar that R8 flagged. The underlying task model must be refactored (see R10 P1 below).

**[P2] Building-closed text ambiguity — FIXED in caption.**
`gantt_figure_caption.md` lines 23–25 now read: "Hatched bands mark hours **outside** the building-open windows (before 6:00 and after 23:00 on weekdays; outside 10:00–16:00 on Saturday…)." This is unambiguous. Cannot verify whether the in-figure legend patch text was also updated, because `generate_gantt.py` and the image files (`equipment_hours.png`, `gantt_experiment_schedule.png`) are not present in the workspace.

**[P3] Standalone shift_coverage.png bottom-margin crowding — CANNOT VERIFY.**
Neither `shift_coverage.png` nor `generate_gantt.py` is present. No visual verification is possible.

#### 2. Visual & Layout Assessment

**Cannot be performed.** The workspace contains only text artifacts (`schedule_data.json`, `schedule_summary.txt`, `gantt_figure_caption.md`). No PNG/SVG image files exist. Overlap, clipping, contrast, label collisions, and color confusion checks require the rendered images.

#### 3. Data Integrity & Numerical Consistency

All numbers that can be cross-checked between `schedule_data.json`, `schedule_summary.txt`, and `gantt_figure_caption.md` are internally consistent **except** the atomizer hands-on/off split (P1 above):

| Resource | Data total | Summary total | Caption total | hands-on (data) | hands-off (data) | Caption claim |
|---|---|---|---|---|---|---|
| LPBF | 80.0 h | 80.0 h | 80 h | 24.0 h | 56.0 h | 24 + 56 ✓ |
| Atomizer | 64.0 h | 64.0 h | 64 h | **0 h** | **64.0 h** | **32 + 32 ✗** |
| SEM | 32.0 h | 32.0 h | 32 h | 32.0 h | 0 h | all hands-on ✓ |
| AutoTrickler | 16.0 h | 16.0 h | 16 h | 16.0 h | 0 h | all hands-on ✓ |

**Throughput**: 3 compositions/weekday + 1 Saturday = 16/week. Confirmed from data — each weekday has exactly 3 atomization starts, Saturday has 1. ✓

**Resource collisions**: Zero collisions across all four shared resources (LPBF, Atomizer, SEM, AutoTrickler). ✓

**Task ordering**: All 16 compositions follow the same 13-step pipeline (Dispense → Atom → Cool → Sieve → Transfer → Setup → Print → Cool → Extract → Transfer → Prep → SEM → Mech) with no intra-composition overlaps. ✓

**Building-hours compliance**: No manual tasks run outside BYU building hours (6–23 wkdy, 10–16 Sat). Five passive powder-cooling tasks (C3, C6, C9, C12, C15) extend to ~22:50, inside the 23:00 building cutoff. ✓

**Utilization denominators**: The LPBF denominator of 108 h decomposes cleanly as 6 weekdays × 17 h (6–23) + 1 Saturday × 6 h (10–16). The BYU-resource denominator of 90 h does not decompose from stated hours (5 × 15 h [7–22] + 6 h [Sat 10–16] = 81 h, or 5 × 17 h [6–23] + 6 h = 91 h). It appears to assume 6 days × 15 h = 90 h, treating Saturday as a full 15-hour day. Minor denominator inconsistency.

#### 4. New Issues

**[N1] Caption staffing claim may overstate concurrent headcount.** `gantt_figure_caption.md` line 20 states "at least three people are on-site at any moment within the 7:00–22:00 staffed window." With three shift bands (Early 7–15, Mid 11–19, Late 14–22), the maximum concurrent coverage from distinct shifts is 3 (during 14:00–15:00 only); outside that window it drops to 1–2 shift-bands. The claim holds only if each shift is staffed by ≥2 people. The headline-numbers section (line 68) says "≥3 undergraduates concurrent on-site across 3 overlapping shifts (drawn from the 2 MS + 10 UG team)" but does not specify per-shift headcount. Either clarify that each shift block is staffed by ≥2 undergraduates, or weaken the claim to "≥1 person on-site at all times, with ≥3 concurrent during peak overlap."

**[N2] "Busiest weekday" phrasing for inlay.** The caption describes Tuesday as "the busiest weekday." All five weekdays are identical: 39 tasks, 54.0 h, 6 compositions each. The parenthetical "(Tuesday by way of example)" partially mitigates this, but "busiest" is strictly inaccurate. Replace with "a representative weekday."

**[N3] "Social window" for Saturday hours.** Line 21 calls the Saturday 10–16 window the "social window." This is nonstandard terminology for a DOE proposal audience. Consider "Saturday access hours" or "Saturday building hours."

**[N4] Missing image artifacts.** Without `generate_gantt.py` or any PNG output, it is impossible to confirm whether R9 code changes actually produced updated figures. The review cycle cannot close until rendered images are available for visual inspection.

---

### Actionable Priorities for R10

**[P1] Fix the atomizer hands-on/off split in the data model (CRITICAL — carried over from R8).**
The `schedule_data.json` Atomization tasks are still monolithic 4 h blocks with `is_automated: true`. Two approaches:
- **(a) Split each Atomization task** into a 2 h manual melt-prep sub-task (`is_automated: false, requires_atomizer: true`) followed by a 2 h automated atomization sub-task (`is_automated: true, requires_atomizer: true`). This is the cleanest fix and makes the data self-documenting.
- **(b) Override in the utilization computation** in `generate_gantt.py`: when computing the equipment-hours bar for the atomizer, hardcode `hands_on_frac = 0.5` for `requires_atomizer` tasks. Quick but fragile.
Either way, the rendered `equipment_hours.png` must show a 32 h solid-blue + 32 h hatched-orange stacked bar for the Atomizer row. Verify visually after regeneration.

**[P2] Regenerate and include all image artifacts.**
The workspace must contain the rendered PNGs (`gantt_experiment_schedule.png`, `equipment_hours.png`, `shift_coverage.png`, and the other standalone subfigures) so visual verification of P1/P2/P3 fixes and any new layout issues can be performed. Include `generate_gantt.py` as well.

**[P3] Clarify the staffing-concurrency claim and minor caption wording (LOW).**
In `gantt_figure_caption.md` line 20, change "at least three people are on-site at any moment" to either specify per-shift headcount (e.g., "with ≥2 undergraduates assigned to each shift, ensuring ≥3 concurrent") or weaken to "≥1 on-site at all times within 7–22, with ≥3 during peak overlap hours." Also fix "busiest weekday" → "a representative weekday" and "social window" → "Saturday building hours."

---

**Discretionary analytical decisions:**

- Defined "hands-on" as tasks with `is_automated: false` and `is_passive: false`, and "hands-off" as tasks with either flag true, matching the logic described in the R8 review
- Treated resource-collision detection as strict interval overlap (end > start of next) rather than allowing touching intervals (end == start)
- Evaluated the "≥3 people" staffing claim by counting distinct overlapping shift-bands rather than assuming multiple people per shift, since per-shift headcount is not specified in the data
- Used atomization start times to determine per-day composition counts (rather than dispensing or any other step)
- Flagged the 90 h denominator inconsistency as minor rather than critical, since it affects utilization percentages but not absolute hours
