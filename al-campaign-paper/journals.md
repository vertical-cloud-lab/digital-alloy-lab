# Target journals

*Compiled 2026-11-27. Read the live guide for authors in a browser before submitting: from this runner, ScienceDirect
returned a captcha, and Taylor & Francis, RSC and tms.org returned 403s. So the format rules below come from
archived copies of the official guides (capture month in brackets), Elsevier's Journal Finder and APC list,
Springer's instruction PDFs and TMS's call PDFs. † marks an item seen only in a search engine's excerpt of an official
page.*

**The Feb 28 date isn't a journal deadline.** No special issue in the shortlisted journals has a deadline between
Jan 15 and Apr 30, 2027 on printed Al alloys or alloy design (details [below](#calls-with-deadlines-near-feb-28)). The
date is the lab's own, so the journal can be chosen on fit.

## Recommendation

| If the paper is | First choice | Why | Then |
|---|---|---|---|
| **Version A** (a new alloy, one striking result) | ***Additive Manufacturing Letters*** | Specific to AM, and its Short Communication allows about 5,000 words, which fits the current draft. Decisions are fast: either conditional acceptance with one minor revision, or rejection, targeted within 4 weeks. Open access at $2,350 | *Materials Research Letters* (3,000 words, 5 figures; the editor screens against 6 criteria and usually wants more than one, so "beats AlSi10Mg" alone won't pass), then *Scripta Materialia* (2,500 words, 5 figures; its current scope asks for mechanistic processing-structure-property links) |
| **Version B** (a benchmarked screen of about 20 compositions) | ***Additive Manufacturing*** | Highest impact factor of the shortlist (11.3), and a Research Paper allows 5,000-13,000 words. Its guide says only "substantial advancements" are considered | *Materials & Design*, whose scope names AI and data science (full OA, $3,750, highlights and graphical abstract required), then *J. Alloys and Compounds* |

*Additive Manufacturing* strongly discourages posting a preprint before submission (2024 guide), and the other
journals allow it. So don't post one until the journal is chosen. The run asked for no preprint anyway.

## Formats and limits

| Journal | Article type that fits: limit | Abstract | Required extras | LaTeX |
|---|---|---|---|---|
| *Scripta Materialia* | Regular article: ≤ 2,500 words excluding figures, tables, captions, abstract, title, authors, references and acknowledgements; ≤ 5 figures; 4-5 printed pages; no subsection headings [2024-02] | 150 words | Graphical abstract mandatory; ≤ 5 keywords, 4 from the journal's list; ≥ 4 suggested referees | Yes |
| *Materials Research Letters* | Original Report: ≤ 3,000 words *including* abstract, tables, captions and notes (references not listed); figures "should not normally exceed 5" [2024-10] | 100 words | Impact statement ≤ 30 words; graphical abstract mandatory; 3-5 keywords; cover letter must say which of 6 prescreen criteria the paper meets | T&F template, Word or LaTeX (PDF plus source) |
| *Additive Manufacturing Letters* | Short Communication: "preferred length… 5000 words without counting references or the abstract" (Journal Finder, live) | not stated | ISO/ASTM 52900 terms in title and abstract (PBF-LB/M, not "LPBF"); ≤ 20 % self-citations; ≥ 25 % of references from the last 3 years; machine-learning papers follow the journal's ML guidelines [2022-07]. Highlights and graphical abstract optional; ≤ 6 keywords | Yes (`elsarticle`, as here) |
| *Additive Manufacturing* | Research Paper: 5,000-13,000 words for the whole manuscript including references and captions [2024-01] | not stated | ISO/ASTM 52900 terms; ML guidelines; highlights and graphical abstract optional; ≤ 6 keywords. If rejected elsewhere, include that correspondence and reviews in the cover letter | Yes |
| *Materials & Design* | Research Paper: no limit stated; no short communications [2024-06] | not stated | Highlights (3-5, ≤ 85 characters each) and graphical abstract required; 1-7 keywords; cover letter should name the journal's priority area | Yes |
| *J. Alloys and Compounds* | Full Length Article: no limit stated [2024-02] | not stated | Highlights mandatory; prime novelty statement ≤ 150 words; ≥ 3 referees, none from the authors' country; purely computational (CALPHAD) work without enough experiment is out of scope | Yes |
| *Materials Science and Engineering: A* | Short Communication: about 2,000 words, abstract ≤ 50 words, ≤ 6 figures, originality statement [2023-12] | ≤ 50 words | Corrosion- or wear-led papers discouraged unless they address mechanical behavior | Yes |
| *Integrating Materials and Manufacturing Innovation* | Technical Article ≤ 8,000 words; Brief Communication ≤ 3,000 [Sep 2026] | 150-250 words | Data availability statement mandatory (returned before review without one); deposit data and code | Word preferred, LaTeX accepted |
| *JOM* | Original Paper ≤ 9,000 words including references; ≤ 12 figures and tables [Aug 2025] | 150-200 words | Three suggested reviewers required; ≤ 2 papers per author per topic | Word; LaTeX with a PDF |

## Cost, policies and speed

| Journal | Open access; APC (USD) | Data policy | Preprint before submission | Speed (Journal Finder: days to first decision) | Impact factor |
|---|---|---|---|---|---|
| *Scripta Materialia* | Hybrid; 3,220 | Sharing and a data statement encouraged | Allowed | 5 | 5.9 |
| *Materials Research Letters* | Full OA; 1,680 (Oct 2024 figure) | Sharing encouraged | Allowed† | 6 (33 to the first decision after review†) | 7.5† |
| *Additive Manufacturing Letters* | Full OA; 2,350 | Sharing encouraged | Allowed in the 2022 guide | 13; 32 % accepted | 5.2 |
| *Additive Manufacturing* | Hybrid; 4,490 | Data statement required if data aren't shared | **Strongly discouraged** (2024) | 2 | 11.3 |
| *Materials & Design* | Full OA; 3,750 | Deposit and link encouraged | Allowed | 7; 39 % accepted | 8.2 |
| *J. Alloys and Compounds* | Hybrid; 3,470 | Data statement required if data aren't available | Allowed | 8; 28 % accepted | 6.7 |
| *MSE A* | Hybrid; 3,610 | as JALCOM | Allowed | 6; 19 % accepted | 7.9 |
| *IMMI* | Hybrid; 3,890 | Statement mandatory; deposit data and code | Allowed (Springer) | not stated | 3.0 |
| *JOM* | Hybrid; 3,990 | Strongly encouraged | Allowed (Springer) | not stated | 2.3 |

Submission-to-acceptance times are on Elsevier's Journal Insights pages, which were blocked. Journal Finder doesn't
date its impact factors.

## What the draft needs for the first choices

- **Either Elsevier journal:** the draft already uses `elsarticle` with numbered references, and it already has data
  availability, code availability, CRediT, competing-interest and generative-AI statements (the AI statement uses
  Elsevier's template wording). Still to do: highlights (drafts are in a note on page 1) and a graphical abstract
  (Fig. 1b with the chosen alloy).
- ***Additive Manufacturing Letters*:**
  - Write "PBF-LB/M" in the title and abstract.
  - Recent references: 19 of the 65 entries (29 %) are from 2024-2026, against the 25 % the guide asks for, but only
    12 of 65 (18 %) if the seven vendor datasheets don't count. As results come in, cite recent work rather than
    older general references.
  - Self-citations: 1 of 65.
  - The current draft has about 3,200 words of body text, notes excluded, against about 5,000 allowed, so there is
    room for results.
- ***Additive Manufacturing*:** 5,000-13,000 words in all. Version B will land near the bottom of that range. Post no
  preprint before submitting.
- ***Materials Research Letters* or *Scripta*:** move most of §2 to the SI. Cut to 3,000 words (MRL, *including*
  abstract and captions) or 2,500 (*Scripta*), with 5 figures. *Scripta* allows no subsection headings.

## Calls with deadlines near Feb 28

None in the six Elsevier journals, MRL, *Virtual and Physical Prototyping* or *Digital Discovery* falls between
Jan 15 and Apr 30, 2027. Elsewhere:
- **JOM:** TMS topic "Experiment and Modeling Synergies to Solve Multiphysics Problems" (due Mar 1, 2027); "Agentic
  AI for Materials Design and Discovery" (due May 1, 2027).
- **IMMI:** "AI-Enabled Materials Processing" (due May 31, 2027).
- **MDPI *Metals* and *Materials*:** several AM-alloy issues fall due Feb 20 to Apr 20, 2027 (for example, *Metals*
  "Laser Powder Bed Fusion for High-Performance Metallic Materials", due Feb 20; *Materials* "Design,
  Characterization and Optimization of AM High-Performance Alloys", due Mar 20).

## Sources

Elsevier Journal Finder (one search per journal), Elsevier's APC list (5 Oct 2026), and archived official guides:
- [*Scripta* 2024-02](https://web.archive.org/web/20240226223155/https://www.sciencedirect.com/journal/scripta-materialia/publish/guide-for-authors)
- [*AM Letters* 2022-07](https://web.archive.org/web/20220705002750/https://www.elsevier.com/journals/additive-manufacturing-letters/2772-3690/guide-for-authors)
- [*Additive Manufacturing* 2024-01](https://web.archive.org/web/20240109212715/https://www.sciencedirect.com/journal/additive-manufacturing/publish/guide-for-authors)
- [*Materials & Design* 2024-06](https://web.archive.org/web/20240629120627/https://www.sciencedirect.com/journal/materials-and-design/publish/guide-for-authors)
- [*JALCOM* 2024-02](https://web.archive.org/web/20240210133726/https://www.sciencedirect.com/journal/journal-of-alloys-and-compounds/publish/guide-for-authors)
- [*MSE A* 2023-12](https://web.archive.org/web/20231228170946/https://www.sciencedirect.com/journal/materials-science-and-engineering-a/publish/guide-for-authors)
- [*MRL* 2024-10](https://web.archive.org/web/20241008182546/https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=tmrl20)

Springer and TMS:
- [IMMI instructions (Sep 2026)](https://link.springer.com/journal/40192/submission-guidelines)
- [JOM instructions (Aug 2025)](https://link.springer.com/journal/11837/submission-guidelines)
- TMS topic PDFs: `https://www.tms.org/portal/downloads/publications/jom/editorialCalendar/{7707,7720,7741,7711}.pdf`
