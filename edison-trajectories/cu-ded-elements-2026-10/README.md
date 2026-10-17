# Copper/DED search space: one Edison query per element (2026-10-17)

*For PR #117, the copper/DED version of the ONR FY27 YIP proposal
(`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex`).
Sterling asked on 2026-10-17 for the copper search space to be backed the way
the aluminum one was, elements and bounds with reasons and a separate Edison
query per element, and for 50 such queries, one per element picked from the
periodic table. He also asked how the CubXL could serve the electrochemical
side; that answer is in
[`near-term-submissions/onr-yip/cubxl-electrochemistry.md`](../../near-term-submissions/onr-yip/cubxl-electrochemistry.md),
from the two Edison queries in [`electrochem/`](electrochem/).*

## The result in short

- **Eight elements are searched from the start,** with Cu as the balance:
  - Ni 0-33, Al 0-10.5, Fe 0-5, Mn 0-4 and Ti 0-0.5 wt%;
  - Cr 0-1, Si 0-0.5 and Nb 0-1 wt%, in Cu-Ni only.
- **Year 2 adds four microalloying options:** Zr, B, Sn (NAB only), and one
  rare earth (La or Ce).
- **Hard constraints:** Cu ≥ 65 wt% and a CALPHAD liquidus ≤ 1,250 °C.
  Because the atomizer's induction module reaches about 1,300 °C, the
  liquidus, not the box bound, is what limits Ni.
- **Rules keyed to the Al content:**
  - **Above 7 Al (NAB):** Ni ≥ Fe and Si ≤ 0.1.
  - **Below 1.5 Al (Cu-Ni):** Fe ≤ 2.3.
  - **Between, in the Cu-Ni-Al bridge with Ni ≥ 10:** Fe ≤ 1.
  - **Cr and Nb:** only up to 3 Al.
  - **Si above 0.1:** only with Nb ≥ 1.55 Si - 0.10.
- **Retained β/β′:** predicted by CALPHAD along the DED thermal history
  (Advance 3), not by a fixed aluminum-equivalent formula. That formula's
  coefficients could not be verified.
- **Impurity limits** sit at or below the welding-grade limits for Cu-Ni:
  Pb ≤ 0.01, S ≤ 0.01, P ≤ 0.02, C ≤ 0.02, Bi ≤ 0.001, Zn ≤ 0.5 wt%, and
  O ≤ 0.02 wt% in powder.
- **Excluded,** each with a reason in the table below:
  - Be and Cd (toxic powder and fume);
  - W and Ta (immiscible with Cu, melting far above the atomizer limit);
  - Ag, Ge and Pd (cost, single-study evidence);
  - Co (counted with Ni);
  - seven others with no seawater benefit found, and six rare earths.

The machine-readable version is [`search_space.py`](search_space.py), which
writes [`search_space.md`](search_space.md). It is the single source of
truth, as `\elementpalette` is for the aluminum proposal. The proposal
carries the eight elements as Table 1 and a paragraph in Task 2.

## How the aluminum space was chosen, and what is the same here

The aluminum palette was chosen in two steps:

