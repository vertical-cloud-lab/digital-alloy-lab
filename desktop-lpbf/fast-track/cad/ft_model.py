"""Parametric CadQuery model of the fast-track machines (FT-0, FT-1, FT-1V) and the states between them (#260).

One model, five states, in the order the parts arrive (``STATES``):

  S1     optics bench: laser, scan head, lens and RTC4 (or RTC5) on the T-slot frame, guide laser onto a target
  S2     the stainless box closed round the beam: window, beam tube, interlocks; full power into a water-cooled dump
  FT-0   single-track bench: heated plate on a fixed rod in the well block, gas, O2 analyzer; layers spread by hand
  FT-1   purge-box LPBF: the rod goes to a Zaber X-VSR20A under the box, a Zaber X-LSM100B moves a hopper-blade
  FT-1V  the same deck cassette, rod drive and optics moved onto an Ideal Vacuum 12 in cube with a pump-purge kit

Run:  python desktop-lpbf/fast-track/cad/ft_model.py            # builds every state, writes out/ft-*.step
      xvfb-run -a python desktop-lpbf/fast-track/cad/ft_render.py   # renders (img/)
      python desktop-lpbf/fast-track/cad/ft_checks.py               # interference, beam, travel, fit, gas, sight lines

Frame: mm. Origin at the centre of the substrate's top face at the start of a build (the powder plane) in the box
states. +X is the recoat direction, +Y points to the back, +Z up. The bench stays put; in FT-1V the cassette and
the optics sit DZ_CUBE higher, because the cube's floor plate is thicker than the box's sheet floor.

Round 2 (2026-11-27): the bought parts that decide fit are drawn in ft_vendor.py from the makers' STEP files (Zaber
X-VSR20A, X-LSM100B; Thorlabs MTS50/M-Z8) or drawings (SCANLAB hurrySCAN 20/30 housing, LINOS 4401-288-000-20,
Saginaw SCE-16EL1208SSLP). The rest are envelopes from published dimensions or estimates, marked in ``P``. Nothing
here is copied from a vendor CAD file. Every part carries its parts.csv line (L1, M2, E1, ...), an MK number for a part
we make (``MADE``), or a MON number for the monitoring parts (``MON``).

build(state, pz, hx, lid_open=False, piston="zaber", monitoring=True): ``piston="thorlabs"`` draws the PCard route's
MTS50/M-Z8 standing on end in place of the X-VSR20A; ``monitoring=False`` leaves out the MON parts; ``lid_open=True``
(box states) takes the beam tube's centre section off and opens the door by P['door_open_deg'].
"""
from __future__ import annotations

import math
import pathlib
import sys
from dataclasses import dataclass

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "cad"))
sys.path.insert(0, str(HERE))
from lpbf_model import box, comp, cyl, kf_stub, polyline_pipe, tslot, tube  # noqa: E402
import ft_vendor as VEN  # noqa: E402

V = cq.Vector
IN = 25.4

# --------------------------------------------------------------------------------------------------
# Parameters. Sources: vendor STEP/drawing (measured 2026-11-27, see ft_vendor.SOURCES), datasheet, study
# (fast_track.py / README), or "est." (estimate).
# --------------------------------------------------------------------------------------------------
P = dict(
    # --- the well and the plate (study; plate redrawn here, see MADE MK-04) ---
    deck_t=10.0,                 # 6061 deck plate (study)
    so_l=12.7, so_d=6.35,        # Macor standoffs under the well block (study: McMaster 8489K75 class)
    so_xy=33.0,                  # standoff positions (+-33, +-33), clear of the overflow cup
    well=(80.0, 80.0, 40.0),     # 6061 well block (study)
    bore=40.00, plate_d=39.80,   # 0.1 mm radial clearance, same alloy at the same temperature (study)
    sub_t=6.0,                   # substrate disc (study)
    hp_t=24.0,                   # heater plate: 21 mm heater holes from below + a 3 mm web (was 28 for 1 in. heaters)
    heater_d=6.0, heater_l=20.0, heater_hole=(6.1, 21.0),   # 3D-printer cartridges, Ø6 x 20, 24 V 50 W (LulzBot KT-CP0013 class)
    blk_heaters=((-30.0, -15.0, 15.0, 30.0)),               # 4 in the well block from its -x face, at these y (this model)
    heater_r=11.5,               # plate heater pitch radius: clear of the rod socket and of the rope groove
    spreader=(48.0, 12.0, 30.0), # FT-0 spreader bar (width in y, thickness, height): fits the 54 mm between nozzle and collector
    rod_od=12.7, rod_wall=0.89,  # 1/2 in. thin-wall 304 tube: rod, thermal break and wire duct (this model)
    socket=8.0,                  # rod socket depth in the heater plate
    lead_groove=(3.0, 2.5),      # lead grooves in the plate's underside, heater/TC hole -> socket (width, depth)
    plug_l=15.0,                 # potted plug (vacuum epoxy) in the rod's lower end (this model)
    rope=3.0,                    # fibreglass rope wiper groove (study), square
    pz_top=5.0, pz_bot=-15.0,    # plate travel: +5 lifted for removal, -15 at the end of a 15 mm build (20 mm)
    # --- recoater: Zaber X-LSM100B-E03 (STEP of the X-LSM100A-E03: 239.2 x 45 x 21.0; 101.6 mm travel, datasheet) ---
    rc_stage="X-LSM100B-E03", rc_travel=101.6, rc_x0=5.0, rc_y=82.0, rc_w=45.0, rc_h=21.0,
    hopper=(20.0, 46.0, 35.0),   # 20 x 46 mm hopper, ~30 cm3 (this model; the study's was ~30 cm3 too)
    cord_d=3.0,                  # silicone cord blade (study, after Heriot-Watt)
    hx_default=37.5,             # hopper parked at the right while lasing (the right park is +35.5, ft_checks)
    # --- gas on the well block top (study: 45 x 4 mm slot at 2.5 m/s) ---
    nozzle_slot=(45.0, 4.0), ovf_x=(22.0, 29.0), ovf_y=22.0,
    # --- deck cassette: 245 mm so it needs a cube face opening of >= 247 mm (the opening is not published) ---
    deck=(245.0, 245.0), deck_c=(-28.0, 45.0),
    # --- the box: Saginaw SCE-16EL1208SSLP, 16 x 12 x 8 in. outside, 0.075 in. 304 (drawing; see ft_vendor.SAG) ---
    box_out=(16 * IN, 12 * IN, 8 * IN), box_t=0.075 * IN,
    # --- the cube: Ideal Vacuum 12 in. (route-catalogue-chambers.csv: plate 301.8 x 301.8 x 22.9 incl. a 7.6 boss;
    #     11.4 in. plate to plate inside). Face opening: est. 266 (vendor site blocked 2026-11-27) ---
    cube_frame=12 * IN, cube_plate=301.8, cube_plate_t=22.9, cube_boss=7.6, cube_open=266.0,
    # --- the piston stage: Zaber X-VSR20A-E01 (STEP: 88 x 101 x 73 retracted, 64 x 64 platform; 20 mm travel) ---
    vs_h=73.0, vs_travel=20.0, vs_foot=(88.0, 101.0), vs_plat=(64.0, 64.0, 7.0),
    blk_h=40.0, rod_end_z=18.0, gap_top=3.0,   # rod-end block (MK-15): height, rod end above its base, gap to the gland
    gland_t=12.0,
    # --- optics: LINOS 4401-288-000-20 (datasheet: WD 296.2, FFL 344.8, Ø118/119.8); hurrySCAN (20/30 drawing) ---
    lens_wd=299.5, lens_ffl=348.1, lens_d=119.8, lens_l=48.6, efl=254.4,   # datasheet WD 296.2 / FFL 344.8 + 3.27 mm
                                 # focus shift from the window (9.53) and cover slide (1.0) in the beam (process worker)
    head=(206.9, 140.0, 180.0), head_obj_x=57.3, head_side=(84.9, 55.1), head_disp=30.4, head_in_z=43.5,
    pivot=348.1 + 20.5 + 24.3,   # chief-ray pivot: the lens nose top + the mean of its recommended mirror distances (est.;
                                 # the process worker's range is 296-424 mm above the focus)
    axis_off=(0.0, -30.0),       # lens axis 30 mm in front of the plate centre: no specular return into the fibre core
                                 # (process worker, 2026-11-27); the head, lens, input stack and collar follow it
    win_c={"box": (0.0, -11.0), "cube": (0.0, -21.0)},   # window stack centres: where the scanned cone crosses them
    tube_c={"box": (0.0, -17.0), "cube": (0.0, -24.0)},  # beam-tube centre section (Ø54 bore) centres
    tube_spigot=(26.5, 3.0),     # outer radius and height of the locating spigots inside the section's ends (this model)
    cs_id=44.0,                  # cover-slide holder opening (was 40): needs Ø41.6 (box), Ø43.4 (cube)
    cs_z=130.0, cs_c=(0.0, -11.0),  # cover slide's lower face above the bed, and its centre, in the box and the cube
    cs_drop_c=(0.0, -16.0),      # FT-1V drop tube axis: between the window (y -21) and the slide holder (y -11)
    window_d=50.8, window_t=9.53, beam_d=5.0, field_d=40.0,
    # --- frame: 30 mm T-slot (McMaster 5537T101 class, study) ---
    bench_z=-272.6,               # bench top: leaves a 10 mm riser under the X-VSR20A
    rail_dy=5.25 * IN,            # support rails at the box's mounting holes (10.50 in. apart)
    # --- monitoring (MON parts; positions chosen here, checked in ft_checks) ---
    cam_xy=(-70.0, -55.0),        # layer camera port, front-left of the window stack (upstream of the plume)
    cam_f=(16.0, 25.0),           # C-mount lens focal length in the box, in the cube
    light_el=(15.0, 30.0),        # raking lights: from -x at 15 deg, from -y at 30 deg (over the nozzle)
    door_open_deg=24.0,           # box door opened this far for build(lid_open=True): free angle with the camera on it
)
P["bed_floor"] = P["deck_t"] + P["so_l"] + P["well"][2]        # 62.7: powder plane above the enclosure floor
P["box_in"] = (P["box_out"][0] - 2 * P["box_t"], P["box_out"][1] - 2 * P["box_t"], VEN.SAG["usable"])
P["dz_cube"] = P["cube_plate_t"] - P["box_t"]                    # 21.0: the cube's floor is this much thicker
P["cube_in"] = P["cube_frame"] - 2 * P["cube_boss"]              # 289.6 plate to plate inside
P["lens_l"] = P["lens_ffl"] - P["lens_wd"]                       # 48.6 below the head's bottom face
P["box_t_old"] = 1.9

