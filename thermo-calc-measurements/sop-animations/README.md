# The five measurement SOPs, animated step by step (#262)

Every step of the five draft SOPs in [`../sops/`](../sops/), drawn in 3-D on CAD models of the instruments. Each new
model is sized from the maker's published dimensions and registered to frames of the real machine. Each video also
shows the data its measurement produces: synthetic inputs run through this repo's own analysis code
([`../analysis/`](../analysis/)).

<!-- WATCH -->

| SOP | Video | Steps | Length |
|---|---|---|---|
<!-- VIDEOS -->

## How it is built

- **Framework.** byu-vcl's vertical-lab code, from [byu-vcl PR 318](https://github.com/vertical-cloud-lab/byu-vcl/pull/318). `vl_fetch.py` fetches it into the git-ignored `vl/`, pinned to commit `0425020`. It supplies:
  - the scene: PyVista/VTK, rendered off-screen, captions drawn with PIL, frames piped to ffmpeg;
  - CadQuery instrument models with joints;
  - `register.py` / `frames.py`, which fit a model to video frames;
  - `people.py`: MakeHuman's CC0 body, skinned, in a lab coat and nitrile gloves;
  - `runner_guard.py`, which keeps several renders from running the runner out of memory.

  This folder adds:
  - `stage.py`: the bench, rigs, mesh cache, data panels, title cards and chapter joins;
  - `fit.py`: `register.py`, pointed at `refs/`;
  - `audit.py`: an FCL collision check on every frame;
  - `longform.py`: one video with chapters and narration;
  - `validation.py`: the table below.
- **Reused models** (byu-vcl):
  - the lab's own **LECO PX500** polisher, fitted to the lab's SOP videos;
  - the **LECO MX400** mounting press;
  - the **Nabertherm NAT 15/65** furnace, fitted to Nabertherm's video;
  - the **Mitutoyo HM-220** micro-Vickers;
  - the **Labconco** fume hood;
  - the **Keyence VHX-7000**;
  - the **Hitachi TM4000PlusII**;
  - a quench tank.
- **New models** (this PR), in `models_dsc.py`, `models_track.py`, `models_density.py`, `models_props.py` and `models_chem.py`. Each one's sources and fit are in `notes/<key>.md`.
- **Edison** (`edison/`): three `LITERATURE_HIGH` searches on the hardware and handling behind each step. They give crucible sizes, purge flows, calibration standards, mounting and polishing parameters, Archimedes practice, Vickers and eddy-current practice, ICP-OES digestion and inert-gas fusion. Each folder has the query, answer, artifacts, references and full trajectory.

## What "validated" means here

<!-- VALIDATION -->

## Run it

```bash
python vl_fetch.py                                   # byu-vcl's framework into vl/ (pinned)
pip install cadquery pyvista trimesh pillow numpy scipy python-fcl matplotlib opencv-python-headless kokoro-onnx soundfile
xvfb-run -a python sop01_dsc.py                      # each chapter -> out/mp4/sop01_c*.mp4, then joined -> out/mp4/sop01.mp4
PREVIEW=1 xvfb-run -a python sop01_dsc.py            # only the last frame of each sub-step: a contact sheet in /tmp
VIZ3D_SIZE=1920x1080 VIZ3D_FPS=30 xvfb-run -a python sop01_dsc.py   # the delivered resolution and rate
python fit.py solve dsc_sta && xvfb-run -a python fit.py draw dsc_sta   # registration and its overlays
python longform.py cards && python longform.py build # the long-form, narrated, with chapters
python validation.py                                 # out/validation.md
```

Frames from makers' videos and photos are not committed. Each view's JSON in `refs/` has the source URL (and the
video ID and time), so `fit.py` fetches them again through a Pi.

## Limits

<!-- LIMITS -->
