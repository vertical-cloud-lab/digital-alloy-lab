"""Bought parts drawn to their published dimensions, as drop-in replacements for the envelopes in lpbf_low.py (issue #260).

Each builder returns a cq.Shape in the SAME local frame as the generic helper or envelope it replaces. 15 of them are
now used by lpbf_low.py (integrated 2026-11-20, with the fit changes listed in real-parts.md); swaps() keeps the
pre-integration swap test (old placements and names) for the record. Round 6 (2026-11-25, oem-parts.md) adds to the model
edwards_nxds6i (BOM G2), filter_train_5169K72 (the 5169K72 on KF-25 adapters, BOM G5) and transmitter_on_sae4 (the 3861N11
on its SAE-4 adapter, BOM G7). Built but not in the model: mcm_4396K21 (the budget pump).
Dimensions come from the vendor's drawing, listing or datasheet named in SOURCES; where the vendor publishes CAD we
compare our shape with it by volume and sorted bounding-box extents, the way verify_fasteners.py does. Vendor CAD is
never committed: it is fetched into /tmp (vendor-cad-manifest.csv records URL, size and sha256).

    python desktop-lpbf/cad/vendor_parts.py inventory   # every Part of build(): which are envelopes, ranked -> analysis/out/real-parts/
    python desktop-lpbf/cad/vendor_parts.py verify      # our shapes vs vendor CAD in /tmp/parts-work/vcad (and /tmp/parts-work/teknic)
    python desktop-lpbf/cad/vendor_parts.py swapcheck   # swap each builder into a build() and run exact booleans against its neighbours

Run each under the memory cap, e.g. /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/cad/vendor_parts.py swapcheck (17 min wall,
7 min CPU on a busy 4-core runner; inventory takes seconds, verify about 5 min with the 64 MB Teknic STEP).
Units mm. Every builder states its local frame; "drop-in for" names the lpbf_low call it replaces.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
V = cq.Vector
IN = 25.4


# --------------------------------------------------------------------------------------------
# small helpers (kept local so this file does not depend on lpbf_low)
# --------------------------------------------------------------------------------------------
def _box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def _cyl(r, p0, d, h):
    return cq.Solid.makeCylinder(r, h, V(*p0), V(*d))


def _fuse(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out.fuse(s)
    return out.clean()


def _revolve(pts):
    """Solid of revolution about local z from a closed (r, z) polyline (r >= 0)."""
    w = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    return w.val()


def _rbox(x0, x1, y0, y1, z0, z1, r, edges="|Z"):
    w = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
    if r > 0:
        w = w.edges(edges).fillet(r)
    return w.val().translate(V(x0, y0, z0))


# --------------------------------------------------------------------------------------------
# Sources: one entry per builder. dims = the numbers the builder uses; cad = vendor file used by verify()
# --------------------------------------------------------------------------------------------
SOURCES = {
    "clearpath_sd_231x": dict(vendor="Teknic", pn="CPM-SDSK-2311S-RLN (2310S same frame)", price="$293 (2311S), $265 (2310S), qty 1-9",
        url="https://teknic.com/files/downloads/23xx%20CPM%20Dimensional%20Drawing.pdf",
        dims="flange 59.10 sq; body 84.81 behind the mounting face; pilot 38.10 x 1.90; shaft 9.50 x 20.57 (3 mm key); 4 x 5.20 on 66.67 BC; connector block 53.85 wide, 22.75 above the flange, 38.49 long (assumed: the unlabelled .515 [38.49] dimension); 0.6 kg. From Teknic's STEP (2026-11-23): 6 mm flange plate with R3 corners, octagonal body behind it (17.5 mm chamfers), Ø2.5 pin fins on the rear 9.8 mm, connector block ends 4.8 mm short of the rear face with a Ø11 boss under it, two connector pockets 9 deep opening toward the flange",
        cad="/tmp/parts-work/teknic/CPM-231x-Q.STEP", fetched="2026-11-20T14:11Z"),
    "mcm_6709K12": dict(vendor="McMaster-Carr", pn="6709K12", price="$144.71 each", url="https://www.mcmaster.com/6709K12/",
        dims="28 overall height from rail bottom; 34 wide; 38.8 steel block + end caps/seals = 56.6 long; grease nipple +5.5; carriage underside 4.7 above rail bottom; 4 x M4 on 26 x 26; end caps and seals 23.5 high (McMaster CAD, 2026-11-23)",
        cad="/tmp/parts-work/vcad/6709K12.STEP", fetched="2026-11-20T13:57Z"),
    "mcm_6709K33": dict(vendor="McMaster-Carr", pn="6709K33", price="$0.31 per mm (280 mm = $86.80)", url="https://www.mcmaster.com/6709K33/",
        dims="15 wide x 15 high; M4 holes 60 c-c, 20 from the end, 9.7 deep counterbore listed; raceway grooves 2 per side (assumed R1.6 at 3.5 and 11 mm, not published)",
        cad="", fetched="2026-11-20T14:05Z"),
    "mcm_4566N401": dict(vendor="McMaster-Carr", pn="4566N401", price="$244.44 each", url="https://www.mcmaster.com/4566N401/",
        dims="length 43; body 23; flange 40 x 10 with flats 30 across (McMaster CAD); bolt circle 32, 6 x 4.5 holes; bore = screw 12",
        cad="/tmp/parts-work/vcad/4566N401.STEP", fetched="2026-11-20T13:58Z"),
    "mcm_6627T91": dict(vendor="McMaster-Carr", pn="6627T91", price="$81.74 each", url="https://www.mcmaster.com/6627T91/",
        dims="NEMA 17, 42.3 sq (stator 41.9); body 48.0 behind the mounting face; pilot 22 x 2; shaft 5 D-profile x 24 beyond the pilot; rear cap with a 0.76 lead boss. From McMaster's CAD (2026-11-23): 9.5 mm end caps (3.5 chamfers), 41.9 stator with 6.4 chamfers, 4 x M3 9 deep, lead notch 9 x 7 through the rear cap, Ø10 x 4.5 rear recess",
        cad="/tmp/parts-work/vcad/6627T91.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5786N23": dict(vendor="McMaster-Carr", pn="5786N23", price="$13.65 each", url="https://www.mcmaster.com/5786N23/",
        dims="ISO-KF 25 flange OD 39.88 (1.57 in.), face bore 26.16, rim 3.05 thick, 15 deg back taper; 1 in. x 0.065 in. tube end; 12.7 long",
        cad="/tmp/parts-work/vcad/5786N23.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5786N25": dict(vendor="McMaster-Carr", pn="5786N25", price="$17.31 each", url="https://www.mcmaster.com/5786N25/",
        dims="ISO-KF 40 flange OD 54.86 (2.16 in.), face bore 41.14, rim 3.05 thick, 15 deg back taper; 1.5 in. x 0.083 in. tube end; 19.05 long",
        cad="/tmp/parts-work/vcad/5786N25.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_4518K72": dict(vendor="McMaster-Carr", pn="4518K72", price="$13.67 each", url="https://www.mcmaster.com/4518K72/",
        dims="KF-25 wing-nut clamp: ring OD 55.2, 17 thick at the ears; hinge to -x (32.5 from the axis), wing nut to +x (44.7) and +y (36.1) (McMaster CAD extents). Ring section from the CAD (2026-11-23): C-channel 16 tall, OD 55.2, channel bottom r 25.0, lips r 15.9 on 15 deg tapers; hinge block 22.4 wide",
        cad="/tmp/parts-work/vcad/4518K72.STEP", fetched="2026-11-20T14:01Z"),
    "mcm_4518K73": dict(vendor="McMaster-Carr", pn="4518K73", price="$15.31 each", url="https://www.mcmaster.com/4518K73/",
        dims="KF-40 wing-nut clamp: ring OD 71.0, 17 thick at the ears; hinge to -x (40.0), wing nut to +x (53.5) and +y (36.1) (McMaster CAD extents). Ring section from the CAD (2026-11-23): C-channel 16 tall, OD 71.0, channel bottom r 30.2, lips r 23.7 on 15 deg tapers; hinge block 22.4 wide",
        cad="/tmp/parts-work/vcad/4518K73.STEP", fetched="2026-11-20T14:01Z"),
    "mcm_4123K45": dict(vendor="McMaster-Carr", pn="4123K45", price="$300.80 each", url="https://www.mcmaster.com/4123K45/",
        dims="KF-25 x KF-25 full-port ball valve: end to end 124.2 (4.89 in.); body 60.45 square (2.38 in.); handle top 91.7 above the axis; lever 138.2 long from the stem (7.89 in. overall). From McMaster's CAD (2026-11-23): 7.5 mm end caps with lobes round 4 x Ø4.8 tie bolts, Ø54.6 centre body, Ø26.6 stem neck flaring to Ø33.8, Ø50 stop plate, lever plate 24 wide rising at 72 deg to a 4.8 thick grip at z 86.9-91.7; bore Ø21.8",
        cad="/tmp/parts-work/vcad/4123K45.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_3861N11": dict(vendor="McMaster-Carr", pn="3861N11", price="$358.05 each", url="https://www.mcmaster.com/3861N11/",
        dims="1/4 NPT male x 16.5 (0.65 in.); 1.96 in. (49.8) from the thread shoulder to the cable exit; 36 in. lead (not drawn). From McMaster's CAD (2026-11-25): thread r 5.6-6.9 over 12.7 with a Ø5.4 port, undercut to r 8.7; hex 27 A/F, corners turned to Ø29, 6.5 thick; body Ø24 to 29.8 above the shoulder; cap to the Ø13 gland at 34.7; gland Ø13 to 39.5, Ø10.2 to 50.15",
        cad="/tmp/parts-work/vcad/3861N11.STEP", fetched="2026-11-20T14:00Z"),
    "mcm_5169K72": dict(vendor="McMaster-Carr", pn="5169K72 (+ 9179K14 HEPA element)", price="$107.84 each (element $48.73)", url="https://www.mcmaster.com/5169K72/",
        dims="3 3/4 in. dia x 3 5/8 in. high (listing). From McMaster's CAD (2026-11-25): outlet boss Ø27.7 x 14.9 (1/2 NPSC female); can Ø87.9 to z 76.5; side inlet boss Ø25.5 at z 48.8 reaching x 57.4 on a Ø42 pad; lid Ø95 z 76.5..86.5 tapering to Ø76 at z 92.96; two bail clips on +/-y (hinge bracket, latch lever, wire hook over the lid)",
        cad="/tmp/parts-work/vcad/5169K72.STEP", fetched="2026-11-20T14:02Z"),
    "mcm_4396K21": dict(vendor="McMaster-Carr", pn="4396K21", price="$587.53 each", url="https://www.mcmaster.com/4396K21/",
        dims="overall 14 1/2 x 5 5/8 x 12 in. (368.3 x 142.9 x 304.8, to the handle top); layout (motor, pump block, handle, top intake) from the catalogue photo; no CAD offered",
        cad="", fetched="2026-11-20T14:02Z"),
    "edwards_nxds6i": dict(vendor="Edwards", pn="nXDS6i, A73501983 (standard variant)", price="$5,977.85 (BOM G2)",
        url="https://cdn.shopify.com/s/files/1/0598/4021/files/nXDS-6i_10i_15i_20i.pdf (page 3: Edwards' dimension drawing); https://global.my.edwardsvacuum.com/en/Catalog/Pumps/Dry-Scroll-Pumps/nXDSi-Scroll-Pumps/nXDS6i/p/A73501983 (26.20 kg, 0.432 m, NW25 in and out)",
        dims="432 long; 265 over the fins, 282 with the exhaust flange (149 from the centre line); 302 to the lifting eye, 286 to the cowl, 285 to the inlet flange; cowl axis 160 above the feet; NW25 inlet 225 from the motor end, 55 off the centre line; NW25 exhaust on the side, 145 high, 347 from the motor end; feet 189 across, slots on 230 x 120. Section shapes read off the drawing's views (+/-3 mm). Silhouette IoU against the drawing's 5 views: cad/oem/drawing_fit.py",
        cad="", fetched="2026-11-25T00:42Z"),
    "sae4_npt_adapter": dict(vendor="(not chosen)", pn="SAE-4 male (7/16-20 O-ring boss) x 1/4 NPT female straight adapter, 316 SS", price="estimate (BOM G7)",
        url="BOM G7: 'an SAE-4 to 1/4 NPT adapter for the 3861N11 (not found: estimate)'",
        dims="assumed from typical catalogue adapters: 3/4 in. hex x 17.1, 9.1 stud below the O-ring seat, 26.2 overall, 1/4 NPT female 12 deep; the 3861N11 engages 10 mm",
        cad="", fetched=""),
    "filter_train_5169K72": dict(vendor="McMaster-Carr + assumed fittings", pn="5169K72 + 9179K14 on 2 x 1/2 NPT x KF-25 adapters and 2 x KF-25 90 deg elbows, on a 6061 stand",
        price="see BOM G5 (adapters and elbows not priced)", url="https://www.mcmaster.com/5169K72/",
        dims="housing as mcm_5169K72, side inlet turned to -y; adapters 20 long; elbows 55 centre to face (assumed); outlet boss 135 above the base plate so the outlet elbow lands on the gas loop's outlet stub (z 60, x +55)",
        cad="/tmp/oem/vcad/5169K72.STEP", fetched="2026-11-25T00:56Z"),
    "thorlabs_fth160_1064": dict(vendor="Thorlabs", pn="FTH160-1064", price="$1,011.78 (vendor-lookups.csv)", url="https://media.thorlabs.com/globalassets/items/f/ft/fth/fth160-1064/stn012046-e0w.pdf",
        dims="50.2 long; output ring 90 dia x 9.2 (= FFL 191.7 - WD 182.5); nose face 41.0 and cone end 34.8 above the flange (dimensioned); M85x1 thread ~12.5 long and 78 dia step to 29.3 (scaled, not dimensioned); nose 53 dia with a 39 aperture; 0.8 kg; A1 7.5 / A2 12.3 / mirror spacing 20 (Figure 1.3)",
        cad="", fetched="2026-11-20T14:00Z"),
    "scanlab_basicube20": dict(vendor="SCANLAB", pn="basiCube 20", price="quote (BOM L5)", url="https://www.scanlab.de/sites/default/files/2025-06/SCANLAB-basiCube-Series-EN.pdf",
        dims="155 deep x 130 wide x 122 high; input aperture 20 dia, axis 30 above the bottom face and 83.5 from the left edge of the input face; output axis 57.15 from the input face, 58.25 from the left edge (beam displacement 25.25); 3.75 kg without objective; objective ring and holes not dimensioned",
        cad="", fetched="2026-11-20T14:15Z"),
    "ipg_collimator_d5": dict(vendor="IPG Photonics", pn="standard collimator, 5 mm beam (YLR-500-U3-SM-AC option)", price="not quoted yet",
        url="quotes/ipg-ylr-500-u3-sm-ac.md (IPG drawing transcribed; PDF not committed)",
        dims="housing 30 dia, 28 dia at the output end, 128 +/- 3 long, plus 78 strain relief (relief diameters and the 28 dia step length assumed)",
        cad="", fetched="2026-11-18"),
    "ipg_collimator_d25": dict(vendor="IPG Photonics", pn="affixed collimator, 2.5 mm beam (YLR series option)", price="not quoted yet",
        url="IPG YLR series datasheet rev 2/26 (lists the 2.5 mm option; no drawing); quotes/ipg-ylr-500-u3-sm-ac.md",
        dims="no IPG drawing found: drawn as the 5 mm unit's housing (30 dia x 128 + 78 strain relief), assumed. No catalogued QBH collimator of f 20-25 mm rated >= 500 W was found "
             "(IPG's shortest standard is 50 mm; Wavelength COL-1070-D25-F30 is f = 30 mm), so the 2.5 mm unit (96 um at f = 160) is the catalogue choice",
        cad="", fetched="2026-11-23T22:41Z"),
    "thorlabs_cage_cube": dict(vendor="Thorlabs", pn="CM1-DCH/M (dichroic cube) + DMSP1000; fold mirror NB1-K14 in a 30 mm cage cube", price="DMSP1000 $331.76; NB1-K14 $172.87",
        url="https://www.thorlabs.com/ndyag-laser-line-mirrors?pn=NB1-K14",
        dims="cube side 41.9 assumed (no Thorlabs drawing read); NB1-K14: Ø1 in. x 6 mm, R > 99.5 % at 1047-1064 nm, 0-45 deg, typ. 99.80 % (s) / 99.41 % (p) at 1070 nm and 45 deg, "
             "CW 20 kW/cm at 1070 nm (Thorlabs certification measurement)",
        cad="", fetched="2026-11-23T22:41Z"),
    "thorlabs_pda36a2": dict(vendor="Thorlabs", pn="PDA36A2", price="$400.01 (vendor-lookups.csv)", url="https://www.thorlabs.com/item/PDA36A2",
        dims="envelope 22.4 x 50.8 x 71.1 with an SM1 port, assumed (the PDA36A2 drawing was not read); 350-1100 nm, 13 mm2, 12 MHz BW",
        cad="", fetched="2026-11-23T22:37Z"),
    "gentec_up55m_500w": dict(vendor="Gentec-EO", pn="UP55M-500W-H12-D0", price="$1,969.00", url="https://www.gentec-eo.com/products/up55m-500w-h12-d0",
        dims="89 H x 89 W x 43 D, 0.81 kg, Ø55 aperture, water-cooled, 500 W continuous, 45 kW/cm2 (Gentec page); fittings and recess assumed. "
             "The fan-cooled UP55G-600F-HD-D0 is 120 x 120 x 135 mm, 2.75 kg: taller than the 120 mm chamber",
        cad="", fetched="2026-11-23T22:38Z"),
    "ipg_ylr500_u3": dict(vendor="IPG Photonics", pn="YLR-500-U3-SM-AC", price="approx. $23k (quote 2026-11-18)", url="quotes/ipg-ylr-500-u3-sm-ac.md (IPG spec G22-29856 and drawings; PDF not committed)",
        dims="4U: 176.5 high; 482.3 over the rack ears, 465 body; 506 body deep, 557.2 over the handles; 40 kg. Front (2026-11-23, from IPG's render of a current rack-mount YLR, YLR_Series_Card on cdn.ipgphotonics.com; the U3's own front drawing is not public): control strip x -212..-144 with START (z 138), e-stop (z 88), key switch (z 36); display x -139..-87, z 22..162; slatted fan grille x -62/-14.5..212, z 12..150, 9 deep; 12 x 12 bar handles z 10..166.5 (+/-5 mm, button sizes assumed). Front redrawn 2026-11-25 from IPG single-mode family render (YLS_SM_Family_Main, its 4U rack unit): operators at x -177.5 (START z 150.7, mushroom z 119, key z 84.2), window x -152.4..-96 z 74..168, dark perforated fan field over the right ~45 % with a curved left edge and a band along the bottom (+/-6 mm)",
        cad="", fetched="2026-11-23T22:45Z"),
    "eaton_5px1500rtg2": dict(vendor="Eaton", pn="5PX1500RTG2", price="not found", url="https://assets.tripplite.com/product-pdfs/en/5px1500rtg2.pdf",
        dims="2U, 86.36 high x 436.88 wide x 447.04 deep; 23 kg; rack ears 482.6 (standard 19 in., not stated for this model). Front (2026-11-23, from the datasheet's straight-on photo, 1.04 mm/px): grille x -213.2..115.3, z 4.3..81.2, 1.5 deep; badge x -176.9..-153.8, z 30.2..55.3; LCD module x 120.1..213.2; LCD x 146.4..195.3, z 29.9..66.1; 5 keys at z 19; LED bar z 6..9.5 (+/-2 mm). Front re-measured 2026-11-25 on Eaton\'s 2000 px straight-on image (eaton.com 5PX1500RTG2_C, 3.85 px/mm): grille x -207.9..107.0 z 5.8..78.7; badge 31 x 31 at x -187.8..-156.8 z 26.6..57.3; LCD module x 133.6..206.8; LCD x 147.5..187.3 z 35.3..62.6; 5 square keys 13.4 mm at z 9.6..22.8; LED bar z 5.8..8.6 (+/-1 mm)",
        cad="", fetched="2026-11-23T22:40Z"),
}


# --------------------------------------------------------------------------------------------
# Motion: servos, steppers, guides, screws
# --------------------------------------------------------------------------------------------
def clearpath_sd_231x(shaft_l=20.57, connector="+y"):
    """Teknic ClearPath-SD NEMA 23, 231x frame (CPM-SDSK-2310S/2311S), drawing D1171/M, refined to Teknic's 3D model
    (CPM-231x-Q.STEP, sections compared 2026-11-23). Drop-in for lpbf_low.servo_nema23(): mounting face at local z = 0,
    body toward -z, shaft +z; the connector block is on local +y (connector="-y" puts it on the other side).
    Drawn: the 6 mm flange plate (59.1 square, R3 corners, 4 x Ø5.2 through on the 66.67 BC), the body behind it as an
    octagon with 17.5 mm corner chamfers (so the bolt heads clear it), the pin-fin heat sink on the rear 9.8 mm (Ø2.5
    pins on a 4.4 x 4.2 mm staggered grid), the connector block with its two connector pockets (8-pin I/O, 4-pin power)
    opening toward the flange, and the rear boss under the block. Not drawn: Teknic's internal annular void (its model
    is hollow between r 6.5 and 26.5 from z -12.5 to -40: the real motor's stator fills it), the four small cover
    screws and the logo relief."""
    sq, L = 59.10, 84.81
    t_fl, fin = 6.0, 9.8                                   # flange plate; pin-fin depth at the rear
    zf = -L + fin                                          # rear face of the solid body (pin roots)
    flange = cq.Workplane("XY").rect(sq, sq).extrude(-t_fl).edges("|Z").fillet(3.0).val()
    for sx in (-1, 1):                                     # 4 x Ø5.2 on a Ø66.67 bolt circle (47.14 square), through the flange
        for sy in (-1, 1):
            flange = flange.cut(_cyl(2.6, (sx * 23.57, sy * 23.57, -t_fl - 0.01), (0, 0, 1), t_fl + 0.02))
    body = cq.Workplane("XY").rect(sq, sq).extrude(-(L - fin - t_fl)).edges("|Z").chamfer(17.5).val().translate(V(0, 0, -t_fl))
    pts = []
    for j in range(14):                                    # staggered pin grid; keep pins inside the octagon (2 mm margin)
        y = 28.5 - 4.2 * j
        for i in range(-7, 8):
            x = 4.4 * i + (2.2 if j % 2 else 0.0)
            if abs(x) <= sq / 2 - 3.0 and abs(y) <= sq / 2 - 3.0 and abs(x) + abs(y) <= sq - 17.5 - 4.5:
                pts.append((x, y))
    pins = cq.Workplane("XY").workplane(offset=-L).pushPoints(pts).circle(1.25).extrude(fin + 0.5).val()
    s = 1.0 if connector == "+y" else -1.0
    blk = cq.Workplane("XY").box(53.85, 22.75 + 6.0, 38.49 - 4.8, centered=False).edges("|Z").fillet(4.0).val()
    blk = blk.translate(V(-53.85 / 2, sq / 2 - 6.0, -L + 4.8))           # block: 53.85 wide, 22.75 proud of the body, z -80.0..-46.32
    for x0, x1 in ((-22.0, -2.0), (2.0, 16.0)):                           # connector pockets (8-pin I/O, 4-pin power), 9 deep from the top
        blk = blk.cut(_box(x0, x1, sq / 2 + 6.5, sq / 2 + 19.5, -L + 38.49 - 9.0, -L + 38.49 + 0.01))
    boss = _cyl(5.5, (10.0, sq / 2 + 11.5, -L), (0, 0, 1), 4.85)          # round boss under the block (Teknic model)
    rear = _fuse([blk, boss])
    if s < 0:
        rear = rear.mirror("XZ")
    pilot = _cyl(19.05, (0, 0, 0), (0, 0, 1), 1.90)
    shaft = _cyl(4.75, (0, 0, 0), (0, 0, 1), shaft_l).cut(_box(-1.5, 1.5, 4.75 - 1.8, 5.0, shaft_l - 12.0, shaft_l + 0.1))
    return _fuse([flange, body, pins, rear, pilot, shaft])


def mcm_6627T91():
    """McMaster 6627T91 NEMA 17 stepper. Drop-in for lpbf_low.stepper_nema17(40): mounting face at z = 0, body toward
    -z, pilot (and here the 5 mm D shaft) toward +z. Refined to McMaster's CAD (2026-11-23): two 9.5 mm end caps 42.3
    square with 3.5 mm chamfers, the 41.9 square stator between them with 6.4 mm chamfers, 4 x M3 tapped 9 deep, the
    lead notch (9 wide, 7 deep) through the rear cap beside its boss, and the Ø10 x 4.5 rear bearing recess."""
    cap_f = cq.Workplane("XY").rect(42.3, 42.3).extrude(-9.5).edges("|Z").chamfer(3.5).val()
    cap_r = cap_f.translate(V(0, 0, -38.5))
    stator = cq.Workplane("XY").rect(41.9, 41.9).extrude(-29.2).edges("|Z").chamfer(6.4).val().translate(V(0, 0, -9.4))
    boss = _box(-8.0, 8.0, 21.15, 21.96, -48.0, -38.4)          # lead exit on the rear cap
    pilot = _cyl(11.0, (0, 0, 0), (0, 0, 1), 2.0)
    shaft = _cyl(2.5, (0, 0, 0), (0, 0, 1), 26.0).cut(_box(2.0, 3.0, -3.0, 3.0, 11.0, 26.1))
    out = _fuse([cap_f, stator, cap_r, boss, pilot, shaft])
    for sx in (-1, 1):
        for sy in (-1, 1):
            out = out.cut(_cyl(1.5, (sx * 15.5, sy * 15.5, -9.0), (0, 0, 1), 9.01))
    out = out.cut(_box(-4.5, 4.5, 14.3, 22.5, -48.01, -38.5))               # lead notch
    out = out.cut(_cyl(5.0, (0, 0, -48.01), (0, 0, 1), 4.51))               # rear bearing recess
    return out.clean()


def mcm_6709K12():
    """McMaster 6709K12 ball carriage for the 15 mm rail. Drop-in for lpbf_low.guide_carriage(57, 34, 28, 3, 15, 15):
    rail along local x, carriage centred at x = 0, rail centred in y, rail bottom at z = 0, carriage top at z = 28.
    McMaster's CAD (2026-11-23): only the steel block reaches the top; the end caps and seals stop at z = 23.5. Not drawn:
    the ball-retainer strips that reach into the rail's grooves, the balls and their return holes."""
    zb, zt = 4.7, 28.0
    blk = _box(-19.4, 19.4, -17.0, 17.0, zb, zt)
    caps = _box(-25.8, 25.8, -16.0, 16.0, zb + 0.4, 23.5)              # plastic end caps (top at z 23.5, McMaster CAD)
    seals = _box(-28.3, 28.3, -16.0, 16.0, zb + 0.5, 23.5)             # rubber end seals
    body = _fuse([blk, caps, seals])
    body = body.cut(_box(-30, 30, -7.8, 7.8, zb - 1, 15.4))            # rail channel (rail 15 x 15, 0.4 above its top)
    body = body.cut(_box(-30, 30, -17.5, -16.2, zb - 1, zb + 3.0)).cut(_box(-30, 30, 16.2, 17.5, zb - 1, zb + 3.0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(_cyl(1.65, (sx * 13.0, sy * 13.0, zt - 5.0), (0, 0, 1), 5.01))   # 4 x M4 x 5 deep, 26 x 26
    nip = _fuse([_cyl(3.5, (28.3, 0, 19.7), (1, 0, 0), 2.5), _cyl(2.6, (30.8, 0, 19.7), (1, 0, 0), 3.0)])   # above the rail top (McMaster CAD)
    return _fuse([body, nip])


def mcm_6709K33(L):
    """McMaster 6709K33 15 mm rail cut to L. Drop-in for lpbf_low.guide_rail(L, 15, 15): along local +x 0..L, centred
    in y, base on z = 0, M4 counterbored holes 60 mm c-c starting 20 mm from the end (listed). The four raceway
    grooves are not published: drawn as R1.6 grooves at z = 11 (upper) and 6.5 (lower) on each side (assumed)."""
    prof = cq.Workplane("YZ").polyline([(-7.5, 0), (7.5, 0), (7.5, 14.2), (6.7, 15.0), (-6.7, 15.0), (-7.5, 14.2)]).close().extrude(L).val()
    for sy in (-1, 1):
        for z in (11.0, 6.5):
            prof = prof.cut(_cyl(1.6, (-1, sy * 7.5, z), (1, 0, 0), L + 2))
    x = 20.0
    while x <= L - 5.0:
        prof = prof.cut(_cyl(2.25, (x, 0, -1), (0, 0, 1), 17)).cut(_cyl(3.75, (x, 0, 15.0 - 5.3), (0, 0, 1), 6.0))
        x += 60.0
    return prof


def mcm_4566N401():
    """McMaster 4566N401 fast-travel flange ball nut (M12, 10 mm lead). Drop-in for lpbf_low.ball_nut(12, 23, 43, 40, 10):
    nut on local x, centred at x = 0, flange at the -x end; bore = the 12 mm screw (contact). Flats 30 across on local y."""
    fl = _cyl(20.0, (-21.5, 0, 0), (1, 0, 0), 10.0).cut(_box(-22, -11, 15.0, 21, -21, 21)).cut(_box(-22, -11, -21, -15.0, -21, 21))
    for k in range(6):
        a = math.radians(60 * k)
        fl = fl.cut(_cyl(2.25, (-22, 16.0 * math.sin(a), 16.0 * math.cos(a)), (1, 0, 0), 12))
    body = _cyl(11.5, (-11.5, 0, 0), (1, 0, 0), 33.0)
    return _fuse([fl, body]).cut(_cyl(6.0, (-22, 0, 0), (1, 0, 0), 44))


# --------------------------------------------------------------------------------------------
# Vacuum hardware: ISO-KF weld stubs, clamps, valve, transmitter
# --------------------------------------------------------------------------------------------
KF_REAL = {   # flange OD, face bore, rim thickness, tube OD, tube ID, fitting length (McMaster CAD sections)
    25: dict(fo=39.88, fb=26.16, rim=3.05, to=25.40, ti=22.10, flen=12.70, pn="5786N23"),
    40: dict(fo=54.86, fb=41.14, rim=3.05, to=38.10, ti=33.88, flen=19.05, pn="5786N25"),
}


def kf_weld_stub(size, stub=None):
    """McMaster 5786N23 (KF-25) / 5786N25 (KF-40) aluminium weld fitting, extended with its own tube to `stub`.
    Drop-in for lpbf_low.kf_stub(size, stub): flange face at local z = 0, tube toward -z, hollow.
    Profile from McMaster's CAD: full-OD rim, then the ISO 2861 15 deg back taper (slope 3.73) down to the tube."""
    k = KF_REAL[size]
    d_taper = k["rim"] + (k["fo"] - k["to"]) / 2 / 3.73
    L = k["flen"] if stub is None else max(stub, d_taper + 0.5)   # a shorter stub = the weld tube trimmed (flange and taper kept)
    ro, rt, rb, ri = k["fo"] / 2, k["to"] / 2, k["fb"] / 2, k["ti"] / 2
    d1 = k["rim"] + (ro - rt) / 3.73
    outer = [(ri, 0.0), (ro, 0.0), (ro, -k["rim"]), (rt, -d1), (rt, -L), (ri, -L)]
    s = _revolve(outer)
    return s.cut(_cyl(rb, (0, 0, -k["rim"] + 0.2), (0, 0, 1), k["rim"]))   # face counterbore for the centring ring


def kf_wing_clamp(size):
    """McMaster 4518K72 (KF-25) / 4518K73 (KF-40) wing-nut clamp. Drop-in for lpbf_low.kf_clamp(size): centred on the
    joint plane (local z = 0), axis z, hinge toward -x, the bolt ears and wing nut toward +x (wing up +y).
    Ring section from McMaster's CAD (2026-11-23): a C-channel 16 mm tall, its bottom 5 mm outside the flange rims and
    its lips on the flanges' 15 deg back tapers; the hinge is a 22.4 mm wide block on -x."""
    if size == 25:
        ro, rb, rt, rl, zl, h, xh, xe, yw = 27.59, 25.02, 24.30, 15.86, 6.56, 8.0, -32.5, 44.65, 36.09
    else:
        ro, rb, rt, rl, zl, h, xh, xe, yw = 35.48, 30.17, 29.44, 23.67, 5.84, 8.0, -40.0, 53.47, 36.09
    zb, zt = 3.45, 4.29                                        # channel bottom half-height; start of the lip taper
    ring = _revolve([(rb, -zb), (rt, -zt), (rl, -zl), (rl, -h), (ro, -h), (ro, h), (rl, h), (rl, zl), (rt, zt), (rb, zb)])
    hinge = _box(xh, -ro + 3.0, -11.2, 11.2, -h, h)
    ears = _box(ro - 4.0, xe - 6.0, -7.0, 7.0, -8.5, 8.5).cut(_box(ro - 4.5, xe, -1.0, 1.0, -9, 9))
    bolt = _cyl(2.5, (xe - 12.0, -10.0, 0), (0, 1, 0), 32.0)
    wing = _fuse([_cyl(6.0, (xe - 12.0, 9.0, 0), (0, 1, 0), 9.0), _box(xe - 24.0, xe, 14.0, yw, -1.5, 1.5)])
    return _fuse([ring, hinge, ears, bolt, wing])


def mcm_4123K45(handle="+x"):
    """McMaster 4123K45 KF-25 x KF-25 manual full-port ball valve (the BOM's pump isolation valve, line G7).
    Local frame: inlet flange face at x = 0, flow along +x, outlet face at x = 124.2, stem up (+z) at x = 62.1; the
    lever (138.2 from the stem) points along `handle` ("+x": over the outlet, "-x": back over the inlet).
    Replaces the 'KF-25 angle, pneumatic' envelope: NOT a drop-in (straight-through, 124 mm long).
    Refined to McMaster's CAD (2026-11-23): KF-25 flange, Ø25.1 neck to x 22.1, Ø28.4 collar, then a 3-piece body: two
    7.5 mm end caps (Ø57.8 disc with lobes round the 4 tie bolts, 60 mm over the lobes) and a Ø54.6 centre body; 4 tie
    bolts Ø4.8 from x 23 to 101; a Ø26.6 stem neck flaring to Ø33.8, the Ø50 stop plate and stem nut; the lever is a
    plate 24 wide, flat over the hub, rising at 72 deg to a 4.8 mm thick straight grip at z 86.9-91.7."""
    k = KF_REAL[25]
    fl_in = _revolve([(10.9, 0), (k["fo"] / 2, 0), (k["fo"] / 2, 3.05), (12.54, 5.05), (12.54, 22.12), (14.19, 23.77), (14.19, 30.0), (10.9, 30.0)])
    fl_out = fl_in.mirror("XY").translate(V(0, 0, 124.2))
    tube = _fuse([fl_in, fl_out]).rotate(V(0, 0, 0), V(0, 1, 0), 90)     # axis z -> x
    body = [_cyl(27.3, (36.9, 0, 0), (1, 0, 0), 50.8)]                      # round centre body, x 37-87.5
    for x0 in (29.5, 87.2):                                                 # end caps 7.5 thick: Ø58 disc + lobes round the tie bolts
        body.append(_cyl(28.9, (x0, 0, 0), (1, 0, 0), 7.5))
        for sy in (-1, 1):
            for sz in (-1, 1):
                body.append(_cyl(5.6, (x0, sy * 23.71, sz * 23.71), (1, 0, 0), 7.5))
                web = _box(x0, x0 + 7.5, -5.6, 5.6, 18.0, 33.53).rotate(V(0, 0, 0), V(1, 0, 0), {(1, 1): -45, (-1, 1): 45, (-1, -1): 135, (1, -1): -135}[(sy, sz)])
                body.append(web)
    body = _fuse(body)
    bolts = [_cyl(2.4, (23.0, sy * 23.71, sz * 23.71), (1, 0, 0), 78.2) for sy in (-1, 1) for sz in (-1, 1)]
    neck = _fuse([_cyl(13.3, (62.1, 0, 27.0), (0, 0, 1), 11.2), cq.Solid.makeCone(13.3, 16.9, 3.7, V(62.1, 0, 38.2), V(0, 0, 1)),
                  _cyl(16.9, (62.1, 0, 41.9), (0, 0, 1), 6.7)])
    plate = _cyl(25.0, (62.1, 0, 48.5), (0, 0, 1), 4.6)
    stop = _cyl(2.5, (81.35, 0, 53.0), (0, 0, 1), 4.4)
    nut = _fuse([_cyl(12.5, (62.1, 0, 53.1), (0, 0, 1), 4.06), cq.Workplane("XY").polygon(6, 15.1).extrude(3.56).val().translate(V(62.1, 0, 57.16))])
    # lever (built for "-x", mirrored about the stem for "+x"): hub, rising arm, straight grip to 138.18 from the stem
    xs = 62.1
    prof = [(xs + 12.5, 53.8), (36.0, 53.8), (25.0, 86.9), (xs - 138.18, 86.9), (xs - 138.18, 91.69), (28.0, 91.69), (39.0, 57.16), (xs + 12.5, 57.16)]
    lever = cq.Workplane("XZ").polyline(prof).close().extrude(12.0, both=True).val()
    if handle == "+x":
        lever = lever.mirror("YZ", (xs, 0, 0))
    out = _fuse([tube, body, neck, plate, stop, nut, lever] + bolts)
    return out.cut(_cyl(10.9, (-1, 0, 0), (1, 0, 0), 126.2))   # full port, open


def mcm_3861N11(bodies=False):
    """McMaster 3861N11 0-15 psia transmitter. Local frame: the hex's port-side face (the thread shoulder) at z = 0 on the
    axis, the 1/4 NPT thread below (z -16.5..0), the cable gland ending at z = 50.15 (the listing's 1.96 in. to the cable
    exit). The 36 in. lead is not drawn. From McMaster's CAD (re-fetched 2026-11-25, sha256 as in cad/oem/cad-manifest.csv):
    thread r 5.6-6.9 over z -16.5..-4.6 with a Ø5.4 port bore, an undercut flaring to r 8.7 under the hex; hex 27 A/F with
    its corners turned to Ø29, 6.5 thick; body Ø24 to z 29.8; a cap tapering to the Ø13 gland at z 34.7; gland Ø13 to
    z 39.5, then Ø10.2 to z 50.15. bodies=True returns the named bodies; their union is the part."""
    b = {}
    thread = _revolve([(0, -16.5), (5.6, -16.5), (6.2, -15.9), (6.9, -4.6), (7.4, -3.8), (8.7, -1.5), (8.7, 0.5), (0, 0.5)])
    hexa = cq.Workplane("XY").polygon(6, 27.0 / math.cos(math.pi / 6)).extrude(6.5).val().rotate(V(0, 0, 0), V(0, 0, 1), 30)
    b["hex_and_thread"] = _fuse([thread, hexa.intersect(_cyl(14.5, (0, 0, 0), (0, 0, 1), 6.5))]).cut(_cyl(2.7, (0, 0, -17.0), (0, 0, 1), 13.0))
    b["body"] = _revolve([(0, 6.0), (12.0, 6.0), (12.0, 29.8), (10.4, 31.6), (7.8, 33.3), (6.48, 34.7), (6.48, 39.5), (0, 39.5)])
    b["cable_gland"] = _cyl(5.08, (0, 0, 39.0), (0, 0, 1), 11.15)
    return _bodies_or_solid(b, bodies)


SAE4_ADAPTER = dict(stud=9.1, hex_af=19.05, hex_h=17.1, npt_depth=12.0, engage=10.0)


def sae4_npt_adapter():
    """Straight adapter, SAE-4 male (7/16-20 UNF O-ring boss) x 1/4 NPT female, 316 SS: BOM G7's 'SAE-4 to 1/4 NPT adapter for
    the 3861N11 (not found: estimate)'. No catalogue drawing was read: proportions assumed from typical catalogue adapters
    (3/4 in. hex, 9.1 mm stud below the O-ring seat, 26.2 mm overall, 1/4 NPT female 12 deep). Local frame: the O-ring seat
    (the hex's bottom face, which lands on the lid) at z = 0, the stud below it."""
    a = SAE4_ADAPTER
    stud = _cyl(5.5, (0, 0, -a["stud"]), (0, 0, 1), a["stud"] + 0.5)          # 7/16-20 stud, 0.05 under the port's major radius
    hexa = cq.Workplane("XY").polygon(6, a["hex_af"] / math.cos(math.pi / 6)).extrude(a["hex_h"]).val()
    hexa = hexa.intersect(_cyl(10.75, (0, 0, 0), (0, 0, 1), a["hex_h"]))                 # corners turned to Ø21.5
    return _fuse([stud, hexa]).cut(_cyl(6.7, (0, 0, a["hex_h"] - a["npt_depth"]), (0, 0, 1), a["npt_depth"] + 1.0)).cut(
        _cyl(2.5, (0, 0, -a["stud"] - 1.0), (0, 0, 1), a["stud"] + a["hex_h"]))


def transmitter_on_sae4(bodies=False):
    """The lid's pressure transmitter as bought: McMaster 3861N11 screwed into the SAE-4 x 1/4 NPT adapter, the adapter in the
    lid's SAE-4 port. Local frame: the adapter's O-ring seat (the lid's top face) at z = 0, axis vertical. The 3861N11's
    thread engages 10 mm of the adapter's 12 mm female thread, so its hex sits 6.5 mm above the adapter: shoulder at
    z = 23.6, gland top at z = 73.75 (the old envelope reached z = 64)."""
    a = SAE4_ADAPTER
    zs = a["hex_h"] + (16.5 - a["engage"])
    t = {k: v.translate(V(0, 0, zs)) for k, v in mcm_3861N11(bodies=True).items()}
    b = dict(adapter=sae4_npt_adapter(), **t)
    return _bodies_or_solid(b, bodies)


# --------------------------------------------------------------------------------------------
# Gas module
# --------------------------------------------------------------------------------------------
def mcm_5169K72(bodies=False):
    """McMaster 5169K72 vacuum-rated intake-filter housing (takes the 9179K14 HEPA element), axis vertical. Local frame: axis
    at x = y = 0, the bottom of the outlet boss (1/2 NPSC female) at z = 0, the lid's top at z = 92.96; the side inlet boss
    toward +x; the bail clips on +/-y. From McMaster's CAD (re-fetched 2026-11-25, sha256 as in cad/oem/cad-manifest.csv;
    it draws the can solid): outlet boss Ø27.7 x 14.9; can Ø87.9 over z 14.9..76.5 with a 2.2 mm bottom chamfer; side inlet
    boss Ø25.5 at z 48.8 reaching x 57.4, on a Ø42 pad to x 48.5; lid Ø95 over z 76.5..86.5, tapering to Ø76 at the top;
    two bail clips (hinge block, latch lever, Ø3 wire hook over the lid's edge). bodies=True returns the named bodies."""
    b = {}
    can = _revolve([(0, 0), (13.87, 0), (13.87, 14.9), (41.7, 14.9), (43.94, 17.1), (43.94, 76.6), (0, 76.6)])
    pad = _cyl(21.0, (38.0, 0, 48.8), (1, 0, 0), 10.5)
    boss = _cyl(12.75, (45.0, 0, 48.8), (1, 0, 0), 12.4)
    b["housing"] = _fuse([can, pad, boss]).cut(_cyl(10.6, (44.0, 0, 48.8), (1, 0, 0), 14.0)).cut(_cyl(10.6, (0, 0, -1.0), (0, 0, 1), 14.0))
    b["lid"] = _revolve([(0, 76.5), (47.5, 76.5), (47.5, 86.5), (44.8, 90.1), (38.0, 92.96), (0, 92.96)])
    clips = []
    for sy in (-1, 1):
        y0, y1 = sorted((sy * 42.0, sy * 56.6))
        clips += [_box(sx * 7.7, sx * 9.2, y0, y1, 44.3, 63.4) if sx > 0 else _box(-9.2, -7.7, y0, y1, 44.3, 63.4) for sx in (-1, 1)]   # hinge bracket
        y0, y1 = sorted((sy * 56.5, sy * 57.7))
        clips.append(_box(-6.0, 6.0, y0, y1, 11.2, 58.1))                                     # latch lever
        for sx in (-1, 1):                                                                   # wire hook over the lid's edge
            clips.append(_cyl(1.5, (sx * 12.3, sy * 59.0, 45.0), (0, 0, 1), 48.3))
            clips.append(_cyl(1.5, (sx * 12.3, sy * 59.0, 93.3), (0, -sy, 0), 23.0))
        clips.append(_cyl(1.5, (-12.3, sy * 59.0, 45.0), (1, 0, 0), 24.6))
    b["bail_clips"] = _fuse(clips)
    return _bodies_or_solid(b, bodies)


KF25_ELBOW_CF = 55.0          # KF-25 90 deg elbow, centre to face (assumed: no catalogue drawing read)


def _kf25_flange(p, d):
    """ISO-KF 25 flange (OD 40, 5.5 thick, 15 deg back taper drawn as a 2 mm chamfer) with its sealing face at p, facing d."""
    fl = cq.Workplane("XY").circle(20.0).extrude(-5.5).faces("<Z").chamfer(2.0).val()
    dv = V(*d).normalized()
    z = V(0, 0, 1)
    ax = z.cross(dv)
    ang = math.degrees(math.acos(max(-1.0, min(1.0, z.dot(dv)))))
    if ax.Length > 1e-9:
        fl = fl.rotate(V(0, 0, 0), ax, ang)
    elif ang > 90:
        fl = fl.rotate(V(0, 0, 0), V(1, 0, 0), 180)
    return fl.translate(V(*p))


def filter_train_5169K72(bodies=False):
    """The G5 filter as placed in the gas module (issue #260, round 6): the 5169K72 housing upright with its side inlet turned
    to -y (toward the front), plumbed with KF-25 parts so that the gas loop's existing outlet stub (pointing +x at z 60 above
    the base plate, its tube end 55 mm from the housing axis) is unchanged:
    - outlet: a 1/2 NPT male x KF-25 adapter (20 mm below the boss) and a KF-25 90 deg elbow (centre to face 55, assumed),
      whose horizontal face lands on the outlet stub;
    - inlet: the same adapter on the side boss, then an elbow turning up, to the inlet stub (moved over the elbow);
    - a 6061 stand (a 30 x 15 post on the base plate with a saddle under the can, assumed).
    Local frame: housing axis at x = y = 0, z = 0 on the gas module's base plate; the outlet boss's bottom at z = 135.
    bodies=True returns the named bodies (housing parts and the plumbing); their union is the part."""
    z0 = 60.0 + KF25_ELBOW_CF + 20.0                     # 135: outlet axis at z 60, elbow, 20 mm adapter
    hb = mcm_5169K72(bodies=True)
    b = {k: v.rotate(V(0, 0, 0), V(0, 0, 1), -90).translate(V(0, 0, z0)) for k, v in hb.items()}   # side boss +x -> -y
    cf = KF25_ELBOW_CF
    # outlet: adapter (Ø25.4 tube, KF face at z0 - 20) and elbow down then +x, its face at x = cf (the outlet stub's tube end)
    pipes = [_cyl(12.7, (0, 0, z0 - 20.0), (0, 0, 1), 20.5), _kf25_flange((0, 0, z0 - 20.0), (0, 0, -1)),
             _kf25_flange((0, 0, z0 - 20.0), (0, 0, 1)),
             _cyl(12.7, (0, 0, 60.0), (0, 0, 1), z0 - 20.0 - 60.0), _cyl(12.7, (0, 0, 60.0), (1, 0, 0), cf), cq.Solid.makeSphere(12.7).translate(V(0, 0, 60.0)),
             _kf25_flange((cf, 0, 60.0), (1, 0, 0))]
    # inlet: side boss end at y = -57.4; adapter to y -77.4; elbow centre at y -132.4, turning up to the face at z_in + cf
    zi = z0 + 48.8
    yb = -57.4 - 20.0
    pipes += [_cyl(12.7, (0, -57.0, zi), (0, -1, 0), 20.4), _kf25_flange((0, yb, zi), (0, 1, 0)), _kf25_flange((0, yb, zi), (0, -1, 0)),
              _cyl(12.7, (0, yb, zi), (0, -1, 0), cf), cq.Solid.makeSphere(12.7).translate(V(0, yb - cf, zi)),
              _cyl(12.7, (0, yb - cf, zi), (0, 0, 1), cf), _kf25_flange((0, yb - cf, zi + cf), (0, 0, 1))]
    b["plumbing"] = _fuse(pipes).cut(_cyl(11.1, (0, 0, z0 - 21.0), (0, 0, 1), 22.0))
    stand = [_box(-15.0, 15.0, 52.0, 67.0, 0.0, z0 + 14.9), _box(-15.0, 15.0, 30.0, 67.0, z0 + 6.0, z0 + 14.9)]   # saddle under the can
    b["stand"] = _fuse(stand)
    return _bodies_or_solid(b, bodies)


FILTER_TRAIN_INLET = (0.0, -57.4 - 20.0 - KF25_ELBOW_CF, 60.0 + KF25_ELBOW_CF + 20.0 + 48.8 + KF25_ELBOW_CF)   # inlet KF face (local)


def mcm_4396K21():
    """McMaster 4396K21 rotary-vane pump (1e-2 Torr, 3 cfm, 1/2 hp), from the listed overall size 368.3 x 142.9 x 304.8
    (14 1/2 x 5 5/8 x 12 in., to the top of the handle) and the catalogue photo's layout: motor on +x, pump block on -x,
    handle over the pump block, flare intake tee on top of the block. McMaster offers no CAD for it, so only the overall
    extents are checked. Local frame: centred in x and y, feet on z = 0, length along x."""
    L, W, H = 368.3, 142.9, 304.8
    feet = _box(-L / 2 + 20, L / 2 - 40, -W / 2 + 10, W / 2 - 10, 0, 18)
    zm = 18 + W / 2 - 6                                                   # motor sits 2 mm into the feet (no tangent faces)
    motor = _cyl(W / 2 - 4, (-L / 2 + 150, 0, zm), (1, 0, 0), L - 150 - 6)
    endcap = _cyl(W / 2 - 14, (L / 2 - 6.5, 0, zm), (1, 0, 0), 6.5)
    block = _rbox(-L / 2, -L / 2 + 150, -W / 2, W / 2, 18, 205, 10)
    sw = _box(40.0, 110.0, -30, 30, 18 + W - 8, 18 + W + 30)                # switch / capacitor box on the motor
    handle = _fuse([_cyl(9.5, (-L / 2 + 30, 0, 205), (0, 0, 1), H - 205 - 9.5), _cyl(9.5, (-L / 2 + 30, 0, H - 9.5), (1, 0, 0), 120),
                    _cyl(9.5, (-L / 2 + 150, 0, 205), (0, 0, 1), H - 205 - 9.5)])
    intake = _fuse([_cyl(8.0, (-L / 2 + 95, 30, 205), (0, 0, 1), 40), _cyl(6.0, (-L / 2 + 75, 30, 235), (1, 0, 0), 40)])
    return _fuse([feet, motor, endcap, block, sw, handle, intake])


def edwards_nxds6i(bodies=False):
    """Edwards nXDS6i dry scroll pump (A73501983; the 6i/10i/15i/20i share one body: 'all variants are the same'). From Edwards'
    dimension drawing as reproduced on page 3 of Provac's nXDS 6i/10i/15i/20i sheet (see SOURCES): 432 long; 265 wide over
    the fins, 282 with the exhaust flange (149 from the centre line); 302 high to the lifting eye, 286 to the top of the fan
    cowl, 285 to the inlet flange; fan and cowl axis 160 above the feet; inlet NW25 225 from the motor end and 55 off the
    centre line; exhaust NW25 on the side, 145 high and 347 from the motor end; rubber feet 189 across; mounting slots on a
    230 x 120 pattern. Section shapes, the 8 side fins per side, the base and the connector panel are read off the drawing's
    views at 1.26 px/mm (+/-3 mm); nothing inside the cowl is drawn.
    Local frame: x from the motor end (x = 0) to the fan end (x = 432); y = 0 on the centre line, with the exhaust, the inlet
    offset and the connector panel on -y (the drawing's side view looks at the exhaust with the fan end on the right);
    z = 0 under the feet. bodies=True returns the named bodies (for per-body finishes); their union is the part."""
    L, zc = 432.0, 160.0
    b = {}
    # scroll housing, x 0..305. Its section is round about the cowl axis and widens toward the cowl: half-width 108 at the
    # motor end to 124 at x 300 in the drawing's plan view (core cone R 102 -> 116, fins 8 proud of it). Side profile from
    # the side views: motor-end block x 0..65 to z 256, top at z 245, rising from x 235 to the cowl's top at x 305.
    side = _prism_y([(0, 92.0), (0, 256.0), (65.0, 256.0), (68.0, 245.0), (235.0, 245.0), (305.0, 286.0), (305.0, 92.0)], -150, 150)
    core = cq.Solid.makeCone(102.0, 116.0, 305.0, V(0, 0, zc), V(1, 0, 0)).intersect(side)
    fins = []
    for zk in (103.0, 120.0, 137.0, 155.0, 173.0, 191.0, 210.0, 228.0):                 # side fins, z read off the side views
        slab = _box(4.0, 303.0, -140.0, 140.0, zk, zk + 3.0).intersect(cq.Solid.makeCone(112.0, 128.0, 305.0, V(0, 0, zc), V(1, 0, 0)))
        fins.append(slab.cut(_box(3.0, 304.0, -70.0, 70.0, zk - 1.0, zk + 4.0)).intersect(side))
    shoulder = _prism_y([(232.0, 238.0), (305.0, 286.0), (305.0, 238.0)], -150, 150).intersect(_box(230.0, 306.0, -80.0, 80.0, 230.0, 290.0))
    eye_boss = _cyl(15.0, (177.0, 0, 238.0), (0, 0, 1), 24.0)                              # boss under the lifting eye
    b["housing"] = _fuse([core, shoulder, eye_boss] + fins)
    # fan cowl, x 305..428: R 128 with a ~30 mm end radius (side views); its underside sweeps from the base (x 305, z 6) up to
    # z 100 at the fan end, as the drawing's side views show
    prof = [(0, 0), (130.0, 0), (130.0, 90.0), (126.0, 100.0), (118.0, 110.0), (106.0, 118.0), (90.0, 122.0), (0, 123.0)]   # (r, x - 305)
    cowl = _revolve(prof).rotate(V(0, 0, 0), V(0, 1, 0), 90).translate(V(305.0, 0, zc))
    cowl = cowl.intersect(_prism_y([(300.0, 0), (312.0, 6.0), (330.0, 14.0), (350.0, 26.0), (372.0, 48.0), (392.0, 74.0), (408.0, 90.0),
                                    (425.0, 99.0), (440.0, 100.0), (440.0, 286.0), (300.0, 286.0)], -150, 150))
    cowl = cowl.cut(_cyl(76.0, (L - 8.0, 0, zc), (1, 0, 0), 12.0))                          # fan recess, 4 deep in the end face (x 428)
    b["cowl"] = cowl.clean()
    grille = _cyl(76.0, (L - 8.0, 0, zc), (1, 0, 0), 1.5)
    for r0, r1 in ((14.0, 24.0), (30.0, 40.0), (46.0, 56.0), (62.0, 72.0)):                 # concentric openings of the guard
        grille = grille.cut(_cyl(r1, (L - 9.0, 0, zc), (1, 0, 0), 4.0).cut(_cyl(r0, (L - 10.0, 0, zc), (1, 0, 0), 6.0)))
    bars = [_box(L - 8.0, L, -100.0, 100.0, zk, zk + 3.0) for zk in (126.0, 144.0, 162.0, 180.0, 198.0)]   # the guard's horizontal bars,
    b["fan_guard"] = _fuse([grille, _box(L - 8.0, L - 6.5, -3.0, 3.0, zc - 74.0, zc + 74.0)] + bars)       # 4 proud of the face
    b["base"] = _rbox(42.0, 300.0, -110.0, 110.0, 8.0, 100.0, 20.0)                   # 220 wide over z 8..100 (front and rear views)
    b["feet"] = _fuse([_cyl(16.0, (x, sy * 78.5, 0), (0, 0, 1), 8.5) for x in (62.0, 278.0) for sy in (-1, 1)])
    b["connector_panel"] = _box(101.0, 254.0, -111.5, -109.0, 12.0, 62.0)
    xi, yi = 225.0, -55.0                                                                  # inlet NW25, flange top z 285
    b["inlet"] = _fuse([_cyl(17.0, (xi, yi, 230.0), (0, 0, 1), 49.5), _cyl(20.0, (xi, yi, 279.0), (0, 0, 1), 6.0)]).cut(
        _cyl(12.25, (xi, yi, 236.0), (0, 0, 1), 50.0))
    xe, ze = 347.0, 145.0                                                                  # exhaust NW25, flange face y -149
    b["exhaust"] = _fuse([_cyl(15.0, (xe, -100.0, ze), (0, -1, 0), 43.5), _cyl(20.0, (xe, -143.0, ze), (0, -1, 0), 6.0)]).cut(
        _cyl(12.25, (xe, -110.0, ze), (0, -1, 0), 40.0))
    ring = _cyl(19.0, (177.0, -4.0, 283.0), (0, 1, 0), 8.0).cut(_cyl(11.0, (177.0, -5.0, 283.0), (0, 1, 0), 10.0))   # eye Ø38, top z 302
    b["lifting_eye"] = _fuse([ring, _cyl(5.0, (177.0, 0, 240.0), (0, 0, 1), 26.0)])
    return _bodies_or_solid(b, bodies)


# --------------------------------------------------------------------------------------------
# Optics and laser
# --------------------------------------------------------------------------------------------
def thorlabs_fth160_1064():
    """Thorlabs FTH160-1064 f-theta lens, from drawing stn012046 (rev A, re-read 2026-11-23). Local frame: output end (toward
    the work) at z = 0, axis +z, input nose at z = 50.2. The flange shoulder (top of the Ø90 ring) is at z = 9.2 = FFL 191.7 -
    WD 182.5; the nose face is 41.0 above it and the cone ends 34.8 above it (both dimensioned). The M85x1 thread's length isn't
    dimensioned: scaled off the PDF it ends ~12.5 above the shoulder (z 21.7) and the Ø78 step runs to z 29.3. Thorlabs designs
    the lens for the 2nd galvo mirror A1 = 7.5 mm above the nose face (A2 = 12.3 to the first lens vertex, mirrors 20 apart;
    f-theta page, Figure 1.3). Drop-in for the lens envelope: translate to (0, 0, P['z_lens0'])."""
    prof = [(0, 0), (45.0, 0), (45.0, 9.2), (42.5, 9.2), (42.5, 21.7), (39.0, 21.7), (39.0, 29.3), (26.5, 44.0), (26.5, 50.2), (0, 50.2)]
    s = _revolve(prof)
    return s.cut(_cyl(19.5, (0, 0, 44.0), (0, 0, 1), 6.3)).cut(_cyl(37.5, (0, 0, -0.01), (0, 0, 1), 1.5))   # Ø39 input aperture, window recess


def scanlab_basicube20():
    """SCANLAB basiCube 20, from the basiCube brochure's drawing (2025-06). Local frame: the OUTPUT axis at x = y = 0,
    the bottom (beam-out) face at z = 0, the input face toward -x. Input aperture Ø20 at (-57.15, -25.25, 30): the beam
    enters 30 mm above the mounting face and 25.25 mm to the side of the output axis (side assumed from first-angle views)."""
    x0, x1 = -57.15, 155.0 - 57.15
    y0, y1 = -(130.0 - 58.25), 58.25
    s = _rbox(x0, x1, y0, y1, 0, 122.0, 6.0)
    s = s.cut(_cyl(10.0, (x0 - 1, -25.25, 30.0), (1, 0, 0), 12.0)).cut(_cyl(10.0, (0, 0, -1), (0, 0, 1), 12.0))
    return s


GALVO_IN = (-57.15, -25.25, 30.0)   # input beam point of scanlab_basicube20() in its local frame
GALVO_H = 122.0                     # basiCube 20 height (brochure)
# 2nd (y) mirror centre in scanlab_basicube20()'s frame: on the output axis at the input beam's height. The brochure gives the
# input height (30 above the mounting face) but not the mirror's: the beam runs level from the x mirror to the y mirror, so the
# y mirror's centre is taken at the same height (assumed). The lens's Ø53 nose can't enter the Ø20 output aperture, so with
# the galvo on the lens's nose plane the mirror sits >= 30 mm from the nose (Thorlabs designs the FTH160-1064 for 7.5 mm).
GALVO_M2 = (0.0, 0.0, 30.0)


def ipg_collimator_d5(relief=True):
    """IPG standard 5 mm-beam collimator on the delivery fibre (YLR-U3 option), from IPG's drawing as transcribed in
    quotes/ipg-ylr-500-u3-sm-ac.md: Ø30 housing, Ø28 at the output end, 128 long, plus 78 of strain relief.
    Local frame: output face at x = 0 on the beam axis, beam toward +x, housing toward -x. The Ø28 step length (8 mm)
    and the relief's diameters (Ø18 to Ø10) are not on the drawing transcription: assumed."""
    out = _cyl(14.0, (-8.0, 0, 0), (1, 0, 0), 8.0)
    body = _cyl(15.0, (-128.0, 0, 0), (1, 0, 0), 120.0)
    parts = [out, body]
    if relief:
        parts.append(cq.Solid.makeCone(5.0, 9.0, 78.0, V(-206.0, 0, 0), V(1, 0, 0)))
    return _fuse(parts)


def ipg_collimator_d25(relief=True):
    """IPG affixed collimator for a 2.5 mm beam (YLR series datasheet rev 2/26), which gives 96 um at f = 160 mm. IPG publishes no
    drawing of it, so it is drawn as the 5 mm unit's housing (Ø30 x 128 + 78 strain relief): assumed. Local frame as
    ipg_collimator_d5 (output face at x = 0, beam toward +x)."""
    return ipg_collimator_d5(relief)


def thorlabs_cage_cube(side=41.9):
    """30 mm cage cube holding a Ø1 in. optic at 45 deg (Thorlabs CM1-DCH/M dichroic mount for the DMSP1000; a kinematic cube of
    the same size for the fold mirror). Envelope only: the cube's side (41.9 mm) is assumed, not read off a Thorlabs drawing.
    Local frame: centred on the optic; Ø25.4 bores on the four beam faces (+/-x, +/-y); the optic's normal in the xy plane."""
    h = side / 2
    s = _box(-h, h, -h, h, -h, h)
    for d in ((1, 0, 0), (0, 1, 0)):
        s = s.cut(_cyl(12.7, tuple(-(h + 1) * c for c in d), d, side + 2))
    return s


def thorlabs_pda36a2():
    """Thorlabs PDA36A2 switchable-gain Si detector (350-1100 nm, 13 mm2): housing envelope 22.4 deep x 50.8 x 71.1 mm with an
    SM1 port on its face (envelope assumed from the PDA series' published outline, not read off the PDA36A2 drawing this
    round). Local frame: the port face at x = 0 facing +x (light arrives travelling -x), the detector on the x axis, the
    71.1 mm side along y."""
    body = _box(-22.4, 0.0, -35.55, 35.55, -25.4, 25.4)
    return _fuse([body, _cyl(15.25, (0, 0, 0), (1, 0, 0), 4.0)])


def gentec_up55m_500w():
    """Gentec-EO UP55M-500W-H12-D0 thermal power head: water-cooled, 500 W continuous, Ø55 mm aperture, 45 kW/cm2 average
    density, 89 H x 89 W x 43 D mm, 0.81 kg (Gentec product page, fetched 2026-11-23T22:38Z). Local frame: aperture face at
    z = 0 facing +z, centred on x = y = 0, body below. The 2 mm aperture recess and the two water fittings (Ø10 x 15 on the
    -y face) are assumed: Gentec's drawing wasn't fetched."""
    body = _box(-44.5, 44.5, -44.5, 44.5, -43.0, 0.0).cut(_cyl(27.5, (0, 0, -2.0), (0, 0, 1), 2.1))
    fits = [_cyl(5.0, (sx * 20.0, -44.5, -21.5), (0, -1, 0), 15.0) for sx in (-1, 1)]
    return _fuse([body] + fits)


def _prism_y(pts_xz, y0, y1):
    """Prism along +y from y0 to y1 over a closed (x, z) polygon."""
    w = cq.Workplane("XZ", origin=(0, y1, 0)).polyline(pts_xz).close().extrude(y1 - y0)   # XZ normal is -y: extrude from y1 back to y0
    return w.val()


def _bodies_or_solid(bodies, as_dict):
    if as_dict:
        return bodies
    return _fuse(list(bodies.values()))


def ipg_ylr500_u3(bodies=False):
    """IPG YLR-500-U3-SM-AC, 4U 19 in. chassis. Local frame: x centred, y = 0 at the rack-ear plane (rear face of the
    front panel), +y into the rack, z = 0 at the chassis bottom. Body 465 x 506 x 176.5, front panel 482.3 wide x 3 thick
    (it carries the ears), two handles to 557.2 - 506 = 51.2 in front of the body (IPG drawing, quotes/ipg-ylr-500-u3-sm-ac.md).
    Front (round 6, 2026-11-25) from IPG's own render of its single-mode family (YLS_SM_Family_Main hero image on IPG's
    'Single-Mode Fiber Lasers' page, cdn.ipgphotonics.com; see cad/oem/photo-manifest.csv), whose 4U rack unit is the
    single-mode rack laser with 'fans on the front panel' that the U3 drawing describes. Read off the 4U unit's front face
    as fractions of its width and height (1 px = 2.9 mm, the face seen ~30 deg off-axis: positions +/-6 mm): a light panel
    carrying one column of operators at x -177.5 (green START Ø29 at z 150.7, red mushroom Ø36 at z 119, key switch Ø29 at
    z 84.2), a light-grey portrait window next to it (x -152.4..-96, z 74..168) and the IPG logo; a dark perforated fan field
    over the right ~45 % whose left edge sweeps down in a curve to a band along the bottom under the operators (drawn as a
    1 mm recess; the perforation is a colour); black vertical bar handles on both ears. Round 5 drew IPG's 3U style (a
    slatted grille beside a dark control strip and a touch display), from a family card that does not show the 4U unit.
    bodies=True returns the named bodies (for per-body finishes in cad/oem/render_oem.py); their union is the part."""
    H, W = 176.5, 482.3
    b = {}
    b["chassis"] = _box(-232.5, 232.5, 0, 506.0, 0, H)
    field = [(-1.9, 168.0), (215.0, 168.0), (215.0, 7.0), (-205.0, 7.0), (-205.0, 57.5), (-192.0, 57.5), (-105.6, 61.8), (-71.9, 68.0),
             (-52.6, 80.1), (-33.3, 112.8), (-14.0, 153.7)]                              # the fan field's outline (x, z)
    win = (-152.4, -96.0, 74.0, 168.0)
    panel = _box(-W / 2, W / 2, -3.0, 0, 0, H)
    b["front_panel"] = panel.cut(_prism_y(field, -3.01, 0.01)).cut(_box(win[0], win[1], -3.01, 0.01, win[2], win[3]))
    b["fan_field"] = _prism_y(field, -2.0, 0.0)                                      # 1 mm recess
    b["display"] = _box(win[0], win[1], -2.5, 0, win[2], win[3])                       # light-grey window, 0.5 mm recess
    xc = -177.5
    b["start_button"] = _fuse([_cyl(14.5, (xc, -2.5, 150.7), (0, -1, 0), 3.5), _cyl(11.0, (xc, -5.5, 150.7), (0, -1, 0), 4.0)])
    b["estop"] = _fuse([_cyl(14.0, (xc, -2.5, 119.0), (0, -1, 0), 6.0), _cyl(18.0, (xc, -8.0, 119.0), (0, -1, 0), 11.0)])
    b["key_switch"] = _fuse([_cyl(14.5, (xc, -2.5, 84.2), (0, -1, 0), 4.0)]).cut(_box(xc - 1.0, xc + 1.0, -6.6, -4.5, 78.2, 90.2))
    hd = []
    for sx in (-1, 1):                     # vertical bar handles nearly the panel's height (IPG render), 12 x 12 bars
        xh = sx * (W / 2 - 14.0)
        hd += [_box(xh - 6, xh + 6, -45.0, -2.0, z0, z0 + 12.0) for z0 in (10.0, H - 22.0)]
        hd.append(_box(xh - 6, xh + 6, -51.2, -39.2, 10.0, H - 10.0))
    b["handles"] = _fuse(hd)
    return _bodies_or_solid(b, bodies)


def eaton_5px1500rtg2(bodies=False, ears=True):
    """Eaton 5PX1500RTG2 2U UPS (datasheet: 86.36 x 436.88 x 447.04, 23 kg). Same frame as ipg_ylr500_u3(): y = 0 at the
    rack-ear plane, the 3 mm front at y -3..0. The 482.6 mm ear width is the 19 in. standard (not stated for this model).
    Front (round 6, 2026-11-25) from Eaton's own straight-on product image (eaton.com SKU page, 5PX1500RTG2_C at 2000 x 2000 px:
    the bezel spans 1680 x 326 px, 3.85 px/mm across and 3.78 px/mm down; round 5 had only the datasheet's 500 px photo):
    a dark-grey bezel frame round a silver perforated grille (x -207.9..107.0, z 5.8..78.7) with the Eaton badge (31 x 31,
    x -187.8..-156.8, z 26.6..57.3); a dark slot to x 117.2; the black LCD module (x 133.6..206.8, z 5.8..78.7) with the lit
    LCD (x 147.5..187.3, z 35.3..62.6), five square keys (13.4 mm, centres x 142.0, 156.8, 170.8, 185.1, 199.6, z 9.6..22.8)
    and the blue LED bar along its bottom (z 5.8..8.6). Positions +/-1 mm. The perforation (Ø4.1 holes, 6.7 x 7.4 mm
    staggered pitch) is a colour, not drawn. ears=False leaves the rack ears off (Eaton's photos show the unit without them).
    bodies=True returns the named bodies; their union is the part."""
    H, Wb = 86.36, 436.88
    b = {}
    b["chassis"] = _box(-Wb / 2, Wb / 2, 0, 447.04, 0, H)
    if ears:
        b["rack_ears"] = _fuse([_box(-482.6 / 2, -Wb / 2, -3.0, 0, 0, H), _box(Wb / 2, 482.6 / 2, -3.0, 0, 0, H)])
    xg0, xg1, zg0, zg1 = -207.9, 107.0, 5.8, 78.7                                     # grille window
    xm0, xm1 = 133.6, 206.8                                                          # LCD module window
    bez = _box(-Wb / 2, Wb / 2, -3.0, 0, 0, H).cut(_box(xg0, xg1, -3.01, 0.01, zg0, zg1)).cut(_box(xm0, xm1, -3.01, 0.01, zg0, zg1))
    b["bezel"] = bez.cut(_box(xg1, 117.2, -3.01, -1.0, zg0, zg1))                       # the dark slot beside the grille, 2 mm deep
    badge = _box(-187.8, -156.8, -3.5, 0, 26.6, 57.3)                                # 0.5 mm proud of the bezel plane
    b["badge"] = badge
    b["grille"] = _box(xg0, xg1, -1.5, 0, zg0, zg1).cut(badge)
    scr = _box(147.5, 187.3, -3.01, -2.0, 35.3, 62.6)
    led = _box(xm0 + 1.3, xm1 - 0.9, -3.01, -2.6, zg0, 8.6)
    b["lcd_module"] = _box(xm0, xm1, -3.0, 0, zg0, zg1).cut(scr).cut(led)
    b["lcd_screen"] = _box(147.5, 187.3, -2.0, 0, 35.3, 62.6)
    b["led_bar"] = _box(xm0 + 1.3, xm1 - 0.9, -2.6, 0, zg0, 8.6)
    b["keys"] = _fuse([_box(xk - 6.7, xk + 6.7, -4.0, -2.9, 9.6, 22.8) for xk in (142.0, 156.8, 170.8, 185.1, 199.6)])   # 1 mm proud
    return _bodies_or_solid(b, bodies)


# --------------------------------------------------------------------------------------------
# Swaps into lpbf_low.build(): the exact placement each one-line change uses (and what it forces)
# --------------------------------------------------------------------------------------------
def swaps(M):
    """[(replaces: exact Part names, new shape in model coordinates, line to change in lpbf_low, note on fit)]."""
    P = M.P
    cx, cy, ix, iy = P["cx"], P["cy"], P["ix"], P["iy"]
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    lz1, xd = P["lid_z1"], P["x_dose"]
    zf = -P["floor"]
    g0 = P["z_base1"]
    import module_params as MP
    import modules_low as ML
    z = ML.zlevels()
    a0 = z["zc"] - MP.ARM_T
    car_lo, car_hi = min(MP.Z_P_MIN, MP.ZSTAGE_RELEASE) + a0, MP.Z_P_MAX + a0 + 40.0
    az1 = car_hi + 3.0
    rzc = lz1 + 28.0
    xc = P["x_park"]
    out = []

    def add(names, shape, line, note):          # names: Part-name prefixes (the model's names grow suffixes)
        out.append(dict(replaces=names, shape=shape, line=line, note=note))

    add(["Recoater servo (ClearPath-SD, NEMA 23)"], M.place(clearpath_sd_231x(20.57), (-cx - 60, ry_, rz_), (0, 1, 0), (1, 0, 0)),
        "rmot = place(VP.clearpath_sd_231x(20.57), (-cx - 60, ry_, rz_), (0, 1, 0), (1, 0, 0))",
        "59.1 sq (not 57.15) and 84.8 long (not 100) + a 22.75 mm connector block on top: the motor bracket top must drop ~1 mm (rz_ - 28.6 -> rz_ - 29.6)")
    add(["Z servo (ClearPath-SD, NEMA 23, folded)"], M.place(clearpath_sd_231x(18.0, connector="-y"), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1)),
        "modules_low.add_zstage: h.place(VP.clearpath_sd_231x(18.0, connector='-y'), (64.0, 80.0, az1), (1, 0, 0), (0, 0, 1))",
        "connector block must face -y (front): on +y it hits the process base plate (12.6 cm3) beyond the window's y = 114 edge; 84.8 long instead of 100")
    add(["Dosing stepper (NEMA 17)"], M.place(mcm_6627T91(), (xd, 74, rzc), (1, 0, 0), (0, -1, 0)),
        "place(VP.mcm_6627T91(), (xd, 74, rzc), (1, 0, 0), (0, -1, 0))",
        "48 mm body (not 40) and the 5 mm x 24 shaft now drawn; the shaft runs into the roller seal housing (designed)")
    add(["Recoater carriage (15 mm rail)"], M.place(mcm_6709K12(), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0)),
        "place(VP.mcm_6709K12(), (xc, iy, P['rc_rail_z']), (1, 0, 0), (0, -1, 0))", "same 28 x 34 section; 62.1 long with the grease nipple (was 57)")
    add(["Recoater guide rail (15 mm, 260 mm)"], M.place(mcm_6709K33(260.0), (-130, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0)),
        "rr = place(VP.mcm_6709K33(260.0), (-130, iy, P['rc_rail_z']), (1, 0, 0), (0, -1, 0))", "same envelope; raceway grooves drawn (assumed)")
    add(["Recoater ball nut (flange on the +x face)"], M.place(mcm_4566N401(), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1)),
        "place(VP.mcm_4566N401(), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1))", "flange has flats 30 mm across (faces +/-y)")
    zl0 = P["z_lens0"]
    add(["f-theta lens, f = 160 mm (FTH160-1064 envelope)"], thorlabs_fth160_1064().translate(V(0, 0, zl0)),
        "lens = VP.thorlabs_fth160_1064().translate(V(0, 0, P['z_lens0']))",
        "fits inside the old envelope; its M85x1 thread (z 191.7-204.5) ends 3.2 mm below the bridge (z 207.7): needs a 16 mm M85x1 adapter ring under the bridge")
    zb1_ = P["z_bridge1"]
    add(["2-axis galvo scan head (basiCube class)"], scanlab_basicube20().translate(V(0, 0, zb1_)),
        "galvo = VP.scanlab_basicube20().translate(V(0, 0, zb1_))",
        "155 x 130 x 122 (was 115 x 115 x 110); beam input at z = z_bridge1 + 30 (was + 45) and y = -25.25 (was 0): beam tube, shutter and collimator move")
    bz = zb1_ + GALVO_IN[2]
    add(["Collimator (QBH, f = 30 mm, D ~ 3.2 mm) on V-mount"], ipg_collimator_d5().translate(V(-210.0, GALVO_IN[1], bz)),
        "coll = VP.ipg_collimator_d5().translate(V(-210, -25.25, P['beam_z'])) with P['beam_z'] = P['z_bridge1'] + 30 (keep the V-mount block)",
        "206 mm with its strain relief (envelope 130): the relief ends at x = -416, 46 mm outside the guard's left panel (x = -370)")
    add(["Vacuum isolation valve (KF-25 angle, pneumatic)"],
        _fuse([M.place(kf_wing_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), mcm_4123K45("+x").translate(V(cx + 18, 0, 70))]),
        "vv = comp([place(VP.kf_wing_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), VP.mcm_4123K45('+x').translate(V(cx + 18, 0, 70))])",
        "the BOM's valve is a straight 124 mm ball valve with a 138 mm lever, not an angle valve: its outlet flange lands at x = 298, outside the guard (x = 290)")
    add(["Pressure transducer"], mcm_3861N11().translate(V(100, 50, lz1)),
        "VP.mcm_3861N11().translate(V(100, 50, lz1)); the lid port must then be 1/4 NPT (Ø13.7 drawn), not the 7/16-20 SAE-4 boss",
        "3861N11 has a 1/4 NPT male thread: the lid's new SAE-4 O-ring-boss port needs a different transmitter (or an SAE-4 x 1/4 NPT female adapter, +~25 mm)")
    for nm, p0, xd_, nrm, stub in [("Inlet plenum port (KF-25)", (0, cy + 32 + 20, 11), (1, 0, 0), (0, 1, 0), 26),
                                   ("Outlet plenum port (KF-25)", (86, (MP.OUTLET_Y[0] + MP.OUTLET_Y[1]) / 2, zf - 45 - 26), (1, 0, 0), (0, 0, 1), 26),
                                   ("Vacuum port (KF-25", (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0), 10)]:
        add([nm], M.place(kf_weld_stub(25, stub), p0, xd_, nrm), f"place(VP.kf_weld_stub(25, {stub}), {p0}, {xd_}, {nrm})", "McMaster 5786N23 profile + 1 in. x 0.065 in. tube")
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    add(["Overflow port (KF-40)"], M.place(kf_weld_stub(40, 16), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, -1)),
        "place(VP.kf_weld_stub(40, 16), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, -1))", "5786N25 takes 1.5 in. tube (38.1 OD), not 41.3")
    add(["Overflow clamp (KF-40)"], M.place(kf_wing_clamp(40), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1)),
        "place(VP.kf_wing_clamp(40), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1))", "wing nut reaches 53.5 mm from the axis (+x)")
    add(["Sealed cyclone + HEPA housing (316L, valves off for passivation)"], mcm_5169K72().translate(V(470, -40, g0 + 20)),
        "filt = VP.mcm_5169K72().translate(V(470, -40, g0 + 20)) (keep the 20 mm stand; inlet is now the side boss, outlet the bottom)",
        "Ø95 x 92 instead of Ø116 x 254; ports are 1/2 NPSC, so the two KF-25 filter ports move to NPT adapters")
    add(["Dry scroll pump (≤ 0.3 mbar, 6 m3/h class)"], mcm_4396K21().translate(V(770, 165, g0)),
        "pump = VP.mcm_4396K21().translate(V(770, 165, g0))", "368 x 143 x 305: 15 mm taller than the envelope with its inlet; intake is a flare tee on the pump block, so the KF-25 inlet moves")
    rx0, rx1, ry0 = -990.0, -430.0, -300.0
    zr_laser = M.Z_TRAY + 25.0 + 2 * 44.45
    add(["Fiber laser source, 500 W single-mode (3U)"], ipg_ylr500_u3().translate(V((rx0 + rx1) / 2, ry0 + 30, zr_laser + 1)),
        "laser unit: nu 3 -> 4 and the rack 470 -> 515 mm tall (or the DIN drawer 3U -> 2U); shape VP.ipg_ylr500_u3().translate(V(-710, ry0 + 30, zr))",
        "4U (176.5), not 3U: overlaps the scan PC above it by 43 mm in a 10U rack; handles 51 mm proud of the rack front")
    add(["UPS (Eaton 5PX 1500 class, 2U)"], eaton_5px1500rtg2().translate(V((rx0 + rx1) / 2, ry0 + 30, M.Z_TRAY + 25.0 + 1)),
        "VP.eaton_5px1500rtg2().translate(V(-710, ry0 + 30, zr))", "smaller than the 2U envelope (447 deep, not 530)")
    return out


