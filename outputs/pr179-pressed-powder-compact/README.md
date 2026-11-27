# Would a pressed powder compact fix the charge's melting and mixing? (Edison, 2026-11-02)

Asked on [PR #179](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/179#issuecomment-6590015569):
would uniaxially pressing the powder into a partly dense compact, then melting that in the atomizer, fix the powder
struggling to melt and mix into the rest of the charge? "Semi-solid part" is read here as a partly dense pressed
pellet (green or sintered), not semi-solid metal in the thixoforming sense.

| File | What it is |
| --- | --- |
| [`query.md`](query.md) | The question sent to Edison, with the set-up and run history |
| [`answer.md`](answer.md) | Edison's full answer with inline citations |
| [`references.md`](references.md) | Its reference list |
| [`artifact-00.md`](artifact-00.md), [`artifact-01.md`](artifact-01.md) | The two tables it built: compaction pressure vs density, and the charge options compared |
| [`task_verbose.json`](task_verbose.json) | The whole trajectory: every paper search, evidence snippet and candidate |
| [`_task_id.json`](_task_id.json) | Task `b49700cb-4c69-40d5-ad98-df2fffa43971`, LITERATURE_HIGH, ran 22:28–22:57 UTC |

## Short answer

A compact should melt in better than loose powder, but it is not a dependable fix by itself. Pressing cracks the
oxide skin on each particle without removing it, and it makes the gas problem worse once the pores close. Nobody
has published this exact case (a pressed Al-powder compact remelted in a small induction crucible for
atomization), so Edison's case rests on near analogues: PM sintering, remelting scrap-chip briquettes, and foundry
alloying tablets. Its ranking for 100–350 g charges:

1. Cast master alloys, or solid stock of the alloy itself
2. An arc-melted button made from the weighed powders
3. A pressed compact, only after a bench melt test

## What Edison found

- **Why the powder doesn't merge.** Each particle keeps its Al₂O₃ skin at 810–840 °C. The aluminium inside
  melts, but the skins hold the droplets apart, and a powder bed conducts heat about 100× worse than solid metal.
  Mg turns the skin into MgO/MgAl₂O₄ spinel, which is tougher, so Mg "plausibly explains" why the AlSi10Mg core
  failed (Sept 30) while the Mg-free 4047 core melted (Oct 2). That rests on one run of each, with different powder
  lots, so treat it as a hypothesis.
- **Pressing helps, partly.** Al powder reaches about 85 % relative density at 90–100 MPa and 92–98 % at
  250–580 MPa. Deforming the particles gives some metal-to-metal contact. Cold-pressed chip briquettes (88 % dense)
  remelted by induction at 850 °C gave 94 % metal yield. Edison's suggested window is 200–300 MPa, 90–95 % dense.
- **A 19 mm compact needs** 5.8 t at 200 MPa and 8.7 t at 300 MPa (checked: π × 9.5² mm² × pressure).
  At 100 MPa it needs 2.9 t.
- **The ejection warning is justified** when gas is sealed in: moisture and hydrated oxide on the powder (released
  above ~350 °C), admixed die lubricant, and closed pores. Heat the compact up with the charge from cold, as we
  already do, and never drop it into a melt. Dry the powder first. Use die-wall lubricant only, or none.
- **The oxide still goes into the melt.** Pressing breaks the skins into fragments, which can still reach the
  0.7 mm nozzle. Edison rates the clogging risk "medium–high" for a cold-pressed compact and "low" for clean
  master alloy.
- **Hold longer.** Edison suggests at least 5 min, against our 2. That matches the furnace maker's own rule
  quoted in PR #172 (≥5 min once molten, 10 min when alloying in the furnace).
- **Compacting inside the cup** under a sliding vented plug is rated "medium–high" risk. The Sept 25 Edison review
  (PR #172, experiment E4) had already advised against pressing powder in a near-sealed cup.

## Where it doesn't fit our set-up

- **Its density window contradicts its own numbers.** Edison says pores start to close at about 85 %, then
  recommends 90–95 % "with connected vent paths". At 90–95 % the compact is already partly sealed. Our set-up
  makes this matter more: the gas washes at 500 °C (#159) pump the chamber down while everything is still solid.
  A compact with open pores (about 85 %, ~100 MPa) is degassed in place. A 90–95 % compact keeps its gas, and so
  does a press-fit cup.
- **"Blend with Al powder to dilute the oxide" is wrong.** Oxide scales with particle surface, so adding Al powder
  adds oxide to the charge. The only gain is that softer Al particles press together better. Dilute with solid 6063.
- **The 25–40 min tablet times are for Ti-powder tablets.** Ti has to *dissolve* into the aluminium. Our 4047 and
  AlSi10Mg powders are already liquid at 810 °C; they only have to *coalesce*. Those times apply to future
  elemental additions (Si, Mn, Fe, Ni, Zr), not to the current powders.
- **"Put the compact at the bottom"** would put it on the floor cone that feeds the nozzle. In our crucible it would
  sit off to one side of the pour hole, in the gap beside the sealing rod. Any sponge or skin left there is the
  first thing poured.
- **Don't run the melt test in the atomizer.** The charge would freeze around the sealing rod. Use a small crucible
  in a furnace with an argon purge.
- **Si dissolution was asked about but not answered.** The Sept 25 review's numbers still stand: Si cylinders at
  738 °C were only 29–44 % dissolved after 2–3.5 min. Use Al-Si master alloy instead.
- **The evidence is thin in places.** Two key sources are theses, and the 94 % briquette yield is from a 2026
  preprint. Chips also carry tens of times less oxide per gram than 15–45 µm powder. The steam-explosion source is
  a 1960 report on uranium.

## What I'd do

1. **For the 4047-in-6063 composition spread, skip the powder.** Weigh solid 4047 (as in the Oct 21 and 22 runs)
   against solid 6063. The spread then needs no cup at all.
2. **For Mg-bearing or elemental additions,** use Al-Si, Al-Mg, Al-Cu, Al-Mn or Al-Zr master alloys where they
   exist. Otherwise arc-melt the weighed powders into a button first. That is AMAZEMET's advice from the 9/17 call
   (#140), and the arc melter at the U is already an option (#153).
3. **If you try a compact,** do the bench test first. Make four pellets of one powder: loose (as a control),
   ~100 MPa (~85 %, vents), 200 MPa and 300 MPa. Dry the powder at 80 °C or more, and use no admixed lubricant.
   Heat each pellet alone in a crucible under argon to 850 °C and hold for 5 min.
   - A pellet that pulls into one shiny bead coalesces.
   - One that keeps its shape is a sponge of skinned droplets, which is what the Sept 30 core did.
   - Then run Edison's fuller test on the winners: the pellet under 6063 pieces, sectioned, with EDS for uniformity
     and the dross weighed.
   - Running AlSi10Mg and 4047 pellets side by side also tests the Mg explanation.
4. **Whatever the charge,** try a 5–10 min hold before going hotter. Going hotter costs Mg, picks up H, and makes
   more Al₄C₃ on the graphite.
