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

## Round 6 (2026-11-25): pump, transmitter, filter housing, IPG and Eaton fronts, and a video reconstruction

On 2026-11-25 Sterling asked for everything round 5 skipped. For the bought parts that meant five things:
- a multi-view reconstruction from a product video;
- the Edwards nXDS6i pump (BOM G2);
- the lid's pressure transmitter (G7);
- the HEPA filter housing (G5);
- the IPG front panel, whose style was a guess, and the Eaton front, whose vendor pages had returned 503.

New files:
- [`cad/oem/drawing_fit.py`](cad/oem/drawing_fit.py): silhouettes against a vendor's orthographic drawing.
- [`cad/oem/video_recon.py`](cad/oem/video_recon.py): the video reconstruction, with
  [`analysis/out/oem/video_recon.md`](analysis/out/oem/video_recon.md).
- `cad/img/oem/before_after_r6_{1,2}.png`.

`compare_cad.py`, `photo_fit.py`, `render_oem.py` and `contact_check.py` gained round-6 cases. Downloads stay in `/tmp/oem`. URLs
and sha256 are in `cad/oem/cad-manifest.csv`, `cad/oem/photo-manifest.csv` and `cad/vendor-cad-manifest.csv`.

### What changed in the model (`cad/lpbf_low.py`)

| Part | Before | After |
|---|---|---|
| Dry scroll pump (G2) | 420 × 250 × 270 box, blue, inlet at (640, 165), exhaust on its +x end | `edwards_nxds6i()`, 432 × 282 × 302, at x 557–989 and y 1–280: NW25 inlet on top at (782, 95); NW25 exhaust on the front side (−y) at x 904, 145 mm up; fan end toward +x (the tray's open edge); 26.2 kg (Edwards: 26.20 kg) |
| Pressure transducer (G7) | 3 cylinders, top 64 mm above the lid | `transmitter_on_sae4()`: the 3861N11 in the SAE-4 × 1/4 NPT adapter that BOM G7 already counts (adapter dimensions assumed); top 73.75 mm above the lid |
| Cyclone + HEPA housing (G5) | Ø116 × 254 mm 316L can | `filter_train_5169K72()`: the 5169K72 upright at (470, −40), side inlet turned to the front; a 1/2 NPT × KF-25 adapter and a KF-25 90° elbow on each port (55 mm centre to face, assumed); a 6061 stand; 1.5 kg (estimate) |
| IPG YLR-500-U3 (4U) | round 5's front (the shorter rack unit's style: slatted grille) | IPG's 4U single-mode front (§3); extents unchanged |
| Eaton 5PX1500RTG2 (2U) | front from the datasheet's 500 px photo | front from Eaton's 2000 px image (§3); the keys stand 1 mm proud |

Three routes that end on these parts moved with them. Each is one entry in `lpbf_low.py`:
- the vacuum hose's last points now pass over the pump to its inlet, clear of the lifting eye;
- the outlet-plenum hose now ends over the filter's inlet elbow;
- the pump exhaust line starts at the exhaust on the pump's front, runs round the fan end and joins its old route to the dock.

The filter's outlet elbow lands on the existing outlet stub, so the filter-to-blower hose did not move.

### Numbers, before → after

