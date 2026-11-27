# *Advanced Materials*: format, limits and the collection

*Checked 2026-11-27. Wiley's live author-guidelines page sits behind a Cloudflare check that couldn't be passed
from the runner (the box wasn't clicked), so the rules below come from Wiley's own Advanced Materials guideline
page as archived on 2024-12-10, Wiley's June 2025 manuscript checklist and Word template for the Advanced journals,
and live Wiley-wide policy pages. **Re-read the live page before submitting**; the 2025 template changed the
reference style, so other details may have moved too.*

Sources:
- **[A]** [Advanced Materials author guidelines, archived 2024-12-10](https://web.archive.org/web/20241210154241/https://onlinelibrary.wiley.com/page/journal/15214095/homepage/author-guidelines)
- **[B]** Wiley's Advanced journals manuscript checklist and Word template, June 2025: `Manuscript-Preparation-Checklist-1749710740523.pdf` and `Article-template-1749710971070.docx` on advanced.onlinelibrary.wiley.com (archived copies)
- **[C]** Wiley-wide pages:
  - [data sharing policy](https://authors.wiley.com/author-resources/Journal-Authors/open-access/data-sharing-citation/data-sharing-policy.html)
  - [preprints](https://authors.wiley.com/author-resources/Journal-Authors/open-access/preprints-policy.html)
  - [CRediT](https://authors.wiley.com/author-resources/Journal-Authors/open-access/credit.html)
  - [APC list](https://authors.wiley.com/asset/Wiley-Journal-APCs-OnlineOpen.xlsx), updated 2026-10-12
- **[S]** Secondary: [Manusights formatting notes](https://manusights.com/blog/advanced-materials-formatting-requirements), which say they read the live page on 2026-10-08

## The collection (decision D1)

**Not identified.** No public *Advanced Materials* call has a late-2027 or early-2028 deadline. The journal's special
issues and series are by invitation, and their deadlines aren't published:
- **Rising Stars** is a series of invited Research Articles "conceptualized and supervised by recognized early career
  researchers" ([archived page](https://web.archive.org/web/20241204072859/https://onlinelibrary.wiley.com/doi/toc/10.1002/(ISSN)1521-4095.Rising-Stars)).
  This would fit an invitation to the PI.
- **Topical special issues.** The closest precedent is "Advanced Materials for Additive Manufacturing", Vol. 36, Issue
  34 (Aug 2024; editorial doi:10.1002/adma.202410446).
- **Institution and anniversary issues**, e.g. NUS 120th, CityU 30th, CAS Institute of Chemistry 70th.
- **Hall of Fame** is invited reviews only, so not this article.

**The invitation letter or the guest editor is the authoritative source** for the collection's scope, article type,
length and deadline. Please add them to the README when you have them.

## Article type and length

| Item | Rule | Source | This draft |
|---|---|---|---|
| Type | Research Article (the other types are Review, Perspective and Comment; Communications no longer exist) | [A] | Research Article |
| Length | "a typical Research Article is around 3000–8000 words (in its entirety) including 3–8 display items… submitted manuscripts can be any length. However, the scientific contents should justify the length." | [A], [S] | Budget ~5,000 words main text + ~1,800 Experimental, 6 figures + 2 tables = 8 display items, at the upper end |
| Recent comparables | Main text 3.6–6.6k words (median ~4.5k), 4–9 figures (median 5), 39–101 references, all with SI; received to online in a median ~5.3 months. Eight Crossref-verified closed-loop/BO/AM-alloy articles from 2023–2026, including Taheri-Mousavi 2026 (6,580 + 2,340 words, 9 figures, 48 refs) | calibration below | |
| Structure | Introduction, main text, conclusion, and optionally an experimental or methods section; "The main article must stand on its own in the absence of the Supporting Information." | [A] | Yes |

## Required elements

| Element | Rule | Source | Status in this draft |
|---|---|---|---|
| Title | Descriptive with keywords, not "catchy but non-descriptive"; capitalize all words except coordinating conjunctions, articles and prepositions; no references or formulae | [A] | Title case applied; see outline §7 for a more descriptive option |
| Abstract | ≤ 200 words, **present tense, impersonal (avoid "we")**, no references | [A], [B] | 190-ish words, present tense, no "we" |
| Keywords | 3–7, not capitalized, plural, separated by commas | [A], [B] | 6 |
| Order | Title, Authors, Affiliations, Keywords, Abstract, Main text with figures in line, Conclusion, Experimental Section/Methods, Acknowledgements, Conflict of Interest, Data Availability Statement, References, Table of Contents. "Funding:" goes on the title page in the 2025 template | [A], [B] | Matches; add Funding line with D4 |
| Experimental Section | At the end, with a closing **"Statistical Analysis"** sub-section | [A] | Added (skeleton) |
| Figures | In line with captions; bitmaps ≥ 300 dpi (≥ 1000 px wide at single-column width); tables use three horizontal rules; axis labels as "Quantity [unit]" | [A] | Draft panels are vector PDF; axis labels to be switched to the bracket form when the final panels are made |
| Table of Contents | 50–60 words, third person, present tense, **different from the abstract**; image 55 × 50 mm or 110 × 20 mm, nothing else; no AI-generated images | [A], [B] | Text drafted (~55 words); image not made |
| References | At first submission, any consistent style. The 2025 style is Chicago-like: more than six authors become three + "et al.", full article titles and journal names, DOI optional. Typesetters reformat | [A], [B] | Wiley-VCH (Angewandte) numbered style, consistent; switch at revision |
| Supporting Information | Separate file with title and all authors; unedited; raw data and code can go separately | [A] | Separate `supporting-information.tex` |
| Data Availability Statement | Required under Wiley's "Expects Data" policy, even if no data are shared. Template wording: "The data that support the findings of this study are openly available in [repository] at http://doi.org/[doi], reference number [...]". Cite datasets as "[dataset] Authors; Year; Title; Repository; Version; Identifier". Scripts and other artefacts should be archived too | [A], [B], [C] | Drafted with this wording |
| **Machine-learning checklist** | "Please fill out this form as part of the submission process for all original research articles reporting machine learning studies" (code link, data sources, benchmarks). A Bayesian-optimization paper falls under this | [A] (checklist dated Nov 2022) | To fill at submission; the pre-registration covers most of it |
| Material compositions | "compositions of all materials central to the manuscript must be disclosed… includes commercial and proprietary products… Manuscripts reporting results using undisclosed material compositions may not be considered" | [A] | Every charge, powder and commercial benchmark needs its composition in the SI; any partner-supplied feedstock must be disclosable |
| Conflict of interest | Declare financial or commercial conflicts, or state that there are none | [A] | Placeholder; partners named in the Acknowledgements may need a statement |
| CRediT | Not required by [A] or [B]; only 2 of the 8 comparables give author contributions, as free text | [A], [C] | Optional; kept as a placeholder |
| Senior author | "the senior scientist… should hold at minimum a permanent staff position" | [A] | PI is faculty |
| Language and units | American English, SI units | [A] | Yes |
| Cover letter | Disclose manuscripts "submitted, soon to be submitted, or in press at other journals that have a bearing" | [A] | **The campaign paper (#277), the BOFN methods companion (#121, if it goes to MethodsX; decision M2) and the powder-doser papers must be disclosed**; the skeleton covers this |
| Reviewers | Single-anonymous, at least two reviewers, partly chosen from the authors' suggestions; in-house professional editors | [A] | Suggest 3–5 with no conflicts |
| Preprint | Allowed on a non-profit server (arXiv, ChemRxiv); only the original submitted version may be posted | [A], [C] | Don't post until submission (this run posted nothing) |
| Open access | Hybrid. APC USD 6,250 / GBP 4,720 / EUR 5,450 for OA (CC BY, CC BY-NC or CC BY-NC-ND) | [C] | Decide with funding (Manusights says $6,470, which conflicts) |
| Templates | Word and LaTeX templates exist, but "You do not need to reformat your manuscript for a new submission"; a single PDF from LaTeX is accepted. The LaTeX class (2020) is a bare skeleton with the old reference style; the 2025 Word template is current | [A], [B] | Plain LaTeX in the journal's section order; reformat at revision |
| Submission system | `wiley.atyponrex.com/journal/ADMA` redirects to Wiley's Research Exchange dashboard (login). Per [S], Editorial Manager is only for submissions started before Nov 25, 2025 | observed, [S] | — |

## Calibration set (Crossref-verified)

| Article | DOI | Main + methods words | Figs/tables | Refs |
|---|---|---|---|---|
| Taheri-Mousavi et al. 2026, ML-designed printable Al alloy, ultrasonic atomization, LPBF | 10.1002/adma.202509507 | 6,580 + 2,340 | 9/0 | 48 |
| Zeinali Galabi et al. 2026, closed-loop multi-objective BO of doped cathodes | 10.1002/adma.202519790 | 3,750 + 1,340 | 5/1 | 39 |
| Jeon et al. 2026, LLM closed-loop synthesis planning | 10.1002/adma.74502 | 4,540 + 340 | 5/3 | 57 |
| Serles et al. 2025, BO of carbon nanolattices | 10.1002/adma.202410651 | 4,040 + 2,010 | 4/0 | 50 |
| Nam et al. 2025, ML grayscale 3D printing | 10.1002/adma.202504075 | 6,420 + 1,180 | 7/0 | 57 |
| Henke et al. 2026, "Synthesizer" nanocrystal growth | 10.1002/adma.202509472 | 6,260 + 1,920 | 6/0 | 83 |
| Jang et al. 2026, active-learning high-entropy thermoelectrics | 10.1002/adma.202515054 | 4,550 (methods in SI) | 5/2 | 101 |
| Ji et al. 2025, eutectic high-entropy alloys by LPBF | 10.1002/adma.202500149 | 3,600 + 1,200 | 5/0 | 54 |
