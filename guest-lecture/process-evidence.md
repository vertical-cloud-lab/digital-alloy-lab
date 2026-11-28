# Process Evidence for Slides 22–32

Reference brief for the UChicago MENG guest lecture on Sterling Baird's research
process. One section per theme (a)–(i). Each entry has a short framing the
lecturer can paraphrase, plus 1–3 concrete repo references with quotes or
paraphrases. No speculation: when a theme has no direct repo evidence it says
so.

Repo: `vertical-cloud-lab/digital-alloy-lab-private` (private). All PR/file
references below are in this repo unless noted.

---

## (a) GitHub + Copilot + Edison are useful alone; composition unlocks more

**Framing:** Each tool — GitHub for versioning + review, Copilot for code/edit
agency, Edison for literature-grounded critique — is useful by itself. The big
wins came from composing them: Copilot reading the *full repo* as context, and
Copilot calling Edison as a literature-steeped adversary in the loop.

- **PR #14** ("BOFN + LLM-BO synthesis ... pKGFN ...",
  https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/14) —
  the original prompt was just *"Explore this integration of LLMs and function
  networks for BO ... Determine what kind of benchmark task would be needed to
  build confidence in it before deploying it."* Copilot returned three
  deliverables (working BoTorch BOFN demo, Edison-found LILO/LLAMBO/BORA
  literature review, and a 5-point LLM-BOFN synthesis with a 4-phase roadmap)
  in a single PR. The Edison literature step was invoked from inside the
  Copilot agent — composition, not separate tools.
- **PR #14, comment 4018517435** — after Copilot answered "yes, fully Bayesian
  is compatible," PI replied *"verify this functionality with a real test using
  `SaasFullyBayesianSingleTaskGP`"* and Copilot landed
  `benchmarks/bofn_fully_bayesian_test.py` in commit `69d9578` with NUTS-fit
  output matching ground truth. GitHub thread → Copilot edit → committed test
  → next review, all in one place.
- **`edison-section-drafts/run_all_parallel.py`** — utility that fans 13
  Edison ANALYSIS section-draft jobs out in parallel ("~10–15 min wall time")
  via `edison-client>=0.11.0`. Concrete artifact of "use Edison as a
  programmable collaborator, not a chat window."

---

## (b) Plan-before-implement; explicit prompts beat clever ones

**Framing:** Two patterns the lecturer relied on heavily: (1) ask the agent
for the *plan* first and confirm it before any code/text is written, and
(2) make the prompt boringly explicit — point at a URL or a line range and
state exactly what to do.

- **PR #52, comment 2026-04-13T15:54Z** — *"@copilot+claude-opus-4.6 create a
  plan for populating the LaTeX proposal template. Just make the plan so I can
  confirm first."* The plan landed as
  `genesis-mission-proposal/proposal-population-plan.md`, was iterated on for
  16 more Edison-feedback rounds (see
  `edison-trajectories/edison-proposal-plan-review-round{1..16}.md`), and only
  *then* was the LaTeX populated.
