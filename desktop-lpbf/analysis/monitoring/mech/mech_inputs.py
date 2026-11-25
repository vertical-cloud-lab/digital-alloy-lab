"""Inputs for the monitoring mechanics checks (issue #260, PR 281), read at run time from the model and the other monitoring files.

Where a number isn't in the repo (a bought part's mass or size, a material constant), it is in ASSUMED below with its source,
or marked "assumed" when there was none to read. Change those here, not in the checks.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                                   # desktop-lpbf
REPO = ROOT.parent
sys.path.insert(0, str(ROOT / "cad"))
import lpbf_low as LL  # noqa: E402  (imports CadQuery, builds nothing)
import module_params as MP  # noqa: E402,F401  (re-exported: mech_monitoring reads MI.MP)
import monitoring_spec as MS  # noqa: E402

OUT_DIR = ROOT / "analysis" / "out"
P = LL.P
MAT = LL.MAT


def jload(rel):
    p = OUT_DIR / rel
    return json.loads(p.read_text()) if p.exists() else None


FRAME_FEATURES = jload("monitoring/fab/frame_features.json")   # the ports as programmed (analysis/monitoring/fab/frame_features.py)
THERMAL = jload("thermal/thermal.json")                         # module thermal FEA (analysis/thermal_module.py)
FEA = jload("fea/fea.json")                                     # bridge modes (case 6), window (case 7)
PLUME_FOULING = jload("monitoring/plume/fouling.json")

# ------------------------------------------------------------------------------------------------ materials (SI-ish: MPa, mm)
GLASS = {
    "fused silica": dict(E=72_700.0, nu=0.16, alpha=0.55e-6, k=1.38, MR=52.4,
                         src="Corning 7980: E 72.7 GPa, nu 0.16, CTE 0.52-0.57 ppm/K, k 1.38 W/mK; 52.4 MPa abraded modulus of "
                             "rupture (the value fea.py case 7 uses for the laser window)"),
    "N-BK7": dict(E=82_000.0, nu=0.206, alpha=7.1e-6, k=1.114, MR=None,
                  src="SCHOTT N-BK7 datasheet: E 82 GPa, nu 0.206, CTE 7.1 ppm/K (-30..70 C), k 1.114 W/mK. SCHOTT publishes no "
                      "modulus of rupture; the check gives the strength a borosilicate window would need instead"),
}
SF_WINDOW = 4.0          # safety factor on the modulus of rupture (the directive; fea.py's laser window uses 4-6)
K_SS = 1.25              # sigma_max = K p a^2 / t^2 for a disc simply supported at radius a (Roark: 3(3+nu)/8 = 1.19-1.24;
                         # 1.25 is the rounded-up value fea.py case 7 uses); clamped edge: 0.75
P_ATM = 0.101325         # MPa
P_OVER = 0.002           # MPa (+20 mbar, the purge's set point; fea.py case 1b)

FKM = dict(shore_A=75, E_c_MPa=(6.0, 12.0), squeeze_flat=(0.15, 0.35), y_seat_MPa=1.4, m_factor=1.0,
           src="flat elastomer gasket: ASME BPVC VIII-1 Appendix 2 Table 2-5.1 gives y = 200 psi (1.4 MPa), m = 1.00 for "
               "elastomer >= 75A; 15-35 % compression is the usual working range for flat FKM vacuum gaskets (assumed); "
               "compression modulus 6-12 MPa for a thin, wide 75A strip (shape factor > 3; assumed from Gent's E_c = E(1 + 2kS^2))")
SHEET_IN_BOM_MM = 25.4 / 32                         # monitoring-bom.csv M0-06: "FKM sheet 1/32 in."
SHEET_LAYER_CAM_MM = 1.0                            # lpbf_low.py: the layer camera's window gasket, 1.0 mm squeezed to 0.75
GASKET_INSTALLED_MM = 0.75                          # frame_features.py GASKET (squeezed thickness the seat depth assumes)
WINDOW_T_TOL_MM = 0.2    # +/- thickness tolerance of Edmund's catalogue windows (36-983, 25-245): "+/-0.20 mm" on their pages (to check)

SCREW_M4 = dict(d=4.0, At=8.78, Sp_A4_70=450.0, preload_frac=0.75, K_nut=0.2,
                src="M4 x 0.7: tensile stress area 8.78 mm2 (ISO 898-1); A4-70 stainless proof stress 450 MPa (ISO 3506-1); "
                    "preload 75 % of proof (Shigley, non-permanent joints); nut factor K 0.2")

SS316 = dict(E=193_000.0, rho=7_990.0, nu=0.27, k=16.3, alpha=16.0e-6, eps=(0.3, 0.6),
             src="316 annealed (ASM / AK Steel 316 datasheet): E 193 GPa, rho 7990 kg/m3, k 16.3 W/mK at 100 C; emissivity "
                 "0.3 (lightly oxidised) to 0.6 (assumed range)")
AL6061 = dict(E=MAT["al6061"]["E"], rho=MAT["al6061"]["rho"], alpha=23.6e-6, k=167.0)
STEEL_303 = dict(alpha=17.3e-6, E=193_000.0, src="Thorlabs ER rods: 303 stainless (product page); CTE 17.3 ppm/K")
F_THETA_MM = 160.0       # Thorlabs FTH160-1064 (lpbf_low.py's f-theta part; monitoring_spec COAX: f_tube = 160 x px/8)


def _tube_lens_f():
    import csv
    import re
    with open(ROOT / "monitoring" / "optics-parts.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["id"] == "MO12":
                return float(re.search(r"AC254-(\d+)", r["part_number"]).group(1))
    return 75.0


TUBE_LENS_F_MM = _tube_lens_f()                     # the coaxial camera's tube lens (optics-parts.csv MO12: AC254-075-B)
ARGON_K = 0.0177                                   # W/mK at 300 K (NIST WebBook / Younglove), 0.024 at 450 K
AIR_K = 0.026

AE = dict(
    f_band_kHz=(100.0, 500.0),
    attenuation_316_dB_per_m=(0.1, 0.5),
    attenuation_src="bulk attenuation in austenitic steel scales ~f^4 (grain scattering) below 1 MHz; 0.1-0.5 dB/m at 100-500 kHz is "
                    "an extrapolation from 1-5 MHz values (assumed); a thin rod adds no geometric spreading",
    waveguide_d_mm=3.0,                       # monitoring_spec AE option 2 (Edison: 1.5-2.0 mm; the BOM line M4-06 is Ø2)
    waveguide_d_alt_mm=2.0,
    preload_N=(10.0, 20.0),                   # Edison r8-ae-waveguide: 9-22 N published, 10-20 N suggested
    sensor_t_max_C=60.0,                      # monitoring_spec AE.sensor_room_temp (preamp <= 65 C)
    rod_end_t_max_C=75.0,                     # monitoring.md §5.4 ("<= ~75 C in round 5's thermal runs")
    interface_dB=dict(greased=(1.0, 3.0), dry_metal=(3.0, 10.0), graphite_foil=(3.0, 6.0), macor_area=None),
    interface_src="Edison r8-ae-waveguide (answer.md §2.3, §3): couplant < 5 dB (Xu 2024); dry metal 3-10+ dB, graphite foil 3-6 dB; "
                  "a 1.59 x 306 mm guide lost ~13 dB vs direct mounting (Zelenyak 2015); 5-15 dB expected for the suggested design",
    Z_MRayl={"6061": 17.3, "316": 45.4, "Macor": 14.2, "graphite foil": 2.5, "grease": 1.5},
    Z_src="acoustic impedances: Al 17.3, 316 45.4 MRayl (Onda tables); Macor 14.2 from E 66.9 GPa, nu 0.29, rho 2.52 (Corning datasheet); "
          "graphite foil ~1-4 (Edison: 3-5; density 1.0-1.1 g/cm3, assumed); silicone grease ~1.5",
)

# ------------------------------------------------------------------------------------------------ bought parts not in the repo
ASSUMED = {
    "Kowa LM50JC10M": dict(d=36.0, L=51.0, kg=0.15, src="assumed (Kowa JC10M 2/3 in. family; check the datasheet)"),
    "IMX296 board + housing": dict(kg=0.06, src="assumed (InnoMaker board ~10 g in a 40 x 40 x 30 printed or Al housing)"),
    "Chronos 2.1-HD": dict(kg=MS.SIDE_CAMERA["mass_kg"], dims=MS.SIDE_CAMERA["body_mm"],
                           src="monitoring_spec SIDE_CAMERA (1.0 kg 'to check' against Kron's datasheet)"),
    # Thorlabs cage parts: masses estimated from the part's size in aluminium (anodised) or steel, not weighed
    "C4W cube + B4C base + FFM1": dict(kg=0.13, src="estimate: 41.3 mm Al cube bored Ø25 four ways (~0.09 kg) + base + mount"),
    "PDA36A2": dict(kg=0.12, src="estimate: Al housing ~70 x 64 x 23 mm with board"),
    "CP33 plate": dict(kg=0.02, src="estimate: 41 x 41 x 8 mm Al plate, bored"),
    "ER rod per 100 mm": dict(kg=0.022, src="Ø6 mm 303 stainless: pi 3^2 x 100 x 7.9e-6"),
    "SM1L10 + optic": dict(kg=0.025, src="estimate: Ø30.5 x 25 mm Al tube + Ø25 optic"),
    "galvo-side stand-off post": dict(kg=0.05, src="estimate: Ø12.7 x 35 mm post + clamp"),
}


def lp_camera_envelope(centre, standoff=None):
    """Steep lid camera on the LP sight line: lens front `standoff` mm (default: the side camera's 15 mm in monitoring_spec)
    outside the port centre, then the lens and the camera body. Returns the numbers bridge_modal.py and the checks use."""
    c = [float(x) for x in centre]
    d0 = math.dist(c, MS.TARGET)
    u = [(q - t) / d0 for q, t in zip(c, MS.TARGET)]            # outward along the sight line
    lens = ASSUMED["Kowa LM50JC10M"]
    body = MS.LID_CAMERA["body_mm"]
    s_front = d0 + (MS.SIDE_CAMERA["standoff_mm"] if standoff is None else standoff)
    length = lens["L"] + body[2]
    radius = max(lens["d"] / 2, math.hypot(body[0], body[1]) / 2)
    front = [t + s_front * k for t, k in zip(MS.TARGET, u)]
    back = [t + (s_front + length) * k for t, k in zip(MS.TARGET, u)]
    return dict(axis_out=u, front_xyz=front, back_xyz=back, length_mm=length, radius_mm=radius, wd_mm=s_front,
                src="lens front at the port centre + 15 mm; Kowa LM50JC10M (assumed Ø36 x 51) + IMX296 housing 40 x 40 x 30 (spec)")


def module_temps():
    """Rod-end and head temperatures across the steady module cases (thermal.json)."""
    out = {}
    if not THERMAL:
        return out
    for k, v in THERMAL["steady"].items():
        out[k] = dict(T_plate=v.get("T_plate_centre"), T_block=v.get("T_block_max"), T_head=v.get("T_head_mean"),
                      T_rod_gland=v.get("T_rod_at_gland"), T_rod_end=v.get("T_rod_end"), T_ch=v["case"].get("T_ch"))
    return out
