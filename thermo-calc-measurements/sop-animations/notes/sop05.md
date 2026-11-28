# SOP 05 video: composition (ICP-OES) and O/N/H (inert gas fusion)

Script: [`sop05_composition.py`](../sop05_composition.py), one SOPScene per chapter (`sop05_c1` … `sop05_c6`),
joined into `out/mp4/sop05.mp4` (`python sop05_composition.py join`). The models it adds are in
[`models_chem.py`](../models_chem.py), with notes [icp_oes.md](icp_oes.md), [onh_analyzer.md](onh_analyzer.md),
[microwave_digester.md](microwave_digester.md) and [heat_sealer.md](heat_sealer.md). It reuses `riffle_splitter` (SOP 01's
`models_dsc.py`), byu-vcl's Labconco fume hood, the A&D HR-202i analytical balance (`labware.py`), and `people.Person`.

The SOP is [`sops/05-composition-interstitials.md`](../../sops/05-composition-interstitials.md). Every panel carries a
badge: **synthetic example**, **computed** or **illustrative**. None of it is a measurement.

## Every SOP line, and where the video shows it

Times are in the joined video (m:ss) and come from `out/sop05.json`.

TIMES_TABLE

## Sources for what the video shows at the contract lab

The SOP is a send-out procedure, so the lab's steps (chapters 4 and 5) are shown as *typical*. The captions say the
lab's own method sets them. Where a number appears, it comes from these sources:

- **Edison, `edison/v3-hardness-eddy-icp-onh/answer.md`** (ICP-OES and inert gas fusion sections):
  - Yamani et al. 2021, [doi:10.1016/j.arabjc.2021.103174](https://doi.org/10.1016/j.arabjc.2021.103174): 150 mg of Al
    alloy, 3.0 mL HNO3 and 5.0 mL HCl, microwave digestion, made up to 100 mL. The video's "~0.15 g" and "HCl and
    HNO3".
  - Robinson 2025, [doi:10.1111/ggr.12555](https://doi.org/10.1111/ggr.12555): HF in closed PTFE/PFA vessels for
    Si-bearing residues, boric acid to complex the fluoride, and lithium-borate fusion as the alternative. The
    video's "with HF for Si, or a fusion" and "boric acid ties up the fluoride".
  - The instrument path, about 6,000–10,000 K, and the radial and axial views: Lotter 2014; Uemoto 2011,
    [doi:10.5772/13727](https://doi.org/10.5772/13727).
  - Liu et al. 2025, [doi:10.1088/1742-6596/2959/1/012001](https://doi.org/10.1088/1742-6596/2959/1/012001):
    80–100 mg of powder in a tin capsule; the ONH836 degasses the crucible at 5.5 kW for 20 s and analyses at 5.0 kW
    for 45 s; NDIR for CO/CO2. The video's outgassing and fusion captions.
  - Paplewski: seal powders airtight under argon, and open them only to weigh. The video's argon flush and heat
    seal.
  - Rezaei 2026, [doi:10.3390/app16136822](https://doi.org/10.3390/app16136822): virgin gas-atomized AlSi10Mg has
    about 500–600 ppm O. The synthetic powder in the oxygen panel (520 ppm) is in that range.
- **LECO**: the ONH836 measures H as H2O by NDIR and N by thermal conductivity (LECO's 736/836 model comparison);
  application notes 203-821-459 and 203-821-427. The video's detection caption follows LECO rather than Edison's
  general "N2 and H2 by TCD".
- **ASTM E3061-24**: *Standard Test Method for Analysis of Aluminum and Aluminum Alloys by Inductively Coupled Plasma
  Atomic Emission Spectrometry (Performance Based)*, the method the SOP names (from Edison q2).

## The computed panel

The oxygen panel draws `w_O = 6/(ρ_Al·D50) · t · ρ_ox · 3M_O/M_Al2O3`: spheres of diameter D50 carrying a uniform
Al2O3 skin of thickness t. It uses ρ_Al = 2.70 g/cm³, ρ_ox = 3.05 g/cm³ (amorphous alumina, an assumption) and
t = 4 nm (the SOP's "~4 nm native oxide, an assumption to check against XPS"). At D50 = 38 µm that gives **336 ppm**.
The synthetic run A1 at 520 ppm is about 1.5 × the skin estimate. The SOP reads an excess like that as oxide from the
melt. The Scheil panel uses the repo's own `analysis/dsc_solidification.scheil_fs`, with the liquidus moved by 1.2 K
for the "measured" curve. It is illustrative, not a Thermo-Calc or pycalphad result.

## Collision audit (`audit.py`, every 2nd frame, deeper than 1.5 mm)

AUDIT_TABLE

Allowed contacts are listed in each chapter's `audit.Audit(..., allow=...)`. They are:
- a glove on what it holds or presses: the jar, spatula, boat, cap, vial, nozzle, bag, the sealer's arm, the drill's
  feed handle, the tongs, tweezers, tube and CRM;
- a tool on what it works: the spatula in the pan, the needle in the bag, the drill's bit in the cube or bar, the
  tweezers on the capsule;
- a sample in its seat: the bag between the sealer's jaws, a vial in the foam, the tube in the SPS 4's rack;
- the drill's quill sliding inside its head;
- the sealed and unsealed bag drawn crossfading in one place;
- the argon hose. It is re-drawn every frame to follow the nozzle, which the audit's cached geometry can't track.

## Left out, and why

- **The lab's own numbers.** The SOP says to ask the lab for its method, detection limits, digestion and uncertainty,
  so the video shows the question (chapter 3) and marks the lab-side steps as typical.
- **Prices and turnaround.** The SOP doesn't quote them, and the repo is public.
- **Names of lab staff.** People appear only by role (in the chain-of-custody panel too).
- **Microwave vessel loading.** The vessel doesn't visibly travel from the hood to the rotor, which is shown already
  loaded.
- **The bag in the shipper.** Only the vial is packed on screen; the caption covers every container.