# --------------------------------------------------------------------------------------------
# CLI: inventory, verify, swapcheck
# --------------------------------------------------------------------------------------------
OUT = HERE.parent / "analysis" / "out" / "real-parts"

# (substring of the Part name, status, real part / reason). status: env = envelope or generic shape of a bought part;
# done = replaced here; design = lab-made part (drawn as designed, not a vendor part)
GENERIC = [
    ("Leveling mounts", "checked", "McMaster 5537T983: drawn to McMaster's CAD dimensions (volume checked here)"),
    ("19 in. rack frame", "env", "no rack chosen; S9 lists 30 mm T-slot for the old cabinet"),
    ("UPS (Eaton", "done", "Eaton 5PX1500RTG2"),
    ("Fiber laser source", "done", "IPG YLR-500-U3-SM-AC (4U)"),
    ("Scan + laser controller PC", "env", "no PC chosen (BOM C1 is a SCANLAB RTC6 card, quote)"),
    ("DIN-rail drawer", "env", "contents chosen (C3, C4, S1) but no drawer/enclosure: BOM C6 is a McMaster 7812K14 wall box"),
    ("Rack side panels", "env", "sheet, no part number"),
    ("Overflow port (KF-40)", "done", "McMaster 5786N25"),
    ("Overflow jar", "env", "KF-40 half nipple: no part number in the BOM"),
    ("Overflow clamp", "done", "McMaster 4518K73"),
    ("Overflow-jar present sensor", "env", "AutomationDirect PAM-AP-1H (M12 x 45): not drawn yet"),
    ("Inlet plenum port", "done", "McMaster 5786N23"),
    ("Outlet plenum port", "done", "McMaster 5786N23"),
    ("Vacuum port (KF-25", "done", "McMaster 5786N23"),
    ("Layer-light LED bar", "env", "no part number"),
    ("Plate-height through-beam", "env", "Omron E32-T61-S: not drawn yet"),
    ("Module-present sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("Recoater guide rail", "done", "McMaster 6709K33 (no CAD offered for the cut length: drawn to the listing)"),
    ("Recoater carriage (15 mm rail)", "done", "McMaster 6709K12"),
    ("Recoater ball screw", "env", "McMaster 4566N101: kept as a Ø12 rod (CAD fetched; helical thread not redrawn)"),
    ("Recoater ball nut", "done", "McMaster 4566N401"),
    ("Recoater servo", "done", "Teknic CPM-SDSK-2311S-RLN"),
    ("Z servo", "done", "Teknic CPM-SDSK-2311S-RLN"),
    ("Z actuator body", "env", "'KR-class' actuator: not in the BOM (M3 lists 6638K11 + 6709K33 + 6709K12)"),
    ("Z carriage", "env", "part of the KR-class actuator envelope"),
    ("Pot magnet", "env", "McMaster 5679K95: CAD fetched; 7 mm cup drawn, 9 mm of extra parts in McMaster's model not resolved"),
    ("Dosing stepper", "done", "McMaster 6627T91"),
    ("Side reservoir port (KF-16", "env", "KF-16 blank: no part number"),
    ("Reservoir-docked sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("Drawer-closed sensor", "env", "AutomationDirect PAM-AP-1H: not drawn yet"),
    ("NFC reader antenna", "env", "Adafruit 364 board: not drawn"),
    ("Load cell", "env", "Laumas ALLUE3: not drawn yet"),
    ("Layer camera", "env", "Raspberry Pi HQ camera + C-mount lens: not drawn yet"),
    ("Pressure transducer", "done", "McMaster 3861N11 on an SAE-4 x 1/4 NPT adapter (transmitter_on_sae4, round 6; the adapter's dimensions are assumed)"),
    ("Overpressure relief valve", "env", "McMaster 4277T52: page needs a set-pressure choice before CAD; not fetched"),
    ("Door hinge leaves", "env", "labelled 1151A87 but drawn as custom knuckles; 1151A87 is a 3 x 3 in. two-leaf hinge (CAD fetched)"),
    ("Door hinge knuckles on the chamber", "env", "as above"),
    ("Draw-latch keepers", "env", "1807A61 strike (CAD fetched): real latch is 135.5 mm long"),
    ("Draw latches on the door", "env", "1807A61 (CAD fetched): real latch is 135.5 x 44 x 30.5 mm, drawn here as 24 x 12 x 18"),
    ("f-theta lens", "done", "Thorlabs FTH160-1064"),
    ("2-axis galvo scan head", "done", "SCANLAB basiCube 20"),
    ("Safety shutter + beam dump", "env", "no product chosen (BOM L4: quote)"),
    ("Collimator (", "env", "IPG 2.5 mm affixed collimator: no IPG drawing, drawn as the 5 mm unit's housing"),
    ("Coaxial-monitoring dichroic", "env", "Thorlabs DMSP1000 in a 30 mm cage cube: cube size assumed"),
    ("Fold mirror", "env", "Thorlabs NB1-K14 in a 30 mm cage cube: cube size assumed"),
    ("Coaxial photodiode chain", "env", "Thorlabs PDA36A2 + SM1 tube: envelope assumed"),
    ("Calibration power head", "done", "Gentec-EO UP55M-500W-H12-D0 (89 x 89 x 43, page dimensions)"),
    ("Process fiber", "env", "IPG delivery cable (Ø8.5 per IPG's QBH drawing; drawn Ø10)"),
    ("Dry scroll pump", "done", "Edwards nXDS6i A73501983 (edwards_nxds6i, round 6, from Edwards' dimension drawing; no CAD is public)"),
    ("Pump inlet (KF-25)", "done", "McMaster 5786N23-type KF-25 stub on the nXDS6i's NW25 inlet (round 6)"),
    ("Sealed cyclone + HEPA housing", "done", "McMaster 5169K72 + 9179K14 on KF-25 adapters and elbows (filter_train_5169K72, round 6; adapters, elbows and stand assumed)"),
    ("Filter inlet (KF-25)", "done", "KF-25 stub on the inlet elbow (round 6)"),
    ("Filter outlet (KF-25)", "done", "KF-25 stub on the outlet elbow (round 6)"),
    ("Sealed side-channel blower", "env", "no gas-tight blower of this size found (KNF N 630.1.2 SP.9 E is 569 x 296 x 315, 45 kg)"),
    ("Blower inlet", "env", "follows the blower"),
    ("Blower outlet", "env", "follows the blower"),
    ("Trace O2 analyzer + dew-point", "env", "Ntron Microx (panel 96 x 96 x 90) + Vaisala DMT143 (Ø28 x 91.6): not drawn yet"),
    ("Argon solenoid manifold", "env", "McMaster 8077K237 x 2 (CAD fetched) on a custom block: not drawn yet"),
    ("Argon pressure regulator", "env", "McMaster 78595A5 (CAD fetched, 91 MB): not drawn yet"),
    ("Vacuum isolation valve", "done", "McMaster 4123K45 (straight ball valve, not an angle valve)"),
    ("Gas-loop + vacuum hoses", "env", "McMaster 3497N23 is a 24 in. hose; routed lengths not matched"),
    ("Guard frame (20 mm T-slot)", "env", "simplified 20 mm profile; BOM S9 lists 30 mm 5537T97"),
    ("Guard-locking door switch", "env", "Omron D4JL-4NFA-C5-NPT: not drawn yet"),
    ("E-stop", "env", "IDEC XA1E-BV3U02-R: not drawn"),
    ("Key switch", "env", "McMaster 6749K3: not drawn"),
    ("Emission indicator", "env", "McMaster 7545K316 + 7545K7: not drawn"),
    ("Reset button", "env", "McMaster 6749K201: not drawn"),
    ("Tray dock", "env", "CombiTac-type: no part number"),
]


def _status(name):
    for sub, st, why in GENERIC:
        if name.startswith(sub) or sub in name:
            return st, why
    return "design", ""


def inventory():
    sys.path.insert(0, str(HERE))
    import lpbf_low as M
    parts = M.build(include_tray=True, fasteners=False)
    P = M.P
    ch = (-P["cx"], P["cx"], -P["cy"], P["cy"], -P["floor"], P["lid_z1"])
    rows = []
    for p in parts:
        st, why = _status(p.name)
        if st == "design":
            continue
        b = p.shape.BoundingBox()
        dx = max(ch[0] - b.xmax, b.xmin - ch[1], 0.0)
        dy = max(ch[2] - b.ymax, b.ymin - ch[3], 0.0)
        dz = max(ch[4] - b.zmax, b.zmin - ch[5], 0.0)
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        tier = "A" if (dist <= 100.0 or p.group) else ("B" if p.module == "process" else ("C" if p.module == "gas" else "D"))
        rows.append(dict(name=p.name, bom=p.bom, module=p.module, group=p.group, status=st, real=why,
                         ext=f"{b.xlen:.0f} x {b.ylen:.0f} x {b.zlen:.0f}", bbox_l=round(b.xlen * b.ylen * b.zlen / 1e6, 3),
                         dist_mm=round(dist, 0), tier=tier))
    rows.sort(key=lambda r: (r["tier"], -r["bbox_l"]))
    for k, r in enumerate(rows, 1):
        r["rank"] = k
    OUT.mkdir(parents=True, exist_ok=True)
    import csv
    with open(OUT / "inventory.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rank", "tier", "name", "status", "real", "bom", "module", "group", "ext", "bbox_l", "dist_mm"])
        w.writeheader()
        w.writerows(rows)
    lines = ["# Bought parts drawn as envelopes or generic shapes in `lpbf_low.build()`", "",
             "Written by `cad/vendor_parts.py inventory`. Tier A: within 100 mm of the chamber or moving; B: rest of the process",
             "module (optics bridge, guard); C: gas module; D: rack and tray. Ranked by tier, then by bounding-box volume.",
             "Status: **done** = a real-part builder is in `vendor_parts.py`; env = still an envelope or generic shape; checked =",
             "already drawn to the vendor's CAD.", "",
             "| Rank | Tier | Part | Status | Real part / why not | BOM | Size (mm) | Box (L) | To chamber (mm) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['rank']} | {r['tier']} | {r['name']} | {'**done**' if r['status'] == 'done' else r['status']} | {r['real']} | {r['bom']} | {r['ext']} | {r['bbox_l']} | {r['dist_mm']:.0f} |")
    (OUT / "inventory.md").write_text("\n".join(lines) + "\n")
    print(len(rows), "bought parts;", sum(r["status"] == "done" for r in rows), "replaced")


def _load_step(path):
    vals = cq.importers.importStep(str(path)).vals()
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)