C = dict(
    tslot="#c3c9cf", alu="#b9c0c7", alu_dark="#8e979f", ss="#a8b1b9", ss_dark="#7d868e", macor="#efe6cf",
    hot="#e8894a", sub="#d0d4d8", zaber="#2a2f36", zaber_top="#596470", black="#151719", glass="#9fd3ff",
    head="#3b4046", lens="#5d6268", laser="#e6e8ea", fiber="#f08c1a", rubber="#3a3a3a", silicone="#d4553b",
    pcb="#2f7d4f", red="#d22b2b", yellow="#f0c419", green="#2bb24c", blue="#2b6cd2", wood="#c8b28a",
    hose="#7f8890", white="#f2f2f2", cube="#b4bcc4", powder="#8b8d8f", copper="#c87533", target="#30343a",
    water="#3d8fd1", gas="#6cb6e0", thor="#1d1f22", epoxy="#2b2420", mon="#8a4fbf", cable="#202326",
)


@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: str
    pid: str = ""            # parts.csv line, MK-nn for a part we make, MONn for a monitoring part, "" for context
    sub: str = ""            # optics | frame | enclosure | cassette | drive | recoater | gas | safety | bench | monitoring
    group: str = ""          # moving group: "piston" or "recoater"
    opacity: float = 1.0


# Parts we make (MK numbers): what each is, from what, and in which states it exists.
MADE = {
    "MK-01": "deck plate, 245 x 245 x 10 mm 6061: carries the whole cassette from box to cube",
    "MK-02": "window ring, retaining flange with the beam tube's lower spigot, (box only) inner clamp ring, 6061; "
             "cover-slide holder (Ø44) and, in the cube, its drop tube",
    "MK-03": "well block, 80 x 80 x 40 mm 6061, Ø40.00 bore, four Ø6.1 x 21 heater holes and a TC hole from -x, overflow slot",
    "MK-04": "heater plate, Ø39.8 x 24 mm 6061, two Ø6.1 x 21 axial heater holes, TC hole, lead grooves, rod socket, rope groove",
    "MK-05": "substrate discs, Ø39.8 x 6 mm 6061, three M2 countersunk screws at r = 17.1 mm",
    "MK-06": "piston rods, 1/2 in. thin-wall 304 tube with a potted lead plug: one for the box, one 21 mm longer for the cube",
    "MK-07": "rod gland plate, two O-rings (rated for rough vacuum so it moves to the cube unchanged), 4 x M5",
    "MK-08": "hopper (bent 304), cord clamp, arm and carriage bracket",
    "MK-09": "scan-head flange plate, 12 mm 6061: bolts to the head's entrance face, hangs from the gantry cross-beam",
    "MK-10": "beam tube: lens collar (floor ring, Ø50 spigot) and a centre section split in two half-shells with 2 toggle "
             "clamps: long (box), short (cube)",
    "MK-11": "slot nozzle and exhaust collector, 304",
    "MK-12": "stage shield, bent 304 sheet with a slot for the carriage bracket",
    "MK-13": "cube top plate: Ideal Vacuum blank P108171 bored for the window ring and the camera port",
    "MK-14": "cube bottom plate: blank bored for the rod gland, tapped for the deck and the gland",
    "MK-15": "piston-stage bracket plate, riser and rod-end block (clamp, lead pocket, AE face)",
    "MK-16": "overflow cup, 304",
    "MK-17": "FT-0 rod collar and lead terminal bracket (hold the plate at the powder plane until the stage arrives)",
    "MK-18": "guide-laser target stand (S1), anodised 6061",
    "MK-19": "camera port: window ring with a Ø1 in. window and a cover slide (box door; cube top plate bore)",
    "MK-20": "camera post, clamp and Scheimpflug wedge (2.9 deg box, 1.9 deg cube)",
    "MK-21": "light ports: window rings on the box's left and front walls; bores in the cube's left plate and door",
    "MK-22": "coaxial branch adapter: cage-cube plate on the head flange, collimator saddle",
    "MK-23": "deck clamps (4) on the box's panel studs",
}

# Monitoring parts (MON numbers; product suggestions, prices for the lead to read). first = first state that has it.
MON = {
    "MON1": dict(first="FT-0", what="layer camera: Raspberry Pi HQ Camera (IMX477, C/CS mount) + 16 mm C-mount lens "
                 "(+ 25 mm for FT-1V), Thorlabs FESH1000 short-pass in front, Pi 5 camera cable; through MK-19"),
    "MON2": dict(first="FT-0", what="raking light from -x at 15 deg: Thorlabs mounted white LED (MCWHL7 class) + SM1 "
                 "tube with an aspheric condenser (ACL2520U class) + LEDD1B driver (TTL, fired in turn by the Pi)"),
    "MON3": dict(first="FT-0", what="raking light from -y at 30 deg over the nozzle: as MON2"),
    "MON4": dict(first="S1", what="coaxial photodiode: a short-pass dichroic (DMSP1000 class, cut to the head's input "
                 "mirror) in place of the hurrySCAN's 45 deg input mirror, so it still folds the 1070 nm beam into the "
                 "head and passes 400-1000 nm straight back out of the mirror block's back port; there an SM1 tube "
                 "with FESH1000 + bandpass + AC254-050-B + 500 um pinhole, and a PDA36A2. Fitted at S1 because it is in "
                 "the beam path and is aligned once; the photodiode is used from FT-0. Check the dichroic's CW damage "
                 "threshold at 2 kW/cm2 (400 W in 5 mm)"),
    "MON5": dict(first="FT-1", what="acoustic emission: a resonant 150 kHz sensor with integrated preamp (MISTRAS "
                 "R15I-AST or Vallen VS150-RIC class) on the rod-end block, couplant, 28 V decoupler to the digitizer"),
    "MON6": dict(first="S2", what="thermocouples: beam tube and window ring (S2, self-adhesive type K patches); plate, "
                 "well block (1/16 in. sheathed type K in their holes) and box air (1/16 in. probe through a "
                 "compression fitting) from FT-0"),
    "MON7": dict(first="FT-0", what="RTC4 (or RTC5) sync (no geometry): laser gate and a job-list layer/trigger bit "
                 "from the card's I/O to the digitizer and the Pi through an isolator"),
    "MON8": dict(first="FT-0", what="digitizer: PicoScope 4444 class, 4 differential channels (photodiode, AE, laser "
                 "gate, layer sync)"),
    "MON9": dict(first="S2", what="thermocouple logger: MCC 134 class 4-channel HAT on the Pi (C2); no geometry"),
}

STATES = ("S1", "S2", "FT-0", "FT-1", "FT-1V")
TITLES = {
    "S1": "S1  optics bench: guide-laser and scanner checks",
    "S2": "S2  box closed round the beam: full power into a dump (Class 1)",
    "FT-0": "FT-0  single-track bench: heated plate, argon, hand-spread layers",
    "FT-1": "FT-1  purge-box LPBF: piston stage under the box, hopper-blade inside",
    "FT-1V": "FT-1V  the same cassette in a 12 in. vacuum cube, pump-purge",
}


# --------------------------------------------------------------------------------------------------
# Derived geometry
# --------------------------------------------------------------------------------------------------
def levels(state):
    """z levels for a state, in the world (bench-fixed) frame."""
    cube = state == "FT-1V"
    dz = P["dz_cube"] if cube else 0.0
    bf = P["bed_floor"]
    L = dict(dz=dz, cube=cube)
    L["floor_top"] = -bf + dz                                    # enclosure inside floor = deck underside
    L["deck_top"] = L["floor_top"] + P["deck_t"]
    L["under"] = -bf - P["box_t"]                                # enclosure underside (same in both: see dz_cube)
    L["gland_bot"] = L["under"] - P["gland_t"]
    if cube:
        c0 = L["floor_top"] - P["cube_boss"] + P["cube_frame"] / 2  # cube centre: boss top = floor_top
        L["cube_c"] = c0
        L["roof_in"] = c0 + P["cube_frame"] / 2 - P["cube_boss"]  # top plate boss underside
        L["roof_out"] = L["roof_in"] + P["cube_plate_t"]
        L["rim"] = L["roof_in"]
    else:
        L["rim"] = L["floor_top"] + VEN.SAG["out"][2] - P["box_t"]  # body rim (the gasket lands here)
        L["roof_in"] = L["floor_top"] + VEN.SAG["usable"]         # the door's inner face (usable depth 8.30 in.)
        L["roof_out"] = L["roof_in"] + P["box_t"]
    L["lens_bot"] = P["lens_wd"] + dz
    L["lens_top"] = P["lens_ffl"] + dz                            # the lens's flange A = the head's bottom face
    L["head_bot"] = L["lens_top"]
    # the rod: at the top of the stroke the rod-end block stops gap_top under the gland (cassette frame -> world)
    gland_bot_c = L["gland_bot"] - dz
    plate_bot_top = P["pz_top"] - P["sub_t"] - P["hp_t"]
    rod_bot_top = gland_bot_c - P["gap_top"] - (P["blk_h"] - P["rod_end_z"])
    L["rod_vis"] = plate_bot_top - rod_bot_top                    # rod length below the heater plate
    return L


def beam_centre(z_rel):
    """Centre of the scanned-beam envelope at height z_rel: the chief rays run from the pivot on the lens axis
    (axis_off) to the Ø40 field centred on the plate, so the envelope's centre moves from the plate centre (z = 0)
    to the lens axis (z = pivot)."""
    dx, dy = P["axis_off"]
    f = z_rel / P["pivot"]
    return (dx * f, dy * f)


def beam_radius(z_rel):
    """Half-width of the scanned-beam envelope at height z_rel above the powder plane: the chief ray to the Ø40 field
    pivots at the scan mirrors (P['pivot'], est. from the lens's recommended mirror distances), plus the converging
    beam's own half-width (beam_d over the EFL)."""
    pivot = P["pivot"]
    chief = P["field_d"] / 2 * (pivot - z_rel) / pivot
    return chief + P["beam_d"] / 2 * z_rel / P["efl"] + 0.1


