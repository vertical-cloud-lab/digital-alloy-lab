"""Vendor data for the monitoring optics (issue #260): every spec and list price the other scripts use, with its source and
fetch time, and the writer for monitoring/optics-parts.csv.

Vendor pages were read through the lab's tunnel on BYU's network on 2026-11-25. Raw pages and data files stay in /tmp (their
sha256 are listed in monitoring/optics.md, Sources); only the numbers used are copied here.

    python parts.py            (writes desktop-lpbf/monitoring/optics-parts.csv)
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

# Thorlabs FTH100-1064 total transmission (same family, coating and element count as the FTH160-1064, 3 elements + N-BK7
# window; Thorlabs publishes the curve only for the FTH100-1064 and FTH160-1064-M39). Raw data fth100-1064.xlsx from
# https://www.thorlabs.com/f-theta-scan-lenses (Graphs tab), fetched 2026-11-25T06:41Z, sha256 96a3a80c9e465955...
FTHETA_T = [(400, 0.245), (425, 0.565), (450, 0.847), (475, 0.899), (500, 0.919), (525, 0.947), (550, 0.955), (575, 0.948),
            (600, 0.945), (625, 0.954), (650, 0.970), (675, 0.979), (700, 0.976), (725, 0.959), (750, 0.933), (775, 0.908),
            (800, 0.886), (825, 0.872), (850, 0.869), (875, 0.876), (900, 0.885), (925, 0.898), (950, 0.914), (975, 0.933),
            (1000, 0.951), (1025, 0.968), (1050, 0.980), (1075, 0.985), (1100, 0.983), (1125, 0.975), (1150, 0.961),
            (1175, 0.942), (1200, 0.920), (1225, 0.895), (1250, 0.870), (1275, 0.843), (1300, 0.818), (1325, 0.793),
            (1350, 0.769), (1375, 0.747), (1400, 0.722), (1425, 0.692), (1450, 0.674), (1475, 0.663), (1500, 0.651),
            (1525, 0.640), (1550, 0.628), (1575, 0.618), (1600, 0.608), (1625, 0.599), (1650, 0.591), (1675, 0.582),
            (1700, 0.576), (1725, 0.570), (1750, 0.564), (1775, 0.558), (1800, 0.550)]
FTHETA_T_SRC = "Thorlabs fth100-1064.xlsx (f-theta-scan-lenses, Graphs tab), 2026-11-25T06:41Z"

# ------------------------------------------------------------------------------------------------ branch optics (radiometry.py)
# Thorlabs raw data (Graphs tabs), unpolarised, 45 deg for the dichroics; fetched 2026-11-25T06:44-07:02Z (sha256 in optics.md):
# dmsp1000.xlsx e99b8b93..., dmlp805.xlsx 889d4d75..., fesh1000.xlsx 142ff897..., nf1064-44_data.xlsx 104fccae...,
# pda36a2_responsivity.xlsx d687d7a8..., pda20cs2_responsivity.xlsx 8d346bdd...
DMSP1000_T = [(500, 0.9377), (525, 0.9666), (550, 0.978), (575, 0.9575), (600, 0.9421), (625, 0.9683), (650, 0.9208), (675, 0.9636),
              (700, 0.9732), (725, 0.9678), (750, 0.9753), (775, 0.9388), (800, 0.9709), (825, 0.9676), (850, 0.9612), (875, 0.9731),
              (900, 0.9792), (925, 0.9654), (950, 0.9632), (975, 0.9434), (1000, 0.6297), (1025, 0.009119), (1050, 0.007768),
              (1070, 0.0006288), (1075, 0.0004791), (1100, 0.006143), (1150, 0.002801), (1200, 6.19e-05), (1300, 0.003094),
              (1400, 0.04635), (1500, 0.007092), (1550, 0.005778), (1600, 0.009831), (1625, 0.01728), (1650, 0.07002), (1675, 0.1219),
              (1700, 0.2733), (1725, 0.376), (1750, 0.42)]
DMLP805_R = [(500, 0.9797), (600, 0.9904), (650, 0.987), (700, 0.9908), (750, 0.9894), (775, 0.9888), (800, 0.5898), (825, 0.04126),
             (850, 0.02647), (900, 0.01426), (950, 0.01762), (1000, 0.01554), (1070, 0.01387), (1100, 0.01438)]
DMLP805_T = [(500, 0.001187), (700, 0.00146), (775, 0.002778), (800, 0.4021), (825, 0.9549), (850, 0.9698), (875, 0.977), (900, 0.982),
             (950, 0.9786), (1000, 0.9813), (1070, 0.9848), (1100, 0.9843), (1300, 0.9324), (1550, 0.103), (1650, 0.08851), (1700, 0.00888)]
FESH1000_OD = [(500, 0.006767), (600, 0.007066), (700, 0.005862), (800, 0.00294), (900, 0.002765), (950, 0.003244), (975, 0.003307),
               (1000, 0.3138), (1025, 3.635), (1050, 5.527), (1064, 5.517), (1070, 5.984), (1075, 5.429), (1100, 5.529), (1300, 7.311),
               (1550, 4.539), (1600, 1.341), (1650, 0.608), (1700, 0.1694)]
# dmsp950.xlsx 06a265c8... (45 deg, unpolarised) and fesh0950_transmission.xlsx 15be81ef... (0 deg)
DMSP950_T = [(500, 0.9624), (600, 0.9601), (700, 0.9608), (800, 0.9713), (850, 0.9712), (900, 0.9606), (910, 0.9615), (920, 0.9577),
             (930, 0.9085), (940, 0.5788), (950, 0.2565), (960, 0.06334), (970, 0.02313), (980, 0.03065), (1000, 0.01013),
             (1070, 0.02087), (1100, 0.0121)]
DMSP950_R = [(850, 0.02752), (900, 0.03785), (920, 0.04067), (930, 0.08899), (940, 0.4175), (950, 0.7417), (960, 0.9344),
             (970, 0.9741), (980, 0.9653), (990, 0.9744), (1000, 0.9871), (1070, 0.9739), (1100, 0.9831)]
FESH0950_OD = [(850, 0.002266), (900, 0.006687), (920, 0.005463), (930, 0.006446), (940, 0.007964), (950, 0.5297), (960, 5.053),
               (970, 5.336), (1000, 5.364), (1070, 5.105), (1100, 5.256)]
# NF1064-44 also blocks 520-720 nm (OD 4.2-4.6 there; its data file): it must not sit in front of a 700 nm channel.
NF1064_OD = [(500, 2.484), (525, 4.3), (600, 4.551), (650, 4.228), (700, 4.308), (725, 2.118), (750, 0.5859), (775, 0.07627),
             (800, 0.003253), (900, 0.02693), (1000, 0.003617), (1025, 0.02069), (1050, 3.646), (1064, 6.103), (1070, 6.049),
             (1075, 5.854), (1080, 3.391), (1100, 0.003693), (1300, 0.001349), (1550, 0.06925)]
# Thorlabs BSW26 (alternative cube2 insert): UVFS plate, 50:50 +/- 12 % at 45 deg, 350-1100 nm, $363.52 (07:02Z)
SPLITTER = dict(R=0.5, T=0.5, part="Thorlabs BSW26 50:50 plate (alternative layout only)")
# Thorlabs FBH hard-coated bandpass filters (10 and 40 nm): T > 90 % at the CWL, OD > 5 from 200 to 1200 nm (covers 1070 nm),
# $193.82; FBH1550-12 / FBH1600-12 / FBH1650-12 $202.63, same blocking (family spec tables, 06:48-06:49Z). FB series discontinued.
FILTERS = {"700/40": 0.9, "700/10": 0.9, "900/40": 0.9, "850/40": 0.9, "850/10": 0.9, "950/10": 0.9, "1550/12": 0.9, "LP1250": 0.99}
FILTER_OD_1070 = 5.0                           # FBH out-of-band blocking (spec: OD > 5)
# InGaAs pick-off right after cube1 (option a): a 45 deg short-pass dichroic that passes < 1000 nm on to the Si branch and
# reflects 1200-1750 nm to the InGaAs photodiode (Thorlabs DMSP1180-class; its curve was not read: R 0.95 assumed).
PICKOFF_1180_R = 0.95
# Semrock NFD01-1064-25x36 (option b): Tavg > 90 % at 350-1015 and 1140-1600 nm, R > 98 % at 1064 nm only (1070 nm not
# specified), 45 deg, 1.05 mm fused silica, damage rating 1 J/cm2 at 532 nm (10 ns) only: no CW rating. $774.18 (07:05Z).
NOTCH_DICHROIC_T = 0.9
FOV_PD_MM = 1.6                               # photodiode field stop on the plate: P500K pinhole (500 um) behind an f = 50 mm lens

# ------------------------------------------------------------------------------------------------ detectors (radiometry.py)
# Each: spectral response table (nm, A/W for photodiodes, QE for cameras), noise and full scale, with sources.
DET = {
    "PDA36A2": dict(
        kind="photodiode", area_mm2=13.0, out_max_V=10.0,
        resp=[(400, 0.062), (450, 0.114), (500, 0.166), (550, 0.22), (600, 0.275), (650, 0.335), (700, 0.389), (750, 0.447),
              (800, 0.499), (850, 0.547), (900, 0.589), (950, 0.624), (975, 0.6355), (1000, 0.624), (1025, 0.553), (1050, 0.404),
              (1070, 0.264), (1100, 0.14)],
        # gain dB: (Hi-Z transimpedance V/A, bandwidth Hz, NEP at the peak W/rtHz)
        gains={0: (1.51e3, 12e6, 75.7e-12), 10: (4.75e3, 1.6e6, 5.8e-12), 20: (1.5e4, 1e6, 3.4e-12), 30: (4.75e4, 260e3, 3.4e-12),
               40: (1.5e5, 90e3, 3.25e-12), 50: (4.75e5, 28e3, 3.69e-12), 60: (1.5e6, 9e3, 4.0e-12), 70: (4.75e6, 3e3, 4.29e-12)},
        src="Thorlabs PDA36A2: $400.01 (item page 06:51Z); gain table and 0-10 V Hi-Z output from the Si amplified photodetector "
            "Specs tab (06:53Z); responsivity pda36a2_responsivity.xlsx (06:55Z); active area flush with the housing face, the SM1 "
            "boss 2.2 mm proud of it (housing drawing)"),
    "PDA20CS2": dict(
        kind="photodiode", area_mm2=3.14, out_max_V=10.0,
        resp=[(800, 0.1727), (850, 0.2198), (900, 0.3095), (950, 0.4515), (1000, 0.4973), (1070, 0.6155), (1100, 0.6523),
              (1200, 0.7602), (1300, 0.8405), (1400, 0.93), (1500, 1.018), (1550, 1.034), (1600, 1.036), (1625, 1.016), (1650, 0.9785),
              (1675, 0.7433), (1700, 0.2574), (1725, 0.11), (1750, 0.047)],
        gains={0: (1.51e3, 11e6, 61e-12), 10: (4.75e3, 1.5e6, 5.7e-12), 20: (1.5e4, 1e6, 2.93e-12), 30: (4.75e4, 260e3, 2.19e-12),
               40: (1.51e5, 90e3, 1.95e-12), 50: (4.75e5, 28e3, 2.24e-12), 60: (1.5e6, 9e3, 2.25e-12), 70: (4.75e6, 3e3, 2.28e-12)},
        src="Thorlabs PDA20CS2 (InGaAs, Ø2 mm): $676.21 (item page 06:51Z); gain table from the InGaAs amplified photodetector Specs "
            "tab (06:53Z); responsivity pda20cs2_responsivity.xlsx (06:55Z): 1.03 A/W at 1550 nm, 0.98 at 1650, 0.26 at 1700"),
    "IMX296 mono": dict(
        kind="camera", px_um=3.45, fwc_e=10636.0, read_e=4.81, bits=10, diag_mm=6.3, min_exposure_us=29.0,
        qe=[(450, 0.623), (525, 0.658), (600, 0.617), (650, 0.541), (700, 0.453), (750, 0.339), (800, 0.247), (808, 0.231),
            (850, 0.165), (900, 0.103), (940, 0.061), (1000, 0.024), (1070, 0.005)],
        src="Sony IMX296 mono as measured in Teledyne FLIR's EMVA 1288 report for the FFY-U3-16S2M "
            "(https://softwareservices.flir.com/FFY-U3-16S2/latest/EMVA/EMVA.html, 2026-11-25T06:46Z): QE 64.3 % at 525 nm, "
            "temporal dark noise 4.81 e-, saturation 10,636 e-, 10-bit; QE at other wavelengths read off its published curve "
            "(+/-1 point; 1070 nm 'at baseline', taken as 0.5 %). Minimum exposure 29-30 us (Raspberry Pi GS camera; InnoMaker: "
            "trigger low-pulse width + 14.26 us)"),
    "Chronos 2.1-HD mono": dict(
        kind="camera", px_um=10.0, fwc_e=15000.0, read_e=25.0, bits=12, diag_mm=22.0, min_exposure_us=10.0,
        qe=[(525, 0.48), (600, 0.44), (700, 0.36), (800, 0.26), (850, 0.185), (900, 0.125), (950, 0.08), (1000, 0.045), (1070, 0.02)],
        src="Kron Chronos 2.1-HD (LUX2100, 1920 x 1080, 10 um, min exposure 10 us, 24,046 fps at 640 x 96; "
            "https://www.krontech.ca/product/chronos-2-1-hd-high-speed-camera/ and its manual, 2026-11-25T06:49Z): QE read off "
            "the manual's curve to 900 nm (48 % at 525, 26 % at 800, 18.5 % at 850, ~12.5 % at 900); 950-1070 nm extrapolated "
            "(assumed). Kron publishes no full well or read noise: XIMEA's LUX19HS camera (15,000 e-, 25 e-) stands in"),
}
CAMS = DET                                      # the viewport cameras use the same entries

# C-mount lenses (focal length, f-number range, minimum object distance from the lens front, image circle, price, source)
LENSES = {
    "Kowa LM50JC10M 50 mm": dict(f_mm=50.0, f_range=(2.8, 16), mod_mm=100.0, image_circle_mm=11.0, price=931.0,
                                 note="400-1000 nm broadband coating; reseller list price (wilcoimaging.com, 07:14Z)"),
    "Edmund 50 mm C Series #59-873 + 10 mm tube": dict(f_mm=50.0, f_range=(2.0, 22), mod_mm=150.0, image_circle_mm=11.0, price=500.0 + 367.0,
                                                       note="MOD 250 mm without a tube; tube kit #54-668 $367; VIS coating 425-675 nm"),
    "Edmund 35 mm C VIS-NIR #67-716": dict(f_mm=35.0, f_range=(1.65, 22), mod_mm=165.0, image_circle_mm=11.0, price=635.0,
                                           note="425-1000 nm BBAR"),
    "Fujinon HF50XA-5M 50 mm": dict(f_mm=50.0, f_range=(2.4, 16), mod_mm=200.0, image_circle_mm=17.6, price=748.0,
                                    note="1.1 in. format; MOD 200 mm from the barrel front; no NIR claim; reseller list"),
    "Edmund 75 mm C VIS-NIR #74-054": dict(f_mm=75.0, f_range=(2.0, 16), mod_mm=500.0, image_circle_mm=11.0, price=690.0,
                                           note="MOD 500 mm: needs ~15 mm of extension at 180-200 mm"),
}


def CAMERA_CASES(wd_lw, wd_lp):
    """(camera, lens, f-number, port, working distance) cases for viewports.py."""
    return [("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 4.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 8.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Edmund 35 mm C VIS-NIR #67-716", 4.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Edmund 75 mm C VIS-NIR #74-054", 5.6, "LW", wd_lw),
            ("IMX296 mono", "Kowa LM50JC10M 50 mm", 4.0, "LW", wd_lw),
            ("IMX296 mono", "Kowa LM50JC10M 50 mm", 5.6, "LP", wd_lp),
            ("IMX296 mono", "Edmund 35 mm C VIS-NIR #67-716", 4.0, "LP", wd_lp)]


ROI = {"Chronos 2.1-HD mono": (640, 96), "IMX296 mono": (1456, 1088)}     # Chronos at 24,046 fps; the IMX296 full frame (60 fps)
