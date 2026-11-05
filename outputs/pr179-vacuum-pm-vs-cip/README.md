# Vacuum die pressing or CIP for pure-Al green parts? (Edison, 2026-11-05)

Asked on [PR #179](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/179#issuecomment-6647458425):
pros and cons of powder metallurgy under vacuum and of cold isostatic pressing (CIP), which makes the safer
green part from pure aluminium powder for the atomizer, and how the two compare on simplicity, speed, cost and
whether the part melts and mixes in.

"Powder metallurgy under vacuum" is read here as uniaxial die pressing with the powder evacuated (an evacuable
die, or a die in a vacuum chamber), with vacuum degassing or vacuum hot pressing as extensions. CIP is cold
isostatic pressing of powder sealed in an elastomer bag.

| File | What it is |
| --- | --- |
| [`query.md`](query.md) | The question sent to Edison |
| [`literature-high.md`](literature-high.md) | Edison's deep-search answer (LITERATURE_HIGH) with inline citations |
| [`literature-high.references.md`](literature-high.references.md) | Its reference list, with DOIs |
| [`literature-high.artifact-00.md`](literature-high.artifact-00.md), [`literature-high.artifact-01.md`](literature-high.artifact-01.md) | Its two tables: the pros-and-cons comparison and the starting recipes |
| [`literature-high.verbose.json`](literature-high.verbose.json) | The whole trajectory: every search, evidence summary and candidate |
| [`literature.md`](literature.md), [`literature.references.md`](literature.references.md), [`literature.verbose.json`](literature.verbose.json) | The same question as a standard search (LITERATURE), used as a cross-check: answer, references, trajectory |
| [`_task_ids.json`](_task_ids.json) | Task ids: `563cb545-…` (LITERATURE_HIGH, 01:59–02:26 UTC) and `31cfe6f4-…` (LITERATURE, 01:59–02:33 UTC) |

Before commit, the trajectory JSON had its account fields (`user`, `build_owner`, `permitted_accessors`), cost
fields, and the raw page text returned by Edison's `read_text` tool removed, since this repo is public. Evidence
summaries, the agent's messages and tool calls, and source metadata (titles, authors, DOIs) are kept. Both tasks
finished with status `success`.

## Short answer

Edison prefers vacuum uniaxial die pressing (A) over CIP (B), and I agree, but the reasons are narrower than
Edison's table suggests. Four properties make a green part safe to melt, and both routes can deliver them:

1. **Open pores, checked rather than assumed.** Gas has to get out during the heat-up and the 500 °C gas washes,
   before melting seals the surface. The deep search puts pore closure at 85–90 % dense, but the standard search
   found no measured threshold for pure Al, and degassing practice keeps preforms near 65–75 %. So aim for the
   lowest density that survives handling, and test that gas flows through a sacrificial slug.
2. **No organics or fluids.** That means no lubricant mixed into the powder, no oil or water from a CIP bag, and
   no mould release agent.
3. **Dry powder, stored dry.**
4. **No cracks or loose powder.**

What separates the routes is what usually goes wrong:

- **A:** Aluminium galls in a steel die, so ejection tends to call for a lubricant. Tall slugs also come out with a
  low-density zone and can laminate. Both are avoided by pressing short slugs, with at most a dry die-wall film.
- **B:** A leaking bag puts oil or water into the powder, and that part has to be scrapped. The diameter is also
  set by the bag rather than a die, so it has to be found by trial.

Evacuating the die or the bag removes the air, which is the smaller gas source. The larger one is the water bound
in the oxide skin, and only heat removes it (see below).

Neither route fixes the melting and mixing problem itself: every particle keeps its oxide skin. Pure Al powder has
no Mg, so its skin is plain alumina. A pure-Al compact should therefore behave more like the 4047 core that melted
in (Oct 2) than the AlSi10Mg core that didn't (Sept 30). That still needs the bench test before an atomizer run.

## Pros and cons

| | A: uniaxial die, evacuated | B: CIP |
| --- | --- | --- |
| **Safety of the part in the atomizer** | ✅ No fluid contact; exact size<br>❌ A lubricant, if used, adds gas and carbon<br>❌ Tall slugs have a low-density zone and can laminate | ✅ No lubricant; uniform density<br>❌ A bag leak puts oil or water in the powder, so the part must be scrapped<br>❌ Pores close at a lower pressure than in a die (next row) |
| **Density vs pressure** | About 80 % at 100 MPa and 95 % at 500 MPa for an Al premix with 1.5 % wax (Alumix 321, 15 mm single-action die). The Nov 2 answer had Al at about 85 % near 100 MPa | Al powder: 85–95 % at 104–138 MPa in 6.35 mm rubber bags (Anderson & Foley 2001); 98 % at 600 MPa (Eksi 2007) |
| **Density uniformity** | ❌ Friction leaves the far end (single action) or the middle (double action) least dense, and this gets worse as the slug gets taller | ✅ Uniform, if pressure is held about 60 s before release |
| **Green strength, shedding** | ✅ Good, with crisp edges<br>❌ End-capping and lamination on ejection | ✅ Good<br>❌ Rounded edges, bag wrinkles; slow release needed to avoid springback cracks |
| **Lubricant** | Usually needed on the die wall; never mixed in | None |
| **Contamination** | Die wear, O-ring grease, die-wall film | Bag material, release agent, fluid ingress |
| **Oxide cracking** | Slightly more shear at particle contacts (inferred, not measured) | Less shear |
| **Fits the 20 mm limit** | ✅ Exactly 19.0 mm from the die | ❌ Bag oversize must be found by trial. In a 22 mm vessel, expect parts of about 17 mm (my estimate, from about 12 % linear shrinkage plus the bag wall) |
| **Process hazards** | Dust while filling; powder drawn into the vacuum line (fit a filter); vent with argon, slowly | Dust while filling bags; a small high-pressure oil vessel (guard it and keep the closure retained) |
| **Time** | About 10 min per slug | About 20–30 min per cycle (fill, evacuate, seal, press, slow release, strip, inspect). Toll pressing takes days to weeks |
| **Equipment (list prices, Nov 2026)** | 20 mm evacuable die: Specac Atlas about $2.5–2.8k; MTI die with vacuum port, 2–25 mm bore, rated to 400 °C, about €675. Needs a press of at least 10 t | MTI CIP20D die set (22 mm bore, 400 MPa, sits in a hydraulic press) $1,998; MTI YLJ-CIP-15 (22 mm, 380 MPa, glovebox-sized) $4,698; MTI YLJ-CIP-20B (30 mm, 330 MPa) from $9,998. Toll services publish no prices |
| **Simplicity** | ✅ Fewest steps | ❌ More steps, and bag integrity has to be checked every time |

Both routes need a press unless CIP is sent out. A 15 t manual lab press lists at roughly $4.6k–12k new. A 19 mm
die needs 2.9 t at 100 MPa, 5.8 t at 200 MPa and 8.7 t at 300 MPa. The prices are vendor list prices read from
search results on Nov 5, not quotes.

## What Edison found

- **Gas in the powder.** Air- and nitrogen-atomized Al-alloy powders carried 13–25 ppm H, or 14.7–27.5 mL H₂ per
  100 g. That is 50–100× a degassed casting, and nearly all of it is water in the oxide skin. Physisorbed water leaves at
  100–200 °C, hydrated oxide converts at about 350 °C, and H₂ release peaks near 450 °C.
- **In-place degassing works if the pores are open.** A compact under about 85–90 % density, heated slowly through
  the washes to 500 °C, should lose most of that water before melting closes it in.
- **Evacuating before pressing** to 10 mbar removes about 99 % of the free air, but none of the oxide-bound water.
- **Blends with elemental Ni, Ti, Fe or Zr powder are discouraged.** Pressed Al–Ni ignites in a self-propagating
  reaction near 640 °C (the Al–Al₃Ni eutectic), below our melt temperature and possibly before the charge around it
  has melted. Use master alloys.
- **Al powder is a combustible dust.** Ground every part, filter the vacuum line, vent with dry argon, keep a
  Class D extinguisher or dry sand, and never use water.
- **Vacuum hot pressing is overkill.** The cited run took 5 h at 550 °C and 175–245 MPa. The result is fully dense
  and gas-free, but that is far more than remelt feed needs.
- **Edison's pick:** A, with lubricant-free, double-action pressing of short slugs (H/D ≤ 1.5) after drying the
  powder. B only with pre-degassed powder in a dry, evacuated double bag, scrapping any part whose bag leaked.

## Where Edison's answer is wrong or doesn't fit

- **Its pressures overshoot its own density target.** It cites Al-powder CIP reaching 85–95 % at 104–138 MPa,
  then recommends 150–250 MPa for 85–90 %. For die pressing it recommends 200–300 MPa for 85–90 %, yet its own
  die data (about 80 % at 100 MPa, 95 % at 500 MPa) and the Nov 2 answer (about 85 % near 100 MPa, 92–98 % from
  250 MPa) put 200–300 MPa near or above 90 %, where pores start to close.
  - To stay at or below about 85–88 %, expect roughly 100–150 MPa in a die and about 100 MPa or less in CIP.
  - Measure a pressure-to-density curve on our powder (geometric density from mass and calipers, no liquids)
    before choosing.
- **The "vacuum" in vacuum pressing removes the smaller gas source.** Take a 30 g slug at 88 %: it has about
  1.5 cm³ of pores.
  - Air sealed in those pores would reach about 3 atm at 660 °C.
  - The oxide's 13–25 ppm H is 4–8 mL of H₂ at STP. In the same pores at 660 °C, that is about 10–19 atm.
  - So the heated degassing matters more than evacuating at room temperature. With open pores, both gases get out
    anyway.
- **"Oxide skins float up as dross" is unlikely here.** Alumina (3.6–4.0 g/cm³) is denser than liquid aluminium
  (about 2.37 g/cm³). Skins that hold no gas will tend to settle toward the bottom-pour nozzle.
- **"90–95 % metal yield" is optimistic.** It comes from machining-chip briquettes, which carry far less oxide per
  gram than 15–63 µm powder. Even for chips, Puga et al. (2009) got 81–91 % incorporation under argon at 850 °C. The
  94 % figure is from a 2026 preprint.
- **Its dust numbers are for finer powder.** MIE "below 1 mJ" and K_St up to 1100 bar·m/s describe fine and
  nano powders. A 40 µm Al powder measured K_St 77 bar·m/s, MIE about 60 mJ and MEC 35 g/m³
  ([Wu et al., Aerosol and Air Quality Research](https://aaqr.org/articles/aaqr-09-06-oa-0043)), read from a search
  summary and not checked against the paper. The precautions still apply, because the fines
  in any lot set the risk.
- **The CIP cost is overstated.** Small CIP dies that sit in a hydraulic press list at $2–5k, the same range as an
  evacuable die. The press is the larger cost for either route.
- **Its CIP stored-energy warning is overstated.** For a 25 × 100 mm vessel of oil at 300 MPa, the energy in the
  oil is about 1 kJ (p²V/2K, with K ≈ 2 GPa), far less than a gas cylinder holds. The real risks are the closure and the fittings.
- **A 350 °C, 2–5 h vacuum pre-degas with glovebox transfer is heavy for this use.** For an open-pore part, the
  heat-up and the 500 °C washes do that job in place. A 100–150 °C vacuum-oven dry before pressing, and a
  desiccator for storage, cover the physisorbed water. One sacrificial slug taken through the real heat-up is the
  check.

## Cross-check: the standard search

The standard LITERATURE search on the same question ([`literature.md`](literature.md)) reaches the same
recommendation: try small, lubricant-free, vacuum-dried, die-pressed slugs first, and don't buy a CIP for this. Send
parts out for CIP only if die-pressed slugs shed powder or crack, and then only with a completely dry bag process.
It is more cautious than the deep search, and adds three points:

- **There is no measured pore-closure density for pure Al.** Degassing practice keeps preforms near 75 % dense, and
  one Al–20Si study pre-pressed to about 65 % to keep the pores connected. Bulk density is not a permeability test.
- **The water comes from humid storage.** Gas-atomized 99.99 % Al (about 25 µm) held 24 h in humid air released
  H₂O from about 207 °C (peak 447 °C) and H₂ peaking near 452 °C. The same powder held in dry air or argon gave no
  detectable H₂. Keep the powder and the pressed parts dry. It also confirms that the 13–25 ppm H figures come
  from air-atomized alloy powders, not pure gas-atomized Al.
- **More compaction can make melt-in worse.** In Puga et al. (2009), chip briquettes pressed at 300 bar gave 88–91 %
  incorporation, and at 500 bar only 75–78 %, because the melt penetrated them less. Those briquettes took 50–70 min
  to melt into a roughly 15 kg charge, so the times don't carry over to our 2–10 min hold.

It also warns that an argon backfill isn't vacuum extraction. Leave the charge at about 500 °C until the chamber
pressure and oxygen settle, rather than going straight to melting. A Ti–Al pressed mix showed its first exotherm at
520–570 °C, below the Ni–Al figure.

## What I'd do

1. **If you try green parts, start with A.**
   - Use a 19–20 mm evacuable die with a powder filter on the vacuum line, in a press of at least 10 t.
   - Press short slugs, 19 mm across and at most 25 mm tall (about 12–15 g), and stack two or three in the charge.
   - Mix no lubricant into the powder. Use a dry die-wall film only if ejection needs it. A dry hBN film is worth
     trying, since hBN is already on the crucible and nozzle (my suggestion, not tested).
2. **Measure a pressure-to-density curve from 50 to 200 MPa,** and press at the lowest pressure that gives a slug
   you can handle (probably 75–85 %). Check on a sacrificial slug that gas flows through it.
3. **Run the bench melt test from the Nov 2 review before the atomizer.**
   - Loose powder against slugs at about 85 % and about 92 %, each in a small crucible under argon at 850 °C, held
     5 min.
   - A slug that pulls into one shiny bead coalesces.
   - Weigh the dross and section the bead.
4. **Use CIP only if you need long one-piece slugs, or if the die-pressed slugs laminate.**
   - Use a small oil-medium vessel, and evacuated double bags filled in a dry place.
   - Press at about 100 MPa or less.
   - Scrap any part whose bag lost vacuum or came out wet or oily.
5. **Don't blend elemental Ni, Ti, Fe or Zr into the Al.** Use master alloys.
6. **The Nov 2 ranking still stands.** Cast master alloys or an arc-melted button beat any green compact for
   melting in, for oxide and for nozzle safety. Green parts make sense only for compositions with no master alloy.