1. **Elements.** A short list was screened by CALPHAD coverage (how many
   Al-X-Y ternaries Thermo-Calc's TCAl10 assesses) and by supply risk, which
   gave 15 elements ([`../edison-search-space-reframing.md`](../edison-search-space-reframing.md)).
2. **Bounds.** Each of the 16 elements (Al included) got its own Edison
   LITERATURE query for a conservative and a non-conservative bound, with
   the failure modes that set them. One query asked for Al_min and one for
   all bounds at once. An Edison ANALYSIS job then merged the answers into a
   bounds table, and a second added multi-element constraints (branch
   `copilot/determine-bounds-for-elements`, `edison-trajectories/element-bounds/`).

This run keeps both steps, but does the per-element queries first and wider:

- **50 elements, not 16.** Each query also asks whether the element belongs
  at all (INCLUDE as an addition, LIMIT as an impurity, or EXCLUDE), so the
  palette comes out of the queries instead of going in.
- **Same coverage screen,** with Thermo-Calc's copper database TCCU7 in place
  of TCAl10 ([`tccu7_coverage.md`](tccu7_coverage.md)).
- **Same synthesis:** one joint query (LITERATURE_HIGH), then two ANALYSIS
  jobs with every answer uploaded: one for the bounds table
  ([`phase2/`](phase2/)) and one for the multi-element constraints
  ([`phase3/`](phase3/)). They ran side by side rather than in sequence, to
  fit the 3-hour job.
- **Extra questions per element:** seawater corrosion, DED and weld
  cracking, repair on cast NAB and wrought Cu-Ni, melting and atomizing in a
  ceramic crucible below about 1,300 °C, supply and toxicity, and a one-line
  VERDICT for tabulation ([`verdicts.md`](verdicts.md)).
- **One step the aluminum run did not have:** every answer was checked
  ([`checks.md`](checks.md)), including the cited DOIs against Crossref.

## Which 50 elements, and why

`elements.py` lists them with the hint each query carried (the alloys and
specifications the element appears in).

| Group | Elements |
| --- | --- |
| Matrix | Cu |
| Major additions in Navy seawater copper alloys | Ni, Al, Fe, Mn, Cr, Sn, Zn, Si, Nb |
| Precipitation, grain-refining and strengthening additions | Be, Co, Ti, Zr, Hf, Mg, Ag, V, B |
| Dezincification inhibitors and deoxidizers | As, Sb, P |
| Free-machining or low-melting, usually impurities | Pb, Bi, Se, Te, S, Cd |
| Interstitials and gases in powder and deposits | O, H, N, C |
| Refractory metals nearly immiscible with Cu | Mo, W, Ta |
| p-block solid-solution elements | Ga, Ge, In |
| Alkali and alkaline-earth deoxidizers | Li, Ca, Sr |
| Rare earths, Sc and Y | Sc, Y, La, Ce, Pr, Nd, Er, Gd |
| Platinum group | Pd |

**Not queried (68).** These classes have no use in seawater copper alloys,
or cost thousands of dollars per kilogram:

- noble gases (He, Ne, Ar, Kr, Xe) and halogens (F, Cl, Br, I);
- elements with no stable isotope (Tc, Pm, Po, At, Rn, and Fr onward,
  including Th and U; 37 in all);
- the heavy alkali metals and Ba (Na, K, Rb, Cs, Ba);
- the platinum group other than Pd, plus Re and Au;
- Hg and Tl, and the lanthanides other than the six queried (Sm, Eu, Tb,
  Dy, Ho, Tm, Yb, Lu).

One member of three borderline classes was queried, so that dropping the
class rests on an answer: Pd for the platinum group, Sr for the heavier
alkaline earths, and Gd for the heavy lanthanides. All three came back
EXCLUDE.

## What was run

| Phase | Jobs | Submitted (UTC) | Returned |
| --- | --- | --- | --- |
| 1 | 50 LITERATURE, one per element | 18:58-19:02 | 19:20-19:35 (19-34 min each) |
| 1 | 1 LITERATURE_HIGH, joint bounds for a 20-element short list | 19:02 | 19:35 |
| 2 | 1 ANALYSIS, palette and bounds table (53 files uploaded) | 19:36 | see [`phase2/`](phase2/) |
| 3 | 1 ANALYSIS, multi-element constraints (53 files uploaded) | 19:36 | 19:48 |
| 4 | 2 LITERATURE, electrochemistry for the CubXL question | 19:03 | 19:28-19:31 |

Each answer file holds the question first, then Edison's answer. Raw
trajectories are in `raw/`, and task IDs and times are in `_task_ids.json`.
To rerun, use `run_elements.py submit|wait|fetch|status`; the questions are
in `queries.py` and `analysis_prompts.py`.

The question template follows the earlier copper run
(`../cu-ded-2026-10/queries.py`):

- a context block, with the PI's own papers excluded;
- requests for DOIs and numbers;
- tags ([CITE], [NUMBERS], [SPEC], [NAVY], [GAP]);
- an instruction to say so when nothing is found;
- no date window, since a window hid older prior art last time.

## CALPHAD coverage (TCCU7)

TCCU7 ([technical information, Thermo-Calc 2026b](https://thermocalc.com/wp-content/uploads/Documentation/Databases/Thermodynamic/tccu7-technical-info.pdf),
document dated 12 June 2026) has:

- **Size:** 34 elements, 175 assessed binaries (every Cu-X binary among its
  elements) and 79 assessed ternaries.
- **Coverage of the 49 queried additions:** 31 are in TCCU7. The 18 that are
  not: H, N, Hf, V, Ga, In, Li, Sr, Sc, Y, Pr, Nd, Er, Gd, Pd, Sb, Te and W.
- **Tiers,** counted like the TCAl10 tiers as assessed Cu-X-Y ternaries:
  - **Tier 1 (6 or more):** Ni 20, Fe 13, Sn 12, Cr 10, Si 10, Mn 9, Al 8,
    Zn 8, Ag 7, Co 6, S 6.
  - **Tier 2 (3-5):** Nb 5; La, Pb and Ti 4; Ce, Mg, Mo, O, P and Zr 3.
  - **Tier 3 (0-2):** Ge, Ta, Be, C, As, B, Bi, Ca, Cd and Se.

**Coverage of the eight-element palette:**
- 18 of its 28 pairs have an assessed Cu-X-Y ternary.
- Of the 56 Cu-X-Y-Z quaternaries, one (Cu-Al-Fe-Ni, the NAB core) has all
  four constituent ternaries assessed, and 15 more have three. That makes 29%
  with at least three of four, against 20% for the aluminum palette in TCAl10.
  The aluminum anchor Al-Mn-Cr-Zr had none of its four ternaries assessed.

**Gaps that matter:**
- **Pairs with no assessed Cu-X-Y ternary:** Al-Cr, Al-Nb, Al-Ti, Fe-Nb,
  Fe-Ti, Mn-Cr, Mn-Nb, Mn-Ti, Cr-Ti and Si-Nb.
- **Mn-Cr has no assessed binary either.** Mn and Cr appear together in
  C72200.
- **Cu-Nb-Si is not assessed,** but the Nb-Si rule depends on Ni-Nb-Si
  precipitates.
- **What to do about them:** candidates that use these pairs at
  substantial levels should be checked against experiment early. One such
  check is wire-arc C72200-type deposits for Mn-Cr. The family rules keep
  Cr and Nb out of high-Al alloys, and Ti at or below 0.1 in NAB, which
  avoids most of the Al-X gaps.

**Edison misjudged this coverage.** Most per-element answers said TCCU
coverage was "unverified", and the joint answer guessed. Neither had the
TCCU7 documentation. For example, Edison expected Cu-Ni-Nb and the rare
earths to be "extrapolated or absent", but Cu-Ni-Nb, Ce-Cu-Ni and Cu-La-Ni
are assessed. The ANALYSIS jobs were given `tccu7_coverage.md` and used it.

## Element by element

Edison's verdict, the decision taken here, and the reason. The bounds are in
[`search_space.md`](search_space.md), and Edison's raw numbers are in
[`verdicts.md`](verdicts.md).

| Element | Edison | Decision | Reason | TCCU7 tier |
| --- | --- | --- | --- | --- |
| [Cu](phase1/el-01-Cu.md) | LIMIT | balance | Balance, at least 65 wt%. The calculated liquidus (at most 1,250 C) is the binding limit: Cu-Ni above about 33 Ni melts too high to atomize. The 60 wt% floor Edison offered is not used in the first campaign. | matrix |
| [Ni](phase1/el-02-Ni.md) | INCLUDE | search | Main film-former in Cu-Ni and a kappa former in NAB; the strongest route to C71500-class resistance. Capped by the liquidus near the atomizer limit (70-30 melts to about 1,240 C). Nickel burden is an objective, not a bound. | 1 |
| [Al](phase1/el-03-Al.md) | INCLUDE | search | Defines the aluminum bronze branch and the Cu-Ni-Al region between the families. The upper range keeps the retained-beta boundary inside the space, so the process-aware CALPHAD screen (H3) can be tested on it, and it includes the duplex alpha+beta bronzes, which crack less as weld filler than single-phase ones but risk selective attack of beta. | 1 |
| [Fe](phase1/el-04-Fe.md) | INCLUDE | search | Needed for the Cu-Ni film and for kappa phases in NAB. Bounded by family rules: kept in solid solution in Cu-Ni (at most 2.3), Ni at least equal to Fe in NAB. | 1 |
| [Mn](phase1/el-05-Mn.md) | INCLUDE | search | Deoxidizer and partial nickel substitute (C71640, MARINEL). Upper bound set by evaporation and oxidation in melting and DED; Mn-Al bronze (11-14 Mn) is left out for that reason. | 1 |
| [Cr](phase1/el-06-Cr.md) | INCLUDE | search | Raises erosion-corrosion resistance of Cu-Ni (C72200 critical velocity about 3 times that of C71500), but higher-Cr Cu-Ni had worse crevice attack in still water. Cu-Ni and Cu-Ni-Al only. | 1 |
| [Sn](phase1/el-07-Sn.md) | INCLUDE | optional | An impurity in the target alloys (C63000 at most 0.20; EN Cu-Ni grades at most 0.03-0.05). About 1 wt% refined cast NAB grains and raised strength (Poojary et al. 2023), but the only chloride series is a porous sintered shape-memory alloy, and Sn widens the freezing range. A Year-2 option for NAB only. | 1 |
| [Zn](phase1/el-08-Zn.md) | LIMIT | limit | Boils at 907 C (evaporation in melting and DED), dezincifies in seawater; Cu-Ni welding grades limit it to 0.5. | 1 |
| [Si](phase1/el-09-Si.md) | INCLUDE | search | Deoxidizer, and with Nb a strengthener of cast 70-30 Cu-Ni (Si up to 0.5 in C96400, with Nb at least about twice Si). Silicides and weld cracking above that; C95800 allows only 0.10, so Si is a Cu-Ni variable. Silicon bronze levels (about 3) are not a seawater-repair target. | 1 |
| [Nb](phase1/el-10-Nb.md) | INCLUDE | search | Added to cast Cu-Ni (C96400, 0.5-1.5) for weldability and present in MARINEL (0.6-0.9). Must be added as a master alloy (Nb melts at 2,477 C). Cu-Ni branch only. | 2 |
| [Be](phase1/el-11-Be.md) | LIMIT | exclude | Beryllium powder and fume are a severe inhalation hazard (OSHA 2017 standard); not compatible with in-house atomization and laser deposition. | 3 |
| [Co](phase1/el-12-Co.md) | INCLUDE | exclude | Counted with Ni in Cu-Ni specifications; costlier and scarcer than Ni, with no seawater benefit shown over Ni and Fe. | 1 |
| [Ti](phase1/el-13-Ti.md) | INCLUDE | search | Deoxidizer in the ERCuNi welding filler (0.20-0.50), the closest analogue of a laser-deposited Cu-Ni. Oxide and nitride inclusions and crucible attack above that. In NAB only up to 0.1 is supported (0.1 Ti lowered the corrosion current of wire-arc NAB by about 16%). | 2 |
| [Zr](phase1/el-14-Zr.md) | INCLUDE | optional | Grain refiner (C15000; cast bronzes from about 0.01), but about half is lost on melting, the excess above its solubility (about 0.1-0.2) goes to grain boundaries, and Cu-Ni-Zr is not assessed in TCCU7. A Year-2 option. | 2 |
| [Hf](phase1/el-15-Hf.md) | EXCLUDE | exclude | Works only after aging, costly, reacts with alumina, not in TCCU7. | 4 |
| [Mg](phase1/el-16-Mg.md) | LIMIT | limit | Deoxidizer residual only; boils at about 1,090 C, below the melt temperature, and attacks alumina; harmful to NAB hot ductility. | 2 |
| [Ag](phase1/el-17-Ag.md) | INCLUDE | exclude | Edison's 'include' rested on one Ag-nanoparticle study in a shape-memory Cu-Al-Ni alloy, read through a review. Residual Ag is counted with Cu, as the specifications do. | 1 |
| [V](phase1/el-18-V.md) | EXCLUDE | exclude | No use or benefit found in seawater copper alloys; not in TCCU7. Watch for pickup from a Ti-6Al-4V sonotrode. | 4 |
| [B](phase1/el-19-B.md) | INCLUDE | optional | Grain refiner at 0.002-0.02 in cast bronzes, but borides, a Ni-B eutectic (about 1,090 C) below the Cu-30Ni solidus, and dosing at 0.5 kg scale make it a later-round option. No Cu-B-X ternary in TCCU7. | 3 |
| [As](phase1/el-20-As.md) | LIMIT | limit | Dezincification inhibitor in brasses (0.02-0.06), not needed without Zn; toxic and volatile. | 3 |
| [Sb](phase1/el-21-Sb.md) | LIMIT | limit | Dezincification inhibitor in brasses; hot shortness; not in TCCU7. | 4 |
| [P](phase1/el-22-P.md) | LIMIT | limit | Deoxidizer residual; promotes hot cracking in Cu-Ni welds (welding grades: at most 0.02). | 2 |
| [Pb](phase1/el-23-Pb.md) | LIMIT | limit | Insoluble, forms low-melting films (hot cracking); toxic. Welding grades: at most 0.02. | 2 |
| [Bi](phase1/el-24-Bi.md) | LIMIT | limit | Grain-boundary films embrittle copper at ppm levels. | 3 |
| [Se](phase1/el-25-Se.md) | LIMIT | limit | Free-machining addition; hot shortness; oxygen-free copper carries only ppm. | 3 |
| [Te](phase1/el-26-Te.md) | LIMIT | limit | Free-machining addition; hot shortness; not in TCCU7. | 4 |
| [S](phase1/el-27-S.md) | LIMIT | limit | Low-melting sulfide films (hot cracking, porosity); ERCuNi allows at most 0.01. | 1 |
| [Cd](phase1/el-28-Cd.md) | LIMIT | limit | Toxic (RoHS, OSHA) and boils at 767 C; never added. | 3 |
| [O](phase1/el-29-O.md) | LIMIT | limit | Oxide films, inclusions and steam porosity; ultrasonically atomized NAB powder carried 0.013. Measured per lot by inert-gas fusion. | 2 |
| [H](phase1/el-30-H.md) | LIMIT | limit | Porosity and steam embrittlement with oxygen; controlled by dry powder and argon. | 4 |
| [N](phase1/el-31-N.md) | LIMIT | limit | Porosity in Cu-Ni welds and nitrides with Ti and Zr; controlled by shielding. | 4 |
| [C](phase1/el-32-C.md) | LIMIT | limit | Picked up from graphite crucibles or carbon-fiber plates; welding grades allow 0.05. Edison's 0.005 had no data behind it. | 3 |
| [Mo](phase1/el-33-Mo.md) | LIMIT | limit | Nearly immiscible with Cu and no seawater benefit in Cu alloys, so never added; capped because a TZM (Mo alloy) sonotrode can add it. | 2 |
| [W](phase1/el-34-W.md) | EXCLUDE | exclude | Immiscible with Cu; melts at 3,422 C. | 4 |
| [Ta](phase1/el-35-Ta.md) | EXCLUDE | exclude | Immiscible; melts at 3,017 C; nanocrystalline Cu-Ta needs mechanical alloying. | 3 |
| [Ga](phase1/el-36-Ga.md) | LIMIT | exclude | No seawater use found; critical mineral; not in TCCU7. | 4 |
| [Ge](phase1/el-37-Ge.md) | INCLUDE | exclude | Edison's 'include' rested on one heat-treated powder-metallurgy NAB sample whose Mn, Fe and Ni also changed; Ge costs about $1,000-4,000/kg, is a critical mineral under export controls, and Cu-Al-Ge and Cu-Ni-Ge are not in TCCU7. | 3 |
| [In](phase1/el-38-In.md) | LIMIT | exclude | No benefit found; critical mineral; not in TCCU7. | 4 |
| [Li](phase1/el-39-Li.md) | LIMIT | exclude | Deoxidizer only; volatile and reactive with crucibles; not in TCCU7. | 4 |
| [Ca](phase1/el-40-Ca.md) | EXCLUDE | exclude | Deoxidizer only; no use in Cu-Ni or bronzes found. | 3 |
| [Sr](phase1/el-41-Sr.md) | EXCLUDE | exclude | No use in copper alloys found (stands in for Sr and Ba). | 4 |
| [Sc](phase1/el-42-Sc.md) | EXCLUDE | exclude | No seawater benefit; very costly; not in TCCU7. | 4 |
| [Y](phase1/el-43-Y.md) | INCLUDE | exclude | One cast 90-10 abstract only; not in TCCU7. Ce or La would take the single rare-earth slot. | 4 |
| [La](phase1/el-44-La.md) | INCLUDE | optional | Shares one rare-earth variable with Ce (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 La resisted 3.5% NaCl better than Cu-10Ni, and better than with Ce (Du et al. 2025); Cu-La-Ni is assessed in TCCU7. | 2 |
| [Ce](phase1/el-45-Ce.md) | LIMIT | optional | Shares one rare-earth variable with La (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 Ce resisted 3.5% NaCl better than Cu-10Ni (Du et al. 2025); Edison's 0.04 cap came from mischmetal retention in brass. Cu-Ni-Ce and Al-Ce-Cu are assessed in TCCU7. | 2 |
| [Pr](phase1/el-46-Pr.md) | EXCLUDE | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Nd](phase1/el-47-Nd.md) | LIMIT | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Er](phase1/el-48-Er.md) | EXCLUDE | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Gd](phase1/el-49-Gd.md) | EXCLUDE | exclude | No data in seawater copper alloys; not in TCCU7 (stands in for the heavy lanthanides). | 4 |
| [Pd](phase1/el-50-Pd.md) | EXCLUDE | exclude | Cathodic modification works for titanium and stainless steels, not shown for copper alloys; thousands of dollars per kg (stands in for the platinum group). | 4 |

## Where the decision differs from Edison, and why

The decision differs from Edison's per-element verdict for 11 elements.

**Edison said include; dropped here (four):**
- **Ag:** Edison's "include" rested on one Ag-nanoparticle study in a
  Cu-Al-Ni shape-memory alloy, read through a review, and Edison reversed
  that study's result.
- **Ge:** one heat-treated powder-metallurgy NAB sample whose Mn, Fe and Ni
  also changed. Ge also costs about $1,000-4,000/kg and is under export
  controls.
- **Y:** one cast 90-10 abstract; Y is not in TCCU7.
- **Co:** the specifications count Co with Ni, and the joint answer dropped
  it too.

**Edison said limit; changed here:**
- **Ce becomes an option:** its 0.04 cap came from mischmetal retention in
  brass. Du et al. 2025 (doi:10.1016/j.jmrt.2025.05.090, abstract read)
  found 0.1 La or Ce improved 90-10 in 3.5% NaCl, with La better.
- **Be, Nd, Ga, In and Li are excluded outright:** nothing in the feedstock
  would carry them, and Be is a toxic powder.

**Edison said include; held for Year 2:**
- **Sn:** the only chloride series behind the "include" is a porous sintered
  shape-memory alloy. Sn is an impurity in the target alloys (C63000 ≤ 0.20;
  EN Cu-Ni grades ≤ 0.03-0.05).
- **Zr:** loss on melting, solubility, and no assessed Cu-Ni-Zr.
- **B:** a Ni-B eutectic (about 1,090 °C) below the Cu-30Ni solidus, and
  dosing at 0.5 kg scale.

**Bounds changed from Edison's VERDICT lines:**
- **Ni:** Edison gave 33/35. 35 Ni melts above the 1,250 °C limit, so 33
  is kept only as the box bound, with the liquidus constraint binding.
- **Fe and Al:** Edison mixed the families in one line. The Fe ceiling is
  5.5, not 6 (no commercial NAB has more), and the Al floor of 1.8 came
  from aluminum brass, so 1.5 (MARINEL) is used.
- **Ti:** Edison's VERDICT used NAB numbers. The Cu-Ni range follows the
  ERCuNi filler (0.20-0.50), and NAB is limited to 0.1.
- **Si:** Edison gave 2.0/3.8, from silicon bronze. The target alloys allow
  0.1 (NAB) to 0.5 (cast 70-30), so the range is 0-0.5.
- **C:** Edison's 0.005 had no data behind it; 0.02 is used, with 0.05 (the
  welding-grade limit) as the outer value.

