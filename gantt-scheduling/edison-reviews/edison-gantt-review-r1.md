
# FLAIME Alloy Experiment Pipeline — Gantt Schedule Audit Report

## Overall Grade: C+ (58/100)

| Category | Grade | Score |
|---|---|---|
| Scheduling Engine Logic | D | 40/100 |
| Task Duration Realism | C | 60/100 |
| Visual Design | C+ | 62/100 |
| Code Quality | B- | 72/100 |
| Throughput Claim Validity | D+ | 45/100 |
| Documentation | B+ | 82/100 |

---

## 1. Scheduling Realism

**12 compositions Mon–Fri = 2.4/day is NOT sustainable.** This throughput figure is an artifact of scheduling engine bugs, not a realistic achievement:

- **Compositions 9–12 have identical early-stage timing** (all start Tue 07:00 with identical Screen→Dispense→Atomize→Sieve sequences) due to a pipeline offset bug. This means 4 compositions are scheduled to use the same atomizer and AutoTrickler simultaneously — physically impossible.
- **Compositions 7–8 also partially collapse** (both Dispense at Tue 07:00-08:00, both Atomize at Tue 08:00-10:30).
- **Atomizer overlaps**: 11 overlapping task pairs detected, including 5 full overlaps (Comps 7-12).
- **AutoTrickler overlaps**: 5 overlapping task pairs (Comps 8-12 all dispense simultaneously).
- **5 manual tasks scheduled after the 6 PM shift end** (Mech testing for Comps 1, 4, 7, 10 runs 18:00-19:00; Comp 6 Dispense runs 17:30-18:30).
- **5 manual tasks cross the lunch break** (Comp 3 Dispense 11:30-12:30, Comp 3/6/9/12 Prep 11:30-12:30).

With bugs fixed and realistic resource tracking, throughput would likely drop to **~1.2–1.5 compositions/day** (6–9 per week), not 12.

---

## 2. Visual Design Assessment

**Strengths:**
- Color coding by task type is effective conceptually
- Hatching pattern for automated tasks is a good distinction
- Sunday/off-hours shading communicates schedule constraints
- LPBF utilization annotation is informative

