"""The copper/DED composition search space: single source of truth (PR #117).

Elements, bounds (wt%, Cu balance), conditional constraints and impurity
limits chosen from the 50 per-element Edison answers (phase1/), the joint
short-list answer (phase1/joint-shortlist.md), the two ANALYSIS syntheses
(phase2/, phase3/), the subagent checks (checks.md) and TCCU7 coverage
(tccu7_coverage.md). README.md gives the reasoning element by element.

Conventions, as in the aluminum bounds table
(branch copilot/determine-bounds-for-elements):
- "conservative": the highest value used in an established commercial or Navy
  alloy, or demonstrated in AM or cladding;
- "nonconservative": defensible but aggressive (experimental alloys, phase or
  liquidus limits);
- "upper": the bound the search uses;
- "floor": the smallest content that counts as "active" when the element is on.

Run: python search_space.py  (writes search_space.md and search_space_table.tex)
"""

import pathlib

from tccu7_coverage import palette_stats, row, tier

HERE = pathlib.Path(__file__).resolve().parent

CU_MIN = 65.0              # conservative; per-element Cu answer and joint answer
LIQUIDUS_MAX_C = 1250.0    # atomizer: induction module reaches about 1,300 C

# (element, upper, conservative, nonconservative, floor, family, set by, sources)
PALETTE = [
    ("Ni", 30.0, 30.0, 33.0, 2.0, "both (NAB <= 5.5)",
     "liquidus: 70-30 melts to about 1,240 C and the atomizer reaches about 1,300 C; nickel burden is an objective",
     "el-02, joint, phase2, checks; C71500 29-33"),
    ("Al", 9.5, 9.5, 10.5, 1.5, "both",
     "retained beta / beta-prime martensite as deposited, already present in laser-deposited C95800, so the boundary lies inside the space",
     "el-03, joint, phase2; C95800 8.5-9.5, C63000 9-11, MARINEL 1.6-2.3"),
    ("Fe", 4.5, 4.5, 5.5, 0.4, "both",
     "Fe out of solution in Cu-Ni (pitting, crevice); coarse Fe-rich kappa in NAB",
     "el-04, joint, phase2, checks; C70600 1.0-1.8, C71640 1.7-2.3, C95800 3.5-4.5"),
    ("Mn", 4.0, 2.5, 5.0, 0.3, "both (NAB <= 1.5 to start)",
     "evaporation and oxidation in melting and DED; beta stabilizer in aluminum bronze",
     "el-05, joint, checks; C71640 1.5-2.5, C95800 0.8-1.5, ERCuNiAl 0.6-3.5, MARINEL 3.8-5.3"),
    ("Cr", 0.7, 0.7, 2.0, 0.3, "Cu-Ni (Al <= 3)",
     "Cr-rich particles and oxide skin; higher-Cr Cu-Ni had worse crevice attack than C71500 in still water",
     "el-06, joint, phase2, checks; C72200 0.3-0.7"),
    ("Si", 0.5, 0.3, 1.0, 0.1, "Cu-Ni (Al < 7)",
     "silicides and weld cracking; C95800 allows only 0.10; strengthens cast Cu-Ni only with Nb",
     "el-09, el-10, joint, checks; C96400 <= 0.5"),
    ("Nb", 0.8, 0.8, 1.5, 0.3, "Cu-Ni (Al <= 3)",
     "undissolved or coarse Nb-rich particles: Nb melts at 2,477 C, so it is added as a master alloy and its dissolution at 1,300 C must be shown; C96400 castings allow 1.5",
     "el-10, joint, phase2; C96400 0.5-1.5, MARINEL 0.6-0.9"),
    ("Ti", 0.5, 0.2, 0.8, 0.05, "both (NAB <= 0.1)",
     "oxide and nitride inclusions, crucible attack, poor recovery",
     "el-13, joint, checks; ERCuNi filler 0.20-0.50"),
]

