# NSF mock-reviewer playbook for LLMs

A structured prompt + checklist that turns the extracted corpus in this
directory into an LLM-driven mock reviewer for NSF (and NSF-style) proposals.
Designed so that pasting the system prompt below + the relevant context files
into any large-context LLM produces feedback that is **specific, evidence-cited,
and actionable** rather than vague.

> "NSF-style" because the same corpus is also useful for DOE, DARPA, USDA NIFA,
> and similar federal solicitations — adjust criterion names where needed.

---

## 1. How to use this playbook

### 1.1 Decide the review mode

| Mode | When to use | Approx. context budget |
| --- | --- | --- |
| **Spot-check** (one section, one criterion) | Iterating on a specific paragraph, e.g. "is my Project Summary IM/BI-compliant?" | 5–15k tokens |
| **Section review** (one chapter / Project Description / Budget) | After a draft of one component is stable | 20–40k tokens |
| **Full-proposal mock review** (all sections, all 5 NSF criteria) | Pre-submission rehearsal | 60–120k tokens (use a 200k+ window) |
| **Compliance audit only** (PAPPG checklist, no scientific opinion) | Final pre-submission sweep | 30–60k tokens |

### 1.2 Load the right context files

Use `_manifest.json` to budget tokens. The minimum-viable context for each mode:

| Mode | Required context files |
| --- | --- |
| Spot-check Project Summary | `pappg-24-1/02-chapter-II.md`, `grant-writers-seminars-workshops/nsf/OverviewTemplateMasterPlanNSF2021.pdf.md` (or `Pre-SubmissionReviewNSF2021.pdf.md`), `grant-writers-seminars-workshops/any-agency/DevelopmentofAbstract.md`, `grant-writers-seminars-workshops/any-agency/DevelopmentofOverviewSection.md` |
| Spot-check Project Description | `pappg-24-1/02-chapter-II.md`, `grant-writers-seminars-workshops/any-agency/WritingtheBodyofYourProposal.md`, GWSW NIH `Rigor-of-Research-Design.md` and `NIH25-Significance-Innovation-Subsections.md` |
| Spot-check Budget Justification | `pappg-24-1/02-chapter-II.md` (budget sections), `pappg-24-1/09-chapter-IX.md` (Allowability of Costs), `grant-writers-seminars-workshops/nsf/NSF-Budget-Justification.md` |
| Compliance audit | All `pappg-24-1/*.md` chapters that the proposal touches (always include `02-chapter-II.md`) + `grant-writers-seminars-workshops/nsf/Pre-SubmissionReviewNSF2021.md` |
| Full mock review | All of the above + the GSS docs (`gold-standard-science-implementation-plan-2025.md`, `ostp-gss-guidance-june-2025.md`) for any rigor / reproducibility / data-management angle |

### 1.3 Provide the proposal draft

Append the LaTeX/markdown/PDF-extracted text of the draft inside an explicit
`<draft>` block so the LLM can quote it back with line numbers.

---

## 2. System prompt template

Copy from here to the next horizontal rule.

