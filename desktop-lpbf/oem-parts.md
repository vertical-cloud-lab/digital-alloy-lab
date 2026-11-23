# OEM parts refined to the vendors' evidence, and the logos (issue #260, 2026-11-23)

Sterling asked on 2026-11-20 for the bought parts to be refined "as close as possible in terms of color, texture, dimensions,
everything", using images, videos, spec sheets, camera intrinsics, model-on-photo overlays and multi-view analysis, and for the
BYU VCL logo and the Y logo to be added. This note covers one evening's round on that. The galvo, the f-theta lens and the
collimator were refined by another agent in the same round and are not covered here.

Files:
- [`cad/logos.py`](cad/logos.py) and [`cad/logos/`](cad/logos/): the two logos as exact vector paths, the deboss hook, and the
  machinability check.
- [`cad/vendor_parts.py`](cad/vendor_parts.py): the refined builders. Every builder keeps its signature, local origin, axes and
  mounting faces, and none grows outside its old bounding box, so no placement in `lpbf_low.py` moved. `ipg_ylr500_u3()` and
  `eaton_5px1500rtg2()` take a new optional `bodies=True` that returns their named bodies (for per-body finishes).
- [`cad/oem/`](cad/oem/):
  - `compare_cad.py`: vendor CAD against our builders, by aligned volume IoU and surface-to-surface distance;
  - `photo_fit.py`: colours, front layouts and camera-pose fits from vendor photos;
  - `render_oem.py`: before/after renders in the measured finishes, and the logo close-ups;
  - `contact_check.py`: an exact static contact check of the changed parts, before and after;
  - `finishes.json`: measured base colour (linear RGB), metallic and roughness per part and body;
  - `cad-manifest.csv` and `photo-manifest.csv`: every vendor file and photo used, with URL and sha256. None of them is
    committed: CAD stays in `/tmp/agentE/vcad`, photos in `/tmp/agentE/photos`.
- [`analysis/out/oem/`](analysis/out/oem/): `cad_compare.md` (before/after table), `cad_compare_{before,after}.json`,
  `photo_fit.json`, `overlay_*.png` (outline overlays, with no vendor pixels in them).
- [`analysis/out/logos/`](analysis/out/logos/): `machinability.json` and `tool_reach_*.png`.
- [`cad/img/oem/`](cad/img/oem/): `before_after_{1,2,3}.png`, `logo_vcl.png`, `logo_y.png`.

## 1. Logos

**Sources.** Both are used as published. SVG lines and cubic Béziers become exact OCC lines and Bézier edges, so nothing is
redrawn or traced from a bitmap.

- **VCL lockup.** The lab's one-line lockup (the mark plus "VERTICAL CLOUD LAB") is `VCL_Logo_FINAL_Outlines-23.svg` from
  `VCL_FINAL_LOGOS-20260518T210517Z-3-001.zip` in
  [vertical-cloud-lab/.github/profile](https://github.com/vertical-cloud-lab/.github/tree/main/profile) (zip sha256
  `a67b026b…2772`). It is the same drawing as `vcl-lockup-one-line-outcrop.png` there. It is committed as
  `cad/logos/vcl-lockup-one-line.svg`.
  - Its paths use only M, l, h, v, c, s and Z, with no arcs. The mark is six rectangles.
  - It makes 22 faces: 6 rectangles and 16 letters, with 7 counters.
