# Who reads the ONR YIP proposal: published backgrounds of the program officer and likely reviewers

Sterling's request on PR 134 (Oct 24, 2026, 05:15 UTC): "run a series of Edison scientific queries with the
backgrounds of the program manager and potential reviewers. Stage and ping an update to DAL that includes this
(fine for real names here)".

**Who evaluates.** NOFO N0001426SF004, p. 31: "The cognizant Program Officer and other Government scientific
experts will perform the evaluation of technical proposals", and support contractors may serve as
subject-matter consultants under a non-disclosure agreement. The program officer named on the cover is
Dr. Charles R. Fisher (Code 332, Materials & Processes for Additive Manufacturing). Dr. Reginald G. Williams
(Code 34) manages the YIP itself. The other people below are guesses at the "other Government scientific
experts" from DAL's own notes (`po-email.md`, `onr-questions.md`, `carderock-questions.md`) and from the
literature. **Nothing in the published record says who will actually review this proposal.**

Eight queries, one batch, submitted 05:26 UTC. The `CONTEXT` block is the one DAL's
`edison-trajectories/cu-ded-2026-10/queries.py` uses, so the answers line up with that batch.
[`edison_reviewers.py`](edison_reviewers.py) is DAL's `edison_cu_ded.py` with a new docstring, so this folder
drops into DAL's `edison-trajectories/` layout unchanged.

| Query | Job | Task | Answer |
|---|---|---|---|
| Charles R. Fisher, program officer | LITERATURE_HIGH | `b015d49c` | [r1-01](batch1/r1-01-fisher-program-officer.md) |
| Carderock and NSWC copper AM and corrosion authors | LITERATURE | `b34e5c11` | [r1-02](batch1/r1-02-carderock-copper-am.md) |
| David A. Shifler, corrosion program officer | LITERATURE | `05081768` | [r1-03](batch1/r1-03-shifler-corrosion.md) |
| Chakrapani (Pani) V. Varanasi, Computer-Aided Materials Design | LITERATURE | `615a9ce5` | [r1-04](batch1/r1-04-varanasi-camd.md) |
| Jennifer N. Wolk, Manufacturing focus area lead | LITERATURE | `636c855c` | [r1-05](batch1/r1-05-wolk-manufacturing.md) |
| Reginald G. Williams (YIP program manager) and past materials YIPs | LITERATURE | `ca860c2f` | [r1-06](batch1/r1-06-yip-program-and-pm.md) |
| NRL, NAVAIR, NPS and Penn State ARL experts on DED and corrosion | LITERATURE | `39e538a2` | [r1-07](batch1/r1-07-navy-lab-am-corrosion-experts.md) |
| Navy and ONR-funded ML and autonomous experimentation for materials | LITERATURE | `8bd7b931` | [r1-08](batch1/r1-08-navy-ml-autonomous-materials.md) |

Full task ids are in [`_task_ids.json`](_task_ids.json). The raw trajectories are not in this public repository:
they hold the text of the papers Edison read, including authors' contact emails and a 2016 workshop attendee
list with emails. They are in the agent-staging drop
`for/vertical-cloud-lab/digital-alloy-lab/2026-10-24-onr-yip-revisions-and-reviewers/` (`sgbaird/agent-staging`
at `6c27df4`, `payload/edison-reviewers/raw/`), and `raw/` is gitignored here. One corresponding-author email
quoted in r1-01 is redacted; the answers are otherwise as Edison returned them.

## What to change in the proposal

These follow from the answers. Every reference below came from Edison; check each DOI on Crossref before it goes
into the bibliography, as DAL does for all references.

1. **Cite the rest of Fisher's copper work where the heat-flow model uses it.** The draft cites Orzolek, Semple
   and Fisher (2022) and the three Norkett and Fisher databases. Two more fit the heat-flow model directly:
   Hatala, Wang, Reutzel, Fisher and Semple, "A thermo-mechanical analysis of laser hot wire additive
   manufacturing of NAB", *Metals* 11, 1023 (2021), doi:10.3390/met11071023, which found that room-temperature
   property constants in place of temperature-dependent ones can reverse the predicted distortion; and Orzolek,
   Norkett and Fisher, "Temperature-dependent material property database for C63200 nickel-aluminum bronze (NAB)
   plate", *IMMI* 12, 481-492 (2023), doi:10.1007/s40192-023-00325-3. Say that the model uses
   temperature-dependent properties from this series and where it falls back on estimates.