```
You are a senior NSF panel reviewer who has served on multiple panels and
chaired several. Your job is to provide a constructive mock review of the
draft proposal in <draft>...</draft>, citing the official NSF policy
documents and the Grant Writers' Seminars & Workshops (GWSW) workbook
chapters in <corpus>...</corpus> as the sole authority for any claim of
"required" / "non-compliant" / "best practice".

Review against the FIVE NSF Merit Review Criteria from PAPPG 24-1
Chapter III (Intellectual Merit, Broader Impacts) plus the Additional Review
Criteria as applicable, and ALSO against the PAPPG Chapter II proposal-
preparation requirements.

OUTPUT FORMAT — strict markdown, in this order:

### Summary judgment (≤120 words)
A panel-style verdict: Competitive / Borderline / Not yet competitive,
plus the 2-3 most consequential issues to fix.

### Compliance findings (PAPPG Chapter II)
A bulleted list. For each finding:
- **[severity: blocker | major | minor]** what is wrong
- **PAPPG citation:** chapter+section (e.g., "PAPPG II.D.2.b")
- **Evidence in draft:** quote 1–2 sentences with line/page reference
- **Fix:** one concrete sentence the PI can act on

If a section is missing entirely, list it as a `blocker`.
Always check (at minimum):
- Project Summary present, ≤1 page, three labeled sections
  (Overview, Intellectual Merit, Broader Impacts)
- Project Description ≤15 pages, includes Results from Prior NSF Support
  if applicable, includes a separately-headed Broader Impacts section
- References Cited: complete bibliographic info, no annotations
- Biographical Sketches: SciENcv-generated, format-compliant
- Current & Pending (Other) Support: SciENcv-generated, all current/pending
- Budget Justification: ≤5 pages, every line item explained
- Facilities, Equipment & Other Resources: factual, no quantifiable info
- Data Management & Sharing Plan: ≤2 pages, addresses generated data types
- Mentoring Plan (if postdocs/grad students supported): ≤1 page
- Format: 11pt+ font, 1" margins, single-column, page numbers

### Intellectual Merit review (NSF criterion 1)
~250 words. Use the GWSW NIH "Significance & Innovation" framing
(`NIH25-Significance-Innovation-Subsections.md`) and the GWSW NSF
"Overview / Master Plan" framing (`OverviewTemplateMasterPlanNSF2021.md`).
Address each PAPPG III.A.1 sub-question:
1. Potential to advance knowledge?
2. Creative, original, transformative?
3. Plan well-reasoned, well-organized, sound rationale?
4. PI(s) qualified?
5. Resources adequate?

For each, give a 1-sentence verdict + a 1-sentence quoted-evidence pointer.
End with the 2 strongest weaknesses a panelist would raise.

### Broader Impacts review (NSF criterion 2)
~200 words. Address the same PAPPG III.A.1 sub-questions in the BI frame.
Distinguish "specific, measurable, with named partners and metrics" from
"generic / aspirational language". Generic BI language is the single most
common reason for downgrade — flag it explicitly.

### Additional review criteria (PAPPG III.A.2 / III.E as applicable)
Cover the ones that apply (data management plan adequacy, mentoring plan
adequacy, postdoc support, RCR, conflicts, etc.).

### Reviewer-experience issues (GWSW "reviewer-centric writing")
~150 words. Concretely: signposting, summary-then-detail, scannability,
where the reviewer's eye lands on each page, jargon load. Cite specific
GWSW chapters from the corpus.

### Top-3 prioritized revisions
A numbered list of EXACTLY 3 items. Each: (a) what to change, (b) where
in the draft, (c) which corpus document supports it, (d) estimated
revision effort (S/M/L).

### Open questions for the PI (≤5)
Things the reviewer cannot determine from the draft and would ask in a
panel discussion or in a "respond to reviewers" round.

RULES:
- Every "required", "must", "should", or compliance claim MUST cite a
  specific corpus file (PAPPG chapter+section preferred, GWSW chapter as
  secondary). If you cannot find a citation in the corpus, soften to
  "I would expect..." or "common practice is...".
- No filler. No restatement of the proposal. No praise without a
  matched concern.
- If the draft is missing entirely or trivially short, say so in
  Summary judgment and stop — do not hallucinate content.
- Do not invent PAPPG section numbers; if unsure, write "PAPPG ch. II
  (section TBD)" rather than fabricating "PAPPG II.D.X.y".
```

End of system prompt.

---

## 3. Criterion-by-criterion checklist (for human verification of LLM output)

Use this to sanity-check what the LLM produced. Each item maps to corpus
files; if the LLM's review touches the item, verify it cited the right
source.

### 3.1 PAPPG Chapter II compliance — the non-negotiables

| # | Item | Corpus anchor |
| --- | --- | --- |
| C1 | Single-column, 11pt+ font, 1" margins, page numbers | `pappg-24-1/02-chapter-II.md` (Format) |
| C2 | Project Summary: 1 page, three labeled sections (Overview / IM / BI) | `pappg-24-1/02-chapter-II.md` (II.D.2.b); GWSW NSF `OverviewTemplateMasterPlanNSF2021.md` |
| C3 | Project Description: ≤15 p, includes BI as a labeled section | `pappg-24-1/02-chapter-II.md` (II.D.2.d) |
| C4 | Results from Prior NSF Support: 5-yr lookback, all PIs/co-PIs | `pappg-24-1/02-chapter-II.md` (II.D.2.d.iii) |
| C5 | References Cited: complete bibliographic info, no annotations | `pappg-24-1/02-chapter-II.md` (II.D.2.e) |
| C6 | Biosketches: SciENcv format, ≤3 pages each | `pappg-24-1/02-chapter-II.md` (II.D.2.h.i) |
| C7 | Current & Pending: SciENcv, every PI/sr-personnel | `pappg-24-1/02-chapter-II.md` (II.D.2.h.ii) |
| C8 | Budget Justification ≤5 p, every cost rationalized | `pappg-24-1/02-chapter-II.md` budget sections; GWSW NSF `NSF-Budget-Justification.md`; PAPPG ch. IX (Allowability) |
| C9 | Facilities, Equipment & Other Resources: no quantifiable info | `pappg-24-1/02-chapter-II.md` (II.D.2.g) |
| C10 | Data Management & Sharing Plan ≤2 p | `pappg-24-1/02-chapter-II.md` (II.D.2.i.ii); GSS docs |
| C11 | Mentoring Plan ≤1 p (if postdocs/grad students supported) | `pappg-24-1/02-chapter-II.md` (II.D.2.i.i) |
| C12 | Disclosures: senior personnel, foreign affiliations | `pappg-24-1/02-chapter-II.md` (II.B / II.D.1) |

### 3.2 Intellectual Merit — five PAPPG III.A.1 questions

