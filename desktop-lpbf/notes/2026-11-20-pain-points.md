<!-- Collected 2026-11-20 by a research subagent of the Claude session on PR #266 (issue #260). Every item has its source inline; SE marks a figure seen only in a search-engine extract. No other repo file was edited. -->
# Pain points from machines like this one, and what each means for the design

Written 2026-11-20 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260). The question:
what has gone wrong in home-built, academic and small commercial LPBF machines, and in the equipment this design borrows from
(polymer SLS, gloveboxes, vacuum chambers, fiber-laser markers, powder handling, heated beds, machine tending), and what check
or change does each lesson imply for the low-profile design in [`low-profile.md`](../low-profile.md),
[`modules.md`](../modules.md), [`hot-swap.md`](../hot-swap.md) and [README](../README.md) §2–3?

| File | What it is |
|---|---|
| [`pain-points.csv`](pain-points.csv) | 59 rows: id, domain, pain point, what happened (with numbers), root cause, source URL(s), implication for this design, design element, recommended check or change, severity, likelihood, score (S × L), evidence type |
| this note | the same items grouped by domain (§4), the ranked top 15 (§2), the severe-but-unlikely ones (§3), where web anecdotes and the literature agree or disagree (§5), what the design already handles (§6) and the gaps (§7) |

Conventions:
- **Severity (S)**: 1 nuisance; 2 rework or delay; 3 failed builds, downtime or misleading data; 4 equipment damage or injury potential; 5 serious injury, fire or explosion.
- **Likelihood (L)** for the design as drawn on 2026-11-20: 1 remote; 2 unlikely; 3 possible; 4 likely; 5 near-certain without the change.
- **Evidence**: *read* = we opened the page or PDF. **SE** = seen only in a search-engine extract, because the page blocked us
  (403, bot wall, login wall); check it before relying on it. *Via Edison* = taken from the two Edison literature reviews in
  this repo ([lab-built lessons](../edison/followup-lab-built-lessons/answer.md), [design review](../edison/followup-design-review/answer.md)),
  which cite the paper and page; the DOIs below are theirs. *Anecdotal* = a user forum or a hobby build.
- Forum posters and staff of companies are not named. *(calc)* is our arithmetic.
- Nothing here has been reviewed by BYU's LSO or EHS.

## 1. Summary

- **59 pain points.** 57 rest on external sources (99 distinct URLs, 20 of them DOIs); P52 and P57 are derived from this
  repo's own numbers (P57 also cites the literature). 23 rows lean partly on search extracts, 14 on the Edison reviews,
  3 on forum or hobby reports.
- **By domain:** home-built, open and academic LPBF 7; commercial and research LPBF process, optics, gas flow and alloys 11;
  polymer SLS 4 (plus P13, listed with the window items in §4.2); gloveboxes and gas sensing 2; vacuum, seals and gas supply 8; lasers,
  optics and laser safety 5; powder fires and explosions 7; heaters and their control 4; motion, powder handling, automation
  and controls 9; argon and fire in a VLM 2.
- **Three patterns stand out:**
  1. **The weak parts are the ones that cross the chamber wall or live in the powder:** PTFE V-ring shaft seals that see a
     full atmosphere at every purge (P26), the recoater ball screw and rail inside the chamber (P45), bore seals (P16, P17),
     a magnetic Z coupling that seal drag can pull apart (P57), and vents nobody has drawn for the under-piston void and the
     reservoir headspace (P28).
  2. **The cover slide and the gas flow are where the process is soft.** A fouled fused-silica slide shifts focus by
     −22 to −30 mm at 400 W (Bonhoff) against our ±3.7 mm Rayleigh range (P12); 2 m/s cross-flow is the published
     threshold for porosity, not a margin (P54); a centre-only power check misses uneven fouling (P13).
  3. **The metal-AM fire record is about cleaning and filters, not printing:** Ti soot that ignited under an ATEX vacuum
     (P35), water on Al filter dust that killed two people at an LPBF machine maker (P34), Powderpart (P37). Putting the
     machine in a VLM adds two of its own: argon and fire inside an enclosed tower (P50, P51).

## 2. Top 15 changes and checks, ranked by severity × likelihood

Ties are broken by severity, then by strength of evidence, then by how specific the finding is to this design.

| Rank | Id | Change or check | Design element | S × L |
|---|---|---|---|---|
| 1 | P12 | Trial an athermal (N-FK51A-type) cover slide against fused silica; watch the slide with a camera or transmission photodiode and change it on a coverage limit; purge the camera and photodiode ports | cover slide, gas knife, lid ports | 4 × 4 = 16 |
| 2 | P26 | Replace the PTFE V-ring packing on the recoater and metering-roller shafts with magnetic-fluid feedthroughs or magnetically coupled drives | shaft feedthroughs | 4 × 4 = 16 |
| 3 | P45 | Get the recoater ball screw and rail out of the powder: outside the envelope, or in a housing with a slot seal and argon flowing outward | recoater axis (M1) | 4 × 4 = 16 |
| 4 | P35 | Passivate condensate (slow air bleed with a liner thermocouple watched, or an oil wipe) before any vacuuming; clean liners outside on a grounded tray; earth people and tools | liners, cleaning SOP | 5 × 3 = 15 |
| 5 | P08 | Detect every recoater strike (servo torque, layer camera), flag it in the dataset, and lay coupons out so one strike can't streak the rest | blade, layer camera, dataset | 3 × 5 = 15 |
| 6 | P14 | Measure the built coupon's composition for each parameter set; expect faster slide and filter fouling with Mg- and Zn-rich alloys | dataset, slide, HEPA | 3 × 5 = 15 |
| 7 | P05 | Dielectric HR mirrors on Si or SiC rated ≥ 500 W CW; a scan-head temperature limit; baffle and air-cool the beam path | scan head, beam tube | 4 × 3 = 12 |
| 8 | P30 | Get IPG's back-reflection rating and trip behaviour in writing; offset the plate from the optical axis or tilt window and slide 2–3°; a gentler first layer on bare plates | laser, plate position, window | 4 × 3 = 12 |
| 9 | P57 | Measure the piston's real position each layer and fault on a missed step; test magnet pull against seal break-out hot and with powder; move to a positive coupling | Z coupling, bore seal, rod gland | 4 × 3 = 12 |
| 10 | P42 | Retain every cartridge heater and thermocouple mechanically (they enter from below); add runaway checks in the supervisor | heater block | 4 × 3 = 12 |
| 11 | P41 | Put the CN708 limit relay (or its contactor) in series with the SSR output for every cartridge; proof-test it each campaign; sense heater current | heater supply | 4 × 3 = 12 |
| 12 | P54 | Design for ≥ 2.5 m/s measured over the whole usable plate (headroom to ~4 m/s), map it before first builds, find each powder's pick-up limit | cross-flow, blower | 3 × 4 = 12 |
| 13 | P02 | First-layer gap ≥ 2 × D90 and stepped down; pause on a torque spike; breakaway blade holder; keep a compliant cartridge | blade, holder, servo | 3 × 4 = 12 |
| 14 | P28 | Give the under-piston void and each reservoir headspace a filtered vent; soft-pump and soft-vent valves | module, reservoirs, pump valve | 3 × 4 = 12 |
| 15 | P47 | Adjustable slot, steeper walls and a small agitator on the reservoirs; test each powder's flow after a simulated VLM transit | reservoirs, roller | 3 × 4 = 12 |

