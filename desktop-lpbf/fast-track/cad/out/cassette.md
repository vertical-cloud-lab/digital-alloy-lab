# Will the deck cassette fit through the cube's face? (`ft_cassette.py`, round 3)

Generated from `ft_model.py` (CAD v2, g3 gantry; 2026-11-28). The cassette is the deck plate and everything bolted on it, with the heater plate and rod out, cables and gas lines unplugged, deck screws not in. Coordinates: x, y from the cube's axis (the deck's centre), z above the cube's floor.

## 1. Envelope

| Hopper | x (mm) | y (mm) | Height (mm) | Tallest part |
|---|---|---|---:|---|
| right park (hx 37.5, where it waits while lasing) | -122.5 to 122.5 | -122.5 to 122.5 | 107.7 | Vibration motor |
| left park (hx -33.1) | -122.5 to 122.5 | -122.5 to 122.5 | 107.7 | Vibration motor |
| left end of travel (hx -45.8) | -122.5 to 122.5 | -122.5 to 122.5 | 107.7 | Vibration motor |

## 2. Passing one face at a fixed orientation (2D, exact for a straight slide)

Smallest opening: a square met flat, a square met rolled to the best angle about the insertion axis (sharp corners; and with 12.7 / 25.4 mm corner radii), and a round hole. Touching sizes: add the clearance.

| Cassette | Hopper | Way in | Square, flat | Square, rolled | Roll (deg) | Rolled, r 12.7 / 25.4 | Round hole |
|---|---|---|---:|---:|---:|---:|---:|
| as it is | right park | door (front face), along +y | 245.0 | 207.3 | 39.3 | 207.3 / 208.0 | 246.9 |
| as it is | right park | side plate, along x | 245.0 | 196.2 | 50.8 | 197.2 / 200.6 | 245.2 |
| as it is | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| as it is | left park | door (front face), along +y | 245.0 | 196.9 | 43.6 | 196.9 / 197.3 | 246.9 |
| as it is | left park | side plate, along x | 245.0 | 196.2 | 50.8 | 197.2 / 200.6 | 245.2 |
| as it is | left park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| as it is | left end of travel | door (front face), along +y | 245.0 | 196.9 | 43.6 | 196.9 / 197.3 | 246.9 |
| as it is | left end of travel | side plate, along x | 245.0 | 196.2 | 50.8 | 197.2 / 200.6 | 245.2 |
| as it is | left end of travel | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| hopper, arm, cord, clamp and vibration motor off (MK-08, M3) | right park | door (front face), along +y | 245.0 | 196.9 | 43.6 | 196.9 / 197.3 | 246.9 |
| hopper, arm, cord, clamp and vibration motor off (MK-08, M3) | right park | side plate, along x | 245.0 | 195.2 | 50.4 | 196.2 / 199.6 | 245.2 |
| hopper, arm, cord, clamp and vibration motor off (MK-08, M3) | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| ... and the stage shield (MK-12) | right park | door (front face), along +y | 245.0 | 192.6 | 45.25 | 192.6 / 193.4 | 245.5 |
| ... and the stage shield (MK-12) | right park | side plate, along x | 245.0 | 195.2 | 50.4 | 196.2 / 199.6 | 245.2 |
| ... and the stage shield (MK-12) | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| ... and the X-LSM100B with its carriage (M1c) | right park | door (front face), along +y | 245.0 | 180.3 | 45.0 | 182.1 / 188.8 | 245.2 |
| ... and the X-LSM100B with its carriage (M1c) | right park | side plate, along x | 245.0 | 195.2 | 50.4 | 196.2 / 199.6 | 245.2 |
| ... and the X-LSM100B with its carriage (M1c) | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| ... and the nozzle and collector (MK-11): deck, standoffs, well block, cup | right park | door (front face), along +y | 245.0 | 180.3 | 45.0 | 182.1 / 188.8 | 245.2 |
| ... and the nozzle and collector (MK-11): deck, standoffs, well block, cup | right park | side plate, along x | 245.0 | 186.8 | 47.3 | 187.8 / 191.4 | 245.2 |
| ... and the nozzle and collector (MK-11): deck, standoffs, well block, cup | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |
| bare deck plate | right park | door (front face), along +y | 245.0 | 180.3 | 45.0 | 182.1 / 188.8 | 245.2 |
| bare deck plate | right park | side plate, along x | 245.0 | 180.3 | 45.0 | 182.1 / 188.8 | 245.2 |
| bare deck plate | right park | top plate off, lowered flat | 245.0 | 245.0 | 0.0 | 252.4 / 259.9 | 346.5 |