2. **End the search in a pedigreed dataset.** Fisher's main body of work is the IMMI series of pedigreed,
   temperature-dependent property databases for Navy steels, NAB and Cu-Ni. Framing the outcome as "the search
   narrows the field, then each finalist gets replicated builds and a property and corrosion dataset in the form
   of Carderock's databases" speaks his language. "Calculations replace measurements" would not. The HSLA-80
   paper put its raw files on Materials Commons (doi:10.13011/m3-cz82-dw37); the data management plan can name
   that as the model for releasing each finalist's data.
3. **Keep kappa phase as a hypothesis to test, with the tools to see it.** Orzolek et al. (2022) did not resolve
   kappa precipitates at the magnifications they used and called for wider heat-input studies and TEM. The
   as-deposited objective is plausible (as-built WAAM NAB has outperformed annealed NAB in chloride), but the
   proposal should say that finalists get TEM or other quantitative phase analysis, not only hardness and the
   one-hour screen.
4. **Separate discovery from qualification.** None of the officers' papers address MIL-PRF-32804, -32815 or
   -32816, and both the Fisher and Wolk answers warn against promising a Navy-ready replacement alloy. Wording
   that fits: composition windows and "the evidence needed to judge whether a controlled repair consumable or a
   specification revision is warranted", or "a candidate for Navy qualification testing". Name what would remain
   after the project (component tests, fatigue, inspection, allowables).
5. **Tie powder oxygen to the repair interface.** Fisher's earlier alloy design (Fisher et al., "A reactive
   element approach to improve fracture healing in metallic systems", *Frontiers in Materials* 6, 210 (2019),
   doi:10.3389/fmats.2019.00210) used oxide thermodynamics to choose additions that improve wetting and bonded
   area, and named powder oxygen in AM as an application. One sentence linking measured powder oxygen to wetting
   and fusion on cast NAB and wrought Cu-Ni would connect to it.
6. **Call the one-hour screen a ranking assay that is calibrated.** Matched preparation and exposure for the
   deposits and wrought C71500, replicates, and localized-damage endpoints measured separately on the deposit,
   the fusion boundary and the substrate. NRL's Hangarter, Geltmacher et al., *ECS Advances* 4, 011501 (2025),
   doi:10.1149/2754-2734/adb16a, measured 3D crevice damage on printed stainless steel by X-ray tomography and
   matched it to electrochemistry; Brewick, *J. Electrochem. Soc.* 169, 011503 (2022),
   doi:10.1149/1945-7111/ac4935, showed printed microstructures pit deeper than a homogeneous model predicts.
   Both argue for keeping microstructure in the corrosion model.
7. **Show uncertainty at each link and test transfer instead of asserting it.** Report calibration of the
   predictions, error on compositions outside the training family (Cu-Ni to NAB), and baselines (random,
   composition only, equal cost per step), scored on total dollars and DED hours to a confirmed candidate rather
   than on cheap tracks screened. Huang, Jamieson (Penn State ARL) and Basak, "Uncertainty-aware
   reconstruction of full process maps in laser-directed energy deposition using scarce data", *Welding in the
   World* (2026), doi:10.1007/s40194-026-02629-2, transferred process maps between wire and powder DED with
   uncertainty; it is the closest precedent for carrying results from the Utah MX-Lab to the Mines X2.
8. **Say what hardness, density and corrosion do not show for a repair.** NAVAIR's Nam Phan and ONR's Michael
   Brindza co-wrote a 2026 review of crack growth in printed steels (Jones et al., *Materials* 19, 372,
   doi:10.3390/ma19020372). A sentence that interface defects, residual stress and fatigue of repairs are
   measured on finalists or left to Navy laboratories closes that gap.
9. **Cite Carderock's own NAB corrosion paper for why screens need checking.** Iannuzzi, Vasanth (NSWCCD Code
   613) and Frankel, "Unusual correlation between SKPFM and corrosion of nickel aluminum bronzes", *J.
   Electrochem. Soc.* 164, C488-C497 (2017), doi:10.1149/2.0391709jes: in C63200 the copper-rich alpha phase
   dissolved first, and the ranking of phases by Volta potential in air did not predict corrosion in solution.
   It is a Navy example of a quick measurement ranking wrongly, which is the case for the audit of screened-out
   candidates.
