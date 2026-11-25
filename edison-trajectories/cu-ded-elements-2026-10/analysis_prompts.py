"""Phases 2 and 3 (Edison ANALYSIS, with the phase-1 answers uploaded).

As in the aluminum run (branch copilot/determine-bounds-for-elements):
phase 2 turns the per-element and joint answers into one bounds table, and
phase 3 adds multi-element constraints. Here the two run side by side rather
than in sequence, to fit the 3-hour job limit; phase 3 gets the same
uploads and does not see phase 2's table.
"""

import pathlib

from queries import CONTEXT

HERE = pathlib.Path(__file__).resolve().parent


def uploads() -> list:
    files = sorted(p.relative_to(HERE).as_posix() for p in (HERE / "phase1").glob("*.md"))
    return files + ["verdicts.md", "tccu7_coverage.md"]


PALETTE_PROMPT = CONTEXT + """
TASK: FINAL PALETTE AND BOUNDS TABLE (synthesis of the attached files).

Attached are 50 per-element literature answers (phase1/el-NN-X.md: one per
element, each ending in a VERDICT line), a joint short-list answer
(phase1/joint-shortlist.md), a table of the parsed verdicts (verdicts.md),
and the coverage of each element in Thermo-Calc's TCCU7 copper database
(tccu7_coverage.md: assessed Cu-X-Y ternaries, and whether Cu-Ni-X and
Cu-Al-X are assessed).

Use ONLY the attached files. Produce:
1. The PALETTE: the elements to search over as designed additions (aim for
   8-14 besides Cu), ranked, with a two-sentence reason each that cites the
   attached answer. Apply these rules and say where you depart from them:
   (a) it must help seawater resistance, DED soundness, repair on cast NAB or
   wrought Cu-Ni, or replace nickel; (b) it must be meltable and atomizable
   in an alumina or zirconia crucible at <= 1,300 C; (c) no element whose
   main hazard (toxicity, regulation) blocks in-house powder making or laser
   deposition; (d) prefer elements whose Cu-X-Y systems are assessed in
   TCCU7, and flag any palette element that is not in TCCU7 at all; (e)
   critical-mineral status is a cost to carry as an objective, not a reason
   to exclude by itself.
2. One markdown table for Cu plus the palette with exactly these columns:
   | Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Functional floor when active (wt%) | Family (Cu-Ni / Al bronze / both) | Upper bound set by | TCCU7 tier | Source files |
   Recommended upper bound = the bound to USE in the search. Justify each
   choice between conservative and non-conservative from the attached
   evidence. Cu: give Cu_min instead.
3. A second table of IMPURITY LIMITS for the powder and the deposit (for
   example C, S, P, Pb, Bi, Se, Te, O, H, N, Zn in Cu-Ni), with the limit and
   its source.
4. A list of EXCLUDED elements, each with a one-line reason and the file it
   comes from, grouped by reason (toxicity; immiscible or above the melting
   limit; no benefit found; not in TCCU7 and little evidence; cost).
5. Disagreements between the per-element answers and the joint answer, and
   how you resolved each.
6. Elements whose evidence is thin or contradictory, as candidates for
   early CALPHAD checks or experiments.
Express all compositions in wt%. Output a single copy-pasteable markdown
section.
"""

CONSTRAINTS_PROMPT = CONTEXT + """
TASK: MULTI-ELEMENT CONSTRAINTS AND EDGE CASES (from the attached files).

Attached are 50 per-element literature answers (phase1/el-NN-X.md, each with
an INTERACTIONS section), a joint short-list answer, the parsed verdicts, and
the TCCU7 coverage table. Per-element bounds are not enough for a safe search
space. Using ONLY the attached files (cite the file for each number), write a
markdown section "Multi-element constraints and edge cases" with:
1. SIMPLEX AND SPARSITY: Cu as balance; Cu_min; how many designed additions
   per composition (k); the dosing floor for an active element given 0.5 kg
   charges weighed to 0.1 mg and induction melting losses.
2. FAMILY STRUCTURE: one continuous space or a Cu-Ni branch and an aluminum
   bronze branch, and the rules that define each (e.g. Ni range, Al range);
   what lies between (Cu-Ni-Al alloys) and whether to search it.
3. SUM AND RATIO CONSTRAINTS, each as an inequality with numbers: the
   aluminum equivalent for retained beta and martensite in aluminum bronze;
   Fe and Ni (and Fe/Ni) in NAB for kappa phases; Fe and Mn in Cu-Ni (Fe kept
   in solid solution); Cr with Fe and Si in Cr-modified Cu-Ni; Mn in place of
   Ni; total solute versus the liquidus (<= about 1,250 C for atomization);
   impurity sums for weld and DED cracking (Pb, S, P, C, Bi, Se, Te).
4. TCCU7 GUARDRAILS: palette pairs with no assessed Cu-X-Y ternary, and
   joint caps when both are active.
5. ATOMIZATION AND DED EDGE CASES: volatile elements (Zn, Mn, Mg) and their
   loss; reactive elements and crucibles or sonotrodes; oxygen pickup.
6. REPAIR EDGE CASES: dilution into cast NAB and wrought Cu-Ni and the
   composition of the mixed zone (e.g. a Cu-Ni deposit on NAB), and galvanic
   pairing of deposit and substrate.
Express all compositions in wt%.
"""

LATER_PHASES = {
    2: {"palette-bounds-table": {"job": "ANALYSIS", "query": PALETTE_PROMPT,
                                 "uploads": uploads()}},
    3: {"multi-element-constraints": {"job": "ANALYSIS", "query": CONSTRAINTS_PROMPT,
                                      "uploads": uploads()}},
}