def beam_cone(state, z0=0.0, z1=None):
    """The scanned-beam envelope from z0 to z1 above the powder plane: coaxial cone, or an oblique (lofted) one when
    the lens axis is offset."""
    L = levels(state)
    z1 = P["lens_wd"] if z1 is None else z1
    r0, r1 = beam_radius(z0), beam_radius(z1)
    c0, c1 = beam_centre(z0), beam_centre(z1)
    if max(abs(c) for c in c0 + c1) < 1e-9:
        return cq.Solid.makeCone(r0, r1, z1 - z0, V(0, 0, z0 + L["dz"]), V(0, 0, 1))
    w0 = cq.Wire.makeCircle(r0, V(c0[0], c0[1], z0 + L["dz"]), V(0, 0, 1))
    w1 = cq.Wire.makeCircle(r1, V(c1[0], c1[1], z1 + L["dz"]), V(0, 0, 1))
    return cq.Solid.makeLoft([w0, w1], True)


def _unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _place_axis(shape, origin, u):
    """Place a shape built with its axis along local +z at origin, local +z -> u (unit)."""
    ux, uy, uz = u
    xd = (-uy, ux, 0.0) if abs(uz) < 0.999 else (1.0, 0.0, 0.0)
    xd = _unit(xd)
    return shape.moved(cq.Location(cq.Plane(origin=V(*origin), xDir=V(*xd), normal=V(*u))))


def window_centre(state):
    """(x, y) of the window stack (window ring, flange, window, inner clamp ring, bore, cover-slide holder and slide):
    the process worker's centres, where the scanned cone crosses those heights (checked in ft_checks)."""
    return P["win_c"]["cube" if state == "FT-1V" else "box"]


def tube_centre(state):
    """(x, y) of the beam tube's centre section."""
    return P["tube_c"]["cube" if state == "FT-1V" else "box"]


def camera_geometry(state):
    """Layer camera: window centre, unit axis toward the camera, tilt off vertical, distance to the plate centre,
    focal length, magnification, um/px and the Scheimpflug angle (IMX477: 4056 x 3040 px of 1.55 um)."""
    L = levels(state)
    cx, cy = P["cam_xy"]
    zw = L["roof_out"] if state != "FT-1V" else L["roof_out"]
    W = (cx, cy, zw)
    bed = (0.0, 0.0, L["dz"])
    d = (W[0] - bed[0], W[1] - bed[1], W[2] - bed[2])
    u = _unit(d)
    dist = math.sqrt(sum(c * c for c in d)) + 25.0                 # entrance pupil ~25 mm above the window (est.)
    f = P["cam_f"][1] if state == "FT-1V" else P["cam_f"][0]
    m = f / (dist - f)
    tilt = math.degrees(math.acos(u[2]))
    px = 1.55e-3 / m * 1000                                         # um per pixel at the plate, across the tilt
    sch = math.degrees(math.atan(m * math.tan(math.radians(tilt))))
    return dict(W=W, u=u, tilt_deg=tilt, dist_mm=dist, f_mm=f, m=m, um_px_across=px,
                um_px_along=px / math.cos(math.radians(tilt)), field_mm=(6.287 / m, 4.712 / m), scheimpflug_deg=sch)


