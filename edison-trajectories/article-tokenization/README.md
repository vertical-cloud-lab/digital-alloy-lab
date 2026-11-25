# Tokenized reference articles

Machine-readable, LLM-friendly tokenizations of the 8 reference PDFs uploaded by
@XZaitzeff (see [PR #4 discussion](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/4)).
Each article lives in its own folder and is converted into faithful Markdown so the
papers can be cited, quoted, and reasoned over by agents working on the Genesis
Mission Topic 3B (Critical Minerals / AMMTO) CALPHAD screening effort.

## Per-article files

Each `<slug>/` folder contains:

| File | Contents |
|---|---|
| `tokenized.md` | Full text in reading order with section headings (Title / Authors / Abstract / Introduction / Methods / Results / Discussion / Conclusions / References). |
| `tables.md` | Every table transcribed as GitHub-flavored Markdown (or a note that the article has none). |
| `figures-captions.md` | Every figure caption, plus a gallery linking the extracted figure images. |
| `figures/` | Raster figure objects extracted directly from the PDF (`pdfimages`). |
| `fulltext.txt` | Local `pdftotext -layout` extraction (faithful fallback / primary source for the directly-built articles). |
| `edison-trajectory.json` | Raw Edison ANALYSIS task response (present only for the 5 Edison-tokenized articles). |

## The 8 articles

| Slug | Article | Why it's here (Topic 3B relevance) | Provenance |
|---|---|---|---|
| [`adma-strengthening-phases-suppmat`](adma-strengthening-phases-suppmat/tokenized.md) | Supporting Information for *Adv. Mater.* 10.1002/adma.202509507 (Taheri-Mousavi, Olson, Hart et al.) | Inverse strengthening-phase screening / down-selection methodology for AM alloys; printability as a forward-predicted constraint | Edison |
| [`computational-alloy-design`](computational-alloy-design/tokenized.md) | Computational design of light and strong high-entropy alloys (Menou et al.) | CALPHAD + genetic-algorithm multi-objective screening of ~8M alloys — direct precedent for the pipeline | Edison |
| [`titanium-thermocalc`](titanium-thermocalc/tokenized.md) | A novel crack-free Ti-modified Al-Cu-Mg alloy designed for SLM (Zhang et al., *Addit. Manuf.* 38 (2021) 101829) | Thermo-Calc/Scheil growth-restriction factor *Q* and crack-susceptibility index from one run; Ti/Al₃Zr-style inoculation | Edison |
| [`si-addition-al-cu-mg`](si-addition-al-cu-mg/tokenized.md) | Effects of Si addition on Al–Cu–Mg in the α + S + T phase field (Chen et al.) | Trace Si as a phase-selecting microalloyant (T → S phase) | Edison |
| [`fe-si-al-mg-cu`](fe-si-al-mg-cu/tokenized.md) | Second-phase precipitates & dispersoids in 2024 Al after aging (Staszczyk et al.) | Fe/Si embrittlement and solute consumption — detrimental-intermetallic penalty | Edison |
| [`al6fe-strengthening`](al6fe-strengthening/tokenized.md) | Thermal stability of refined Al₆(Fe,Mn) formed in LPBF (Wang et al., *J. Alloys Compd.* 992 (2024) 174593) | Mn stabilization of Al₆(Fe,Mn), suppression of brittle θ-Al₁₃Fe₄; equilibrium-vs-kinetics caveat | Built directly¹ |
| [`al-zn-mg-cu-si-thermal-stability`](al-zn-mg-cu-si-thermal-stability/tokenized.md) | Superior thermal stability in a high-strength Al–Zn–Mg–Cu–Si alloy via tailored precipitation sequence (Mo et al.) | Zn/Mg ratio tunes η vs. the more stable T phase; thermal stability of precipitates | Edison |
| [`al-mg-zn-sciadv`](al-mg-zn-sciadv/tokenized.md) | Step-like interfacial structure of η₄ precipitates in Al-Zn-Mg (Kim et al., *Sci. Adv.* 2023) | Atomic-scale η-precipitate interface structure underpinning Zn/Mg strengthening | Built directly¹ |

¹ **Built directly:** for these articles the Edison ANALYSIS jobs were still running at the
end of the prior session and their task IDs were not recorded, so the `tokenized.md` /
`tables.md` / `figures-captions.md` were reconstructed from the committed
`fulltext.txt` (a faithful `pdftotext -layout` extraction) and the already-extracted
`figures/`, in the same format as the Edison outputs. They carry no
`edison-trajectory.json` and their companion files note the provenance in a header
comment. (Edison's API key was unavailable in the action environment used to finish
this work.)

> Note on three titles: the folder slugs predate retrieval of the actual PDFs, so a few
> are looser than the papers they hold — `al6fe-strengthening` is really about the
> ternary Al₆(Fe,**Mn**) phase, `al-mg-zn-sciadv` is the η₄-interface paper rather than a
> Zn/Mg-ratio strength-vs-heat study, and `titanium-thermocalc` is the crack-free
> Ti-modified Al-Cu-Mg SLM paper. Slugs were left unchanged to preserve links.

---

## Cross-article synthesis

This synthesis was drafted by reading the eight tokenized reference articles directly (the Edison API was unavailable in this run), with quotes pulled verbatim from each `tokenized.md`.

- **Make printability a screened CALPHAD output, not an afterthought.** The MIT/Olson supplemental drives composition design by inverse-optimizing a coarsening metric while "All other microstructural features are forward predicted and work as constraints for the inversely designed composition," contour-mapping freezing range, CSC, and HCS over the Ni–Zr space. **[adma-strengthening-phases-suppmat — Methods/Experimental]** → relevance: validates the lab's plan to emit freezing-range / crack-susceptibility / coarsening scores per candidate and treat them as Bayesian-optimization constraints rather than post-hoc checks.

- **Low diffusivity is the lever for coarsening resistance, and Zr dominates it.** In the screening study "Zr has the greatest influence on the diffusion resistivity, increasing it by 0.78," and "the diffusion resistivity is more influential, decreasing the coarsening metric (by 0.96) than the misfit strain (by 0.22)." **[adma-strengthening-phases-suppmat — Methods/Experimental]** → relevance: supports prioritizing Zr (and Er) in the Al-Zr / Al-Mn-Cr-Zr palette and weighting a diffusion-resistivity proxy heavily in any thermal-stability or precipitation-kinetics score.

- **Mn stabilizes Al₆(Fe,Mn) and suppresses the brittle θ-Al₁₃Fe₄ phase, decoupling strength from printability.** Wang et al. stabilize Al₆Fe "by introducing third elements into the Al–Fe binary alloy to achieve superior mechanical performance without losing printability," because the brittle θ phase "causes a significant crack propagation along the melt pool boundaries." **[al6fe-strengthening — 1. Introduction]** → relevance: a concrete Mn-microalloying rule for the Al-Mn-Cr-Zr family, and a flag that Fe-bearing candidates need a θ-phase / detrimental-intermetallic penalty in the mineral-burden and printability scoring.

- **CALPHAD equilibrium fractions can overpredict detrimental phases; couple them with kinetics.** Despite calculated equilibrium showing comparable θ and Al₆(Fe,Mn) fractions, "the θ-Al13Fe4 phase was scarcely found even after long-term exposure to 500 ℃," attributed to "sluggish kinetics... due to the low diffusivity of Fe and Mn elements." **[al6fe-strengthening — Abstract]** → relevance: cautions that pure-equilibrium Thermo-Calc fractions may overstate intermetallic burden; pairing with Scheil/diffusion-length estimates (already in the pipeline) gives more realistic down-selection.

- **Ti gives grain refinement and CET without worsening hot-cracking — a Scheil-quantified design win.** Zhang et al. find "the Ti addition can strongly improve the growth restriction factor, but have little effect on the crack susceptibility index," with crack-free density rising from 96.7% to 99.7% via in-situ Al₃Ti inoculants. **[titanium-thermocalc — 5. Conclusions]** → relevance: a template for computing both Kou's |dT/d(fs)^1/2| index and growth-restriction factor Q from one Scheil run, exactly the dual-output screening the lab targets for Ti/Zr/Sc inoculant additions.

- **Use the growth-restriction factor Q as a quantitative, ranked grain-refinement screen.** "The Qtrue values of Al-Cu-Mg alloy without the Ti addition and 1.5 wt% Ti/Al-Cu-Mg alloy are 11.37 K and 277.60 K, respectively," mapping via d = K(1/Q)^(1/3) to a ~3× grain-size reduction. **[titanium-thermocalc — 3. Results]** → relevance: Q is a cheap, CALPHAD-derivable descriptor the lab can compute across the 16-element palette to rank inoculant potency and printability before any print.

- **Zn/Mg ratio is a tunable knob that selects between η (coarsening-prone) and the more stable T phase.** Mo et al. note that "By reducing the Zn/Mg ratio to near 1... the precipitated strengthening phases transition to the more thermally stable T phase, thereby achieving an optimal balance between strength and thermal stability." **[al-zn-mg-cu-si-thermal-stability — Methods/Experimental]** → relevance: a composition-ratio rule for any Zn/Mg-bearing candidates in the palette, expressible as a CALPHAD solvus / phase-field constraint in the screening objective.

- **Trace Si steers Al-Cu-Mg precipitation from T-phase toward S-phase — a microalloying selection rule.** Chen et al. show "The addition of Si stimulates the precipitation of the S phase, and restrains the formation of the T phase. The precipitation of T-phase is almost completely suppressed when the Si content reaches 0.5 wt.%." **[si-addition-al-cu-mg — Conclusions]** → relevance: confirms Si as a phase-selecting microalloyant in Cu-Mg families and warns that small Si moves shift the equilibrium phase field, which the CALPHAD screen must resolve at fine composition steps.

- **Si and Fe are detrimental-intermetallic formers that consume strengthening solute — penalize them in the mineral-burden score.** Staszczyk et al. conclude "higher Si and Fe contents prevent the θ and S phases from growth," forming complex multiphase / core–shell particles instead because Si/Fe "extracts Cu and Mg from the supersaturated solution." **[fe-si-al-mg-cu — Conclusions]** → relevance: justifies treating Fe/Si as penalized impurities in the mineral-burden and detrimental-intermetallic scoring, important since recycled/critical-mineral feedstocks (Topic 3B) carry elevated Fe/Si.

- **CALPHAD + global optimization is the only tractable route through trillion-scale composition spaces — the core Topic 3B thesis.** Menou et al. couple CALPHAD, SSH and density models in an NSGA-II run where "about eight million alloys were evaluated," concluding "Computational design combining physical models with data mining was the only way to discover such an alloy; experimental trial-and-error approaches would be unfeasible." **[computational-alloy-design — Conclusions]** → relevance: direct precedent for the lab's high-throughput CALPHAD → Bayesian-optimization / pKGFN pipeline, including the Pareto trade-off framing (strength vs. single-phase stability vs. density) that maps onto strength / printability / mineral-burden objectives.
