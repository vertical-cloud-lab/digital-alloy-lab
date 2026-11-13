# Thermo-Calc AM Module — R2: Preliminary Results (M0)

**Source:** Thermo-Calc's account manager (Thermo-Calc AB), first batch in response to r1 (`edison-thermocalc-compositions-r1.md`).
**Delivery location:** `figures/thermo-calc-am-module-prelim-results/`
**Status:** preliminary; AlSi10Mg + BYU blend only. Alloy C and Al-Zr runs still pending.

---

## 1. Delivered (M0)

Four PNGs in `figures/thermo-calc-am-module-prelim-results/`:

- `AlSi10Mg-printability-map.png` — P–v printability map (lack-of-fusion / keyhole / balling regions) for stock AlSi10Mg.
- `BYU-AA1100-Si-AlSi10Mg-blend-printability-map.png` — same map for the BYU AA1100 + elemental-Si + AlSi10Mg blend planned for the early-FLAIME atomization runs.
- `AlSi10Mg-250W 900mm-s.png` — steady-state melt-pool cross-section, stock AlSi10Mg, **250 W, 900 mm s⁻¹**.
- `BYUMix-375W-400mms.png` — steady-state melt-pool cross-section, BYU blend, **375 W, 400 mm s⁻¹**.

(File renaming to `AlSi10Mg-meltpool-250W-900mms.png` / `BYUMix-meltpool-375W-400mms.png` is owned by a separate sub-agent; current names on disk are as listed above.)

## 2. Coverage vs. r1 request

| r1 item | Composition | Status |
|---|---|---|
| §1 "Alloy C" + perturbations | Al-5Mn-0.8Cr-0.5Zr, Al-2.5Mn-0.5Cr-0.5Zr, Al-5Mn-0.8Cr-0.1Zr | **Not yet delivered.** |
| §2 Al-Zr ladder | Al-1.5Zr / Al-0.5Zr / Al-0.25Zr | **Not yet delivered.** |
| Workflow anchor (implied by r1 §4 item 1 and proposal §1 Thermo-Calc Partnership paragraph, `flaime-genesis-proposal.tex` ~line 1081) | AlSi10Mg | **Delivered** — printability map + one melt-pool point. |
| Bonus (not requested in r1) | BYU AA1100 + Si + AlSi10Mg blend | **Delivered** — useful early-FLAIME composition bracket; flag as bonus. |

So the Alloy-C and Al-Zr anchor systems — the scientifically novel asks in r1 — are still open. What landed is the workflow / absorptivity-calibration baseline plus a free-of-charge bracket for the first BYU-atomized feedstock.

## 3. Sanity-check items from r1 §4 — status

1. **Absorptivity calibration (r1 §4.1).** AlSi10Mg run *implicitly* exercises whatever absorptivity pre-factor Thermo-Calc chose, but the value is not annotated on the figures. Open — needs explicit confirmation.
2. **Equiaxed-transition / dendrite-tip undercooling (r1 §4.2).** Irrelevant for the AlSi10Mg-only deliverable (near-eutectic, no primary L1₂-Al₃Zr nucleation to stress the model). Will become relevant once Al-Zr runs land.
3. **TCAl10 ternary coverage for Al-Mn-Zr / Al-Cr-Zr (r1 §4.3).** Not exercised by AlSi10Mg or the BYU blend (both are Al-Si dominated). Open — only testable once Alloy C is run.
4. **Metastable L1₂ vs equilibrium D0₂₃ phase selection (r1 §4.4).** Not exercised here (no Zr in either delivered system). Open — must be confirmed before Al-Zr / Alloy C Scheil curves are interpreted.

## 4. Next request to Thermo-Calc (prioritized)

1. **Alloy C (Al-5Mn-0.8Cr-0.5Zr, wt%):** printability map + steady-state melt-pool at one representative operating point (suggest a mid-window P–v from the AlSi10Mg map for direct comparison).
2. **Al-1.5Zr (wt%):** same deliverables — printability map + one melt-pool section.
3. **Absorptivity:** explicit confirmation of the absorptivity pre-factor used for the AlSi10Mg run, and whether the same value was reused for the BYU blend.
4. **Phase selection:** confirm L1₂-Al₃Zr was kept active and D0₂₃ suspended for any Scheil curves embedded in / underlying the printability maps, so the convention is locked in before the Zr-bearing runs.

## 5. Where in the proposal these results land

Top sub-panel of `Fig.~\ref{fig:baseline-supp}` (the AlSi10Mg-baseline supplementary figure in Appendix 8) of `genesis-mission-proposal/flaime-genesis-proposal.tex`. Cross-referenced from the §1 Thermo-Calc Partnership paragraph (~line 1081) and the §A8.2 AM Module cost paragraph (~line 2232). The Alloy C / Al-Zr anchor figure (`fig:anchor-calphad`) is **not** filled by this delivery and remains a placeholder pending the Alloy C and Al-1.5Zr runs requested above. LaTeX edits to wire these images in are owned by a separate sub-agent.
