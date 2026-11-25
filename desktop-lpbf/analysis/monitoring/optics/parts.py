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
             (970, 0.9741), (980, 0.9653), (990, 0.9744), (1000, 0.9871), (1070, 0.9739), (1100, 0.9831), (1300, 0.9838),
             (1400, 0.9874), (1500, 0.9826), (1550, 0.9712), (1600, 0.9613), (1650, 0.8057), (1700, 0.5748), (1750, 0.5351)]
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
# InGaAs pick-off (both options): the DMSP950 at cube2 also reflects 1300-1750 nm into the camera arm (R 0.96 at 1600, 0.81 at
# 1650, 0.57 at 1700 nm; its data file), so a fourth cube in that arm, a 45 deg ~1180 nm dichroic (Thorlabs DMLP/DMSP1180
# class; its curve was not read: 0.9 assumed), splits 1200-1750 nm to the InGaAs photodiode and 955-990 nm to the camera.
PICKOFF_1180_R = 0.9
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
    return [("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 2.8, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 4.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 5.6, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 8.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Kowa LM50JC10M 50 mm", 11.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Edmund 35 mm C VIS-NIR #67-716", 4.0, "LW", wd_lw),
            ("Chronos 2.1-HD mono", "Edmund 75 mm C VIS-NIR #74-054", 5.6, "LW", wd_lw),
            ("IMX296 mono", "Kowa LM50JC10M 50 mm", 4.0, "LW", wd_lw),
            ("IMX296 mono", "Kowa LM50JC10M 50 mm", 5.6, "LP", wd_lp),
            ("IMX296 mono", "Edmund 35 mm C VIS-NIR #67-716", 4.0, "LP", wd_lp)]


ROI = {"Chronos 2.1-HD mono": (640, 96), "IMX296 mono": (1456, 1088)}     # Chronos at 24,046 fps; the IMX296 full frame (60 fps)

# ------------------------------------------------------------------------------------------------ the parts list
# group, item, part number, vendor, qty, unit price (USD; None = quote), price basis, url, fetched (UTC), where / why
T_ = "https://www.thorlabs.com/item/"
PARTS = [
    # coaxial branch, baseline (monitoring_spec.COAX: cube1 x -155, cube2 x -215 to -y, cube3 x -285)
    ("coax", "45 deg short-pass dichroic, cube1 (already in the design: optics-bom O5)", "DMSP1000", "Thorlabs", 0, 331.76, "list",
     T_ + "DMSP1000", "2026-11-25T06:43Z", "reflects the laser into the galvo; T 0.96 at 520-985 nm; leaks 0.063 % at 1070 nm (OD 3.2)"),
    ("coax", "beam trap on cube1's far port: the DMSP1000 passes 0.06-0.12 % of the forward beam (0.3-0.6 W at 500 W) straight through",
     "cage-mounted beam trap rated >= 1 W at 1070 nm (Thorlabs BTC30 class)", "Thorlabs", 1, None, "estimate $100-200", "", "",
     "a Class 4 stray beam exists today wherever cube1's -y face is open"),
    ("coax", "shared 1070 nm blocker after cube1 (short-pass 1000 nm, OD 5.4-6.0 at 1064-1100 nm)", "FESH1000", "Thorlabs", 1, 169.26, "list",
     T_ + "FESH1000", "2026-11-25T06:57Z", "replaces the NF1064-44 (O16), which also blocks 520-720 nm (OD 4.2-4.6) and would cut the 700 nm channel"),
    ("coax", "cube2 dichroic: reflects 955-990 nm to the camera (-y), passes < 930 nm on", "DMSP950", "Thorlabs", 1, 331.76, "list",
     T_ + "DMSP950", "2026-11-25T06:43Z", "Thorlabs raw data: T 0.96 below 920 nm, R 0.93-0.97 at 960-1000 nm"),
    ("coax", "cube3 dichroic: reflects < 790 nm to photodiode A, passes > 825 nm to photodiode B", "DMLP805", "Thorlabs", 1, 331.76, "list",
     T_ + "DMLP805", "2026-11-25T06:46Z", "R 0.99 at 650-775 nm; T 0.97-0.98 at 850-1000 nm"),
    ("coax", "photodiode A band, 700 nm, 40 nm FWHM (OD > 5 at 200-1200 nm)", "FBH700-40", "Thorlabs", 1, 193.82, "list",
     "https://www.thorlabs.com/hard-coated-nir-bandpass-filters", "2026-11-25T06:48Z", "clean of plume lines for metals (lines.md); outside the 750-875 nm galvo stop band"),
    ("coax", "photodiode B band, 900 nm, 40 nm FWHM", "FBH900-40", "Thorlabs", 1, 193.82, "list",
     "https://www.thorlabs.com/hard-coated-nir-bandpass-filters", "2026-11-25T06:48Z", "Mg I 880.7 nm at its edge (weak); Ar I 912 nm only if argon were excited"),
    ("coax", "photodiode B (A is the existing T2 / O15 unit)", "PDA36A2", "Thorlabs", 1, 400.01, "list", T_ + "PDA36A2", "2026-11-25T06:51Z",
     "run at 30-40 dB (260-90 kHz): SNR 40-150 on the pool"),
    ("coax", "photodiode lenses, f = 50 mm achromat (one exists as O18)", "AC254-050-B", "Thorlabs", 1, 110.91, "list", T_ + "AC254-050-B",
     "2026-11-25T07:09Z", "images the plate at 0.31x onto the field stop"),
    ("coax", "field stops, 500 um pinhole (1.6 mm on the plate), one per photodiode, at each band's own focus", "P500K", "Thorlabs", 2, 84.12, "list",
     T_ + "P500K", "2026-11-25T07:11Z", "sized for the lateral colour (up to 0.6 mm at 700 nm at the L75 edge) plus the pool"),
    ("coax", "coaxial camera, monochrome IMX296 board for the Pi 5 (C/CS mount, trigger input, no IR filter on the mono version)",
     "CAM-IMX296RAW (mono)", "InnoMaker", 1, 69.0, "list (sale; $79 regular)", "https://www.inno-maker.com/product/cam-mipi296raw-trigger/",
     "2026-11-25T06:49Z", "7.4 um/px with the 75 mm tube lens; minimum exposure ~30 us"),
    ("coax", "tube lens for the IMX296, f = 75 mm (7.4 um/px; 0.94 x 0.71 mm at 128 x 96 px)", "AC254-075-B", "Thorlabs", 1, 110.91, "list",
     T_ + "AC254-075-B", "2026-11-25T07:09Z", "refocus 0.1-0.3 mm at the sensor for the 955-990 nm band"),
    ("coax", "second 1070 nm blocker in the camera arm (OD ~14 in all)", "FESH1000", "Thorlabs", 1, 169.26, "list", T_ + "FESH1000",
     "2026-11-25T06:57Z", "the camera band has no bandpass filter, so this replaces its out-of-band blocking"),
    ("coax", "30 mm cage cube for a round Ø1 in. dichroic (cube + base + 45 deg mount), cubes 2 and 3", "C4W + B4C/M + FFM1", "Thorlabs", 2,
     75.32 + 122.65 + 72.77, "list (sum)", T_ + "C4W", "2026-11-25T07:13-07:17Z", "CM1-DCH/M ($205.91) takes only 25 x 36 mm rectangles"),
    ("coax", "cage plates, rods and lens tubes (4 x CP33/M, 12 x ER2-ER4, 6 x SM1L10, 2 x SM1A3/A6)", "CP33/M, ER2/3/4, SM1L10, SM1A3", "Thorlabs", 1,
     4 * 20.43 + 12 * 7.64 + 6 * 16.49 + 2 * 22.8, "list (sum, typical counts)", T_ + "CP33_M", "2026-11-25T07:15-07:19Z", "count to be set from the drawn layout"),
    # options
    ("coax option", "InGaAs channel behind the DMSP1000 (1625-1725 nm leaks through it at 3-30 %): photodiode", "PDA20CS2", "Thorlabs", 0, 676.21,
     "list", T_ + "PDA20CS2", "2026-11-25T06:51Z", "sees solid metal down to ~800-890 K filling the field stop at 9-90 kHz (radiometry.md)"),
    ("coax option", "InGaAs channel: two 1070 nm blockers (long-pass 1250 nm, OD ~5.2 each at 1070, T ~0.99 at 1300-1700)", "FELH1250", "Thorlabs", 0,
     169.26, "list", T_ + "FELH1250", "2026-11-25T06:57Z", "one alone leaves the diffuse 1070 nm leak at ~10 % of the pool signal, a cat's-eye return at ~100x"),
    ("coax option", "InGaAs channel: lens f = 100 mm, 1050-1700 nm AR, and a 1.0 mm pinhole (1.6 mm on the plate)", "AC254-100-C + P1000K", "Thorlabs", 0, 120.45 + 84.12,
     "list (sum)", T_ + "AC254-100-C", "2026-11-25T07:09Z", ""),
    ("coax option", "InGaAs channel: fourth cube in the camera arm, a 45 deg ~1180 nm dichroic (the DMSP950 reflects 1300-1750 nm into that arm)",
     "DMLP1180 / DMSP1180 class + cube", "Thorlabs", 0, None, "not priced (Ø1 in. DMLP/DMSP parts list at $331.76; cube $270.74)", "", "",
     "curve not read: check it splits 955-990 nm from 1600-1750 nm"),
    ("coax option", "InGaAs channel: move the shared FESH1000 into the two Si photodiode arms (it blocks 1550-1650 nm)", "FESH1000", "Thorlabs", 0,
     169.26, "list", T_ + "FESH1000", "2026-11-25T06:57Z", "qty 2 if the InGaAs channel is added"),
    ("coax option", "notch dichroic to replace the DMSP1000 (InGaAs at 1140-1600 nm): NOT recommended", "NFD01-1064-25x36", "Semrock (IDEX)", 0, 774.18,
     "list", "https://www.idex-hs.com/store/product-detail/nfd01_1064_25x36?cat_id=semrock_optical_filters&node=individual_optical_filters",
     "2026-11-25T07:05Z", "no CW rating (1 J/cm2 at 532 nm, 10 ns only); 1070 nm not specified; would carry 500 W at 20 kW/cm2"),
    ("coax option", "if the galvo passes 850 nm: cube2 a 50:50 plate (camera 850/10, NIST-like)", "BSW26 + FBH850-10", "Thorlabs", 0, 363.52 + 193.82,
     "list (sum)", T_ + "BSW26", "2026-11-25T07:02Z", "halves every channel's light"),
    ("coax option", "Chronos on the coaxial arm: tube lens f = 200 mm (8.0 um/px)", "AC254-200-B", "Thorlabs", 0, 110.91, "list", T_ + "AC254-200-B",
     "2026-11-25T07:09Z", "the camera itself is the side camera's (S1), moved"),
    # side camera at LW
    ("side (LW)", "high-speed camera, mono, 8 GB (16 GB $7,200, 32 GB $7,900)", "Chronos 2.1-HD", "Kron Technologies", 1, 6800.0, "list",
     "https://www.krontech.ca/product/chronos-2-1-hd-high-speed-camera/", "2026-11-25T06:49Z", "24,046 fps at 640 x 96; 10 us minimum exposure"),
    ("side (LW)", "50 mm C-mount lens that focuses at 176 mm (MOD 100 mm), 400-1000 nm coating, 2/3 in. image circle", "LM50JC10M", "Kowa", 1, 931.0,
     "reseller list (wilcoimaging.com)", "https://wilcoimaging.com/products/kowa-lm50jc10m", "2026-11-25T07:14Z", "25 um/px across, 113 um along the plate"),
    ("side (LW)", "camera filter: 850 nm, 10 nm FWHM (OD > 5 to 1200 nm)", "FBH850-10", "Thorlabs", 1, 193.82, "list", T_ + "FBH850-10",
     "2026-11-25T06:56Z", "FBH850-40 ($193.82) with an LED source"),
    ("side (LW)", "second 1070 nm blocker (OD > 11 with the bandpass)", "FESH1000", "Thorlabs", 1, 169.26, "list", T_ + "FESH1000", "2026-11-25T06:57Z",
     "0.1 W of diffuse 1070 nm reaches a 12.5 mm pupil at LW"),
    ("side (LW)", "light: 850 nm LED, 2.7 W minimum, through LP or BW", "SOLIS-850C", "Thorlabs", 1, 1377.86, "list", T_ + "SOLIS-850C",
     "2026-11-25T07:00Z", "enough for ~10 us at f/4 from LP, ~50 us from BW (viewports.md)"),
    ("side (LW)", "LED driver with pulse mode (250 kHz small-signal; rise time not published)", "DC2200", "Thorlabs", 1, 2593.01, "list", T_ + "DC2200",
     "2026-11-25T06:56Z", "check a 10 us pulse on the bench"),
    ("side (LW) option", "light: 808 nm, 10 W, fibre-coupled, pulses from 10 us (Class 4: the guard panel is transparent at 808 nm)",
     "808LD-2-CCMMINI-2-MM (AeroDIODE)", "LaserDiodeSource", 0, 6490.0, "list",
     "https://www.laserdiodesource.com/shop/808nm-10W-CW-Source-System-AeroDiode", "2026-11-25T07:03Z", "LSO review first"),
    ("side (LW) option", "camera with 1 us minimum exposure (freezes 20 m/s spatter with enough light)", "Chronos 1.4", "Kron Technologies", 0, 4500.0,
     "list (8 GB)", "https://www.krontech.ca/product/chronos-1-4-high-speed-camera/", "2026-11-25T06:51Z", "24 % QE at 850 nm"),
    ("side (LW) option", "pulsed diode-laser illumination, 300-500 W peak at 810 nm, 10 ns-10 us", "CAVILUX Smart UHS", "Cavitar", 0, None, "quote",
     "https://www.cavitar.com/product/cavilux-smart-uhs-for-ultra-high-speed-illumination/", "2026-11-25T07:03Z", "Class 3B/4"),
    # steep camera at LP
    ("steep (LP)", "monochrome IMX296 board", "CAM-IMX296RAW (mono)", "InnoMaker", 1, 69.0, "list (sale)",
     "https://www.inno-maker.com/product/cam-mipi296raw-trigger/", "2026-11-25T06:49Z", "10 um/px over 15 x 11 mm with the 50 mm lens"),
    ("steep (LP)", "50 mm C-mount lens, MOD 100 mm", "LM50JC10M", "Kowa", 1, 931.0, "reseller list", "https://wilcoimaging.com/products/kowa-lm50jc10m",
     "2026-11-25T07:14Z", "alternative: Edmund 35 mm C VIS-NIR #67-716 ($635, MOD 165 mm; 16 um/px)"),
    ("steep (LP)", "filters: 850 nm 10 nm bandpass + 1070 nm short-pass", "FBH850-10 + FESH1000", "Thorlabs", 1, 193.82 + 169.26, "list (sum)",
     T_ + "FBH850-10", "2026-11-25T06:56Z", "up to 0.4 W diffuse and a 1.3 W glint bound at 1070 nm reach its pupil"),
    # layer camera (existing M6): blocking during lasing
    ("layer camera (M6)", "second 1070 nm blocker behind the FESH0950 (OD 5.1 alone; 0.44 W diffuse + a 1.4 W glint bound reach its pupil)",
     "FESH1000", "Thorlabs", 1, 169.26, "list", T_ + "FESH1000", "2026-11-25T06:57Z", "for dashcam video during lasing"),
]


def main():
    out = ROOT / "monitoring" / "optics-parts.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "group", "item", "part_number", "vendor", "qty", "unit_usd", "line_usd", "price_basis", "url", "fetched_utc", "notes"]
    rows = []
    tot = {}
    for i, (g, item, pn, ven, q, u, basis, url, t, note) in enumerate(PARTS, 1):
        line = None if u is None else round(q * u, 2)
        rows.append(dict(id=f"MO{i}", group=g, item=item, part_number=pn, vendor=ven, qty=q, unit_usd="" if u is None else round(u, 2),
                         line_usd="" if line is None else line, price_basis=basis, url=url, fetched_utc=t, notes=note))
        if line:
            tot[g] = tot.get(g, 0.0) + line
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    for g, v in tot.items():
        print(f"{g}: ${v:,.2f}")
    print("wrote", out)
    return tot


if __name__ == "__main__":
    main()
