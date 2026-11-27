# The seven laserbeamFoam runs, rerun in the final review (2026-11-27)

The files here are the same kind as the originals one folder up, written by the same post-processing
(`scripts/keyhole_cfd_laserbeamfoam.py post`):
- `<run>-summary.json`;
- `<run>-pool-vs-time.csv`;
- `<run>-absorbed-power-vs-time.csv`.

`amalgamation-summary.json` is `scripts/keyhole_amalgamation.py` rerun on them.

**How they were made:**
- **The build.** openfoam.com's apt repository served the runner a bot-check page, so OpenFOAM v2506 came from
  the official Docker image `opencfd/openfoam-dev:2506` (Ubuntu 24.04, gcc 13.3). laserbeamFoam `38a6d38` was built
  in it with `./Allwmake` and `wmake`.
- **The runs.** Each committed case in [`../cases/`](../cases/) was copied unchanged and run with `./Allrun 2` from
  t = 0, then `reconstructPar -fields '(T alpha.metal U)'`. Unlike three of the originals, none was restarted
  partway.
- **Pauses.** The container was paused twice while other jobs needed the runner's cores. That doesn't change the
  results, but it does make the `blend-fresnel-rho65` log's clock time long.

What they show is in the keyhole write-up,
[`../../README.md`](../../README.md#rerun-in-the-final-review).