10. **Cite the closest ICME precedent.** Wang and Xiong, "Uncertainty quantification and composition
    optimization for alloy additive manufacturing through a CALPHAD-based ICME framework", *npj Comput. Mater.*
    6 (2020), doi:10.1038/s41524-020-00454-9, screened 450,000 HSLA steel compositions for the probability of
    meeting strength, toughness and weldability targets under powder-composition uncertainty, with ONR support
    (not a YIP). The comparison with other approaches should say what this proposal adds: thermal history,
    corrosion, and choosing which experiment to run.
11. **Open with a general scientific question, then the naval test.** The past materials YIPs Edison found
    (Ong's alloy potentials, 2016; Locke's corrosion fatigue of sensitized AA5456, 2016, managed by Dr. Airan
    Perez; Moridi's printing of refractory metals and reactive aluminum composites, 2022) each answered a
    mechanism question and then tied it to an application. One sentence near the top in that form would help,
    for example: how do powder composition and the DED thermal history together set segregation, cracking,
    interface soundness and corrosion of as-deposited copper alloys? Repair on cast NAB and wrought Cu-Ni and the
    C71500 benchmark are then the demanding test of the answer.
12. **Write the corrosion plan for the corrosion program officer.** Dr. Shifler's own record is seawater testing
    and galvanic corrosion: Shifler and Aylor, "Considerations for the testing of materials and components in
    seawater", CORROSION 2002, doi:10.5006/c2002-02217; Shifler, "Understanding and modeling galvanic corrosion
    in marine environments", CORROSION 2006, doi:10.5006/c2006-06283; Shifler and Enos, "Marine corrosion
    testing", *LaQue's Handbook of Marine Corrosion* (2022), doi:10.1002/9781119788867.ch15. What that suggests:
    report the screen's rank agreement with 30-day immersion and its false-negative rate with confidence
    intervals (the audit gives these), and add a few candidates just either side of the cutoff; expose the repair
    as a couple (deposit on cast NAB and on wrought Cu-Ni, fusion boundary exposed, stated area ratio) as well as
    free-standing coupons; section after exposure to find the deepest selective attack; and name the Navy
    laboratory hand-off for natural and flowing seawater with a sample count. Edison's suggested phrase:
    "mechanism-checked, cost-aware screening with quantified escape risk and a staged path to flowing-seawater
    validation". Phrases to avoid: anything implying a one-hour scan or ASTM D1141 immersion certifies seawater
    service.
13. **Cite and distinguish the one paper that already sketches this workflow.** Collins and Ales, "Additive
    manufacturing enabled autonomous laboratory for materials discovery and concurrent design of materials and
    shape", *MRS Bulletin* 51, 746-769 (2026), doi:10.1557/s43577-026-01078-y, is a perspective whose
    hypothetical case study is a naval brass made by DED with quick surrogate tests and later erosion-corrosion
    tests. It is not a result, but a reviewer who knows it will ask what is new. The answer is in the draft
    already (costs per step, real paired observations, purchased sessions, the audit); one sentence in the
    comparison with other approaches makes it explicit.
14. **Show that a funnel can lose to random, then beat both.** Reyes, Liu and Diaz Vargas, "Decision-making under
    uncertainty for multi-stage pipelines", *JOM* 74, 2897-2907 (2022), doi:10.1007/s11837-022-05368-z, found in
    simulation that a sensible-looking screening funnel sometimes did worse than random selection. Add a fixed
    top-k funnel to the baselines, report each gate's false rejections, and call the campaign "human-supervised"
    rather than autonomous where DED bookings and immersion are run by hand.

## Applied to the copper proposal (2026-10-24)

All 14 items are now in `near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex`, written short
because of the 20-page limit; together they take the draft from 19 to 20 counted pages. All 15 DOIs above
resolve on Crossref with the titles, authors, volumes and pages given (the Materials Commons DOI resolves on
DataCite), and each claim was checked against an abstract or the open full text as noted.

| # | What changed | Where | Checked against |
|---|---|---|---|
| 1 | The heat-flow model is calibrated to melt pools and given the properties Carderock measured for 70-30 and 90-10 Cu-Ni, C63200 plate and wire-arc NAB. Room-temperature constants can reverse the predicted distortion. New compositions get properties from the nearest measured alloy and CALPHAD, with the added uncertainty carried | Scientific concepts | Hatala 2021 abstract (reversed substrate displacement); Orzolek 2023 title and metadata |
| 2 | Each finalist gets replicated builds and a dataset in the form of the Carderock databases, raw files public; the DMP names Materials Commons, as for HSLA-80 | Task 4; DMP | Semple 2022 metadata; dataset 10.13011/m3-cz82-dw37 on DataCite (C. Fisher, Materials Commons, 2022) |
| 3 | Finalists get TEM, so fine kappa precipitates are measured, not assumed | Task 2, microscopy | Not attributed to Orzolek 2022: ScienceDirect blocks the runner, and Edison's support for "called for TEM" came from two theses that cite it |
| 4 | Finalists are candidates for Navy qualification testing; component tests, fatigue, inspection, allowables, and the consumable or specification decision remain | Task 4 | (wording) |
| 5 | Powder oxygen and the repair interface | Task 2, powder checks | Fisher 2019 full text: better wetting and bonded area; names oxygen in powder AM as an application |
| 6 | The screen as a ranking that has to be calibrated (same preparation and exposure, replicates, test conditions recorded); microstructure stays in the corrosion model | Task 2, corrosion | Brewick 2022 and Hangarter 2025 abstracts |
| 7 | Calibration at each link, error outside the training family (NAB from Cu-Ni data), ablations, scoring on dollars and DED hours; Utah-to-Mines transfer tested on paired compositions | Task 3 | Huang, Jamieson and Basak 2026 abstract (wire to powder DED, with uncertainty) |
| 8 | Hardness, density and corrosion do not show whether a repair lasts; fatigue and residual stress are left to Navy laboratories | Advance 4 | Jones et al. 2026 abstract |
| 9 | Carderock's NAB SKPFM paper as a quick measurement that ranked the phases backwards | Copper alloys in naval service | Iannuzzi 2017 full text: rolled C63200, alpha attacked; Vasanth at NSWCCD Code 613 |
| 10 | The closest ICME precedent and what it leaves out | Comparison | Wang and Xiong 2020 full text: ONR AMANE program (N00014-17-1-2586), which r1-08 could not confirm; inputs are composition and heat treatment |
| 11 | A materials question beside the methods question, with repair as the demanding test | Problem and objectives | (wording) |
| 12 | Rank agreement and false rejections with confidence intervals, candidates near the cutoff (H5); repair coupons immersed whole at a stated area ratio; sectioning for the deepest attack; flowing seawater for three leading candidates and two references, with a TODO to confirm with Carderock | H5; Task 2, corrosion | Shifler and Aylor 2002 and Shifler 2006 abstracts; Shifler and Enos 2022 metadata |
| 13 | Collins and Ales cited and set apart | Comparison | Full text (Iowa State repository copy): Case Study 2 is a hypothetical naval brass by DED with a hardness screen ahead of erosion-corrosion tests; ONR grant N000142312721 |
| 14 | A fixed top-k funnel among the baselines; the funnel-worse-than-random result; campaigns "supervised by people" | Task 3 | Reyes 2022 (arXiv 2203.01143): "screening can even perform worse than random in some cases" |

## What the record says about each person

**Dr. Charles R. Fisher** ([answer](batch1/r1-01-fisher-program-officer.md), the deep query). Every paper since
2015 lists NSWC Carderock; his ONR role is on ONR's pages, not in a paper. A SMART scholar with University of
Florida co-authors (Manuel, Mecholsky), so probably a UF Ph.D. Three lines of work: the IMMI series of
temperature-dependent property databases for ICME (naval steels DH36 to HY-100, C63200 NAB plate, wire-arc NAB,
cast 70-30 and 90-10 Cu-Ni), copper-alloy AM and welding (NAB processing in *Additive Manufacturing* 2022, the
laser hot-wire NAB model in *Metals* 2021 with Penn State ARL), and self-healing alloys designed with oxide
thermodynamics. He co-edited the ICME 2017 World Congress proceedings. His papers characterize specification
alloys and do not propose new compositions, which is the gap this proposal fills. Recurring co-authors: Semple,
Norkett, Bechetti, Orzolek (NSWCCD), Wei Zhang (Ohio State), Hatala and Reutzel (Penn State ARL).

**Dr. Chakrapani (Pani) V. Varanasi** ([answer](batch1/r1-04-varanasi-camd.md)). Thin record: one verified
paper, with an Army Research Office affiliation in 2013 (carbon nanotube growth on diamond films, with AFRL and
UDRI co-authors). Edison would not infer AFRL or UDRI positions from co-authors' affiliations. What he would
probe is inferred from ONR program context: a precisely named computational advance, uncertainty at every link,
validation on compositions the models have not seen, and transfer shown rather than claimed.

**Dr. Jennifer N. Wolk** ([answer](batch1/r1-05-wolk-manufacturing.md)). Thin record: a 2011 University of
Maryland thesis on friction-stir-welded Ti-5111, two papers with Nimer and Zupan on location-specific weld
properties (2013, 2014), and a Navy attendee line in ORNL's 2016 big-area AM workshop report. A FY2018 MURI topic
on physics-based models of as-deposited AM alloys named Billy Short and Jennifer Wolk as topic chiefs (from the
Varanasi answer). The advice drawn from this: promise qualification-relevant evidence, not certification; keep
an auditable record from powder lot to test; treat deposits on themselves and repairs as separate cases.

**Navy laboratory experts** ([answer](batch1/r1-07-navy-lab-am-corrosion-experts.md)). Five verified groups:
NRL's Carlos Hangarter, Andrew Geltmacher and co-authors (3D crevice corrosion of printed stainless steel);
NRL's Patrick Brewick (phase-field pitting in printed 316L); Penn State ARL's Cory Jamieson (uncertainty-aware
DED process maps from scarce data); NAVAIR's Nam Phan (crack growth and qualification of printed parts, with
Brindza); and NPS's Troy Ansell (liquid-metal printing review, adjacent only). It found no post-2015 copper
paper from NRL Key West.