# Microalloying additions, searched from Year 2 once the core space is mapped
# (thin or indirect evidence; see decisions.py).
OPTIONAL = [
    ("Zr", 0.15, 0.15, 0.3, 0.01, "both",
     "ZrO2 inclusions and crucible reaction; about half lost on melting; excess above its solubility goes to grain boundaries; Cu-Ni-Zr not assessed in TCCU7",
     "el-14, joint, checks; C15000 0.10-0.20"),
    ("B", 0.02, 0.02, 0.05, 0.002, "both (Cu-Ni <= 0.01)",
     "borides; a Ni-B eutectic (about 1,090 C) below the Cu-30Ni solidus; no Cu-B-X ternary in TCCU7",
     "el-19, joint, checks"),
    ("Sn", 1.0, 0.2, 1.0, 0.5, "NAB only (Cu-Ni <= 0.05)",
     "wide freezing range and Sn-rich boundary phases; benefit shown only for cast NAB grain refinement and strength (Poojary 2023)",
     "el-07, joint, checks; C63000 Sn <= 0.20"),
    ("La or Ce", 0.1, 0.05, 0.1, 0.02, "Cu-Ni",
     "oxide and oxysulfide inclusions; one rare-earth variable; B10 with 0.1 La or Ce beat Cu-10Ni in 3.5% NaCl (Du 2025). Y (0.021 best in one cast Cu-10Ni study; not in TCCU7) is the alternative phase2 preferred",
     "el-44, el-45, el-43, joint, phase2, checks"),
    ("Ge", 0.2, 0.2, 1.0, 0.2, "NAB only",
     "one matched 0 vs 0.2 test: the only lead is a heat-treated powder-metallurgy NAB with 31% lower jet erosion-corrosion loss but other changes too; cost and export controls",
     "el-37, phase2, checks"),
]

# Conditional constraints (hard unless marked soft). Al sets the family.
CONSTRAINTS = [
    ("Cu balance", "Cu >= 65", "el-01; joint"),
    ("Liquidus", "CALPHAD liquidus <= 1,250 C for every candidate (atomizer superheat); 70-30 already melts at about 1,240 C",
     "el-01, el-02; joint; checks"),
    ("NAB rules", "if Al >= 7: Fe <= Ni <= 5.5, Si <= 0.1, Ti <= 0.1",
     "el-01, el-04, el-09, el-13; joint; phase2; C95800 (Ni 4.0-5.0, Fe 3.5-4.5, Si <= 0.10), C63000 (Ni 4.0-5.5)"),
    ("Cu-Ni rule", "if Al < 1.5: Fe <= 2.3 (kept in solid solution)", "el-04; joint; C71640 max 2.3"),
    ("Cu-Ni-Al rule", "if 1.5 <= Al < 7 and Ni >= 10: Fe <= 1.0", "joint (MARINEL Fe about 1 max, for stress-corrosion resistance)"),
    ("Cr, Nb, Si", "Cr, Nb > 0 only if Al <= 3; Si > 0.1 only if Al < 7", "el-06, el-09, el-10; joint"),
    ("Nb with Si", "if Si > 0.1: Nb >= 1.55 Si - 0.10 (cast Cu-Ni weldability rule; stricter practice Nb >= 2 Si)",
     "el-10 (Van Konynenburg 1990 review)"),
    ("Retained beta", "no fixed aluminum equivalent: predicted by CALPHAD along the DED thermal history (Advance 3, H3)",
     "el-03; joint (Al_eq coefficients unverified)"),
    ("Sparsity", "at most 6 active additions in all (soft)", "phase3 (a search-policy choice, not a literature limit)"),
    ("Low-melting impurities", "track BiE = Bi + 0.7 Te + 0.4 Pb + 0.2 Se + 0.1 S (Cu-Ni hot-ductility index; about 0.009 at the caps); not a hard limit",
     "el-27; phase3"),
]

# Impurity limits for powder and deposit (wt%). Outer = commercial or weld-grade ceiling.
IMPURITIES = [
    ("Zn", 0.5, 1.0, "C71500 welding grade (outer: C71500 general)", "el-08; joint"),
    ("Pb", 0.01, 0.02, "C96400 0.010; C71500 welding grade and ERCuNi 0.02", "el-23; joint; checks"),
    ("P", 0.02, 0.02, "C71500 welding grade; ERCuNi", "el-22; joint"),
    ("S", 0.01, 0.02, "ERCuNi 0.01; C71500 welding grade 0.02", "el-27; joint"),
    ("C", 0.02, 0.05, "C71500 welding grade 0.05; graphite pickup", "el-32; joint; checks"),
    ("Bi", 0.001, 0.002, "grain-boundary films at ppm levels", "el-24; joint; checks"),
    ("Se", 0.006, 0.006, "copper refinery practice", "el-25"),
    ("Te", 0.003, 0.003, "copper refinery practice", "el-26"),
    ("Sb", 0.02, 0.02, "", "el-21"),
    ("As", 0.005, 0.02, "not added; 5 ppm (C10100) is a feedstock aim only", "el-20; checks"),
    ("Sn", 0.05, 0.2, "when not an addition: EN Cu-Ni grades (outer: C63000)", "el-07; checks"),
    ("Mg", 0.01, 0.05, "deoxidizer residual", "el-16; checks"),
    ("Cd", 0.01, 0.01, "toxic; never added", "el-28"),
    ("Mo", 0.02, 0.1, "TZM sonotrode pickup (outer for Cu-Ni with >= 10 Ni)", "el-33; checks"),
    ("O", 0.02, 0.03, "powder; ultrasonically atomized NAB powder had 0.013", "el-29; joint; checks"),
    ("H", 0.0005, 0.001, "dried powder; porosity is the acceptance test", "el-30; joint; checks"),
    ("N", 0.001, 0.002, "argon shielding; 22 ppm went with about 10% porosity in the one direct study", "el-31; joint; checks"),
]