# --------------------------------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------------------------------
def build(state="FT-1", pz=0.0, hx=None, lid_open=False, piston="zaber", monitoring=True):
    """Parts for a state. pz: substrate top (0 = start of a build); hx: hopper centre x (None = parked at the right,
    P['hx_default']). piston: 'zaber' (X-VSR20A) or 'thorlabs' (MTS50/M-Z8 on end). monitoring: draw the MON parts."""
    assert state in STATES, state
    assert piston in ("zaber", "thorlabs"), piston
    L = levels(state)
    dz = L["dz"]
    i_state = STATES.index(state)
    has_box = state in ("S2", "FT-0", "FT-1")
    has_cassette = i_state >= STATES.index("FT-0")
    has_stages = state in ("FT-1", "FT-1V")
    cube = state == "FT-1V"
    if not has_stages:
        pz = 0.0
    hx = P["hx_default"] if hx is None else hx
    parts: list[Part] = []

    def add(name, shape, color, pid="", sub="", group="", opacity=1.0):
        if shape is not None:
            parts.append(Part(name, shape, color, pid, sub, group, opacity))

    def mon(i):
        return monitoring and i_state >= STATES.index(MON[i]["first"])

    xc, yc = P["deck_c"]
    zb = P["bench_z"]
    h = 15.0                                          # half T-slot
    zbed = dz                                         # powder plane (world)
    wx, wy = window_centre(state)                     # window stack centred on the beam footprint at its height

    # ---------------- bench and frame (S1 on) ----------------
    add("Bench top", box(-860, 640, -360, 430, zb - 40, zb), C["wood"], "", "bench", opacity=1.0)
    ry = (yc - P["rail_dy"], yc + P["rail_dy"])       # rails along X, under the box's mounting holes
    ux = (xc - 260.0, xc + 260.0)                     # gantry upright centres
    z_rail_top = L["under"]                           # support rails carry the enclosure (same height for both)
    frame = []
    for y in ry:
        frame.append(tslot((xc - 290, y, zb + h), "x", 580))              # base rails
        frame.append(tslot((xc - 290, y, z_rail_top - h), "x", 580))      # support rails
    for x in (xc - 275, xc + 275):
        frame.append(tslot((x, ry[0] + h, zb + h), "y", ry[1] - ry[0] - 2 * h))
        for y in ry:
            frame.append(tslot((x, y, zb + 2 * h), "z", z_rail_top - zb - 4 * h))
    add("T-slot base and support rails", comp(frame), C["tslot"], "E4", "frame")
    hb = L["head_bot"]
    z_beam = hb + 90.0                                # cross-beam centre: the head flange plate bolts to its front face
    z_beam_max = P["lens_ffl"] + P["dz_cube"] + 90.0
    z_up_top = z_beam_max + h + 10.0
    ups = [tslot((x, ry[1], z_rail_top), "z", z_up_top - z_rail_top) for x in ux]
    add("Gantry uprights", comp(ups), C["tslot"], "E4", "frame")
    add("Gantry cross-beam (clamped at the head height)", tslot((ux[0] + h, ry[1], z_beam), "x", ux[1] - ux[0] - 2 * h),
        C["tslot"], "E4", "frame")

    # ---------------- optics (S1 on): hurrySCAN hung by its entrance face, LINOS lens, coax cube, collimator, laser ----
    lax, lay = P["axis_off"]                          # lens axis (x, y)
    AX = V(lax, lay, hb)
    hd = VEN.scanlab_hurryscan25().translate(AX)
    add("SCANLAB hurrySCAN 25 (20/30 housing, drawing)", hd, C["head"], "L3", "optics")
    add("LINOS F-Theta-Ronar f = 254 mm (datasheet)", VEN.linos_ftheta_254().translate(AX), C["lens"], "L4",
        "optics")
    xe = lax - P["head_obj_x"]                        # entrance face
    y_in, z_in = lay - P["head_disp"], hb + P["head_in_z"]   # input beam axis (est.)
    fl_x0, fl_x1 = xe - 12.0, xe
    fl = box(fl_x0, fl_x1, lay - P["head_side"][0], ry[1] - h, hb + 5, hb + 125)
    fl = fl.cut(cyl(26.0, (fl_x0 - 1, y_in, z_in), "x", 14))                  # the input turret passes through
    add("Scan-head flange plate (MK-09)", fl, C["alu"], "MK-09", "optics")
    ang = [box(fl_x0 - 40, fl_x0, ry[1] - h - 40, ry[1] - h, z_beam - 15, z_beam - 11),
           box(fl_x0 - 4, fl_x0, ry[1] - h - 40, ry[1] - h, z_beam - 15, z_beam + 15),
           box(fl_x0 - 40, fl_x0 - 36, ry[1] - h - 4, ry[1] - h, z_beam - 15, z_beam + 15)]
    add("Flange-to-beam angle brackets (MK-09)", comp(ang), C["alu_dark"], "MK-09", "optics")
    # the unit's input stack (by eye from the seller's photos): focusing turret and a 45 deg mirror block; the beam comes
    # in from -y. With a short-pass dichroic in place of the input mirror, the melt-pool light passes straight through
    # the block to the photodiode on its back face (MON4).
    tur, mblk = VEN.hurryscan_input_stack()
    add("hurrySCAN input turret (focusing lens; by eye from listing photos)", tur.translate(AX), C["alu"], "L3",
        "optics")
    add("hurrySCAN 45 deg input-mirror block (goniometer; by eye from listing photos)", mblk.translate(AX),
        C["alu"], "L3", "optics")
    xb1 = xe - VEN.HS_IN["turret"][1]
    xbm = xb1 - VEN.HS_IN["block"][0] / 2                                    # the mirror's x
    xb0 = xb1 - VEN.HS_IN["block"][0]
    yb0 = y_in - VEN.HS_IN["block"][1] / 2
    coll = cyl(20, (xbm, yb0 - 110, z_in), "y", 110)
    add("Collimator (L2 if the fibre has none)", coll, C["ss"], "L2", "optics")
    # IPG YLR-400-SM-EOS: 19 in. rack chassis (seller's label photo), 4U and 600 deep (est.); fibre out of the front
    las = box(-800, -350, -170 + 30, 390 - 30, zb, zb + 177.8).fuse(box(-362, -350, -170, 390, zb, zb + 177.8))
    add("IPG YLR-400-SM-EOS, 19 in. rack chassis (4U, depth est.)", las, C["laser"], "L1", "optics")
    add("Fibre bend restrictor", cyl(9, (-350, 120, zb + 120), "x", 110), C["black"], "L1", "optics")
    fib = polyline_pipe([(-241, 120, zb + 120), (-300, 120, zb + 140), (-300, 120, 300.0 + dz), (-300, -100, z_in - 30),
                         (-240, -230, z_in), (xbm, -230, z_in), (xbm, yb0 - 110, z_in)], 3.0)
    add("Process fibre", fib, C["fiber"], "L1", "optics")
    add("PC with the RTC4 (or RTC5) (tower, est.)", box(420, 590, -20, 400, zb, zb + 380), C["black"], "C1", "bench")
    add("+-15 V supply for the head (DIN, est.)", box(ux[1] - 15 - 60, ux[1] - 15, ry[1] - 15 - 30, ry[1] - 15,
                                                     hb + 10, hb + 100), C["alu_dark"], "L6", "optics")
    ys_ = lay - P["head_side"][0]
    hcab = polyline_pipe([(xe + 22, ys_ - 12.5, hb + 156), (xe + 22, ys_ - 60, hb + 156), (xe + 22, ys_ - 90, hb + 230)], 4.0)
    add("Head cables and hoses (DB-9, DB-25, water, air)", hcab, C["cable"], "L7", "optics")
    if monitoring and mon("MON4"):
        pd = [tube(15.25, 12.7, (xb0 - 55, y_in, z_in), "x", 55),                       # SM1 tube: filters + lens
              box(xb0 - 55 - 23, xb0 - 55, y_in - 25, y_in + 25, z_in - 35.5, z_in + 35.5)]  # PDA36A2 (est. 71 x 50 x 23)
        add("Photodiode branch on the mirror block: FESH1000, bandpass, AC254-050-B, pinhole, PDA36A2 (MON4)", comp(pd),
            C["thor"], "MON4", "monitoring")

    # ---------------- S1: target on the deck plate, the deck on the support rails ----------------
    deck_x0, deck_x1 = xc - P["deck"][0] / 2, xc + P["deck"][0] / 2
    deck_y0, deck_y1 = yc - P["deck"][1] / 2, yc + P["deck"][1] / 2
    deck_z0 = L["floor_top"] if (has_box or cube) else z_rail_top
    deck = box(deck_x0, deck_x1, deck_y0, deck_y1, deck_z0, deck_z0 + P["deck_t"])
    deck = deck.cut(cyl(10.0, (0, 0, deck_z0 - 1), "z", P["deck_t"] + 2))
    deck = deck.cut(box(P["ovf_x"][0] - 2, 62, -26, 26, deck_z0 - 1, deck_z0 + P["deck_t"] + 1))
    for sx in (-1, 1):                                                         # M6 clearance for the cube's deck screws
        for sy in (-1, 1):
            deck = deck.cut(cyl(3.3, (xc + sx * 112.0, yc + sy * 92.1, deck_z0 - 1), "z", P["deck_t"] + 2))
    add("Deck plate (MK-01)", deck, C["alu"], "MK-01", "cassette")
    if state == "S1":
        st = box(-30, 30, -30, 30, deck_z0 + P["deck_t"], -3.0)
        add("Guide-laser target stand (MK-18)", st, C["alu_dark"], "MK-18", "cassette")
        add("Anodised target, 80 x 80 x 3 mm", box(-40, 40, -40, 40, -3.0, 0.0), C["target"], "MK-18", "cassette")
    if state == "S2":
        d = cyl(40, (0, 0, L["deck_top"]), "z", 50).cut(cyl(12, (0, 0, L["deck_top"] + 30), "z", 21))
        add("Water-cooled beam dump, 500 W (Thorlabs LB2L/M class, envelope)", d, C["black"], "L9", "cassette")
        w = polyline_pipe([(30, 25, L["deck_top"] + 25), (90, 60, L["deck_top"] + 20),
                           (xc + P["box_in"][0] / 2 - 5, 60, L["deck_top"] + 20)], 3.0, smooth=True)
        add("Dump water lines", w, C["water"], "L9", "cassette")

    # ---------------- enclosure: the box (S2, FT-0, FT-1): Saginaw SCE-16EL1208SSLP lid-up ----------------
    bx, by, bz = P["box_in"]
    t = P["box_t"]
    x0, x1, y0, y1 = xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2
    cam = camera_geometry(state) if (monitoring and mon("MON1")) else None
    lights = light_geometry(state) if (monitoring and mon("MON2")) else {}
    if has_box:
        z0 = L["floor_top"]
        sag = VEN.saginaw_16el1208sslp()
        T = V(xc, yc, z0)
        body = sag["body"].translate(T)
        body = body.cut(cyl(10.0, (0, 0, z0 - t - 1), "z", t + 2))                      # rod hole
        for gx in (-21.0, 21.0):
            for gy in (-21.0, 21.0):
                body = body.cut(cyl(2.75, (gx, gy, z0 - t - 1), "z", t + 2))            # gland screws (M5)
        for p0, ax in (((x0 - t - 1, -60.0, 4.0), "x"), ((x1 - 1, 47.0, 5.0), "x")):
            body = body.cut(cyl(6.5, p0, ax, t + 2))                                     # gas bulkheads
        for gx, gz in ((-120.0, L["deck_top"] + 20.0), (-85.0, -10.0)):
            body = body.cut(cyl(8.0, (gx, y1 - 1, gz), "y", t + 2))                      # M16 cable glands
        body = body.cut(cyl(3.2, (40.0, y1 - 1, 30.0), "y", t + 2))                      # air TC fitting
        for k, lg in lights.items():                                                     # light ports
            body = body.cut(cyl(14.0, lg["port_in"], lg["n"], t + 2))
        add("Saginaw SCE-16EL1208SSLP 304 box, 16 x 12 x 8 in. (body)", body, C["ss"], "E1", "enclosure", opacity=0.35)
        add("Poured-in-place door gasket", sag["gasket"].translate(T), C["rubber"], "E1", "enclosure")
        door = sag["door"].translate(T).cut(cyl(26.5, (wx, wy, L["roof_in"] - 12), "z", 30))
        if cam:
            door = door.cut(cyl(14.0, (cam["W"][0], cam["W"][1], L["roof_in"] - 12), "z", 30))
        add("Box door (the lid): window bore, camera port", door, C["ss"], "E1", "enclosure", opacity=0.35)
        add("Quarter-turn latch", sag["latch"].translate(T), C["ss_dark"], "E1", "enclosure")
        add("Concealed hinges (2)", sag["hinges"].translate(T), C["ss_dark"], "E1", "enclosure")
        add("Panel studs (4, on the floor)", sag["studs"].translate(T), C["ss_dark"], "E1", "enclosure")
        # deck clamps on the panel studs (no holes through the floor for the deck)
        dcl, nuts = [], []
        sx_, sy_ = VEN.SAG["studs"][0] / 2, VEN.SAG["studs"][1] / 2
        for a in (-1, 1):
            for b_ in (-1, 1):
                xs, ys = xc + a * sx_, yc + b_ * sy_
                xd0 = xc + a * (P["deck"][0] / 2 - 8)
                dcl.append(box(min(xs, xd0) - 6, max(xs, xd0) + 6, ys - 9, ys + 9, L["deck_top"], L["deck_top"] + 4).cut(
                    cyl(2.6, (xs, ys, L["deck_top"] - 1), "z", 6)))
                nuts.append(cyl(4.5, (xs, ys, L["deck_top"] + 4), "z", 3.5))
        add("Deck clamps on the panel studs (MK-23)", comp(dcl), C["alu_dark"], "MK-23", "cassette")
        add("Stud nuts (4)", comp(nuts), C["ss_dark"], "MK-23", "cassette")
        # window stack on the thin door: inner clamp ring under it
        add("Inner clamp ring (MK-02)", tube(50, 22, (wx, wy, L["roof_in"] - 6), "z", 6), C["alu"], "MK-02", "enclosure")
        win_ring_z = L["roof_out"]
    else:
        win_ring_z = L["roof_out"] if cube else None

    # ---------------- enclosure: the cube (FT-1V) ----------------
    if cube:
        F, pt, bs, op = P["cube_frame"], P["cube_plate_t"], P["cube_boss"], P["cube_open"]
        cz = L["cube_c"]
        fr = box(xc - F / 2, xc + F / 2, yc - F / 2, yc + F / 2, cz - F / 2, cz + F / 2)
        for ax in ("x", "y", "z"):
            dx_, dy_, dz_ = ((F + 2, op, op) if ax == "x" else (op, F + 2, op) if ax == "y" else (op, op, F + 2))
            fr = fr.cut(box(xc - dx_ / 2, xc + dx_ / 2, yc - dy_ / 2, yc + dy_ / 2, cz - dz_ / 2, cz + dz_ / 2))
        add("Ideal Vacuum 12 in. cube frame P107540 (face opening est.)", fr, C["cube"], "E2", "enclosure", opacity=0.45)
        pw, bw = P["cube_plate"], op - 2.0

        def plate(axis, sign, name, pid, holes=(), tilted=(), op_=0.45):
            body = box(-pw / 2, pw / 2, -pw / 2, pw / 2, 0, pt - bs).fuse(box(-bw / 2, bw / 2, -bw / 2, bw / 2, -bs, 0))
            for (hx_, hy_, hr) in holes:
                body = body.cut(cyl(hr, (hx_, hy_, -bs - 1), "z", pt + 2))
            # local z = outward normal; boss toward the inside. Place on the face.
            if axis == "z":
                sh = body if sign > 0 else body.rotate(V(0, 0, 0), V(1, 0, 0), 180)
                sh = sh.translate(V(xc, yc, cz + sign * F / 2))
            elif axis == "x":
                sh = body.rotate(V(0, 0, 0), V(0, 1, 0), 90 * sign).translate(V(xc + sign * F / 2, yc, cz))
            else:
                sh = body.rotate(V(0, 0, 0), V(1, 0, 0), -90 * sign).translate(V(xc, yc + sign * F / 2, cz))
            for (p_, u_, r_) in tilted:                                       # bores along a line of sight (world)
                sh = sh.cut(_place_axis(cq.Solid.makeCylinder(r_, 120.0, V(0, 0, -60.0), V(0, 0, 1)), p_, u_))
            add(name, sh, C["cube"], pid, "enclosure", opacity=op_)

        top_tilt = [(cam["W"], cam["u"], 13.0)] if cam else []
        plate("z", +1, "Cube top plate, bored for the window ring and the camera port (MK-13)", "MK-13",
              holes=((wx - xc, wy - yc, 26.5),), tilted=top_tilt)
        plate("z", -1, "Cube bottom plate, bored for the rod gland (MK-14)", "MK-14", holes=((-xc, yc, 10.0),))
        plate("y", -1, "Cube front plate = door (hinge kit P106868), light port", "E2",
              tilted=[(lights["MON3"]["port_in"], lights["MON3"]["u"], 12.0)] if "MON3" in lights else [])
        plate("y", +1, "Cube back plate (KF-25 feedthroughs)", "E2")
        plate("x", -1, "Cube left plate (pump and gauge ports), light port", "E2",
              tilted=[(lights["MON2"]["port_in"], lights["MON2"]["u"], 12.0)] if "MON2" in lights else [])
        plate("x", +1, "Cube right plate (argon in, exhaust, vent)", "E2")
        hinge = cyl(5.0, (xc - pw / 2, yc - F / 2 - (pt - bs) - 6, cz - pw / 2 + 20), "x", pw)
        add("Door hinges (hinge kit)", hinge, C["ss_dark"], "E2", "enclosure")
        kfs = []
        sx = xc - F / 2 - (pt - bs)
        kf_left = ((yc + 25, cz - 60), (yc + 95, cz - 60))                   # moved clear of the MON2 light port
        for (yy, zz) in kf_left:
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(0, 1, 0), -90).translate(V(sx - 30, yy, zz)))
        sx1 = xc + F / 2 + (pt - bs)
        for (yy, zz) in ((yc - 60, cz - 60), (yc + 60, cz - 60)):
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(0, 1, 0), 90).translate(V(sx1 + 30, yy, zz)))
        sy1 = yc + F / 2 + (pt - bs)
        for xx in (xc - 60, xc + 60):
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(1, 0, 0), -90).translate(V(xx, sy1 + 30, cz - 60)))
        add("KF-25 ports: pump, Pirani, argon, exhaust, 2 electrical feedthroughs", comp(kfs), C["ss"], "E3", "enclosure")
        pump = box(-820, -440, -345, -185, zb, zb + 230)
        add("Rotary-vane pump (McMaster 4396K21 class, envelope est.)", pump, C["blue"], "E3", "gas")
        hose = polyline_pipe([(sx - 30, kf_left[0][0], kf_left[0][1]), (sx - 120, kf_left[0][0] - 40, cz - 90),
                              (-470, -250, zb + 250), (-560, -250, zb + 230)], 13.0)
        add("KF-25 pump hose and valve", hose, C["hose"], "E3", "gas")
        # deck screws into the bottom plate (blind tapped)
        dsc = [cyl(5.0, (xc + a * 112.0, yc + b_ * 92.1, L["deck_top"]), "z", 6.0) for a in (-1, 1) for b_ in (-1, 1)]
        add("Deck screws into the bottom plate, M6 (4)", comp(dsc), C["ss_dark"], "MK-14", "cassette")

    # ---------------- window stack (S2 on) ----------------
    if win_ring_z is not None:
        z = win_ring_z
        ring = tube(50, 22, (wx, wy, z), "z", 10).cut(cyl(P["window_d"] / 2 + 0.25, (wx, wy, z + 2), "z", 9))
        add("Window ring (MK-02)", ring, C["alu"], "MK-02", "enclosure")
        add("Window, Ø50.8 x 9.53 fused silica, 1064 V-coat", cyl(P["window_d"] / 2, (wx, wy, z + 2), "z", P["window_t"]),
            C["glass"], "L8", "enclosure", opacity=0.5)
        fl_ = tube(50, 22, (wx, wy, z + 10), "z", 6).cut(cyl(P["window_d"] / 2 + 0.25, (wx, wy, z + 10 - 0.1), "z", 1.8))
        tx, ty = tube_centre(state)                                              # beam tube's centre section (Ø54 bore)
        sp_r, sp_h = P["tube_spigot"]
        fl_ = fl_.fuse(tube(sp_r, sp_r - 1.5, (tx, ty, z + 16), "z", sp_h))         # spigot inside the tube's lower end
        add("Window retaining flange (MK-02)", fl_, C["alu"], "MK-02", "enclosure")
        # M4 flat-head screws countersunk flush in the flange, so the beam tube's half-shells slide off over them
        scr = [cq.Solid.makeCone(2.2, 4.1, 2.3, V(wx + 40 * math.cos(math.radians(60 * k)),
                                                  wy + 40 * math.sin(math.radians(60 * k)), z + 16 - 2.3), V(0, 0, 1))
               for k in range(6)]
        add("Window-stack screws, M4 x 12 flat head, flush", comp(scr), C["ss_dark"], "MK-02", "enclosure")
        # cover slide ~130 mm above the bed in both enclosures (process worker: a sooted slide defocuses ~4x less there
        # than under the cube's top plate), held in a Ø44 ring centred on the beam footprint at that height
        csx, csy = P["cs_c"]
        zs = L["dz"] + P["cs_z"]                                                # slide's lower face
        cs_top = L["roof_in"] - 6.0 if has_box else zs + 10.0
        if cube:
            dtx, dty = P["cs_drop_c"]
            drop = tube(32, 27, (dtx, dty, cs_top), "z", L["roof_in"] - cs_top).fuse(
                tube(45, 27, (dtx, dty, L["roof_in"] - 5), "z", 5))
            add("Cover-slide drop tube from the top plate (MK-02)", drop, C["alu"], "MK-02", "enclosure")
        holder = tube(35, P["cs_id"] / 2, (csx, csy, zs - 4.5), "z", cs_top - (zs - 4.5)).cut(
            cyl(25.3, (csx, csy, zs - 0.1), "z", 1.2))
        holder = holder.cut(box(csx, csx + 40, csy - 25.3, csy + 25.3, zs - 0.1, zs + 1.1))   # slide goes in from +x
        add("Cover-slide holder, Ø44 opening (MK-02)", holder, C["alu"], "MK-02", "enclosure")
        add("Cover slide, Ø50 x 1 mm", cyl(25, (csx, csy, zs), "z", 1.0), C["glass"], "L8", "enclosure", opacity=0.5)
        # beam tube in two parts (fixes round 1's captive tube): a collar clamped on the lens body with a floor ring,
        # and a centre section split lengthwise (in the y-z plane) in two half-shells held by 2 toggle clamps. The
        # section butts on the window flange below and the collar's floor ring above, and both ends overlap a 3 mm
        # spigot INSIDE its bore (light-tight, and nothing outside it), so each half-shell comes off sideways (+-x)
        # with no lift; then the door opens (ft_checks: tube_removal, door_swing)
        t0 = z + 16
        lb = L["lens_bot"]
        col = tube(68, P["lens_d"] / 2 + 0.7, (lax, lay, lb - 4), "z", 34).fuse(
            cyl(68, (lax, lay, lb - 10), "z", 6).cut(cyl(27.0, (tx, ty, lb - 11), "z", 8)))
        col = col.fuse(tube(sp_r, sp_r - 1.5, (tx, ty, lb - 10 - sp_h), "z", sp_h))   # spigot inside the upper end
        add("Beam-tube lens collar, clamped on the lens (MK-10)", col, C["alu_dark"], "MK-10", "enclosure", opacity=0.7)
        cs_len = (lb - 10) - t0
        ctr = tube(30, 27, (tx, ty, t0), "z", cs_len)
        add("Beam tube centre section, split, long (MK-10)" if not cube else "Beam tube centre section, split, short (MK-10)",
            ctr, C["alu_dark"], "MK-10", "enclosure", opacity=0.7)
        add("Beam-tube interlock switch (on the collar; actuator on the centre section)",
            box(lax + 68, lax + 92, lay - 10, lay + 10, lb - 2, lb + 16), C["yellow"], "S1", "safety")
        if monitoring and mon("MON6"):
            tcs = [box(tx + 30.0, tx + 32.0, ty - 6, ty + 6, t0 + 5, t0 + 15), box(wx - 6, wx + 6, wy - 52.0, wy - 50.0, z + 2, z + 8)]
            add("Surface thermocouples: beam tube, window ring (MON6)", comp(tcs), C["mon"], "MON6", "monitoring")

    # ---------------- cassette (FT-0 on) ----------------
    if has_cassette:
        z0 = L["floor_top"] + P["deck_t"]                                  # deck top
        bw_, bd_, bh_ = P["well"]
        zb0 = z0 + P["so_l"]                                               # well block bottom
        sos = [cyl(P["so_d"] / 2, (sx_, sy_, z0), "z", P["so_l"]) for sx_ in (-P["so_xy"], P["so_xy"])
               for sy_ in (-P["so_xy"], P["so_xy"])]
        add("Macor standoffs under the well block (4)", comp(sos), C["macor"], "H4", "cassette")
        blk = box(-bw_ / 2, bw_ / 2, -bd_ / 2, bd_ / 2, zb0, zbed).cut(cyl(P["bore"] / 2, (0, 0, zb0 - 1), "z", bh_ + 2))
        blk = blk.cut(box(P["ovf_x"][0], P["ovf_x"][1], -P["ovf_y"], P["ovf_y"], zb0 - 1, zbed + 1))
        hd_, hdep = P["heater_hole"]
        for sy_ in P["blk_heaters"]:
            blk = blk.cut(cyl(hd_ / 2, (-bw_ / 2 - 1, sy_, zb0 + bh_ / 2), "x", hdep + 1))
        blk = blk.cut(cyl(0.8, (-bw_ / 2 - 1, 0.0, zbed - 8.0), "x", 16))              # TC hole from -x, with the heaters
        add("Well block, Ø40.00 bore (MK-03)", blk, C["hot"], "MK-03", "cassette")
        if has_stages:
            hs = [cyl(P["heater_d"] / 2, (-bw_ / 2 - 0.5, sy_, zb0 + bh_ / 2), "x", P["heater_l"]) for sy_ in P["blk_heaters"]]
            add("Well-block heaters, 4 x Ø6 x 20, 50 W", comp(hs), C["copper"], "H1", "cassette")
        # plate stack: substrate on the heater plate on the rod (moves with pz)
        zt = zbed + pz
        sub = cyl(P["plate_d"] / 2, (0, 0, zt - P["sub_t"]), "z", P["sub_t"])
        for k in range(3):
            a = math.radians(90 + 120 * k)
            p_ = (17.1 * math.cos(a), 17.1 * math.sin(a))
            sub = sub.cut(cyl(1.1, (p_[0], p_[1], zt - P["sub_t"] - 1), "z", P["sub_t"] + 2))
            sub = sub.cut(cq.Solid.makeCone(1.1, 2.1, 1.0, V(p_[0], p_[1], zt - 1.0), V(0, 0, 1)))
        add("Substrate disc Ø39.8 x 6 (MK-05)", sub, C["sub"], "MK-05", "cassette", "piston")
        hp_z0 = zt - P["sub_t"] - P["hp_t"]
        hpl = cyl(P["plate_d"] / 2, (0, 0, hp_z0), "z", P["hp_t"])
        hpl = hpl.cut(tube(P["plate_d"] / 2 + 1, P["plate_d"] / 2 - P["rope"], (0, 0, zt - P["sub_t"] - 7), "z", P["rope"]))
        hpl = hpl.cut(cyl(P["rod_od"] / 2 + 0.05, (0, 0, hp_z0 - 1), "z", P["socket"] + 1))
        gw_, gd_ = P["lead_groove"]
        for k in range(3):
            a = math.radians(30 + 120 * k)
            p_ = (P["heater_r"] * math.cos(a), P["heater_r"] * math.sin(a))
            r_, dep_ = (P["heater_hole"][0] / 2, P["heater_hole"][1]) if k < 2 else (0.8, P["heater_hole"][1])
            hpl = hpl.cut(cyl(r_, (p_[0], p_[1], hp_z0 - 1), "z", dep_ + 1))
            # lead groove from the hole to the socket along the radius, in the underside
            g = box(0, P["heater_r"], -gw_ / 2, gw_ / 2, hp_z0 - 1, hp_z0 + gd_).rotate(V(0, 0, 0), V(0, 0, 1), 30 + 120 * k)
            hpl = hpl.cut(g)
        add(f"Heater plate Ø39.8 x {P['hp_t']:g} (MK-04)", hpl, C["hot"], "MK-04", "cassette", "piston")
        rope = tube(P["plate_d"] / 2 + 0.08, P["plate_d"] / 2 - P["rope"], (0, 0, zt - P["sub_t"] - 7), "z", P["rope"])
        add("Fibreglass rope wiper", rope, C["white"], "H4", "cassette", "piston")
        ph = []
        for k in range(2):
            a = math.radians(30 + 120 * k)
            ph.append(cyl(P["heater_d"] / 2, (P["heater_r"] * math.cos(a), P["heater_r"] * math.sin(a), hp_z0 + 0.5),
                          "z", P["heater_l"]))
        add("Plate heaters, 2 x Ø6 x 20, 50 W", comp(ph), C["copper"], "H1", "cassette", "piston")
        if monitoring and mon("MON6"):
            a = math.radians(270.0)
            tc = cyl(0.79, (P["heater_r"] * math.cos(a), P["heater_r"] * math.sin(a), hp_z0 + 0.5), "z", P["heater_l"])
            add("Plate thermocouple, 1/16 in. type K (MON6)", tc, C["mon"], "MON6", "monitoring", "piston")
            tcb = cyl(0.79, (-bw_ / 2 - 6, 0.0, zbed - 8.0), "x", 21)                     # from the -x face, 15 deep
            add("Well-block thermocouple, 1/16 in. type K (MON6)", tcb, C["mon"], "MON6", "monitoring")
        # rod: thin-wall tube from the socket down through the deck, floor and gland; leads run inside it to a potted plug
        rod_vis = L["rod_vis"]
        rod_top = hp_z0 + P["socket"]
        rod_bot = hp_z0 - rod_vis
        rod = tube(P["rod_od"] / 2, P["rod_od"] / 2 - P["rod_wall"], (0, 0, rod_bot), "z", rod_top - rod_bot)
        for k in range(3):                                                    # lead notches at the rod's top
            rod = rod.cut(box(P["rod_od"] / 2 - 2, P["rod_od"] / 2 + 1, -gw_ / 2, gw_ / 2, hp_z0 - 1, hp_z0 + gd_).rotate(
                V(0, 0, 0), V(0, 0, 1), 30 + 120 * k))
        add("Piston rod, long, for the cube (MK-06)" if cube else "Piston rod (MK-06)", rod, C["ss"], "MK-06", "drive",
            "piston")
        plug = cyl(P["rod_od"] / 2 - P["rod_wall"], (0, 0, rod_bot), "z", P["plug_l"])
        add("Potted lead plug, vacuum epoxy (MK-06)", plug, C["epoxy"], "MK-06", "drive", "piston")
        gl = box(-30, 30, -30, 30, L["gland_bot"], L["under"]).cut(cyl(P["rod_od"] / 2 + 0.1, (0, 0, L["gland_bot"] - 1),
                                                                         "z", P["gland_t"] + 2))
        add("Rod gland plate, 2 O-rings (MK-07)", gl, C["ss_dark"], "MK-07", "drive")
        gsc = [cyl(4.25, (gx, gy, L["gland_bot"]), "z", 5) for gx in (-21.0, 21.0) for gy in (-21.0, 21.0)]   # counterbored
        add("Gland screws M5 x 25 with bonded seals (4)", comp(gsc), C["ss_dark"], "MK-07", "drive")
        if state == "FT-0":
            coll = tube(15, P["rod_od"] / 2, (0, 0, z0), "z", 10).cut(box(-0.75, 0.75, 4, 16, z0 - 1, z0 + 11))
            add("FT-0 rod collar (MK-17)", coll, C["black"], "MK-17", "cassette")
            brk = box(-20, 20, -34, -30, rod_bot - 30, L["gland_bot"]).fuse(box(-20, 20, -54, -34, rod_bot - 30, rod_bot - 26))
            brk = brk.cut(box(-6, 6, -35, -29, rod_bot - 20, rod_bot - 6))                  # pigtail passes through
            add("FT-0 lead terminal bracket (MK-17)", brk, C["alu_dark"], "MK-17", "drive")
            add("Lead terminal block, 6-way pluggable", box(-15, 15, -52, -36, rod_bot - 26, rod_bot - 8), C["green"], "H2",
                "drive")
            pig = polyline_pipe([(0, 0, rod_bot), (0, 0, rod_bot - 8), (0, -20, rod_bot - 12), (0, -38, rod_bot - 14)], 2.5)
            add("Lead pigtail, 4 heater + 2 TC wires", pig, C["cable"], "H3", "drive")
        # overflow cup (in the deck pocket, on the floor)
        cup = box(P["ovf_x"][0] - 0.5, P["ovf_x"][1] + 0.5, -24, 24, L["floor_top"], zb0 - 1.0)
        cup = cup.cut(box(P["ovf_x"][0], P["ovf_x"][1], -23.5, 23.5, L["floor_top"] + 1, zb0))
        add("Overflow cup (MK-16)", cup, C["ss"], "MK-16", "cassette")
        # gas: slot nozzle (front) and exhaust collector (back) on the block top
        sw, sh_ = P["nozzle_slot"]
        nz = box(-27.5, 27.5, -46, -27, zbed, zbed + 8).cut(box(-sw / 2, sw / 2, -28, -26.5, zbed + 2, zbed + 2 + sh_))
        nz = nz.fuse(cyl(5, (0, -46, zbed + 4), "-y", 6))
        add("Slot nozzle 45 x 4 mm (MK-11)", nz, C["ss"], "MK-11", "gas")
        ex = box(-30, 30, 27, 40, zbed, zbed + 10).cut(box(-25, 25, 26.5, 28, zbed + 2, zbed + 8))
        add("Exhaust collector (MK-11)", ex, C["ss"], "MK-11", "gas")
        x_wall_in = x0 if has_box else (xc - P["cube_in"] / 2)
        x_wall_out = x1 if has_box else (xc + P["cube_in"] / 2)
        feed = polyline_pipe([(0, -52, zbed + 4), (0, -60, zbed + 4), (-40, -60, zbed + 4), (x_wall_in + 2, -60, zbed + 4)],
                             3.2, smooth=False)
        add("Argon feed tube to the nozzle", feed, C["gas"], "G3", "gas")
        exh = polyline_pipe([(0, 40, zbed + 5), (0, 47, zbed + 5), (40, 47, zbed + 5), (x_wall_out - 2, 47, zbed + 5)],
                            6.0, smooth=False)
        add("Exhaust hose to the HEPA", exh, C["gas"], "G3", "gas")
        if state == "FT-0":
            # a straight ground bar that rides on the block top between the nozzle and the collector (54 mm apart);
            # the layer depth is set by the plate's recess under the block top (shims under the FT-0 collar)
            sw2, st2, sh2 = P["spreader"]
            app = box(-38, -38 + st2, -sw2 / 2, sw2 / 2, zbed, zbed + sh2 - 8).fuse(
                box(-38 + 2, -38 + st2 - 2, -sw2 / 2 + 4, sw2 / 2 - 4, zbed + sh2 - 8, zbed + sh2))
            add("FT-0 spreader bar, 48 mm, ground edge, parked (M4)", app, C["ss_dark"], "M4", "cassette")
        # well-block heater and TC leads: out along -x, over the stage's motor end, to the back wall / feedthrough
        y_back = (y1 - 2) if has_box else (yc + P["cube_in"] / 2 - 4)
        z_back = -10.0 if has_box else (L["cube_c"] - 60)
        wl = polyline_pipe([(-bw_ / 2 - 2, 0, zb0 + bh_ / 2), (-85, 0, zb0 + bh_ / 2), (-85, 30, zbed - 10),
                            (-85, 150, zbed - 10), (-85, y_back, z_back)], 3.0)
        add("Well-block heater and TC leads", wl, C["cable"], "H3", "cassette")
        if has_box:
            gland = [cyl(11.0, (gx, y1 + t, gz), "y", 10) for gx, gz in ((-120.0, L["deck_top"] + 20.0), (-85.0, -10.0))]
            add("IP68 cable glands M16 (2, back wall)", comp(gland), C["black"], "H3", "enclosure")
        if monitoring and mon("MON6") and has_box:
            add("Box-air thermocouple and fitting (MON6)", cyl(0.79, (40.0, y1 - 60, 30.0), "y", 60).fuse(
                cyl(7.0, (40.0, y1 + t, 30.0), "y", 10)), C["mon"], "MON6", "monitoring")

    # ---------------- recoater (FT-1, FT-1V): Zaber X-LSM100B ----------------
    if has_stages:
        z0 = L["deck_top"]
        yr = P["rc_y"]
        fixed, car = VEN.zaber_x_lsm100(hx - P["rc_x0"], parts=True)
        Tr = V(P["rc_x0"], yr, z0)
        add("Zaber X-LSM100B-E03 recoater stage", fixed.translate(Tr), C["zaber"], "M1c", "recoater")
        add("X-LSM carriage", car.translate(Tr), C["zaber_top"], "M1c", "recoater", "recoater")
        car_top = z0 + P["rc_h"]
        hl, hw_, hh_ = P["hopper"]
        arm_z0 = zbed + hh_ - 8
        foot = box(hx - 20, hx + 20, yr - 22, yr + 18, car_top, car_top + 6)
        upr = box(hx - 20, hx + 20, yr - 22, yr - 14, car_top + 6, arm_z0 + 8)
        arm = box(hx - 8, hx + 8, hw_ / 2, yr - 14, arm_z0, arm_z0 + 8)
        add("Carriage bracket and arm (MK-08)", comp([foot, upr, arm]), C["alu"], "MK-08", "recoater", "recoater")
        x_a, x_b = P["rc_x0"] - 78.0, P["rc_x0"] + 88.0
        sz = car_top + 8
        sh = box(x_a, x_b, yr - 25, yr + 25, sz, sz + 1)
        half = P["rc_travel"] / 2
        sh = sh.cut(box(P["rc_x0"] - half - 22, P["rc_x0"] + half + 22, yr - 24, yr - 12, sz - 1, sz + 2))
        sh = sh.fuse(box(x_a, x_b, yr - 26, yr - 25, z0, sz + 1))
        add("Stage shield (MK-12)", sh, C["ss"], "MK-12", "recoater", opacity=0.55)
        hop = (cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (hl / 2, hh_), (-hl / 2, hh_)]).close()
               .extrude(hw_).val())
        hop = hop.fuse(cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (1.5, 2.0), (-1.5, 2.0)]).close()
                       .extrude(hw_).val())
        hop = hop.cut(box(-hl / 2 + 0.8, hl / 2 - 0.8, -hw_ + 0.8, -0.8, 7, hh_ + 1))
        hop = hop.translate(V(hx, hw_ / 2, zbed))
        add("Hopper, ~30 cm3 (MK-08)", hop, C["ss"], "MK-08", "recoater", "recoater")
        cord = cyl(P["cord_d"] / 2, (hx - hl / 2 - 2.0, -hw_ / 2, zbed + P["cord_d"] / 2), "y", hw_)
        add("Silicone-cord blade, 3 mm", cord, C["silicone"], "M3", "recoater", "recoater")
        clamp = box(hx - hl / 2 - 4, hx - hl / 2, -hw_ / 2, hw_ / 2, zbed + P["cord_d"], zbed + 12)
        add("Cord clamp (MK-08)", clamp, C["ss_dark"], "MK-08", "recoater", "recoater")
        vib = cyl(5, (hx, hw_ / 2 + 4, arm_z0 + 8), "y", 22)
        add("Vibration motor", vib, C["black"], "M3", "recoater", "recoater")
        # the stage's M8 cable from its side connector: to a gland in the back wall (box) or a KF feedthrough (cube)
        cx_ = P["rc_x0"] + VEN.LSM["conn_side"][0][0]
        cy_ = yr + VEN.LSM["conn_side"][0][2]
        if has_box:
            m8 = polyline_pipe([(cx_, cy_, z0 + 12.2), (cx_, cy_ + 25, z0 + 12.2), (-120.0, y1 - 15, z0 + 20.0),
                                (-120.0, y1 + t + 10, z0 + 20.0)], 2.5)
        else:
            m8 = polyline_pipe([(cx_, cy_, z0 + 12.2), (cx_, cy_ + 20, z0 + 12.2), (-88.0, yc + P["cube_in"] / 2 - 20,
                                L["cube_c"] - 60), (-88.0, yc + P["cube_in"] / 2 - 4, L["cube_c"] - 60)], 2.5)
        add("Recoater M8 data and power cable", m8, C["cable"], "M1c", "recoater")

    # ---------------- piston drive (FT-1, FT-1V) ----------------
    if has_stages:
        s = pz - P["pz_bot"]                                         # stage stroke 0..20
        zt = zbed + pz
        rod_bot = zt - P["sub_t"] - P["hp_t"] - L["rod_vis"]
        plat_top = rod_bot - P["rod_end_z"]
        # rod-end block (MK-15): clamp on the rod, a pocket where the potted plug's leads leave the rod, AE face at +x
        bh = P["blk_h"]
        blk = box(-32, 32, -20, 20, plat_top, plat_top + bh)
        blk = blk.cut(cyl(P["rod_od"] / 2 + 0.05, (0, 0, plat_top + 16), "z", bh))
        blk = blk.cut(box(-8, 8, -21, 8, plat_top + 4, plat_top + 16))               # lead pocket, open to -y
        blk = blk.cut(box(-0.75, 0.75, 0, 21, plat_top + 20, plat_top + bh + 1))     # clamp slit toward +y
        for a in (-1, 1):
            for b_ in (-1, 1):
                blk = blk.cut(cyl(3.3, (a * 25, b_ * 12.5, plat_top - 1), "z", bh + 2))
                blk = blk.cut(cyl(5.5, (a * 25, b_ * 12.5, plat_top + bh - 6.5), "z", 7))
        add("Rod-end block: clamp, lead pocket, AE face (MK-15)", blk, C["alu_dark"], "MK-15", "drive", "piston")
        add("Rod clamp screw M4", cyl(3.5, (32, 12, plat_top + 30), "x", 4), C["ss_dark"], "MK-15", "drive", "piston")
        tb = box(10, 30, -36, -20, plat_top + 2, plat_top + 26)
        add("Lead terminal block, 6-way pluggable, on the rod-end block", tb, C["green"], "H2", "drive", "piston")
        pig = polyline_pipe([(0, 0, rod_bot), (0, 0, plat_top + 10), (0, -14, plat_top + 10), (6, -24, plat_top + 12),
                             (12, -28, plat_top + 14)], 2.5)
        add("Lead pigtail, 4 heater + 2 TC wires", pig, C["cable"], "H3", "drive", "piston")
        if monitoring and mon("MON5"):
            ae = cyl(10.0, (32, -8, plat_top + 28), "x", 22).fuse(cyl(3.0, (54, -8, plat_top + 28), "x", 8))
            add("AE sensor on the rod-end block, R15I-AST class (MON5)", ae, C["mon"], "MON5", "monitoring", "piston")
            aec = polyline_pipe([(62, -8, plat_top + 28), (80, -8, plat_top + 20), (95, -40, plat_top - 20),
                                 (95, -70, plat_top - 50)], 2.0)
            add("AE cable to the decoupler (MON5)", aec, C["cable"], "MON5", "monitoring")
        hcab = polyline_pipe([(20, -36, plat_top + 14), (20, -60, plat_top + 6), (40, -85, plat_top - 30),
                              (60, -85, plat_top - 70)], 3.0)
        add("Heater and TC cable to the controller (H2)", hcab, C["cable"], "H2", "drive")
        if piston == "zaber":
            fixed, moving = VEN.zaber_x_vsr20a(s, parts=True)
            base = plat_top - P["vs_h"] - s
            rot = lambda sh_: sh_.rotate(V(0, 0, 0), V(0, 0, 1), 180).translate(V(0, 0, base))  # noqa: E731  housing to +y
            add("Zaber X-VSR20A-E01 piston stage", rot(fixed), C["zaber"], "M2", "drive")
            add("X-VSR20A platform", rot(moving), C["zaber_top"], "M2", "drive", "piston")
            bp = box(-90, 90, ry[0] - h, ry[1] + h, zb + 2 * h, zb + 2 * h + 10)
            riser = box(-32, 32, -32, 32, zb + 2 * h + 10, base)
            add("Piston-stage bracket plate and riser (MK-15)", comp([bp, riser]), C["alu"], "MK-15", "drive")
            bsc = [cyl(5.0, (a * 70, y_, zb + 2 * h + 10), "z", 6) for a in (-1, 1) for y_ in ry]
            add("Bracket-plate screws to the base rails, M6 (4)", comp(bsc), C["ss_dark"], "MK-15", "drive")
            vc = VEN.VSR["conn"]
            cxv, cyv = -(vc[0] + vc[1]) / 2, -(vc[2] + vc[3]) / 2               # after the 180 deg turn
            vcab = polyline_pipe([(cxv - 8, cyv, base + 13), (-90, cyv, base + 13), (-130, cyv - 30, base - 10),
                                  (-150, cyv - 60, zb + 2 * h + 12)], 2.5)
            add("X-VSR20A M8 cable", vcab, C["cable"], "M2", "drive")
        else:
            # Thorlabs MTS50/M-Z8 on end beside the rod: carriage faces -y, front end up; an L-arm carries the block
            fixed, car = VEN.thorlabs_mts50_z8(s, parts=True)
            y_cf = 32.0                                                       # carriage face
            oz = L["under"] - 2.0 - VEN.MTS["front"]                          # front end 2 mm under the enclosure
            pl = cq.Plane(origin=V(0, y_cf + VEN.MTS["h"], oz), xDir=V(0, 0, 1), normal=V(0, -1, 0))
            loc = cq.Location(pl)
            add("Thorlabs MTS50/M-Z8 piston stage, on end", fixed.moved(loc), C["thor"], "M2b", "drive")
            add("MTS50 carriage", car.moved(loc), C["alu_dark"], "M2b", "drive", "piston")
            zc_car = oz + VEN.MTS["car_home"] + s
            arm_v = box(-21.5, 21.5, y_cf - 8, y_cf, plat_top - 10, zc_car + 21.5)
            arm_h = box(-32, 32, -20, y_cf - 8, plat_top - 10, plat_top)
            add("MTS50 L-arm to the rod-end block (MK-15)", comp([arm_v, arm_h]), C["alu"], "MK-15", "drive", "piston")
            yb0 = y_cf + VEN.MTS["h"]
            twr = box(-30, 30, yb0, yb0 + 10, zb + 2 * h + 10, oz)
            bp = box(-90, 90, ry[0] - h, ry[1] + h, zb + 2 * h, zb + 2 * h + 10).cut(
                box(-24, 24, y_cf - 2, yb0 + 1, zb + 2 * h - 1, zb + 2 * h + 11))
            add("MTS50 tower plate and bracket plate (MK-15)", comp([twr, bp]), C["alu"], "MK-15", "drive")

    # ---------------- monitoring outside the enclosure (MON1-MON3, MON8) ----------------
    if cam:
        _add_camera(add, state, cam, has_box, L)
    for k, lg in lights.items():
        _add_light(add, k, lg, has_box)
    if monitoring and mon("MON8"):
        add("Digitizer, PicoScope 4444 class (MON8, envelope est.)", box(440, 630, -210, -40, zb, zb + 40), C["blue"],
            "MON8", "monitoring")

    # ---------------- gas, O2 and safety outside (FT-0 on for gas; S2 on for safety) ----------------
    if i_state >= STATES.index("S2"):
        add("Safety relay box: E-stop, key switch (S1)", box(330, 470, -330, -230, zb, zb + 70), C["yellow"], "S1",
            "safety")
        add("E-stop", cyl(18, (360, -280, zb + 70), "z", 22), C["red"], "S1", "safety")
        add("Key switch", cyl(10, (420, -280, zb + 70), "z", 14), C["black"], "S1", "safety")
        add("Emission lamp", cyl(14, (ux[1], ry[1], z_up_top), "z", 40), C["red"], "S1", "safety")
    if has_box:
        z_lid = L["roof_out"]
        sw_ = []
        for xx in (xc - 160, xc + 160):
            sw_.append(box(xx - 18, xx + 18, y0 - t - 16, y0 - t, z_lid - 50, z_lid - 24))
        add("Coded lid switches (2)", comp(sw_), C["yellow"], "S1", "safety")
    if cube:
        F = P["cube_frame"]
        sw_ = []
        for xx in (xc - 110, xc + 110):
            fz_ = yc - F / 2 - (P["cube_plate_t"] - P["cube_boss"])
            sw_.append(box(xx - 18, xx + 18, fz_ - 16, fz_, L["cube_c"] + 60, L["cube_c"] + 86))
        add("Coded lid switches (2)", comp(sw_), C["yellow"], "S1", "safety")
    if has_cassette:
        add("Argon regulator and solenoid valve panel", box(-330, -230, -330, -250, zb, zb + 160), C["alu_dark"], "G1",
            "gas")
        add("Exhaust HEPA housing and check valve", cyl(45, (300, -170, zb), "z", 190), C["white"], "G4", "gas")
        add("Trace O2 analyzer (Alpha Omega 3000, envelope)", box(250, 400, 250, 410, zb, zb + 140),
            C["white"], "G5", "gas")
    if state == "FT-1":
        fx_ = x0 - t
        add("120 mm fan blowing on the enclosure", box(fx_ - 30, fx_ - 5, yc + 30, yc + 150, -50, 70), C["black"], "E4",
            "enclosure")
    if cube:
        fy_ = yc + P["cube_frame"] / 2 + P["cube_plate_t"] - P["cube_boss"]
        cz_ = L["cube_c"]
        add("120 mm fan blowing on the enclosure", box(xc - 60, xc + 60, fy_ + 5, fy_ + 30, cz_ - 5, cz_ + 115), C["black"],
            "E4", "enclosure")
    if lid_open and has_box:
        parts = open_door(parts, state)
    return parts