| # | Question | Corpus anchor |
| --- | --- | --- |
| IM1 | Potential to advance knowledge? | `pappg-24-1/03-chapter-III.md`; GWSW NIH `NIH25-Significance-Innovation-Subsections.md` |
| IM2 | Creative, original, transformative? | same |
| IM3 | Well-reasoned, well-organized, sound rationale? | `pappg-24-1/03-chapter-III.md`; GWSW NIH `Rigor-of-Research-Design.md` |
| IM4 | PI(s) qualified to execute? | `pappg-24-1/03-chapter-III.md`; GWSW NIH `Senior-Key-Personnel.md` |
| IM5 | Adequate resources? | `pappg-24-1/03-chapter-III.md`; GWSW USDA `USDAFacilitiesandOtherResources2021.md` |

### 3.3 Broader Impacts — five PAPPG III.A.1 questions in BI frame

Same five questions, evaluated through the lens of *outcomes for society*
(K-12 education, broadening participation, public engagement,
workforce development, infrastructure, etc.). Corpus anchor:
`pappg-24-1/03-chapter-III.md`. The *single most common* reviewer downgrade
is generic BI language ("we will train students, publish papers, give
talks") with no named partners, no metrics, no plan. Reviewer should flag
any BI section that does not contain at least one of: named partner
organization, quantified target (N students, N events), assessment plan.

### 3.4 Reviewer-experience checklist (GWSW)

| # | Item | Corpus anchor |
| --- | --- | --- |
| R1 | Specific Aims / Overview page exists and is self-contained | GWSW NSF `OverviewTemplateMasterPlanNSF2021.md` |
| R2 | Reviewer can find IM and BI verdicts in <30 s of skimming | GWSW NSF `Pre-SubmissionReviewNSF2021.md` |
| R3 | Hypothesis-driven framing (problem → gap → approach → expected outcome) | GWSW any-agency `WritingtheBodyofYourProposal.md` |
| R4 | Section/sub-section signposts; figures with informative captions | GWSW any-agency `BeforeYouBegintoWrite.md` |
| R5 | "Sentence stems" / topic sentences carry the argument standalone | GWSW USDA `USDASentenceStemsforOverview2021.md` (transferable) |
| R6 | Pre-submission review by ≥1 colleague outside the immediate field | GWSW NSF `Pre-SubmissionReviewNSF2021.md` |

### 3.5 Gold Standard Science (Supplements 26-200 / 26-202)

For any proposal funded on/after the supplement effective dates, the LLM
should additionally check:

| # | Item | Corpus anchor |
| --- | --- | --- |
| G1 | Methods reproducibility: code + data deposit plan | `gold-standard-science-implementation-plan-2025.md`, `ostp-gss-guidance-june-2025.md` |
| G2 | Pre-registration / preprint plan, where applicable | same |
| G3 | Error-correction commitment (corrigenda, retractions) | same |
| G4 | Conflict-of-interest and reviewer-integrity disclosures | `pappg-24-1/02-chapter-II.md` (II.B) |

---

## 4. Worked example — minimal invocation

Given a draft `proposal.md`:

```
SYSTEM:
<paste system prompt from §2>

USER:
<corpus>
[contents of nsf-resources-text/pappg-24-1/02-chapter-II.md]
[contents of nsf-resources-text/pappg-24-1/03-chapter-III.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/nsf/Pre-SubmissionReviewNSF2021.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/nsf/OverviewTemplateMasterPlanNSF2021.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/nsf/NSF-Budget-Justification.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/any-agency/DevelopmentofOverviewSection.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/nih/NIH25-Significance-Innovation-Subsections.md]
[contents of nsf-resources-text/grant-writers-seminars-workshops/nih/Rigor-of-Research-Design.md]
</corpus>

<draft>
[contents of proposal.md]
</draft>
```

The total context here is ~85k tokens (corpus) + the draft, well within a
200k-context model. For tighter budgets, drop the GWSW NIH chapters first
(they are the "transferable" set), then GWSW any-agency, then
`pappg-24-1/03-chapter-III.md` (only if you also drop the IM/BI sections of
the system prompt).

---

## 5. Notes & caveats

* The text extractions are best-effort: pymupdf preserves reading order well
  but headers/footers/footnotes can interleave. For verbatim quotes, always
  reconcile against the source PDF in `../nsf-resources/`.
* PAPPG section numbering can drift between editions; the playbook above is
  pinned to PAPPG 24-1 + supplements 26-200 / 26-202.
* This playbook is **not** a substitute for a pre-submission review by a
  human colleague (see GWSW `Pre-SubmissionReviewNSF2021.md`). Treat LLM
  output as a triage layer, not a verdict.
* A complementary repo skill, `mock-reviewer`, exists for the FLAIME
  Genesis Mission DOE proposal and uses an analogous three-persona
  approach. The structure of this playbook is intentionally compatible.
