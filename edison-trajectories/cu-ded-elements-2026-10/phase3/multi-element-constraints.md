<!--
Edison Scientific ANALYSIS task (phase 3)
- Task ID: 84ef6022-25ed-4bc7-bb59-eea9c9478217
- Submitted: 2026-10-17T19:36:21Z
- Fetched: 2026-10-17T19:48:38Z (status: success)
- Raw trajectory JSON: ../raw/multi-element-constraints.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

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

---

## Multi-element constraints and edge cases

**I recommend a sparse union of a Cu–Ni branch, an aluminum-bronze branch, and a separately flagged Cu–Ni–Al bridge—not an unrestricted continuous simplex.** Below, I distinguish attachment-supported ranges, provisional constraints proposed by the attached answers, and new search-policy choices. None establishes crack freedom or seawater equivalence as deposited.

An editable, expanded version is saved as [multi-element-constraints.md](multi-element-constraints.md). All compositions below are **wt%**, with Cu as balance.

### 1. Simplex, sparsity, and dosing floor

For concentrations \(c_i\), including measured impurities,

\[
c_i\ge0,\qquad c_{Cu}=100-\sum_{i\ne Cu}c_i.
\]

Use the following nested solute budgets:

\[
\begin{aligned}
&Cu\ge65 &&\Longleftrightarrow &&\sum_{i\ne Cu}c_i\le35 &&\text{main search},\\
&Cu\ge60 &&\Longleftrightarrow &&\sum_{i\ne Cu}c_i\le40 &&\text{exploratory Cu–Ni-rich tier},\\
&Cu\ge79 &&\Longleftrightarrow &&\sum_{i\ne Cu}c_i\le21 &&\text{C95800-like branch}.
\end{aligned}
\]

The first two are attachment-proposed design bounds, not specification limits. The C95800-like minimum has a reproduced specification basis. None guarantees meltability or favorable phases. ([el-01-Cu.md](el-01-Cu.md), recommendation and comparator table.)

**Sparsity—my policy choice.** With binary activation variables \(z_i\), encode

\[
z_i f_i\le c_i\le z_iU_i,\qquad k=\sum_i z_i\le6,
\]

and permit **\(k\le7\)** only for explicitly labeled interaction experiments. Cu and incidental impurities do not count; deliberately charged deoxidizers do. These element-count limits are **new experimental-design choices**, not literature-derived limits. They accommodate the Ni–Al–Fe–Mn NAB core plus a small number of probes without activating the entire palette.

**Weighability is not the functional floor.** For the user-specified 0.1 mg weighing increment and the attached 0.5 kg charge,

\[
100\frac{0.0001\ \mathrm{g}}{500\ \mathrm{g}}=0.000020\ \mathrm{wt\%}
\]

per balance increment. The charge size is specified in, for example, [el-03-Al.md](el-03-Al.md); the weighing resolution comes from this task, not an attachment.

| Addition, wt% | Calculated element mass per charge | Balance increments | Interpretation |
|---:|---:|---:|---|
| 0.000020 | 0.1 mg | 1 | Instrument increment only |
| 0.002 | 10 mg | 100 | Attached B screening floor; transfer to Cu–Ni/NAB remains unproven |
| 0.010 | 50 mg | 500 | My default practical dosing floor before applying a functional floor |
| 0.012 | 60 mg | 600 | Attached smallest demonstrated Ti microstructural-effect level |

*Functional-floor sources: [el-19-B.md](el-19-B.md), bounds; [el-13-Ti.md](el-13-Ti.md), bounds. Masses and increment counts are calculations, not reported experiments.*

For ordinary active variables I would use \(f_i=\max(0.010,f_{i,\mathrm{functional}})\), with **0.010 explicitly an analyst-selected operational floor**. A targeted B experiment may retain its **0.002** floor using characterized master alloy and verified retained chemistry; Zr’s attached practical floor is **0.010**. Major solutes retain their higher element-specific functional floors. ([el-19-B.md](el-19-B.md); [el-14-Zr.md](el-14-Zr.md); [verdicts.md](verdicts.md), floor column.)

