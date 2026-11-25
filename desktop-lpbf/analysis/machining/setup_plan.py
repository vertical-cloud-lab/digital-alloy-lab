"""Setup plan for the machined parts of the desktop LPBF (issue #260, PR #266): 3-axis against 4th-axis, and the full process
plan for the chamber's through-frame and floor plate (chamber-construction.md).

1. Every machined part (inventory.py's STLs): the six axis directions a tool can reach each piece of the part's skin from
   (cam_sim.py's dexel reach, a 1/8 in. tool of unlimited reach), then
     3-axis   the fewest setups (greedy cover), each a vise or fixture-plate setup;
     4th axis for a rotary axis along the part's x, y or z: one clamping reaches the four directions square to it (the part is
              held by an end face, which is not machined in that clamping), and the leftover skin needs the +/-axis
              directions as extra 3-axis setups. The best axis, its swing radius against the Haas HRT210's 152.4 mm centre
              height, and the mass against its 38.6 kg unsupported limit;
     5-axis / special tool: skin no axis direction reaches (undercuts: grooves, dovetails, bayonet lugs, the camera boss).
2. The frame and the floor plate: blank, core removal, every setup (machine, fixture, which face is up as a rotation from the
   model frame, A-axis index angles), and per operation the feature, the tool (type, diameter, stick-out), the cuts it makes as
   references to the model code (lpbf_low.CHAMBER_OPS ids "FR-xx" / "FP-xx" and joints.py keys "J:<key>", whose solids are in
   joints.CUTS), and a time from vendor feeds and speeds (sources in FEEDS).
Writes desktop-lpbf/analysis/out/machining/setup_plan.json (the build animation reads it).

Run after inventory.py:  OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/setup_plan.py
(~3 min: one model build for the op volumes, then the voxel reach of every part). $MACH_PARTS overrides inventory.py's
output folder (default /tmp/mach-work/parts).

Since 2026-11-25 the frame and floor-plate setups also carry what freecad_cam.py actually programs ("program": the FreeCAD
jobs, the G-code recount and the CAMotics time, from freecad_cam.json and camotics/camotics_sim.json when they exist), the
workholding holder_check.py checked (edge clamps, no end tabs; the dummy-floor plate flush with the frame; the floor
plate held through its port), and F-S3 as programmed per A index: programmed minutes from the G-code plus an estimate for
the spot drills, taps, STI taps, reamers and SAE port tools, which are not programmed.
"""
from __future__ import annotations

import json
import os
import math
import pathlib
import sys
import time

import numpy as np
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "desktop-lpbf" / "cad"))
import cam_sim as CS  # noqa: E402

OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "machining"
PARTS = pathlib.Path(os.environ.get("MACH_PARTS", "/tmp/mach-work/parts"))
IN = 25.4

# ---------------------------------------------------------------------------------------------------------------- machines
VF4 = dict(model="Haas VF-4", travels_mm=[1270, 508, 635], nose_to_table_mm=[107, 742], table_mm=[1321, 495], t_slots="5 x 16 mm at 80 mm",
           spindle="CT40/BT40, 8100 rpm, 22.4 kW, 122 N m at 2000 rpm", atc="20 pockets, tool max Ø89 mm / 5.4 kg, tool-to-tool 4.2 s",
           source="https://www.haascnc.com/machines/vertical-mills/vf-series/models/medium/vf-4.html (fetched 2026-11-20 22:27 UTC)",
           byu="ME Prototyping Lab (EB 117) per machining.md's 14:00 UTC fetch; not re-confirmed on the live page at 22:44 UTC")
HRT210 = dict(model="Haas HRT210 rotary table (4th axis, A)", platter_d_mm=210, centre_height_mm=152.4, max_kg_with_tailstock=77.1, max_kg_unsupported=38.6,
              t_slots="6 at 60 deg", brake_Nm=271, backlash_arcsec=30,
              source="https://www.haascnc.com/machines/rotaries-indexers/rotary-tables/models/hrt210.html (fetched 2026-11-20 22:31 UTC)",
              byu=("no BYU page names a rotary model; Physics' Haas VF-2SS 'provides new capabilities like a 4th axis' "
                   "(https://physics.byu.edu/department/news/2020-08-new-mill-becomes-part-of-the-p-a-family, 22:31 UTC), "
                   "and the BYU machinist who reviewed the design says the shop has 4-axis machines"))

# ---------------------------------------------------------------------------------------------------------------- feeds
FEEDS = {
    "endmill_6061": dict(sfm=(1600, 2400), fz_in={"1/2": dict(slot=(.0035, .0047), heavy=(.0047, .0063), light=(.0058, .0079), finish=(.0035, .0047)),
                                                   "3/4": dict(slot=(.0053, .0071), heavy=(.0070, .0095), light=(.0088, .0119), finish=(.0053, .0071))},
                         doc="regular LOC: heavy roughing ADOC <= 1.5 D, RDOC 30-50 %; light roughing ADOC = LOC, RDOC 15-25 %; longer than regular LOC: light "
                             "roughing ADOC <= 2 D, RDOC 10-15 %; finishing RDOC 3-5 %",
                         source="Helical aluminium parameters (HAL-C-3 / H35AL-3 / H40ALV-3 / HAL-3), https://cdn.shopify.com/s/files/1/0612/0733/files/Helical_Aluminum_Parameters.pdf (22:32 UTC)"),
    "hem": dict(note="Helical HEM: RDOC 7-30 % D, ADOC up to 2 D; 1/2 in. 3-flute in 6061 at 18,000 rpm, 500 ipm, 40 % x 2 D = 100 in3/min",
                source="Helical Machining Guidebook (2016) pp. 25, 30-31, https://mae.ufl.edu/designlab/Advanced%20Manufacturing/Helical_Machining_Guidebook.pdf (22:32 UTC)"),
    "long_reach": dict(note="Haas: 'Reduce cut depth and feed by 50% for long-flute or long-reach tools'; Helical: finishing deeper than 3 x D 'may require a 50% feed rate "
                            "reduction', and use necked tools beyond 2-3 x D",
                       source="Haas HM42-3FL chart (22:41 UTC); Helical guidebook pp. 7, 10, 11"),
    "facemill": dict(sfm=(2296, 4920), fz_in=(0.0039, 0.0196), source="Haas HPAL2 insert chart, wrought aluminium (22:41 UTC)"),
    "drill": dict(sfm=659, ipr=(0.0079, 0.0102), source="Haas HCD TSC carbide drills, wrought aluminium (22:41 UTC)"),
    "tap": dict(sfm=(33, 65), source="Haas metric aluminium taps 10-15 m/min; Haas ALU tap chart 50-65 SFM (22:41 UTC)"),
    "deflection": dict(note="end mill as a solid rod of 0.7-0.8 x D in delta = F L^3 / (3 E I), I = pi D_e^4 / 64",
                       source="Mitsubishi Materials technical course, https://www.mmc-carbide.com/permanent/courses/70/cutting-edge-classification.html (22:33 UTC)"),
    "waterjet": dict(note="WARDJet: 4 in. aluminium at 0.72 ipm (Q5) to 4.2 ipm (Q1); speed ~ 1/thickness^1.15 gives 0.50-2.9 ipm at 5.5 in. (scaled)",
                     source="https://www.wardjet.com/nozzle-and-orifice/ (22:39 UTC); UF EML2322L waterjet notes (22:35 UTC)"),
    "setup": dict(note="median setup 68-90 min (last good part to first good part), Modern Machine Shop Top Shops survey; manual tool setting up to 6 min "
                       "per tool against 30 s with a probe (Renishaw)",
                  source="https://mmsonline.com/articles/best-practices-of-top-us-shops (22:43 UTC); Renishaw tool-setting brief (22:42 UTC)"),
}
RPM_MAX = 8100