**Carderock's copper and welding group** ([answer](batch1/r1-02-carderock-copper-am.md)). The verified group is
a characterization and computational-welding team in the Welding, Processing and Nondestructive Evaluation
Branch: Jennifer K. Semple, Daniel H. Bechetti, Sean M. Orzolek, Justin E. Norkett, Jack H. Canaday and Fisher,
with Wei Zhang (Ohio State) and Hatala, Wang and Reutzel (Penn State ARL) as collaborators. The one verified
Carderock corrosion author is K. L. Vasanth (Code 613), on NAB. Nothing places a copper-alloy author at NSWC
Philadelphia. Their papers characterize specification alloys and their temperature-dependent properties; none
designs a new powder, so the gap the proposal fills is the linked composition, powder, as-deposited repair and
seawater record. Edison's advice: check each Carderock dataset's contents and terms before using it, and don't
carry cast or wire-arc property curves to laser powder DED without validation.

**Dr. Reginald G. Williams and past materials YIPs** ([answer](batch1/r1-06-yip-program-and-pm.md)). No
research record could be tied to him with confidence, so nothing here describes his preferences. The YIP awards
Edison could verify from paper acknowledgments are in item 11 above.

**Dr. David A. Shifler** ([answer](batch1/r1-03-shifler-corrosion.md)). A 2024 review acknowledges him as an
ONR program officer. His papers (2000 to 2022) cover marine material interactions (*Corrosion Science* 47, 2335,
2005), seawater testing with Denise Aylor, galvanic corrosion in naval piping, and hot corrosion and coatings for
marine gas turbines (the 2016 Speller Award lecture). Edison found no paper of his on printed Cu-Ni or NAB and no
dated record of earlier Navy laboratory positions. Item 12 is the corrosion plan this record points to.