There is **no apparatus-specific recovery distribution** in the attachments from which to calculate a universal loss-adjusted dosing floor. For element recovery \(r_i\), use

\[
c_{i,\mathrm{powder}}=100r_i m_{i,\mathrm{charge}}/M_{\mathrm{powder}},
\]

then account separately for deposition. Measure charge → melt → size-fractionated powder → deposit chemistry. The approximately **50% Zr loss during an hour of holding** reported in a different copper-casting study is a warning, not a rePOWDER correction factor. ([el-14-Zr.md](el-14-Zr.md), powder-making discussion.)

### 2. Family structure and the bridge

I would begin with these **operational search regions**, not treat them as fully qualified composition boxes:

| Region | Initial rules, wt% | Qualification |
|---|---|---|
| **Cu–Ni main branch** | \(9\le Ni\le30\), \(0\le Al<2\); no intentional Al in baseline controls | The lower Ni endpoint is anchored to C70600. The upper endpoint is a practical initial cap, subject to liquidus. Any active Al triggers additional bridge checks. |
| **NAB-centered aluminum-bronze branch** | \(8.5\le Al\le9.5\), \(4\le Ni\le5\), \(3.5\le Fe\le4.5\), \(0.8\le Mn\le1.5\), \(Cu\ge79\), \(Ni>Fe\) | A C95800-like starting region—not the entire aluminum-bronze family. The Mn lower endpoint is the grade precedent, rather than an isolated-effect floor. |
| **Cu–Ni–Al bridge: exploratory** | \(2\le Ni\le25\), \(1.8\le Al\le5\), \(Fe\le1\); initially \(Mn\le1.5\), with a flagged extension to \(Mn\le4.4\) | A research region assembled from attachment precedents and provisional bounds. Its rectangular extent and seawater performance are not established. |

*Endpoint sources: [el-01-Cu.md](el-01-Cu.md), comparator table; [el-02-Ni.md](el-02-Ni.md), bounds; [el-03-Al.md](el-03-Al.md), bounds; [el-05-Mn.md](el-05-Mn.md), bounds; [joint-shortlist.md](joint-shortlist.md), §§3c and 4. The Al = 2 organizational marker is suggested by the joint answer, not a phase boundary.*

The bridge is worth searching, but **not by assuming interpolation of corrosion performance**. The joint answer identifies **Cu–7Ni–3Al** and MARINEL-type compositions around **15–25 Ni, 1.6–2.3 Al, 3.8–5.3 Mn, 0.6–1.2 Fe, 0.6–0.9 Nb, and 0.35–0.48 Cr**, Cu balance. These are reported precedents, not an as-deposited qualification window. Several exceed the conservative rules proposed here and should be separately flagged exceptions. ([joint-shortlist.md](joint-shortlist.md), §4.)

I would not automatically fill the **5–8.5 Al** gap or import the **10.5 Al** exploratory bronze ceiling into the main region. Lower-Ni aluminum bronzes and intermediate-Al compositions deserve targeted extensions with phase maps and corrosion tests. The detailed Al answer explicitly labels its Cu–Ni–Al limits provisional; the joint answer’s proposed “blending” supplies no numerical blending law. ([el-03-Al.md](el-03-Al.md), bounds; [joint-shortlist.md](joint-shortlist.md), §4.)

### 3. Sum, ratio, and phase constraints

#### Aluminum equivalent: incomplete evidence

The joint answer proposes

\[
Al_{eq}=Al+\tfrac14Mn+\tfrac16Si+\tfrac12Sn-\tfrac16Ni-a_{Fe}Fe,
\qquad Al_{eq}\le9.0\quad\text{or exploratorily}\quad\le9.4.
\]