def rpm(d_mm, sfm):
    return min(RPM_MAX, sfm * 12 / (math.pi * d_mm / IN))


# a shop running a first part runs below the vendor numbers: roughing at ~60 % of the HEM rate (air moves, ramps, lead-ins)
EFF = 0.6
TOOLS = {
    "T1": dict(type="indexable face mill, 2-1/2 in., 4 inserts (HPAL2-type)", d=63.5, flutes=4, stick_out=None, holder="CT40 shell-mill arbor"),
    "T2": dict(type="3-flute carbide end mill, 3/4 in., 1-1/2 in. LOC, 4 in. OAL", d=19.05, flutes=3, stick_out=66.0,
               holder="CT40 ER32 collet chuck, 2-1/2 in. gauge (Haas 04-0010; holder_check.py: a side-lock at 63 mm had 1.0 mm over the top face)"),
    "T3": dict(type="3-flute carbide end mill, 1/2 in., 1 in. LOC, 3 in. OAL", d=12.7, flutes=3, stick_out=38.0, holder="CT40 ER32"),
    "T4": dict(type="2-flute carbide end mill, 4 mm (O-ring grooves: R4 / R6 gland corners)", d=4.0, flutes=2, stick_out=16.0, holder="CT40 ER20"),
    "T5": dict(type="3-flute carbide end mill, 1/4 in.", d=6.35, flutes=3, stick_out=25.0, holder="CT40 ER20"),
    "T6": dict(type="carbide spot drill, 90 deg, 1/2 in.", d=12.7, flutes=2, stick_out=30.0, holder="CT40 ER32"),
    "T7": dict(type="carbide drill 3.3 mm (M4 tap drill)", d=3.3, flutes=2, stick_out=30.0, holder="CT40 ER20"),
    "T8": dict(type="carbide drill 4.22 mm, No. 19 (M4 STI)", d=4.22, flutes=2, stick_out=30.0, holder="CT40 ER20"),
    "T9": dict(type="carbide drill 5.3 mm (M5 STI)", d=5.3, flutes=2, stick_out=35.0, holder="CT40 ER20"),
    "T10": dict(type="spiral-point tap M4 x 0.7 (rigid tapping)", d=4.0, flutes=3, stick_out=30.0, holder="CT40 ER20 tap collet"),
    "T11": dict(type="STI bottoming tap M4 x 0.7", d=4.91, flutes=3, stick_out=30.0, holder="CT40 ER20 tap collet"),
    "T12": dict(type="STI bottoming tap M5 x 0.8", d=6.04, flutes=3, stick_out=35.0, holder="CT40 ER20 tap collet"),
    "T13": dict(type="carbide drill 5.8 mm + 6 mm H7 reamer (dowels)", d=6.0, flutes=2, stick_out=40.0, holder="CT40 ER20"),
    "T14": dict(type="SAE J1926 -4 port tool (spot face, O-ring cone, thread relief) + 7/16-20 UNF tap", d=12.9, flutes=2, stick_out=40.0, holder="CT40 ER32"),
    "T15": dict(type="carbide drill 5.2 mm + M6 x 0.75 tap (fibre heads)", d=6.0, flutes=2, stick_out=30.0, holder="CT40 ER20"),
    "T16": dict(type="2-flute carbide end mill, 1/16 in. (2-010 face groove, 2.3 wide)", d=1.5875, flutes=2, stick_out=6.0, holder="CT40 ER11"),
    "T17": dict(type="carbide drill 2.9 mm + 3 mm H7 reamer (3 mm dowel pins)", d=2.9, flutes=2, stick_out=25.0, holder="CT40 ER16"),
    "T18": dict(type="carbide drill 6.3 mm (M6 STI, tooling-bom D11)", d=6.3, flutes=2, stick_out=40.0, holder="CT40 ER16"),
}
# freecad_cam.py numbers its tools differently; its T -> this table's T (for the "program" records)
FC_TOOL = {1: "T1", 2: "T2", 3: "T3", 4: "T4", 5: "T9", 6: "T7", 7: "T8", 8: "T13", 9: "T5", 10: "T15", 11: "T17", 12: "T9", 13: "T18",
           14: "T13"}


def program_info():
    """what freecad_cam.py programs per setup (recount and CAMotics minutes), if its outputs exist"""
    fc_p, cs_p = OUT / "freecad_cam.json", OUT / "camotics" / "camotics_sim.json"
    if not fc_p.exists():
        return {}
    fc = json.loads(fc_p.read_text())
    cs = json.loads(cs_p.read_text()) if cs_p.exists() else {}
    out = {}
    for part in fc.get("parts", {}).values():
        for su in part["setups"]:
            c = cs.get("setups", {}).get(su["setup"], {})
            out[su["setup"]] = dict(
                recount_min=su["totals"]["total_min"], tool_changes=su["totals"]["tool_changes"],
                camotics_min=c.get("time", {}).get("camotics_min"), rapids_through_stock=c.get("n_rapids_through_stock"),
                ops=[dict(label=m.get("label"), tool=FC_TOOL.get(m.get("tool"), m.get("tool")),
                          minutes=round(m.get("cut_time_min", 0) + m.get("rapid_time_min", 0), 2)) for m in su["ops"] if "error" not in m])
    return out


