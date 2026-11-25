# Vacuum, air ingress and the purge: the frame + floor plate, the pump, and what reaches the melt pool

Written 2026-11-23 for [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer
to: "How does the ability to hold a vacuum and reduce air ingress get affected by no longer using the solid block for the
chamber? Also, in this system do we do a vacuum followed by inert gas backfilling? If so, is it a turbo or a roughing
pump? How is that going to affect the prints?"

The numbers come from [`analysis/seals/vacuum_purge.py`](analysis/seals/vacuum_purge.py)
([results](analysis/out/seals/vacuum_purge.md)). It reuses the seal-by-seal budget in [`seals.md`](seals.md) and the floor
joint in [`chamber-construction.md`](chamber-construction.md). Nothing has been built, leak-tested or measured: these are
models, and their inputs (permeability, outgassing, powder moisture) are uncertain by a factor of 2–5.

## Short answers

1. **The frame + floor plate makes the chamber a little leakier on paper, and riskier only when the floor comes off.**
   - **It adds one seal:** a 947 mm FKM face O-ring under the walls, plus 4 bonded washers on the rail-hole plugs. The
     block had neither.
   - **Air that gets in by permeation rises 26 %.** During a build, O₂ goes from 1.76 to 2.21 ppm/h with no make-up gas,
     and the argon make-up that holds 10 ppm O₂ goes from 37 to 47 sccm. That's about 0.6 L of argon more per hour.
   - **A well-made static O-ring joint doesn't leak.** The real risk is a defect left when the floor is put back on. A
     20 µm channel across the seal land, about one fine powder grain, lets in 8 × 10⁻³ mbar·L/s at vacuum, 80 times the
     whole machine's leak budget. This seal sits at the bottom of the chamber, where powder collects.
   - **The rate-of-rise test catches it.** A channel wider than about 8 µm fails the acceptance test in `seals.md` §7, so
     run it after every reassembly.
   - **During a build such a leak lets no air in.** At +20 mbar argon flows out through it fast enough that O₂ can't
     diffuse back (Péclet 16–320 for 10–45 µm channels). O₂ still comes in through the rubber itself, because overpressure
     doesn't stop permeation.
   - **The joint itself holds.** Atmospheric pressure presses it shut at vacuum, and the screws keep it shut at +20 mbar
     (Shigley separation factor ≥ 3.2). The new crevices empty in under a second and the plugged rail holes in about
     20 s, so neither is a virtual leak.
2. **Yes: vacuum, then argon back-fill, three times, then the build runs at +5–20 mbar of argon.** The sequence is
   [below](#the-atmosphere-cycle).
3. **It's a roughing pump, with no turbo.** BOM line G2 is an Edwards nXDS6i dry scroll: oil-free, 6.2 m³/h peak pumping
   speed, 0.02 mbar ultimate.
   - **Speed:** with a throttled start, it pumps the 11.3 L gas envelope to 1 mbar in about 1.1 min. One cycle takes about
     3.6 min, and three take about 11 (1.5, 4 and 12 min until round 6, when the soft-pump check started reading the jar's
     real depth from the model: [`analysis/out/seals/vacuum_purge.md`](analysis/out/seals/vacuum_purge.md)).
   - **Three cycles reach the argon's own impurity:** 1.2–2.2 ppm O₂ in theory, with Ar 5.0 at 1–2 ppm.
   - **Why no turbo:** it would get there in one cycle instead of two, but no lower. It needs this pump as its backing pump
     anyway, and fine powder in a turbo wrecks it.
4. **Effect on prints: the pump and the floor joint change nothing you'd measure. Water in the powder matters far more.**
   - **We print at about 1 atm of argon, not in vacuum.** The melt pool, plume and spatter behave as in commercial argon
     machines. The vacuum only takes the air out first.
   - **Oxygen:** this machine starts a build at ~1–2 ppm O₂ in theory, and probably a few to tens of ppm at the sensor,
     against 100–1,000 ppm for flow-purged commercial machines.
     For AlSi10Mg, going from 1,000 to 100 ppm changed tensile properties by only 1–6 %
     ([Baroutaji et al. 2023](https://doi.org/10.3390/ma16010430), EOS M 290). The floor joint's +0.45 ppm/h is far below
     anything that matters.
   - **Water:** this is where aluminium is sensitive, because water splits in the melt pool and leaves hydrogen pores.
     The powder carries 100 times more water than the walls and seals give off: 150 g at 150–300 ppm by mass is
     2,500–5,000 ppmv in the loop if the hot plate drives it off.
   - **No pump removes that water at room temperature.** Dry the powder (vacuum oven), handle it dry, and use the
     dew-point sensor (BOM G9) with the make-up flow.

## The frame + floor plate against the block

### What changed in the gas envelope

| | Block (before 2026-11-20) | Frame + floor plate (now) |
|---|---|---|
| Body joints | none | one 947 mm FKM 75A face O-ring (3.53 mm cord, Parker gland, 25 % squeeze), metal to metal, 18 × M4 |
| Rail mounting | 4 inserts blind in the back wall's inside face: screws in blind holes inside the envelope, a classic virtual leak | 4 holes tapped through the wall, plugged from outside on bonded washers: 4 small outer seals instead |
| Interior | 280 × 190 × 120 mm, R5 corners and coves | the same, R10 vertical corners; the floor meets the wall at a clamped hairline, 1.5 mm deep to the O-ring |
| Gas envelope | 11.3 L (chamber 6.4 L) | unchanged |
| Walls cut through the plate's thickness | yes (6 in. block) | yes (5-1/2 in. plate): the same for both, see [material](#material-and-machining) |

### Permeation (the air that comes in through the rubber)

| Design | O₂ in during a build (ppm/h, no make-up) | H₂O in (ppm/h) | Ar make-up for 10 ppm O₂ | Rate of rise at vacuum from permeation |
|---|---|---|---|---|
| Block | 1.76 | 15.8 | 37 sccm | 3.2 × 10⁻⁴ mbar/min |
| Frame + floor plate | 2.21 | 19.9 | 47 sccm | 4.0 × 10⁻⁴ mbar/min |
| The floor joint alone | 0.45 | 4.1 | 9.6 sccm | 0.8 × 10⁻⁴ mbar/min |

- The floor cord is taken at 60 °C, which is conservative. It runs under the walls, away from the heated module, and at
  40 °C its share is 0.42 times this.
- Overpressure doesn't stop permeation. O₂ dissolves in the rubber on the room side and diffuses through, driven by its own
  partial pressure, whatever the total pressure inside. That's why the make-up flow exists.
- Per unit of partial pressure, water permeates FKM 130–200 times faster than O₂ (Parker's O₂ value against
  [Sturm et al. 2004](https://doi.org/10.1029/2003JD004073)'s water value, and Sturm's own pair). Room air at 50 % RH holds 15 times less water than O₂, so
  the water column still comes out 9 times larger.

### Real leaks: what the extra seal could cost

A static O-ring face seal on a clean, flat, Ra ≤ 0.8 µm land is tight to well below 10⁻⁶ mbar·L/s; what is left is
permeation. The failure is a defect across the land: a scratch, a hair, a powder grain, a bad splice. Treating it as one
square channel across a 2 mm land in viscous flow (Shah & London):

| Defect channel | Air in at the 1 mbar hold | Rate of rise | O₂ in during a build at +20 mbar |
|---|---|---|---|
| 2 µm | 8 × 10⁻⁷ mbar·L/s | 4 × 10⁻⁶ mbar/min | 6 × 10⁻⁹ sccs, by diffusion |
| 5 µm | 3 × 10⁻⁵ | 1.7 × 10⁻⁴ | 4 × 10⁻⁹ sccs |
| 10 µm | 5 × 10⁻⁴ | **2.7 × 10⁻³: fails the test** | 4 × 10⁻¹³ sccs (Péclet 16) |
| 20 µm (one fine powder grain) | 8 × 10⁻³ | 0.04 | none (Péclet 63) |
| 45 µm (a coarse grain or a hair) | 0.2 | 1.1 | none (Péclet 320) |

Permeation through all the seals brings in 7 × 10⁻⁶ sccs of O₂ during a build, so even the smallest channels add less than
0.1 % to it.

- **At vacuum** a defect matters. A 20 µm channel during each 2 min hold adds about 17 ppm O₂ per purge cycle, and it
  slows the pump-down's last decade.
- **During a build** it doesn't: argon leaves through the channel at 0.2–3 m/s, and O₂ can't diffuse back against that.
  It costs a fraction of a sccm of argon.
- **Where it would come from.** The floor seal is the one at the bottom of the chamber, where powder settles, and it is
  the one that is opened with powder around it. The lid and door seals are opened more often, but they sit higher and are
  easy to wipe.

**Procedure for the floor joint:**
1. Before opening it, vacuum the powder out of the chamber and the floor corner.
2. Wipe the cord and both lands with IPA and lint-free wipes, and look for scratches across the land.
3. After closing it, run the rate-of-rise test before the next build: after ≥ 1 h at ≤ 1 mbar, close the valve and read
   the Pirani for 10 min. It passes under 1 × 10⁻³ mbar/min ([`seals.md`](seals.md) §7).
4. If it fails, find the leak with argon or helium spray and a leak detector. A rented helium leak detector is the one
   place a turbo is useful: it has its own.

The floor comes off only for major maintenance ([`chamber-construction.md`](chamber-construction.md)), so this is rare.

### Virtual leaks

| Volume | Size | Time constant to empty (molecular flow, the slow case) | O₂ if it all came out after back-fill |
|---|---|---|---|
| Floor joint's hairline crevice, inside the O-ring | 35 mm³ at its worst | 0.2 ms | 0.6 ppm |
| Plugged rail holes (between the rail screw's tip and the plug) | 4 × ~20 mm³ | ~20 s | 1.5 ppm |

Both empty during the first pump-down, long before the hold ends, so they don't show in the purge or the rate-of-rise test
after the first few minutes. The block's blind rail inserts were the same kind of trap, so this is a wash.

### Structure: does it still hold vacuum?

From [`chamber-construction.md`](chamber-construction.md) (CalculiX and Shigley):
- **The joint never opens.** At full vacuum the atmosphere presses the floor plate on. At +20 mbar the 18 screws' 24.9 kN
  preload keeps it shut, with a separation factor of 3.2–9.5, including a +0.5 bar regulator fault with the stiffest
  O-ring.
- **Lid on, at full vacuum:** yield safety factor 9.9, against 30 for the block. The largest displacement is 63 µm, at the
  floor plate's centre, against 24 µm for the block. The door land moves 4.3 µm, against 4.1 µm, which is nothing to its
  O-ring.
- **The worst case is the lid off,** with the frame's front wall spanning the door opening: SF 5.1, against 6.4 for the
  block.

### Material and machining

- **Leak paths along the plate's grain.** In thick rolled plate, laminations and stringers run parallel to the rolling
  plane. Both designs cut their walls through the plate's thickness, so a flaw at the plate's mid-plane would cross a
  16 mm wall from inside to outside. The frame is no worse than the block here.
- **The floor plate is cut flat,** so its rolling plane runs parallel to its sealing faces. Only the Ø96 port bore and the
  slots cut across it inside the O-ring.
- **Asks for the shop:**
  - certified T651 plate from a known mill;
  - no MIC-6 or other cast plate for any wall of the gas envelope (cast tooling plate can be porous). The model uses MIC-6
    only for the two module base plates (BOM F4), and neither is part of the envelope;
  - a helium or argon spray over the outside of the walls during the first leak test.
- **Surface finish.** Face both sealing faces of the joint flat to 0.025 mm at Ra ≤ 0.8 µm, as `chamber-construction.md`
  already specifies, and reject any scratch that crosses the seal's path.

## The atmosphere cycle

What the machine does before every build. Times are for the nXDS6i through two 24 in. KF-25 hoses into the 11.3 L envelope.

1. **Close up.** Plate in, powder loaded, door and drawer clamped. The reservoir's lid and dock are sealed
   ([`seals.md`](seals.md) §0).
2. **Soft pump to 100 mbar (about 1 min).** A needle valve beside the main KF-25 valve limits the start to V/S ≥ 25 s, so
   the gas leaving the powder beds doesn't lift them.
3. **Full pump to ≤ 1 mbar (about 0.5 min more).** The main valve opens.
4. **Hold at ≤ 1 mbar, about 2 min (assumed here).** The powder's pores and the walls give up air. A longer hold on the
   first cycle after the chamber has been open also takes off more water.
5. **Back-fill with Ar 5.0 to +20 mbar (about 0.5 min).** It goes through the same flow limit (≤ 25 L/min) and a sintered
   diffuser, so the inrush doesn't blow the bed.
6. **Repeat steps 2–5 twice more.**
   - **Ideal O₂ after each cycle:** 204, 1.4 and 1.2 ppm with argon at 1 ppm O₂; 205, 2.4 and 2.2 ppm with argon at
     2 ppm.
   - **What sets the floor:** after the second cycle, what is left is the argon's own impurity plus what leaks in during
     the holds (0.2 ppm per cycle at the full 1 × 10⁻⁴ mbar·L/s budget).
7. **Start the loop.**
   - The blower starts and the plate heats.
   - The analyser opens the make-up valve to hold O₂ at its setpoint, at +5–20 mbar.
   - The laser is enabled when O₂ is under its setpoint and the pressure is in its window; those two permissives are
     hardwired ([README](README.md) §3.4). This note suggests adding the dew point as a third.

**What a real machine will read.** It will read higher than the ideal numbers: the O₂ that the powder and seals release,
sensor offset, and where the sample is taken all add. Expect a few ppm to a few tens of ppm. Measuring this is phase 2
of the plan ([README](README.md) §5).

**Precedents:**
- Renishaw's AM250 evacuates its chamber and then fills it with argon
  ([Das et al. 2019](https://doi.org/10.1038/s41598-019-50238-5)).
- The ESRF's miniature LPBF used three vacuum–argon cycles to get below 100 ppm (Lhuissier et al. 2022).
- LLNL's synchrotron testbed used a diaphragm and turbo pump, then an argon back-fill (Calta et al. 2018).
- NIST's AMMT can evacuate to about 10⁻³ mbar (Lane et al. 2016).
- All four are via Edison: [`edison/followup-sealing-o2/answer.md`](edison/followup-sealing-o2/answer.md) and
  [`edison/followup-lab-built-lessons/answer.md`](edison/followup-lab-built-lessons/answer.md).
- Most commercial machines (EOS, TRUMPF) flow-purge instead, to about 1,000 ppm, using about 800 L of argon on an
  EOS M 290 (Pauzon et al., via Edison).

## Roughing pump or turbo

| | Roughing pump only (as designed) | Roughing pump + turbo |
|---|---|---|
| Pump | Edwards nXDS6i dry scroll (BOM G2): oil-free, 6.2 m³/h peak pumping speed (6.8 m³/h displacement), 0.02 mbar ultimate, 26 kg, $5,978 new; a used Agilent IDP-3 is about $1,285 ([`cost-scenarios.md`](cost-scenarios.md)) | the same scroll as backing pump, plus a ~60 L/s turbo with its controller and a gate valve |
| Base pressure here | ≈ 0.02 mbar after 5 min (the pump's ultimate, not the walls' outgassing) | 10⁻⁴–10⁻⁵ mbar after an hour or more, limited by the unbaked Al and FKM giving off water and by the KF-25 hose (~0.6 L/s in molecular flow) unless the turbo sits on the chamber |
| O₂ after one cycle | 204 ppm at 1 mbar; 11 ppm if held at 0.05 mbar | 1.2–2.2 ppm |
| O₂ after three cycles | **1.2–2.2 ppm** | **1.2–2.2 ppm**: the argon's own impurity sets both |
| Time | ~3.6 min per cycle, ~11 min for three (round 6) | one cycle instead of two or three: a few minutes faster, if the turbo stays spinning behind a gate valve |
| Water | the walls give up water at a rate that falls as ~1/t; time and temperature set it, not the pump | the same; a turbo lowers the pressure, but the walls dry no faster unless they are heated |
| Powder | an inlet filter (McMaster 3394N12) and the soft-pump start protect the scroll | fine Al powder wrecks a turbo's blades: it needs a filter, a gate valve and a slow start, and still risks a crash |
| Cost | in the BOM | +$5–10k (turbo, controller, gate valve), not priced here |

**Where a turbo would make sense:**
- printing in vacuum or under reduced pressure, which isn't planned;
- an electron-beam machine;
- helium leak detection, where the detector carries its own turbo.

**If a lower O₂ floor is ever wanted,** buy cleaner argon (6.0) or put a point-of-use purifier on the argon line. A bigger
pump won't help. Nothing in the aluminium literature asks for less than ~100 ppm, so it isn't needed now.

## What this does to the prints

**The prints run in about 1 atm of argon, not in vacuum.** The pump and the floor joint only change how clean that argon is
when the build starts, and how much O₂ and water creep in over the hours of a build.

### Oxygen

| Start of build | O₂ |
|---|---|
| Flow-purged commercial machines | 100–1,000 ppm (a typical start threshold is ~1,000 ppm) |
| This machine, 3 roughing cycles | ~1–2 ppm in theory; a few to tens of ppm expected at the sensor (not measured yet) |
| With a turbo | the same |
| During a build | rises ~2.2 ppm/h without make-up (0.45 ppm/h of it from the floor joint); 47 sccm of make-up argon holds 10 ppm |

- **For aluminium, O₂ under ~100 ppm isn't what limits part quality.**
  - [Baroutaji et al. 2023](https://doi.org/10.3390/ma16010430) built AlSi10Mg on an EOS M 290 at 100 and 1,000 ppm. At
    100 ppm, elongation was 5.7 % higher, UTS 3 % lower and yield 1 % lower (via Edison; the authors call it
    preliminary).
  - The README's targets stand: a hard interlock at 1,000 ppm, and operation below 100–200 ppm.
- **Oxides still matter for fatigue.** [Tang (2017)](https://doi.org/10.1184/r1/6720185.v1) found oxide-related pores at
  fatigue initiation in AlSi10Mg; the larger oxides form when metal vapour oxidises during the build. Lower O₂ helps here,
  but the gain from 100 to 10 ppm is not measured in the papers we have.
- **The floor joint's +0.45 ppm/h** is the difference between 37 and 47 sccm of make-up argon. It doesn't change the
  prints.

### Water: the part that matters for aluminium

- **The mechanism.** Water meeting liquid aluminium forms Al₂O₃ and hydrogen. The hydrogen dissolves in the melt and comes
  out as round pores when it freezes, which is how dry argon and dry powder lower porosity in Al builds (Edison's review,
  [`edison/followup-sealing-o2/answer.md`](edison/followup-sealing-o2/answer.md) §2 and §5).
- **Where the water comes from in this machine:**

  | Source | Water in the 11.3 L loop |
  |---|---|
  | Powder, 150 g at 150–300 ppm by mass, driven off by the hot plate | 2,500–5,000 ppmv |
  | Walls and seals, first hour after back-fill | 13–36 ppm, depending on how long the hold was (10–60 min) |
  | Permeation through all the seals | ~20 ppm/h |
  | Ar 5.0 | 1–3 ppm |

- **The powder dominates by about 100 times,** and no pump changes that at room temperature: its water is adsorbed or
  bound in the oxide and hydroxide film, and it comes off when heated.
- **What to do:**
  - Dry the powder in a vacuum oven and load it dry. Lubkowitz et al. (2024) found vacuum-dried AlSi10Mg gave denser parts
    than oven-dried.
  - Make the dew-point sensor (BOM G9) a laser permissive alongside O₂. Today only O₂ and pressure are.
  - Size the make-up flow for water as well as O₂: about 60 sccm holds a −40 °C dew point against the walls and seals
    ([`seals.md` results](analysis/out/seals/seals.md)).
- **The vacuum step does help with water.** Van Cauwenbergh et al. (2019) printed AlSi7Mg0.6 at ~3 ppm O₂ and ≤ 5 ppm H₂O
  after a vacuum pre-cycle, and the parts held 13 ± 4 ppm hydrogen against 45 ± 11 ppm in the powder.
- **The recirculation filter isn't a water source.** McMaster's 9179K14 HEPA element is polyester and fibreglass. Das et
  al. (2019) found cellulose filters in LPBF can hold tens of grams of water.

### What the vacuum step can do badly, and the guards already in the design

| Risk | Guard |
|---|---|
| Pumping down too fast lifts or fluidises the powder in the bed, reservoir and overflow jar (Δp up to 0.95 × the bed's weight in the 90 mm jar) | soft-pump start at V/S ≥ 25 s to 100 mbar ([`seals.md`](seals.md) §6) |
| The back-fill inrush blows the bed | the same flow limit and a sintered diffuser |
| Powder drawn into the pump | KF-25 inlet filter (McMaster 3394N12) on the scroll |
| Powder on a seal when the chamber is closed | wipe and check the lid, door and drawer seals each build; the floor seal procedure above |

### Why not print under vacuum?

- **More evaporation.** At reduced pressure the boiling point drops, so more Mg and Zn evaporate. That would shift exactly
  the compositions we are screening, as the 500 °C note found for heat ([`preheat-and-plates.md`](preheat-and-plates.md)).
- **A wider powder-free strip beside each track.** The metal vapour jet drives a flow of gas that pulls powder in toward
  the track. Between atmospheric pressure and ~10 Torr of argon, the lower the pressure, the wider the denuded zone it
  leaves ([Matthews et al. 2016](https://doi.org/10.1016/j.actamat.2016.05.017); Bidare et al. 2018 found the same).
- **Different conditions.** Results would also not carry over to commercial argon machines.
- **So vacuum is only for purging,** which is all a roughing pump has to do.

## Changes made

- **New:** [`analysis/seals/vacuum_purge.py`](analysis/seals/vacuum_purge.py) and its
  [results](analysis/out/seals/vacuum_purge.md).
- **The purge re-sized for the dry scroll.** `seals.py` still sizes the purge with the McMaster 4396K21 rotary vane
  (3 cfm, 0.013 mbar), which BOM line G2 replaced on 2026-11-22. The scroll does it in about the same time: 1.5 min to
  1 mbar with the throttled start, against 1.6 min. So the conclusions in `seals.md` §6 stand.
- **[README](README.md) §3.4** now says the pump is a roughing pump with no turbo, and links here.

## Not done

- **No measurements.** The first rate-of-rise test and an O₂ and dew-point log through a purge are phase 2 of the plan.
- **The pump's speed curve is a simple model:** S = S₀(1 − p_ult/p) through the hose conductance, with S₀ the listed
  6.2 m³/h peak speed. Edwards' own curve may differ by 10–20 % below 1 mbar, which doesn't change the conclusions. The
  BOM's "6.8 m³/h" for G2 is the displacement, not the pumping speed.
- **The pump's inlet limit.** Edwards lists 200 mbar as the nXDS6i's maximum continuous inlet pressure. Each cycle starts
  from atmosphere for about a minute, which the soft-pump valve throttles, but the duty of repeated cycling isn't checked
  against Edwards' manual.
- **Gas the powder and seals give off after the purge isn't modelled**, apart from water.
- **The floor seal's temperature is assumed (60 °C),** not taken from the thermal FEA.
