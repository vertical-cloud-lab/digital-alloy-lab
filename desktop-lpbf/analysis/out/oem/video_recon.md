# ClearPath from Teknic's product video: COLMAP reconstruction against `clearpath_sd_231x()` (round 6, 2026-11-25)

Made by [`cad/oem/video_recon.py`](../../../cad/oem/video_recon.py); every number is in [`video_recon.json`](video_recon.json).
Nothing from the video is committed: frames, masks and the COLMAP workspace stay in `/tmp/oem/video`. The two figures show
only outlines, our model and the reconstructed points.

**Result:** COLMAP solved all 74 frames of a turntable shot (281.9° of the motor seen), but the
reconstruction does not keep the motor's proportions: fitting one scale per axis spreads them by 26.2 %. So our model
fits it only to a median silhouette IoU of 0.8119 over all 74 views, with 48.7 % of the points within 1 mm
and 25.4 % within 0.5 mm. That is not a measurement of our model to 0.5 mm. The likely cause is the focal length,
which a narrow-angle turntable shot fixes poorly.

## Video

- Teknic, "ClearPath: Teknic's Integrated Brushless Servo Motor, Drive and Encoder", YouTube [`_SYhCRwacDs`](https://www.youtube.com/watch?v=_SYhCRwacDs), linked from
  [Teknic's ClearPath page](https://teknic.com/products/clearpath-brushless-dc-servo-motors/). Fetched with yt-dlp through the lab tunnel, since YouTube asks the runner
  to sign in. 1280 × 720, 29.97 fps, sha256 `4c69d76229ce93a878a4037dbaa72b8063a238d831303f9e3ddd39b1cbe8c7f2`.
- **Segment:** 598.6–606.0 s. The motor turns about a vertical axis in front of a fixed camera on
  a white backdrop, from shaft-left through the rear to nearly shaft-on. It is a turntable render of Teknic's own 3D model,
  not footage of a real unit. The ClearPath logo and three lines of text sit over the left of the frame and stay still.
- **Frames:** 74 at 10 fps, full frame. Each frame's foreground is the largest connected region
  darker than the backdrop (minimum RGB channel below a threshold), closed and hole-filled. The overlay text is a separate
  region, so it drops out. COLMAP got that mask at threshold 235, dilated 4 px, so all its features are on the motor.
- **First video tried:** "ClearPath-SD (Step and Direction) Series Overview" (`-gigcf7ZzAQ`, the SD page's video). It
  shows the motor only in still poses, so it has no multi-view segment.

## COLMAP

COLMAP 3.12.6 (Ubuntu's build, no CUDA), under the 3 GB cap with 2 threads:
- SIFT on the CPU, up to 8,192 features per frame at full resolution (585–2,524 found, median 1,572);
- exhaustive matching with guided matching;
- the incremental mapper, with one SIMPLE_RADIAL camera for all frames and the principal point fixed at the image centre.

| | |
|---|---|
| Registered frames | **74 of 74** |
| 3D points | 13,502 (mean track 4.88 frames) |
| Reprojection error | mean 0.838 px, median 0.642 px |
| Focal length | 2673.0 px, 78.8 mm in 35 mm terms (horizontal field of view 26.9°) |
| Radial distortion k1 | -0.36155. A render has none, so this is a first sign that the intrinsics absorb an error |
| Solved camera path | an arc of 281.9° round the motor, in one plane (out-of-plane RMS 0.41 % of the radius). Its radius varies 19.87 % (1 sd), where a fixed camera and a turntable give a circle: a second sign of the distortion |

Dense MVS (`patch_match_stereo`) needs CUDA, so it was not run. A visual hull from the solved cameras stands in for it.

## Alignment, scale and distances

- **Cloud:** 9,966 points after filtering (reprojection error < 2 px, track >= 3, kNN(8) mean-distance outliers > mean + 2.5 sd removed).
- **Rejected start:** unconstrained start (centroid + principal axes, 24 axis rotations, trimmed ICP with scale): best trimmed mean 1.11 mm at 84.4 mm per unit, but a median silhouette IoU of 0.53 at that pose, so it converged on a wrong fit of the sparse cloud.
- **Rejected free rotation:** an earlier run with the 3-D rotation free as well tipped the model shaft-up within one 350-evaluation pass (mean IoU 0.76 on the fitted views, not converged); the frames show the shaft level, so the rotation is held upright.
- **Alignment used:** turntable frame (orbit axis = model +y, connector block up), turn about it scanned in 10 deg steps x 6 scales by silhouette IoU on every 6th view, then Nelder-Mead over 5 DoF (turn about the vertical, translation, scale; the model kept upright) on the T220 masks of every 3rd view (25), half resolution, silhouettes splatted from 120,000 surface samples, two passes, 356 evaluations. Mean IoU over those views: 0.6239 → 0.8072.
- **Known dimensions measured in the cloud** at that pose:
  - flange plate (z −6 to 0): 111 points spanning 61.36 × 62.94 mm (0.5–99.5 percentiles), against the
    drawing's 59.1 mm square;
  - shaft: 10.76 mm across from 12 points (drawing 9.5 mm);
  - the cloud runs from z -83.86 to 15.53 (0.5 and 99.5 percentiles); the drawing runs from the pin
    tips at -84.81 to the shaft end at +20.57.
  - Scaling the cloud so the flange measures 59.10 changes the silhouette scale by -4.91 %;
  - letting ICP choose the scale changes it by -3.26 %.
- **Proportions:** fitting a separate scale on each model axis (diagnostic only) gives x 0.8622, y 1.0172, z 1.0878: a
  26.2 % spread. A Euclidean reconstruction gives three equal scales, so the cloud's proportions differ from
  the motor's. With those scales, the median distance would be 0.872 mm and
  56.8 % of points would be within 1 mm.

**Cloud to our model's surface** (distance to the nearest of 1,000,000 points sampled on it, about 0.25 mm apart, so up to
about 0.1 mm high):

| Pose and scale | Mean | Median | P95 | Within 0.5 mm | Within 1 mm | Within 2 mm |
|---|---|---|---|---|---|---|
| Silhouette fit, no ICP | 2.257 | 1.162 | 8.343 | 22.5 % | 44.3 % | 62.6 % |
| Rigid ICP, silhouette scale | 1.894 | 1.036 | 6.542 | 24.9 % | 48.5 % | 68.9 % |
| Rigid ICP, scale set by the flange (59.10 mm) | 1.903 | 1.028 | 6.833 | **25.4 %** | **48.7 %** | 69.6 % |
| ICP with free scale | 1.893 | 1.017 | 6.951 | 26.3 % | 49.3 % | 69.9 % |

## Silhouettes through the solved cameras

Our model is projected through each of the 74 solved cameras (with k1, filled one triangle at a time) and compared
with that frame's foreground mask. The silver flange and rear cover are nearly white where they catch the light, so the
mask depends on the threshold: 220 keeps them, lower thresholds cut into them. The backdrop's soft shadow under the motor is
darker than 220, so the T220 mask also takes in a band of shadow. The "shadow rows cut" line drops the rows below our
model's lowest point in both masks.

| Pose | Mask | Median IoU | Min | Max |
|---|---|---|---|---|
| Silhouette fit | T180 | 0.8014 | 0.6713 | 0.8959 |
| Silhouette fit | T200 | 0.8135 | 0.6844 | 0.8884 |
| Silhouette fit | T220 | 0.8119 | 0.735 | 0.8742 |
| Silhouette fit | T220 shadow rows cut | 0.8223 | 0.7405 | 0.8742 |
| Rigid ICP, scale set by the flange (59.10 mm) | T220 | 0.7934 | 0.7141 | 0.8939 |
| Rigid ICP, scale set by the flange (59.10 mm) | T220 shadow rows cut | 0.7954 | 0.7141 | 0.8939 |

[`video_recon_silhouettes.png`](video_recon_silhouettes.png): six of the views, the frame mask's outline in black and our
model's in red, at the silhouette-fit pose.

## Visual hull

Voxels of 1.0 mm in our model's frame (silhouette-fit pose) are kept where they project inside the mask
(T220 dilated 1 px) in at least 95 % of the solved views. A visual hull can't see concavities, so it is an outer bound: the gaps
between the pin fins, the connector pockets and the steps between the flange and the body all stay filled. The shadow
band adds to its bottom.

| Hull | Volume (cm³) | IoU with our model | Our model inside the hull |
|---|---|---|---|
| all views | 331.3 | 0.6191 | 84.4 % |
| 95 % views | 372.0 | 0.6052 | 88.8 % |
| our model | 271.6 (exact) | | |

Surface distances, ≥ 95 % hull: hull to model mean 5.04 mm (P95 11.95), model to
hull mean 4.37 mm (P95 9.87); chamfer (mean of the two) 4.7 mm.

## What this does and does not show

- The video is Teknic's render of its own CAD. So at best this checks our builder against Teknic's model by a second route;
  the STEP comparison in [`cad_compare.md`](cad_compare.md) is the first, and the better one (IoU 0.661). It says nothing about
  how a real unit differs from Teknic's CAD, and the intrinsics are those of a virtual camera.
- The solve is self-consistent (sub-pixel reprojection error, all frames registered), but its proportions are off, and k1 is
  large for a render. A narrow field of view (about 27°) and an object that only turns about one axis leave the focal length
  weakly fixed, and an error in it stretches the reconstruction. Fixing f to candidate values and re-running the mapper
  would test that; it was not run (about 15 min per mapper run on the shared runner).
- The sparse points sit where SIFT finds texture: the pin fins, the connector block, the cover screws, the flange's edges and
  holes, and the body's ribs. Smooth faces have few points, so the distance numbers weight those features.
- Not done: dense MVS (needs CUDA) and a NeRF or Gaussian splat (not quick on 4 shared CPU cores).
- [`video_recon_cloud.png`](video_recon_cloud.png): the aligned cloud over our model in three views, coloured by distance,
  and the solved camera path.

## Focal-length test (2026-11-25)

To test whether the distortion comes from a mis-solved focal length, the mapper was re-run on the same features and
matches with f held fixed and k1 = 0 (a render has no lens distortion). 1778 px is a 50 mm lens on a 36 mm-wide sensor,
a common default in 3D render tools; 4010 and 6000 px are 1.5 and 2.25 × the self-calibrated f. Each mapper run took 6.5-9.3 min.
Each model was compared with ours the same way: the first
run's pose carried over through the camera centres, refitted on the silhouettes (upright, every 6th view), then the per-axis
scales, the flange, the distances (rigid ICP at the flange scale) and the IoU over all views.

| f (px) | k1 | Registered | Points | Reproj. (px) | Orbit radius sd | Per-axis scales x / y / z | Spread | Flange (mm) | Median IoU, all views | Within 1 mm |
|---|---|---|---|---|---|---|---|---|---|---|
| 2673 (self-calibrated) | -0.36155 | 74 | 13,502 | 0.838 | 19.87 % | 0.8494 / 1.0072 / 1.083 | **27.5 %** | 64.3 × 64.7 | 0.8108 | 49.7 % |
| 1778 (fixed, k1 = 0 (50 mm lens)) | 0.0 | 74 | 13,875 | 0.844 | 22.13 % | 0.8365 / 1.0213 / 1.1325 | **35.4 %** | 54.8 × 61.1 | 0.8086 | 47.7 % |
| 4010 (fixed, k1 = 0 (1.5x)) | 0.0 | 74 | 12,761 | 0.842 | 18.74 % | 0.8511 / 1.021 / 0.8896 | **20.0 %** | – | 0.7934 | 48.6 % |
| 6000 (fixed, k1 = 0 (2.25x)) | 0.0 | 74 | 12,226 | 0.852 | 18.42 % | 0.6365 / 0.9905 / 0.792 | **55.6 %** | 23.7 × 66.6 | 0.7777 | 17.7 % |

f 4010: no cloud points fell in the flange plate's slab at this pose, so the 'flange-scaled' ICP kept the silhouette scale.

f 6000: the carried-over pose started at a mean IoU of 0.34 and the 150-evaluation refit stopped at 0.77, not converged, so this run's spread, flange and distances are not reliable.

**Result:** the focal length changes the distortion but does not remove it, and the frames cannot tell the values apart. The per-axis spread is 35.4 % at f 1778, 27.5 % at the self-calibrated 2673 and 20.0 % at 4010. At 6000 it is 55.6 %, but that pose fit did not converge. The solved orbit's radius sd falls only from 22.1 % to 18.4 % over the whole range. The mean reprojection error is the same for all four (0.84-0.85 px), so this turntable shot does not fix f. Over the first three, the median silhouette IoU over all views barely moves (0.81, 0.81, 0.79), and neither does the share of points within 1 mm (48-50 %). The least distorted run (f 4010) is still 20 % out of proportion, with a camera path far from a circle. Something besides f is off, perhaps a camera that also moves or zooms in Teknic's render. The video can't check our model to better than a few mm.
