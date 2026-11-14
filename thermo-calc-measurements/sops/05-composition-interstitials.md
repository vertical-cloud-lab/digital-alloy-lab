# SOP 05 (draft): composition (ICP-OES) and O/N/H (inert gas fusion) for powder and printed parts

**Why it comes first:** every Thermo-Calc and pycalphad number we compare against must be computed for the
*measured* composition. EDS isn't accurate enough at the 0.2–0.5 wt% level the campaign needs
(#255 transcript, 10:36–11:29). The same measurements also check:
- the AM Module's evaporation mode: Mg (and Zn, Li) lost between powder and print;
- the oxide content of the powder, which drives lack of fusion and balling in Al.

Draft. It's a send-out procedure; the schedule in #256 already plans an "O/ICP batch 1".

## What to send
| Sample | Mass | Split | Measure | Why |
|---|---|---|---|---|
| Powder, every run (20–63 µm cut) | 2–5 g | riffle splitter | ICP-OES, all intended elements plus Fe and Si | composition for Thermo-Calc |
| Powder, every run, sealed under Ar within 48 h of atomizing (#256 already plans 5 g) | 1–2 g | the same | O, N, H by inert gas fusion | oxide and moisture; the powder-quality axis |
| Printed cube, one per alloy per build | ~1 g of chips, dry-cut | – | ICP-OES (Mg, Zn and other volatiles at least) | evaporation loss vs the AM Module |
| Feedstock (the bar and master alloys in the cups and plugs) | 2 g | – | ICP-OES | mass balance through the atomizer |
| A certified reference material of a similar Al (or Cu) alloy | per lab | – | the same | lab accuracy check |

## Handling
- **Tools and containers:** clean, dry plastic or stainless tools; new screw-cap vials or heat-sealed bags flushed with Ar;
  no paper envelopes.
- **Labels:** run ID, sieve cut, date atomized, date sealed and the requested analytes. Log each
  sample in the run record (#159) with its chain of custody.
- **Duplicates:** send a blind duplicate of every tenth sample.
- **Ask the lab for:**
  - the ICP-AES/OES method for Al alloys they follow (Edison q2 names ASTM E3061);
  - method detection limits;
  - the digestion used (Si-bearing Al alloys need HF or a fusion digestion to keep Si in solution; ask how they handle Si,
    the open question in #255);
  - uncertainty for each element.

## Analysis
- **Recalculate:** Thermo-Calc / pycalphad equilibrium and Scheil for the measured composition.
  Store both the nominal and the measured result.
- **Evaporation loss:** ΔX/X = (X_powder − X_print)/X_powder for each volatile element, set against
  the AM Module's evaporation-mode prediction at the same P, v and hatch.
- **Oxygen:** compare with the surface-area estimate (D50 and a ~4 nm native oxide, an assumption to check
  against XPS if available). A large excess points to oxide inclusions from the melt.

## Open questions
- Is there an on-campus ICP-OES with HF/fusion digestion for Si-bearing Al (see the README's access table)?
  If not, budget a commercial lab. Prices and turnaround aren't quoted here.
- Spark-OES or XRF on printed coupons would be faster for routine checks. Validate them against
  ICP-OES on 3–4 alloys before relying on them.
