# TMS 2027 Abstract — Ronnie's Working Draft (compositional & microstructural analysis of AM powders and prints)

> Companion to #98 (making the powder) and #100 (printing the part); this one covers **measuring** what was made.
> The symposium-selection + submission-version write-up lives alongside this file in
> `tms-2027-compositional-analysis-abstract.md`. This file tracks **Ronnie's own draft and revisions** (inlaid
> here from issue #102) so we can refine it in the PR.
>
> **Current status (2026-07-13):** Ronnie is aligning the abstract with **AI/ML/Data Informatics for
> Materials Discovery** (Flyer **022**) after learning Carl is submitting to AI-ICME (Flyer 024) — putting
> Ronnie in 022 (where @sgbaird holds an invited talk) de-conflicts the two BYU abstracts and gives the group
> two rooms instead of one. See the [symposium note](#symposium-decision) below. **v5 is the latest and the
> current submission candidate** — @sgbaird's manual line-edit of v4, now with a platform name (**CALIBER**)
> and a title. v4/v3 are earlier versions kept for reference (v3 is the AI-ICME fallback framing).

---

## v5 — @sgbaird manual edit + platform name, **current submission candidate** (147 words)

*This is the version to submit (Flyer 022, oral). It is @sgbaird's own line edit of v4 — tightens the
prose, keeps the concrete Mg/EBSD hook, adds "**uncertainty-aware**" to the feedback loop, and reframes the
recommender as a **model** ("the model recommends"). Word count 147 (`wc -w`), under the ~150-word cap.*

**Platform name:** the platform is named **CALIBER** (see the [naming note](#platform-name) below). Weaving
it into the first system sentence is a clean, one-word change that also fixes the slightly awkward "We
present on…":*

> Understanding a novel metal alloy's properties depends on accurate characterization, but leading
> analytical methods (SEM, EDS, EBSD, XRF) only return representative results when their acquisition
> parameters are set correctly. For example, standardless SEM-EDS can over-report trace Mg in AlSi10Mg
> several-fold, and EBSD indexing yield on laser powder bed fusion-derived Al-Si can vary from 40% to 80%
> once beam current and the phase model were corrected. Finding the right parameters takes trial-and-error.
> We present **CALIBER**, an AI-enabled platform that couples characterization literature through
> retrieval-augmented generation (RAG), a growing experimental dataset, and an uncertainty-aware feedback
> loop. Based on these, the model recommends high-fidelity acquisition settings for a given sample and
> analysis goal. Combining established characterization knowledge with data we collect in-house yields a
> literature- and physics-grounded method for choosing baseline parameters. This reduces the time needed to
> reach compositional and microstructural analysis of new alloys.

*@sgbaird's text **verbatim** (no name inserted, 147 words), in case you'd rather keep the platform name out
of the abstract body and reserve it for the title:*

> Understanding a novel metal alloy's properties depends on accurate characterization, but leading
> analytical methods (SEM, EDS, EBSD, XRF) only return representative results when their acquisition
> parameters are set correctly. For example, standardless SEM-EDS can over-report trace Mg in AlSi10Mg
> several-fold, and EBSD indexing yield on laser powder bed fusion-derived Al-Si can vary from 40% to 80%
> once beam current and the phase model were corrected. Finding the right parameters takes trial-and-error.
> We present on an AI-enabled platform to help address this that couples characterization literature through
> retrieval-augmented generation (RAG), a growing experimental dataset, and an uncertainty-aware feedback
> loop. Based on these, the model recommends high-fidelity acquisition settings for a given sample and
> analysis goal. Combining established characterization knowledge with data we collect in-house yields a
> literature- and physics-grounded method for choosing baseline parameters. This reduces the time needed to
> reach compositional and microstructural analysis of new alloys.

### Title

Proposed (leads with the platform name, then a plain-language description — good for the data-informatics
room, which rewards a clear system framing):

> **CALIBER: A Retrieval-Augmented, Uncertainty-Aware Platform for Selecting High-Fidelity Characterization
> Parameters for Novel Alloys**

Alternatives, by flavor:

| Title | Flavor |
| --- | --- |
| CALIBER: An AI Platform for Recommending High-Fidelity SEM/EDS/EBSD/XRF Acquisition Parameters for Novel Alloys | Names the modalities explicitly; concrete |
| Setting the Instrument Right: A Retrieval-Augmented, Uncertainty-Aware Platform (CALIBER) for High-Fidelity Alloy Characterization | Catchy lead phrase, name in parentheses |
| Literature- and Physics-Grounded Parameter Selection for High-Fidelity Alloy Characterization | Name-free; describes the contribution |

### Platform name

**CALIBER** — recommended. It reads as a real word (no forced acronym), and every association is
on-message for a *metrology* platform: "caliber" is literally a **measurement** term, "high-caliber" evokes
the **high-fidelity** results the system targets, and it sounds like **calibrate** — which is exactly what
the ICP-MS/MS-benchmarked loop does. Catchy without being cutesy or hype-y, so it should sit well even in a
hype-skeptical 022 room. If you want a loose backronym for a slide, *Characterization Acquisition via
Literature- and Interaction-simulation-Based Empirical Recommendation* works, but it's better left as a
plain name.

Shortlist of alternatives, if CALIBER doesn't land:

| Name | Why it works | Watch-out |
| --- | --- | --- |
| **SETPOINT** | A real process-control term (the target value a system drives toward) — apt for "set the acquisition right"; resonates with a data/control-savvy 022 audience | Slightly less warm than CALIBER |
| **SAGE** | Connotes a knowledgeable *advisor* — matches the decision-support framing; short | Common acronym, somewhat used |
| **COMPASS** | Evokes navigating parameter space to the right settings | Very common in software naming |
| **METIS** | Greek figure of wise counsel; near-homophone of "metrology" | Obscure; needs a gloss |

CALIBER is the strongest of the set — it's the only one whose plain-word meaning (*measurement precision*)
is the pitch itself.

---

## v4 — 022-tailored (AI/ML/Data Informatics), submission candidate (150 words)

*This is the version to submit if the target is Flyer 022. It applies the four review edits: (1) the
Bayesian-optimization powder-design sentence is **trimmed** (022 cares about the characterization *system*,
not the powder-design loop — so those words are spent on a hook instead of bridged), (2) a **concrete hook**
(trace-Mg over-report + EBSD indexing 40%→77%) makes the time-savings claim credible, (3) the fidelity claim
is **benchmarked against ICP-MS/MS**, and (4) the AI stays framed as **decision-support** ("recommend,"
"method for choosing"), not replacement. Ronnie's short-sentence voice is preserved; longest sentence 24
words.*

> Understanding a novel metal alloy's properties depends on accurate characterization. But the leading
> analytical methods — SEM, EDS, EBSD, and XRF — only return representative results when their acquisition
> parameters are set correctly. Setting them wrong is easy: standardless SEM-EDS can over-report trace Mg in
> AlSi10Mg several-fold, and EBSD indexing yield on LPBF Al–Si rose from ~40% to ~77% once beam current and
> the phase model were corrected. Finding the right parameters takes time and trial-and-error. We are
> building a system to fix this. It couples characterization documentation through retrieval-augmented
> generation (RAG), a growing provenance-tracked experimental dataset, and a feedback loop. Together these
> recommend high-fidelity acquisition settings for a given sample and analysis goal, benchmarked against
> ICP-MS/MS. Combining established characterization knowledge with data we collect in-house yields a
> literature- and physics-grounded method for choosing baseline parameters. This reduces the time needed to
> reach compositional and microstructural analysis of new alloys.

*Note the deliberate omission for 022: the "we create novel metal alloy powders through Bayesian
optimization" line from v3 is **gone**. It was the AI-ICME process→structure→property bridge; in the
data-informatics room it reads as a topic-switch, so those ~20 words now buy the concrete Mg/EBSD hook. If
the group reverts to **AI-ICME (024)**, use **v3** instead — there the BO line (plus Ronnie's approved
"High-fidelity characterization data then feeds this design loop") is an asset, not a distraction.*

---

## v3 — Ronnie's latest, AI-ICME-tailored (submission candidate)

**Ronnie's own version (verbatim, 141 words):**

> Understanding the properties of a novel metal alloy depends on accurate characterization, yet the leading
> analytical methods — SEM, EDS, EBSD, and XRF — only return representative results when their acquisition
> parameters are set correctly. Currently, finding those parameters takes substantial time and
> trial-and-error. We work to build a system that couples current characterization documentation with
> retrieval-augmented generation (RAG), a growing experimental dataset, and a feedback loop, resulting in
> high-fidelity acquisition setting recommendations for a given sample and analysis goal. By combining
> established characterization knowledge with the data we collect in-house, the system yields a literature-
> and physics-grounded method for choosing baseline parameters. Through a process involving Bayesian
> optimization, we create novel metal alloy powders in efforts to achieve desired material properties. This
> new system will greatly reduce the time needed to reach high-fidelity compositional and microstructural
> analysis of new alloys.

**Short-sentence variant (same content + voice, 140 words; per Ronnie's "keep sentences short" preference —
longest sentence 23 words):**

> Understanding a novel metal alloy's properties depends on accurate characterization. But the leading
> analytical methods — SEM, EDS, EBSD, and XRF — only return representative results when their acquisition
> parameters are set correctly. Finding those parameters today takes substantial time and trial-and-error.
> We are building a system to fix this. It couples current characterization documentation through
> retrieval-augmented generation (RAG), a growing experimental dataset, and a feedback loop. Together these
> produce high-fidelity acquisition-setting recommendations for a given sample and analysis goal. Combining
> established characterization knowledge with data we collect in-house yields a literature- and
> physics-grounded method for choosing baseline parameters. We create novel metal alloy powders through a
> process involving Bayesian optimization, targeting desired material properties. High-fidelity
> characterization data then feeds this design loop. The system greatly reduces the time needed to reach
> high-fidelity compositional and microstructural analysis of new alloys.

*The one added line Ronnie approved ("High-fidelity characterization data then feeds this design loop")
closes the process → structure → property loop, which is AI-ICME's #1 theme and what makes this the right
symposium rather than a generic characterization talk.*

---

## Symposium decision

**Update (2026-07-13):** Ronnie is now aligning to **AI/ML/Data Informatics for Materials Discovery**
(Flyer **022**) — on learning Carl is submitting to AI-ICME (024), moving Ronnie to 022 de-conflicts the two
BYU abstracts and leans on @sgbaird's invited-talk home-court there. The submission draft is now **v4**
(above). The AI-ICME framing below is kept as the fallback (v3).

Ronnie's earlier read: **AI-ICME** ("Artificial Intelligence Applications in Integrated Computational
Materials Engineering", TMS 2027 **Flyer 024**) — good fit, and it ties the characterization system to the
lab's atomizer + LPBF loop. The mock-review campaign in this PR agrees AI-ICME is a top-2 home (4/5).

Open call from @sgbaird: he is **split between AI-ICME (024) and AI/ML/Data Informatics for Materials
Discovery: Bridging Experiment, Theory, and Modeling (Flyer 022)**, where he holds an invited talk. Both
are strong; the whole-program ranking put **022 #1 (4/5)** and **024 #2 (4/5)**. Trade-off summary:

- **022 (AI/ML/Data Informatics):** best pure-scope fit — the agentic/RAG/FAIR *system* is the star; Baird's
  invited talk gives a home-court advantage. Downside: a hype-skeptical, data-native room that wants the
  architecture (not the Al results) to be the contribution.
- **024 (AI-ICME):** rewards the process → structure → property thread (atomizer → LPBF → characterize),
  which is exactly the lab story. Downside noted by @sgbaird — **Carl is also submitting to AI-ICME**, so
  two BYU-group abstracts in one room can split the odds of both getting oral slots.

See `tms-2027-compositional-analysis-abstract.md` → *Symposium selection* and
`edison-trajectories/tms-2027-all-symposia-top10/` for the full ranking and organizer personas.

---

## v1 — Ronnie's first draft (verbatim, for history)

Characterizing metals carries extreme importance when working to understand the material properties of
novel metal alloys. Prominent characterization methods such as SEM, EDS, EBSD, and XRF require the
correct parameters to give accurate, representative results. Finding the parameters needed to obtain
these useful results requires a substantial amount of time and trial and error. We work to create a
system that will incorporate either a large dataset or integration with AI, RAG, and current
characterization documentation with a feedback loop. This system will greatly shorten the time needed to
generate parameters to supply high-fidelity compositional and microstructural analysis. Combining the
existing characterization knowledge with our experimental collected data will lead to a literature- and
physics-based method for choosing baseline parameters in novel metal alloy characterization.

---

## The "characterization" wording question

`characterization` / `characterizing` is a **term of art** in materials science — it names the specific
act of using instruments to measure structure, composition, and properties. A full one-for-one synonym
that keeps *all* of that meaning is hard to find, so the best move is usually to (a) keep the term where
precision matters and (b) vary the surrounding phrasing so the word doesn't repeat 5–6 times. Options,
roughly ordered from "closest meaning" to "looser":

| Alternative | Best used as | Notes |
| --- | --- | --- |
| **materials analysis** / **analysis** | verb-ish + noun | Closest general substitute; "analyzing metals," "analytical methods." |
| **metrology** / **measurement science** | noun | Precise, professional; emphasizes the *measurement* fidelity angle we care about. |
| **microstructural and compositional analysis** | noun (formal) | Spells out exactly what we measure; good for the opening sentence. |
| **material evaluation** / **assessment** | noun/verb | Slightly broader (can imply judging suitability), still reads well. |
| **probing** (a material) / **interrogating** | verb | "probing the microstructure," "interrogating composition"; vivid, still accurate. |
| **measuring** (composition/microstructure) | verb | Plain and honest; pairs well with "high-fidelity." |
| **material fingerprinting** | noun (informal) | Evocative but less standard — use sparingly. |

**Recommendation:** keep **"characterization"** for the named methods (SEM/EDS/EBSD/XRF *are*
characterization techniques — that phrase is expected), and swap the *other* occurrences for
**"analysis," "measurement," "metrology,"** or the explicit **"compositional and microstructural
analysis."** That removes the repetition without weakening any meaning. (v3 above already applies this.)

---

## v2 — lightly polished (same idea, varied wording, "characterization" de-repeated)

Understanding the properties of a novel metal alloy depends on measuring it accurately, yet the leading
analytical methods — SEM, EDS, EBSD, and XRF — only return representative results when their acquisition
parameters are set correctly. Finding those parameters today takes substantial time and trial-and-error.
We are building a system that couples current characterization documentation with retrieval-augmented
generation (RAG), a growing experimental dataset, and a feedback loop, so that it can recommend
high-fidelity acquisition settings for a given sample and analysis goal. By combining established
characterization knowledge with the data we collect in-house, the system yields a literature- and
physics-grounded method for choosing baseline parameters — sharply reducing the time needed to reach
high-fidelity compositional and microstructural analysis of new alloys.

---

## Small content suggestions for the refining pass (not urgent)

1. **Pick "large dataset" *and* "AI/RAG," not "either…or."** The v1 draft said "*either* a large dataset
   *or* integration with AI." Our actual pitch (and byu-vcl#95) is that the dataset **feeds** the AI/RAG
   loop — they're one system, not alternatives. (v2/v3 already fix this.)
2. **Consider one concrete hook.** The strongest version names a real failure it fixes — e.g., standardless
   SEM-EDS over-reporting trace Mg in AlSi10Mg, or EBSD indexing yield jumping once beam current/phase model
   were corrected (both from byu-vcl#95). One sentence of that makes the time-savings claim credible rather
   than generic. *(Still not in v3 — see the comment thread; optional given the 150-word cap.)*
3. **Say what "high-fidelity" is measured against.** Even a half-clause ("benchmarked against ICP-MS")
   tells reviewers the fidelity claim is falsifiable.
4. **Scope the AI as decision-support, not replacement** — "recommends and refines parameters," which is
   both honest and less likely to draw skeptical reviewers. (v3 does this.)

None of these change the core idea; they just make it land harder.
