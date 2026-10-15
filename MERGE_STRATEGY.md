# PR Merge Strategy — Path Forward for Converging Content

*Generated 2026-04-09, updated 2026-04-11 for issue #35*

This document analyzes all 20 open PRs (plus 1 merged, 2 closed) in `digital-alloy-private`, identifies conflicts, dependencies, and content categories, and recommends a concrete merge order with step-by-step instructions.

> **Note — Topic 3B pivot (April 10, 2026):** The Genesis Mission proposal (DE-FOA-0003612) now targets **Topic 3B: Securing America's Critical Minerals Supply — Focus Area B: AI-Enabled Materials Discovery and Engineering (AMMTO)**. Material strategy: Al-Zr and Al-Mn-Cr-Zr families are PRIMARY (~80% Phase I effort) for discovering critical-mineral-lean alloys that eliminate Mg/Sc/REE dependency; Cu-Cr-Zr is a COMPLEMENT (~20% stretch) for Be-Cu replacement. AlSi10Mg is retained as a baseline for benchmarking only.

### Partnership Structure

| Type | Partner | Role |
|---|---|---|
| **Letter of Collaboration** | **Valimet** (Stockton, CA) | Gas atomization service contract, Phase I powder supply |
| **Letter of Collaboration** | **AMAZEMET** (Warsaw, Poland) | Ultrasonic atomizer vendor (rePOWDER system), powder atomization returns |
| **Letter of Collaboration** | **Thermo-Calc** (Solna, Sweden / Pittsburgh, PA) | CALPHAD/AM Module simulations, TC-Python/TCAl10 advisory |
| Letter of Support | Ames National Laboratory | CMI Hub legacy, Phase II GARS pathway (Ames Lab contacts) |
| Letter of Support | Fehrmann Alloys (Hamburg, Germany) | Specialty AM feedstock validation |
| Letter of Support | Taylor Sparks (University of Utah) | LPBF printing access, AM expertise |
| Letter of Support | Ashley Speer | Materials characterization support |
| Letter of Support | Adam Clare | AM process engineering and parameter expertise |
| Letter of Support | Chris Stiles | AM process engineering |
| Letter of Support | Jae Hattrick-Simpers | Autonomous experimentation, SDL methodology validation |
| Letter of Support | Keith Brown (Boston University) | SDL pioneer, independent validation of AI acceleration claims |

### Preliminary Results Available for Proposal

| Asset | Status | Impact |
|---|---|---|
| AMAZEMET ultrasonic atomizer installed in BYU lab | ✅ Ready | Shows operational readiness for closed-loop powder synthesis |
| 3D-printed AlSi10Mg tensile specimen (printed at U of Utah) | ✅ Ready | Demonstrates LPBF access and printing capability |
| Tensile data for U of Utah specimen | ✅ Ready | Quantitative mechanical property baseline |
| 3D Powder Tech AlSi10Mg tensile specimen | ✅ Ready | Commercial benchmark comparison |
| SEM + EDS of precursor powders (AlSi10Mg, Si powder) | ✅ Ready | Input QC characterization demonstrated |
| SEM + EDS of AMAZEMET-atomized mixture (Al wire + Si addition) | ✅ Ready | Validates ultrasonic atomization with composition modification |
| High-temperature tensile data (standard Al specimen) | ✅ Ready | Elevated-temperature testing capability |
| Thermo-Calc AM Module simulations (provided by TC) | ✅ Ready | CALPHAD/AM integration preliminary results |
| Thermo-Calc simulations on BYU HPC clusters | ✅ Ready | High-throughput CALPHAD screening capability |
| Full pKGFN pipeline implementation | ✅ Ready | Core BOFN algorithm demonstrated end-to-end |
| Automated powder dispensing demonstration | ✅ Ready | Automation infrastructure for closed-loop operation |

---

## Executive Summary

**Three viable approaches** are outlined below, depending on whether you want to preserve the ability to do independent Copilot follow-ups on topic branches:

- **Option 1 (Full Merge to `main`):** Sequential merge of all PRs into `main`, followed by a single integration session. Clean main, but branches are closed and follow-ups require new issues/PRs.
- **Option 2 (Consolidate + Keep Branches on `main`):** Merge content into `main` via `git merge --no-ff` but **do not close the PRs via the GitHub UI**. Branches stay open for independent Copilot follow-ups, and `main` has a consolidated snapshot for integration work.
- **Option 3 (Consolidation Branch — Recommended):** Create a dedicated `consolidation` branch off `main` and merge all PRs there instead. `main` stays clean and untouched, all PR branches remain open for `@copilot` follow-ups, and the consolidation branch provides a unified view of all content for integration work (e.g., populating the LaTeX template). When ready, fast-forward or merge `consolidation` → `main`.

Most PRs are additive (new files) with minimal conflicts, making sequential merging straightforward regardless of which option is chosen. The four shared files (`.gitignore`, `README.md`, `bofn-llm-bo-synthesis.md`, `figures/lpbf_parameter_space.py`) require minor conflict resolution during merge, all of which are mechanical (appending lines or taking the latest version).

Cross-session Copilot orchestration (one PR reading others) is **not recommended** — the context-window cost of loading 20 PR diffs (~280K+ lines) is prohibitive, and sequential merges are cleaner and more auditable.

### Why keep branches open?

Merging all PRs via GitHub's merge button **closes** them, which means:
- You lose the ability to `@copilot` follow-up on an existing topic-specific PR
- Each follow-up requires opening a new issue + PR, losing the comment history context
- Copilot on a merged `main` sees all ~130 files at once, making it easier to pick up unrelated context and get confused

Keeping branches open preserves:
- **Isolated context** — Copilot on PR #44 only sees the preliminary-results files, not the full repo
- **Comment history** — the full conversation thread stays active and actionable
- **Incremental iteration** — you can keep refining individual documents without cross-contamination

### How "Consolidate + Keep Branches" works

1. **Merge content to main locally** using the same wave order (Options A or C below), pushing to `origin main` directly — this brings all content to `main` without using GitHub's merge button
2. **Do NOT use "Merge pull request" in the GitHub UI** — that would close the PR
3. **After merging**, each PR's diff on GitHub will shrink (showing only lines not yet on `main`). PRs with no remaining diff will show "This branch has no new changes" but remain open
4. **For follow-ups**, simply comment `@copilot ...` on the existing PR — Copilot sees the branch context, not the full repo
5. **When a topic is truly done**, close the PR manually via the GitHub UI

> **Trade-off:** GitHub will show some PRs as "up to date" (0-diff) after the merge-to-main step, which looks unusual. This is the cost of preserving branch-level Copilot access. An alternative is to close done PRs and only keep active ones open.

---

## PR Inventory

### Content Categories

| Category | PRs | Purpose |
|---|---|---|
| **Foundation / Literature** | #4, #6, #8, #18, #22 | Edison LITERATURE_HIGH searches forming the knowledge base |
| **Technical Analysis** | #14, #20, #24, #32 | Deep-dive technical topics (BOFN, parameter space, Thermo-Calc, slicing) |
| **Grant Strategy** | #16, #42 | Company landscape (reframed for Topic 3B), publication strategy |
| **Genesis Mission Proposal** | #26, #28, #30, #34, #38, #40, #44, #46, #49 | Topic 3B selection, naming (3B backronym), metrics (3B KPIs), scale-up, LaTeX template, budget, preliminary results, gotchas, AI advantage statement |
| **Meta / Process** | #36 (this PR) | Merge strategy |

### PR Status Summary

