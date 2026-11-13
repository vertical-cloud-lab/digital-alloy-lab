# Tier 1 Outreach Drafts — README

Three email drafts for **today** covering the four Tier 1 contacts on
`plan.md`. All drafts bundle the Letter of Commitment with the relevant
technical ask into a single email so PI only has to send three messages.

| # | File | Recipients | Bundled content |
|---|---|---|---|
| 01 | `01-thermocalc.md` | Thermo-Calc's account manager (to), a Thermo-Calc specialist (cc) | AM Module preliminary sim ask (4 comps) **+** TC Letter of Commitment |
| 02 | `02-valimet.md`               | Valimet's CTO (to), Valimet's technical manager (cc) | Valimet scope confirmation + Letter of Commitment + coordinated app |
| 03 | `03-amazemet.md`              | Amazemet's CEO (to), Amazemet's application engineer (cc) | AMAZEMET scope confirmation + Letter of Commitment + coordinated app |
| 04 | `04-tier2-collaboration-letters.md` | Spear, Meta, Jensen, Sparks (LLM-BO rewrite), Clare (NEW), 3D Powder Tech | Six 2-sentence Letters of Collaboration (FOA-compliant) |
| 05 | `05-distributed-manufacturing-network.md` | Top-75 metal-AM contacts (PR #57) | Master 2-sentence letter template for multi-site validation network, populates `[TBD_N_UNIV/LAB/COMPANY]` in tex:686 |
| 06 | `06-additional-letters-identified.md` | Ames Lab, Fehrmann, Stiles, Hattrick-Simpers, Brown | Newly-identified collaborators from population plan; PI triage required |
| 07 | `07-vcl-student-commitment.md` | VCL student roster | Leave-semester commitment collection email |
| 08 | `08-byu-spo-package.md`       | BYU SPO | Institutional Letter of Commitment request package — **TRUE LONG POLE (5-10 biz days)** |

## PI fill-in items across all three drafts

**Compositions (for #01) — 4 total:**
- [ ] Al-Mn-Cr-Zr anchor wt% (TBD)
- [ ] Al-Zr anchor wt% (TBD)
- [x] AlSi10Mg commercial reference (Si 10.0, Mg 0.325, Al bal — MSE midpoint)
- [x] Blend chemistry Al 75.56 / Si 24.30 / Mg 0.14 wt%
      (per byu-vcl/thermo-calc-100g-mixture-composition.md)

**Email addresses:**
- [ ] Thermo-Calc contacts (thermocalc.com)
- [ ] Valimet contacts (valimet.com)
- [ ] Amazemet contacts (amazemet.com)

**Scope parameters:**
- [ ] Valimet: N_COMPS, LOT_KG
- [ ] AMAZEMET: N_CRUCIBLES per composition

**Deadlines:** fill each `[DEADLINE]` placeholder (≥3 business days before FOA submission for signed PDFs; AM Module sim turnaround depends on Thermo-Calc's capacity).

## Attachments to prepare

1. Narrative §Methods excerpt (1-2 pages) — context for all three partners.
2. Commitment letter `.docx` for each partner, converted from the
   pre-drafted text in `flaime-genesis-proposal.tex`:
   - TC: lines 1884–1912
   - Valimet: adapted from generic template, lines 1798–1823
   - AMAZEMET: adapted from generic template, lines 1798–1823
3. Pointer to FOA application instructions for Valimet and AMAZEMET
   coordinated applications.

## Notes

- All three emails use the FOA-correct "coordinated multi-application"
  framing (not subawards). Confirmed per PI directive 2026-04-14 in memory.
- TC email intentionally bundles sims + letter; if Thermo-Calc's account manager prefers to
  split, the letter half can go to the Thermo-Calc signatory directly.
- These drafts are **not** committed to the repo — they live in
  session-state `files/` per project convention.