## 3. Sitting in the cube (the deck in the bottom face's pocket, aligned)

| Pocket corner radius (mm) | Pocket side needed (mm) |
|---:|---:|
| 0 | 245.0 |
| 6.35 | 248.72 |
| 12.7 | 252.44 |
| 19.05 | 256.16 |
| 25.4 | 259.88 |
| 38.1 | 267.32 |

A round pocket would need 346.5 mm, more than the 289.6 mm inside: a square deck cannot lie in a round-bored cube.

Deck corner rule: s >= 245 + 0.586 (r - R_d), R_d = the deck's corner radius (0 as drawn).

## 4. 3D insertion through the door (python-fcl)

The frame redrawn with a through-pocket of side s and corner radius r on all six faces (the five closed plates' bosses 1 mm smaller), the cassette carried in at mid-height of the door's opening (or slid in 0.5 mm over its sill), along +y in 2 mm steps, then lowered onto the floor in 1 mm steps; bisection on s to 0.05 mm.

| Corner radius r (mm) | Smallest opening, carried at mid-height (mm) | With 1 mm a side (mm) | Slid in on the sill (mm) |
|---:|---:|---:|---:|
| 0 | 245.02 | 247.0 | 245.02 |
| 6.35 | 248.76 | 250.8 | 252.78 |
| 12.7 | 252.44 | 254.4 | 263.4 |
| 19.05 | 256.17 | 258.2 | 274.5 |
| 25.4 | 259.91 | 261.9 | 285.79 |
| 38.1 | 267.32 | 269.3 | over 289 |

The model's estimated 266 mm square opening: passes.

Rolled 39.3 deg through a 19.4 mm wall with a square hole (no pocket behind it): needs 207.3 mm in 2D; in 3D hole 207.8 mm: passes, hole 206.8 mm: blocked at step 4.

Run time 337 s.

## 5. The live-reads worker's estimates of the opening (243, 250, 255, 260 mm; estimates until Ideal Vacuum's P107540 drawing)

Carried in at mid-height of the door's opening and set down on the floor (python-fcl, as in 4); yes = in flat with no contact (zero clearance).

| Cassette | Corner radius r (mm) | 243 mm | 250 mm | 255 mm | 260 mm |
|---|---:|---:|---:|---:|---:|
| deck as drawn (245 x 245, sharp corners) | 0 | no | yes | yes | yes |
| deck as drawn (245 x 245, sharp corners) | 6.35 | no | yes | yes | yes |
| deck as drawn (245 x 245, sharp corners) | 12.7 | no | no | yes | yes |
| deck as drawn (245 x 245, sharp corners) | 25.4 | no | no | no | yes |
| deck corners rounded to R 15 | 0 | no | yes | yes | yes |
| deck corners rounded to R 15 | 6.35 | no | yes | yes | yes |
| deck corners rounded to R 15 | 12.7 | no | yes | yes | yes |
| deck corners rounded to R 15 | 25.4 | no | no | yes | yes |
| deck corners rounded to R 30 | 0 | no | yes | yes | yes |
| deck corners rounded to R 30 | 6.35 | no | yes | yes | yes |
| deck corners rounded to R 30 | 12.7 | no | yes | yes | yes |
| deck corners rounded to R 30 | 25.4 | no | yes | yes | yes |
| cube deck cut to the parts' spread, shield cut back | 0 | yes | yes | yes | yes |
| cube deck cut to the parts' spread, shield cut back | 6.35 | yes | yes | yes | yes |
| cube deck cut to the parts' spread, shield cut back | 12.7 | yes | yes | yes | yes |
| cube deck cut to the parts' spread, shield cut back | 25.4 | yes | yes | yes | yes |

The cube deck is 240.2 x 197.3 mm and needs a sharp-cornered opening of 240.21 mm.