| PR | Branch | Title (short) | Files | Conflicts? |
|---|---|---|---|---|
| #2 | *(merged)* | Edison trajectory deep-dive | 2 | — |
| #4 | `copilot/can-calphad-thermocalc-run-high-throughput` | High-throughput CALPHAD | 6 unique | None |
| #6 | `copilot/get-started-deep-literature-search` | 8 Edison lit searches + BOFN demo | 9 unique, 2 shared | `README.md`, `bofn-llm-bo-synthesis.md` |
| #8 | `copilot/identify-databases-for-alloys` | Alloy databases survey | 5+ unique, 1 shared | `README.md` |
| #14 | `copilot/explore-llms-function-networks-bo` | BOFN + LLM-BO (includes pKGFN pipeline) | 5+ unique, 2 shared | `README.md`, `bofn-llm-bo-synthesis.md` |
| #16 | `copilot/identify-companies-involved` | Company landscape (reframed for Genesis Mission/3B) | 5 unique | None |
| #18 | `copilot/explore-welding-data-integration` | Welding data | 1 unique | None |
| #20 | `copilot/explore-24-parameters` | LPBF parameter space (process-general, not topic-specific) | 3 unique, 2 shared | `.gitignore`, `figures/lpbf_parameter_space.py` |
| #22 | `copilot/perform-literature-search-powders` | LPBF superalloy powders | 1 unique | None |
| #24 | `copilot/explore-thermo-calc-am-module` | Thermo-Calc AM module | 1 unique, 1 shared | `README.md` |
| #26 | `genesis-mission` | Genesis Mission — Topic 3B (30+ files: 10 deep-dives, GA scaleup, topic assessments, focus area scan, partnership strategy) | 27 unique, 3 shared | `.gitignore` |
| #28 | `copilot/brainstorm-project-name` | FLAIME naming + title + 3B backronym assessment | 6 unique | None |
| #30 | `copilot/scale-up-validation-am-alloys` | AM scale-up validation | 1 unique, 1 shared | `figures/lpbf_parameter_space.py` |
| #32 | `copilot/research-slicing-software-am-alloys` | Slicing software | 1 unique | None |
| #34 | `copilot/brainstorm-metrics-genesis-mission` | Genesis metrics v4 (14 Edison iters, 3B KPIs incl. mineral-burden) | 1 unique | None |
| #38 | `copilot/create-latex-template-genesis` | LaTeX proposal template (Topic 3B, 5-page narrative) | 2 unique, 1 shared | `.gitignore` |
| #40 | `copilot/assess-budget-requirements` | Budget assessment (Valimet/TC/Ames partnerships, 3B framing) | 1 unique | None |
| #42 | `copilot/edison-scientific-publications` | Publication strategy | 1 unique, 1 shared | `README.md` |
| #44 | `copilot/preliminary-results-collection` | Preliminary results roadmap (Topic 3B, Al-Zr/Al-Mn-Cr-Zr families) | 6 unique | None |
| #46 | `copilot/identify-gotchas-genesis-proposal` | Gotchas analysis (updated for 3B + 3 collab + 8 support letters) | 1 unique | None |
| #49 | `copilot/develop-ai-advantage-statement` | AI advantage statement (Topic 3B, AF/EF/time-ledger metrics) | 1 unique | None |

---

## Conflict Analysis

Only **4 files** are touched by multiple PRs. All conflicts are low-severity:

| File | PRs | Nature of Conflict | Resolution |
|---|---|---|---|
| `.gitignore` | #20, #26, #38 | Each PR appends different ignore patterns | Accept all — append each PR's additions |
| `README.md` | #6, #8, #14, #24, #42 | Each PR adds a line to the Contents list | Accept all — combine all new list entries |
| `bofn-llm-bo-synthesis.md` | #6, #14 | #6 creates initial version (221 lines), #14 replaces with expanded version (400 lines) | Merge #6 first, then #14 overwrites (take #14's version) |
| `figures/lpbf_parameter_space.py` | #20, #30 | #20 creates original, #30 imports from it | Merge #20 first, then #30 adds dependent code |

**Verdict:** No hard conflicts. All resolvable by merge order.

---

## Recommended Merge Order

Merge in **four waves**, each containing PRs that can be merged in parallel (no conflicts within a wave). Within each wave, the listed order handles any residual shared-file conflicts.

### Wave 1 — Foundation (independent, no conflicts with each other)