**Joint-answer rules rejected or softened:**
- **"Fe + Mn ≤ 2.5 in Cu-30Ni"** contradicts C71640, which carries up to
  2.3 Fe and 2.5 Mn. The per-element Fe answer found no such rule, so it is
  not used.
- **The aluminum equivalent** was given with a missing Fe coefficient and an
  unverified source (Brezina 1982 was unobtainable). Retained β is left to
  the process-aware CALPHAD node instead.
- **The constraints ANALYSIS suggested halving-type caps** (a 0.25 factor)
  for pairs with no assessed ternary. That would cap Cr at 0.125 wherever Mn
  is present, which rules out C72200. It is listed as an option, not used.

## The two ANALYSIS syntheses

**Constraints ([`phase3/multi-element-constraints.md`](phase3/multi-element-constraints.md)).**
It used the TCCU7 table over the joint answer's guesses, and it marks which
of its numbers are its own policy choices.

- **Three regions:** a Cu-Ni branch (Ni 9-30, Al < 2), a C95800-like NAB
  branch, and a flagged Cu-Ni-Al bridge (Ni 2-25, Al 1.8-5, Fe ≤ 1).
  - **How the space here implements them:** through rules keyed to Al, with
    the same breakpoints (Fe ≤ 2.3 below 1.5 Al, Fe ≤ 1 in the bridge, NAB
    rules above 7 Al).
  - **Where it differs:** the space here does not shrink the NAB branch to
    the C95800 box, since finding a better NAB composition is the point.