| Part | Check | Before | After |
|---|---|---|---|
| nXDS6i | Silhouette IoU against Edwards' drawing, mean of 5 views, at the drawing's scale | 0.867 (envelope) | **0.923** |
| 3861N11 | Volume IoU against McMaster's CAD | 0.692 (round 5: 0.267, see §3) | **0.948** |
| 3861N11 | Mean / P95 surface distance (mm) | 1.70 / 7.58 | 0.24 / 1.48 |
| 5169K72 | Volume IoU against McMaster's CAD | 0.746 | **0.949** |
| 5169K72 | Mean / P95 surface distance (mm) | 4.06 / 10.9 | 0.84 / 4.98 |
| 3861N11 | Silhouette IoU, McMaster's image, camera solved | 0.925 | **0.925** (this view cannot tell the two apart; the CAD check can) |
| 5169K72 | Silhouette IoU, McMaster's image, camera solved | 0.887 | **0.897** |
| Eaton 5PX1500RTG2 | Silhouette IoU, Eaton's three-quarter image, camera solved | 0.954 | **0.956** |
| ClearPath (video) | COLMAP on Teknic's turntable video: points within 1 mm of `clearpath_sd_231x()`; silhouette IoU through the 74 solved cameras (median) | — | 48.7 %; 0.81 (the reconstruction's proportions are off by up to 14 %: see below) |

Per-body colour, metallic and roughness for the nXDS6i, the IPG 4U front and the Eaton front are in
[`finishes.json`](cad/oem/finishes.json) (§3 has the tables). The renders are
[`before_after_r6_1.png`](cad/img/oem/before_after_r6_1.png) and [`before_after_r6_2.png`](cad/img/oem/before_after_r6_2.png).

### Video reconstruction (ClearPath, from Teknic's product video)

Full note: [`video_recon.md`](analysis/out/oem/video_recon.md). Numbers: `video_recon.json`. Figures:
[`video_recon_cloud.png`](analysis/out/oem/video_recon_cloud.png) and
[`video_recon_silhouettes.png`](analysis/out/oem/video_recon_silhouettes.png), which show outlines and points only. The
video, frames and COLMAP workspace stay in `/tmp/oem/video`.