However, it does **not specify \(a_{Fe}\)**, supplies no Zn coefficient, and acknowledges that the precise formula was not verified. The detailed Al answer warns that **9.4 is a binary screening warning, not a fixed multicomponent NAB transition**. I would not invent the missing coefficients or present this as a validated Brezina equation. ([joint-shortlist.md](joint-shortlist.md), §3a; [el-03-Al.md](el-03-Al.md), phase discussion and interactions.)

If numerical triage is required before resolving that gap, I would use the explicitly **partial, no-Fe-credit index**

\[
A^*=Al+0.25Mn+\tfrac16Si+0.50Sn-\tfrac16Ni\le9.0,
\]

with **\(9.0<A^*\le9.4\)** restricted to exploratory trials. This is **my operational use of the joint answer’s proposed coefficients**, not a verified aluminum equivalent or proof of conservatism. It gives no favorable Fe credit or quantitative Zn correction; use no intentional Zn in this bronze screen. Resolve retained β/β′, γ, and κ using equilibrium/Scheil calculations and actual deposited microstructures. ([joint-shortlist.md](joint-shortlist.md), §3a; [el-03-Al.md](el-03-Al.md), interactions.)

#### Family-conditioned inequalities

| Interaction | Numerical rule, wt% | Evidence and limitation |
|---|---|---|
| **NAB Fe–Ni/κ package** | \(3.5\le Fe\le4.5\), \(4\le Ni\le5\), \(Fe/Ni<1\); consequently \(7.5\le Fe+Ni\le9.5\) | The preferred approximate **Fe/Ni = 4/5 = 0.8** is an attachment-reported anchor, not a universal optimized ratio. The sum is an arithmetic consequence, not a separate phase boundary. NiAl- and Fe₃Al-related κ morphology matters, not simply total κ. ([el-03-Al.md](el-03-Al.md), §1; [joint-shortlist.md](joint-shortlist.md), §3b; [el-04-Fe.md](el-04-Fe.md).) |
| **Cu–Ni Fe and Mn** | 90/10-like: \(Fe\le1.8\). 70/30-like: \(Fe\le1.0\), preferably \(0.4\le Fe\le0.7\). Exploratory only: \(Fe\le2.0\). Initially \(Mn\le1.5\); near 70/30 use provisional \(Fe+Mn\le2.5\). | **Fe must remain available in the Cu–Ni matrix.** The 2.5 sum is a joint-answer proposal, not a demonstrated solubility surface or DED reheat threshold; the detailed Fe answer explicitly finds no validated universal Fe+Mn rule. ([el-01-Cu.md](el-01-Cu.md), comparator table; [el-04-Fe.md](el-04-Fe.md), bounds; [el-05-Mn.md](el-05-Mn.md), bounds; [joint-shortlist.md](joint-shortlist.md), §§3c–d.) |
| **Bridge Fe** | \(Fe\le1.0\) | A provisional SCC-oriented screen—not permission to transfer the NAB Fe package into a Ni-rich bridge. ([joint-shortlist.md](joint-shortlist.md), §3c.) |
| **Cr–Fe–Si in Cu–Ni** | \(Cr>0.3\Rightarrow Fe\ge0.5\ \land\ Si\le0.5\). Initially also \(Cr\le0.5\), \(Si\le0.30\). | The implication is a **joint-answer proposal**, not a validated boundary. The detailed Cr comparator is approximately **15 Ni–0.8 Fe–0.5 Cr**; that answer finds no universal Cr+Fe or Cr/Ni limit. ([joint-shortlist.md](joint-shortlist.md), §3e and table; [el-06-Cr.md](el-06-Cr.md), evidence table/interactions.) |
| **Mn replacing Ni** | Main \(Mn\le1.5\); exploratory \(Mn\le4.4\), without relaxing the branch’s Ni floor | No defensible \(Ni+aMn\ge b\) replacement rule exists in the attachments. Approximately **4.4 Mn–4.7 Ni** gave **83.2 µm/year**, versus **25.6 µm/year** for binary **4.4 Mn**, in a short chloride test—not long-term repair qualification. ([el-05-Mn.md](el-05-Mn.md), §§2 and 5.) |
| **Nb–Si weldability edge** | Assess \(Nb-1.55Si+0.10>0\); separately, the stricter historical alternative is \(Nb\ge2Si\). | These are different cast-Cu–Ni rules, not interchangeable DED qualifications. With **Nb ≤0.80**, the stricter rule implies calculated **Si ≤0.40**; with the joint shortlist’s **Nb ≤0.50**, it implies **Si ≤0.25**. ([el-10-Nb.md](el-10-Nb.md), §6; [joint-shortlist.md](joint-shortlist.md), table.) |