# The box door (lid) and everything that rides on it; it turns about the concealed hinges (axis est.: the door's back
# top edge). Before it opens, the beam tube's centre section comes off (two half-shells, sideways).
DOOR_GROUP = ("Box door", "Window ring", "Window, ", "Window retaining flange", "Window-stack screws", "Inner clamp ring",
              "Cover-slide holder", "Cover slide", "Camera port", "Layer camera", "Camera post", "Quarter-turn latch")


def door_hinge(state="FT-1"):
    """(y, z) of the box door's hinge axis (along x)."""
    return P["deck_c"][1] + VEN.SAG["door"][1] / 2, levels(state)["roof_out"]


def open_door(parts, state="FT-1", deg=None):
    """The parts with the box door opened by deg (default P['door_open_deg'], the free angle from ft_checks) and the
    beam tube's centre section (and its surface thermocouple) taken off."""
    deg = P["door_open_deg"] if deg is None else deg
    yh, zh = door_hinge(state)
    out = []
    for p in parts:
        if p.name.startswith(("Beam tube centre section", "Surface thermocouples")):
            continue
        if p.name.startswith(DOOR_GROUP):
            p = Part(p.name, p.shape.rotate(V(0, yh, zh), V(1, yh, zh), -deg), p.color, p.pid, p.sub, p.group, p.opacity)
        out.append(p)
    return out