def t_mill(vol_cm3, tool, mode="hem"):
    """Minutes to remove vol_cm3 with an end mill: HEM at RDOC 10 %, ADOC 2 D, a feed per tooth in Helical's light-roughing range halved
    for the 3.3:1 stick-out (Haas / Helical long-reach rule) and capped by spindle speed, times EFF."""
    T = TOOLS[tool]
    d = T["d"]
    n = rpm(d, 1600)
    fz = {"T2": 0.0088 * IN * 0.6, "T3": 0.0058 * IN * 0.6, "T5": 0.0035 * IN}.get(tool, 0.002 * IN)
    f = n * T["flutes"] * fz
    if mode == "slot":
        mrr = d * min(d, T["stick_out"]) * n * T["flutes"] * (0.0053 * IN if d > 15 else 0.0035 * IN) * 0.5 / 1000.0
    else:
        mrr = 0.10 * d * min(2 * d, T["stick_out"] - 2) * f / 1000.0       # cm3/min
    return vol_cm3 / (mrr * EFF), dict(rpm=round(n), feed_mm_min=round(f), mrr_cm3_min=round(mrr, 1))


def t_face(area_cm2, depth_mm):
    T = TOOLS["T1"]
    n = rpm(T["d"], 3000)
    f = n * 4 * 0.004 * IN
    passes = max(1, math.ceil(depth_mm / 3.0))
    return passes * area_cm2 * 100 / (0.7 * T["d"] * f) / EFF + 1.0, dict(rpm=round(n), feed_mm_min=round(f), passes=passes)


def t_holes(n_holes, depth_mm, kinds):
    """Minutes for n holes: per hole ~5 s spot, depth / (rpm x ipr) drilling with pecks and ~4 s per rapid, tapping at 50 SFM; plus a
    4.2 s tool change per tool."""
    t = 0.0
    for k in kinds:
        if k == "spot":
            t += n_holes * 5.0
        elif k == "drill":
            t += n_holes * (depth_mm / (RPM_MAX * 0.008 * IN) * 60 * 1.6 + 4.0)
        elif k == "tap":
            t += n_holes * (2 * depth_mm / (rpm(5.0, 50) * 0.75) * 60 + 4.0)
        elif k == "ream":
            t += n_holes * (2 * depth_mm / (1000 * 0.15) * 60 + 4.0)
        t += 4.2
    return t / 60.0


def rot(face_up):
    """Rotation matrix (rows: machine x, y, z in model coordinates) that puts this model face on top, the spindle being vertical."""
    return {"+z": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "-z": [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
            "-y": [[1, 0, 0], [0, 0, 1], [0, -1, 0]], "+y": [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
            "+x": [[0, 1, 0], [0, 0, 1], [1, 0, 0]], "-x": [[0, -1, 0], [0, 0, 1], [-1, 0, 0]]}[face_up]


def a_axis_rotations():
    """Frame on the rotary: its bottom (-z) on a fixture plate bolted to the platter, model z along machine +X (away from the platter).
    At A = 0 the front (-y) faces up. Returns {A: rotation model -> machine (3 x 3 rows) and the face up}."""
    R0 = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]], float)      # machine X = model z, machine Y = -model x, machine Z = -model y
    out = {}
    for A, face in ((0, "front (-y)"), (90, "left (-x)"), (180, "back (+y)"), (270, "right (+x)")):
        a = math.radians(A)
        Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
        out[A] = dict(face_up=face, rotation_model_to_machine=np.round(Rx @ R0, 6).tolist())
    return out


# ---------------------------------------------------------------------------------------------------------------- model op volumes
def op_volumes():
    """Volume each CHAMBER_OPS cut and each joints.py hole set removes, applied in order to the blank (cm3), and the part volumes."""
    import joints as J
    import lpbf_low as M
    parts = M.build(include_tray=False, module="M50")
    res = {}
    for key, pre in (("frame", "Process chamber body"), ("floor", "Chamber floor plate")):
        d = M.CHAMBER_OPS[key]
        cur = d["blank"]
        vols = {}
        for oid, label, tool in d["ops"]:
            nxt = cur.cut(tool)
            vols[oid] = round((cur.Volume() - nxt.Volume()) / 1000.0, 2)
            cur = nxt
        jk = {}
        for k, tool in J.CUTS.get(pre, []):
            jk[k] = jk.get(k, 0) + 1
        part = [p for p in parts if p.name.startswith(pre)][0]
        res[key] = dict(blank_cm3=round(d["blank"].Volume() / 1000.0, 1), part_cm3=round(part.shape.Volume() / 1000.0, 1), op_cm3=vols,
                        joint_holes={k: v for k, v in jk.items()}, labels={oid: label for oid, label, _ in d["ops"]}, name=part.name)
    return res, M.FRAME, M.P


# ---------------------------------------------------------------------------------------------------------------- 4th axis
DIRS = CS.DIRS


