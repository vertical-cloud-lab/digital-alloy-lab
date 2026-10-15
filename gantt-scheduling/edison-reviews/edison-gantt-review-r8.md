### Edison Gantt Chart Review (R8)

**Grade: B** (Significant layout/spillover improvements achieved by rendering standalone subfigures, but introduces a major domain/data bug regarding atomizer utilization, plus some minor labeling ambiguities).

The shift to independent `plt.figure()` renders for the subfigures completely resolved the bounding-box cropping issues from R7. The combined view is much cleaner, and the "inlay →" marker removal fixed the main panel overlap. However, the hands-on/hands-off split logic introduced a critical error in the equipment utilization data.

#### 1. Visual & Layout Assessment
- **Combined Figure:** Clean and legible at single-column width. Panel identifiers (a)–(d) are clear and correctly match the caption. No overlapping elements or clipped text remain in the combined view.
- **Standalone Subfigures:** Each survives independently. However, the standalone shift panel has a minor visual clutter issue: the in-bar text for the final row (`Early\n7-15`, etc.) sits immediately below the x-axis, creating the appearance of redundant/colliding x-axis labels. The aspect ratio of the standalone shift panel (3.5 × 9.0) is also quite tall and narrow.
- **Dual Y-Axis:** This remains visually awkward in the combined figure because the main panel (spanning 9 days) and the inlay (spanning 20 hours) sit side-by-side sharing vertical space but have entirely different time scales. A horizontal separator or moving the inlay below the main panel would be better, but the orange frame helps.

#### 2. Hands-on vs. Hands-off Split (Critical Bug)
The stacked-bar visualization is a huge improvement over the single-bar version, but the underlying data for the Atomizer is **incorrect**.
- **The Bug:** Panel (d) shows the Atomizer as `0 h hands-on + 64 h hands-off`. The PI explicitly requested a `32 h + 32 h` split, and the caption even correctly states the atomizer is "roughly half hands-on melt prep + QC". 
- **The Cause:** In `generate_gantt.py`, the `Atom` task is a monolithic 4-hour block flagged as `is_automated = True`. The utilization logic calculates `hands_on_h` by summing tasks that are `not is_automated`. Thus, the entire 64 hours of atomization gets dumped into the hands-off bucket. You must either split the `Atom` task into a manual prep phase + automated run phase, or hardcode/override the 50% split in the utilization computation for that specific resource.

#### 3. Caption & Legend Clarity
- **Ambiguous 'Closed' Labeling:** The legend includes a hatched patch labeled `Building closed (6–23 wkdy / 10–16 Sat)`. This reads as though the building is *closed* during those hours. Those are actually the building's *open* hours. The caption repeats this exact phrasing: "Hatched bands mark building-closed hours (6:00–23:00...".
- **Color Mentions:** Excellent. All colors (orange, magenta, blue, gray, pink, etc.) are mentioned inline with their respective concepts.
- **"Ship" vs "Transfer":** Successfully updated across all assets.

#### 4. Scientific / Operational Plausibility
- Throughput calculation (16 compositions/week = 2.29/working-day) is correct.
- LPBF utilization math (80h / 108 building-hours = 74.1%) is correct for the scheduled span.
- The 16-composition diagonal cascade maintains the 0-collision invariant perfectly.

---

### Actionable Priorities for R9

**[P1] Fix Atomizer hands-on/hands-off split:**
Refactor the pipeline task definitions or the utilization math so the Atomizer reflects the PI's `32 h hands-on + 32 h hands-off` reality, matching the caption text.

**[P2] Fix the 'Building closed' text ambiguity:**
Update line 1245 in `generate_gantt.py` and the corresponding caption text to clarify that 6–23 / 10–16 are the *open* windows. 
*Suggested fix:* `Building closed (outside 6–23 wkdy / 10–16 Sat)` or `Building hours: 6–23 wkdy / 10–16 Sat (closed otherwise)`.

**[P3] Clean up the standalone shift panel bottom margin:**
Consider setting `show_y_labels=False` or finding a way to prevent the bottom-most in-bar labels from crowding the x-axis area when rendered as a standalone subfigure.