def light_geometry(state):
    """The two raking lights: port centre on the wall's inner face, unit axis from the plate centre to the light, and
    the wall normal (box) for the port bore."""
    L = levels(state)
    zbed = L["dz"]
    xc, yc = P["deck_c"]
    out = {}
    if state == "FT-1V":
        xin = xc - P["cube_in"] / 2
        yin = yc - P["cube_in"] / 2
    else:
        xin = xc - P["box_in"][0] / 2
        yin = yc - P["box_in"][1] / 2
    el2, el3 = (math.radians(a) for a in P["light_el"])
    p2 = (xin, 0.0, zbed + abs(xin) * math.tan(el2))
    out["MON2"] = dict(port_in=p2, u=_unit((p2[0], p2[1], p2[2] - zbed)), n="-x", el=P["light_el"][0], azimuth="-x")
    p3 = (0.0, yin, zbed + abs(yin) * math.tan(el3))
    out["MON3"] = dict(port_in=p3, u=_unit((p3[0], p3[1], p3[2] - zbed)), n="-y", el=P["light_el"][1], azimuth="-y")
    for lg in out.values():                                     # the bore is cut from just inside the wall outward
        nvec = (-1.0, 0.0, 0.0) if lg["n"] == "-x" else (0.0, -1.0, 0.0)
        lg["port_in"] = tuple(c + 1.0 * nc for c, nc in zip(lg["port_in"], (-nvec[0], -nvec[1], 0.0)))
        lg["port_out"] = lg["port_in"]
    return out


