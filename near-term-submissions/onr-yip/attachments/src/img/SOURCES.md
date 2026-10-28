# Photos in the Facilities and Equipment attachments

Cropped and resized by hand from the sources below (JPEG, quality 86, metadata
dropped). No person appears in any of them. YouTube frames were pulled on the
lab Pi (YouTube blocks player access from Actions runners) and extracted with
ffmpeg at the time given.

**In DAL.** Only the four `lab-enclosure-*.jpg` frames are stored in this folder. The other
images were already in this repo, byte for byte (sha256 checked on Oct 28, 2026), so the HTML
reads them from there instead of from a second copy. Its `src` paths, relative to `src/`:

| Image (byu-finances path) | `src` in the DAL HTML |
|---|---|
| `../../project-description/figures/enclosure-2026-09-03.jpg`, `atomizer-installed-2026-09-28.jpg` | `../../figures-src/img/` + the same name |
| `img/lab-atomizer-melting.jpg`, `byu-emf-apreo.jpg`, `byu-icpms-8900.jpg`, `byu-px300-polisher.jpg`, `utah-insstek-mxlab.jpg`, `mines-formalloy-x2.jpg`, `lab-powder-doser.jpg`, `lab-cubxl-gantry.jpg`, `lab-cubxl-corrosion-plan.jpg` | `../../figures-src/img/` + the same name |
| `img/mines-cuni-track.jpg` | `../../figures-cu-ded/mines_cuni_track.jpg` |

A newer HTML from byu-finances needs the same `src` changes. The rows below keep the
byu-finances provenance.

| File | Used in | Source |
|---|---|---|
| `../../../project-description/figures/enclosure-2026-09-03.jpg`, `atomizer-installed-2026-09-28.jpg` | Facilities Fig. 1a and 1b | The enclosure frames pulled by the Oct 24 gas-atomization run (see that folder's README); read from there, not copied |
| `lab-atomizer-melting.jpg` | Facilities Fig. 1c | DAL `figures/al-melting-rods.png` (in-house atomizer photo strip, from `digital-alloy-lab-private@7b3af86`) |
| `byu-emf-apreo.jpg` | Facilities Fig. 2a | BYU Electron Microscopy Facility services page photo (`apreo.jpg`), as committed in `digital-alloy-lab-private/genesis-mission-proposal/figures/equipment/apreo-sem.jpg` |
| `byu-icpms-8900.jpg` | Facilities Fig. 2b | BYU Spectroscopic Facility, atomic analysis page (labs.chem.byu.edu), fetched through the Pi |
| `byu-px300-polisher.jpg` | Facilities Fig. 2c | BYU VCL YouTube `id_y-Nr6gAY` ("Polisher training", public), frame at 0:54 |
| `utah-insstek-mxlab.jpg` | Facilities Fig. 3a | University of Utah metallurgy 3D printing center, DED page (`_resources/images/ded_pics/ded_machine.jpg`) |
| `mines-formalloy-x2.jpg` | Facilities Fig. 3b | Colorado School of Mines ADAPT capabilities page (`wp-content/uploads/sites/329/2023/01/Form-Alloy.png`) |
| `mines-cuni-track.jpg` | Facilities Fig. 3c | Photograph by S. Webster (Colorado School of Mines, email of Oct 21, 2026): copper-nickel powder, not from our atomizer, melted into a track in a groove. Cropped to x 235-670 from DAL `figures-src/img/mines-cuni-track-in-groove.png` (see `figures-cu-ded/README.md`). Row added in DAL; the byu-finances table has none |
| `lab-powder-doser.jpg` | Equipment Fig. 1a | BYU VCL YouTube `prj_xgeuQtM` ("Atomizer charge prep (Sep 29): dosing AlSi10Mg", public), frame at 34:27 |
| `lab-cubxl-gantry.jpg` | Equipment Fig. 1b | BYU VCL YouTube `lmQbUWNqTmM` ("Pipette test on CubXL", public), 1080p frame at 3:00 |
| `lab-cubxl-corrosion-plan.jpg` | Equipment Fig. 2 | BYU VCL YouTube `CTQMzOfOmBI` ("Copper corrosion on the CubXL: one spot, start to finish (proposal)", unlisted), frame at 1:40 |
| `lab-enclosure-services.jpg` | Facilities Fig. 1d | BYU VCL YouTube Short `Kv9DT3Vo0GE` ("Atomizer installation (Sep 1): the lab enclosure under construction", public, 1080 x 1920), frame at 3 s, cropped to 1080 x 1440 at y = 0 and resized to 600 x 800 |
| `lab-enclosure-exhaust.jpg` | Facilities Fig. 1e | BYU VCL YouTube Short `Kv9DT3Vo0GE` ("Atomizer installation (Sep 1): the lab enclosure under construction", public, 1080 x 1920), frame at 33 s, cropped to 1080 x 1440 at y = 120 and resized to 600 x 800 |
| `lab-enclosure-curtain.jpg` | Facilities Fig. 1f | BYU VCL YouTube Short `Kv9DT3Vo0GE` ("Atomizer installation (Sep 1): the lab enclosure under construction", public, 1080 x 1920), frame at 55 s, cropped to 1080 x 1440 at y = 240 and resized to 600 x 800 |
| `lab-enclosure-disconnect.jpg` | Facilities Fig. 1g | BYU VCL YouTube Short `Kv9DT3Vo0GE` ("Atomizer installation (Sep 1): the lab enclosure under construction", public, 1080 x 1920), frame at 138 s, cropped to 1080 x 1440 at y = 0 and resized to 600 x 800 |

The Utah, Mines, Electron Microscopy Facility and Spectroscopic Facility images
are the institutions' own and are credited in the captions; ask the facility if
a reviewer copy needs written permission.