**Next tier (also 12):** P06 schedule and O2-first commissioning, P07 monthly health battery, P11 ΔP and flow on the loop,
P13 multi-point power through the slide, P17 seal-life tracking, P18 short-feed abort, P22 virtual leaks and porous parts,
P23 O-ring grooves that hold their rings, P29 pump inlet trap, P44 thermal cutoff run too close to its rating, P49 load cell
across a pressure boundary.

## 3. Severe but unlikely: S = 5, L = 2

These rank below the top 15 only because they are rare; most fixes are cheap SOP or wiring items.

| Id | Hazard | Check |
|---|---|---|
| P10 | condensate filter fire on opening the HEPA housing | controlled passivation with a thermocouple on the housing; two people; sand |
| P33 | eye injury during alignment or with a beam assumed off | no open-beam work above Class 3R without an LSO-approved SOP; guide-laser or < 1 W alignment into a dump |
| P34 | hydrogen from water on Al dust | no water at the machine: drop the chilled-water line from the dock; choose the cleaning vacuum with EHS |
| P37 | Powderpart-type fire: lone work, dust left in collectors, shop vac | empty the overflow every build; no lone cleaning; no shop vacs; tell the fire marshal what is stored |
| P46 | interlocks defeated because the 50 °C cool-down blocks work | coded guard-lock switch; show why the door is locked and for how long; log lock events |
| P50 | argon pooling inside the VLM | duct relief and pump exhaust out of the VLM; auto shut-off at the dock; low-level O2 monitors in the bay |
| P51 | an Al fire inside an enclosed VLM, met by water or nitrogen | ask EHS and the VLM vendor; limit powder on the tray; smoke or heat sensor inside the guard |
| P53 | an interlock fitted in the wrong place | proof-test every interlock at commissioning and after any panel change |

## 4. The pain points, by domain

### 4.1 Home-built, open and academic LPBF

