#!/usr/bin/env python3
"""
FLAIME Genesis Mission Proposal — Cross-Document Consistency Checker

Scans the LaTeX source, population plan, and checklist for inconsistencies
in numbers, terminology, cross-references, and FOA compliance.

Usage:
    python3 .github/skills/proposal-consistency-check/check_consistency.py
"""

import os
import re
import sys
from dataclasses import dataclass, field
from math import comb
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration — CANONICAL PROPOSAL PARAMETERS
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
TEX_FILE = REPO_ROOT / "genesis-mission-proposal" / "flaime-genesis-proposal.tex"
PLAN_FILE = REPO_ROOT / "genesis-mission-proposal" / "proposal-population-plan.md"
CHECKLIST_FILE = REPO_ROOT / "genesis-mission-proposal" / "proposal-checklist.md"

# Budget (current as of April 2026 — post-audit rebalance, N=320 consumables sizing)
BUDGET_TOTAL = 750_000
BUDGET_BYU = 600_000           # audited rebalance: MS=2@$25, 4UG-FT@$22.50+8UG-PT@$15/sem, M&S@N=320
BUDGET_VALIMET = 0            # partner-specific amount redacted
BUDGET_AMAZEMET = 0           # partner-specific amount redacted
BUDGET_THERMOCALC = 0         # partner-specific amount redacted

# Personnel
EXPECTED_MS = 2
EXPECTED_UG = 12              # 4 full-time + 8 part-time per semester

# Element palette — 15 NON-Al elements; Al is always the base
PALETTE_ELEMENTS = {"Mn", "Cr", "Zr", "Mg", "Si", "Cu", "Ti", "Fe", "Ni",
                    "Ce", "Sc", "Li", "Er", "Zn", "Sn"}
N_ELEMENTS = 15  # len(PALETTE_ELEMENTS)

# Sub-system counting: k = number of alloying elements chosen (NOT total components)
# k=2 → ternary (Al + 2 elements), k=3 → quaternary, ..., k=8 → 9-component
K_MIN = 2
K_MAX = 8
EXPECTED_SUBSYSTEMS = sum(comb(N_ELEMENTS, k) for k in range(K_MIN, K_MAX + 1))  # 22,803

# Composition targets (softened per Kosmos review April 2026)
COMPOSITION_RANGE = (100, 200)

# Other KPIs
MINERAL_BURDEN_REDUCTION = 40  # percent
DISCOVERY_YIELD = 3            # percent
ACCELERATION_FACTOR = 3        # times vs random baseline
GATE_MONTHS = {1: 3, 2: 5, 3: 7}
EXPECTED_TRLS = {2, 4, 6}     # entry, Phase I exit, Phase II

# FLAIME acronym
FLAIME_EXPANSION = "Fast Learning AI for Mineral Efficiency"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    severity: str   # CRITICAL, WARNING, INFO
    category: str   # NUMERICAL, TERMINOLOGY, CROSS-DOC, FOA-COMPLIANCE, REFERENCE, LOGIC
    message: str
    details: list[str] = field(default_factory=list)


findings: list[Finding] = []