EXCLUDED = {
    "toxic powders and fume": ["Be", "Cd"],
    "immiscible with Cu, melting far above the atomizer limit": ["W", "Ta"],
    "no seawater benefit found and little evidence": ["V", "Ca", "Sr", "Li", "Ga", "In", "Hf"],
    "rare earths beyond the one optional slot (most not in TCCU7)": ["Sc", "Y", "Pr", "Nd", "Er", "Gd"],
    "cost, with only single-study evidence": ["Ag", "Pd"],
    "counted with Ni in the specifications, and scarcer than Ni": ["Co"],
    "impurity limits only": ["Zn", "Mg", "P", "S", "Pb", "Bi", "Se", "Te", "Sb", "As", "C", "Mo", "O", "H", "N"],
}


def markdown() -> str:
    names = [p[0] for p in PALETTE]
    st = palette_stats(names)
    lines = ["# Copper/DED search space (generated by `search_space.py`)", "",
             f"Cu is the balance: at least {CU_MIN:g} wt%. "
             f"Every candidate must have a CALPHAD liquidus of at most {LIQUIDUS_MAX_C:,.0f} °C.", "",
             "## Palette (designed additions)", "",
             "| Element | Range searched (wt%) | Conservative upper | Non-conservative upper | "
             "Floor when active | Family | Upper bound set by | TCCU7 tier | Sources |",
             "| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |"]
    for el, up, cons, non, floor, fam, why, src in PALETTE:
        lines.append(f"| {el} | 0-{up:g} | {cons:g} | {non:g} | {floor:g} | {fam} | {why} | "
                     f"{tier(row(el))} | {src} |")
    lines += ["", "## Microalloying additions (from Year 2)", "",
              "| Element | Range (wt%) | Conservative | Non-conservative | Floor | Family | Upper bound set by | TCCU7 tier | Sources |",
              "| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |"]
    for el, up, cons, non, floor, fam, why, src in OPTIONAL:
        t = "; ".join(f"{e} {tier(row(e))}" for e in el.split(" or ")) if " or " in el else tier(row(el))
        lines.append(f"| {el} | 0-{up:g} | {cons:g} | {non:g} | {floor:g} | {fam} | {why} | {t} | {src} |")
    lines += ["", "## Constraints", "", "| Name | Rule | Source |", "| --- | --- | --- |"]
    lines += [f"| {n} | {r} | {s} |" for n, r, s in CONSTRAINTS]
    lines += ["", "## Impurity limits (powder and deposit)", "",
              "| Element | Limit (wt%) | Outer limit (wt%) | Basis | Source |",
              "| --- | ---: | ---: | --- | --- |"]
    lines += [f"| {el} | {lim:g} | {outer:g} | {basis} | {src} |" for el, lim, outer, basis, src in IMPURITIES]
    lines += ["", "## Excluded", ""]
    lines += [f"- **{reason}:** {', '.join(els)}" for reason, els in EXCLUDED.items()]
    lines += ["", "## TCCU7 coverage of the palette", "",
              f"- {st['pairs_covered']} of {st['pairs']} palette pairs have an assessed Cu-X-Y ternary.",
              f"- Cu-X-Y-Z quaternaries by number of assessed constituent ternaries (of 4): "
              f"{st['quaternaries_by_assessed_ternaries']}.",
              f"- Pairs without an assessed Cu-X-Y ternary: {', '.join(st['pairs_without_ternary'])}.",
              f"- Palette elements not in TCCU7: {', '.join(st['not_in_tccu7']) or 'none'}."]
    return "\n".join(lines) + "\n"


def latex_rows() -> str:
    out = []
    for el, up, cons, non, floor, fam, why, src in PALETTE:
        out.append(f"{el} & 0--{up:g} & {why} \\\\")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    md = markdown()
    (HERE / "search_space.md").write_text(md)
    (HERE / "search_space_table.tex").write_text(latex_rows())
    print(md)