- **Repair interfaces land in the bridge.** Its dilution examples, at a
  melted-substrate fraction of 0.3:
  - a Cu-20Ni-1Fe-1Mn deposit on NAB gives a first layer of about
    Cu-15.5Ni-2.7Al-1.9Fe-1Mn;
  - an NAB deposit on C71500 gives about Cu-12.5Ni-6.3Al-3.0Fe.

  Both are between the families. That is a second reason to keep the bridge
  in the space and to test each interface as its own alloy.
- **Adopted from it:**
  - at most 6 active additions;
  - a 0.010 wt% operational dosing floor (B 0.002, from master alloy);
  - the BiE hot-ductility index as a tracked impurity sum;
  - galvanic tests of deposit and substrate couples (see the CubXL note).
- **Not adopted:**
  - **Its partial aluminum index** (Al + 0.25 Mn + Si/6 + 0.5 Sn - Ni/6
    ≤ 9.0). It says itself that the formula is incomplete. It can still
    serve as a cross-check on the CALPHAD prediction of retained β.
  - **The 0.25-factor caps on pairs with no assessed ternary.** They would
    exclude C72200, so they remain an option.
  - **Its tighter impurity targets** (S ≤ 0.005, P ≤ 0.010, C ≤ 0.005). These
    are kept as aims; the limits follow the specifications.
  - **Its preference for a 1,200 °C liquidus in a conservative tier.** The
    atomizer limit is not yet confirmed, so the cap stays at 1,250 °C.