**Navy and ONR-funded ML for materials** ([answer](batch1/r1-08-navy-ml-autonomous-materials.md)). NRL's
Patrick G. Callahan (Materials Science and Technology Division) co-edited a 2022 *JOM* topic on autonomous data
collection and active learning. The closest ONR-funded corrosion cluster is the MURI around John Scully
(Virginia), Jason Hattrick-Simpers (Toronto) and Howie Joress and Brian DeCost (NIST): scanning-droplet-cell
screening, Gaussian-process active learning of corrosion, and Bayesian analysis of impedance spectra (AutoEIS).
The draft already cites DeCost 2022 and Sur 2023. Penn State ARL's Abdalla Nassar (in-process porosity
monitoring) and NRL-funded Saunders, Michopoulos et al. (Gaussian-process surrogates for printed
microstructures) are the AM side. Items 13 and 14 come from this answer, as does the benchmark matrix in it
(budget-matched baselines, ablations, held-out builds).

All eight answers were fetched by 06:00 UTC.

## Limits

- Edison works from papers, reports and program pages. It cannot see who sits on a review, and the profiles
  above are what the record supports, not a full CV. Where a record is thin (Varanasi, Wolk), it says so.
- Some 2025-2026 papers were found through metadata only, without full text; the answers mark them.
- Every person named is a Government employee or a published researcher, named from public records. Sterling
  cleared real names for this hand-off.