def _ext(s):
    b = s.BoundingBox()
    return sorted([round(b.xlen, 2), round(b.ylen, 2), round(b.zlen, 2)])


def verify(keys=None):
    """Volume and sorted bbox extents of our shapes against the vendor CAD in /tmp (where it exists)."""
    ours = {"mcm_6709K12": mcm_6709K12, "mcm_4566N401": mcm_4566N401, "mcm_6627T91": mcm_6627T91,
            "mcm_5786N23": lambda: kf_weld_stub(25), "mcm_5786N25": lambda: kf_weld_stub(40),
            "mcm_4518K72": lambda: kf_wing_clamp(25), "mcm_4518K73": lambda: kf_wing_clamp(40),
            "mcm_4123K45": lambda: mcm_4123K45("-x"), "mcm_3861N11": mcm_3861N11, "mcm_5169K72": mcm_5169K72,
            "clearpath_sd_231x": clearpath_sd_231x, "mcm_4396K21": mcm_4396K21, "thorlabs_fth160_1064": thorlabs_fth160_1064,
            "scanlab_basicube20": scanlab_basicube20, "ipg_collimator_d5": ipg_collimator_d5, "ipg_ylr500_u3": ipg_ylr500_u3,
            "eaton_5px1500rtg2": eaton_5px1500rtg2, "mcm_6709K33": lambda: mcm_6709K33(260.0)}
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "verify.json"                       # merge into earlier results, keyed by builder
    res = [r for r in (json.loads(f.read_text()) if f.exists() else []) if not keys or r["key"] not in keys]
    for k, fn in ours.items():
        if keys and k not in keys:
            continue
        s = fn()
        r = dict(key=k, pn=SOURCES[k]["pn"], ours_mm3=round(s.Volume(), 1), ours_ext=_ext(s), vendor_mm3=None, vendor_ext=None)
        cad = SOURCES[k]["cad"]
        if cad and pathlib.Path(cad).exists():
            try:
                v = _load_step(cad)
                r["vendor_mm3"], r["vendor_ext"] = round(v.Volume(), 1), _ext(v)
                if k == "mcm_3861N11":      # drop the coiled 36 in. lead (the solid that reaches furthest)
                    sol = sorted(v.Solids(), key=lambda q: -max(q.BoundingBox().xlen, q.BoundingBox().ylen, q.BoundingBox().zlen))
                    rest = cq.Compound.makeCompound(sol[1:])
                    r["vendor_note"] = f"without the coiled lead: {rest.Volume():.0f} mm3, extents {_ext(rest)}"
                r["dvol_pct"] = round(100.0 * (r["ours_mm3"] - r["vendor_mm3"]) / r["vendor_mm3"], 1)
                r["dext_max_mm"] = round(max(abs(a - b) for a, b in zip(r["ours_ext"], r["vendor_ext"])), 2)
            except Exception as e:     # report and carry on
                r["vendor_note"] = f"{type(e).__name__}: {e}"
        res.append(r)
        print(json.dumps(r), flush=True)
        f.write_text(json.dumps(sorted(res, key=lambda q: q["key"]), indent=1))
    return res