**Palette and bounds table ([`phase2/`](phase2/)).** Still running at the
first push (submitted 19:36 UTC); summarized here once it returns.


## How the answers were checked

Five subagents each read the full answers for a group of elements and wrote
a digest ([`checks.md`](checks.md)). Each digest gives the key numbers and
sources, interactions, red flags, a recommendation, and a Crossref check of
up to three DOIs per element.

- **DOIs:** all checked DOIs matched title, journal and year except three.
  - The Se and Cd answers cite a DOI for a Copper Development Association
    publication that resolves to a 1999 news item.
  - The Er answer cites a Wang 2026 DOI that does not resolve.
- **Errors in Edison's reasoning:**
  - reversed results (Ag);
  - zero-width ranges (Ge, Y, Cr);
  - bounds above solubility (Zr at 0.5);
  - VERDICT lines that mix the two families (Ni, Al, Fe, Ti, B).
- **Checkers' own recollections** of standards are marked as such in the
  digests. The ones the proposal relies on were checked here:
  - C96400 (ASTM B369): Nb 0.50-1.5, Si ≤ 0.5, Pb ≤ 0.010, P and S ≤ 0.020;
  - C71640: Fe 1.7-2.3, Mn 1.5-2.5;
  - the 2025 critical-minerals list: 60 minerals, adding Cu, Ag, Si, Pb, B
    and others.

