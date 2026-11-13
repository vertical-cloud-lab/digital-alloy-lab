# Edison R7 Gantt review (task cb627a75-b5e7-4a95-8bee-a7ec58f43fb6)

_Submitted 2026-04-17 after PI feedback that the combined figure still had overlap and spillover despite sub-panel exports. Job name: ANALYSIS._

## Query context

Panels attached: gantt_experiment_schedule.png (combined), subfigures/{shift_coverage,compositions_main,compositions_inlay,equipment_hours,legend}.png, generate_gantt.py, gantt_figure_caption.md, edison-gantt-review-r5.md.

## Answer

### TL;DR for PI

**Grade:** B (Sub-panels communicate their core ideas well but suffer from bleeding/clipping due to being cropped from a single matplotlib figure; some minor numerical text/label improvements needed).

**Top 3 highest-impact fixes:**
1. **Stop using `bbox_inches` crops for subfigures.** The "bleeding" (shift panel showing main Gantt labels, inlay showing slivers of midnight bars) is because `generate_gantt.py` draws one giant `GridSpec` and then crops it. You must refactor the plotting code to generate each subfigure as a standalone `plt.figure()` with its own axes.
2. **Fix the dual y-axis confusion in the combined view.** The main panel (spanning 9 days) and the zoomed inlay (spanning 20 hours) sit side-by-side sharing vertical space, but have completely different time scales. This makes the inlay's 06:00–00:00 y-axis labels look like they belong to the main panel. Move the inlay *below* the main panel, or at least add a strong visual separator.
3. **Correct the "114 h/wk" building denominator text in the caption.** The code schedules 16 compositions over an 8-day span (Mon–Mon, 6 weekdays + 1 Sat) which equals 108 building hours (6×17 + 1×6), not 114. The 114h figure is a leftover from a previous review that assumed different building hours (7–22).

---

### A) Single-Idea Communication
- **Shift Coverage:** Communicates the 3-shift overlap well, but in standalone mode it lacks y-axis labels (they belong to the main panel). 
- **Compositions Main:** Excellent communication of the diagonal 16-composition cascade.
- **Compositions Inlay:** Successfully highlights task-level sequencing (Dispense → Atomize → Cool, etc.) on a representative 2-hour scale.
- **Equipment Hours:** Clean, effective visualization of resource bottlenecks relative to a 40-h FTE workweek.
- **Legend:** Clear and category-focused.

### B) Text / Label Spillover
- **Shift Coverage (standalone):** The right-side text is severely clipped ("Monda", "Tuesda", "Wednesda") because the `bbox_inches` crop cuts through the main panel's y-axis labels. The orange "inlay →" text from the main panel also bleeds into this crop.
- **Inlay (standalone):** At the very bottom-left corner near 00:00, tiny colored bar slivers bleed into the frame. These are actually late-night bars from compositions 13–16 on the main panel getting caught in the inlay's crop box.
- **Main Panel:** Has no inside-bar labels (which successfully avoids repetition), but the inlay correctly labels only the longest >1.5h tasks (Atom, Print, SEM, Prep) to prevent visual clutter.

### C) Visual Overlap / Crowding in Combined Figure
- **Y-axis mismatch:** The main panel and inlay share the same vertical space (Row 0) but completely different time scales (9 days vs 20 hours). The inlay's time labels (06:00, 08:00) sit uncomfortably between the two panels, acting as a confusing "double y-axis".
- **"inlay →" marker:** This marker is plotted at x=0.38 on the main axes, which is technically off-chart (main x-axis starts at 0.4). This causes it to crowd the shared border with the shift panel.
- **Wasted space in inlay:** The top and bottom 1.5 hours of the inlay are hatched "building closed" zones. This vertical space could be reclaimed to make the working bars taller and labels more readable.