- **Video.** Teknic's "ClearPath: Teknic's Integrated Brushless Servo Motor, Drive and Encoder"
  ([YouTube `_SYhCRwacDs`](https://www.youtube.com/watch?v=_SYhCRwacDs)), linked from Teknic's ClearPath page. yt-dlp fetched it
  through the lab tunnel, because YouTube asks the runner to sign in. 1280 × 720, sha256 `4c69d762…c7f2`.
  - The segment used, 598.6–606.0 s, is a 266° turntable shot of a CPM-23 motor on a white backdrop.
  - It is a render of Teknic's own CAD, not footage of a real unit.
  - The first video tried, the ClearPath-SD overview, shows the motor only in still poses.
- **COLMAP** 3.12.6, CPU, under the 3 GB cap. 74 frames at 10 fps, each masked to the motor; SIFT; exhaustive matching; one
  SIMPLE_RADIAL camera.
  - **Registered: 74 of 74** frames, 13,502 points, reprojection error 0.84 px mean (0.64 median).
  - **Focal length 2,673 px** (78.8 mm in 35 mm terms, 26.9° across), principal point fixed at the centre, k1 = −0.36.
  - The solved cameras run on a 282° arc. The radius varies 20 % (1 sd), and the path is out of plane by 0.4 % RMS.
  - Dense MVS needs CUDA and was not run. A visual hull from the solved cameras stands in for it.
- **Scale and alignment.**
  - The cloud was set upright on the turntable axis and fitted by silhouette IoU over the solved views. That gives a mean
    IoU of 0.81 on 25 views.
  - Rigid ICP then refined it, with the scale set by the flange (59.10 mm square on Teknic's drawing).
  - In the cloud, the flange measures 61.4 × 62.9 mm and the shaft 10.8 mm (drawing: 9.5).
- **Against `clearpath_sd_231x()`**, cloud to our surface, 9,966 filtered points:
  - mean 1.90 mm, median 1.03 mm, P95 6.8 mm;
  - **25.4 % of points within 0.5 mm, 48.7 % within 1 mm**, 69.6 % within 2 mm.
- **Silhouette IoU** of our model through the 74 solved cameras: **median 0.81** (0.74–0.87 on the 220 threshold mask).
- **Visual hull** (1 mm voxels, kept in ≥ 95 % of views):
  - IoU 0.61 with our model, which lies 89 % inside it;
  - chamfer 4.7 mm.
  - A hull cannot see concavities: the fin gaps, the connector pockets and the flange step stay filled.
- **What it shows.**
  - The solve is self-consistent: sub-pixel reprojection error, all frames registered.
  - **Its proportions are off,** so it cannot measure our model to 0.5 mm. Fitting a separate scale per axis gives 0.86,
    1.02 and 1.09, where a true reconstruction would give three equal scales. The flange is rebuilt about 12 mm too far back,
    and the solved orbit's radius varies 20 % where a turntable gives a circle. The large k1 on a render points the same way.
  - The likely cause is the focal length. A 27° view of an object turning about one axis fixes it poorly, and an error in it
    stretches the reconstruction.
  - **Focal-length test** (`video_recon_fixedf.json`). The mapper was re-run on the same matches with f held and k1 = 0, at
    1778 px (a 50 mm lens, a common render default), 4010 px (1.5 × the solved f) and 6000 px:

    | f (px) | Per-axis spread | Orbit radius sd | Reprojection (px) | Median silhouette IoU | Within 1 mm |
    |---|---|---|---|---|---|
    | 1778 | 35.4 % | 22.1 % | 0.84 | 0.81 | 47.7 % |
    | 2673 (solved) | 27.5 % | 19.9 % | 0.84 | 0.81 | 49.7 % |
    | 4010 | 20.0 % | 18.7 % | 0.84 | 0.79 | 48.6 % |
    | 6000 | 55.6 % | 18.4 % | 0.85 | 0.78 | 17.7 % (its pose fit did not converge) |

    - f changes the distortion but no tested value removes it, and the frames can't tell the values apart: the same
      reprojection error, about the same IoU.
    - Something besides f is off, perhaps a camera that also moves or zooms in Teknic's render.
    - A per-frame focal length (one COLMAP camera per frame) is the next test. It was not run.
    - So the video checks our model to a few mm, not better.
  - Because the video is a render of Teknic's CAD, this is a second route to the same reference. The STEP comparison (IoU
    0.661) is the better one, and neither says how a delivered motor differs from Teknic's CAD.
- **Not done:** a NeRF or Gaussian splat. It is not quick on 4 shared CPU cores.

### Checks

- **Exact interference sweep, M50/M,** on the round-6 model: `analysis/interference.py M50` under a 3 GB cap, 1,624 s on
  the shared runner. Results in [`interference_M50_r6.md`](analysis/out/oem/interference_M50_r6.md); the shared
  `analysis/out/interference.*` were left for the lead to regenerate.
  - **0 interferences** in all 6 static states (calibration included) and all 8 motion sweeps.
  - Every sweep's tightest gap is the same as round 5's merged model: recoater 0.05, piston 0.15 and guard door 2.00 mm. The
    others are the designed contacts at 0.
  - Designed joints went from 22 to 20. Both changes follow from the new routes:
    - pump with exhaust line: the line now starts on the exhaust flange's face, a face contact with no shared volume;
    - pump inlet stub with vacuum hose: the hose now ends 20 mm above the stub's face, the same as at the filter's inlet
      stub. The old route only overlapped the flange because it came in at a slant.
- **After the sweep started,** the Eaton front changed (its keys stand 1 mm proud). The UPS and the laser were then intersected
  exactly with every part whose box they touch.
  - UPS: no shared volume with the rack frame or the side panels.
  - Laser: no shared volume except with the process fibre where it enters the front panel, a designed joint. That joint holds
    5,236 mm³ (round 5: 4,189; round 4: 5,760): round 5's 9 mm deep fan recess is gone and the new fan field is a 1 mm
    recess.
- **Round 5's `contact_check.py`** was given the round-6 part list but stopped after 22 minutes. Its exact booleans on the
  long hose compound are slow on the shared runner, and the sweep covers the same pairs.
- **Clearances round the pump:** below, under "The pump's ventilation and controls".

### What this changes, and open questions

- **The lid transmitter's lead has no room to leave.**
  - The BOM's 3861N11 on its SAE-4 adapter stands 73.75 mm tall. Its cable gland ends 1.25 mm under the optics bridge (z 211),
    and the bridge is solid there.
  - The 36 in. lead leaves the gland straight up, so it can't be routed.
  - **Options:** a 90° SAE-4 × 1/4 NPT elbow, which lays the transmitter along +x over the lid; a transmitter with an SAE-4
    port and a side cable exit; or a bore in the bridge.
  - The model draws the straight adapter, as the BOM has it.
- **The filter needs two KF-25 adapters and two elbows that the BOM doesn't list.** Their dimensions are assumed. The
  5169K72's flow is side-in, bottom-out, as McMaster intends, and its lid stays on top, so the element can be changed.
- **The pump's ventilation and controls.** Edwards' instruction manual
  ([A735-01-880 issue B](https://www.nanofab.utah.edu/wp-content/uploads/2022/12/Edwards-nXDS-15i-pump-manual.pdf), §3.4,
  which covers the nXDS6i) asks for four things:
  - ventilation at both ends;
  - an ambient of 40 °C or less;
  - at least 25 mm between the pump and any enclosure wall;
  - the gas ballast and the user controls within reach.

  In the model:
  - the fan end faces +x, toward the tray's open edge. The nearest part in front of it is the re-routed exhaust line, 62.5 mm
    from the fan guard. That is the distance from the line's centreline (smoothed as `polyline_pipe` draws it) to the
    tessellated pump, less the line's radius;
  - the motor end is at least 35 mm from the argon regulator;
  - the connector panel and the gas ballast face the front;
  - the vacuum hose passes 16 mm over the motor end's top edge.

  The gas module has no enclosure walls drawn, so the 40 °C ambient is not checked.

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

- **Still approximate (round 5).**
  - IPG shows two rack front styles. One is the compact rack unit with START, e-stop, key and display over a slatted fan grille,
    which is what is drawn. The other is the YLR-U rack (-1500/-3000/-6000-U), with LEDs at the left, a light panel with a
    curved edge, a dark dot-pattern field and a blue swoosh. Its layout is in `photo_fit.json` → `layouts`.
  - Which one the U3 has should be checked on IPG's front-view drawing or a photo of the delivered unit. Positions are
    ±5 mm, and the button sizes assume standard 22 mm operators.
  - **For the coordinator:** `lpbf_low.py` still colours the whole part `C["white"]`; the measured colours are only used by
    `render_oem.py`.
- **Round 6 (2026-11-25): front redrawn.** IPG's own render of its single-mode family (`YLS_SM_Family_Main` on IPG's
  [Single-Mode Fiber Lasers](https://www.ipgphotonics.com/products/lasers/industrial-cw-fiber-lasers/industrial-single-mode-lasers)
  page) shows two single-mode rack lasers. The shorter one has a slatted grille like round 5's drawing. The 4U one, the single-mode
  rack laser with fans in its front panel that the U3 drawing describes, has:
  - one column of operators on a light panel: green START (Ø29, z 150.7), a red mushroom (Ø36, z 119) and a key switch
    (Ø29, z 84.2), all at x −177.5;
  - a light-grey portrait window beside them (x −152.4 to −96, z 74 to 168) and the IPG logo;
  - a dark perforated fan field over the right ~45 %. Its left edge sweeps down in a curve to a band along the bottom, under
    the operators. It is drawn as a 1 mm recess; the perforation is a colour.

  The face is seen ~30° off-axis at 2.9 mm per pixel, so positions are ±6 mm. The extents and handles are unchanged. Colours
  from the same render: light panel #f6f6f6, fan field #505051 (dots and holes averaged), window #dcdcdc, handles #454747,
  chassis #232323 (m 0; roughness heuristic). It is still a render, not a photo of a delivered U3.

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

- **Still approximate (round 5).** The perforation is a colour, not holes. The bezel's frame and chassis colours are assumed: #3b3e44
  and #202226.
- **Round 6 (2026-11-25): re-measured on Eaton's own images.** Eaton's
  [SKU page](https://www.eaton.com/us/en-us/skuPage.5PX1500RTG2.html) loaded through the tunnel this time (status 200, headed
  Chrome). Its images come from eaton.com's `mdmfiles` store, which answers 403 to curl but serves a browser navigation. Two
  2000 × 2000 px images were used: `5PX1500RTG2_C` (straight on) and `_R` (three-quarter).
  - **Front, from `_C`.** The bezel spans 1680 × 326 px: 3.85 px/mm across, 3.78 px/mm down (its ratio is 5.15:1, against
    5.06:1 from the datasheet, so ±1 mm). Changes from round 5:

    | Feature | Round 5 (500 px datasheet photo) | Round 6 (2000 px) |
    |---|---|---|
    | Grille window (x; z) | −213.2 to 115.3; 4.3 to 81.2 | −207.9 to 107.0; 5.8 to 78.7 |
    | Badge (x; z) | −176.9 to −153.8; 30.2 to 55.3 | −187.8 to −156.8; 26.6 to 57.3 (a 31 mm square) |
    | LCD module (x) | 120.1 to 213.2 | 133.6 to 206.8, a dark slot to x 117.2 beside the grille |
    | LCD (x; z) | 146.4 to 195.3; 29.9 to 66.1 | 147.5 to 187.3; 35.3 to 62.6 |
    | Keys | five Ø7 recesses at z 19 | five 13.4 mm square keys at z 9.6 to 22.8, 1 mm proud, centres x 142.0, 156.8, 170.8, 185.1, 199.6 |
    | LED bar (z) | 6 to 9.5 | 5.8 to 8.6 |

  - **Colours, from `_C`.** Grille #aaaaaa (holes included) and #cbcaca (metal between the holes); bezel frame #2c2b31, which
    replaces round 5's assumed #3b3e44; LCD module #070709; lit LCD #2a5d9c; LED bar #0093ee; badge #d5d6d6; keys #111017.
    The holes are Ø4.1 on a 6.7 × 7.4 mm staggered pitch, still a colour and not geometry.
  - **Silhouette fit, from `_R`.** The camera was solved as for the ClearPath, with the ears off because the photo has none.
    Silhouette IoU **0.956** at f = 2778 px (42.5 mm equivalent). Round 5's builder scores 0.954 on the same photo: the box
    dominates the outline, so the front details hardly move it. With f held at 1111, 1945, 4168 and 6946 px the IoU is 0.919,
    0.942, 0.964 and 0.940, so f is only loosely fixed. Outline [`overlay_eaton_5px1500rtg2.png`](analysis/out/oem/overlay_eaton_5px1500rtg2.png).

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

### McMaster 3861N11 transmitter and 5169K72 filter housing (round 5: built, not in the model; round 6: refined and placed)

- **CAD check (round 5).**
  - 3861N11: IoU 0.267. McMaster's straight lead runs out to 172.8 mm, and that dominates the score.
  - 5169K72: IoU 0.746. McMaster's part is an Ø88 can under an Ø95 lid, with the outlet nipple 2.9 mm below our datum.
- **Not refined (round 5).** Neither part is placed in the model: the lid port is SAE-4, and the gas-loop hoses are not re-routed.
- **Colours.**
  - 3861N11: black body #272727, stainless hex #aeafac.
  - 5169K72: black housing #3b3d3a, steel bail clips #a6a7a5.
- **Round 6 (2026-11-25).** Both STEP files were re-fetched through the tunnel (McMaster's file-type list → 3-D STEP →
  Download, in headed Chrome); their sha256 match the 2026-11-20 manifest. The section shapes were read off the STEPs with axial
  slices.
  - **3861N11, `mcm_3861N11()`.**
    - **Shape now:** the 1/4 NPT thread (r 5.6 to 6.9 over 12.7 mm, Ø5.4 port) with its undercut; a 27 A/F hex with its
      corners turned to Ø29, 6.5 thick; a Ø24 body; a cap tapering to the Ø13 gland; then Ø10.2 to 50.15 mm above the
      shoulder.
    - **The lead is not drawn.** The round-5 builder ended in a 20 mm cable stub instead.
    - **The comparison now drops the lead's seven stripped wire ends too.** They are solids up to 139.6 mm out, and round 5
      kept them. They hold almost no volume, but they moved the bounding-box centre used for the first alignment, so the
      round-5 0.267 was mostly misalignment. With the wire ends dropped, round 5's builder scores 0.692.

    | | Round 5 builder | Round 6 builder |
    |---|---|---|
    | Volume IoU against McMaster's CAD | 0.692 | **0.948** |
    | Volume vs McMaster | +23.5 % | +1.4 % |
    | Distance, mean / P95 / max (mm) | 1.70 / 7.58 / 11.9 | 0.24 / 1.48 / 8.3 |

    The 8.3 mm maximum was not traced to a feature.
  - **5169K72, `mcm_5169K72()`.**
    - **Shape now:** a Ø27.7 outlet boss 14.9 tall; the Ø87.9 can; the side inlet boss (Ø25.5 at z 48.8, reaching x 57.4) on
      a Ø42 pad; the Ø95 lid tapering to Ø76; two bail clips (hinge bracket, latch lever, Ø3 wire hook over the lid).
    - Round 5 drew one Ø95.2 can over the full height.

    | | Round 5 builder | Round 6 builder |
    |---|---|---|
    | Volume IoU against McMaster's CAD | 0.746 | **0.949** |
    | Volume vs McMaster | +30.6 % | 0.0 % |
    | Distance, mean / P95 / max (mm) | 4.06 / 10.9 / 13.9 | 0.84 / 4.98 / 13.1 |

    The P95 and maximum come from the clip wires, which are drawn as straight Ø3 rods.
  - **Silhouettes from McMaster's product images, cameras solved** (round 5's method):

    | Part | IoU, round 5 builder | IoU, round 6 builder | f (px, 35 mm equiv.) | Outline mean |
    |---|---|---|---|---|
    | 3861N11 | 0.925 | **0.925** | 2587, 133 mm | 3.8 px (0.57 mm) |
    | 5169K72 | 0.887 | **0.897** | 2682, 126 mm | 14.9 px (2.45 mm) |

    - The 3861N11 image shows the coiled lead, so its mask is cut on a line square to the axis at the cable gland's end (`CUTS` in
      `photo_fit.py`).
    - The 5169K72 score is held down by the clip wires, which spread wider in the photo than the drawn hooks.
    - Outlines: [`overlay_mcm_3861N11.png`](analysis/out/oem/overlay_mcm_3861N11.png),
      [`overlay_mcm_5169K72.png`](analysis/out/oem/overlay_mcm_5169K72.png).
  - **In the model.** See the Round 6 section above: the transmitter on its SAE-4 adapter, and the housing on KF-25 adapters and
    elbows.

### Edwards nXDS6i dry scroll pump (BOM G2) — `edwards_nxds6i()` (round 6, 2026-11-25)

- **Sources.**
  - Edwards publishes no CAD for the nXDS. Its dimension drawing appears on page 3 of Provac's
    [nXDS 6i/10i/15i/20i datasheet](https://cdn.shopify.com/s/files/1/0598/4021/files/nXDS-6i_10i_15i_20i.pdf), which notes
    "all variants are the same". It has six views: fan end, both sides, motor end, top and bottom.
  - Edwards' [webshop page for A73501983](https://global.my.edwardsvacuum.com/en/Catalog/Pumps/Dry-Scroll-Pumps/nXDSi-Scroll-Pumps/nXDS6i/p/A73501983)
    gives 26.20 kg, 0.432 m long and NW25 inlet and outlet.
  - The cover photo of Edwards'
    [nXDS brochure](https://assets.testequity.com/te1/Documents/pdf/Edwards/Edwards_nXDS_Brochure_0425.pdf) gives the finishes.
- **Dimensioned on the drawing:**
  - 432 long; 265 over the fins, 282 with the exhaust flange (149 from the centre line);
  - 302 to the lifting eye, 286 to the cowl, 285 to the inlet flange; the cowl and fan axis 160 above the feet;
  - the NW25 inlet 225 from the motor end and 55 off the centre line;
  - the NW25 exhaust on the side, 145 high and 347 from the motor end;
  - feet 189 across, mounting slots on a 230 × 120 pattern.
- **Read off the views at 1.37 px/mm (±3 mm):**
  - the finned scroll housing: round about the cowl axis, widening from a half-width of 110 at the motor end to 128 at
    x 300, with 8 side fins; its top at z 245, a motor-end block to z 256, and a shoulder rising to the cowl;
  - the R 130 fan cowl with a ~30 mm end radius, its underside sweeping from the base up to z 100 at the fan end;
  - the fan guard (concentric rings, five bars 4 mm proud);
  - a 220-wide base with the connector panel on the exhaust side;
  - a Ø38 lifting eye on a boss.
- **Check against the drawing** ([`drawing_fit.py`](cad/oem/drawing_fit.py),
  [`drawing_fit_edwards_nxds6i.png`](analysis/out/oem/drawing_fit_edwards_nxds6i.png)).
  - **Method.** Each view's outline was segmented from the line drawing, and the extension lines that close loops with the
    outline were erased first (front view). The builder was projected orthographically in the same direction, at the
    drawing's own scale (432 mm = 590.8 px at 300 dpi), with the offset fitted.
  - **Before** is the envelope the pump replaces, in the same frame.

  | View | IoU, envelope | IoU, `edwards_nxds6i()` | Outline mean / P95 (mm), before → after |
  |---|---|---|---|
  | Fan end | 0.888 | **0.928** | 7.6 / 21.2 → 4.5 / 13.6 |
  | Side, exhaust side | 0.848 | **0.926** | 12.6 / 46.3 → 6.0 / 33.9 |
  | Side, back | 0.848 | **0.927** | 12.4 / 46.2 → 5.9 / 32.8 |
  | Motor end | 0.876 | **0.943** | 8.4 / 26.2 → 3.4 / 13.2 |
  | Top | 0.876 | **0.892** | 10.2 / 25.1 → 11.8 / 63.9 |
  | Mean | 0.867 | **0.923** | |

  - **Free scale.** With the scale also fitted, the side and end views settle within 1 % of the drawing's scale (0.993 to
    1.007), so the model's size agrees with the dimensions.
  - **The two outliers.**
    - The fan-end view wants 3 % more: the cowl's upper corners are squarer than the R 130 circle.
    - The top view prefers 0.954 and then scores 0.942. The side views share its 432 mm length and fit at 0.99 to 1.01, so
      either the sheet draws the plan smaller or its outline lost the ends. The 64 mm P95 at the drawing's scale is the fan
      end's plan corners.
- **Colours** (brochure cover; the fan end is under a translucent overlay, so the cowl takes the housing's paint):

  | Body | Colour | m | r |
  |---|---|---|---|
  | Housing, fins and cowl (painted cast aluminium) | #c9c9c9 | 0 | 0.95 |
  | Base | #c1c0c0 | 0 | 0.95 |
  | Connector panel | #cccdcc | 0 | 0.76 |
  | NW25 inlet / exhaust flanges, lifting eye (stainless) | #bcaea6 / #c4bab0 / #bfc3b7 | 1 | 0.58–0.87 |
  | IEC inlet | #181a1d | 0 | |
  | START / STOP keys | #7bb85f / #cb7063 | 0 | |

  The stainless reads warm (#bcaea6): the photo has a warm cast.
- **Not drawn:** the gas-ballast knob, the cast 'nXDS' lettering, the panel's sockets and LEDs, the inside of the fan cowl.

### McMaster 4396K21 pump (built, not in the model)

- No vendor CAD, so it was not refined.
- **Colours.** Black motor #383838; aluminium block #aeaeae.

## 4. Checks

- **Static contacts of the parts changed in this round** (`cad/oem/contact_check.py`, M50, closed and parked).
  - Each changed part was intersected exactly with every part whose box it touches, on this tree and on 0dbb5a3.
  - Before and after alike there is one contact: the IPG chassis with the armoured process fibre where the fibre enters it,
    which is a designed joint.
  - Its shared volume went from 5,760 to 4,189 mm³, because the fan-grille recess now takes some of the chassis there.
  - No new contact appeared.
- **Exact interference sweep, M50/M** (`analysis/interference.py`, 597 s): **0 interferences**.
  - It covers all 5 static states and all 8 motion sweeps: recoater, piston, door, guard door, cartridge, drawer, Z stage
    and module.
  - The 18 designed joints are unchanged.
  - The only gap changes are +0.02 mm, between the overflow clamp and the module on its swap path (0.50 → 0.52 mm).
- **Exact interference sweeps, S25/S (585 s) and L75/L (516 s):** **0 interferences** in all 5 static states and 8 motion
  sweeps. S25 has 17 designed joints and L75 has 18, both unchanged. The only gap changes are the same +0.02 mm at the
  overflow clamp.
- **`vendor_parts.py inventory`:** 63 bought parts, 17 drawn as real parts.
- **`vendor_parts.py verify`**, against the re-fetched McMaster CAD:
  - The volume deltas match the IoU table: clamps +5.6 / +1.7 %, valve −6.9 %, carriage +3.2 %, stepper +0.8 %.
  - The sorted extents match within 0.1 mm, except the valve body, which is now 58.6 against the vendor's 60.45 mm
    (it was 59.8).

## 5. Not done

- **(d) multi-view / NeRF-style reconstruction.** Skipped. Two videos were found but not downloaded:
  - Teknic's ClearPath SD overview (YouTube, linked from the ClearPath products page);
  - IPG's Wistia video on the ultra-compact laser page.

  The 20-minute time box went on the silhouette fits instead. The next step is frames from the Teknic video, then COLMAP
  (Docker) for the intrinsics and poses, then a visual hull against `clearpath_sd_231x()`.
  **Round 6:** done; see the Round 6 section.
- **Eaton product pages.** eaton.com and the Tripp Lite product page return 503 through the tunnel, even in headed Chrome. So
  the Eaton front comes from the datasheet's photo alone. **Round 6:** the SKU page loaded on 2026-11-25, and its 2000 px
  images now set the front.
- **Lens, galvo and collimator.** Another agent's area this round.
- **The rack drawer, PC and the other envelope parts** listed in `analysis/out/real-parts/inventory.md`. They have no vendor
  part chosen yet.
- **Texture.** The perforations, the fan-grille dots and the labels are colours in the render, not geometry or texture
  maps. Still true after round 6.
- **Still not done after round 6.**
  - No silhouette fit for the IPG. Its only 4U image is a group render in which another unit sits on it.
  - No silhouette fit for the nXDS6i against a photo. The brochure photo has a translucent overlay over the fan end; the
    drawing's five views stand in.
  - The SAE-4 adapter, the KF-25 filter adapters and elbows and the filter's stand have assumed dimensions: no part is chosen.
  - `lpbf_low.py` still gives each part one colour. The measured finishes are used only by `render_oem.py`.