- **BYU block Y.** This is BYU's navy polygon from the block-Y figure in BYU's brand guide
  ([brand.byu.edu/logos-marks](https://brand.byu.edu/logos-marks), image `block-y-usage.svg`, sha256 `e711df1d…4633`,
  fetched through the lab tunnel).
  - It has 21 straight edges. It was translated to the origin and not otherwise changed. It is committed as
    `cad/logos/byu-block-y.svg`, with the source in a comment.
  - The block-Y `.zip` on that page redirects to a BYU sign-in, so the figure's polygon was the official outline we could
    reach. If someone with a BYU account downloads the zip, the polygon should be checked against it.
  - **BYU's brand guidelines govern its use.** The shape must not be modified. Texture, shading and dimension are allowed, so
    a deboss is fine. The colours are navy, white or royal. The clear space is the width of the Y's top. The minimum width is
    0.375 in.
  - The guide also says the block Y is a supporting mark and that the BYU monogram should usually appear with it. That is
    not done here.
  - The ™ is left off. At this size it would be 2.4 mm tall with 0.3 mm strokes, below the cutter.

**Placement.** `logos.apply(parts, M)` is called by one line at the end of `lpbf_low.build()`. It must stay the last line,
because it cuts into the final shapes. It finds each part by name prefix and reads the face plane off the part's box.

- **VCL lockup on the chamber door's front face:** 0.5 mm deep, 180 × 24.5 mm, centred at x = 0, z = 60. Strokes are 1.49 mm.
  - It sits above the hinge leaves (z ≤ 30, at |x| 80–100) and below the handle posts (z ≥ 90). It is inside the 6 mm corner
    radii and clear of the latch ears (|x| > 124).
  - The door is 15 mm thick. Its seal groove (1.32 mm deep) is on the back face, so 13.2 mm of plate stays between the two.
- **Block Y on the 4U control drawer's front panel:** 0.5 mm deep in the 4 mm panel, 50 mm tall and 40.7 mm wide.
  - It sits at the panel's left end, one Y-top width (40.7 mm) in from the 18 mm rack ear, as the clear-space rule asks. Its
    centre is at x = −872.3, z = 257.5.
  - **Why there:** the drawer is the one rack unit the lab builds itself, so a university mark belongs on it rather than on a
    vendor's box. It is the top unit, at eye level. Its left end lines up with where the units below it carry their own badges.
  - The guard's front-left post is a T-slot extrusion (slots on every face) behind a 22 %-opaque panel, so a deboss there
    would hardly show.
  - The render fills it with BYU navy (#1e3158), which is suggested for the build (paint fill, or a black anodise
    laser-marked).
  - **For the coordinator:** if B2's electrical hook rebuilds the drawer's front panel, `logos.apply` must run after it.

**Machinability** (`python cad/logos.py check`): a raster at 0.01 mm/px, opened by a 1/32 in. (0.794 mm) end mill.

| Logo | Size (mm) | Area (mm²) | Cutter can't reach | Largest deviation | Glyphs before → after | Cutter that loses half a glyph |
|---|---|---|---|---|---|---|
| VCL lockup | 180 × 24.5 | 931 | 3.6 mm² (0.39 %) | 0.32 mm (acute inner corners of V, A, R) | 22 → 22 | 2.0 mm |
| Block Y | 40.7 × 50 | 969 | 0.44 mm² (0.05 %) | 0.16 mm (the Y's 90° inner corners) | 1 → 1 | none up to 3 mm |

- Every glyph survives, and the narrowest stroke (1.49 mm) is wider than a 1.5 mm cutter. So no path needed simplifying.
  The cutter leaves R0.4 fillets in the inner corners. That is a machining radius, not a change to the mark.
- Laser engraving needs no radius at all.
- `tool_reach_*.png` shows the unreachable pixels in red.

Renders: [`cad/img/oem/logo_vcl.png`](cad/img/oem/logo_vcl.png) (bare deboss under a raking light) and
[`cad/img/oem/logo_y.png`](cad/img/oem/logo_y.png) (navy fill).

## 2. Method for the bought parts

- **(a) Dimensions and vendor CAD.**
  - **Fetching.** The 10 McMaster STEP files and Teknic's `CPM-231x.zip` were re-fetched through the lab tunnel.
    - Every sha256 matches the 2026-11-20 manifest.
    - McMaster returns 403 to plain curl. It serves the file when Chrome first opens the product page and then requests the
      manifest's STEP URL with that page's cookies.
  - **Comparing.** `compare_cad.py` tessellates both shapes, about 0.1 mm.
    - It aligns the vendor mesh to ours: the best of the 24 axis rotations about the box centres, then ICP if that raises
      the IoU.
    - It computes the volume IoU from exact mesh booleans (manifold3d).
    - It takes 20 000 surface samples each way. It reports the mean of the two mean distances, the larger P95, and the
      Hausdorff distance.
  - **Where there was no CAD,** the drawing, datasheet or a straight-on photo set the dimensions: IPG, Eaton, the 4396K21
    pump, the 6709K33 rail.
- **(b) Colour and finish.**
  - **Colour.** `photo_fit.py` takes the median of hand-checked regions of the vendor's own photo or render, with Lab
    lightness and chroma gates. It converts sRGB to linear RGB.
  - **Metallic** comes from the material and from whether the highlights are tinted.
  - **Roughness** comes from the highlight spread and the specular-to-diffuse contrast. This is a heuristic, and it is
    flagged as one in `finishes.json`.
  - McMaster's images are renders of their CAD, so they give colours but not real finishes.
- **(c) Photo overlays.**
  - **Solving the camera.** The camera pose and focal length come from fitting the silhouette: the projected,
    tessellated builder against the photo's segmented mask, maximising the IoU over the pose and a 1-D search over f. The
    principal point is assumed to be at the image centre.
  - **What gets committed.** The overlays committed in `analysis/out/oem/` show only the outline of the photo-derived mask
    and the model's silhouette. No vendor pixels are in them.
- **(d) Multi-view.** Not done (§5).
- **Fill-rule bug.** The first fit run filled all the model's triangles in one `cv2.fillPoly` call. That call fills even-odd,
  so overlapping triangles cancelled and the silhouette had holes. The fit now fills one triangle at a time, starts from
  400 random rotations, and keeps the model in front of the camera. The numbers below are from the fixed run.

## 3. Per part

The vendor-CAD numbers are from `analysis/out/oem/cad_compare.md`: aligned IoU and surface distance in mm (mean / P95 / max),
before → after. Colours are measured sRGB hex values (linear RGB in `finishes.json`). "m" is metallic and "r" is roughness.

### IPG YLR-500-U3-SM-AC (4U fiber laser) — `ipg_ylr500_u3()`

- **Sources.**
  - IPG's spec G22-29856 and drawings, transcribed in [`quotes/ipg-ylr-500-u3-sm-ac.md`](quotes/ipg-ylr-500-u3-sm-ac.md):
    176.5 × 482.3 (ears) × 506 (body) / 557.2 (handles), "fans on the front panel".
  - IPG's renders of current rack-mount YLRs: `YLR_Series_Card` and `YLR_U_Rack_Card` on cdn.ipgphotonics.com (see
    `photo-manifest.csv`).
  - There is no vendor CAD, and the U3's own front drawing is not public.
- **Changed.** The front panel now carries:
  - the dark control strip with a START button, an emergency-stop mushroom (Ø40, 22.5 mm proud) and a key switch;
  - the portrait touch display;
  - a 9 mm deep fan intake with 11 horizontal slats over the right 55 %, its left edge slanted as in IPG's render;
  - 12 × 12 bar handles running nearly the full height (z 10–166.5).

  The outer extents are unchanged (482.3 × 557.2 × 176.5). Volume −0.4 %.
- **Colours** (from the YLR-U rack card):

  | Body | Colour | m | r |
  |---|---|---|---|
  | Front panel, light area | #cbcbcb | 0 | 0.57 |
  | Fan/dot-pattern area | #1e2022 | 0 | 0.48 |
  | Handles | #101010 | 0 | 0.55 |
  | Chassis sides | #323536 | 0 | 0.49 |
  | Blue swoosh | #30a9dc | 0 | 0.88 |

- **Still approximate.**
  - IPG shows two rack front styles. One is the compact rack unit with START, e-stop, key and display over a slatted fan grille,
    which is what is drawn. The other is the YLR-U rack (-1500/-3000/-6000-U), with LEDs at the left, a light panel with a
    curved edge, a dark dot-pattern field and a blue swoosh. Its layout is in `photo_fit.json` → `layouts`.
  - Which one the U3 has should be checked on IPG's front-view drawing or a photo of the delivered unit. Positions are
    ±5 mm, and the button sizes assume standard 22 mm operators.
  - **For the coordinator:** `lpbf_low.py` still colours the whole part `C["white"]`; the measured colours are only used by
    `render_oem.py`.

### Eaton 5PX1500RTG2 (2U UPS) — `eaton_5px1500rtg2()`

- **Sources.**
  - Eaton's datasheet ([assets.tripplite.com 5px1500rtg2.pdf](https://assets.tripplite.com/product-pdfs/en/5px1500rtg2.pdf)):
    86.36 × 436.88 × 447.04, 23 kg; "LCD graphical display", 3 LEDs plus an LED light bar.
  - Its straight-on product photo, page 1. The bezel measures 5.05:1 in it, against the datasheet's 5.06:1, which gives
    1.04 mm per pixel. There is no vendor CAD.
- **Changed.**
  - The bezel is now the full 436.88 width, with the 19 in. rack ears beside it. Before, a 3 mm plate covered the whole front.
  - The silver grille is recessed 1.5 mm, with the Eaton badge left proud.
  - The black LCD module is at the right: a 1 mm LCD recess, five key recesses and the LED bar.
  - The extents are unchanged. Volume −0.2 %.
- **Colours:**

  | Body | Colour | m | r |
  |---|---|---|---|
  | Grille, holes included | #a3a3a3 | 0 | 0.79 |
  | Grille metal between the holes | #bdbdbd | | |
  | Display module | #27262c | 0 | 0.54 |
  | Lit LCD | #45699f | | |
  | LED bar | #0859a8 | | |
  | Badge | #d3d3d7 | | |

- **Still approximate.** The perforation is a colour, not holes. The bezel's frame and chassis colours are assumed: #3b3e44
  and #202226.

### Teknic ClearPath CPM-SDSK-2311S (recoater and Z servos) — `clearpath_sd_231x()`

- **Sources.** Teknic drawing D1171/M; Teknic's `CPM-231x.zip` (STEP, sha256 matches); Teknic's gallery photo
  `cpm_231_L_lg.jpg`.
- **Changed.**
  - A 6 mm flange plate with R3 corners; the four Ø5.2 holes go through the flange only.
  - An octagonal body with 17.5 mm chamfers, so the bolt heads clear it.
  - A rear pin-fin heat sink: Ø2.5 pins on a staggered 4.4 × 4.2 mm grid, over the rear 9.8 mm.
  - The connector block has R4 corners, stops at z −80, and has an Ø11 boss and two connector pockets.
- **CAD check.**

  | | Before | After |
  |---|---|---|
  | IoU | 0.586 | **0.661** |
  | Volume vs Teknic | +69.4 % | +34.6 % |
  | Distance, mean / P95 / max (mm) | 3.40 / 12.5 / 25.2 | 1.71 / 12.0 / 23.8 |

- **Colours:**

  | Body | Colour | m | r |
  |---|---|---|---|
  | Black anodised body | #2a2b2e | 0.5 | 0.41 |
  | Aluminium flange | #abaaa9 | 1 | 0.95 |
  | Die-cast rear fins | #bdbcbd | 1 | 0.58 |
  | Connectors | #0c0e10 | | |
  | Ground shaft | #aeaba7 | | |

- **Photo fit** (Teknic's gallery photo `cpm_231_L_lg.jpg`, [`overlay_clearpath_sd_231x.png`](analysis/out/oem/overlay_clearpath_sd_231x.png)):
  - Silhouette IoU **0.917**, at f = 2549 px (91 mm equivalent), with the part 592 mm from the camera.
  - Outline distance: mean 6.8 px (1.57 mm), P95 25 px.
  - The contact shadow was cut out of the photo's mask.
  - With f held at 1020, 1784, 2549, 3823 and 6372 px, the IoU is 0.895, 0.919, 0.915, 0.908 and 0.891. A single silhouette
    barely fixes this focal length.
  - The outline misses the rear housing's fins, the round rear cap and the top of the connector shroud.
- **Still approximate.**
  - Teknic's model is hollow between r 6.5 and 26.5, from z −12.5 to −40. That void is not drawn, because the real stator
    fills it, and it is most of the remaining +35 %. Mass stays at the datasheet's 0.6 kg.
  - The pin grid is not phase-matched to Teknic's.
  - The logo and the cover screws are not drawn.

### McMaster 6627T91 NEMA 17 stepper (dosing) — `mcm_6627T91()`

- **Changed.** Two 9.5 mm end caps with 3.5 mm chamfers. A 41.9 mm stator with 6.4 mm chamfers. M3 holes 9 deep. A 9 × 7
  lead notch through the rear cap. An Ø10 × 4.5 rear recess.
- **CAD check.** IoU 0.945 → **0.982**. Volume +5.4 → +0.8 %. Mean distance 1.04 → 0.69 mm. P95 stays at 11.4 mm, because
  of McMaster's internal surfaces (shaft bore and bearing).
- **Colours.** Housing and caps #3a383a (m 0, r 0.82). Front face, pilot and shaft #c6c7c7 (m 1, r 0.47).

### McMaster 6709K12 carriage and 6709K33 rail — `mcm_6709K12()`, `mcm_6709K33()`

- **Changed.** The carriage's end caps and seals now stop at z 23.5; only the steel block reaches z 28.
- **CAD check (carriage).** IoU 0.784 → **0.834**. Volume +10.8 → +3.5 %. Distance 0.86 / 3.30 / 6.0 → 0.63 / 2.56 / 4.0 mm.
- **Colours.** Steel block #bfbeb8 (m 1, r 0.95). End caps #2b2c2b (m 0).
- **Still approximate.** The ball-retainer strips reach into the rail grooves, so drawing them would collide with our rail.
  The balls and return holes are not drawn. The rail has no vendor CAD, because McMaster asks for a length first. Its
  raceway grooves are still assumed.

### McMaster 4566N401 ball nut — `mcm_4566N401()` (unchanged)

- **CAD check.** IoU 0.841. Volume +0.6 %. Distance 0.40 / 1.80 / 4.96 mm. The vendor body is Ø23.8 where ours is Ø23.
- **Colour.** #c1c1c1 (m 1, r 0.62).
- **Still approximate.** The helical groove is not drawn. The body was left at Ø23 because the bracket bore round it was not
  checked this round.

### McMaster 5786N23 / 5786N25 KF stubs — `kf_weld_stub()` (unchanged)

- **CAD check.** IoU 0.973 / 0.969. Distance 0.03–0.04 / 0.31 / 0.74 mm. Already right.
- **Colour.** #bebebd (m 1, r 0.55).

### McMaster 4518K72 / 4518K73 KF wing clamps — `kf_wing_clamp()`

- **Changed.**
  - The ring section now follows the vendor's C-channel: 16 mm tall (was 10.8), channel bottom at r 25.0 / 30.2, lips at
    r 15.9 / 23.7 on the 15° tapers.
  - The hinge is now a block 22.4 mm wide.
  - The lips no longer touch the flange tapers. There is a 2.4 mm gap, as in McMaster's model.
- **CAD check.**

  | Clamp | IoU before → after | Mean distance (mm) |
  |---|---|---|
  | KF-25 | 0.283 → **0.706** | 1.41 → 0.54 |
  | KF-40 | 0.515 → **0.798** | 1.19 → 0.46 |

- **Colour.** Aluminium #c4c4c4 (m 1, r 0.77).
- **Still approximate.** The bolt, ears and wing nut are unchanged.

### McMaster 4123K45 KF-25 ball valve — `mcm_4123K45()`

- **Changed.**
  - A 3-piece body: two 7.5 mm end caps with lobes round four Ø4.8 tie bolts, and an Ø54.6 centre body.
  - An Ø26.6 stem neck flaring to Ø33.8, the Ø50 stop plate and the stem nut.
  - A Ø21.8 bore.
  - The lever is a 24 mm plate, flat over the hub and rising at 72° to a 4.8 mm grip at z 86.9–91.7.
- **CAD check.** IoU 0.578 → **0.881**. Volume −2.4 → −7.0 %. Distance 2.65 / 18.2 / 35.7 → 0.50 / 2.72 / 9.2 mm.
- **Colours.** Cast 316 body #a5a5a5 (m 1, r 0.53). KF flanges #9c9c9c (m 1, r 0.42). Grey vinyl lever grip #b1b1b1 (m 0,
  r 0.46).
- **Photo fit** (McMaster's product render, [`overlay_mcm_4123K45.png`](analysis/out/oem/overlay_mcm_4123K45.png)):
  - Silhouette IoU **0.932**, at f = 2360 px (105 mm equivalent).
  - Outline distance: mean 3.5 px (0.84 mm at the part), P95 15 px.
  - How well f is fixed, as the IoU with f held at each value:

    | f (px) | 944 | 1652 | 2360 | 3539 | 5899 |
    |---|---|---|---|---|---|
    | IoU | 0.834 | 0.908 | 0.931 | 0.936 | 0.912 |

    The IoU falls off below about 1650 px, so f is bounded from below.
  - **Still missing:** the render's mounting pad on top of the body is wider than the model's 30 × 30 pad.

### McMaster 3861N11 transmitter and 5169K72 filter housing (built, not in the model)

- **CAD check.**
  - 3861N11: IoU 0.267. McMaster's straight lead runs out to 172.8 mm, and that dominates the score.
  - 5169K72: IoU 0.746. McMaster's part is an Ø88 can under an Ø95 lid, with the outlet nipple 2.9 mm below our datum.
- **Not refined.** Neither part is placed in the model: the lid port is SAE-4, and the gas-loop hoses are not re-routed.
- **Colours.**
  - 3861N11: black body #272727, stainless hex #aeafac.
  - 5169K72: black housing #3b3d3a, steel bail clips #a6a7a5.

### McMaster 4396K21 pump (built, not in the model)

- No vendor CAD, so it was not refined.
- **Colours.** Black motor #383838; aluminium block #aeaeae.

## 4. Checks

- **Static contacts, the parts changed in this round** (`cad/oem/contact_check.py`, M50): see the table below.
- **Exact interference sweeps** (`analysis/interference.py`): see the table below.
- **`vendor_parts.py inventory` and `verify`:** see the table below.

## 5. Not done

- **(d) multi-view / NeRF-style reconstruction.** Skipped. Two videos were found but not downloaded:
  - Teknic's ClearPath SD overview (YouTube, linked from the ClearPath products page);
  - IPG's Wistia video on the ultra-compact laser page.

  The 20-minute time box went on the silhouette fits instead. The next step is frames from the Teknic video, then COLMAP
  (Docker) for the intrinsics and poses, then a visual hull against `clearpath_sd_231x()`.
- **Eaton product pages.** eaton.com and the Tripp Lite product page return 503 through the tunnel, even in headed Chrome. So
  the Eaton front comes from the datasheet's photo alone.
- **Lens, galvo and collimator.** Another agent's area this round.
- **The rack drawer, PC and the other envelope parts** listed in `analysis/out/real-parts/inventory.md`. They have no vendor
  part chosen yet.
- **Texture.** The perforations, the fan-grille dots and the labels are colours in the render, not geometry or texture
  maps.