- **PR #52, comment 2026-04-13T15:53Z (explicit-prompt-with-link pattern):**
  *"@copilot+claude-opus-4.6 apply changes based on the comments in
  [this thread](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/52#pullrequestreview-4099746119)"*
  → Copilot replied with commit `dd8a848` listing all 8 review comments
  resolved one-by-one (RNG seeding, docstring drift, Unicode glyphs, etc.). The
  prompt isn't clever; it's a literal pointer to a specific review block.
- **PR #14, comment 2026-04-09T03:07Z** — *"update implementation based on
  recent developments in #26 and #30 and #20 ... Run a single high effort
  Edison scientific search asking for feedback on your proposed approach,
  incorporate that feedback, perform a second follow up Edison scientific
  query, and then incorporate that feedback. Keep track of the IDs in case you
  hit a wall time limit ..."* — explicit numbered steps, named PR cross-refs,
  and a recovery instruction. Same shape as the line-range pattern, scaled to a
  multi-step procedure.

**One PR #52 review-thread example end-to-end** (theme: "explicit prompt with
link + line range, applied all at once"):

- *Thread on `genesis-mission-proposal/flaime-genesis-proposal.tex` ~line 502*,
  PI wrote: *"Double to make sure this is the correct citation"* on the
  `tobias_2025_autonomy` bib entry.  Copilot verified the claim against the
  cited paper, then in commit `7037de0` corrected the author names from
  "Tobias, Elia and Wahab, Hamid" to "Alexander V. Tobias and Adam Wahab,"
  added the journal (*Royal Society Open Science*, 12(7), 250646, 2025), and
  the DOI `10.1098/rsos.250646`. One terse review comment → one specific
  commit fixing exactly the lines/fields named.

---

## (c) Consolidating across many threads under tight word budgets is still human

**Framing:** Agents are great at proposing fixes inside one thread. Compressing
*dozens* of threads into a 5-page narrative without losing the load-bearing
ideas is still a human job — important things get lost otherwise.

- **PR #52** — 100 review threads (75 marked outdated by merge time), 39
  top-level comments, 383 commits, 137,902 additions across 373 files, all
  driving toward a **5-page** Field 8 narrative
  (`genesis-mission-proposal/flaime-genesis-proposal.tex`).
- **`edison-trajectories/edison-narrative-trim-plan-review.md`** exists as a
  dedicated trim-plan review — i.e. the consolidation step needed its own
  artifact and Edison pass.
- **PR #52, 2026-04-14T05:05Z** — PI directive: *"see thoughts below as I read
  through the `proposal-population-plan.md`. Send this to Edison analysis along
  with all files in this branch for feedback ... Carry out this iterative
  process on the plan with Edison sixteen more times."* Even with 16 automated
  rounds, the PI's hand-written reading and triage are what set the direction.

---

## (d) Oversight scales as you approach "final"; vision models, agent self-iteration; sometimes drop the LLM

**Framing:** Early on the agent can sprint with light review. The closer to
"final," the more oversight per change — and at the very end it's often
faster to leave the LLM and finish in PowerPoint / Inkscape / matplotlib by
hand.

- **Build-toggle workflow** in `genesis-mission-proposal/Makefile`:
  `make draft` (watermark + todonotes), `make clean-pdf`, `make final`
  (also strips abstract/biosketch/budget). Three different oversight regimes
  baked into the build itself; no manual edits to `\drafttrue`/`\submissiontrue`.
- **Vision-model figure iteration:** `edison-trajectories/edison-figure-analysis-round{1..8}.md`
  — eight rounds of figure critique. Then the recent commit train (`5276f7f`,
  `47b42da`, `5b63ea7`, `46547e8`, `28f4d18`, ..., `736c3be`) is *all*
  hand-tuning the FLAIME pipeline DAG (`figures/flaime_pipeline_dag.py`):
  glyph spacing, S-curve diagonals, color-coded edges, portrait layout.
  Once the LLM had taken it 80 % of the way, the last 20 % was direct
  matplotlib edits.
- **Non-LLM figure assets** in the repo: `figures/sem/` (12 SEM/EDS PNGs from
  the EDAX TEAM instrument), `figures/al-wire/` (raw camera photos),
  `figures/dag-thumbnails/` (vector partner logos as `.svg`), and the panel
  scripts `figures/panels/panel_a_parameter_grid.py` etc. — concrete examples
  of "drop the LLM and finish in Inkscape/PPT/matplotlib."

---

## (e) Workflow has been very useful for choosing which sims/experiments to run

**Framing:** A big part of the value isn't writing prose — it's deciding which
preliminary results to generate. The agent + Edison loop produced a triaged
shortlist of sims and experiments worth running before submission.

- **`edison-trajectories/edison-preliminary-results-asset-readiness.md`** and
  **`edison-preliminary-results-mock-review.md`** — explicit triage of which
  preliminary-results assets exist, which are missing, and which should be
  prioritized.
- **Preliminary-results commit train** (`e38f858` "Add preliminary results and
  printability maps for AlSi10Mg and BYU blend", `484870f` "Update proposal
  PDF with revised printability maps and calibration data"). The maps live in
  `figures/thermo-calc-am-module-prelim-results/` — two melt-pool PNGs +
  two printability maps targeted exactly at the compositions the proposal
  needed to defend. Decision driven by the agent loop, simulation run by hand.
- **PR #14 → BOFN benchmark** (`benchmarks/`, `figures/lpbf_parameter_space.py`,
  `figures/composite_4panel.png`) — the benchmark itself was scoped from a
  prompt asking *what* benchmark would build confidence before deploying
  LLM-BOFN. The framework chose the experiment; the experiment then produced a
  proposal figure.
- **PR #66** (BYU ORC SLURM port of the BOFN benchmark) — direct downstream:
  once BOFN-on-BoTorch worked locally, the agent ported the sweep to HPC
  (`hpc/bofn_benchmark/submit.sh`, `CELL_TIME=24:00:00`, 120-cell array
  `11603325` + 20-cell pKGFN array `11603446`) so the proposal could cite a
  real convergence trace. Trace then pulled into the proposal in commit
  `201d52b` ("Swap in latest BOFN optimization trace from PR #14").

---

## (f) Student anecdote — "three months of work in a week"

**No direct repo evidence.** Lecturer to tell the story from experience: the
student felt they had compressed three months of work into a week because
both the *plan* and the *final-form target* were crystal clear from the
start. (PR #52 is the closest indirect analogue — plan-first + clear target
artifact = the LaTeX template — but that's the PI's own workflow, not the
student's.)

---

## (g) Fine-tuning / perfectionism comes at the end

**Framing:** The first 80 % is "land the structure." The last 20 % is where
you let perfectionism off the leash — typography, transitions, citations,
single-word swaps.

- **Commit train on the DAG figure** (April 2026): `dag: equal-pitch rows,
  tighter no-glyph gaps, curve diagonals` (`ab39392`); `dag: stronger S-curve
  so inp_c -> tc2 enters vertically` (`657e64e`); `dag: stagger MVS->char
  glyph y-position to avoid overlap` (`91d3d94`); `Side-by-side BOFN glyphs
  in TC->atom and MVS->char rows` (`5276f7f`). Pure visual fine-tuning, all
  *after* the science was settled.
- **Late-stage PR #52 prose tweaks**: many resolved threads are one-line
  `suggestion`/grammar fixes — e.g. thread on
  `flaime-genesis-proposal.tex`: ```` ```suggestion validating \flaime{}'s
  modality focus over alternative metal 3D printing methods. ``` ```` →
  *"Applied in `0846086`."* And `8b375f5` "App. 7: reframe printing-partner
  letter around cross-printer validation; fix heading to FOA wording" — pure
  framing polish on a supporting letter.
- **Late-stage Edison checklist sweeps**:
  `edison-trajectories/edison-checklist-review-round{6,7,8}.md` — three
  consecutive rounds of "is anything still wrong?" near the end, not at the
  start.

---

## (h) Agent transcripts = low-effort self-documentation

**Framing:** You don't have to write a process journal — the transcript
already is one. Save the session and you've documented the work for free.

- **`copilot-session-68eb6141-82dd-49f2-b744-e4bf2774ea4b.md`** in the repo
  root: 50 088 lines, ~17 h 53 m duration, exported directly from Copilot CLI.
  Header: *"Session ID 68eb6141..., Started 4/16/2026 3:03 AM, Duration
  1073m 49s, Exported 4/16/2026 8:57 PM."* It captures the literal prompts,
  tool calls (`view`, `view_range`), and outputs that produced the
  proposal-consistency-checker skill — no extra writing required.
- **PR #52 + #14 comment threads** are the same artifact in a different
  shape: each `@copilot ...` → Copilot reply → linked commit forms a
  human-readable audit log. PR #14 alone has 110 review threads + comments
  documenting the BOFN/pKGFN exploration end-to-end.
- **`.github/agents/{proposal-consistency-checker,mock-reviewer,draft-feedback,proposal-editor}.agent.md`**
  + `.github/skills/*/SKILL.md` — the agents themselves are checked-in
  prose specs of "how we work on this proposal." Future you (or a
  collaborator) can read them like onboarding docs.

---

## (i) Don't lose human connection — agents surface contacts; emails are still yours

**Framing:** Agents are excellent at building shortlists of named people with
verified emails. But the actual personalized outreach — and the relationship
— is still yours to do.

- **Commit `5a13555`**: "Add validation-print shortlist: verified LPBF/DED/BJ
  printer-owners + OEM/reseller downselection." Followed by `2d208a8` "v11:
  one-by-one email verification pass" and `d5b7eca` "v12: verify 10 more
  named individuals (Constellium Chehab, Airbus Palm, AFRL Gupta, NRC Li,
  Cornell Moridi, NIST DeCost+Lane, KU Leuven Kruth+Van Hooreweder, ASU Bhate,
  TAMU Elwany, RMIT Brandt, PoliMi Vedani, Northwestern Dunand)" — agent did
  the surfacing and the verification.
- **Commit `44a4abb`**: "v14: surface named contacts + emails inline in
  P2-B/P2-C/P3 shortlist tables; +47 CSV rows for aerospace/service-bureau/OEM
  general inboxes." Same loop, more breadth.
- **Hand-written letters** (commits `cda9b3a`, `30febeb`, `e679371`,
  `8fbcf2d`, `82799c3`, `1cb1dcc`, `8b375f5`): Jensen $50K cost-share letter,
  Alik Nielsen UofU Metal 3D Printing core op letter, the Printing Partner
  letter reframing — every one of these is a personal, edited-by-hand artifact
  built on top of the agent-surfaced shortlist. Agents found the contacts;
  the PI wrote the letters.