def add(severity: str, category: str, message: str, details: Optional[list[str]] = None):
    findings.append(Finding(severity, category, message, details or []))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.exists():
        add("CRITICAL", "CROSS-DOC", f"Missing file: {path.relative_to(REPO_ROOT)}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def line_numbers_of(text: str, pattern: str, flags: int = 0) -> list[int]:
    result = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(pattern, line, flags):
            result.append(i)
    return result


# ---------------------------------------------------------------------------
# Load files
# ---------------------------------------------------------------------------

tex = read(TEX_FILE)
plan = read(PLAN_FILE)
checklist = read(CHECKLIST_FILE)
all_text = tex + "\n" + plan + "\n" + checklist


# ===========================================================================
# CHECK 1: Numerical consistency
# ===========================================================================

def check_numerical():
    # --- Budget ---
    budget_section = re.search(
        r"Summary Budget Information.*?\\end\{tabularx\}", tex, re.DOTALL
    )
    if budget_section:
        budget_text = budget_section.group(0)
        budget_totals = re.findall(r"\\textbf\{Total\}.*?(\d[\d,]+)", budget_text)
        for bt in budget_totals:
            val = int(bt.replace(",", ""))
            if val != BUDGET_TOTAL:
                add("CRITICAL", "NUMERICAL",
                    f"Budget total in summary table is ${val:,} — expected ${BUDGET_TOTAL:,}",
                    [f"Found: {bt}"])

        byu_budget = re.findall(r"BYU.*?(\d[\d,]+)", budget_text)
        for b in byu_budget:
            val = int(b.replace(",", ""))
            if val not in (BUDGET_BYU,):
                add("WARNING", "NUMERICAL",
                    f"BYU budget in summary table is ${val:,} — expected ${BUDGET_BYU:,}")

        val_budget = re.findall(r"Valimet.*?(\d[\d,]+)", budget_text)
        for v in val_budget:
            val = int(v.replace(",", ""))
            if val not in (BUDGET_VALIMET,):
                add("WARNING", "NUMERICAL",
                    f"Valimet budget is ${val:,} — expected ${BUDGET_VALIMET:,}")

    # --- Personnel ---
    ms_matches = re.findall(r"(\d+)\s*MS\s*student", tex, re.IGNORECASE)
    ug_matches = re.findall(r"(\d+)\s*U[GR]\s*(?:researcher|student|undergrad)", tex, re.IGNORECASE)

    for m in ms_matches:
        if m != str(EXPECTED_MS):
            add("CRITICAL", "NUMERICAL",
                f"MS student count is {m} — expected {EXPECTED_MS}")
    for u in ug_matches:
        if u != str(EXPECTED_UG):
            add("CRITICAL", "NUMERICAL",
                f"UG researcher count is {u} — expected {EXPECTED_UG}")

    ms_plan = re.findall(r"(\d+)\s*MS", plan)
    ug_plan = re.findall(r"(\d+)\s*UG", plan)
    for m in ms_plan:
        if m not in (str(EXPECTED_MS),):
            add("WARNING", "NUMERICAL",
                f"Population plan mentions {m} MS students — expected {EXPECTED_MS}")
    for u in ug_plan:
        if u not in (str(EXPECTED_UG),):
            add("WARNING", "NUMERICAL",
                f"Population plan mentions {u} UGs — expected {EXPECTED_UG}")

    # --- Sub-systems count ---
    # Match the \subsystemcountraw LaTeX variable
    subsys_raw = re.search(r"\\subsystemcountraw\{(\d+)\}", tex)
    if subsys_raw:
        val = int(subsys_raw.group(1))
        if val != EXPECTED_SUBSYSTEMS:
            add("CRITICAL", "NUMERICAL",
                f"\\subsystemcountraw is {val:,} — expected {EXPECTED_SUBSYSTEMS:,}")

    # Also check free-text mentions
    subsys_mentions = re.findall(
        r"(\d[\d,]{3,})\s*(?:sub-?systems|element combinations)", all_text, re.IGNORECASE
    )
    for s in subsys_mentions:
        val = int(s.replace(",", ""))
        if val < 100:
            continue  # skip small numbers from comments/unrelated context
        if val != EXPECTED_SUBSYSTEMS:
            add("CRITICAL", "NUMERICAL",
                f"Sub-system count {val:,} doesn't match Σ C({N_ELEMENTS},k) for k={K_MIN}..{K_MAX} = {EXPECTED_SUBSYSTEMS:,}")

    # Verify the combinatorial formula in LaTeX
    tex_formula = re.search(r"\\sum_\{k=(\d+)\}\^\{(\d+)\}", tex)
    if tex_formula:
        k_lo, k_hi = int(tex_formula.group(1)), int(tex_formula.group(2))
        if k_lo != K_MIN or k_hi != K_MAX:
            add("CRITICAL", "NUMERICAL",
                f"LaTeX formula uses k={k_lo}..{k_hi} — expected k={K_MIN}..{K_MAX}")

    # Also look for \binom{\elementcount}{k} and verify elementcount
    elem_count_match = re.search(r"\\elementcount.*?(\d+)", tex)

    # --- Composition targets ---
    # Accept 100-200 range or individual mentions of 100, 200 near "composition"
    geq200_comp = re.findall(r"\\geq.{0,3}200\s*(?:~|\s)*composition", tex, re.IGNORECASE)
    if geq200_comp:
        add("WARNING", "NUMERICAL",
            f"Found '≥200 compositions' — should be '100–200' range (softened per Kosmos)",
            [f"Matches: {len(geq200_comp)}"])

    # --- Throughput ---
    throughput_max = 2 * 6 * 39  # ~468
    if "468" not in all_text:
        add("INFO", "NUMERICAL",
            "Throughput theoretical max (~468) not found in documents")

    # --- Discovery yield ---
    yields = re.findall(r"[≥>]\s*(\d+(?:\.\d+)?)\s*%.*?discovery\s*yield", all_text, re.IGNORECASE)
    yield_vals = set(float(y) for y in yields)
    if len(yield_vals) > 1:
        add("WARNING", "NUMERICAL",
            f"Multiple discovery yield targets: {yield_vals} (expected ≥{DISCOVERY_YIELD}%)")

    # --- Mineral-burden reduction ---
    mbr_30 = line_numbers_of(tex, r"[≥>\\geq]\s*30\s*\\?%.*?(?:mineral|reduction|MBS)", re.IGNORECASE)
    mbr_40 = line_numbers_of(tex, r"[≥>\\geq]\s*40\s*\\?%.*?(?:mineral|reduction|MBS)", re.IGNORECASE)
    if mbr_30 and mbr_40:
        add("WARNING", "NUMERICAL",
            f"Both 30% and 40% mineral-burden reduction mentioned",
            [f"30% at lines {mbr_30}", f"40% at lines {mbr_40}",
             f"Expected: ≥{MINERAL_BURDEN_REDUCTION}% consistently"])
    elif mbr_30 and not mbr_40:
        add("WARNING", "NUMERICAL",
            f"Mineral-burden reduction is 30% — should be {MINERAL_BURDEN_REDUCTION}%")

    # --- TRL levels ---
    trl_set = set(int(x) for x in re.findall(r"TRL\s*[~]?\s*(\d)", all_text))
    unexpected = trl_set - EXPECTED_TRLS - {9}  # TRL 9 may appear as CMI reference
    if unexpected:
        add("INFO", "NUMERICAL",
            f"Unexpected TRL values: {unexpected} (expected {EXPECTED_TRLS})")

    # --- Go/No-Go gate months ---
    gate_months = {}
    for m in re.finditer(r"^(\d+)\s*&\s*M\d+/G(\d)", tex, re.MULTILINE):
        month = int(m.group(1))
        gate = int(m.group(2))
        gate_months[gate] = month

    for g, expected_mo in GATE_MONTHS.items():
        if g in gate_months and gate_months[g] != expected_mo:
            add("WARNING", "NUMERICAL",
                f"G{g} is at month {gate_months[g]} — expected month {expected_mo}")


# ===========================================================================
# CHECK 2: Terminology consistency
# ===========================================================================

def check_terminology():
    # --- FLAIME acronym ---
    flaime_tex = re.findall(r"FLAIME.*?Fast Learning AI for (\w+ \w+)", tex)
    for exp in flaime_tex:
        if exp.lower() != "mineral efficiency":
            add("CRITICAL", "TERMINOLOGY",
                f"FLAIME expansion mismatch: 'Fast Learning AI for {exp}'",
                [f"Expected: '{FLAIME_EXPANSION}'"])

    # --- Database name TCAl10 vs TCAL8 ---
    tcal8_refs = line_numbers_of(tex, r"TCAl?8\b", re.IGNORECASE)
    if tcal8_refs:
        add("CRITICAL", "TERMINOLOGY",
            f"TCAL8 referenced in .tex (should be TCAl10)",
            [f"Lines: {tcal8_refs}"])

    tcal8_plan = line_numbers_of(plan, r"TCAl?8\b", re.IGNORECASE)
    if tcal8_plan:
        add("WARNING", "TERMINOLOGY",
            f"TCAL8 referenced in population plan (should be TCAl10)",
            [f"Lines: {tcal8_plan}"])

    # --- LPBF vs L-PBF ---
    lpbf_count = len(re.findall(r"\bLPBF\b", tex))
    l_pbf_count = len(re.findall(r"\bL-PBF\b", tex))
    if lpbf_count > 0 and l_pbf_count > 0:
        add("WARNING", "TERMINOLOGY",
            f"Mixed LPBF/L-PBF usage: LPBF={lpbf_count}, L-PBF={l_pbf_count}")

    # --- Thermo-Calc spelling ---
    bad_tc = []
    # Strip email addresses before checking (thermocalc.com is the correct domain)
    tex_no_emails = re.sub(r'\S+@thermocalc\.\S+', '', tex)
    if re.search(r"ThermoCalc", tex_no_emails, re.IGNORECASE):
        bad_tc.append("ThermoCalc")
    if re.search(r"Thermocalc(?![\w-])", tex_no_emails):
        bad_tc.append("Thermocalc")
    if bad_tc:
        add("WARNING", "TERMINOLOGY",
            f"Non-standard Thermo-Calc spelling: {bad_tc}")

    # --- AMAZEMET casing ---
    amazemet_lower = line_numbers_of(tex, r"(?<![A-Z])Amazemet(?![A-Z])")
    if amazemet_lower:
        add("WARNING", "TERMINOLOGY",
            f"'Amazemet' (lowercase) found — should be 'AMAZEMET'",
            [f"Lines: {amazemet_lower}"])

    # --- pycalphad casing ---
    bad_pycalphad = re.findall(r"PyCalphad|PYCALPHAD|Pycalphad", tex)
    if bad_pycalphad:
        add("INFO", "TERMINOLOGY",
            f"pycalphad should be lowercase: found {bad_pycalphad}")

    # --- Sub-size vs subsize ---
    subsize_variants = {
        "sub-size": len(re.findall(r"sub-size", tex, re.IGNORECASE)),
        "subsize": len(re.findall(r"(?<!-)subsize", tex, re.IGNORECASE)),
        "sub size": len(re.findall(r"sub size", tex, re.IGNORECASE)),
    }
    active = {k: v for k, v in subsize_variants.items() if v > 0}
    if len(active) > 1:
        add("INFO", "TERMINOLOGY", f"Mixed 'sub-size' variants: {active}")

    # --- $TBD budget placeholders ---
    tbd_lines = line_numbers_of(tex, r"\$TBD")
    if tbd_lines:
        add("WARNING", "NUMERICAL",
            f"Budget placeholder '$TBD' still present",
            [f"Lines: {tbd_lines}"])

    # --- MVS defined before first use ---
    mvs_first = tex.find("MVS")
    mvs_def = tex.find("minimum-viable-specimen (MVS)")
    if mvs_def == -1:
        mvs_def = tex.find("Minimum Viable Specimen (MVS)")
    if mvs_first != -1 and mvs_def != -1 and mvs_first < mvs_def:
        first_line = tex[:mvs_first].count('\n') + 1
        def_line = tex[:mvs_def].count('\n') + 1
        add("WARNING", "TERMINOLOGY",
            f"MVS used at line ~{first_line} before definition at line ~{def_line}")


# ===========================================================================
# CHECK 3: LaTeX cross-references
# ===========================================================================

def check_references():
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", tex))

    broken = refs - labels
    if broken:
        add("CRITICAL", "REFERENCE",
            f"Broken \\ref references (no matching \\label): {broken}")

    unused = labels - refs
    if unused:
        add("INFO", "REFERENCE",
            f"Labels defined but never \\ref'd: {unused}",
            ["May be intentional for appendix figures"])

    # \lipsum placeholder text
    lipsum_lines = line_numbers_of(tex, r"\\lipsum")
    if lipsum_lines:
        add("CRITICAL", "CROSS-DOC",
            f"\\lipsum still present (placeholder text!)",
            [f"Lines: {lipsum_lines}"])

    # Placeholder content
    placeholder_lines = line_numbers_of(tex, r"Placeholder:")
    if placeholder_lines:
        add("WARNING", "CROSS-DOC",
            f"Placeholder content still in .tex",
            [f"Lines: {placeholder_lines}",
             "Replace with actual figures/content before submission"])


# ===========================================================================
# CHECK 4: FOA compliance
# ===========================================================================

def check_foa_compliance():
    # Buy America statement in first 2 pages of narrative
    # Team 2-of-3 categories
    has_ihe = bool(re.search(r"BYU|Brigham Young|universit", tex, re.IGNORECASE))
    has_industry = bool(re.search(r"Valimet|AMAZEMET", tex))
    categories = sum([has_ihe, has_industry])
    if categories < 2:
        add("WARNING", "FOA-COMPLIANCE",
            f"Team has {categories}/2 required institution categories")

    # Abstract: "Application Stage: Phase I"
    abstract_end = tex.find(r"\newpage")
    abstract_section = tex[:abstract_end] if abstract_end > 0 else tex[:5000]
    if "Application Stage" not in abstract_section:
        add("CRITICAL", "FOA-COMPLIANCE",
            "Abstract missing 'Application Stage: Phase I'",
            ["FOA §IV.C requires application stage in abstract header"])

    # Abstract: no \cite{} (must be self-contained)
    abstract_start = tex.find(r"\section*{Project Summary")
    if abstract_start >= 0:
        abstract_text = tex[abstract_start:abstract_end] if abstract_end > abstract_start else ""
        cite_in_abstract = re.findall(r"\\cite\{", abstract_text)
        if cite_in_abstract:
            add("WARNING", "FOA-COMPLIANCE",
                f"Abstract contains {len(cite_in_abstract)} \\cite commands — abstract must be self-contained",
                ["Use inline parenthetical (Author, Year) instead"])

    # Abstract: coinvestigators listed
    if abstract_start >= 0:
        abstract_header = tex[abstract_start:abstract_start + 2000]
        if not re.search(r"Senior.*Key.*Personnel|[Cc]oinvestigator|Partner.*:.*\w+\.\s*\w+", abstract_header):
            add("INFO", "FOA-COMPLIANCE",
                "Abstract may not list coinvestigator names (FOA wants names + affiliations)")

    # DMSP not required at submission
    if "not required" not in tex.lower() and "NOT required" not in tex:
        add("INFO", "FOA-COMPLIANCE",
            "Consider noting DMSP is not required at Phase I submission")


# ===========================================================================
# CHECK 5: Cross-document consistency
# ===========================================================================

def check_cross_doc():
    # Element palette
    tex_elements = set(re.findall(
        r"\b(Mn|Cr|Zr|Mg|Si|Cu|Ti|Fe|Ni|Ce|Sc|Li|Er|Zn|Sn)\b", tex
    ))
    tex_missing = PALETTE_ELEMENTS - tex_elements
    if tex_missing:
        add("WARNING", "CROSS-DOC",
            f"Elements missing from .tex: {tex_missing}")

    plan_elements = set(re.findall(
        r"\b(Mn|Cr|Zr|Mg|Si|Cu|Ti|Fe|Ni|Ce|Sc|Li|Er|Zn|Sn)\b", plan
    ))
    plan_missing = PALETTE_ELEMENTS - plan_elements
    if plan_missing:
        add("INFO", "CROSS-DOC",
            f"Elements missing from population plan: {plan_missing}")

    # Figure count
    tex_fig_count = len(re.findall(r"\\begin\{figure\}", tex))
    if tex_fig_count == 0:
        add("WARNING", "CROSS-DOC", "No figures found in .tex")

    # Word count estimate for narrative
    narrative_match = re.search(
        r"\\setcounter\{page\}\{1\}(.*?)(?=\\newpage\s*\\section\*\{Appendix|$)",
        tex, re.DOTALL
    )
    if narrative_match:
        narrative = narrative_match.group(1)
        stripped = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", " ", narrative)
        stripped = re.sub(r"\\[a-zA-Z]+", " ", stripped)
        stripped = re.sub(r"\{[^}]*\}", " ", stripped)
        stripped = re.sub(r"%.*$", "", stripped, flags=re.MULTILINE)
        stripped = re.sub(r"\\begin\{.*?\\end\{[^}]+\}", " ", stripped, flags=re.DOTALL)
        words = len(stripped.split())
        if words > 2000:
            add("WARNING", "CROSS-DOC",
                f"Estimated narrative word count: ~{words} (target: ~1,570)")
        elif words < 1000:
            add("INFO", "CROSS-DOC",
                f"Estimated narrative word count: ~{words} (may be under-developed)")


# ===========================================================================
# CHECK 6: Logic validation
# ===========================================================================

def check_logic():
    # Verify combinatorics
    computed = sum(comb(N_ELEMENTS, k) for k in range(K_MIN, K_MAX + 1))
    if computed != EXPECTED_SUBSYSTEMS:
        add("CRITICAL", "LOGIC",
            f"Internal error: Σ C({N_ELEMENTS},{K_MIN}..{K_MAX}) = {computed}, expected {EXPECTED_SUBSYSTEMS}")

    # Individual binomial coefficients
    expected_by_k = {k: comb(N_ELEMENTS, k) for k in range(K_MIN, K_MAX + 1)}
    for k, exp in expected_by_k.items():
        plan_vals = re.findall(rf"C\(15,{k}\)\s*=\s*(\d[\d,]*)", plan)
        for pv in plan_vals:
            if int(pv.replace(",", "")) != exp:
                add("CRITICAL", "LOGIC",
                    f"Population plan: C(15,{k}) = {pv}, should be {exp:,}")

    # k=2 → ternary check (NOT binary!)
    # Since Al is always the base, k=2 means 2 alloying elements + Al = ternary
    ternary_lines = line_numbers_of(tex, r"ternary", re.IGNORECASE)
    binary_lines = line_numbers_of(tex, r"binary", re.IGNORECASE)
    # If kmin=2 and text says "binary" for k=2 systems, that's wrong
    for bl in binary_lines:
        line = tex.splitlines()[bl - 1]
        if "k=2" in line or "kmin" in line.lower():
            add("WARNING", "LOGIC",
                f"Line {bl}: 'binary' used for k=2 — should be 'ternary' (Al + 2 elements = 3 components)")

    # Throughput max
    throughput_max = 2 * 6 * 39  # ~468
    if "468" not in all_text and str(throughput_max) not in all_text:
        add("INFO", "LOGIC",
            "Throughput max (~468) not found in documents")

    # Budget arithmetic: BYU + partners = total
    budget_sum_k = (BUDGET_BYU + BUDGET_VALIMET + BUDGET_AMAZEMET + BUDGET_THERMOCALC) // 1000
    if budget_sum_k != BUDGET_TOTAL // 1000:
        add("CRITICAL", "LOGIC",
            f"Budget items sum to ${budget_sum_k}K, expected ${BUDGET_TOTAL // 1000}K")


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 70)
    print("FLAIME Proposal Consistency Checker")
    print(f"  Elements: {N_ELEMENTS} | k: {K_MIN}..{K_MAX} | Sub-systems: {EXPECTED_SUBSYSTEMS:,}")
    print(f"  Budget: ${BUDGET_TOTAL:,} | Personnel: {EXPECTED_MS} MS + {EXPECTED_UG} UG")
    print(f"  Compositions: {COMPOSITION_RANGE[0]}–{COMPOSITION_RANGE[1]} | MB: ≥{MINERAL_BURDEN_REDUCTION}%")
    print("=" * 70)
    print()

    check_numerical()
    check_terminology()
    check_references()
    check_foa_compliance()
    check_cross_doc()
    check_logic()

    severity_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    findings.sort(key=lambda f: severity_order.get(f.severity, 3))

    if not findings:
        print("✅ No inconsistencies found!")
        return 0

    critical = [f for f in findings if f.severity == "CRITICAL"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos = [f for f in findings if f.severity == "INFO"]

    print(f"Found {len(findings)} issues: "
          f"{len(critical)} critical, {len(warnings)} warnings, {len(infos)} info\n")

    if critical:
        print("## CRITICAL (must fix before submission)")
        print("-" * 50)
        for i, f in enumerate(critical, 1):
            print(f"  {i}. [{f.category}] {f.message}")
            for d in f.details:
                print(f"     → {d}")
        print()

    if warnings:
        print("## WARNING (should review)")
        print("-" * 50)
        for i, f in enumerate(warnings, 1):
            print(f"  {i}. [{f.category}] {f.message}")
            for d in f.details:
                print(f"     → {d}")
        print()

    if infos:
        print("## INFO (minor / stylistic)")
        print("-" * 50)
        for i, f in enumerate(infos, 1):
            print(f"  {i}. [{f.category}] {f.message}")
            for d in f.details:
                print(f"     → {d}")
        print()

    return 1 if critical else 0


if __name__ == "__main__":
    sys.exit(main())