For C95800-like chemistry, also retain the joint table’s **\(Si\le0.10\)** rather than importing the much higher palette-wide Si verdict into NAB. ([joint-shortlist.md](joint-shortlist.md), composition table.)

#### Total solute versus liquidus

There is no attachment-supported linear “total solute → liquidus” equation. Apply both the simplex budgets and

\[
T_L(\mathbf c)\le1250\ ^\circ\mathrm C,
\quad T_{operating}-T_L\ge\Delta T_{required},
\quad T_{operating}\le1300\ ^\circ\mathrm C.
\]

I would prefer **\(T_L\le1200\ ^\circ\mathrm C\)** for the conservative tier. The required superheat remains experimentally determined. The nominal module ceiling leaves calculated headrooms of **50 °C** and **100 °C**, respectively—not guaranteed usable superheat. Check **complete dissolution of refractory particles**, not first melting. ([el-02-Ni.md](el-02-Ni.md), §4; [el-03-Al.md](el-03-Al.md), §4; [el-06-Cr.md](el-06-Cr.md), powder-making discussion.)

The joint answer reports approximately **1240 °C at 30 Ni**, but the detailed Ni answer declines a universal Ni cutoff. Thus initial **Ni ≤30** does not replace full-composition calculations or justify atomization of **33–35 Ni** simply because those verdict maxima exist. ([joint-shortlist.md](joint-shortlist.md), §3g; [el-02-Ni.md](el-02-Ni.md), thermodynamics/bounds; [verdicts.md](verdicts.md), Ni row.)

#### Impurity sums: no compensating allowances

The joint answer proposes

\[
Pb+Bi\le0.015,\qquad S+P\le0.020,\qquad
Pb+S+P+C+Bi\le0.050.
\]

These are provisional welding-derived targets—not demonstrated DED crack thresholds. Retain the following individual controls simultaneously:

| Impurity | Initial limit, wt% | Source and scope |
|---|---:|---|
| Pb | \(\le0.010\) | [el-23-Pb.md](el-23-Pb.md), stricter welding-derived screen |
| S | \(\le0.005\) | [el-27-S.md](el-27-S.md), stricter operational target rather than its 0.010 outer screen |
| P | \(\le0.010\) | [joint-shortlist.md](joint-shortlist.md); the detailed [el-22-P.md](el-22-P.md) instead proposes 0.020, or 0.015 for Al bronze |
| C | \(\le0.005\) | [el-32-C.md](el-32-C.md), engineering screening cap |
| Bi | \(\le0.001\) | [el-24-Bi.md](el-24-Bi.md), Cu–Ni hot-workability-derived screen; Sn-rich variants warrant its tighter 0.0004 target |
| Se | \(\le0.006\) | [el-25-Se.md](el-25-Se.md), provisional Cu–Ni-derived screen |
| Te | \(\le0.003\) | [el-26-Te.md](el-26-Te.md), hot-workability-derived screen |

*Joint-sum source: [joint-shortlist.md](joint-shortlist.md), §3h. None of the individual limits guarantees crack-free DED.*

These individual caps imply the calculated envelopes

\[
Pb+S+P+C+Bi+Se+Te\le0.040,
\qquad Se+Te\le0.009.
\]

Those are arithmetic consequences, **not measured synergistic limits**. Low P/S does not license excessive Pb/Bi; Mn, Ti, or rare earths receive no impurity-neutralization credit. ([el-23-Pb.md](el-23-Pb.md), interactions; [el-24-Bi.md](el-24-Bi.md), joint constraints; [el-25-Se.md](el-25-Se.md), joint constraints.)

