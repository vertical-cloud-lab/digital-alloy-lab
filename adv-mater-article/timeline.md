# Timeline back from an early-2028 deadline

*Draft of 2026-11-27. Assumes the collection closes in late February 2028 (decision D1: please confirm the
exact date) and that the campaign paper (#277) is submitted on Feb 25, 2027 and owns campaign 1's alloys.
Dates are proposals; nothing has been booked or ordered.*

## Gates

| Gate | Date | Pass | If it fails |
|---|---|---|---|
| G-A0 | Fri Dec 18, 2026 | Decisions made: collection and due date (D1), the split with the campaign paper (D2), desktop LPBF build or buy and who orders it (D7); bench logging of step times (L1–L2) started | Each week of delay on D7 moves P1 by a week |
| G-A1 | Wed Mar 31, 2027 | ≥ 5 valid Block A runs checked against the bar (A1–A2); campaign 1 step costs compiled (L1–L2); mineral burden computed (B4); twin refit to campaign 1 records (T1, first pass) | Block A is the one thing version B can't do without: if it isn't done, run it in April before anything else |
| G-A2 | Mon May 31, 2027 | Desktop LPBF prints dense Al cubes (P1); Block B and its ICP back (C2); the acquisition decided (M7) and campaign 2's optimizer, baselines, targets and stopping rule pre-registered and committed (B1), with the twin's out-of-sample prediction of campaign 2; the industry baselines (B6) measured in-house at least once (by the campaign paper, late Jan to mid-Feb 2027 if the PO goes out by Dec 4–11), and their parity with the data sheets (B8) known | If P1 is late, campaign 2 starts with the Utah MIDI and the desktop joins when ready; Fig. 1c and Fig. 4 shrink |
| — | Jul 6 – Oct 15, 2027 | **Campaign 2**: ~14 weeks including flex; ~25–35 atomizer runs; hardness and density on every print; tensile on finalists | |
| G-A3 | Thu Sep 30, 2027 | The decision log shows acquisition stops at different steps, with the audit running (Fig. 5a–b); at least one candidate on track to expand the in-house front of the industry baselines; version A or B chosen | Version B: write it from Blocks A/B, campaign 1 data and the twin, for another journal |
| G-A4 | Mon Nov 15, 2027 | Data freeze; finalists' samples at the outside lab (V1–V2) | Report outside results as pending, or drop V2 |
| G-A5 | Mon Dec 20, 2027 | Outside results back; twin validated against campaign 2 (T4) and counterfactuals run (T2–T3); full draft to co-authors | |
| — | Jan 2028 | Co-author edits; internal read by someone outside the lab; precedent scan re-run (A6); figures final; SI and data deposit ready (DOIs reserved, not published) | |
| **Submit** | **Tue Feb 15, 2028** | Version A to the collection if G-A3 passed; otherwise version B to another journal (it can go as early as Jul 2027) | ~2 weeks of buffer before a late-February deadline |

## What campaign 1 (Nov 2026–Feb 2027) has to log for this article

Campaign 1's alloys belong to the campaign paper, but this article needs three things from those weeks, and
they cost almost nothing if they are logged at the bench rather than reconstructed later:

1. **A filled run record for every atomizer run** (byu-vcl `run-record-template.yaml`), failed runs included,
   with the six-part mass balance and a sealed 5 g sample.
2. **Timestamps and consumables for every step** (L1–L2): start and end of each step, who, which machine, what
   was used. #256 already asks for this ("Fig. 1 of the paper is the cost of each step").
3. **Block A before the composition runs.** It is the article's most important single dataset (Fig. 2) and,
   per #256, the first thing on the schedule. Since Nov 13 it waits on the collection cup (#269).

## Why February 2028 is realistic, and what would move it

- **Version B by Jul 2027: likely** if Block A runs by the end of March 2027. Everything else for version B (Blocks
  A/B, step costs, campaign 1 data, the refit twin) is in the lab's control. It has no new alloy, so it fits
  another journal better than *Advanced Materials* (outline §5).
- **Version A by Feb 2028: possible, not yet likely.** It needs three things that don't exist today: a
  desktop LPBF printing Al by about May 2027 (not yet ordered; FT-1 needs 4–9 weeks after the order plus
  safety approvals), an optimizer that makes non-trivial step choices on real data (decision M7: pKGFN's
  knowledge gradient is flat on most decisions in bofn-clocked and trails when the screen is right; BOFN with powder
  reuse is robust but only chooses between new powder and a reprint), and an atomizer that delivers valid runs at 2–3 a
  week (2 of 10 runs so far were good). It also needs the industry baselines bought and printed here in time
  for campaign 2's first build; their sourcing and lead times are in the campaign paper's run (#277).
- **If the collection is actually due Feb 2027**, this plan merges into the campaign paper (see README, D1).