These PRs only add new files and have zero overlap with each other:

| Order | PR | Rationale |
|---|---|---|
| 1 | **#4** — CALPHAD/Thermo-Calc HPC | Standalone literature, 6 new files |
| 2 | **#16** — Company landscape | Standalone analysis, 5 new files |
| 3 | **#18** — Welding data integration | Standalone Edison trajectory, 1 new file |
| 4 | **#22** — LPBF superalloy powders | Standalone lit search, 1 new file |

> **Expected conflicts:** None. All files are unique to each PR.

### Wave 2 — Literature + Analysis (shared file: `README.md`)

| Order | PR | Rationale |
|---|---|---|
| 5 | **#6** — Deep literature search (8 topics) + initial BOFN | Creates `bofn-llm-bo-synthesis.md` (needed before #14), adds to `README.md` |
| 6 | **#8** — Alloy databases | Adds to `README.md` |
| 7 | **#24** — Thermo-Calc AM module | Adds to `README.md` |
| 8 | **#42** — Publication strategy | Adds to `README.md` |

> **Expected conflicts:** Minor `README.md` content-list conflicts between #6, #8, #24, #42 (append lines). All are mechanical.

### Wave 3 — Technical Deep-Dives (shared file: `bofn-llm-bo-synthesis.md`, `.gitignore`, `figures/`)

| Order | PR | Rationale |
|---|---|---|
| 9 | **#14** — BOFN + LLM-BO benchmarks | Overwrites `bofn-llm-bo-synthesis.md` from #6, adds `benchmarks/` |
| 10 | **#20** — LPBF parameter space | Creates `figures/lpbf_parameter_space.py`, adds `.gitignore` entries |
| 11 | **#30** — AM scale-up validation | Imports from `figures/lpbf_parameter_space.py` (must follow #20) |
| 12 | **#32** — Slicing software | Standalone, 1 new file |

> **Expected conflicts:** #14 will conflict on `bofn-llm-bo-synthesis.md` — take #14's version. #30 must follow #20 for figure dependency.

### Wave 4 — Genesis Mission Proposal (builds on all prior content, all targeting Topic 3B)

| Order | PR | Rationale |
|---|---|---|
| 13 | **#26** — Genesis Mission strategy (largest PR, 30+ files) | Topic 3B deep-dives, focus area scan, GA scaleup with Valimet/Ames partnership strategy, topic assessments. Must be first in wave. |
| 14 | **#28** — FLAIME naming + title (incl. 3B backronym: "Fast-Learning AI for Mineral-Efficient Alloy Design") | Builds on topic selection from #26 |
| 15 | **#34** — Metrics v4 (14 Edison iterations, 3B KPIs) | Extends metrics with mineral-burden KPIs, CMDRI, supply-risk-reduced framing |
| 16 | **#49** — AI advantage statement | AF/EF/time-ledger metrics, partnership context, Topic 3B-specific |
| 17 | **#40** — Budget assessment | Budget for Valimet/AMAZEMET/Thermo-Calc collaboration + Ames support, 3B-reframed |
| 18 | **#44** — Preliminary results roadmap | 19-day sprint plan for Topic 3B: Al-Zr/Al-Mn-Cr-Zr primary, Cu-Cr-Zr complement |
| 19 | **#46** — Gotchas analysis | Weakness analysis with 3 collaboration + 8 support letters, 3B-specific risks |
| 20 | **#38** — LaTeX proposal template | The actual 5-page proposal document. Merge last. Adds `.gitignore` entries. |

> **Expected conflicts:** `.gitignore` accumulates entries from #26 and #38 — accept both. #44, #46, and #49 are standalone new files but depend on #26 for context.

### Final: This PR

| Order | PR | Rationale |
|---|---|---|
| 21 | **#36** — Merge strategy (this PR) | Meta-document. Merge last or close after all others are merged. |

---

## Step-by-Step Merge Instructions

### Option A: Manual sequential merge to `main`

For each PR in the order above:

```bash
# 1. Ensure main is up to date and fetch all remote branches
git checkout main
git pull origin main
git fetch origin --prune

# 2. Merge the PR branch
git merge origin/<branch-name> --no-ff -m "Merge PR #<N>: <title>"

# 3. If conflicts arise (check `git status` for unmerged paths), resolve them:
#    - .gitignore: keep all appended lines from both sides
#    - README.md: keep all list entries from both sides
#    - bofn-llm-bo-synthesis.md: take the incoming (PR #14) version
#    - figures/lpbf_parameter_space.py: take the incoming version
#    Then stage only the resolved files and complete the merge:
#    git add <resolved-files>
#    git commit
#    (If the merge completed without conflicts, the merge commit is
#    already created — skip this step to avoid a "nothing to commit" error.)

# 4. Push
git push origin main
```

### Option B: GitHub UI merge (simpler, but does not preserve the original PR commit graph)

Use GitHub's "Squash and merge" for each PR in the order listed above. This keeps history linear by reducing each PR to a single commit, but it loses the original branch's individual commits and merge structure. GitHub will auto-detect and flag conflicts. For the 4 shared files, resolve via the web editor or locally.

### Option C: Consolidation branch (recommended)

Create a dedicated `consolidation` branch off `main` and merge all PRs there. This keeps `main` clean, preserves all PR branches for `@copilot` follow-ups, and gives you a unified view of all content for integration work.

**Advantages over merging to `main`:**
- `main` stays untouched — no risk of a broken or half-merged main
- All PR branches remain open with their original isolated context
- You can `@copilot` follow up on any PR independently, as before
- The consolidation branch can be recreated from scratch if something goes wrong
- When everything looks good, fast-forward `main` to the consolidation branch

**Step-by-step:**

```bash
# 1. Start fresh from main
git checkout main
git pull origin main
git fetch origin --prune

# 2. Create the consolidation branch
git checkout -b consolidation main

# 3. Merge each PR in wave order
for branch in \
  copilot/can-calphad-thermocalc-run-high-throughput \
  copilot/identify-companies-involved \
  copilot/explore-welding-data-integration \
  copilot/perform-literature-search-powders \
  copilot/get-started-deep-literature-search \
  copilot/identify-databases-for-alloys \
  copilot/explore-thermo-calc-am-module \
  copilot/edison-scientific-publications \
  copilot/explore-llms-function-networks-bo \
  copilot/explore-24-parameters \
  copilot/scale-up-validation-am-alloys \
  copilot/research-slicing-software-am-alloys \
  genesis-mission \
  copilot/brainstorm-project-name \
  copilot/brainstorm-metrics-genesis-mission \
  copilot/develop-ai-advantage-statement \
  copilot/assess-budget-requirements \
  copilot/preliminary-results-collection \
  copilot/identify-gotchas-genesis-proposal \
  copilot/create-latex-template-genesis; do
  git merge origin/$branch --no-ff -m "Merge $branch" || {
    echo "CONFLICT in $branch — resolve manually, then: git add <files> && git commit"
    echo "Re-run this script afterward to continue with remaining branches."
    exit 1
  }
done

# 4. Push the consolidation branch
git push origin consolidation
```

**After merging all PRs to `consolidation`:**
- Use the `consolidation` branch for integration work (populating LaTeX template, cross-referencing, etc.)
- Open a new PR from `consolidation` → `main` when ready to finalize, or fast-forward main:
  ```bash
  git checkout main
  git merge consolidation --ff-only
  git push origin main
  ```
- If a topic branch needs to pick up consolidated content, rebase it:
  ```bash
  git checkout <topic-branch>
  git rebase consolidation
  git push --force-with-lease origin <topic-branch>
  ```
- To start fresh (e.g., after new PR content lands), delete and recreate:
  ```bash
  git branch -D consolidation
  git checkout -b consolidation main
  # Re-run the merge loop above
  ```

### Option D: Legacy integration branch script

Same as Option C but named `integration` — use this if you prefer the simpler approach without the "keep PRs open" workflow:

```bash
git checkout -b integration main
for branch in \
  copilot/can-calphad-thermocalc-run-high-throughput \
  copilot/identify-companies-involved \
  copilot/explore-welding-data-integration \
  copilot/perform-literature-search-powders \
  copilot/get-started-deep-literature-search \
  copilot/identify-databases-for-alloys \
  copilot/explore-thermo-calc-am-module \
  copilot/edison-scientific-publications \
  copilot/explore-llms-function-networks-bo \
  copilot/explore-24-parameters \
  copilot/scale-up-validation-am-alloys \
  copilot/research-slicing-software-am-alloys \
  genesis-mission \
  copilot/brainstorm-project-name \
  copilot/brainstorm-metrics-genesis-mission \
  copilot/develop-ai-advantage-statement \
  copilot/assess-budget-requirements \
  copilot/preliminary-results-collection \
  copilot/identify-gotchas-genesis-proposal \
  copilot/create-latex-template-genesis; do
  git merge origin/$branch --no-ff -m "Merge $branch" || {
    echo "CONFLICT in $branch — resolve manually, then: git add <files> && git commit"
    echo "Re-run this script afterward to continue with remaining branches."
    exit 1
  }
done
```

---

## Cross-Session Copilot Guidance

### Should one Copilot session read other sessions' PRs?

**No — sequential merge (into `main` or a `consolidation` branch) is better.** Reasons:

1. **Context window limits.** The 20 open PRs contain ~280K+ lines of additions across ~130 files. No single Copilot session can hold all of this in context.

2. **Additive content.** Most PRs add new files without modifying existing ones. There's no "reconciliation" needed — just merging.

3. **The 4 conflict files are trivial.** All are either append-only (`.gitignore`, `README.md`) or supersede (take latest version for `bofn-llm-bo-synthesis.md`).

4. **Auditability.** Sequential merges produce a clean `git log` showing exactly which PR contributed what.

### Preserving independent Copilot follow-ups

If using the **Consolidation Branch** approach (Option C, recommended):

- All PRs stay open — `main` is untouched, `consolidation` holds the unified snapshot
- Continue using `@copilot` on individual PRs for topic-specific follow-ups
- Copilot on an open branch sees only that branch's files, avoiding confusion from unrelated content
- The `consolidation` branch serves as a read-only integration point for cross-cutting work (LaTeX template, final review)
- When a topic branch needs to pick up consolidated content, rebase onto `consolidation` and force-push — this refreshes the branch while keeping the PR open
- The consolidation branch can be deleted and recreated at any time if branches have diverged significantly

### When a cross-session approach *would* help

After all PRs are merged into the `consolidation` branch, a **single integration Copilot session** could:

