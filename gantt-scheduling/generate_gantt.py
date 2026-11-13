#!/usr/bin/env python3
"""Generate a Gantt scheduling chart for the FLAIME alloy experiment pipeline.

Models the daily/weekly workflow for the BYU Vertical Cloud Lab (VCL) alloy
development pipeline, accounting for:
  - Building hours and shift schedules (morning/evening, 6 days/week)
  - Reduced Saturday hours
  - Locational considerations (drives between BYU campus buildings)
  - LPBF printer, atomizer, and AutoTrickler as shared bottleneck resources
  - SEM facility booking limits (shared university resource)
  - Automated vs. manual steps with shift-boundary enforcement
  - Cooling/cleaning times between compositions (powder cool-down, LPBF
    chamber cleaning, build-plate cool-down)
  - Campus transit integrated into scheduling (not just visualization)
  - Asynchronous pipeline parallelism (atomize N+1 while printing N while
    characterizing N-1)

Target throughput: 3 unique compositions/day weekdays, 1/day Saturday
(= 16 compositions/week), 9-month Phase I.  Enabled by extended staffed
atomizer coverage (7 AM–10 PM weekdays) and a 3-person-minimum on-site
staffing rotation drawn from 2 MS + 10 UG team (three concurrent workers
provides single-person-out redundancy).  Saturday throughput is reduced
to 1/day for social reasons (10 AM–4 PM effective window).

Pipeline stages (per composition):
  1.  Powder dispensing via AutoTrickler               (manual, ~1.0 h)
  2.  Ultrasonic atomization                           (automated, ~4.0 h)
  3.  Powder cooling                                   (passive wait, ~0.5 h)
  4.  Powder sieving & QC                              (manual, ~0.5 h)
  5.  Ship powder BYU → U of Utah                      (manual, ~0.75 h)
  6.  LPBF chamber prep & powder changeout             (manual, ~1.5 h)
  7.  LPBF printing                                    (automated, ~3.0 h)
  8.  Build-plate cool-down                            (passive wait, ~0.5 h)
  9.  Build-plate removal & specimen extraction         (manual, ~0.5 h)
  10. Ship samples U of Utah → BYU                     (manual, ~0.75 h)
  11. Sample preparation (mounting, polishing, cure)    (manual, ~2.0 h)
  12. SEM/EDS/EBSD characterization                    (semi-auto, ~2.0 h)
  13. Mechanical testing (hardness + PIP)              (semi-auto, ~1.0 h)

Note: Thermo-Calc / Bayesian composition screening is *not* modeled as a
per-composition Gantt task — it runs 24/7 as a continuous batch process on
BYU HPC and is never on the critical path.  Data upload / AI-model update
is housekeeping and similarly omitted.

References:
  - alloy-workflow-review.md (pipeline status)
  - FLAIME personnel: PI + 2 MS students + 10 UGs @ $30/hr
  - Issue #54: Gantt scheduling chart for experiments
  - Edison R1 review: C+ grade with critical fixes implemented
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# ── Schedule constants ────────────────────────────────────────────────────────

# BYU Clyde Engineering / Crabtree Technology Building access hours
# (PI-confirmed 2026-04-17: building open 6 AM–11 PM M–Sa; Saturday
# effective window reduced to 10 AM–4 PM for social/staffing reasons.)
WEEKDAY_START = 6   # 6:00 AM (building opens)
WEEKDAY_END = 23    # 11:00 PM (building closes)

SATURDAY_START = 10  # 10:00 AM (effective start for social reasons)
SATURDAY_END = 16    # 4:00 PM (effective end)

# Staffed shift windows (24-h clock) — manual / supervised work only during
# these windows.  Weekday staffing 7 AM–10 PM (tighter than building hours
# "to be safe") covers startup/shutdown of atomizer runs throughout the day.
# With 3-person-minimum on-site rotation (≥2 always present for redundancy),
# sustained 3 atomizations/day on weekdays is feasible.
MORNING_SHIFT = (7, 12)    # 7 AM – 12 PM (5 h)
LUNCH_BREAK = (12, 13)     # 12 PM – 1 PM
EVENING_SHIFT = (13, 22)   # 1 PM – 10 PM (9 h)
SATURDAY_SHIFT = (10, 16)  # 10 AM – 4 PM (6 h, single shift, no lunch)

# Manual shift end on weekdays — manual tasks must finish by 10 PM
MANUAL_SHIFT_END = 22

# After-hours automated window (fully unattended equipment only after 10 PM)
AUTO_EVENING = (22, 23)  # 10 PM – 11 PM automated only

# Minimum on-site staffing (single-person-out redundancy).  Not enforced in
# the scheduler — documented here for proposal/budget cross-reference.
STAFFING_MIN_CONCURRENT = 3

# ── Plotting constants ────────────────────────────────────────────────────────

# Vertical spacing between composition rows (>1.0 prevents above/below label
# of adjacent rows from colliding)
ROW_STEP = 1.35
BAR_HEIGHT = 0.6

# Label-placement thresholds (bar duration in hours)
LABEL_INSIDE_MIN_H = 2.5   # only bars ≥ 2.5 h get inside-bar labels
LABEL_OUTSIDE_MIN_H = 0.8  # bars 0.8–2.5 h get above/below labels
# Tolerance for threshold comparisons — mdates.date2num conversion can
# introduce sub-millisecond float error, e.g. an exact 2.5 h bar comes back
# as 2.4999999h. Using −0.01 h (~36 s) ensures same-duration bars always get
# the same label placement.
LABEL_THRESHOLD_TOL_H = 0.01

# Locations — BYU Clyde/Engineering Bldg houses VCL (atomizer, AutoTrickler),
# the microscopy facility, and workbench prep space; LPBF is off-site at
# University of Utah, so inter-campus shipping is the only real transit.
LOC_BYU_CLYDE = "BYU-Clyde"          # Atomizer, AutoTrickler, prep space
LOC_BYU_MICROSCOPY = "BYU-Micro"   # SEM/EDS/EBSD facility (same building)
LOC_UOFU = "U of Utah"             # Off-site LPBF printer
LOC_TRANSIT = "Transit"            # Inter-campus shipping BYU ↔ U of U

# ── Colorblind-safe palette (Okabe-Ito, category-grouped) ────────────────────
# https://jfly.uni-koeln.de/color/
# Per-task colors retired in favor of category colors so the figure reads as
# four pipeline stages instead of ~12 individual tasks.

OI_BLUE = "#0072B2"
OI_ORANGE = "#E69F00"
OI_GREEN = "#009E73"
OI_RED = "#D55E00"
OI_PURPLE = "#CC79A7"
OI_YELLOW = "#F0E442"
OI_CYAN = "#56B4E9"
OI_BLACK = "#000000"
OI_GREY = "#999999"
OI_BROWN = "#8B6914"

# Pipeline-category colors — each task is tagged with one category and
# rendered in the category color. Sub-task granularity (Setup vs Print vs
# Cool vs Extract) is preserved via inside-bar labels, but colored alike so
# the viewer sees stages rather than an overwhelming 12-color palette.
CAT_FEEDSTOCK = "Feedstock (atomizer)"   # Dispense, Atomize, Cool, Sieve
CAT_PRINT = "Printing (LPBF, U of U)"    # Setup, Print, Cool, Extract
CAT_CHARACTERIZE = "Characterization"    # Prep, SEM, Mech
CAT_TRANSIT = "Transfer BYU ↔ U of U"    # Inter-campus courier

CATEGORY_COLORS: dict[str, str] = {
    CAT_FEEDSTOCK: OI_ORANGE,
    CAT_PRINT: OI_PURPLE,
    CAT_CHARACTERIZE: OI_BLUE,
    CAT_TRANSIT: "#BBBBBB",
}
OI_TRANSIT = CATEGORY_COLORS[CAT_TRANSIT]

# ── Pipeline task definitions ────────────────────────────────────────────────


@dataclass
class PipelineTask:
    """A single task in the alloy-experiment pipeline."""
    name: str
    short_name: str
    duration_h: float
    is_automated: bool     # True → can run unattended (building hours, not shift)
    is_passive: bool       # True → passive wait (cooling); no personnel/equipment
    location: str
    personnel: str
    category: str = CAT_FEEDSTOCK
    requires_lpbf: bool = False
    requires_sem: bool = False
    requires_atomizer: bool = False
    requires_trickler: bool = False
    # Optional override for hands-on (supervised) hours within this task.
    # If None, hands-on hours default to the full duration for manual tasks
    # and 0 for automated or passive tasks.  Use this when a single
    # scheduled block mixes supervised and unattended phases — e.g. the
    # Atomization block is 1.5 h supervised changeout + 2.0 h automated
    # run + 0.5 h supervised collect/clean, so hands_on_h=2.0 of 4.0.
    hands_on_h: Optional[float] = None
    notes: str = ""

    @property
    def color(self) -> str:
        return CATEGORY_COLORS[self.category]


# Pipeline tasks (post-PI-R6 review):
#   * "Comp. screening" removed — Thermo-Calc BO runs 24/7 on BYU HPC as a
#     continuous background process; it is not a per-composition Gantt item.
#   * "Data upload & AI update" removed — automated pipeline housekeeping,
#     not a scheduling constraint.
#   * "Transit VCL→Crabtree" removed — VCL, workbench, and SEM are all in
#     the Clyde/Engineering Bldg, so intra-building moves are not tasks.
#   * Transit now represents inter-campus shipping to the off-site LPBF at
#     U of Utah (~45 min drive each way between Provo and Salt Lake City).
PIPELINE_TASKS = [
    PipelineTask(
        name="Powder dispensing",
        short_name="Dispense",
        duration_h=1.0,
        is_automated=False,
        is_passive=False,
        location=LOC_BYU_CLYDE,
        personnel="UG",
        category=CAT_FEEDSTOCK,
        requires_trickler=True,
        notes="AutoTrickler v4; manual loading",
    ),
    # Atomizer scheduling note: The atomizer is classified as automated because
    # the 2h atomization phase runs semi-autonomously.  However, startup (melt
    # prep, feedstock changeout, purge) and shutdown (powder collection, nozzle
    # cleaning) require operator presence during shift hours — ~1.5h changeout
    # matches typical LPBF powder changeout time reported by BYU CMDRI.
    # The 4h block may be *initiated* during shift hours and extend into the
    # evening.  For utilization, we use shift-hour capacity as the denominator
    # because the operator-dependent startup/shutdown steps constrain how many
    # runs can be *started* per day.  With 15 h staffed window (7:00–22:00)
    # and 4 h per run, 3 atomizations/day is achievable on weekdays given the
    # 3-person-minimum staffing rotation; Saturday is capped at 1/day due to
    # the 6 h effective window (10:00–16:00).
    PipelineTask(
        name="Atomization",
        short_name="Atom",
        duration_h=4.0,
        is_automated=True,
        is_passive=False,
        location=LOC_BYU_CLYDE,
        personnel="UG (supervised)",
        category=CAT_FEEDSTOCK,
        requires_atomizer=True,
        hands_on_h=2.0,  # 1.5 h prep/changeout + 0.5 h collect/clean (2 h of 4 h block)
        notes="1.5 h changeout/prep + 2.0 h atomize + 0.5 h collect/clean",
    ),
    PipelineTask(
        name="Powder cooling",
        short_name="Cool",
        duration_h=0.5,
        is_automated=True,
        is_passive=True,
        location=LOC_BYU_CLYDE,
        personnel="None (passive)",
        category=CAT_FEEDSTOCK,
        notes="Safety: hot reactive Al powder must cool",
    ),
    PipelineTask(
        name="Sieving & QC",
        short_name="Sieve",
        duration_h=0.5,
        is_automated=False,
        is_passive=False,
        location=LOC_BYU_CLYDE,
        personnel="UG",
        category=CAT_FEEDSTOCK,
        notes="PSD check, flowability",
    ),
    PipelineTask(
        name="Transfer BYU→U of U",
        short_name="Transfer",
        duration_h=0.75,
        is_automated=False,
        is_passive=False,
        location=LOC_TRANSIT,
        personnel="Student courier",
        category=CAT_TRANSIT,
        notes="Inter-campus drive, ~45 min Provo→SLC",
    ),
    PipelineTask(
        name="LPBF setup & changeout",
        short_name="Setup",
        duration_h=1.5,
        is_automated=False,
        is_passive=False,
        location=LOC_UOFU,
        personnel="MS student",
        category=CAT_PRINT,
        requires_lpbf=True,
        notes="Powder changeout, params, Ar purge, cleaning (~1.5 h)",
    ),
    PipelineTask(
        name="LPBF printing",
        short_name="Print",
        duration_h=3.0,
        is_automated=True,
        is_passive=False,
        location=LOC_UOFU,
        personnel="Unattended (monitored)",
        category=CAT_PRINT,
        requires_lpbf=True,
        notes="Automated; can run into evening window",
    ),
    PipelineTask(
        name="Build-plate cool-down",
        short_name="Cool",
        duration_h=0.5,
        is_automated=True,
        is_passive=True,
        location=LOC_UOFU,
        personnel="None (passive)",
        category=CAT_PRINT,
        requires_lpbf=True,
        notes="Cool before safe extraction",
    ),
    PipelineTask(
        name="Extraction",
        short_name="Extract",
        duration_h=0.5,
        is_automated=False,
        is_passive=False,
        location=LOC_UOFU,
        personnel="MS student / UG",
        category=CAT_PRINT,
        notes="Build plate removed; extraction at workbench",
    ),
    PipelineTask(
        name="Transfer U of U→BYU",
        short_name="Transfer",
        duration_h=0.75,
        is_automated=False,
        is_passive=False,
        location=LOC_TRANSIT,
        personnel="Student courier",
        category=CAT_TRANSIT,
        notes="Inter-campus drive, ~45 min SLC→Provo",
    ),
    PipelineTask(
        name="Sample prep",
        short_name="Prep",
        duration_h=2.0,
        is_automated=False,
        is_passive=False,
        location=LOC_BYU_MICROSCOPY,
        personnel="UG",
        category=CAT_CHARACTERIZE,
        notes="Mount, grind, polish + epoxy cure",
    ),
    PipelineTask(
        name="SEM/EDS/EBSD",
        short_name="SEM",
        duration_h=2.0,
        is_automated=False,
        is_passive=False,
        location=LOC_BYU_MICROSCOPY,
        personnel="MS student / UG",
        category=CAT_CHARACTERIZE,
        requires_sem=True,
        notes="Pump-down, imaging, composition maps",
    ),
    PipelineTask(
        name="Mechanical testing",
        short_name="Mech",
        duration_h=1.0,
        is_automated=False,
        is_passive=False,
        location=LOC_BYU_MICROSCOPY,
        personnel="UG",
        category=CAT_CHARACTERIZE,
        notes="Vickers hardness + PIP indentation",
    ),
]

# ── Scheduling engine ─────────────────────────────────────────────────────────


@dataclass
class ScheduledBlock:
    """A scheduled time-block for one task on one composition."""
    composition_id: int
    task: PipelineTask
    start: datetime
    end: datetime


@dataclass
class ResourceTracker:
    """Tracks when shared resources become free."""
    lpbf_free: datetime
    sem_free: datetime
    atomizer_free: datetime
    trickler_free: datetime

    def earliest_for(self, task: PipelineTask) -> datetime:
        """Return the earliest time this task can start given resource locks."""
        t = datetime.min
        if task.requires_lpbf:
            t = max(t, self.lpbf_free)
        if task.requires_sem:
            t = max(t, self.sem_free)
        if task.requires_atomizer:
            t = max(t, self.atomizer_free)
        if task.requires_trickler:
            t = max(t, self.trickler_free)
        return t

    def release(self, task: PipelineTask, end: datetime) -> None:
        """Mark resources used by *task* as free after *end*."""
        if task.requires_lpbf:
            self.lpbf_free = end
        if task.requires_sem:
            self.sem_free = end
        if task.requires_atomizer:
            self.atomizer_free = end
        if task.requires_trickler:
            self.trickler_free = end


def _is_saturday(dt: datetime) -> bool:
    return dt.weekday() == 5


def _is_sunday(dt: datetime) -> bool:
    return dt.weekday() == 6


def _day_start(dt: datetime) -> datetime:
    """Return the start-of-work for the day containing *dt*."""
    if _is_saturday(dt):
        return dt.replace(hour=SATURDAY_START, minute=0, second=0, microsecond=0)
    return dt.replace(hour=WEEKDAY_START, minute=0, second=0, microsecond=0)


def _manual_end(dt: datetime) -> datetime:
    """Return the end of staffed manual work for the day containing *dt*."""
    if _is_saturday(dt):
        return dt.replace(hour=SATURDAY_SHIFT[1], minute=0, second=0, microsecond=0)
    return dt.replace(hour=MANUAL_SHIFT_END, minute=0, second=0, microsecond=0)


def _auto_end(dt: datetime) -> datetime:
    """Return the end of automated/building hours for the day."""
    if _is_saturday(dt):
        return dt.replace(hour=SATURDAY_END, minute=0, second=0, microsecond=0)
    return dt.replace(hour=WEEKDAY_END, minute=0, second=0, microsecond=0)


def _next_workday_start(dt: datetime) -> datetime:
    """Advance to the start of the next working day (skip Sunday)."""
    nxt = (dt + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    if _is_sunday(nxt):
        nxt += timedelta(days=1)
    return _day_start(nxt)


def _earliest_manual_start(dt: datetime) -> datetime:
    """Earliest time manual (staffed) work can begin at or after *dt*.

    Manual work: weekday morning (7-12) + evening (13-22), Saturday (10-16).
    Skips lunch break on weekdays.
    """
    if _is_sunday(dt):
        dt = _next_workday_start(dt)

    day_s = _day_start(dt)

    if _is_saturday(dt):
        sat_end = dt.replace(hour=SATURDAY_SHIFT[1], minute=0, second=0)
        if dt < day_s:
            return day_s
        if dt <= sat_end:
            return max(dt, day_s)
        return _next_workday_start(dt)

    # Weekday
    morning_start = dt.replace(hour=MORNING_SHIFT[0], minute=0, second=0)
    morning_end = dt.replace(hour=MORNING_SHIFT[1], minute=0, second=0)
    lunch_end = dt.replace(hour=LUNCH_BREAK[1], minute=0, second=0)
    shift_end = dt.replace(hour=MANUAL_SHIFT_END, minute=0, second=0)

    if dt < morning_start:
        return morning_start
    if dt < morning_end:
        return dt
    if dt < lunch_end:
        return lunch_end
    if dt <= shift_end:
        return dt
    return _next_workday_start(dt)


def _earliest_auto_start(dt: datetime) -> datetime:
    """Earliest time automated/passive work can begin at or after *dt*.

    Automated work runs during all building-open hours (6 AM–11 PM weekdays,
    10 AM–4 PM Saturday effective).
    """
    if _is_sunday(dt):
        dt = _next_workday_start(dt)
    day_s = _day_start(dt)
    day_e = _auto_end(dt)
    if dt < day_s:
        return day_s
    if dt <= day_e:
        return dt
    return _next_workday_start(dt)



def _schedule_task(
    task: PipelineTask,
    earliest: datetime,
    resources: ResourceTracker,
) -> tuple[datetime, datetime]:
    """Find the [start, end) window for *task* beginning no earlier than
    *earliest*, respecting resource constraints and shift boundaries.

    Manual tasks are constrained to staffed shifts (13-22 weekdays;
    10-16 Saturday). Automated tasks can run during full building hours.
    Passive tasks (cooling) can span any building-open period.
    """
    dur = timedelta(hours=task.duration_h)
    is_manual = not task.is_automated and not task.is_passive

    # Resource constraint
    t = max(earliest, resources.earliest_for(task))

    # Transit tasks: snap to manual start, check shift boundary
    if task.location == LOC_TRANSIT:
        t = _earliest_manual_start(t)
        if t + dur > _manual_end(t):
            t = _next_workday_start(t)
            t = _earliest_manual_start(t)
        return t, t + dur

    # Snap to valid shift window
    if is_manual:
        t = _earliest_manual_start(t)
    else:
        t = _earliest_auto_start(t)

    # Check lunch-break crossing for manual weekday tasks
    if is_manual and not _is_saturday(t) and not _is_sunday(t):
        lunch_s = t.replace(hour=LUNCH_BREAK[0], minute=0, second=0)
        lunch_e = t.replace(hour=LUNCH_BREAK[1], minute=0, second=0)
        if t <= lunch_s and t + dur > lunch_s:
            # Would cross lunch — push to after lunch
            t = lunch_e

    # Determine day boundary
    if is_manual:
        day_limit = _manual_end(t)
    else:
        day_limit = _auto_end(t)

    if t + dur <= day_limit:
        return t, t + dur

    # Doesn't fit today → advance workdays until the task fits in a shift.
    # Safety cap of 14 iterations (~2 weeks) prevents infinite loops if a
    # task duration is longer than any available shift window.
    for _ in range(14):
        t = _next_workday_start(t)
        t = max(t, resources.earliest_for(task))
        if is_manual:
            t = _earliest_manual_start(t)
            day_limit = _manual_end(t)
        else:
            t = _earliest_auto_start(t)
            day_limit = _auto_end(t)
        if t + dur <= day_limit:
            return t, t + dur

    # Give up safely — schedule at cursor (should never hit with real tasks)
    return t, t + dur


def _advance_work_hours(start: datetime, hours: float) -> datetime:
    """Advance *hours* of working time from *start*, counting only staffed
    shift hours (morning + evening on weekdays, single shift on Saturday).
    Used to stagger composition start times in work-hours, not wall-clock.
    """
    remaining = timedelta(hours=hours)
    t = start

    for _ in range(100):  # safety bound
        if remaining <= timedelta(0):
            return t

        t = _earliest_manual_start(t)

        if _is_saturday(t):
            sat_end = t.replace(hour=SATURDAY_SHIFT[1], minute=0, second=0)
            available = sat_end - t
            if remaining <= available:
                return t + remaining
            remaining -= available
            t = _next_workday_start(t)
            continue

        # Weekday: morning shift
        morning_end = t.replace(hour=MORNING_SHIFT[1], minute=0, second=0)
        if t < morning_end:
            available = morning_end - t
            if remaining <= available:
                return t + remaining
            remaining -= available
            # Skip lunch
            t = t.replace(hour=LUNCH_BREAK[1], minute=0, second=0)

        # Evening shift
        evening_end = t.replace(hour=EVENING_SHIFT[1], minute=0, second=0)
        if t < evening_end:
            available = evening_end - t
            if remaining <= available:
                return t + remaining
            remaining -= available

        t = _next_workday_start(t)

    return t


def schedule_compositions(
    n_compositions: int,
    start_date: datetime,
    pipeline_offset_work_h: float = 4.0,
) -> list[ScheduledBlock]:
    """Schedule *n_compositions* through the full pipeline.

    Compositions are staggered by *pipeline_offset_work_h* working hours
    (not wall-clock hours) to model pipelined parallelism. This ensures
    compositions don't collapse onto the same time slot when offsets
    exceed a single day.

    All shared resources (LPBF, atomizer, AutoTrickler, SEM) are tracked
    to prevent double-booking.
    """
    blocks: list[ScheduledBlock] = []
    resources = ResourceTracker(
        lpbf_free=start_date,
        sem_free=start_date,
        atomizer_free=start_date,
        trickler_free=start_date,
    )

    for comp_id in range(1, n_compositions + 1):
        comp_start = _advance_work_hours(
            start_date, pipeline_offset_work_h * (comp_id - 1)
        )
        cursor = comp_start

        for task in PIPELINE_TASKS:
            start, end = _schedule_task(task, cursor, resources)
            blocks.append(ScheduledBlock(comp_id, task, start, end))
            resources.release(task, end)
            cursor = end

    return blocks


# ── Resource utilization computation ──────────────────────────────────────────


def compute_resource_utilization(
    blocks: list[ScheduledBlock],
) -> dict[str, dict[str, float]]:
    """Compute per-resource utilization metrics.

    For each shared resource, computes:
      - total_h: total hours the resource is in use
      - available_h: total available hours in the schedule span, based on
        resource type (building hours for LPBF, shift hours for supervised
        resources like atomizer/trickler/SEM)
      - utilization_pct: total_h / available_h × 100

    The atomizer, AutoTrickler, and SEM are classified as shift-constrained
    because they require operator supervision (reactive Al safety for atomizer,
    manual operation for trickler, semi-manual for SEM).  LPBF printing runs
    fully unattended, so its availability spans all building hours.
    """
    global_min = min(b.start for b in blocks)
    global_max = max(b.end for b in blocks)

    # Compute available hours in the schedule span
    building_h = 0.0  # total building-open hours
    shift_h = 0.0     # total staffed shift hours
    day = global_min.replace(hour=0, minute=0, second=0, microsecond=0)
    while day <= global_max:
        if _is_sunday(day):
            day += timedelta(days=1)
            continue
        if _is_saturday(day):
            building_h += SATURDAY_END - SATURDAY_START  # 6 h
            shift_h += SATURDAY_SHIFT[1] - SATURDAY_SHIFT[0]  # 6 h
        else:
            building_h += WEEKDAY_END - WEEKDAY_START  # 17 h
            # Shift = morning (5 h) + evening (9 h) = 14 h
            shift_h += (MORNING_SHIFT[1] - MORNING_SHIFT[0]) + (
                EVENING_SHIFT[1] - EVENING_SHIFT[0]
            )
        day += timedelta(days=1)

    # Resource definitions: (flag, display_name, is_shift_constrained)
    resources = [
        ("requires_atomizer", "Atomizer", True),
        ("requires_lpbf", "LPBF printer", False),
        ("requires_sem", "SEM facility", True),
        ("requires_trickler", "AutoTrickler", True),
    ]

    result: dict[str, dict[str, float]] = {}
    for flag, name, is_shift in resources:
        res_blocks = [b for b in blocks if getattr(b.task, flag)]
        total_h = sum(
            (b.end - b.start).total_seconds() / 3600 for b in res_blocks
        )
        # Hands-on vs hands-off split (PI review comment 3106203530):
        # supervised/manual operator work vs unattended automated run +
        # passive cool-down.  Helps the reader see that e.g. the LPBF
        # printer's 80 h/wk is dominated by hands-off print time, whereas
        # the atomizer's 64 h/wk is half hands-on melt prep + QC.
        # A task may declare a hands_on_h override when a single scheduled
        # block mixes supervised + unattended phases (e.g. Atomization:
        # 1.5 h supervised prep + 2 h automated run + 0.5 h supervised
        # collect/clean → hands_on_h=2.0 of a 4.0 h block).
        def _block_hands_on(b):
            block_h = (b.end - b.start).total_seconds() / 3600
            if b.task.hands_on_h is not None:
                # Scale the declared hands-on hours by the fraction of the
                # task actually scheduled (defensive: all current tasks run
                # full duration, but this keeps the math robust).
                return b.task.hands_on_h * (block_h / b.task.duration_h)
            if b.task.is_automated or b.task.is_passive:
                return 0.0
            return block_h

        hands_on_h = sum(_block_hands_on(b) for b in res_blocks)
        hands_off_h = total_h - hands_on_h
        avail = shift_h if is_shift else building_h
        pct = total_h / avail * 100 if avail > 0 else 0
        result[name] = {
            "total_h": total_h,
            "hands_on_h": hands_on_h,
            "hands_off_h": hands_off_h,
            "available_h": avail,
            "utilization_pct": pct,
            "is_shift_constrained": is_shift,
        }

    return result



# ── Summary ───────────────────────────────────────────────────────────────────


def print_schedule_summary(
    blocks: list[ScheduledBlock], n_compositions: int
) -> str:
    """Print a text summary of the schedule with throughput analysis."""
    lines = []
    lines.append("=" * 90)
    lines.append("FLAIME Experiment Pipeline — Schedule Summary")
    lines.append("=" * 90)

    global_min = min(b.start for b in blocks)
    global_max = max(b.end for b in blocks)
    span = global_max - global_min

    lines.append(f"Compositions scheduled:  {n_compositions}")
    lines.append(
        f"Schedule span:          "
        f"{global_min:%a %Y-%m-%d %H:%M} → {global_max:%a %Y-%m-%d %H:%M}"
    )
    lines.append(
        f"Total span:             "
        f"{span.total_seconds()/3600:.1f} h "
        f"({span.days} days {span.seconds//3600} hours)"
    )

    # Count working days
    working_days = 0
    d = global_min.replace(hour=0, minute=0, second=0, microsecond=0)
    while d <= global_max:
        if not _is_sunday(d):
            working_days += 1
        d += timedelta(days=1)
    throughput = n_compositions / max(working_days, 1)
    lines.append(f"Working days in span:   {working_days}")
    lines.append(f"Effective throughput:    {throughput:.2f} compositions/day")
    lines.append("")

    for comp_id in range(1, n_compositions + 1):
        comp_blocks = sorted(
            [b for b in blocks if b.composition_id == comp_id],
            key=lambda b: b.start,
        )
        lines.append(f"── Composition {comp_id} ──")
        for b in comp_blocks:
            tags = []
            if b.task.is_automated and not b.task.is_passive:
                tags.append("AUTO")
            elif b.task.is_passive:
                tags.append("PASSIVE")
            else:
                tags.append("MANUAL")
            if b.task.requires_lpbf:
                tags.append("⚙LPBF")
            if b.task.requires_atomizer:
                tags.append("⚗ATOM")
            if b.task.requires_trickler:
                tags.append("⚖TRICK")
            if b.task.requires_sem:
                tags.append("🔬SEM")
            tag_str = " [" + " ".join(tags) + "]"
            lines.append(
                f"  {b.start:%a %H:%M}–{b.end:%H:%M}  "
                f"{b.task.short_name:<10s}{tag_str:<30s}  "
                f"@ {b.task.location}"
            )
        lines.append("")

    # Resource utilization (with proper availability denominators)
    lines.append("─" * 70)
    lines.append("Resource utilization:")
    util_data = compute_resource_utilization(blocks)
    sorted_util = sorted(
        util_data.items(), key=lambda kv: kv[1]["utilization_pct"], reverse=True,
    )
    for name, ud in sorted_util:
        constraint = "shift-hrs" if ud["is_shift_constrained"] else "bldg-hrs"
        marker = " ◀ BOTTLENECK" if name == sorted_util[0][0] else ""
        lines.append(
            f"  {name:<20s} {ud['total_h']:5.1f}h / "
            f"{ud['available_h']:5.0f}h {constraint:<10s} = "
            f"{ud['utilization_pct']:5.1f}%{marker}"
        )

    lines.append("")
    lines.append("Per-task time totals:")
    task_totals: dict[str, float] = {}
    for b in blocks:
        task_totals[b.task.name] = task_totals.get(b.task.name, 0) + (
            (b.end - b.start).total_seconds() / 3600
        )
    for name, total in task_totals.items():
        lines.append(f"  {name:<35s} {total:6.1f} h")

    summary = "\n".join(lines)
    print(summary)
    return summary






# ── Plotting ─────────────────────────────────────────────────────────────────


# Category ordering for the legend — mirrors pipeline flow
CATEGORY_ORDER = [CAT_FEEDSTOCK, CAT_PRINT, CAT_CHARACTERIZE, CAT_TRANSIT]

# Default staffing rotation used by the shift-coverage sidebar.  Three
# overlapping windows that together span the staffed weekday (7–22).
# Each is labeled with an anonymized shift name and staffed by a rotating
# subset of the 2 MS + 10 UG team; ≥3 concurrent on-site is documented in
# STAFFING_MIN_CONCURRENT above.
WEEKDAY_SHIFT_WINDOWS: list[tuple[str, int, int, str]] = [
    # (label, start_hour, end_hour, color)
    ("Early (3 UGs)",  7, 15, "#9ecae1"),   # morning + mid-day overlap
    ("Mid (3 UGs)",   11, 19, "#fdae6b"),   # lunch-spanning coverage
    ("Late (3 UGs)",  14, 22, "#a1d99b"),   # evening overlap
]
SATURDAY_SHIFT_WINDOWS: list[tuple[str, int, int, str]] = [
    ("Sat crew (3 UGs)", SATURDAY_SHIFT[0], SATURDAY_SHIFT[1], "#c994c7"),
]


# ── Shared shading constants (panel-agnostic) ────────────────────────────────
CLOSED_COLOR = "#C0C0C0"
CLOSED_ALPHA = 0.55
SUNDAY_COLOR = "#B0B0B0"
SUNDAY_ALPHA = 0.65
LUNCH_COLOR = "#E8E8E8"
LUNCH_ALPHA = 0.4

# Only label the few "headline" tasks on bar interiors — Atom, Print, SEM,
# Prep.  Setup/Cool/Extract/Ship/Sieve/Dispense/Mech are short and highly
# repetitive across 16 compositions; their identity is carried by the
# category color + legend.
LABELED_SHORT_NAMES = {"Atom", "Print", "SEM", "Prep"}


def _draw_closed_regions(ax, y_min: datetime, y_max: datetime) -> None:
    """Shade building-closed and Sunday hours on a date y-axis."""
    day = y_min.replace(hour=0, minute=0, second=0, microsecond=0)
    while day <= y_max:
        next_day = day + timedelta(days=1)
        if _is_sunday(day):
            ax.axhspan(
                mdates.date2num(day), mdates.date2num(next_day),
                color=SUNDAY_COLOR, alpha=SUNDAY_ALPHA, zorder=0,
                hatch="xx", linewidth=0,
            )
        else:
            ds = _day_start(day)
            de = _auto_end(day)
            if ds > day:
                ax.axhspan(
                    mdates.date2num(day), mdates.date2num(ds),
                    color=CLOSED_COLOR, alpha=CLOSED_ALPHA, zorder=0,
                    hatch="//", linewidth=0,
                )
            ax.axhspan(
                mdates.date2num(de), mdates.date2num(next_day),
                color=CLOSED_COLOR, alpha=CLOSED_ALPHA, zorder=0,
                hatch="//", linewidth=0,
            )
            if not _is_saturday(day):
                lb_s = day.replace(hour=LUNCH_BREAK[0], minute=0)
                lb_e = day.replace(hour=LUNCH_BREAK[1], minute=0)
                ax.axhspan(
                    mdates.date2num(lb_s), mdates.date2num(lb_e),
                    color=LUNCH_COLOR, alpha=LUNCH_ALPHA, zorder=0,
                )
        day = next_day


def _draw_bars(ax, blocks_to_draw, col_width: float,
               col_centers: dict[int, float] | None = None,
               label_min_h: float | None = None,
               fontsize: int = 8) -> None:
    """Draw category-colored bars on *ax*.

    If *label_min_h* is None, no text is drawn inside bars (used for the
    main panel where columns are too narrow to fit any text).  When set,
    only tasks in LABELED_SHORT_NAMES with duration ≥ *label_min_h* get a
    single label inside the bar.
    """
    from matplotlib.patches import Rectangle

    for b in blocks_to_draw:
        comp_id = b.composition_id
        cx = col_centers[comp_id] if col_centers is not None else comp_id
        x = cx - col_width / 2
        y0 = mdates.date2num(b.start)
        y1 = mdates.date2num(b.end)
        if b.task.is_passive:
            fc = b.task.color
            alpha = 0.35
            ls = "--"
        else:
            fc = b.task.color
            alpha = 0.92
            ls = "-"
        rect = Rectangle(
            (x, y0), col_width, y1 - y0,
            facecolor=fc, edgecolor="#303030",
            linewidth=0.5, linestyle=ls, alpha=alpha, zorder=3,
        )
        ax.add_patch(rect)
        if label_min_h is None:
            continue
        bar_hours = (b.end - b.start).total_seconds() / 3600
        if (bar_hours + LABEL_THRESHOLD_TOL_H >= label_min_h
                and b.task.short_name in LABELED_SHORT_NAMES):
            ax.text(
                cx, (y0 + y1) / 2, b.task.short_name,
                ha="center", va="center",
                fontsize=fontsize, fontweight="bold",
                color="#FFFFFF", zorder=5,
            )


def _compute_time_range(
    blocks: list[ScheduledBlock],
) -> tuple[datetime, datetime, datetime]:
    """Return (start_day, end_day, inlay_day) used by all plotting paths."""
    global_min = min(b.start for b in blocks)
    global_max = max(b.end for b in blocks)
    start_day = global_min.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = (global_max + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    day_start_count: dict[datetime, int] = {}
    d = start_day
    while d <= end_day:
        if not _is_sunday(d) and not _is_saturday(d):
            day_end = d + timedelta(days=1)
            count = sum(1 for b in blocks if b.start >= d and b.start < day_end)
            day_start_count[d] = count
        d += timedelta(days=1)
    inlay_day = (
        max(day_start_count, key=lambda d: day_start_count[d])
        if day_start_count else start_day
    )
    return start_day, end_day, inlay_day


# ── Per-panel draw functions (self-contained, take an axes) ──────────────────


def _draw_main_panel(
    ax,
    blocks: list[ScheduledBlock],
    n_compositions: int,
    start_day: datetime,
    end_day: datetime,
    *,
    inlay_day: datetime | None = None,
    show_inlay_marker: bool = False,
    show_y_labels: bool = True,
) -> None:
    """Render the multi-day main Gantt panel into *ax*."""
    _draw_closed_regions(ax, start_day, end_day)
    _draw_bars(ax, blocks, col_width=0.75, label_min_h=None)

    # Sunday text label (only if a Sunday is in range)
    d = start_day
    while d <= end_day:
        if _is_sunday(d):
            ax.text(
                n_compositions / 2 + 0.5,
                mdates.date2num(d + timedelta(hours=12)),
                "SUNDAY  CLOSED",
                ha="center", va="center",
                fontsize=12, fontweight="bold", color="#666666",
                alpha=0.7, zorder=1,
            )
            break
        d += timedelta(days=1)

    ax.set_xlim(0.4, n_compositions + 0.6)
    ax.set_ylim(mdates.date2num(end_day), mdates.date2num(start_day))
    ax.set_xticks(range(1, n_compositions + 1))
    ax.set_xticklabels(
        [f"C{i}" for i in range(1, n_compositions + 1)],
        fontsize=10, fontweight="bold",
    )
    ax.set_xlabel(f"Composition (n = {n_compositions})",
                  fontsize=11, fontweight="bold")

    ax.yaxis_date()
    ax.yaxis.set_major_locator(mdates.DayLocator())
    ax.yaxis.set_minor_locator(mdates.HourLocator(byhour=[7, 12, 22]))
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%A"))
    ax.tick_params(axis="y", which="major", labelsize=10, pad=4,
                   labelleft=show_y_labels)
    ax.tick_params(axis="y", which="minor", length=3)
    ax.grid(axis="y", which="major", color="#DDDDDD",
            linewidth=0.8, zorder=0.5)
    ax.grid(axis="y", which="minor", color="#EEEEEE",
            linewidth=0.4, zorder=0.5)
    ax.set_axisbelow(True)
    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)

    # Inlay marker removed: the zoomed inlay now lives directly below the
    # main panel (Edison R7 #2), is self-labeled with its weekday, and
    # attempting to squeeze an "inlay →" marker into the left margin of the
    # main panel overlapped the C1 bars on the representative day (PI
    # review comment 3106199131).
    _ = (inlay_day, show_inlay_marker)  # kept in signature for back-compat


def _draw_shift_panel(
    ax,
    start_day: datetime,
    end_day: datetime,
    *,
    show_y_labels: bool = True,
    show_xtick_labels: bool = True,
) -> None:
    """Render the shift-coverage sidebar into *ax*.

    When *show_y_labels* is True, the panel carries its own weekday y-tick
    labels so it survives as a standalone PNG (Edison R7 #3).

    When *show_xtick_labels* is False, the Early/Mid/Late x-tick labels are
    suppressed — the in-bar labels already carry that information, and in
    the standalone panel the duplicated labels crowded the bottom-most bar
    (Edison R8 #3).
    """
    from matplotlib.patches import Rectangle

    n_shifts = len(WEEKDAY_SHIFT_WINDOWS)
    ax.set_xlim(0, n_shifts)
    ax.set_ylim(mdates.date2num(end_day), mdates.date2num(start_day))
    d = start_day
    while d <= end_day:
        if _is_sunday(d):
            d += timedelta(days=1)
            continue
        windows = (SATURDAY_SHIFT_WINDOWS if _is_saturday(d)
                   else WEEKDAY_SHIFT_WINDOWS)
        for idx, (label, s_h, e_h, color) in enumerate(windows):
            y0 = mdates.date2num(d.replace(hour=s_h, minute=0))
            y1 = mdates.date2num(d.replace(hour=e_h, minute=0))
            if _is_saturday(d) and len(windows) == 1:
                x0, w = 0, n_shifts
            else:
                x0, w = idx, 1
            ax.add_patch(Rectangle(
                (x0, y0), w, y1 - y0,
                facecolor=color, edgecolor="#505050",
                linewidth=0.4, alpha=0.7, zorder=2,
            ))
            # Label the bar so the Saturday crew band (the lone pink bar
            # spanning all three columns) is self-explanatory rather than
            # reading as a separate kind of shift (PI review comment
            # 3106201644).
            short = label.split(" (")[0]
            ax.text(
                x0 + w / 2, (y0 + y1) / 2, f"{short}\n{s_h}–{e_h}",
                ha="center", va="center", fontsize=6.5,
                color="#303030", zorder=3,
            )
        d += timedelta(days=1)
    for xv in range(1, n_shifts):
        ax.axvline(xv, color="#AAAAAA", linewidth=0.3, zorder=1)
    ax.set_xticks([0.5, 1.5, 2.5])
    if show_xtick_labels:
        ax.set_xticklabels(["Early", "Mid", "Late"],
                           fontsize=8, rotation=0)
    else:
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
    if show_y_labels:
        ax.yaxis_date()
        ax.yaxis.set_major_locator(mdates.DayLocator())
        ax.yaxis.set_major_formatter(mdates.DateFormatter("%A"))
        ax.tick_params(axis="y", which="major", labelsize=9, pad=4)
    else:
        ax.tick_params(axis="y", labelleft=False, length=0)
    ax.set_xlabel("Shift coverage\n(≥3 UGs)",
                  fontsize=9, fontweight="bold")
    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)


def _draw_inlay_panel(
    ax,
    blocks: list[ScheduledBlock],
    inlay_day: datetime,
    *,
    pad_h: float = 0.5,
) -> None:
    """Render the single-day zoomed inlay into *ax*.

    *pad_h* (Edison R7 #5) reduced from 1.5 → 0.5: enough that bars don't
    abut the building-closed hatch, but no longer wastes ~1/3 of vertical
    space on hatching alone.
    """
    inlay_start = inlay_day.replace(hour=0)
    inlay_end = inlay_day + timedelta(days=1)
    inlay_blocks = [
        b for b in blocks if b.start < inlay_end and b.end > inlay_start
    ]
    active_ids = sorted({b.composition_id for b in inlay_blocks})
    inlay_centers = {cid: i + 1 for i, cid in enumerate(active_ids)}
    n_inlay = max(len(active_ids), 1)
    if _is_saturday(inlay_day):
        view_ymin = inlay_day.replace(hour=SATURDAY_START) - timedelta(hours=pad_h)
        view_ymax = inlay_day.replace(hour=SATURDAY_END) + timedelta(hours=pad_h)
    else:
        view_ymin = inlay_day.replace(hour=WEEKDAY_START) - timedelta(hours=pad_h)
        view_ymax = inlay_day.replace(hour=WEEKDAY_END) + timedelta(hours=pad_h)
    _draw_closed_regions(ax, view_ymin, view_ymax)
    _draw_bars(ax, inlay_blocks, col_width=0.72,
               col_centers=inlay_centers,
               label_min_h=1.5, fontsize=8)
    ax.set_xlim(0.4, n_inlay + 0.6)
    ax.set_ylim(mdates.date2num(view_ymax), mdates.date2num(view_ymin))
    ax.set_xticks(range(1, n_inlay + 1))
    ax.set_xticklabels(
        [f"C{cid}" for cid in active_ids],
        fontsize=9, fontweight="bold",
    )
    ax.yaxis_date()
    ax.yaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.yaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.tick_params(axis="y", which="major", labelsize=8)
    ax.grid(axis="y", which="major", color="#DDDDDD",
            linewidth=0.6, zorder=0.5)
    ax.grid(axis="y", which="minor", color="#EEEEEE",
            linewidth=0.3, zorder=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor(OI_ORANGE)
        spine.set_linewidth(1.8)
    ax.set_xlabel(
        f"Composition  ·  zoomed inlay: {inlay_day.strftime('%A')}",
        fontsize=10, fontweight="bold", color=OI_ORANGE,
    )


def _draw_util_panel(
    ax,
    blocks: list[ScheduledBlock],
) -> None:
    """Render the equipment-hours bar chart into *ax*.

    Each resource bar is split into hands-on (supervised/manual) and
    hands-off (automated or passive) segments — PI review comment
    3106203530 requested this breakdown so the reader can see that e.g.
    the LPBF printer's 80 h/wk is dominated by unattended print time,
    while the atomizer's 64 h/wk is half operator work.
    """
    util_data = compute_resource_utilization(blocks)
    sorted_util = sorted(
        util_data.items(), key=lambda kv: kv[1]["total_h"], reverse=True,
    )
    names = [n for n, _ in sorted_util]
    hours = [ud["total_h"] for _, ud in sorted_util]
    hands_on = [ud["hands_on_h"] for _, ud in sorted_util]
    hands_off = [ud["hands_off_h"] for _, ud in sorted_util]

    y_pos = list(range(len(names)))
    # Hands-on segment: solid, darker (operator work)
    ax.barh(
        y_pos, hands_on, height=0.62,
        color="#0072B2", edgecolor="#303030", linewidth=0.5, alpha=0.9,
        zorder=3, label="Hands-on (supervised)",
    )
    # Hands-off segment: hatched, lighter (unattended / passive)
    ax.barh(
        y_pos, hands_off, left=hands_on, height=0.62,
        color="#E69F00", edgecolor="#303030", linewidth=0.5, alpha=0.55,
        hatch="///", zorder=3, label="Hands-off (unattended / passive)",
    )
    ax.axvline(40, color="#303030", linewidth=1.0,
               linestyle="--", zorder=2)
    ax.text(40, -0.85, "40 h = 1 FTE",
            ha="center", va="top", fontsize=8,
            fontweight="bold", color="#303030")
    ax.axvline(168, color="#888888", linewidth=0.8,
               linestyle=":", zorder=2)
    ax.text(168, -0.85, "168 h = wall-clock week",
            ha="center", va="top", fontsize=8, color="#666666")

    for i, (_name, ud) in enumerate(sorted_util):
        h = ud["total_h"]
        on_h = ud["hands_on_h"]
        off_h = ud["hands_off_h"]
        fte_pct = h / 40 * 100
        ax.text(
            h + 2, i,
            f"{h:.0f} h/wk   ·   {on_h:.0f} h hands-on + "
            f"{off_h:.0f} h hands-off   ·   {fte_pct:.0f}% of 40-h FTE",
            ha="left", va="center", fontsize=8.5, color="#222",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9.5, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, max(max(hours) * 1.45, 180))
    ax.set_xlabel(
        "Equipment hours per representative week "
        "(blue = hands-on operator time; hatched orange = hands-off "
        "automated/passive time)",
        fontsize=9.5,
    )
    ax.grid(axis="x", color="#EEEEEE", linewidth=0.4, zorder=0.5)
    ax.set_axisbelow(True)
    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)


def _draw_legend_panel(ax) -> None:
    """Render the category legend into *ax* (axis off)."""
    ax.axis("off")
    handles = []
    labels = []
    for cat in CATEGORY_ORDER:
        handles.append(mpatches.Patch(
            facecolor=CATEGORY_COLORS[cat], edgecolor="#303030",
            alpha=0.92, linewidth=0.5,
        ))
        labels.append(cat)
    handles.append(mpatches.Patch(
        facecolor=CLOSED_COLOR, alpha=CLOSED_ALPHA,
        hatch="//", edgecolor="#606060",
    ))
    labels.append(
        f"Building closed (outside {WEEKDAY_START}–{WEEKDAY_END} wkdy / "
        f"{SATURDAY_SHIFT[0]}–{SATURDAY_SHIFT[1]} Sat)"
    )
    handles.append(mpatches.Patch(
        facecolor=SUNDAY_COLOR, alpha=SUNDAY_ALPHA,
        hatch="xx", edgecolor="#606060",
    ))
    labels.append("Sunday (off)")
    handles.append(mpatches.Patch(
        facecolor="#FFFFFF", alpha=0.35, edgecolor="#303030",
        linewidth=0.6, linestyle="--", hatch="",
    ))
    labels.append("Passive cooling (no staff/equipment)")

    ax.legend(
        handles, labels, loc="center", ncol=4,
        fontsize=9, frameon=False,
        handlelength=1.6, handleheight=1.1, columnspacing=1.2,
    )


# ── Standalone per-panel renderers (each owns its plt.figure) ────────────────
# Per Edison R7 #1: dedicated figures replace the old `bbox_inches` crop
# loop, eliminating cross-panel bleeding (clipped weekday labels in
# shift_coverage.png, midnight-bar slivers in compositions_inlay.png).


def plot_shift_standalone(
    blocks: list[ScheduledBlock], save_path: Path,
) -> None:
    start_day, end_day, _ = _compute_time_range(blocks)
    fig, ax = plt.subplots(figsize=(3.5, 9.0), dpi=150)
    _draw_shift_panel(
        ax, start_day, end_day,
        show_y_labels=True, show_xtick_labels=False,
    )
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_main_standalone(
    blocks: list[ScheduledBlock], n_compositions: int, save_path: Path,
) -> None:
    start_day, end_day, _ = _compute_time_range(blocks)
    fig, ax = plt.subplots(figsize=(9.0, 9.0), dpi=150)
    # Standalone main panel: no inlay marker (no inlay to point at), and
    # carry its own y-axis labels.
    _draw_main_panel(
        ax, blocks, n_compositions, start_day, end_day,
        inlay_day=None, show_inlay_marker=False, show_y_labels=True,
    )
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_inlay_standalone(
    blocks: list[ScheduledBlock], inlay_day: datetime, save_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(5.0, 8.0), dpi=150)
    _draw_inlay_panel(ax, blocks, inlay_day, pad_h=0.5)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_equipment_standalone(
    blocks: list[ScheduledBlock], save_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 3.0), dpi=150)
    _draw_util_panel(ax, blocks)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_legend_standalone(save_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 1.0), dpi=150)
    _draw_legend_panel(ax)
    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_gantt_vertical(
    blocks: list[ScheduledBlock],
    n_compositions: int,
    save_path: Path | None = None,
) -> None:
    """Render the FLAIME pipeline Gantt (vertical layout, proposal-ready).

    Layout, top → bottom (revised per Edison R7 #2 — inlay no longer
    side-by-side with the main panel, eliminating dual y-axis confusion):
      * Row 0 — [shift panel] [main gantt]   — weekday-only y-axis
      * Row 1 — [zoomed inlay (centered, narrower width)]
      * Row 2 — utilization bar chart
      * Row 3 — category legend (4 entries)

    Per PI review (comment 4265035541):
      * No in-figure title — caption lives in a separate .md file.
      * No text footer — utilization is visualized as a bar chart showing
        both raw hours and % of a 40-hr FTE workweek.
      * Bars colored by experimental *category*.
      * Weekday labels only on the y-axis (no calendar dates).
      * Shift-coverage sidebar makes the ≥3-person staffing visible.
    """
    import matplotlib.gridspec as gridspec

    start_day, end_day, inlay_day = _compute_time_range(blocks)

    # ── figure layout: 4 rows × 3 cols.  Inlay is centered below main
    # to avoid the dual-time-scale confusion Edison R7 flagged.
    fig = plt.figure(figsize=(11, 17), dpi=150)
    gs = gridspec.GridSpec(
        4, 3,
        height_ratios=[1.0, 0.55, 0.22, 0.07],
        width_ratios=[0.22, 1.0, 0.22],
        left=0.06, right=0.98, top=0.98, bottom=0.03,
        hspace=0.32, wspace=0.10,
    )
    ax_shift = fig.add_subplot(gs[0, 0])
    ax_main = fig.add_subplot(gs[0, 1:])
    ax_inlay = fig.add_subplot(gs[1, 1])
    ax_util = fig.add_subplot(gs[2, :])
    ax_legend = fig.add_subplot(gs[3, :])

    _draw_main_panel(
        ax_main, blocks, n_compositions, start_day, end_day,
        inlay_day=inlay_day, show_inlay_marker=True, show_y_labels=True,
    )
    # In the combined figure the shift panel is adjacent to the main panel,
    # so suppress its weekday labels (they already appear on ax_main).
    _draw_shift_panel(ax_shift, start_day, end_day, show_y_labels=False)
    _draw_inlay_panel(ax_inlay, blocks, inlay_day, pad_h=0.5)
    _draw_util_panel(ax_util, blocks)
    _draw_legend_panel(ax_legend)

    # Panel identifiers (a)/(b)/(c)/(d) — PI review comment 3106199672.
    for ax, tag in [
        (ax_shift, "(a)"),
        (ax_main, "(b)"),
        (ax_inlay, "(c)"),
        (ax_util, "(d)"),
    ]:
        ax.text(
            -0.02, 1.02, tag, transform=ax.transAxes,
            ha="right", va="bottom",
            fontsize=13, fontweight="bold", color="#222",
        )

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"Gantt chart saved to {save_path}")

        # Subfigures: each rendered independently in its own plt.figure
        # (Edison R7 #1) — no more bleeding from sibling axes.
        subfig_dir = save_path.parent / "subfigures"
        subfig_dir.mkdir(exist_ok=True)
        plot_shift_standalone(blocks, subfig_dir / "shift_coverage.png")
        plot_main_standalone(
            blocks, n_compositions, subfig_dir / "compositions_main.png",
        )
        plot_inlay_standalone(
            blocks, inlay_day, subfig_dir / "compositions_inlay.png",
        )
        plot_equipment_standalone(
            blocks, subfig_dir / "equipment_hours.png",
        )
        plot_legend_standalone(subfig_dir / "legend.png")
        print(f"Sub-panels saved to {subfig_dir}/")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    """Generate the Gantt chart and schedule summary."""
    # Schedule 16 compositions across one representative work-week
    # (3/day weekdays × 5 + 1/day Saturday = 16 compositions/week).  The
    # start_date is only used internally — the rendered figure uses weekday
    # labels only so the schedule reads as a representative week.
    n_compositions = 16
    start_date = datetime(2026, 9, 7, 7, 0)  # arbitrary Monday 7 AM anchor

    print("Scheduling pipeline...")
    blocks = schedule_compositions(
        n_compositions=n_compositions,
        start_date=start_date,
        # 14 work-hours/weekday ÷ 3 comps/day ≈ 4.67 h offset; this keeps
        # atomizer (4 h) non-overlapping and fills the 15 h staffed window.
        pipeline_offset_work_h=4.67,
    )

    output_dir = Path(__file__).parent
    gantt_path = output_dir / "gantt_experiment_schedule.png"

    print("Generating Gantt chart (vertical orientation + inlay)...")
    plot_gantt_vertical(blocks, n_compositions, save_path=gantt_path)

    summary = print_schedule_summary(blocks, n_compositions)

    # Save summary
    summary_path = output_dir / "schedule_summary.txt"
    summary_path.write_text(summary)
    print(f"\nSchedule summary saved to {summary_path}")

    # Save JSON for downstream use
    schedule_json = []
    for b in blocks:
        schedule_json.append({
            "composition_id": b.composition_id,
            "task": b.task.name,
            "short_name": b.task.short_name,
            "start": b.start.isoformat(),
            "end": b.end.isoformat(),
            "duration_h": b.task.duration_h,
            "is_automated": b.task.is_automated,
            "is_passive": b.task.is_passive,
            "location": b.task.location,
            "requires_lpbf": b.task.requires_lpbf,
            "requires_atomizer": b.task.requires_atomizer,
            "requires_trickler": b.task.requires_trickler,
            "requires_sem": b.task.requires_sem,
        })
    json_path = output_dir / "schedule_data.json"
    json_path.write_text(json.dumps(schedule_json, indent=2))
    print(f"Schedule JSON saved to {json_path}")


if __name__ == "__main__":
    main()