## The options left open last round

The previous round ([`../cu-ded-2026-10/README.md`](../cu-ded-2026-10/README.md))
ended with optional alloy-space changes and one testing idea. They are now
settled as follows:

- **0-2 wt% Cr in Cu-Ni (C72200-like):** in, at 0-1, Cu-Ni only. The
  evidence is strongest for erosion-corrosion resistance, while still-water
  crevice attack is the risk.
- **Mn-Al bronze as a nickel-lean family:** out for now. At 11-14 Mn it
  loses Mn and gives off Mn fume in melting and DED, and its selective-phase
  corrosion is worse than NAB's. Mn is searched up to 4 instead, which
  covers C71640 (1.5-2.5) and the low end of MARINEL's range (3.8-5.3).
- **Duplex α+β bronzes, to avoid cracking:** inside the space, since Al runs
  to 10.5. The CALPHAD screen along the thermal history (H3) weighs the
  crack resistance of duplex structures against selective attack of β.
- **Reading immersion coupons at about 1, 10 and 30 days:** in the proposal
  now, done by the CubXL. It draws small samples of each immersion solution
  for ICP-MS at about 1, 3, 10 and 30 days, so the metal released over time
  is an intermediate result between the one-hour screen and the 30-day mass
  loss.

## Open items for Sterling