def _add_light(add, key, lg, has_box):
    """Port ring on the wall (box) and the LED stack along the light's axis, outside the enclosure."""
    p, u = lg["port_in"], lg["u"]
    wall_t = P["box_t"] + 2.0 if has_box else P["cube_plate_t"] + 2.0
    el = math.radians(lg["el"])
    s0 = (wall_t + 6.0 + 20.0 * math.sin(el)) / math.cos(el) + 3.0   # stack starts clear of the wall and the port ring
    st = cq.Solid.makeCylinder(15.25, 30.0, V(0, 0, s0), V(0, 0, 1)).fuse(
        cq.Solid.makeCylinder(17.0, 22.0, V(0, 0, s0 + 30.0), V(0, 0, 1))).fuse(
        cq.Solid.makeCylinder(20.0, 16.0, V(0, 0, s0 + 52.0), V(0, 0, 1)))
    s = _place_axis(st, p, u)
    # world-aligned port ring on the outside of the wall
    if lg["n"] == "-x":
        ring = cyl(22.0, (p[0] - wall_t + 1.0 - 6.0, p[1], p[2]), "x", 6.0).cut(cyl(15.0, (p[0] - 40, p[1], p[2]), "x", 80))
    else:
        ring = cyl(22.0, (p[0], p[1] - wall_t + 1.0 - 6.0, p[2]), "y", 6.0).cut(cyl(15.0, (p[0], p[1] - 40, p[2]), "y", 80))
    name = "Raking light from -x, 15 deg: LED, condenser tube" if key == "MON2" else "Raking light from -y, 30 deg: LED, condenser tube"
    add(f"{name} ({key})", s, C["mon"], key, "monitoring")
    add(f"Light port ring and window (MK-21, {key})", ring, C["alu"], "MK-21", "monitoring")


