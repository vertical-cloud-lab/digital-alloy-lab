"""Toolpaths from the OpenCAMLib runs (cam_ocl.py): G-code, pictures, and a check of the dexel simulation against OCL.

For each OCL job it
  - turns the drop-cutter grid into a zig-zag raster finishing toolpath (tool tip z = max(z_cutter, z_holder - stick-out)),
    and writes it as G-code (G0/G1, mm, the setup frame of cam_ocl.ROT) to /tmp/mach-work/cam/<job>.nc;
  - draws the part with the raster (blue) and OCL waterline contours (orange) -> analysis/out/machining/toolpath_<job>.png;
  - compares OCL's cutter-location z with cam_sim.py's grey dilation of the voxel height map for the same cutter
    (the basis of the stock-removal simulation) -> toolpaths.json.

Run:  /tmp/capmem 3 xvfb-run -a -s "-screen 0 1600x1024x24" /tmp/venv/bin/python desktop-lpbf/analysis/machining/toolpaths.py
"""
from __future__ import annotations

import json
import pathlib
import sys

import cv2
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cam_sim as CS  # noqa: E402

OUT = CS.OUT
CAM = pathlib.Path("/tmp/mach-work/cam")
PARTS = pathlib.Path("/tmp/mach-work/parts")
JOBS = [  # (npz, part slug, stick-out mm, pitch for the cross-check, label)
    ("ocl_chamber_z", "process_chamber_body_6061_t6_6_4_l", 114.0, 0.5, "chamber body, +Z, 1/2 in. x 6 in. OAL end mill, ER32 holder"),
    ("ocl_lid_z", "chamber_lid_6061_t6_16_mm_cover_slide_drawer_slot", 32.0, 0.4, "lid, +Z, 1/4 in. end mill"),
    ("ocl_door_y", "chamber_door_6061_t6_15_mm_drops_down", 32.0, 0.4, "door, +Y (seal face), 1/4 in. end mill"),
    ("ocl_spigot_z", "build_module_m50_spigot_flange_honed_316l_cylinder_50_8_bore", 32.0, 0.4, "M50 module body, +Z, 1/4 in. end mill"),
]


def raster(d, stick):
    z = d["z_cl"].copy()
    if "z_holder" in d:
        z = np.maximum(z, d["z_holder"] - stick)
    xs, ys = d["xs"], d["ys"]
    pts = []
    for j, y in enumerate(ys):
        row = list(range(len(xs)))
        if j % 2:
            row.reverse()
        pts.extend((xs[i], y, z[j, i]) for i in row)
    return np.array(pts), z


def gcode(pts, path, safe):
    with open(path, "w") as f:
        f.write("(raster finishing toolpath from OpenCAMLib BatchDropCutter; setup frame; mm)\nG21 G90 G17\n")
        f.write(f"G0 Z{safe:.3f}\nG0 X{pts[0, 0]:.3f} Y{pts[0, 1]:.3f}\nG1 F1200\n")
        for x, y, z in pts:
            f.write(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f}\n")
        f.write(f"G0 Z{safe:.3f}\nM30\n")


def main():
    import pyvista as pv
    pv.OFF_SCREEN = True
    out = {}
    for name, slug, stick, pitch, label in JOBS:
        d = dict(np.load(CAM / f"{name}.npz"))
        R = d["R"]
        pts, ztip = raster(d, stick)
        gcode(pts, CAM / f"{name}.nc", float(d["hi"][2]) + 20)
        # cross-check: OCL z_cl vs grey dilation of the voxel height map (same cutter), in the setup frame
        tris = CS.read_stl(str(PARTS / f"{slug}.stl")) @ R.T
        lo, shape = CS.grid_for(tris, pitch, 15.0)
        vox, _ = CS.voxelize(tris, pitch, lo, shape)
        nz = shape[2]
        occ = vox.any(axis=-1)
        top = np.where(occ, nz - np.argmax(vox[..., ::-1], axis=-1), -1e6).astype(np.float32)
        D = {"ocl_chamber_z": 12.7}.get(name, 6.35)
        zcl_vox = cv2.dilate(top, CS.disk(D / 2 / pitch), borderType=cv2.BORDER_CONSTANT, borderValue=-1e6)
        X, Y = np.meshgrid(d["xs"], d["ys"])
        ix = np.clip(np.floor((X - lo[0]) / pitch).astype(int), 0, shape[0] - 1)
        iy = np.clip(np.floor((Y - lo[1]) / pitch).astype(int), 0, shape[1] - 1)
        zv = lo[2] + pitch * zcl_vox[ix, iy]
        zo = d["z_cl"]
        touch = (zo > d["zmin"] + 0.5) & (zv > -1e5)
        diff = (zo - zv)[touch]
        stats = dict(points=int(touch.sum()), median_mm=round(float(np.median(diff)), 3), p95_abs_mm=round(float(np.percentile(np.abs(diff), 95)), 3),
                     within_pitch_pct=round(100.0 * float((np.abs(diff) <= pitch + 1e-6).mean()), 1))
        # picture: part (in the setup frame) + raster + waterlines
        import trimesh
        m = trimesh.Trimesh(vertices=tris.reshape(-1, 3), faces=np.arange(len(tris) * 3).reshape(-1, 3), process=True)
        pm = pv.wrap(m)
        pl = pv.Plotter(off_screen=True, window_size=(1100, 760))
        pl.add_mesh(pm, color="#c9d0d6", opacity=0.55)
        step = max(1, len(d["ys"]) // 60)
        for j in range(0, len(d["ys"]), step):
            line = np.c_[d["xs"], np.full_like(d["xs"], d["ys"][j]), ztip[j] + 0.3]
            pl.add_mesh(pv.lines_from_points(line), color="#1f77b4", line_width=1.2)
        if "wl" in d:
            k = 0
            for n in d["wl_n"]:
                loop = d["wl"][k:k + n]
                k += n
                if n > 2:
                    pl.add_mesh(pv.lines_from_points(np.vstack([loop, loop[:1]])), color="#ff7f0e", line_width=2.5)
        pl.add_text(f"OpenCAMLib toolpaths: {label}\nblue: drop-cutter raster (every {step}. pass shown), orange: waterlines\n"
                    f"OCL vs dexel sim cutter-location z: median {stats['median_mm']:+.2f} mm, {stats['within_pitch_pct']:.0f} % within one voxel",
                    font_size=9, color="black")
        pl.set_background("white")
        pl.camera_position = "iso"
        pl.camera.azimuth = -30
        pl.camera.elevation = 10
        pl.reset_camera()
        pl.camera.zoom(1.2)
        pl.screenshot(str(OUT / f"toolpath_{name[4:]}.png"))
        pl.close()
        out[name] = dict(label=label, cl_points=int(zo.size), gcode_lines=len(pts), check=stats,
                         waterline_loops=int(len(d["wl_n"])) if "wl" in d else 0)
        print(name, out[name], flush=True)
    (OUT / "toolpaths.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