- Read the `consolidation` branch with all content available
- Populate the LaTeX template (#38) with content from the Edison trajectories, targeting Topic 3B
- Incorporate the AI advantage statement (#49) into the Decision Gate Metrics section
- Integrate the preliminary results (atomizer photos, tensile data, SEM/EDS, CALPHAD simulations, pKGFN demo, automated dispensing) into the narrative
- Ensure partnership references (Valimet, AMAZEMET, Thermo-Calc collaborations; Ames, Fehrmann, Sparks, Speer, Clare, Stiles, Hattrick-Simpers, Brown support) are consistent across all sections
- Ensure cross-references between documents are consistent
- Generate a final consolidated `README.md` table of contents
- Verify all Edison trajectory citations are consistent

This is the recommended post-merge step, and it could be filed as a new issue: *"Populate LaTeX proposal template with merged Edison trajectory content."*

---

## Dependency Graph

```
Wave 1 (independent):
  #4  ─┐
  #16 ─┤
  #18 ─┤── all merge cleanly
  #22 ─┘

Wave 2 (shared: README):
  #6  ──→ #8 ──→ #24 ──→ #42
       (README)  (README)  (README)

Wave 3 (shared: bofn doc, figures):
  #14 (depends on #6 for bofn-llm-bo-synthesis.md)
   ↓
  #20 ──→ #30 (figures/lpbf_parameter_space.py)
   ↓
  #32 (independent)

Wave 4 (Genesis Mission Topic 3B, builds on all):
  #26 ──→ #28 ──→ #34 ──→ #49 ──→ #40 ──→ #44 ──→ #46 ──→ #38
  (strategy) (naming) (metrics) (AI adv.) (budget) (prelim   (gotchas) (LaTeX)
                                                    results)
```

---

## Issue Cross-Reference

Each open issue maps to one or more PRs. After merging, issues can be closed:

| Issue | PR(s) | Can Close After Merge? |
|---|---|---|
| #1 | #2 (merged) | ✅ Already closeable |
| #3 | #4 | ✅ Yes |
| #5 | #6 | ✅ Yes |
| #7 | #8 | ✅ Yes |
| #9 | #10 (closed) | ✅ Yes (PR closed, issue can close separately) |
| #11 | #12 (closed) | ✅ Yes (PR closed, issue can close separately) |
| #13 | #14 | ✅ Yes |
| #15 | #16 | ✅ Yes |
| #17 | #18 | ✅ Yes |
| #19 | #20 | ✅ Yes |
| #21 | #22 | ✅ Yes |
| #23 | #24 | ✅ Yes |
| #25 | (no PR) | ❌ Needs separate work |
| #27 | #28 | ✅ Yes |
| #29 | #30 | ✅ Yes |
| #31 | #32 | ✅ Yes |
| #33 | #34 | ✅ Yes |
| #35 | #36 (this PR) | ✅ Yes, after strategy is reviewed |
| #37 | #38 | ✅ Yes |
| #39 | #40 | ✅ Yes |
| #41 | #42 | ✅ Yes |
| #43 | #44 | ✅ Yes |
| #45 | #46 | ✅ Yes |
| #47 | (no PR) | ❌ Needs separate work (Contact Meta/BoTorch) |
| #48 | #49 | ✅ Yes |

---

## Post-Merge Checklist

After all 20 PRs are merged (to `consolidation` branch or `main`):

- [ ] Verify `README.md` table of contents includes all new documents
- [ ] Verify `.gitignore` has all needed patterns (LaTeX, figures, literature)
- [ ] Run the LaTeX build (`pdflatex` + `bibtex`) for `genesis-mission-proposal/`
- [ ] Run any Python figure scripts (`figures/`, `benchmarks/`) to verify they still execute
- [ ] Verify pKGFN pipeline (`benchmarks/partial_kgfn/`) runs end-to-end
- [ ] Verify all partnership references are consistent (3 collaboration + 8 support letters)
- [ ] Verify all Topic 3B references are consistent (no remaining 12F/11C refs except in archived docs)
- [ ] Verify all 4 shared-file conflicts resolved correctly
- [ ] Verify preliminary results are referenced in the LaTeX template todonotes
- [ ] Open a new issue: *"Populate LaTeX proposal template with merged Edison trajectory content for Topic 3B"*
- [ ] **If using Consolidation Branch (Option C):** Keep all PRs open — use `@copilot` for follow-ups on individual topic branches. Open a PR from `consolidation` → `main` when ready to finalize.
- [ ] **If using Full Merge to `main` (Option A):** Decide which PRs to keep open for follow-up (recommended: #38, #44, #46, #49) vs. close as done (e.g., #4, #18, #22)
- [ ] Consider archiving completed Edison trajectory raw outputs if repo size is a concern

---

## Estimated Effort

| Task | Time | Who |
|---|---|---|
| Wave 1 merge (4 PRs) | ~5 min | Human or Copilot |
| Wave 2 merge (4 PRs) | ~10 min | Human or Copilot (minor README conflicts) |
| Wave 3 merge (4 PRs) | ~10 min | Human or Copilot (bofn + figures conflicts) |
| Wave 4 merge (8 PRs) | ~20 min | Human or Copilot (.gitignore conflicts) |
| Post-merge verification | ~15 min | Human |
| **Total** | **~60 min** | |