**Weaknesses (not publication-ready):**
- White text on colored bars is illegible on light backgrounds (SEM/Mech/Prep bars)
- 7pt labels too small for grant figures; minimum should be 8-9pt
- Figure size (22" × ~18" at 200 DPI) is far too large for a standard NSF/DOD proposal figure slot
- X-axis labels are cluttered (rotated 45° with "Day HH:MM" across 5 days)
- Comps 9-12 have perfectly overlapping bars due to the scheduling bug, creating a misleading visual
- Drive blocks are nearly invisible thin gray slivers
- Legend has 13 entries in 4 columns — too dense
- Screen and AI Update share the same color (#4C72B0), undermining the color-coding scheme
- No colorblind-safe palette

**Recommendations:** Compress to 7" wide, use black text labels above bars, use Okabe-Ito palette, compress non-working hours, show 5-6 representative compositions, add critical path highlighting.

---

## 3. Missing Real-World Constraints

**Missing from the schedule:**

| Constraint | Impact | Estimated Duration |
|---|---|---|
| Powder cooling after atomization | Safety-critical (hot reactive Al powder) | 30–60 min |
| LPBF build plate cool-down | Required before safe extraction | 30–60 min |
| LPBF chamber cleaning between compositions | Critical for avoiding cross-contamination when switching alloy powders | 30–60 min |
| SEM facility booking limits | BYU Microscopy is a shared university resource with advance booking | ~4h/day max availability |
| Student class schedules | UGs have 15-18 credit hours; availability is fragmented | Reduces effective labor pool by ~50% during class hours |
| Wire EDM time (if used for extraction) | Notes mention Wire EDM but duration assumes manual removal | 2–4h vs. 0.5h |
| Sample prep curing time | Epoxy mount cure is 45-60 min alone | Doubles the Prep duration |
| SEM pump-down and sample exchange | Each sample load requires vacuum cycle | 15–30 min per session |
| LPBF atmosphere purge | Ar/N₂ fill for fresh build | 15–30 min (included in expanded Setup) |
| Sieving station availability | Only 1 sieve set; sequential use required | Already violated in schedule |

---

## 4. Pipeline Bug: Root Cause of Comp 9-12 Collapse

**Root cause identified in `schedule_compositions()` (line 375-377):**

```python
comp_start = start_date + timedelta(hours=pipeline_offset_h * (comp_id - 1))
```

This computes raw calendar-time offsets that ignore working hours:
- Comp 8: Mon 07:00 + 14h = Mon 21:00
- Comp 9: Mon 07:00 + 16h = Mon 23:00
- Comp 10: Mon 07:00 + 18h = Tue 01:00
- Comp 11: Mon 07:00 + 20h = Tue 03:00
- Comp 12: Mon 07:00 + 22h = Tue 05:00

All five after-hours timestamps snap to **Tue 07:00** via `_earliest_auto_start()`, producing identical schedules for the first 4 pipeline stages. Comps 7-8 also partially collapse (both start dispensing at Tue 07:00).

**Secondary bug amplifying the problem:** The atomizer and AutoTrickler are not tracked as shared resources, so even the identical-start compositions aren't forced apart by resource contention.

**Fix:** Replace the fixed-offset approach with an event-driven scheduler where each composition starts when the earliest shared resource becomes free, OR implement a working-hours-aware offset function that only counts staffed hours.

---

## 5. Throughput Validation

**The schedule does NOT reliably demonstrate ~2 compositions/day throughput.**

| Metric | Value |
|---|---|
| Compositions scheduled | 12 |
| Working days used | 5 (Mon–Fri; Saturday not used despite being claimed) |
| Raw throughput | 2.4/day |
| Completions by day | Mon:1, Tue:3, Wed:3, Thu:3, Fri:2 |
| LPBF total time | 48.0h (4.0h per composition) |
| LPBF utilization | 64% of available hours |
| Theoretical LPBF max | 3.75 comps/day (15h available ÷ 4h per comp) |

**However, the 2.4/day figure is artificially inflated by bugs:**
- Comps 9-12 use the same atomizer and trickler simultaneously (impossible)
- 5 manual tasks run after the evening shift ends
- No cooling times, no chamber cleaning, no transit delays enforced
- Task durations underestimate reality by ~36% (12.5h current vs. ~17.0h realistic)

**Corrected estimate:** With all bugs fixed and realistic durations, the LPBF bottleneck alone limits throughput to ~2 comps/day (4h LPBF per comp, 8h of LPBF in a staffed window). But the front-end bottleneck (dispensing + atomization = 3.5h serial per comp on single shared equipment) further constrains to ~1.5 comps/day. Adding cooling times, chamber cleaning, and transit pushes this toward **~1.0–1.5 comps/day realistic steady-state**.

---

## 6. Code Quality Assessment

**Strengths:**
- Clean, well-structured Python with PEP 8 compliance
- Excellent docstrings throughout (module-level, function-level, class-level)
- Good use of dataclasses for PipelineTask and ScheduledBlock
- Clean separation of concerns: scheduling, drive computation, plotting, summary
- JSON export for downstream use is thoughtful
- Type hints throughout

**Bugs:**
1. **CRITICAL:** `_schedule_task()` checks manual task end against `_day_end()` (22:00) instead of shift end (18:00) — manual tasks can run after staff leave
2. **CRITICAL:** `_schedule_task()` doesn't check if manual tasks cross the lunch break (12:00-13:00)
3. **CRITICAL:** Pipeline offset in `schedule_compositions()` uses raw timedelta, not working-hours-aware arithmetic
4. **CRITICAL:** Atomizer and AutoTrickler not tracked as shared resources (only LPBF and SEM are)
5. **MAJOR:** `_compute_drives()` creates visual-only blocks; transit time not integrated into scheduling logic
6. **MINOR:** Lines 337-340 — automated task check against `auto_end` is redundant with the `day_e` check since both equal `WEEKDAY_END`

**Edge cases:**
- Sunday start date handled correctly ✓
- Date verification: Sep 7, 2026 is indeed Monday ✓
- Saturday shift logic present but never triggered (no work reaches Saturday)

---

## Prioritized Changes (Implementation Order)

### PRIORITY 1 — CRITICAL
1. **P1.1** Fix pipeline offset to use working-hours arithmetic (or event-driven scheduling)
2. **P1.2** Track atomizer as shared resource (`atomizer_free_after`)
3. **P1.3** Track AutoTrickler as shared resource (`trickler_free_after`)
4. **P1.4** Enforce shift boundaries for manual tasks (18:00 end, lunch break gap)

### PRIORITY 2 — MAJOR
5. **P2.1** Integrate transit times into scheduling (not just visualization)
6. **P2.2** Add powder cooling time after atomization (30-60 min)
7. **P2.3** Add LPBF build plate cool-down between compositions (30-60 min)
8. **P2.4** Add LPBF chamber cleaning for powder changeover (30-60 min)
9. **P2.5** Revise task durations to realistic values (+36% overall)

### PRIORITY 3 — MODERATE
10. **P3.1** Add SEM facility booking constraint (limited daily availability)
11. **P3.2** Add personnel assignment model (verify no single person is double-booked)
12. **P3.3** Redesign as event-driven scheduler (composition starts when resources free)
13. **P3.4** Actually use Saturday hours or remove the "6 days/week" claim

### PRIORITY 4 — VISUAL
14. **P4.1** Resize figure for grant proposals (7" wide, 300 DPI)
15. **P4.2** Use black text labels above/beside bars
16. **P4.3** Adopt colorblind-safe palette
17. **P4.4** Compress non-working hours in the time axis
18. **P4.5** Add critical path highlighting
19. **P4.6** Show 5-6 representative compositions, not all 12
20. **P4.7** Add companion capacity utilization panel

---

## Discretionary Analytical Decisions

- Classified the pipeline offset bug as "CRITICAL" rather than "MAJOR" because it causes 4 of 12 compositions to have physically impossible identical schedules, fundamentally undermining the throughput claim
- Estimated "realistic" task durations (e.g., Sample Prep 2.0h, SEM 2.5h, LPBF Setup 1.0h) based on general metallography and SEM practice norms; actual BYU lab workflows could differ
- Categorized the atomizer as a single shared resource based on the workflow review describing one ultrasonic atomization system; if the lab acquires multiple atomizers, this constraint would relax
- Assessed the 0.5h Sieve/QC as optimistic based on inclusion of PSD analysis and flowability testing in the task notes; if only visual sieving is done, 0.5h may be sufficient
- Used a 3-tier severity scale (Critical/Major/Minor) rather than a continuous scale for bug classification
- Estimated corrected throughput at 1.0-1.5 comps/day based on back-of-envelope LPBF and atomizer bottleneck analysis rather than running a fully corrected scheduler simulation
- Scored "Code Quality" at B- (72/100) despite critical bugs, because the code structure, documentation, and Python practices are genuinely good — the issues are in domain logic, not software engineering
- Classified transit time enforcement as "MAJOR" rather than "CRITICAL" because campus transit times (10-15 min) are relatively short compared to task durations, so the scheduling impact is moderate (~2h total across 12 compositions)
- Assessed Wire EDM extraction duration as 2-4h based on general AM post-processing practice; if the lab uses manual removal (bandsaw/chisel) exclusively, 0.5h may be closer to realistic
- Included LPBF chamber cleaning as a separate constraint rather than folding it into Setup duration, because cross-contamination prevention between alloy compositions is a distinct operational concern that should be explicitly modeled