1. **Check the Thermo-Calc license.** Does the BYU license include TCCU,
   and which version? TCCU7 needs Thermo-Calc 2026b. If the license is
   older, the coverage numbers above (TCCU7) are a little better than what
   is available: TCCU6 has 32 elements, 148 binaries and 64 ternaries.
2. **Ni versus the atomizer.** Confirm the induction module's maximum melt
   temperature. If it is lower than 1,300 °C, the liquidus cap drops and
   70-30 leaves the space, which then tops out near 90-10 to 80-20 Cu-Ni
   plus the NAB branch.
3. **Read the full texts behind three numbers:** Du et al. 2025 (rare
   earths), Poojary et al. 2023 (Sn in NAB, doi:10.1038/s41598-023-44146-y),
   and Tuck's MARINEL work (the joint answer's Cu-Ni-Al bridge ranges). The
   checked MARINEL paper is Campbell et al. 2002, doi:10.5006/1.3277305.
4. **An NAB corrosion guideline the checks recalled:** Al ≤ 8.2 + 0.5·Ni
   (attributed to Weill-Couly). Edison did not return a source, so it is not
   used; worth checking against CDA Publication 80.
5. **Mn-Al bronze (C95700, 11-14 Mn) is left out** because Mn evaporates. If
   a Ni-free family is wanted, it could be a later branch.
6. **The missing-ternary pairs (Mn-Cr, Si-Nb, Al-Ti and others)** need early
   CALPHAD-versus-experiment checks before the search leans on them.

## Files

| File | What |
| --- | --- |
| `elements.py` | The 50 elements, groups, and per-element hints |
| `queries.py`, `analysis_prompts.py` | All questions (phases 1-4) |
| `run_elements.py` | Submit, wait, fetch, status |
| `phase1/` | 50 per-element answers and the joint answer |
| `phase2/`, `phase3/` | The two ANALYSIS syntheses |
| `electrochem/` | The two CubXL/potentiostat answers |
| `raw/` | Gzipped raw trajectories |
| `verdicts.md`, `verdicts.json`, `tabulate_verdicts.py` | Edison's VERDICT lines, parsed |
| `tccu7_coverage.py`, `tccu7_coverage.md` | TCCU7 coverage tiers and palette statistics |
| `decisions.py`, `decisions_table.md`, `make_decisions_table.py` | The decision and reason for each element |
| `search_space.py`, `search_space.md`, `search_space_table.tex` | The search space (single source of truth) |
| `checks.md` | Subagent checks of every answer |
| `_task_ids.json` | Task IDs and times |