def access(slug, b, mass_kg):
    tris = CS.read_stl(str(PARTS / f"{slug}.stl"))
    big = max(b[1] - b[0], b[3] - b[2], b[5] - b[4])
    pitch = 0.25 if big < 60 else (0.4 if big < 150 else (0.6 if big < 350 else 1.5))
    sbox = [b[0] - 2, b[1] + 2, b[2] - 2, b[3] + 2, b[4] - 2, b[5] + 2]
    lo, shape = CS.grid_for(tris, pitch, 4.0, sbox)
    vox, _ = CS.voxelize(tris, pitch, lo, shape)
    st = CS.stock_mask(lo, shape, pitch, sbox)
    skin = ndimage.binary_dilation(vox, structure=ndimage.generate_binary_structure(3, 1)) & ~vox & st
    reach = {}
    for d in DIRS:
        r, _ = CS.removable(CS.to_setup(vox, d), pitch, 3.175, None, None)
        reach[d] = CS.from_setup(r, d) & skin
    anyr = np.logical_or.reduce([reach[d] for d in DIRS])
    unreach = skin & ~anyr
    nskin = int(skin.sum())
    tol = max(0.002 * nskin, 3)

    def cover(target, dirs):
        covered = np.zeros_like(target)
        chosen = []
        while True:
            gains = {d: int((reach[d] & target & ~covered).sum()) for d in dirs if d not in chosen}
            if not gains:
                break
            d = max(gains, key=gains.get)
            if gains[d] < tol:
                break
            chosen.append(d)
            covered |= reach[d] & target
        return chosen

    three = cover(skin & anyr, DIRS)
    four = {}
    idx = np.argwhere(vox)
    xyz = lo + pitch * (idx + 0.5)
    c = np.array([(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2])
    for ax, k in (("x", 0), ("y", 1), ("z", 2)):
        perp = [d for d in DIRS if d[1] != ax]
        rot_cov = np.logical_or.reduce([reach[d] for d in perp])
        rest = skin & anyr & ~rot_cov
        extra = cover(rest, [f"+{ax}", f"-{ax}"])
        used = [d for d in perp if int((reach[d] & skin).sum()) >= tol]
        q = np.delete(xyz - c, k, axis=1)
        swing = float(np.sqrt((q ** 2).sum(axis=1)).max()) if len(q) else 0.0
        four[ax] = dict(setups=1 + len(extra), rotary_faces=used, extra_3axis=extra, swing_mm=round(swing, 1))
    best = min(four, key=lambda a: (four[a]["setups"], -len(four[a]["rotary_faces"]), four[a]["swing_mm"]))
    return dict(pitch=pitch, three_axis=three, n3=len(three), unreachable_pct=round(100 * float(unreach.sum()) / max(nskin, 1), 2),
                four_axis=four, best_axis=best, n4=four[best]["setups"], swing_mm=four[best]["swing_mm"],
                fits_hrt210=four[best]["swing_mm"] <= HRT210["centre_height_mm"] - 5, mass_ok=mass_kg <= HRT210["max_kg_unsupported"])


# special tools / 5-axis: what the reach analysis can't say on its own, from dfm.json and the model (machining.md)
SPECIAL = {
    "camera_viewport_adapter": "bore and boss on a compound angle (the line of sight from (75, -45) to the plate centre): two rotations, so a 4th axis "
                               "alone can't square it up; a sine plate + 4th axis, a 5-axis, or make the boss a turned part on a single-tilt seat",
    "build_plate": "bayonet lugs and the gripper groove are undercuts: turn and groove on the lathe",
    "heater_block": "bayonet socket undercut: internal grooving tool on the lathe + three milled entry slots",
    "piston_head": "seal grooves are radial: turned",
    "chamber_lid": "the cover-slide drawer slot is enclosed (machining.md): open it from the underside (then a 1/4 in. keyseat cutter for the ledges) "
                   "or sinker EDM; still drawn enclosed in lpbf_low section 7",
    "chamber_door": "half-dovetail O-ring groove: a dovetail cutter (special tool) or a plain groove with a moulded seal",
    "cover_slide_drawer": "half-dovetail O-ring groove on the front plate: dovetail cutter",
    "build_module_m50": "spigot's radial O-ring groove and the bore: turned after welding; honing outsourced",
    "module_m50_bottom_flange": "rod-gland grooves: internal grooving tool on the lathe",
    "optics_bridge_posts": "closed inside of the welded tube (expected)",
}


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    vols, FR, P = op_volumes()
    print(f"op volumes in {time.time() - t0:.0f} s: frame {vols['frame']['op_cm3']}\n floor {vols['floor']['op_cm3']}", flush=True)
    meta = json.load(open(PARTS / "parts.json"))
    dfm = {r["slug"]: r for r in json.loads((OUT / "dfm.json").read_text())["parts"]} if (OUT / "dfm.json").exists() else {}
    RA = a_axis_rotations()

    # ---------------- frame ----------------
    fv, pv = vols["frame"], vols["floor"]
    bl = FR["blank_in"]
    m_blank = bl[0] * bl[1] * bl[2] * IN ** 3 * 2.7e-6
    core_cm3 = fv["op_cm3"]["FR-02"]
    perim_core = 2 * (2 * (P["ix"] - FR["core_off"]) + 2 * (P["iy"] - FR["core_off"])) - (8 - 2 * math.pi) * (FR["r_in"] - FR["core_off"])
    wj_min = (perim_core / IN / 2.9, perim_core / IN / 0.50)
    ops_t = {}

    def op(oid, feature, refs, tool, minutes, strategy="", A=None, extra=None):
        T = TOOLS[tool]
        d = dict(id=oid, feature=feature, cuts=refs, tool=dict(id=tool, type=T["type"], d_mm=T["d"], stick_out_mm=T["stick_out"], holder=T["holder"]),
                 strategy=strategy, minutes=round(minutes, 1))
        if A is not None:
            d["A_deg"] = A
        if extra:
            d.update(extra)
        ops_t[oid] = minutes
        return d

    # chips per setup: the volumes from the model's op list
    v = fv["op_cm3"]
    face_area = 2 * (P["cx"] * 2) * (P["cy"] * 2) / 100.0
    blank_h = bl[2] * IN
    face_depth = (blank_h - (P["lid_z0"] + FR["skirt"])) / 2
    outer_cm3 = v["FR-01"]
    tf, ff = t_face(face_area / 2 * 1.3, face_depth)
    tr_out, fr_out = t_mill(outer_cm3 / 2, "T2")
    t34, f34 = t_mill((v["FR-03"] + v["FR-04"]) / 2, "T2")
    fin_in = 2 * (2 * P["ch_x"] + 2 * P["ch_y"]) / 2000.0 * 2          # two finishing levels per side at 2000 mm/min, two springs
    fin_out = 2 * (2 * 312 + 2 * 222) / 2000.0 * 2
    trb, _ = t_mill(v["FR-05"], "T2")
    gl_len = 2 * (2 * (P["ix"] + 3 + P["gland_w"] / 2) + 2 * (P["iy"] + 3 + P["gland_w"] / 2))
    t_gl = 4 * gl_len / (rpm(4.0, 1200) * 2 * 0.03)                     # 2 depth steps x 2 side passes, 4 mm end mill, 0.03 mm/tooth
    jh = fv["joint_holes"]
    frame_setups = [
        dict(id="F-S0", name="saw the blank; core out as one slug", machine="horizontal bandsaw; abrasive waterjet (ME Prototyping Lab EB 117 or MFGEN 101 CTB list one)",
             fixture="blank flat on the waterjet slats, weighted; a Ø12 start hole drilled first (drill press)", face_up="+z", rotation_model_to_machine=rot("+z"),
             ops=[op("F-S0-1", f"saw-cut blank {bl[0]:g} x {bl[1]:g} x {bl[2]:g} in. from 5-1/2 in. 6061-T651 plate (Metals Depot lists it cut to size)", [], "T6", 15.0,
                     "bandsaw; supplier can cut to size"),
                  op("F-S0-2", f"core out as one {2 * (P['ix'] - FR['core_off']):.0f} x {2 * (P['iy'] - FR['core_off']):.0f} slug ({core_cm3 / 1000:.2f} L, "
                     f"{core_cm3 * 2.7e-3:.0f} kg of reusable 6061), 3 mm inside the finished opening", ["FR-02"], "T6", (wj_min[0] + wj_min[1]) / 2,
                     f"waterjet: {perim_core / IN:.1f} in. of cut at 0.50-2.9 ipm (WARDJet 4 in. data scaled to 5.5 in.) = {wj_min[0]:.0f}-{wj_min[1]:.0f} min. "
                     "If the shop's waterjet can't take 5.5 in. (OMAX: machines 'optimized' for 1/4-3 in.): trepan on the mill instead, a 3/4 in. slot round "
                     "the core from each side in F-S1 and F-S2 (+~40 min), or a contour bandsaw with the blade threaded through the start hole and welded",
                     extra=dict(machine_note="off the mill"))]),
        dict(id="F-S1", name="bottom up: datum face, rebate, lower halves, floor-screw and dowel holes", machine="VF-4, 3-axis",
             fixture=("blank on four 1-1/2 in. riser blocks on the table, held by four low-profile edge clamps (McMaster 2172A42, BOM L3) on its x-end "
                      "faces below model z 63 (5 mm under this setup's deepest cut, z 58 from the bottom); no end tabs: holder_check.py found the face "
                      "mill and T2's outside passes running into toe clamps on 1 in. tabs (213 collisions, 2026-11-23); probe the blank for x, y, z zero"),
             face_up="-z", rotation_model_to_machine=rot("-z"),
             ops=[op("F-S1-1", "face the bottom (the skirt face, z -3.9)", ["FR-01"], "T1", tf, f"face mill, {ff['rpm']} rpm, {ff['feed_mm_min']} mm/min, {ff['passes']} passes",
                     extra=dict(note="FR-01 is shared: bottom face here, top face in F-S2, outer profile half and half")),
                  op("F-S1-2", "outer profile 312 x 222 R8, from the bottom up to mid-height (z 58.5)", ["FR-01"], "T2", tr_out + fin_out / 2,
                     f"HEM, RDOC 1.9 mm, ADOC 38 mm, {fr_out['rpm']} rpm, {fr_out['feed_mm_min']} mm/min; finish 0.25 mm; T2 66 mm out of an ER32 chuck"),
                  op("F-S1-3", "opening finished from the bottom to mid-height: 280 x 190, R10 corners", ["FR-04"], "T2", t34 + fin_in / 2,
                     "HEM off the 3 mm waterjet stock, then the finish in two passes (A5 has 38.1 mm of flutes); 66 mm stick-out (3.5:1)"),
                  op("F-S1-4", "rebate 8 x 3.9 round the bottom of the opening", ["FR-05"], "T2", trb + 2.0, "one level, two passes"),
                  op("F-S1-5", f"18 floor-screw holes M4 x 0.7 (Ø3.3 x 11, rigid tap 9) and 2 dowel holes Ø6 H7 x 10.4", ["J:floor", "J:floor_dowels"], "T7",
                     t_holes(18, 11, ["spot", "drill", "tap"]) + t_holes(2, 10.4, ["drill", "ream"]), "spot T6, drill T7, tap T10, dowels T13")]),
        dict(id="F-S2", name="top up: top face, upper halves, lid gland, lid inserts", machine="VF-4, 3-axis",
             fixture=("'Dummy floor' fixture plate (1 in. MIC-6, 312 x 222, flush with the frame; its own 18 Ø4.5 holes and 2 Ø6 pins matching the "
                      "frame's) on the table; the frame sits on its skirt face on the plate and is pulled down by the 18 M4 screws from below: "
                      "nothing on top or outside is in the way"),
             face_up="+z", rotation_model_to_machine=rot("+z"),
             ops=[op("F-S2-1", "face the top to height (123.9 mm overall)", ["FR-01"], "T1", tf, "face mill"),
                  op("F-S2-2", "outer profile from the top down to mid-height (overlap 1 mm with F-S1-2)", ["FR-01"], "T2", tr_out + fin_out / 2, "HEM + finish"),
                  op("F-S2-3", "opening finished from the top down to mid-height", ["FR-03"], "T2", t34 + fin_in / 2, "HEM + finish; the witness line at mid-height is "
                     "blended by the finishing springs (< 0.02 mm step with one tool and a probed z)"),
                  op("F-S2-4", "lid O-ring face gland (4.6 x 2.65, R4/R6 corners)", ["FR-06"], "T4", t_gl, "2 depth steps x 2 side passes; Ra <= 0.8 um floor"),
                  op("F-S2-5", "20 lid-screw insert holes M5 STI (Ø5.3 x 10.5, STI tap 7.5)", ["J:lid"], "T9", t_holes(20, 10.5, ["spot", "drill", "tap"]),
                     "spot T6, drill T9, STI tap T12 (freecad_cam.py drills these 6.0 then 5.0 mm, the model's two steps: use the 5.3 mm STI drill)")]),
        dict(id="F-S3", name="the four walls on the 4th axis (one clamping, four index angles)", machine="VF-4 with an HRT210-class rotary (A axis along machine X)",
             fixture=(f"the same dummy-floor plate (312 x 222, flush with the frame) bolted to the HRT210 platter, the frame on it with its bottom against the "
                      f"plate (2 pins + 18 M4 screws), so the frame's z axis is the A axis. The frame swings {math.hypot(P['cx'] - 8, P['cy'] - 8) + 8:.1f} mm "
                      "about it, more than the HRT210's 152.4 mm centre height: put the rotary on a 2-1/2 in. (63.5 mm) riser so A sits 215.9 mm above the "
                      "table (27 mm clear). No tailstock: the open top overhangs ~150 mm, 4.3 kg + the plate, inside the 38.6 kg unsupported rating. "
                      "Z to machine home before every index (the plate's corners swing 192 mm)"),
             face_up="A-indexed",
             alternatives=("A along the frame's x instead (it swings only 127 mm, so no riser), held by its side walls between a platter plate and the "
                           "tailstock: one clamping for top, bottom, front and back, but the two side walls then need their own setups, and the big sealing "
                           "faces are cut on the rotary rather than flat on the table. Same three setups; this plan keeps the faces that matter most on "
                           "the table."),
             a_axis=dict(axis_in_model="+z (frame bottom on the platter side)", centre_above_table_mm=152.4 + 63.5, riser_mm=63.5,
                         swing_radius_mm=round(math.hypot(P["cx"] - 8, P["cy"] - 8) + 8, 1), index=RA,
                         program=("freecad_cam.py jobs frame_C0, frame_C90, frame_C180, frame_C270 (one per index, each in the machine frame at that "
                                  "index, work zero on the A axis), joined into one Haas program with the A moves: gcode/frame_C_haas.nc "
                                  "(G53 G00 Z0. / M11 / G00 A<deg>. / M10 before each index)")),
             ops=[op("F-S3-1", "front: door opening 220 x 92, R6.5 corners, through the 16 mm wall", ["FR-07"], "T3", t_mill(v["FR-07"], "T3")[0] + 3.0,
                     "programmed: T3 adaptive through the wall (the window goes to chips); the door's sealing land round it is the as-faced front face", A=0),
                  op("F-S3-2", "left: recoater bore Ø18 through; through-beam M6 x 0.75 through with a Ø10.8 x 1.32 O-ring counterbore outside",
                     ["FR-10", "FR-13"], "T3", t_mill(v["FR-10"] / 2, "T3")[0] + t_mill(v["FR-13"] / 2, "T5")[0] + t_holes(1, 14.7, ["drill", "tap"]) + 1.0,
                     "programmed: Ø18 helix-milled with T3, the counterbore helix-milled with T5, the 5.2 mm tap drill through (T15); not programmed: "
                     "the M6 x 0.75 tap", A=90),
                  op("F-S3-3", "back: inlet slot 120 x 8 through, argon SAE-4 port, 7 inlet-plenum M4 STI holes and 2 Ø3 pin holes, 4 rail holes M4 "
                     "tapped THROUGH (the plugs' bonded seal washers seat on the as-faced wall)",
                     ["FR-08", "FR-09", "J:plenum_in", "J:plenum_in_pins", "J:rail"], "T5",
                     t_mill(v["FR-08"], "T5", "slot")[0] + t_mill(v["FR-09"], "T5")[0] + 1.0 + t_holes(7, 11.5, ["spot", "drill", "tap"])
                     + t_holes(2, 5.5, ["drill", "ream"]) + t_holes(4, 16, ["spot", "drill", "tap"]) + t_holes(1, 4.5, ["drill"]) + 2.0,
                     "programmed: the slot profiled with T5 in 3 mm steps; the port helix-milled to its 25/64 in. tap drill with T5 and its Ø4 passage "
                     "drilled 3.3 mm (T7); inserts 4.2 mm (T8); pins 2.9 mm (T17); rail holes 3.3 mm through (T7); not programmed: spot drills, "
                     "the SAE port tool T14 (spot face, cone, 7/16-20 thread), the STI taps T11, the M4 tap T10, the 3 mm reamer", A=180),
                  op("F-S3-4", "right: KF-25 bore Ø25.4, recoater bore Ø18, through-beam as on the left, O2 SAE-4 port, 4 vacuum-adapter M5 STI, "
                     "4 bearing-cap M4 STI, 4 Ø3 pin holes",
                     ["FR-10", "FR-11", "FR-12", "FR-13", "J:vac_port", "J:vac_port_pins", "J:bearing_cap", "J:bearing_cap_pins"], "T3",
                     t_mill(v["FR-11"], "T3")[0] + t_mill(v["FR-10"] / 2, "T3")[0] + t_mill(v["FR-13"] / 2, "T5")[0] + t_holes(1, 14.7, ["drill", "tap"])
                     + t_mill(v["FR-12"], "T5")[0] + 1.0 + t_holes(1, 4.5, ["drill"]) + t_holes(4, 12.5, ["spot", "drill", "tap"])
                     + t_holes(4, 7.5, ["spot", "drill", "tap"]) + t_holes(4, 5.5, ["drill", "ream"]) + 2.0,
                     "programmed: the KF-25 and Ø18 bores helix-milled with T3; the counterbore and the O2 port (to its tap drill) with T5; drills 5.3 mm "
                     "(T9: M5 STI), 5.2 mm (T15: the through-beam), 4.2 mm (T8: M4 STI), 3.3 mm (T7: the port's passage), 2.9 mm (T17: pins); not programmed: "
                     "spot drills, the taps and STI taps, the port tool T14, the reamer", A=270)]),
    ]
    # the CAM blank's ring outside the 312 x 222 R8 outline, 8 mm tall: what P-S1-2b (z -4..-12) and P-S2-2 (z -12..-20) each
    # remove (freecad_cam.FLOOR_BLANK, 317.5 x 228.6: no end tabs since the edge clamps)
    import freecad_cam as FCAM
    ring8_cm3 = (FCAM.FLOOR_BLANK[0] * FCAM.FLOOR_BLANK[1] - (312 * 222 - (4 - math.pi) * 8 ** 2)) * 8 / 1000
    floor_setups = [
        dict(id="P-S0", name="saw the blank", machine="bandsaw", fixture="-", face_up="+z", rotation_model_to_machine=rot("+z"),
             ops=[op("P-S0-1", f"saw {FR['floor_blank_in'][0]:g} x {FR['floor_blank_in'][1]:g} in. from 1 in. 6061-T651 (McMaster 89155K165, 12 x 24 in., $267.02)",
                     [], "T6", 10.0, "")]),
        dict(id="P-S1", name="top up: datum face, pad step, gland, port, slots, dowel and clearance holes", machine="VF-4, 3-axis",
             fixture=("blank on 1/2 x 1-1/2 in. parallels along x (kept clear of the port and the slots), held by four low-profile edge clamps (L3) on its "
                      "x-end faces under model z -15, 3 mm below this setup's outside passes; no end tabs (holder_check.py, 2026-11-23: the face mill ran into "
                      "toe clamps on tabs and T2's outside passes through the tab roots). Check that the clamps, gripping the bottom 7.7 mm of the 1 in. "
                      "blank, hold against the adaptive cuts"),
             face_up="+z", rotation_model_to_machine=rot("+z"),
             ops=[op("P-S1-1", "face the top (the pad face, z 0)", ["FP-01"], "T1", t_face(312 * 222 / 100 * 1.3, 2.7)[0], "face mill"),
                  op("P-S1-2", "step the edge band down 4 mm, leaving the 4 mm pad (295.5 x 205.5, R17.75)", ["FP-02"], "T2", t_mill(pv["op_cm3"]["FP-02"], "T2")[0] + 3.0,
                     "HEM, one level"),
                  op("P-S1-2b", "outer profile 312 x 222 R8 from the band (z -4) down to z -12 only; P-S2 cuts the rest", ["FP-01"], "T2",
                     t_mill(ring8_cm3, "T2")[0] + 1.0, "HEM, one level; the edge clamps sit 3 mm below"),
                  op("P-S1-3", "floor O-ring face gland (4.6 x 2.65, 1.5 mm outside the walls)", ["FP-03"], "T4", t_gl * 0.95, "as the lid gland; Ra <= 0.8 um"),
                  op("P-S1-4", "module port Ø96 H7 through", ["FP-04"], "T2", t_mill(pv["op_cm3"]["FP-04"], "T2")[0] + 4.0,
                     "helical trepan through with T2 at radius 48 - D/2, 0.5 mm past the blank, so the slug drops here (programmed); finish to H7 with a "
                     "probed bore check (or bore with a boring head)"),
                  op("P-S1-5", "outlet slot 124 x 8 and overflow slot 20 x 104 through", ["FP-05", "FP-06"], "T5",
                     t_mill(pv["op_cm3"]["FP-05"] + pv["op_cm3"]["FP-06"], "T5", "slot")[0] + 3.0,
                     "1/4 in. end mill round each slot's outline, 0.5 mm past the blank (programmed): the 20 x 104 slot's 7 x 91 core drops, so hold it"),
                  op("P-S1-6", "2 dowel holes Ø6 H7 x 10.5 in the band; 18 clearance holes Ø4.5 through the band", ["J:floor_dowels", "J:floor"], "T13",
                     t_holes(2, 10.5, ["drill", "ream"]) + t_holes(18, 16, ["spot", "drill"]), "")]),
        dict(id="P-S2", name="bottom up: face to thickness, outer profile, U-notches, blind holes for every under-floor mount", machine="VF-4, 3-axis",
             fixture=("the dummy-floor plate (L7) as a fixture plate, with 2 Ø6 pins in the floor plate's dowel holes; an expanding ID clamp (L10, about Ø94, "
                      "shop-made) in the Ø96 port, its top 5 mm under the faced bottom, pulls the plate down. The outer profile and the whole underside are "
                      "free (setup_plan's earlier centre stud and Ø104 washer sat on the face this setup faces: holder_check.py, 2026-11-23)"),
             face_up="-z", rotation_model_to_machine=rot("-z"),
             ops=[op("P-S2-1", "face the bottom to 20.0 mm", ["FP-01"], "T1", t_face(312 * 222 / 100 * 1.3, 2.7)[0], "face mill"),
                  op("P-S2-2", "outer profile 312 x 222 R8 below z -12, the ring of blank outside it, and the 18 U-notches 8 wide x 8 deep, in one adaptive",
                     ["FP-01", "J:floor"], "T5", t_mill(ring8_cm3, "T5")[0] + 18 * 0.4 + 3.0,
                     "1/4 in. end mill adaptive outside the outline, 4 mm steps (programmed: 14.2 min in the G-code)"),
                  op("P-S2-4", "module-screw M6 STI and dowel / diamond-pin holes; outlet-plenum, funnel and Z-flange inserts (M4/M5 STI); leg inserts (M6 STI)",
                     ["FP-07", "J:module_flange", "J:plenum_out", "J:funnel", "J:zmount", "J:legs"], "T8",
                     t_holes(2, 13.5, ["spot", "drill", "tap"]) + t_holes(10, 7.5, ["spot", "drill", "tap"]) + t_holes(4, 9, ["spot", "drill", "tap"]) + t_holes(4, 11, ["spot", "drill", "tap"]),
                     "spot T6; STI drills T8/T9/6.3 mm; STI taps")]),
    ]
    prog = program_info()
    for su_, names in (("F-S1", ["frame_B"]), ("F-S2", ["frame_A"]), ("F-S3", ["frame_C0", "frame_C90", "frame_C180", "frame_C270"]),
                       ("P-S1", ["floor_A"]), ("P-S2", ["floor_B"])):
        rec = next(x for x in frame_setups + floor_setups if x["id"] == su_)
        if all(n in prog for n in names):
            rec["program"] = dict(freecad_jobs=names, gcode=[f"gcode/{n}.ngc" for n in names] + (["gcode/frame_C_haas.nc"] if su_ == "F-S3" else []),
                                  recount_min=round(sum(prog[n]["recount_min"] for n in names), 2),
                                  camotics_min=(round(sum(prog[n]["camotics_min"] for n in names), 2)
                                                if all(prog[n]["camotics_min"] is not None for n in names) else None),
                                  tool_changes=sum(prog[n]["tool_changes"] for n in names),
                                  rapids_through_stock=(sum(prog[n]["rapids_through_stock"] for n in names)
                                                        if all(prog[n]["rapids_through_stock"] is not None for n in names) else None),
                                  ops={n: prog[n]["ops"] for n in names},
                                  note="cutting time in the posted G-code (length / F, rapids at 25.4 m/min) and CAMotics' own count; no "
                                       "acceleration, tool changes or A indexing; taps, STI taps, reamers and port tools are not programmed")
    run_f = sum(o["minutes"] for s in frame_setups for o in s["ops"] if not s["id"].endswith("S0"))
    run_p = sum(o["minutes"] for s in floor_setups for o in s["ops"] if not s["id"].endswith("S0"))
    plan = dict(
        units="mm, minutes; model frame of cad/lpbf_low.py (origin at the floor's top centre, +y to the back)",
        generated_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        how_to_animate=("Start from CHAMBER_OPS[part]['blank']; in each setup turn the part by rotation_model_to_machine (rows are machine x, y, z in model "
                        "coordinates; for the 4th-axis setup use index[A]), and for each op cut, in order, the solids it lists: 'FR-xx'/'FP-xx' are "
                        "lpbf_low.CHAMBER_OPS[...]['ops'] entries, 'J:<key>' the tools in joints.CUTS['Process chamber body' / 'Chamber floor plate'] "
                        "with that key. The spindle stays vertical (machine +z). FR-01 / FP-01 is the outside trim and both faces, shared between the "
                        "two flat setups (bottom face and lower half of the profile first, then the rest)."),
        machines=dict(mill=VF4, rotary=HRT210), feeds=FEEDS, tools=TOOLS, efficiency_note=f"roughing rates x {EFF} for a first part (leads, air, ramps)",
        frame=dict(part=fv["name"], material="6061-T651",
                   blank=dict(size_in=bl, size_mm=[round(x * IN, 1) for x in bl], mass_kg=round(m_blank, 1),
                              source="5-1/2 in. 6061-T651 plate cut to size (Metals Depot lists 5, 5-1/2 and 6 in. plate; McMaster's rolled plate stops at 4 in.)",
                              why_5_5=("5 in. plate is +/-0.130 in. (+/-3.3 mm) thick per OnlineMetals' table, so it can arrive thinner than the 123.9 mm frame"),
                              end_tabs=("none since 2026-11-23: F-S1 holds the blank with edge clamps on its x-end faces (toe clamps on 1 in. end tabs "
                                        "were in the face mill's and T2's way), so the 15 in. length can be cut to 13 in."),
                              cam_blank_mm=("freecad_cam.py and CAMotics cut a 317.5 x 228.6 x 127 box (12.5 x 9 x 5 in.), the frame plus 2.75-3.3 mm a "
                                            "side and 1.55 mm a face; from 5-1/2 in. plate the two face ops take 7.9 mm a face, 2-4 more "
                                            "passes each, roughly 4-7 min a face (not programmed)")),
                   core=dict(volume_cm3=core_cm3, mass_kg=round(core_cm3 * 2.7e-3, 1), route="waterjet (default) / trepan on the mill / contour bandsaw",
                             waterjet_min=[round(x) for x in wj_min]),
                   model_volumes_cm3=fv, setups=frame_setups, run_minutes_on_mill=round(run_f), part_handling="the frame weighs 4.3 kg finished; the blank 39 kg"),
        floor=dict(part=pv["name"], material="6061-T651",
                   blank=dict(size_in=FR["floor_blank_in"], size_mm=[round(x * IN, 1) for x in FR["floor_blank_in"]],
                              end_tabs=("none since 2026-11-23: P-S1 holds the blank with edge clamps on its x-end faces, so 12.5 x 9 in. "
                                        "will do (freecad_cam.py and CAMotics cut a 317.5 x 228.6 x 25.4 box)"),
                              source="1 in. 6061-T651 oversized plate 12 x 24 in., McMaster 89155K165, $267.02 (fetched 22:33-22:37 UTC)"),
                   model_volumes_cm3=pv, setups=floor_setups, run_minutes_on_mill=round(run_p)),
    )
    # ---------------- every machined part ----------------
    rows = {}
    t1 = time.time()
    for p in meta["parts"]:
        if p["kind"] != "stock":
            continue
        mass = p["volume_mm3"] * {"al6061": 2.7e-6, "mic6": 2.65e-6, "ss316l": 8.0e-6, "steel": 7.85e-6, "macor": 2.52e-6}.get(p["mat"], 2.7e-6)
        try:
            a = access(p["slug"], p["bbox"], mass)
        except Exception as e:  # noqa: BLE001
            print(p["slug"], "failed", e)
            continue
        sp = next((v for k, v in SPECIAL.items() if p["slug"].startswith(k)), "")
        dd = dfm.get(p["slug"], {})
        rows[p["slug"]] = dict(name=p["name"], mat=p["mat"], mass_kg=round(mass, 2), bbox_mm=[round(p["bbox"][1] - p["bbox"][0], 1), round(p["bbox"][3] - p["bbox"][2], 1),
                                                                                                round(p["bbox"][5] - p["bbox"][4], 1)],
                               machine=dd.get("machine"), stock=dd.get("stock"), **a, special=sp,
                               summary=(f"3-axis: {a['n3']} setups ({', '.join(a['three_axis'])}); 4th axis along {a['best_axis']}: {a['n4']} "
                                        f"({'one clamping for ' + ', '.join(a['four_axis'][a['best_axis']]['rotary_faces']) if a['four_axis'][a['best_axis']]['rotary_faces'] else '-'}"
                                        f"{' + ' + ', '.join(a['four_axis'][a['best_axis']]['extra_3axis']) if a['four_axis'][a['best_axis']]['extra_3axis'] else ''})"))
        print(f"{p['slug'][:48]:48s} 3ax {a['n3']} {a['three_axis']}  4ax[{a['best_axis']}] {a['n4']}  swing {a['swing_mm']:.0f}  unreach {a['unreachable_pct']} %", flush=True)
    plan["parts"] = rows
    n3 = sum(r["n3"] for r in rows.values())
    for r in rows.values():           # the rotary only counts where the part swings inside the HRT210 (152.4 mm centre height, 5 mm clear) and it saves a setup
        r["n4_used"] = r["n4"] if (r["fits_hrt210"] and r["n4"] < r["n3"]) else r["n3"]
    n4 = sum(r["n4_used"] for r in rows.values())
    plan["totals"] = dict(parts=len(rows), setups_3axis=n3, setups_with_4th_axis=n4,
                          parts_where_the_rotary_saves_setups={k: [r["n3"], r["n4_used"]] for k, r in rows.items() if r["n4_used"] < r["n3"]},
                          parts_needing_special_tool_or_5axis=[k for k, r in rows.items() if r["special"]],
                          note="per part, the 4th-axis count is used only where it is lower; a part held on a rotary still needs its fixture made")
    (OUT / "setup_plan.json").write_text(json.dumps(plan, indent=1, default=float))
    print(f"setups: 3-axis {n3}, with a 4th axis {n4}; frame {run_f:.0f} min on the mill, floor {run_p:.0f} min; {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
