# CubXL pipette protocols, copied from byu-vcl

These are the CubOS config files for the P20 pipette runs on the CubXL, brought over for
[#236](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/236). Each one is a
byte-for-byte copy of the file at the same path on byu-vcl's `claude/issue-169-20261009-2151`
branch ([byu-vcl#269](https://github.com/vertical-cloud-lab/byu-vcl/pull/269)), at
[`4d5446c`](https://github.com/vertical-cloud-lab/byu-vcl/tree/4d5446c11e82716532fb4f7fc3bd8640f0639239/cubos/configs).
They are the same files the runs below used: each run saved a copy of its configs next to its
results, and those copies match these.

A CubOS run takes three files: a **gantry** file (the machine and its instruments), a **deck** file
(the labware and where it sits) and a **protocol** (the steps).

## `pipette_test` and the mix test

| File | What it is |
|---|---|
| [`configs/protocol/vcl/pipette_test.yaml`](configs/protocol/vcl/pipette_test.yaml) | home → park the capper → decap vial_1 → pick up a tip (A1) → aspirate 20 µL from vial_1 → park the pipette → recap vial_1 → decap vial_2 → blow out into vial_2 → drop the tip (A1) → recap vial_2 → home |
| [`configs/protocol/vcl/pipette_test_mix.yaml`](configs/protocol/vcl/pipette_test_mix.yaml) | `pipette_test` with `mix` (20 µL, 3 cycles, height −35) in place of step 4's `aspirate` in vial_1 and step 8's `blowout` in vial_2 |
| [`configs/deck/ben_2vials_tiprack.yaml`](configs/deck/ben_2vials_tiprack.yaml) | Ben's deck from 2026-10-02: vial_1 and vial_2 at deck (136.668, 45) and (136.668, 78), rims at z 56, and the 2 × 15 tip rack with A1 at (291.332, 89), pick-up z 59 |
| [`configs/gantry/cub_xl_ben_3_instrument.yaml`](configs/gantry/cub_xl_ben_3_instrument.yaml) | Ben's gantry file from 2026-10-02: the capper (offset 0, 0) and the P20 (offset 55, 11), both on the Uno at `/dev/ttyACM0`, plus a camera mount |

Both protocols run on that deck and gantry file.

| Run | Protocol | Plunger driver | Result | Record in byu-vcl |
|---|---|---|---|---|
| 2026-10-02 | `pipette_test` | Tic T500 | 12/12, 160 s | [`pipette_test_20261002c`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/pipette_test_20261002c/README.md) |
| 2026-10-06 | `pipette_test` | Tic T500 | 12/12, 141 s | [`pipette_test_20261006`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/pipette_test_20261006/README.md) |
| 2026-10-07 | `pipette_test` | TMC2209, spreadCycle firmware | 12/12, 137 s | [`pipette_test_20261007`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/pipette_test_20261007/SUMMARY.md) |
| 2026-10-09 | `pipette_test_mix` | TMC2209 | 12/12, 218 s | [`pipette_test_mix_20261009b`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/pipette_test_mix_20261009b/README.md) |

## Two later mixing tests

| File | What it is | Run |
|---|---|---|
| [`configs/protocol/vcl/pipette_test_stir.yaml`](configs/protocol/vcl/pipette_test_stir.yaml) | Stirring with the pipette tip: `pipette_test_mix` with vial_2's `mix` replaced by 61 single-axis moves of the dipped tip, never more than 5 mm from the centre. byu-vcl's [`stir_moves.py`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/tools/stir_moves.py) generated them. Same deck and gantry file as above | 2026-10-12, TMC2209: 74/74, but it didn't mix, because the gantry can't move the tip fast enough ([record](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/pipette_test_stir_20261012/README.md)) |
| [`configs/protocol/vcl/stir_module_trial.yaml`](configs/protocol/vcl/stir_module_trial.yaml) | The first protocol with the stir module on the deck: decap vial_2 → tip on → aspirate 20 µL from vial_2 → recap vial_2 → decap vial_1 → blow out 20 mm below vial_1's rim → recap vial_1 → drop the tip (A1) → home. A tipped pipette doesn't clear a capped vial on the stir module, so the tip never passes over vial_1 while it is capped. The stir itself (`30,600,60`) is sent from a script after the run, because CubOS has no stir step yet | 2026-11-05, TMC2209: 11/11 ([record](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/results/stir_module_trial_20261105/README.md)) |
| [`configs/deck/stir_module_trial.yaml`](configs/deck/stir_module_trial.yaml) | Ben's deck for that trial: vial_1 on the compact stir module at (126, 45) with its rim at z 66 (raised on a spacer and 3 washers), vial_2 at (136.668, 89). It uses the same gantry file | |

`pipette_test_stir.yaml` gained a "ran on hardware" note in its header after the run. Apart from
that comment, it is the file that ran.

## SHA-256

| File | SHA-256 |
|---|---|
| `configs/protocol/vcl/pipette_test.yaml` | `16eb7f2c5376f90f4e5e0c9177ad31fec82e4162e9d2f1715ddd83813cb7fe2c` |
| `configs/protocol/vcl/pipette_test_mix.yaml` | `9263ab7131b7803388df65eef26bf2d03cdc2c769a16e932ed6b677ab81d19a1` |
| `configs/deck/ben_2vials_tiprack.yaml` | `6c0502f1f18abd8b09cb9f65870e1ac4a799b9dcc9f8901a2220212c2e7d3dbd` |
| `configs/gantry/cub_xl_ben_3_instrument.yaml` | `996da208d8d72c0131a4fb83a9164dc8bf260d0c8b99d83692aa92fd275a4cc4` |
| `configs/protocol/vcl/pipette_test_stir.yaml` | `316eab1af43b28b4c1c55f5e7a9cdab94716b97797876069000466b2fb3d3bbd` |
| `configs/protocol/vcl/stir_module_trial.yaml` | `9a82a38f22db4c8182a2d65337d610edb9e30deb36004b874f163099e961713a` |
| `configs/deck/stir_module_trial.yaml` | `81936d2f2d5d97b5c00fd6c5d096a1c6d3d83a5434bfd0ef0e013561c0b45452` |

## Running them

The runner, the CubOS patches, the Uno firmware and the Tic settings are only in byu-vcl, so run
these from a byu-vcl checkout on the CubXL Pi. These are the same files at the same paths there.
For example, the mix test:

```bash
~/CubOS/.venv/bin/python cubos/tools/cubxl_run.py --name pipette_test_mix_<date> \
    --gantry cubos/configs/gantry/cub_xl_ben_3_instrument.yaml \
    --deck cubos/configs/deck/ben_2vials_tiprack.yaml \
    --protocol cubos/configs/protocol/vcl/pipette_test_mix.yaml \
    --no-tic --home-check
```

- **Always pass `--gantry` and `--deck`.** [`cubxl_run.py`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/tools/cubxl_run.py)
  defaults to older files (`cub_xl_ben_pipette_capper.yaml` and `ben_6vials_tiprack.yaml`).
- **`--no-tic`** while the TMC2209 drives the plunger, as it has since 2026-10-07. Leave it off
  if the plunger is back on the Tic T500.
- **`--checks-only`** runs the checks and the offline gates (`validate_setup`, the mock run,
  `passive_shadow`) and moves nothing.
- **Software they ran on:** CubOS `496819c` plus byu-vcl's four patches
  ([`cubos/patches/`](https://github.com/vertical-cloud-lab/byu-vcl/tree/4d5446c/cubos/patches):
  `grbl-prompt-status-polling`, `p20-gen2-plunger-constants`,
  `pipette-connect-tolerate-failed-home-main`, `tipped-hover-clamp-main`). The Uno ran byu-vcl's
  builds of the PANDA firmware: the 10-01 image for the two Tic runs, the 10-07 spreadCycle image
  for the 10-07, 10-09 and 10-12 runs, and the stirrer image (flashed 2026-11-03) for the 11-05
  trial ([firmware README](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/firmware/README.md)).

## Before reusing them

- **The comments in the files are byu-vcl's.** `#169`, `#269` and `PR #171` are byu-vcl issue and
  PR numbers, and relative paths such as `../../../results/...` point into byu-vcl's tree.
- **20 µL is nominal.** CubOS's P20 volume constants are still placeholders, so the P20 still needs
  calibrating, usually by weighing dispensed water.
- **What `mix` does on this firmware:** every `DISPENSE` goes to the blowout plane, so each stroke
  ends in a full blowout. After the first stroke, each `ASPIRATE` draws about 23 µL, not 20. The
  first `ASPIRATE` pushes about 21 µL of air into the liquid, because `pick_up_tip` leaves the
  plunger at the top.
- **Raised vials.** The pre-run checks don't test whether a tip clears a capped vial. With a vial on
  the stir module, a tipped pipette doesn't clear its cap (Ben, 2026-11-05). Run byu-vcl's
  [`capped_vial_keepout.py`](https://github.com/vertical-cloud-lab/byu-vcl/blob/4d5446c/cubos/tools/capped_vial_keepout.py)
  on any deck with a raised vial before running on it.
- **`pipette_test_stir`'s moves are at a fixed deck Z 21** (35 mm below a rim at 56). Regenerate
  them with `stir_moves.py` before using them on a vial at another height.