def swapcheck(skip=()):
    """Swap each builder into build() and intersect it (exact OCC boolean) with every part whose box it touches."""
    sys.path.insert(0, str(HERE))
    import lpbf_low as M
    parts = M.build(include_tray=True, fasteners=True)
    res = []
    OUT.mkdir(parents=True, exist_ok=True)
    for sw in swaps(M):
        if any(s in sw["replaces"][0] for s in skip):
            continue
        new = sw["shape"]
        nb = new.BoundingBox()
        old = [p for p in parts if any(p.name.startswith(n) for n in sw["replaces"])]
        hits, old_hits = [], []
        for p in parts:
            if any(p.name.startswith(n) for n in sw["replaces"]) or "context" in p.tags:
                continue
            pb = p.shape.BoundingBox()
            if pb.xmin > nb.xmax or pb.xmax < nb.xmin or pb.ymin > nb.ymax or pb.ymax < nb.ymin or pb.zmin > nb.zmax or pb.zmax < nb.zmin:
                continue
            try:
                v = new.intersect(p.shape).Volume()
            except Exception as e:
                v = float("nan")
            if v > 0.5 or v != v:
                ov = sum(o.shape.intersect(p.shape).Volume() for o in old) if old else 0.0
                hits.append(dict(part=p.name, mm3=round(v, 1), envelope_mm3=round(ov, 1)))
        ob = old[0].shape.BoundingBox() if old else None
        r = dict(replaces=sw["replaces"][0], found=bool(old), line=sw["line"], note=sw["note"],
                 new_bbox=[round(x, 1) for x in (nb.xmin, nb.xmax, nb.ymin, nb.ymax, nb.zmin, nb.zmax)],
                 old_bbox=[round(x, 1) for x in (ob.xmin, ob.xmax, ob.ymin, ob.ymax, ob.zmin, ob.zmax)] if ob else None,
                 hits=hits)
        res.append(r)
        print(json.dumps(r), flush=True)
        (OUT / "swapcheck.json").write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if cmd == "inventory":
        inventory()
    elif cmd == "verify":
        verify(sys.argv[2:] or None)
    elif cmd == "swapcheck":
        swapcheck()