The S answer also reports the empirical simple-Cu–Ni hot-ductility index

\[
BiE=Bi+0.7Te+0.4Pb+0.2Se+0.1S.
\]

Its linear form permits all inputs and output to be expressed in wt%. At the caps above, calculated **\(BiE\le0.0088\)**. This is **not a literature safe threshold**: the attachment cautions against quantitative transfer to complex precipitation-hardened alloys, and the index excludes P and C. ([el-27-S.md](el-27-S.md), welding discussion.)

### 4. TCCU7 coverage guardrails

I prioritize **[tccu7_coverage.md](tccu7_coverage.md)** over the joint answer’s speculative coverage statements. For the shortlist with Ce rather than Y, the following Cu-containing ternaries are explicitly **not assessed**:

| Palette element X | Core partners Y lacking assessed Cu–X–Y |
|---|---|
| Cr | Al, Mn |
| Nb | Al, Fe, Mn |
| Ti | Al, Fe, Mn, Cr |
| Zr | Ni, Al, Fe, Mn |
| B | Ni, Al, Fe, Mn, Cr—and every other partner, because B has no assessed Cu-containing ternary |
| Ce | Fe, Mn, Cr |
| Sn, Si | None of the listed core partners |

*Source: [tccu7_coverage.md](tccu7_coverage.md), element rows and core-pair list. Missing ternary assessment does not necessarily mean a missing X–Y binary.*

Important distinctions:

- Al–Cr has an assessed binary but no assessed Cu–Al–Cr; Mn–Cr lacks both listed assessments.
- Cu–Ni–Nb and Cu–Ni–Ti **are assessed**; Cu–Ni–Zr is not. Cu–Cr–Nb and Cu–Cr–Zr are assessed.
- Cu–Al–Ce is assessed, but **Y is absent from TCCU7**. For La, Cu–La–Ni and Cu–La–Cr are assessed; its Al/Fe/Mn core ternaries are not.
- The table does **not identify every minor–minor pair**. Except for B’s zero-ternary case, counts alone cannot establish the status of Cu–Nb–Ti, Cu–Sn–Zr, or similar pairs. Treat these as **coverage unknown**, not automatically assessed or absent.
- H, N, and Te are absent; Bi, B, and Se have no assessed Cu-containing ternaries. Metallic CALPHAD screening therefore cannot replace gas/impurity controls.

All coverage statements above come from [tccu7_coverage.md](tccu7_coverage.md). Assessed ternaries also do not establish assessed higher-order interactions or validate every relevant phase model.

**Joint caps—explicitly new policy.** No attachment supplies concentration caps calibrated to missing assessments. To limit high–high extrapolation, I propose for each known-missing pair, and provisionally each coverage-unknown pair,

\[
z_X=z_Y=1\Rightarrow
\min\!\left(\frac{c_X}{U_X},\frac{c_Y}{U_Y}\right)\le0.25.
\]

The **0.25 factor is my precautionary search-policy choice**, not a thermodynamic limit. Reference scaling ceilings \(U_i\), all wt%, are **Ni 30, Al 9.5, Fe 4.5, Mn 1.5, Cr 0.50, Sn 1.0, Si 0.30, Nb 0.50, Ti 0.10, Zr 0.15, B 0.020, Ce 0.040**; tighter branch rules still prevail. Sources: [joint-shortlist.md](joint-shortlist.md), table; stricter Mn/Cr/Ti values from [el-05-Mn.md](el-05-Mn.md), [el-06-Cr.md](el-06-Cr.md), and [el-13-Ti.md](el-13-Ti.md); Ce’s provisional residual cap from [el-45-Ce.md](el-45-Ce.md). Ce is an optional controlled probe/residual here, not an endorsed main-search addition.

When the other partner exceeds one-quarter of its reference ceiling, this gives calculated conditional caps:

| Missing-pair example | Conditional cap, wt% |
|---|---:|
| Cr with substantial Al/Mn | \(Cr\le0.125\) |
| Nb with substantial Al/Fe/Mn | \(Nb\le0.125\) |
| Ti with substantial Al/Fe/Mn/Cr | \(Ti\le0.025\) |
| Zr with substantial Ni/Al/Fe/Mn | \(Zr\le0.0375\) |
| B with a substantial partner | \(B\le0.005\) |
| Ce with substantial Fe/Mn/Cr | \(Ce\le0.010\) |

These are the cited reference ceilings multiplied by the **new policy factor**, not measured phase boundaries. If a cap falls below a functional floor, **turn that addition off in the main search** rather than claiming the smaller dose retains its documented function. Cr–Mn and Nb–Al recipes may therefore require targeted, experimentally validated exceptions. This policy reduces extrapolation exposure; it does not make extrapolated predictions reliable.

### 5. Atomization and DED edge cases

| Edge case | Constraint or control |
|---|---|
| **Zn volatility** | No intentional Zn; provisional \(Zn\le0.50\). Approximately **43 Zn** powder yielded **35.46 Zn** in infrared LPBF—a different composition/process, not a dilute-Zn DED correction. Lower liquidus does not solve vaporization, fume, porosity, or dezincification. ([el-08-Zn.md](el-08-Zn.md), deposition/powder discussion and bounds.) |
| **Mn loss** | Retain family-conditioned caps; assay melt-to-powder and powder-to-deposit recovery. The attachments provide a volatility/oxidation warning but **no numerical apparatus-specific loss fraction**. ([el-05-Mn.md](el-05-Mn.md), §3.) |
| **Mg loss/reactivity** | No intentional Mg variable; provisional \(Mg\le0.010\). Late Mg deoxidation is a Cu–Ni processing precedent, not a seawater benefit; Al-bronze ductility concerns and unquantified recovery argue against routine use. ([el-16-Mg.md](el-16-Mg.md), decision and powder-making discussion.) |
| **Reactive solutes and hardware** | Al, Ti, Zr, B, and rare earths require retained-element/inclusion assays. Do not assume alumina, zirconia, Ti-alloy tips, or Mo tips are inert. Blank-test each pairing and assay Al/Zr/Ti/Mo/O/C. Graphite contact can consume Ti into TiC and B into carbide particles. Observed carbon-fiber/ceramic contamination in another ultrasonic bronze study does not quantify contamination from the proposed sonotrodes. ([el-03-Al.md](el-03-Al.md), §4; [el-13-Ti.md](el-13-Ti.md), §3; [el-14-Zr.md](el-14-Zr.md), §4; [el-19-B.md](el-19-B.md).) |
| **Oxygen and moisture** | Provisionally require \(O_{powder}\le0.013\), \(O_{deposit}\le0.013\), preferably **0.005** where achievable; independently screen \(H\le0.0001\) and \(N\le0.0005\). These are attachment-proposed controls, not universal DED thresholds. Argon and oxygen-free charge do not exclude oxide entrainment or steam porosity. ([el-29-O.md](el-29-O.md), constraints; [el-30-H.md](el-30-H.md), bounds; [el-31-N.md](el-31-N.md), bounds.) |

Gettering transfers oxygen into oxide/dross/inclusions unless products are removed; low calculated dissolved O is not proof of clean powder. The O answer specifically states that Mn/B cannot reduce existing alumina films. Measure powder oxygen by size fraction and deposited oxygen separately. An oxide-related infrared-absorption benefit cannot substitute for density, cracking, or seawater qualification. ([el-29-O.md](el-29-O.md), interactions and LPBF counterexample.)

### 6. Repair dilution and galvanic pairing

Treat the mixed zone as a separate alloy. For melted-substrate **mass fraction** \(d\),

\[
c_{i,mixed}(d)=(1-d)c_{i,deposit}+dc_{i,substrate},\qquad0\le d\le1.
\]