- **P01 · Polymer or elastomer blade edges die on hot metal** (S2 × L3; anecdotal). A hobbyist's 500 W fiber + galvo SLM
  build: a printed-plastic blade with a silicone-cord edge was damaged scraping over freshly fused metal; a stainless blade
  gave "much more consistent performance" ([Hackaday 2026](https://hackaday.com/2026/01/03/printing-in-metal-with-diy-slm)).
  *For us:* the FKM or silicone-cord option runs over a 200 °C plate plus fresh tracks far above FKM's 204 °C rating.
  *Do:* keep HSS as default; elastomer only on unheated, curl-prone trials, inspected after each build; a carbon-fibre brush
  is the compliant option at 200 °C.
- **P02 · A rigid spreader jams when the gap is smaller than the coarse powder** (S3 × L4). Heriot-Watt: tungsten-carbide
  knives and cylinders 50 µm above the plate "jammed by the build-up of particles between the rigid spreader and the build
  plate"; a 3 mm silicone cord replaced them, and the ~10 mm/s spreader then dominated the ~1.5 h build of 5 mm cubes
  ([Bidare et al. 2017](https://doi.org/10.1016/j.addma.2017.06.007), read via [SHURA](https://shura.shu.ac.uk/33282/)).
  Rigid ceramic blades leave collision and rebound marks; compliant rubber imposes little stress even with the gap closed
  ([Skácelík et al. 2026](https://doi.org/10.1007/s00170-026-18515-6), via Edison). *For us:* the HSS blade runs 0.05 mm
  above plate and floor with 15–63 µm powder, Heriot-Watt's failing case, and the stiffened holder won't yield. *Do:* see
  top 15, rank 13.
- **P03 · The effective layer is not the Z step for the first layers** (S2 × L5). Bidare et al. eq. 1: layer 1 equals the
  spreader height; later layers converge to z-step ÷ consolidation fraction. *For us:* 30 µm steps give ~60 µm steady
  layers *(calc)*; 15 mm coupons have a transient base, and the 1.8 dose factor assumes the steady state. *Do:* build on a
  1–2 mm sacrificial base; record effective layer thickness; calibrate dose at steady state.
- **P04 · Opening a chamber that is still inert; optics on a flexing chamber** (S3 × L3). NIST AMMT decoupled its optics
  tower because "pulling vacuum on the chamber will cause it to deflect", and its door sign turns green "only after the oxygen
  level reaches above 19.5%" ([Lane et al., SFF 2016](https://utw10945.utweb.utexas.edu/sites/default/files/2016/093-Lane.pdf), read).
  *For us:* the bridge already stands on its own posts. The unload sequence (modules.md §4) vents and unlocks without saying
  with what gas, and the trace analyzer can't read 19.5 %. *Do:* vent through a slow dry-air bleed and add a percent-range
  O2 cell as an unlock permissive.
- **P05 · Scattered and back-reflected light overheats scan-path mirrors** (S4 × L3; via Edison). AMMT: after 7 min at 60 %
  of 500 W, the fused-silica fold mirror measured 220.2 °C (~275 °C after emissivity correction) and its protected-silver
  coating failed, while the SiC scanner mirrors stayed at 82.7 and 58.7 °C; scatter also heated an anodized mount
  ([Grantham et al., SPIE 2016](https://doi.org/10.1117/12.2214246)). *Do:* rank 7.
- **P06 · A from-scratch LPBF takes person-years, and O2 dominates quality** (S3 × L4; SE). DTU's open-source OpenAM-PBF
  is reported at 38 man-years ([AM Media](https://additivemanufacturing.media/articles/the-downloadable-metal-3d-printer));
  a DTU digital-twin study ranked chamber O2 the largest single effect on quality and gas speed the smallest
  ([DTU, 2021](https://digitalscience.forskningsportal.dk/display/pub.1136951789)). *For us:* a semester plan with a
  go/no-go. *Do:* keep the commercial fallback; commission leak-tightness and O2 first; reuse OpenAM's safety design.
- **P07 · Machine health drifts unless it is tested on a schedule** (S3 × L4). Kansas City NSC's battery: power, position,
  caustic, gas flow at several points including under the windows, elevator accuracy and inerting time; poor focus can cut
  delivered intensity without showing in a power test ([Hilton & Gray, SFF 2022](https://utw10945.utweb.utexas.edu/sites/default/files/2022/Machine%20Health%20Verification%20Process%20for%20Laser%20Powd.pdf), read).
  *For us:* months of screening data will read drift as alloy effects. *Do:* a monthly battery logged with every build.

### 4.2 Commercial and research LPBF: process, optics, filters, alloys

- **P08 · Recoater strikes on curled or super-elevated edges** (S3 × L5). On a One Click Metal MPrint+, collisions with
  spatter elevations, warped overhangs or heat-induced build-up damaged blades, delaminated parts or ended builds, and were a
  primary cause of build loss ([Friedo et al., AALE 2026](https://doi.org/10.33968/2026.29), via Edison). Xact Metal users
  call "recoated bumps and cracking" significant problems ([3DPrint.com](https://3dprint.com/312830/xact-metal-adds-panoptimization-simulation-to-low-cost-metal-3d-printing/)).
  UniBw: damaged lips leave stripes that hit neighbouring parts ([Brenner et al. 2022](https://www.unibw.de/mb/institute/we1/we14/veroeffentlichungen/2022/2022-nr1));
  AlSi10Mg specimens from crashed builds kept strength and hardness but lost elongation ([2023](https://link.springer.com/article/10.1007/s40964-023-00471-2), SE).
  *For us:* screening runs coupons off-window on purpose. *Do:* rank 5.
- **P09 · A notched hard blade streaks and fails builds** (S3 × L3). EDM-notched HSS blades: the build failed at the largest
  notch, with local deviations up to 0.46 mm and a bead caught in a notch ([Massey & Saldaña, SFF 2024](https://utw10945.utweb.utexas.edu/sites/default/files/2024/103%20On%20the%20Nature%20of%20Recoater%20Damage%20Powder%20Spread.pdf), read).
  *Do:* image the blade edge at park every N layers; regrind when a notch exceeds a layer; two blades per alloy.
- **P10 · Condensate filter fires** (S5 × L2). EOS calls condensate "highly reactive, often pyrophoric, ultrafine"
  ([EOS](https://www.eos.info/content/blog/tackling-the-hidden-challenge-in-metal-am), read); per Fabbaloo its minimum
  ignition energy is below 1 mJ and filter fires start by slow oxidation once air reaches the cake
  ([Fabbaloo 2020](https://www.fabbaloo.com/2020/05/eos-focuses-on-metal-3d-print-safety), SE). *For us:* the housing valves
  off under argon (handled) but no passivation step is written. *Do:* §3.
- **P11 · A loading filter quietly cuts the cross-flow** (S3 × L4; SE). Filter health depends on material, flow and plate
  density, not hours; a new filter lasted 2,500 h in one study; Renishaw and 3D Systems track pressure drop
  ([Ti-6Al-4V filter-condition study](https://ouci.dntb.gov.ua/works/4KQoLBv9)). *Do:* ΔP across the HEPA and a loop flow
  sensor logged per layer; run the blower to a flow set point.
- **P12 · Cover-slide fouling shifts focus by more than the Rayleigh range** (S4 × L4). At 400 W, 0.5 % extra absorption on
  fused silica modelled −21.6 mm; fouled windows measured −22 to −30 mm with the waist growing from 35 to 53 µm, while
  transmission fell < 1 %; N-FK51A modelled −1.3 mm ([Bonhoff et al., LiM 2017](https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution31_final.pdf),
  also cited in low-profile.md; the [design review](../edison/followup-design-review/answer.md) ranks it critical).
  Fraunhofer reports transient shifts up to 8.3 mm within 1 s ([Fraunhofer](https://publica.fraunhofer.de/entities/publication/e2534c2c-c723-4686-aef5-33c40d5b30f3), SE).
  *For us:* low-profile.md chose fused silica for its low *clean* absorption; that doesn't help once the slide is fouled.
  *Do:* rank 1.
- **P13 · Single-point power checks miss uneven fouling** (S3 × L4). On a Sinterstation 2500 (CO2, ZnSe) one build cost
  ~10 %; three builds 20–25 % with a standard window against 3–5 % with a heated one; attenuation varied by up to
  3.5 ± 0.25 % across the window, while practice was one centre reading ([Sassaman et al., SFF 2018](https://utw10945.utweb.utexas.edu/sites/default/files/2018/189%20TwoDimensionalCharacterizationofWindowContami.pdf), read).
  *Do:* map transmission through each used slide at ≥ 5 points; keep slide ID and age in the dataset.
- **P54 · 2 m/s cross-flow is the threshold, not a margin, and small chambers recirculate** (S3 × L4; via Edison). Porosity
  stayed < 0.1 % at 2.5–4.0 m/s but rose sharply at ≤ 2.0 m/s ([Reijonen et al. 2020](https://doi.org/10.1016/j.addma.2019.101030));
  a commercial machine's flow fell from ~4 m/s at the inlet to ~1 m/s at the outlet, and too much flow lifts powder
  ([Shen et al. 2020](https://doi.org/10.1007/s11837-020-04020-y)); low-velocity regions matched porosity at DTU
  ([Kjer et al. 2023](https://doi.org/10.3390/jmmp7040143)); in a compact MIT testbed baffles and vanes only moved the
  recirculation, and a second nozzle at the window stopped it ([Griggs et al. 2021](https://doi.org/10.48550/arxiv.2107.01744));
  an EOS M290 recirculation zone went away when a backward-facing step was removed ([Medinilla et al. 2025](https://doi.org/10.3390/jmmp10010003)).
  *For us:* README §3.4 designs for ~2 m/s through a 120 × 8 mm slot (~115 L/min) in a 120 mm-tall chamber with the outlet in
  the floor. *Do:* rank 12; ≥ 2.5–4 m/s through that slot is ~145–230 L/min *(calc)*.
- **P14 · Volatile elements leave the alloy being screened** (S3 × L5). AlSi10Mg at 0.440 wt% Mg built at 0.356 wt%
  typically and 0.272 wt% at the highest energy density; strength fell below ~0.306 wt%
  ([Liu & Gibbons, SFF 2023](https://utw10945.utweb.utexas.edu/sites/default/files/2023/027%20ControllingChemicalCompositionChangesinLaserPowderBedFusionofAlSi10Mg.pdf), read).
  *Do:* rank 6.
- **P15 · Moist Al powder: hydrogen porosity, and drying has side effects** (S3 × L3). Water desorbs from powder, walls,
  porous insulation and seals after backfill and heating; the laser splits it ([Revanur 2024](https://doi.org/10.17638/03176890), via Edison).
  Vacuum drying 18 h at 70 °C removed ~0.05 % mass ([preprint](https://easychair.org/publications/preprint/V1ld), SE);
  furnace and vacuum drying leave an oxide layer (Procedia CIRP 2024, SE). *Do:* dew point as a permissive; dry-argon flow
  while the plate heats, then re-check; reservoirs sealed and stored under argon.
- **P55 · 200 °C preheat doesn't stop cracking in crack-prone wrought alloys** (S3 × L3; via Edison). 7075 at 100–200 °C
  showed no significant drop in cracking and 400 °C made columnar crack networks ([Velikajne et al. 2026](https://doi.org/10.3390/ma19050970));
  Zr-modified 6182 was crack-free and > 99 % dense only at 500 °C ([Riener et al. 2022](https://doi.org/10.1007/s00170-022-08673-8)).
  *For us:* Tier A is 200 °C, 500 °C is reserved ([`preheat-and-plates.md`](../preheat-and-plates.md)). *Do:* scope the first
  campaigns to AlSi10Mg, Al-Mg-Sc-Zr and grain-refined alloys; run crack-prone wrought alloys as Tier B campaigns.
- **P56 · Edge effects shrink small plates** (S2 × L4). Wall effects on packing grow as layers approach particle size
  ([Jacob et al. 2016](https://doi.org/10.1088/0957-0233/27/11/115601)); the design review estimates ~17–21 mm usable on a
  Ø25 plate and ~67–71 mm on Ø75 (engineering estimate). *Do:* keep coupons ≥ 2–3 mm inside the rim; edge and centre
  witnesses on early builds; log radial position.

### 4.3 Polymer SLS

- **P13** above is an SLS result.
- **P16 · Steps in the cylinder wall leak powder and bulge layers** (S3 × L3; anecdotal). Formlabs Fuse 1 owners: at a metal
  "thermal break" band ~25 mm below the top of the chamber, gaps of ~1.6 mm under and ~0.8 mm above; powder leaked into
  sinkholes and 2 of 3 chambers aborted at that height (another owner: 3 of 6); only a chamber swap fixed it
  ([forum](https://forum.formlabs.com/t/chamber-design-flaw-confirmed-consistent-layer-bulging-and-powder-leaks-within-the-first-inch-of-build-chambers/40735)).
  *For us:* the module is a 316 spigot TIG-welded to a 3 mm-wall tube, and the plate's rim wiper crosses that joint (at
  z = −20 mm; the plate travels −42 to +8 mm) every build. *Do:* hone after welding as one body; gauge the joint for steps
  (≤ 10 µm); weigh what leaks past per 100 layers on the phase 0 rig.
- **P17 · Felt bed seals compact and leak** (S3 × L4). Leaks come through the build-chamber seals, the print-bed felt (voids
  round the cake edge) and the doser seal; the printer schedules seal service ([Formlabs](https://formlabs.com/support/Powder-leaks-Fuse-1-generation/), read).
  The design review found no peer-reviewed leakage or wear data for LPBF piston seals. *For us:* powder past the bore seal or
  rim wiper lands on the heater stack, and the thermal FEA puts M50's start power at 226 W against 150 W installed if the gaps
  fill. *Do:* count layers per seal set; vacuum and weigh under the piston each campaign through the gland plate.
- **P18 · Short feed must stop or redo the layer** (S3 × L4). Fuse Vision aborts (Error 112) when a recoat lays too little
  powder; causes include the recoater motor, hopper debris and unsieved powder ([Formlabs](https://formlabs.com/eu/support/Underdosing-SLS/), read).
  *For us:* the roller meters 0.04–0.33 g, and the load cell cannot resolve a dose (modules.md §3). *Do:* camera coverage
  score every layer with re-dose or pause; sieve every fill; debris screen above the roller.
- **P19 · Powder in the plug of a swappable module** (S3 × L3; anecdotal). Sintered "sinterworms" on about every second job;
  a Formlabs staff member: "in most cases ... imperfect contact on the build chamber plug", also bent pins or powder in the
  plug ([forum](https://forum.formlabs.com/t/fuse-1-print-problem/38534)). *For us:* M12 heater and type K plugs are unplugged
  at every module swap. *Do:* plugs out of the powder path, capped; pin check per swap; open-circuit and plausibility checks
  before heating.

### 4.4 Gloveboxes and gas sensing

- **P20 · Purifiers saturate and need long regenerations** (S2 × L3). Regenerate when O2 or H2O stays above 1 ppm
  ([UCD SOP](https://www.ucd.ie/chem/t4media/School%20of%20Chemistry%20SOP%20For%20Operation%20Of%20Glove%20Boxes.pdf));
  a purifier patent cites 12–24 h per regeneration; leaks come through gloves, antechamber and feedthroughs
  ([Ossila](https://www.ossila.com/pages/glove-box-maintenance)) (SE). *Do:* if a purifier joins the loop, put it after the
  HEPA, budget the downtime, keep forming gas out of the chamber; log glovebox O2/H2O at each reservoir fill.
- **P21 · Zirconia O2 sensors read low with H2 or other combustibles** (S4 × L2; SE). The hot platinum electrode burns them
  with the sample's O2 ([PST](https://www.processsensing.com/en-us/blog/what-gases-and-chemicals-to-avoid.htm)); one glovebox
  vendor lists H2 as unacceptable for its zirconia analyzer ([Terra Universal](https://www.terrauniversal.com/printing/popup/download/david/18108/)).
  *For us:* the laser permissive rests on one O2 reading, and Al melting with moisture makes H2. *Do:* choose the permissive's
  sensor technology deliberately (or cross-check two); monthly span check with certified O2-in-Ar.

### 4.5 Vacuum, seals and the gas supply

- **P22 · Virtual leaks and porous parts keep feeding O2** (S3 × L4). A 1/4 in. blind tapped hole with 1/16 in. left under the
  screw holds 0.6 Torr·L of air ([Normandale](https://normandale.edu/academics/degrees-certificates/vacuum-and-thin-film-technology/articles/understanding-virtual-leaks.html), read);
  seals in series risk virtual leaks ([Pfeiffer](https://know-how-book.pfeiffer-vacuum.com/en/tips-tricks/container!download.action@referer=2582&download=%252Ffilepool%252Ffile%252Ftips-and-tricks%252Fvirtual-leaks-pi0423pen.pdf), SE).
  One such hole emptying into 6.4 L of argon after the last backfill is ~26 ppm O2 *(calc)*. *For us:* blind lid and door
  holes, the double rod-gland interspace, gaps behind liners, graphite foil, felt and HEPA medium. *Do:* keep the vented
  screws; vent the rod-gland interspace; stand liners off the walls; accept on rate-of-rise and O2 drift after the third purge.
- **P23 · O-rings fall out of vertical or upside-down face grooves** (S3 × L4). Dovetail grooves retain rings but are costly
  and tolerance-critical ([Parker](https://www.parker.com/us/en/divisions/o-ring-and-engineered-seals-division/resources/oring-ehandbook/static-oring-sealing/dovetail-and-half-dovetail-grooves.html));
  in a vertical or inverted groove "the O-ring may fall out" ([Gallagher](https://www.gallagherseals.com/blog/press-in-place-seals)).
  *For us:* the drop-down door seal is vertical, the drawer's O-ring too, and a robot will close that door thousands of times.
  *Do:* grooves in the body facing up where possible; half-dovetail or moulded press-in seals on door and drawer; a 30 s
  rate-of-rise test after every automated close.
- **P24 · Spliced cord O-rings are weakest at the joint** (S3 × L3; vendor). Bonded splices are the weak point and unsuited
  to vacuum; moulded or vulcanized rings are preferred ([Rubber & Seal](https://rubberandseal.com/what-is-the-difference-between-spliced-and-vulcanized-o-rings),
  [Marco](https://www.marcorubber.com/spliced.htm)). *For us:* ~2.3 m of 96515K127 cord spliced on a 9262N11 jig.
  *Do:* buy moulded or vulcanized FKM rings; if spliced in-house, keep joints off corners and leak-test them.
- **P25 · Helium leak checks mislead on elastomer seals** (S2 × L3). One KF-16 Viton ring lets a 1 L chamber rise from
  1e-6 to 1e-3 Torr in 222 min by air permeation alone; long helium probing gives a slow, permeation-driven rise mistaken for
  a leak ([Normandale](https://normandale.edu/academics/degrees-certificates/vacuum-and-thin-film-technology/articles/gas-load-from-elastomer-and-metal-seals.html), read).
  *Do:* accept on rate-of-rise from ≤ 1 mbar and O2 rise over 1 h at +20 mbar argon.
- **P26 · V-ring packing shaft seals are not vacuum seals** (S4 × L4; SE). An SKF/Chicago Rawhide V-ring lists dirt
  exclusion, 10 psi maximum and a 4.35 psi (0.3 bar) maximum differential ([distributor listing](https://www.applied.com/c-brands/c-skf-corp/c-chicago-rawhide/400164/V-Ring-Seal/p/100916090));
  standard lip seals are designed for ~7 psi ([MRO Magazine](https://www.mromagazine.com/features/how-to-select-the-proper-industrial-shaft-seal-for-an-application/)).
  *For us:* the recoater and roller shafts pass the wall through 9572K33 PTFE V-ring packing and see 1 bar at every purge
  (README §6a already calls them the weak seals). *Do:* rank 2.
- **P27 · Backfill overpressure breaks windows** (S4 × L2; SE). A chamber vented from a nitrogen cylinder and left
  unattended over-pressurized and its window shattered ([UC Berkeley EH&S](https://ehs.berkeley.edu/sites/default/files/lessons_learned_-_vacuum_chamber_over-pressurization.pdf));
  Jefferson Lab requires that the source relieving vacuum not exceed 15 psig in any failure mode ([JLab ES&H](https://www.jlab.org/ehs/ehsmanual/Pressure%20and%20Vacuum%20Systems%20Supplement/PSS%20Part%207%20Vacuum%20Systems.htm)).
  *For us:* door, drawer and slide are designed around vacuum and +20 mbar. *Do:* size the 0.5 psi relief for the worst-case
  argon flow; a restricting orifice; a hardware pressure switch at ~+40 mbar that drops the argon valves.
- **P28 · Pump-down and venting blow powder out of cylinders and hoppers** (S3 × L4). UT's direct-SLS patent joins the void
  above the bed to the voids under the powder columns "to prevent ejection of powder ... during chamber evacuation", and
  throttles evacuation with bellows valves ([US 6676892 B2](https://patents.google.com/patent/US6676892B2/en), read).
  *For us:* the under-piston void can only vent through the bore seal and the bed; each reservoir's headspace vents through
  its powder and the roller. *Do:* rank 14.
- **P29 · Powder and condensate reach the scroll pump** (S3 × L4; SE). Edwards sells a KF-25 trap (5 µm, 1 µm option) for
  nXDS inlets "to protect from debris", or exhausts, for tip-seal dust ([listing](https://www.vacstock.com/edwards-nxds-series-dry-scroll-vacuum-pump-micron-filter-trap-can-be-used-on-the-inlet-or-pump-exhaust-kf-25-vacuum-flanges-pn-a505-97-805)).
  *Do:* a 1 µm inlet trap treated like the HEPA; pump from a port away from the bed; pump-down time as a health metric.

### 4.6 Lasers, optics and laser safety

- **P05** (scan mirrors) is in §4.1.
- **P30 · Back-reflection from Al: instability, trips or damage** (S4 × L3). Reflective metals cause unstable operation,
  shutdowns or failure ([Laser Focus World](https://www.laserfocusworld.com/industrial-laser-solutions/article/14216489/fiber-laser-allows-processing-of-highly-reflective-materials));
  "legacy fiber lasers often employ software isolation which shuts off the laser when back-reflection is detected"
  ([nLIGHT](https://www.nlight.net/back-reflection-protection)). *For us:* small plates sit at the field centre, near normal
  incidence, and first layers hit bare 6061; IPG hasn't confirmed protection ([quote](../quotes/ipg-ylr-500-u3-sm-ac.md)).
  *Do:* rank 8.
- **P31 · Thermal focal shift in the f-theta at 500 W** (S3 × L3; SE). F-theta lenses measured under a 500 W fiber laser;
  passive compensation cut the shift by 60 % ([Stubenvoll et al. 2014](https://doi.org/10.1364/OE.22.025385)); standard
  optical glass absorbs too much for high power ([Jenoptik, euspen 2012](https://www.euspen.eu/knowledge-base/ICE12192.pdf)).
  *For us:* the FTH160-1064 envelope lists only a pulsed damage threshold. *Do:* a fused-silica f-theta rated ≥ 500 W CW;
  measure the caustic cold and after 10 min at power.
- **P32 · Galvo drift and calibration** (S2 × L3). SCANcube IV 30: < 20 µrad/K offset, < 50 µrad over 8 h after a 30 min
  warm-up ([SCANLAB](https://www.scanlab.de/en/scancube-iv-30)); at f = 160 mm that is 3.2 µm/K and 8 µm *(calc)*. NIST
  calibrates with a 7 × 7 dot grid burned at ~15 W, scanned at 4800 dpi, targeting < 1e-3 mm/mm
  ([Lane et al., TN 2099](https://doi.org/10.6028/nist.tn.2099), via Edison). *Do:* warm-up in the recipe; a dot-grid
  calibration; three fiducials per build imaged by the layer camera.
- **P33 · Eye injuries when a beam is assumed off, and during alignment** (S5 × L2). A researcher put a dielectric mirror
  into a 1 W CW 852 nm beam believed off ([UC Berkeley lessons learned](https://ehs.berkeley.edu/sites/default/files/lessons-learned-laser-eye-exposure.pdf), read);
  an earlier Berkeley injury came from a stray reflection while aligning a Class 4 Nd:YAG
  ([Berkeley EH&S](https://ehs.berkeley.edu/news/laser-safety-research-laboratories)). *Do:* §3.
- **P53 · Factory-built interlocks can be wrong** (S5 × L2). FDA Class 2 recall, 8 Aug 2024: 751 Epilog Fusion Pro 24
  engravers, some "released with an incorrectly placed Interlock device", so they could run with the front door open
  ([FDA](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=211119), read). *For us:* every interlock here is
  built in-house, and the engraver route modifies a bought machine's. *Do:* §3.

### 4.7 Metal powder fires and explosions

- **P34 · Water on Al filter dust: hydrogen deflagrations, two dead** (S5 × L2). Shanghai, 14 Sep 2023, at an LPBF machine
  maker: during a cartridge-filter swap an operator sprayed tap water on the element; hydrogen ignited; later water poured on a
  smoking filter caused a second deflagration; 2 dead, 2 injured with burns over 90 % and 70 % (investigation unconfirmed)
  ([Dust Safety Science](https://dustsafetyscience.com/?p=16940), read). *For us:* modules.md §4 suggests a wet immersion
  separator vacuum for Al condensate (it makes hydrogen and needs venting), and low-profile.md still routes chilled water
  through the dock although the quoted IPG laser is air-cooled. *Do:* §3.
- **P35 · Condensate on chamber walls ignites during vacuum cleaning** (S5 × L3). ARIA 50745, Cebazat, 22 Sep 2017: Ti soot
  on the inner walls of an LPBF machine ignited when cleaned with an ATEX vacuum; flames spread to plastic parts; 54 people
  evacuated; the risk analysis hadn't covered the soot; the stepladder wasn't earthed
  ([ARIA](https://www.aria.developpement-durable.gouv.fr/accident/50745_en/?lang=en), read). *Do:* rank 4.
- **P36 · Static ignition in a vacuum with Al dust** (S4 × L2; SE). An operating industrial vacuum exploded while a second one
  was being cleaned; static suspected ([ARIA 31934](https://www.aria.developpement-durable.gouv.fr/accident/31934_en/?lang=en)).
  *Do:* conductive bonded hose; one vacuum per alloy family; never service one while another runs on the line.
- **P37 · The AM fire OSHA cited** (S5 × L2). Powderpart, Woburn, 5 Nov 2013: third-degree burns to an employee working
  alone; one willful item (no Class D) and nine serious, $64,400; dust collector not emptied daily or monthly; an unrated
  shop vac at the sieving station; sprinklers couldn't be disconnected ([OSHA](https://www.dol.gov/newsroom/releases/osha/osha20140520-2),
  [EHS Today](https://www.ehstoday.com/safety/article/21918077/osha-cites-3-d-printing-firm-after-explosion)). *Do:* §3.
- **P38 · Al dust in a closed barrel took on water and blew its lid** (S4 × L2; SE). The dust cloud exploded in a fireball
  ([HIAD 746](https://h2tools.org/hiad-event/explosion-metallic-products-plant-746)). *Do:* store spent elements and
  condensate dry under sand in vented, grounded metal cans.
- **P39 · Accumulated fine metal dust lofted by a small event** (S4 × L1). Hoeganaes, 2011: two iron-dust flash fires and a
  hydrogen explosion that lofted dust; 5 killed ([CSB](https://www.csb.gov/csb-releases-final-investigation-report-on-three-accidents-at-the-hoeganaes-iron-powder-facility-in-gallatin-tennessee/)).
  *Do:* wipe-downs per campaign; ask EHS to include the VLM in the dust hazard analysis.
- **P40 · An explosion in a dust collector travels back through ducts** (S4 × L1). Hayes Lemmerz, 2003
  ([CSB](https://www.csb.gov/hayes-lemmerz-dust-explosions-and-fire/)). *For us:* the loop is closed and inert (handled).
  *Do:* never tie the chamber or guard to shared dust extraction.

### 4.8 Heaters and their control

- **P41 · SSRs fail shorted** (S4 × L3; SE). A shorted SSR is "the most prevalent concern" ([Thermal Devices](https://thermaldevices.com/wp-content/uploads/2017/01/SSR-Catalog-Pages.pdf));
  semiconductor switches are "not legal for over temperature limit or safety devices" ([Watlow](https://www.watlow.com/-/media/documents/user-manuals/sdmae-a.ashx)).
  *For us:* the CN708 limit with a mechanical relay is the right architecture if its relay breaks the power path. *Do:* rank 11.
- **P42 · A heater or sensor backs out of its hole and nothing notices** (S4 × L3). A desktop 3D printer caught fire after its
  cartridge came loose from the block, undetected by stock firmware ([Hackaday 2018](https://hackaday.com/2018/03/18/3d-printer-halts-and-catches-fire-analysis-finds-a-surprising-culprit));
  Prusa trips when the temperature drops > 15 °C for > 45 s ([Prusa](https://help.prusa3d.com/en/article/thermal-runaway-i3-series_2131)).
  *For us:* cartridges and thermocouples enter the block from below. *Do:* rank 10.
- **P43 · Cartridge heaters fail at the lead end and when loose** (S3 × L3; SE). Contamination, corrosion, over-temperature
  and lead failure; a loose fit runs much hotter; cycling draws material into the lead end
  ([Tempco](https://www.tempco.com/Tempco/Blog/High-Temperature-Cartridge-Heaters-Overcoming-Failure-in-Industrial-Heating-Applications.htm),
  [Watlow FIREROD](https://core.instrumart.com/assets/firerodcartridge_brochure.pdf)). *For us:* lead ends point down into the
  pockets where escaped powder collects. *Do:* reamed holes; glass or mica leads; sealed lead pockets; insulation tests.
- **P44 · A thermal cutoff run too close to its rating** (S3 × L4; SE). Keep TCOs below Tf − 25 °C continuously; no published
  DC ratings for MICROTEMP ([datasheet copy](https://www.farnell.com/datasheets/1582151.pdf)). *For us:* a 240 °C cutoff in a
  block at 204–221 °C with a 225 °C heat-up cap sits above 215 °C. *Do:* move or re-rate it (with a DC rating); the CN708 stays
  the primary limit.

### 4.9 Motion, powder handling, automation and controls

- **P45 · Fine powder destroys ball screws and guides** (S4 × L4; SE). Foreign matter in a ball nut causes fast abnormal wear
  and can block recirculation ([Kuroda](https://kurodaprecision.com/global/products/technical-information/bs/bs003.html)); bellows
  suit larger particles, fine ones need robust seals or full enclosure ([guide](https://dings-motion.squarespace.com/blog/keeping-dust-metal-and-moisture-out-how-to-extend-the-life-of-your-motion-system)).
  *For us:* the 6709K12 carriage (rubber end seals, grease fitting, 175 °F) and the ball screw are inside the chamber while the
  design also says no lubricant inside. *Do:* rank 3.
- **P46 · Interlocks get defeated when they block work** (S5 × L2; SE). An object in a gate relay; a door interlock defeated
  with a rag; a worker who spent 40 minutes disabling one ([NIOSH](https://stacks.cdc.gov/view/cdc/205908),
  [A3](https://www.automate.org/industry-insights/robot-safety-and-you-examples-of-real-life-accidents-we-can-learn-from)). *Do:* §3.
- **P47 · Cohesive powder arches and ratholes** (S3 × L4). TU Berlin's synchrotron LPBF on an Aconity MINI base: fine or
  cohesive powders bridged its funnel, so vibration motors were added ([Uhlmann et al. 2020](https://doi.org/10.14279/depositonce-16115), via Edison);
  MIT's vibrated hopper needed empirical calibration of dose against pressure and time ([Oropeza et al. 2021](https://doi.org/10.1063/5.0031191));
  mass-flow cones need walls steeper than 58–71° from horizontal ([Chem. Eng.](https://www.chemengonline.com/hopper-design-principles), SE).
  *Do:* rank 15.
- **P48 · Fine Al powder charges on insulators and in dry gas** (S3 × L3). AlSi10Mg picked up about −2.8 to −5.7 nC/m² on
  stainless; drier gas keeps charge longer and fines can charge opposite to coarse particles (theses via Edison;
  [Galindo et al. 2024](https://doi.org/10.1038/s41598-024-67295-0)); insulating liners charge powder far more than aluminium
  walls ([Bristol, arXiv 2025](https://arxiv.org/html/2507.18193v1)). *Do:* bond every metal part in the powder path; dissipative
  polymers only; test spreading in dry argon.
- **P49 · Pressure forces swamp a load cell across a sealed joint** (S3 × L4; SE). A hopper sealed to a separately supported
  hood weighs wrong as pressure changes, and needs venting ([OMEGA](https://it.omega.com/literature/transactions/volume3/weigh2.html));
  the error is pressure × sealed area ([HBM](https://www.hbm.com/pt/3722/structural-design-of-tank-weighing-systems/)).
  *For us:* a ~20 × 100 mm sealed reservoir outlet sees ~4 N at +20 mbar and ~200 N at full vacuum *(calc)*, far past a
  2–3 kg cell. *Do:* keep the pressure boundary out of the load path; overload stops; weigh at a known pressure.
- **P52 · The VLM moves a tray mid-build** (S4 × L2; derived). low-profile.md §4.2 assumes 2 m/s² tray motion; the dock parts
  as the tray leaves. *Do:* make the tray un-callable while lasing, hot, off atmosphere or mid-build, by a hardware permissive.
- **P57 · Seal drag can pull the piston off its magnetic coupling** (S4 × L3; derived). The design review flags coupling slip
  and seal drag as Z errors to qualify at temperature. Our numbers: M50 break-out drag ~133 N, magnet break-away ~217 N clean
  but ~27 % of that across a 0.1 mm gap, so ~59 N with one grain on the striker ([`hot-swap.md`](../hot-swap.md) §1–2, *calc*):
  the arm drops, the piston stays, the next layer is ~0 µm and the blade hits the part. *Do:* rank 9.
- **P58 · Closed or analog controls obsolete or degrade a machine** (S3 × L3; via Edison). A Realizer 250 became inoperable
  when its DOS control PC crashed, with no service path (Aagaard et al. 2023); DTU's first analog scanner links picked up noise,
  so their second generation went digital ([Andersen et al. 2022](https://doi.org/10.26153/tsw/44600)). *For us:* the engraver
  route's locked EZCAD board; the laser's 0–10 V analog power input. *Do:* code and config in git with a spare board; open
  protocols; short shielded analog lines; check power ripple with the photodiode.
- **P59 · Monitoring data mislead unless tied to machine state** (S2 × L4; via Edison). An Aconity MINI's pyrometer logged
  through laser-off travel, giving false lows (Maddison 2022); an MPrint+ refreshed its live view only every few seconds,
  too slow to save a crash ([Friedo et al. 2026](https://doi.org/10.33968/2026.29)); LLNL had to correct laser timing for galvo
  acceleration ([Calta et al. 2018](https://doi.org/10.1063/1.5017236)). *Do:* sample the photodiode on the scan controller's
  clock with gate and position; tune delays and skywriting on a test pattern; automatic aborts.

### 4.10 Argon and fire inside a VLM

- **P50 · Argon pools out of sight** (S5 × L2; SE). Argon leaked from an autoclave into a ~4,500 ft³ basement with its
  ventilation off; two workers died; there was no continuous O2 monitoring ([summary of the CSB report](https://safteng.net/argon-asphyxiates-two-workers-leak-checking-a-process/));
  floor O2 can be below 15 % while breathing height reads above 20 % ([LBNL](https://ehs.lbl.gov/service/chemical-lab-safety/oxygen-deficiency-hazards-and-asphyxiation/)).
  *For us:* each build dumps 2–3 chamber volumes plus the loop inside an enclosed tower, and the room's O2 monitor is outside it. *Do:* §3.
- **P51 · VLM towers hide fires and defeat sprinklers** (S5 × L2). Towers of 30 ft or more trap heat and smoke; sprinklers
  are designed for open shelving; Kardex and Fike recommend aspirating detection and IG-100, which is nitrogen
  ([Kardex](https://kardex.com/en-us/blog/vlm-warehouse-fire-suppression-system), read). *For us:* water reacts with Al, and
  Mg burns in nitrogen (the reason for the lab's argon rule). *Do:* §3.

## 5. Where web anecdotes and the literature agree or disagree

| Topic | Web, incident and vendor sources | Literature (mostly via the two Edison reviews) | Verdict for this design |
|---|---|---|---|
| Recoater strikes | Xact users; Formlabs curling (P08) | MPrint+ build loss (Friedo 2026); UniBw; Skácelík 2026 | **Agree**: strikes are the main way small machines lose builds |
| Rigid vs compliant blade | hobby SLM: silicone edge destroyed by hot metal, steel worked (P01) | Heriot-Watt's rigid blades jammed (Bidare 2017); compliant rubber took collisions (Skácelík); the design review puts compliant first; UniBw's rubber lips were grooved by crashes | **Partly disagree.** Compliant blades survive strikes but wear, burn and shed polymer; rigid blades crash. Keep both cartridges and log which ran |
| Window and slide fouling | Fraunhofer: transient 8.3 mm shifts (SE); SLS: 10–25 % power loss (CO2, ZnSe) | Bonhoff: −22 to −30 mm, transmission < 1 % lower | **Agree** that focus shift, not power loss, is the problem at 1 µm. **Disagrees with low-profile.md's reason** for fused silica: its low clean absorption doesn't help a fouled slide. Trial an athermal slide (P12) |
| Cross-flow speed | README §3.4 design point ~2 m/s (citing Reijonen via the first Edison review) | Reijonen: degradation at ≤ 2.0 m/s, < 0.1 % porosity at 2.5–4.0 m/s; Shen; Kjer; Griggs | **Disagree with our design point**, not between sources: 2 m/s is the threshold. Aim for ≥ 2.5 m/s measured (P54) |
| Fine-powder hoppers | hopper-design guidance: steep walls, vibration can make cohesive powder worse | Uhlmann (funnel clogged, vibrators added); Oropeza (vibrated hopper, empirical dose) | **Agree** that agitation and per-powder testing are needed. The design review's load-cell dose check doesn't fit us: the 3 kg cell can't resolve a 0.04–0.33 g dose, so use camera coverage and the overflow mass balance (P18, P47) |
| Piston and bed seals | Formlabs support and forum: felt leaks, wall steps (P16, P17) | design review: essentially no peer-reviewed leakage or wear data | **No conflict; a gap.** SLS experience is the only evidence, so measure and publish our own leakage |
| Fires | ARIA, OSHA, CSB, Dust Safety Science (P34–P40) | neither review covers fire beyond O2 spikes at filter service (Revanur) | **Gap in the literature**: the incident databases are the evidence base for the cleaning and filter SOPs |
| Purging | TruPrint 1000 ≤ 3000 ppm without its glovebox option (README §2.2); Heriot-Watt's flow purge only reached < 0.5 % | ESRF replicator needed 3 vacuum–argon cycles for < 100 ppm (Lhuissier 2022); DTU: O2 dominates quality | **Agree**: vacuum cycles plus measurement. The design review assumed a single evacuation, but README §3.4 already plans 2–3 cycles |
| Mirror heating | README's earlier "~275 °C" (via the first Edison review) | Grantham 2016: 220.2 °C measured, ~275 °C estimated | **Agree** |
| Electrostatics | Bristol preprint, AIChE abstract | Alchikh-Sulaiman, Galindo, Ramirez | **Agree**: dry gas and insulators make it worse |
| Alloy changeover on small machines | no public user reports found | Aconity MINI cleaning ~1 h against ≥ 5 h on a Renishaw (Maddison 2022) | Supports building small; no conflict |

## 6. What the design already handles well

- **Vacuum–argon purge cycles, not flow purging** (README §3.4, `budgets.py`). Flow-purged machines plateau: Heriot-Watt
  reached < 0.5 % O2 and the TruPrint 1000 ≤ 3000 ppm without its glovebox option; the ESRF replicator needed three vacuum
  cycles for < 100 ppm, and DTU found O2 the dominant quality factor.
- **Optics on a bridge of their own.** NIST decoupled AMMT's optics because vacuum deflects the chamber; our bridge stands on
  its own posts, and the FEA puts the lid's sag at 24 µm.
- **A gas knife under the window.** In a compact chamber, Griggs et al. found that only a second nozzle near the window
  stopped recirculation there (baffles and vanes just moved it); AMMT has an air knife under its scanner optics too. Flow
  speed (P54) and slide material (P12) still need work.
- **The cover slide treated as a consumable and pressure-equalized**, as LLNL protected its Be windows with sacrificial Kapton.
- **A thermal break under the heated plate** (Macor and shields, sized by FEA). A hobby welder-printer welded its plate to its
  Z gantry ([Hackaday 2026](https://hackaday.com/2026/02/01/building-a-metal-3d-printer-with-a-laser-welder)).
- **No polymer inside the gas envelope, bare 6061, FKM seals, per-alloy consumables and lift-out 316L liners.** In ARIA 50745
  the fire spread to the machine's plastic parts; the design review recommends removable stainless liners against carry-over.
- **The HEPA housing valves off under argon, spent elements go under dry sand, and a Class D extinguisher sits at the
  machine** (EOS, Shanghai 2023, Powderpart). P10 and P34 add the passivation step and keep water away.
- **A hardwired dual-channel interlock chain with guard locking; software can only request emission** (as OpenAM and the ESRF
  hutch interlock). P53 adds proof-testing.
- **An independent limit controller with a mechanical relay and manual reset**, the right answer to SSRs that fail shorted
  (P41), once its wiring and the cutoff's rating (P44) are fixed.
- **Vented screws in blind holes and FKM rather than silicone** (P22's main cure, and low permeation).
- **Fastener-free robot swaps** ([`hot-swap.md`](../hot-swap.md)): System 3R names "the unscrewing operation inside a powder
  environment" as the problem with screwed plates.
- **A small chamber, a removable gland plate under each module and a small powder inventory**: quicker alloy changes, access
  to the powder that passes the bore seal (P17), and less fuel in a fire.

## 7. Gaps in this search

- **No public user reports turned up** for the TruPrint 1000, MYSINT100, ORLAS Creator, AO Metal or Farsoon FS121M, and no
  recalls or service bulletins for any desktop LPBF machine (the only recall found was the Epilog engraver, P53). The best
  small-machine user evidence is the MPrint+ (Friedo 2026) and Aconity MINI (Maddison 2022) papers, via Edison.
- **Reddit couldn't be read**: old.reddit.com now asks for a login, and www.reddit.com returned 403 even through the lab Pi.
- **Blocked pages** (Fraunhofer, OUCI, AM Media, Fabbaloo, HIAD, automate.org, Metal AM) are marked SE in the CSV.
- **The literature lacks** piston-seal leakage and wear rates, dose repeatability for fine Al through narrow slots, and measured
  usable-area fractions for 25–75 mm plates (the design review says so too). This machine could publish all three.
- **Synchrotron replicators** were covered only through the lab-built-lessons review (LLNL, UCL, ESRF, TU Berlin).