def _add_camera(add, state, cam, has_box, L):
    """Camera port (MK-19) on the box door or the cube top plate, and the camera stack along its line of sight."""
    W, u = cam["W"], cam["u"]
    zt = W[2]
    port = tube(22.0, 13.0, (W[0], W[1], zt), "z", 7.0).cut(cyl(12.95, (W[0], W[1], zt + 2), "z", 6))
    add("Camera port ring with a Ø1 in. window and cover slide (MK-19)", port, C["alu"], "MK-19", "monitoring")
    add("Camera port window, Ø25.4 x 3 fused silica", cyl(12.7, (W[0], W[1], zt + 2), "z", 3.0), C["glass"], "MK-19",
        "monitoring", opacity=0.5)
    # the stack along u (local z), starting 20 mm along the axis from the window (clear of the port ring)
    s0 = 20.0
    st = [cq.Solid.makeCylinder(15.25, 12.0, V(0, 0, s0), V(0, 0, 1)),                    # FESH1000 in an SM1 tube
          cq.Solid.makeCylinder(17.0, 30.0, V(0, 0, s0 + 12), V(0, 0, 1)),               # C-mount lens (est. Ø34 x 30)
          cq.Solid.makeCylinder(19.0, 6.0, V(0, 0, s0 + 42), V(0, 0, 1)),                # Scheimpflug wedge (MK-20)
          cq.Solid.makeCylinder(18.25, 10.0, V(0, 0, s0 + 48), V(0, 0, 1)),              # HQ camera C/CS mount
          cq.Solid.makeBox(38.0, 38.0, 18.0, V(-19, -19, s0 + 58))]                      # HQ camera board
    stack = comp([_place_axis(x, W, u) for x in st])
    add("Layer camera: Pi HQ, C-mount lens, FESH1000 (MON1)", stack, C["mon"], "MON1", "monitoring")
    # post and clamp (MK-20): a vertical post outboard of the camera, an arm to the mount ring
    mr = tuple(W[i] + (s0 + 53.0) * u[i] for i in range(3))
    hdir = _unit((u[0], u[1], 0.0))
    px_, py_ = mr[0] + 32.0 * hdir[0], mr[1] + 32.0 * hdir[1]
    post = cyl(6.0, (px_, py_, zt), "z", mr[2] - zt + 6.0)
    arm = polyline_pipe([(px_, py_, mr[2]), (mr[0] + 19.0 * hdir[0], mr[1] + 19.0 * hdir[1], mr[2])], 5.0, smooth=False)
    foot = cyl(12.0, (px_, py_, zt), "z", 4.0)
    add("Camera post, arm and foot (MK-20)", comp([post, arm, foot]), C["alu_dark"], "MK-20", "monitoring")


def bom_by_state():
    """{state: {part name: pid}} for the progression tables."""
    out = {}
    for s in STATES:
        out[s] = {p.name: p.pid for p in build(s)}
    return out


def diff_states(a, b, tol=0.5):
    """Parts added, moved and removed going from state a to state b (by name; moved = bounding box shifted)."""
    def bbs(parts):
        out = {}
        for p in parts:
            bb = p.shape.BoundingBox()
            out[p.name] = (p.pid, (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
        return out
    pa, pb = bbs(build(a)), bbs(build(b))
    added = [(n, pb[n][0]) for n in pb if n not in pa]
    removed = [(n, pa[n][0]) for n in pa if n not in pb]
    moved = [(n, pb[n][0]) for n in pb if n in pa and max(abs(x - y) for x, y in zip(pa[n][1], pb[n][1])) > tol]
    return dict(added=added, moved=moved, removed=removed, kept=len(pb) - len(added) - len(moved))


def to_assembly(parts, name):
    a = cq.Assembly(name=name)
    for i, p in enumerate(parts):
        r, g, b = (int(p.color[k:k + 2], 16) / 255 for k in (1, 3, 5))
        nm = "".join(ch if ch.isalnum() else "_" for ch in p.name)[:60] + f"_{i:03d}"
        a.add(p.shape, name=nm, color=cq.Color(r, g, b, p.opacity))
    return a


if __name__ == "__main__":
    import time
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for s in STATES:
        t0 = time.time()
        parts = build(s)
        print(f"{s}: {len(parts)} parts in {time.time() - t0:.1f} s")
        if "--no-export" not in sys.argv and s in ("FT-0", "FT-1", "FT-1V"):
            to_assembly(parts, s.replace("-", "_")).export(str(out / f"{s.lower()}.step"))
    if "--no-export" not in sys.argv:
        t0 = time.time()
        to_assembly(build("FT-1", piston="thorlabs"), "FT_1_thorlabs").export(str(out / "ft-1-thorlabs.step"))
        print(f"FT-1 (thorlabs piston) in {time.time() - t0:.1f} s")