Geometric dilution requires appropriate conversion before use as \(d\). This relation neglects selective loss and segregation; replace predictions with measured traverses. Dilution need not be equal on the two substrates. ([el-03-Al.md](el-03-Al.md), repair discussion.)

The following are **calculated illustrations**, not reported repair experiments, using my selected **\(d=0.30\)**:

| Material or zone | Cu | Ni | Al | Fe | Mn |
|---|---:|---:|---:|---:|---:|
| Illustrative Cu–Ni powder | 78.00 | 20.00 | 0 | 1.00 | 1.00 |
| Nominal NAB substrate/powder | 81.00 | 5.00 | 9.00 | 4.00 | 1.00 |
| Nominal C71500 substrate | 69.50 | 30.00 | 0 | 0.50 | 0 |
| **Cu–Ni on NAB: mixed zone** | **78.90** | **15.50** | **2.70** | **1.90** | **1.00** |
| **NAB on C71500: mixed zone** | **77.55** | **12.50** | **6.30** | **2.95** | **0.70** |

*All compositions are wt%. Nominal NAB/C71500 inputs: [el-01-Cu.md](el-01-Cu.md), comparator table. The Cu–Ni feed and dilution fraction are illustrative analyst inputs; mixed-zone values use the relation in [el-03-Al.md](el-03-Al.md).*

Thus Al-free Cu–Ni deposited on NAB can create an Al-bearing first layer outside the proposed bridge Fe cap, even though its undiluted feed passes. NAB on C71500 can enter the deliberately unsampled intermediate-Al region. **Leaving a nominal grade box triggers separate interface qualification, not automatic rejection or acceptance.** Sweep plausible dilution paths, including uncertainty, through phase/freezing-range checks; inspect the fusion boundary, substrate heat-affected zone, reheated layers, and top deposit separately. Cast β/κ remelting and wrought-substrate thermal changes are not captured by bulk powder chemistry. ([el-02-Ni.md](el-02-Ni.md), repair discussion; [el-03-Al.md](el-03-Al.md), repair discussion; [el-05-Mn.md](el-05-Mn.md), repair discussion.)

**Galvanic compatibility must be tested.** The attachments establish no universal deposit–NAB or deposit–Cu–Ni potential-difference cutoff, fixed anodic member, or acceptable exposed-area ratio. NAB’s susceptible phase can change with local pH; air-measured phase nobility need not match chloride attack. ([el-03-Al.md](el-03-Al.md), corrosion discussion.)

I would add coupled deposit/substrate exposures at the intended exposed-area ratio, with uncoupled controls and matched surface preparation/film aging. Measure coupled current where feasible and resolve attack on the deposit, interface, and substrate/heat-affected zone. The acceptance objective is that the **deposit and repair couple meet the matched wrought-C71500 comparison in the specified 30-day exposure**, including maximum selective-attack depth—not merely favorable isolated open-circuit potential or polarization resistance. The attached Cr answer explicitly treats electrochemical screens as supporting diagnostics rather than substitutes for immersion-depth comparison. ([el-06-Cr.md](el-06-Cr.md), acceptance gate.)

**Discretionary analytical decisions**

- I use family-conditioned branches plus an exploratory bridge because Fe’s desired state and Al-bearing phase risks change across families; the attachments provide no validated blending law.
- I select sparsity and practical dosing policies explicitly, rather than claiming attachment-derived element-count or induction-loss limits.
- I prioritize detailed per-element qualifications over unedited verdict maxima, and explicit TCCU7 coverage over speculative database statements.
- I retain provisional sum/ratio rules as screens, expose the incomplete aluminum-equivalent equation, and do not invent missing coefficients or a Mn-for-Ni exchange rate.
- I introduce missing-ternary joint caps only as precautionary search restrictions, with targeted exceptions where they conflict with functional floors or useful bridge precedents.
- I distinguish analyzed powder, deposited bulk, and mixed zones. The dilution examples are calculations; I have not performed CALPHAD, deposition, or corrosion experiments.