### D) Matplotlib Layout Recommendations
To resolve the PI's core complaint about "weird overlap":
1. **Drop the combined composition entirely.** Generate each panel as an independent `plt.figure(figsize=(...))` and `\includegraphics` them in the proposal LaTeX. This completely eliminates bleeding and shared-axis clipping.
2. **If a combined figure must be kept:** Move the zoomed inlay to a new row *below* the main panel. Side-by-side panels with radically different y-axis time scales are fundamentally confusing.
3. **Give the shift panel its own y-axis.** Do not use `sharey=ax_main`. Give `ax_shift` its own weekday labels so it works perfectly as a standalone PNG.

### E) Label Strategy (Keep vs. Drop)
The current balance is correct:
- **Main Panel:** Keep empty (no inside-bar labels). The color-coding + legend is sufficient to show the macro cascade.
- **Inlay:** Keep current logic (only label `{'Atom', 'Print', 'SEM', 'Prep'}` when `duration ≥ 1.5h`). Setup, Cool, Extract, and Sieve are too short and repetitive to label; their category colors tell the story.
- **Equipment Hours:** The `xlabel` says "(Atomizer / SEM / AutoTrickler are supervised; LPBF is unattended)", but 24 hours of the LPBF total is manual setup. Better phrasing: "...LPBF printing phase is unattended".

### F) Numerical / Scientific Correctness
- **Throughput:** 16 comps/week (3/weekday × 5 + 1 Sat) — **Correct** and verified by schedule output.
- **Equipment Hours:** LPBF 80h, Atomizer 64h, SEM 32h, Trickler 16h — **Correct** based on task durations × 16 compositions.
- **FTE Percentages:** LPBF 200%, Atomizer 160%, SEM 80%, Trickler 40% — **Correct** (Hours / 40h).
- **Shift / Bldg Denominators (Caption):** The caption text "bldg = 114 h/wk denominator" is **Incorrect** for the current code. The code uses 6:00–23:00 weekdays (17h) and 10:00–16:00 Saturday (6h). For a single 6-day workweek, that is 91 building hours (5×17 + 6). The actual 8-day scheduled span (Mon–Mon) uses 108 building hours (6×17 + 6). The 114h figure is a remnant from a previous schedule revision.

### G) Prioritized Patch List

**1. Refactor into independent figures instead of cropping:**
Replace the `bbox_inches` crop loop at the end of `plot_gantt_vertical` with dedicated rendering functions for each panel:
```python
def plot_shift_standalone(blocks, save_path): ...
def plot_main_standalone(blocks, save_path): ...
def plot_inlay_standalone(blocks, inlay_day, save_path): ...
```
**2. Fix the off-chart "inlay →" marker coordinate:**
In `generate_gantt.py`, move the marker into the visible coordinate space or remove it for standalone renders:
```python
# Change from x=0.38 to x=0.6 (inside the main chart area)
ax_main.text(0.6, (inlay_y0 + inlay_y1) / 2, "inlay →", ha="right"...)
```
**3. Give the shift panel its own y-axis tick labels:**
Remove `sharey=ax_shift` when creating the main panel, and explicitly add weekday labels to the shift panel so it can survive as a standalone image.
```python
ax_shift.yaxis.set_major_formatter(mdates.DateFormatter("%A"))
ax_shift.tick_params(axis="y", labelleft=True)
```
**4. Reduce wasted vertical space in the zoomed inlay:**
Change the padding from `pad_h = 1.5` to `pad_h = 0.25` so the inlay zooms closer on the actual working hours rather than the "building closed" hatching.
```python
pad_h = 0.25  # In plot_gantt_vertical()
```
**5. Correct the caption markdown denominator values:**
In `gantt_figure_caption.md`:
```markdown
# Change:
# shift = 76 h/wk denominator, bldg = 114 h/wk denominator
# To:
# shift = 76 h/wk denominator, bldg = 91 h/wk denominator (5 wkdy × 17h + 1 Sat × 6h)
```