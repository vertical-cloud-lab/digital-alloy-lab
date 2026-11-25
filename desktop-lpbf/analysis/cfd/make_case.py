"""Write an OpenFOAM (v2406, simpleFoam, k-omega SST) case for the argon cross-flow in the desktop LPBF chamber.

Issue #260, PR #266. The gas volume is the low-profile chamber of desktop-lpbf/cad/lpbf_low.py: the 280 x 190 x 120 mm
interior, the inlet plenum behind the back wall with its KF-25 port and the 120 x 8 mm slot through the wall, the
124 x 8 mm outlet slot in the floor by the door, the 10 x 13 mm channel under the floor and the boot to its KF-25
port, the door recess, the Ø56 / Ø46 recess under the cover slide, and the parts that stand in the gas: the parked
recoater (blade, holder, arm, carriage block), its rail and ball screw on the back wall, the dose chute and the
gas-knife body. Every part is an axis-aligned box (round holes become squares of the same area), so the mesh is a
rectilinear grid of hexahedra whose lines fall on every edge. Each grid interval pair is one blockMesh block, and
solid blocks are left out.

Coordinates as in the model: mm, z = 0 is the powder plane (floor top), +x is the recoat direction, +y points to the
back wall, so the cross-flow runs in -y. Argon at 25 C and ~+10 mbar: rho 1.65 kg/m3, mu 22.6 uPa s.

Re-run (writes the case to --out; nothing in the repo):
    /tmp/venv/bin/python desktop-lpbf/analysis/cfd/make_case.py --res coarse --q-lpm 115 --out /tmp/cfd/coarse
    desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/coarse
(the full sequence, fine mesh and variants included, is in desktop-lpbf/gas-flow.md section 9)
Options: --res coarse|fine, --q-lpm (blower flow through the bed slot), --cad-dir (model copy), --iters, and
--variant baseline|fix. "fix" is the layout tried in gas-flow.md section 5: a perforated plate (~25 % open, K ~ 18)
in the inlet slot and in the outlet slot (porous zones), the under-floor outlet channel widened to 35 mm with a
KF-40 boot, and a 100 x 4 mm upper slot under the lid (--upper-lpm, default 40 L/min) sweeping under the slide.
The gas knife is drawn as a body only; its flow is not specified in the model, so it is off in every case.
The outlet plenum's channel, link and boot and the inlet plenum's cavity are read from lpbf_low.py's own box() expressions
(since 2026-11-25; the round-5 model moved the boot and its KF-25 port to the plenum's left end, x = -86). --outlet-end
right|left mirrors the boot and link about x = 0 (right = where the 2026-11-20 runs had them). run_case.sh runs simpleFoam
on 2 MPI ranks (NP=1 for serial), so the case also gets a decomposeParDict.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # desktop-lpbf/

RHO = 1.65            # kg/m3, Ar at 298 K and ~1023 mbar
MU = 2.26e-5          # Pa s, Ar at 298 K
NU = MU / RHO


def load_params(cad_dir: pathlib.Path):
    """module_params.py is pure Python; P of lpbf_low.py is read as text so CadQuery isn't needed."""
    spec = importlib.util.spec_from_file_location("module_params", cad_dir / "module_params.py")
    MP = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MP)
    src = (cad_dir / "lpbf_low.py").read_text()
    s = src.index("P = dict(")
    e = src.index("\n)\n", s)
    body = src[s + len("P = dict("):e]
    P = eval("dict(" + body + ")", {"MP": MP})   # the model's own parameter dict (numbers and MP refs only)
    P["_cav"] = model_cavities(src, MP, P)
    return MP, P


def model_cavities(src, MP, P):
    """The plenum cavities as lpbf_low.py cuts them, read from its own box() expressions, so that a move in the model moves
    the CFD with it (2026-11-25: the outlet boot had moved to the left end and this script still drew it at the right):
    the outlet plenum's channel, link and boot (KF-25 port in the boot's bottom, at x = xb_o) and the inlet plenum's
    cavity and KF-25 bore."""
    iy, wall, zf = P["ch_y"] / 2, P["wall"], -P["floor"]
    cy = iy + wall
    y0o, y1o = MP.OUTLET_Y
    xb_o = float(re.search(r"^\s*xb_o\s*=\s*([-+0-9.eE]+)", src, re.M).group(1))
    s = src.index("plo = plo.cut(fuse([")
    e = src.index("]))", s)
    boxes = eval(src[s + len("plo = plo.cut(fuse("):e + 1], {"box": lambda *a: tuple(float(v) for v in a),
                                                             "y0o": y0o, "y1o": y1o, "zf": zf, "xb_o": xb_o})
    channel = next(b for b in boxes if b[5] > zf)                 # the one open to the floor slot (cut to zf + 1)
    boot = min(boxes, key=lambda b: b[4])                          # the deep one, with the KF-25 port in its bottom
    link = next(b for b in boxes if b is not channel and b is not boot)
    line = next(ln for ln in src.splitlines() if ln.strip().startswith("plen_in = fuse("))
    cav = [float(eval(a, {"cy": cy})) for a in re.search(r"\.cut\(box\(([^()]*)\)\)", line).group(1).split(",")]
    m = re.search(r"\.cut\(cyl\(([0-9.]+), \(([^()]*)\), \"y\"", line)
    return dict(xb_o=xb_o, channel=channel[:5] + (zf,), link=link, boot=boot, inlet_cavity=tuple(cav),
                inlet_port_r=float(m.group(1)), inlet_port_z=float(eval(m.group(2).split(",")[2], {"cy": cy})))


def geometry(MP, P, variant="baseline"):
    """Fluid and solid boxes (x0, x1, y0, y1, z0, z1) in mm, with where each number comes from in lpbf_low.py."""
    ix, iy, iz = P["ch_x"] / 2, P["ch_y"] / 2, P["ch_z"]          # 140, 95, 120
    wall, fl = P["wall"], P["floor"]                                 # 16, 20
    cy = iy + wall                                                   # 111: outer face of the back wall
    ih = MP.INLET_HALF                                               # 60
    oh = MP.OUTLET_HALF                                              # 62
    oy0, oy1 = MP.OUTLET_Y                                           # -94, -86
    zf = -fl                                                         # -20: floor underside
    xp, xd, dh = P["x_park"], P["x_dose"], P["dose_y"]               # -106, -90, 50
    cav = P["_cav"]
    pc = cav["inlet_cavity"]                                         # box(-60, 60, cy - 1, cy + 27, 1.5, 25): floor at z 1.5 since round 5
    s_in = cav["inlet_port_r"] * math.sqrt(math.pi)                  # Ø25.4 bore as a square of the same area (22.5 mm)
    pz0 = max(pc[4], cav["inlet_port_z"] - s_in / 2)                 # bore centre z 11, kept inside the cavity's height
    fluid = {
        "chamber": (-ix, ix, -iy, iy, 0.0, iz),
        "door recess": (-110.0, 110.0, -cy, -iy, 8.0, 100.0),       # ch.cut(box(-110, 110, -cy-1, -iy+1, 8, 100)); door face at y=-cy
        "inlet slot": (-ih, ih, iy, cy, 4.0, 12.0),                  # ch.cut(box(-INLET_HALF, INLET_HALF, iy-1, cy+1, 4, 12))
        "inlet plenum": (pc[0], pc[1], cy, pc[3], pc[4], pc[5]),     # plen_in cavity, read from the model (x +/-60, to cy+27, z 1.5-25)
        # KF-25 port (Ø25.4 bore at z = 11) as a 22.5 mm square duct of the same area, 5 mm long
        "inlet port": (-s_in / 2, s_in / 2, pc[3], pc[3] + 5.0, pz0, pz0 + s_in),
        "outlet slot": (-oh, oh, oy0, oy1, zf, 0.0),                 # ch.cut(box(-OUTLET_HALF, OUTLET_HALF, OUTLET_Y, -fl-1, 1))
        # the plo cavities, read from the model: channel box(-63, 72, y0o-1, y1o+1, zf-13, zf+1); since 2026-11-23 the link
        # box(xb_o+6, xb_o+26, ...) and the boot box(xb_o-10, xb_o+10, y0o-8, y1o+4, zf-41, zf-3) are at the LEFT end (xb_o = -86)
        "outlet channel": cav["channel"],
        "outlet link": cav["link"],
        "outlet boot": cav["boot"],                                  # KF-25 port below its bottom face (the 'outlet' patch)
        # Ø56 lid bore (z 120-125) and the drawer's Ø46 opening (z 125-126) under the cover slide, as equal-area squares
        "slide recess": (-25.0, 25.0, -25.0, 25.0, iz, iz + 5.0),
        "slide opening": (-20.0, 20.0, -20.0, 20.0, iz + 5.0, iz + 6.0),
    }
    if variant == "fix":
        # under-floor outlet channel widened from 10 to 35 mm (y -95..-60: clear of the Ø96 module port at y > -48), a
        # 40 x 42 mm boot to a KF-40 port, and a 100 x 4 mm upper slot through the back wall just under the lid that
        # blows along the ceiling under the cover slide toward the door (its own feed; not drawn in the model)
        # The boot stays at the model's end (the left since 2026-11-23) and grows to 40 mm in x away from the slot (it was
        # x 76-116 at the right end in the 2026-11-20 runs)
        ch, lk, bt = cav["channel"], cav["link"], cav["boot"]
        fluid["outlet channel"] = (min(ch[0], lk[0]), max(ch[1], lk[1]), oy0 - 1, -60.0, zf - 13, zf)
        fluid["outlet link"] = (lk[0], lk[1], oy0 - 1, -60.0, zf - 13, zf - 3)
        bx = (bt[0], bt[0] + 40.0) if bt[0] > 0 else (bt[1] - 40.0, bt[1])
        fluid["outlet boot"] = (bx[0], bx[1], oy0 - 8, -60.0, zf - 41, zf - 3)
        fluid["upper slot"] = (-50.0, 50.0, iy, cy, iz - 6.0, iz - 2.0)
    solid = {
        # parked recoater: blade (x xp+9..xp+10.5, z 0.05-18) and holder (x xp-9..xp+9, z 3-34) as one block to the floor
        "blade + holder": (xp - 9.0, xp + 10.0, -dh - 3.0, dh + 3.0, 0.0, 35.0),
        "arm + block": (xp - 22.0, xp + 22.0, dh + 3.0, iy - 28.0, 14.0, 100.0),   # arm z 14-25, block z 25-99
        "block rear + nut + carriage": (xp - 22.0, xp + 22.0, iy - 28.0, iy, 25.0, 100.0),
        "rail": (-135.0, 135.0, iy - 15.0, iy, P["rc_rail_z"] - 7.0, P["rc_rail_z"] + 8.0),
        "ball screw (Ø12 as 10 x 10)": (-ix, ix, P["rc_screw_y"] - 5.0, P["rc_screw_y"] + 5.0, P["rc_screw_z"] - 5.0, P["rc_screw_z"] + 5.0),
        "dose chute": (xd - 6.0, xd + 6.0, -dh, dh, 37.0, iz),     # box(xd-6, xd+6, -dose_y, dose_y, 37, lz0), hollow but closed by the roller
        "gas knife body": (-32.0, 32.0, -42.0, -36.0, iz - 14.0, iz - 8.0),
    }
    return fluid, solid


def lines(fluid, solid, axis):
    vals = set()
    for b in list(fluid.values()) + list(solid.values()):
        vals.add(round(b[2 * axis], 3))
        vals.add(round(b[2 * axis + 1], 3))
    return sorted(vals)


def spacing(axis, c, res):
    """Target cell size (mm) at coordinate c along axis."""
    f = 1.0 if res == "fine" else 1.5
    if axis == 2:
        if -3.0 <= c <= 14.0:
            return 1.0 * f          # bed, slot and wall jet
        if 14.0 < c <= 25.0 or 118.0 <= c <= 127.0:
            return 1.5 * f          # above the jet; ceiling and slide recess
        return 3.0 * f
    if axis == 1 and 95.0 <= c <= 112.0:
        return 2.0 * f              # the slot channel
    return 3.0 * f


def inside(b, p):
    return b[0] < p[0] < b[1] and b[2] < p[1] < b[3] and b[4] < p[2] < b[5]


def build(args):
    MP, P = load_params(pathlib.Path(args.cad_dir))
    cav = P["_cav"]
    if args.outlet_end != "model" and (cav["boot"][0] < 0) != (args.outlet_end == "left"):
        # mirror the link and boot about x = 0 (the 2026-11-20 runs had them at x 60-80 and 76-96, the model's old right end)
        flip = lambda b: (-b[1], -b[0]) + tuple(b[2:])
        cav.update(link=flip(cav["link"]), boot=flip(cav["boot"]), xb_o=-cav["xb_o"])
    fluid, solid = geometry(MP, P, args.variant)
    X, Y, Z = (lines(fluid, solid, a) for a in range(3))
    N = [[max(1, math.ceil((L[i + 1] - L[i]) / spacing(a, 0.5 * (L[i] + L[i + 1]), args.res) - 1e-9)) for i in range(len(L) - 1)]
         for a, L in enumerate((X, Y, Z))]
    nx, ny, nz = len(X) - 1, len(Y) - 1, len(Z) - 1

    def is_fluid(i, j, k):
        if not (0 <= i < nx and 0 <= j < ny and 0 <= k < nz):
            return False
        p = (0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1]))
        return any(inside(b, p) for b in fluid.values()) and not any(inside(b, p) for b in solid.values())

    F = {(i, j, k) for i in range(nx) for j in range(ny) for k in range(nz) if is_fluid(i, j, k)}
    vid = {}
    verts = []

    def v(i, j, k):
        key = (i, j, k)
        if key not in vid:
            vid[key] = len(verts)
            verts.append((X[i], Y[j], Z[k]))
        return vid[key]

    blocks = []
    ncell = 0
    zones = {"screenIn": fluid["inlet slot"], "screenOut": fluid["outlet slot"]} if args.variant == "fix" else {}
    for (i, j, k) in sorted(F, key=lambda t: (t[2], t[1], t[0])):
        h = [v(i, j, k), v(i + 1, j, k), v(i + 1, j + 1, k), v(i, j + 1, k),
             v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)]
        pc = (0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1]))
        zn = next((zname for zname, zb in zones.items() if inside(zb, pc)), "")
        blocks.append((h, (N[0][i], N[1][j], N[2][k]), zn))
        ncell += N[0][i] * N[1][j] * N[2][k]

    # boundary faces that get their own patch (everything else is 'walls')
    patches = {"inlet": [], "inlet2": [], "outlet": [], "floor": [], "slide": []}
    up = fluid.get("upper slot")
    port = fluid["inlet port"]
    boot = fluid["outlet boot"]
    for (i, j, k) in F:
        xc, yc, zc = 0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1])
        if j == ny - 1 and port[0] < xc < port[1] and port[4] < zc < port[5]:          # +y face at the port end
            patches["inlet"].append((v(i, j + 1, k), v(i, j + 1, k + 1), v(i + 1, j + 1, k + 1), v(i + 1, j + 1, k)))
        if up and abs(Y[j + 1] - up[3]) < 1e-9 and up[0] < xc < up[1] and up[4] < zc < up[5]:   # +y end of the upper slot
            patches["inlet2"].append((v(i, j + 1, k), v(i, j + 1, k + 1), v(i + 1, j + 1, k + 1), v(i + 1, j + 1, k)))
        if k == 0 and boot[0] < xc < boot[1] and boot[2] < yc < boot[3]:                 # -z face at the boot bottom
            patches["outlet"].append((v(i, j, k), v(i, j + 1, k), v(i + 1, j + 1, k), v(i + 1, j, k)))
        if abs(Z[k]) < 1e-9 and not is_fluid(i, j, k - 1):                                # the chamber floor = powder plane
            patches["floor"].append((v(i, j, k), v(i, j + 1, k), v(i + 1, j + 1, k), v(i + 1, j, k)))
        if abs(Z[k + 1] - (P["ch_z"] + 6.0)) < 1e-9:                                       # the cover slide's underside
            patches["slide"].append((v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)))

    purge = args.slide_purge_lpm > 0
    if purge:
        # gas-flow.md §7 item 6: argon fed into the lid bore above the Ø46 opening leaves the recess downward. Modelled as an
        # even inflow through the cover slide's underside (the 40 x 40 square standing for the Ø46 opening, z 126)
        patches["inlet3"] = patches.pop("slide")
    out = pathlib.Path(args.out)
    for d in ("system", "constant", "0"):
        (out / d).mkdir(parents=True, exist_ok=True)
    hdr = lambda cls, obj, loc="": ("FoamFile\n{\n    version 2.0;\n    format ascii;\n    class %s;\n%s    object %s;\n}\n"
                                     % (cls, ('    location "%s";\n' % loc) if loc else "", obj))
    with open(out / "system/blockMeshDict", "w") as f:
        f.write(hdr("dictionary", "blockMeshDict", "system"))
        f.write("scale 0.001;\n\nvertices\n(\n")
        f.write("".join("    (%g %g %g)\n" % p for p in verts))
        f.write(");\n\nblocks\n(\n")
        f.write("".join("    hex (%s) %s (%d %d %d) simpleGrading (1 1 1)\n" % (" ".join(map(str, h)), zn, *n) for h, n, zn in blocks))
        f.write(");\n\nedges ();\n\nboundary\n(\n")
        for name, faces in patches.items():
            if not faces:
                continue
            typ = "patch" if name in ("inlet", "inlet2", "inlet3", "outlet") else "wall"
            f.write("    %s\n    {\n        type %s;\n        faces\n        (\n" % (name, typ))
            f.write("".join("            (%d %d %d %d)\n" % fc for fc in faces))
            f.write("        );\n    }\n")
        f.write(");\n\ndefaultPatch { name walls; type wall; }\n\nmergePatchPairs ();\n")

    q = args.q_lpm / 60000.0           # m3/s
    q2 = args.upper_lpm / 60000.0 if args.variant == "fix" else 0.0
    q3 = args.slide_purge_lpm / 60000.0
    a_port = (port[1] - port[0]) * (port[5] - port[4]) * 1e-6
    k_in = 1.5 * (0.05 * q / a_port) ** 2
    w_in = math.sqrt(k_in) / (0.09 ** 0.25 * 0.07 * 0.0254)
    walls = "walls|floor|slide"
    files = {
        "0/U": hdr("volVectorField", "U") + f"""dimensions [0 1 -1 0 0 0 0];
internalField uniform (0 0 0);
boundaryField
{{
    inlet {{ type flowRateInletVelocity; volumetricFlowRate constant {q:.6g}; extrapolateProfile no; value uniform (0 0 0); }}
    inlet2 {{ type flowRateInletVelocity; volumetricFlowRate constant {q2:.6g}; extrapolateProfile no; value uniform (0 0 0); }}
    inlet3 {{ type flowRateInletVelocity; volumetricFlowRate constant {q3:.6g}; extrapolateProfile no; value uniform (0 0 0); }}
    outlet {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}
    "({walls})" {{ type noSlip; }}
}}
""",
        "0/p": hdr("volScalarField", "p") + f"""dimensions [0 2 -2 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "inlet.*" {{ type zeroGradient; }}
    outlet {{ type fixedValue; value uniform 0; }}
    "({walls})" {{ type zeroGradient; }}
}}
""",
        "0/k": hdr("volScalarField", "k") + f"""dimensions [0 2 -2 0 0 0 0];
internalField uniform {k_in:.4g};
boundaryField
{{
    "inlet.*" {{ type turbulentIntensityKineticEnergyInlet; intensity 0.05; value uniform {k_in:.4g}; }}
    outlet {{ type inletOutlet; inletValue uniform {k_in:.4g}; value uniform {k_in:.4g}; }}
    "({walls})" {{ type kqRWallFunction; value uniform {k_in:.4g}; }}
}}
""",
        "0/omega": hdr("volScalarField", "omega") + f"""dimensions [0 0 -1 0 0 0 0];
internalField uniform {w_in:.4g};
boundaryField
{{
    "inlet.*" {{ type turbulentMixingLengthFrequencyInlet; mixingLength {0.07 * 0.0254:.4g}; value uniform {w_in:.4g}; }}
    outlet {{ type inletOutlet; inletValue uniform {w_in:.4g}; value uniform {w_in:.4g}; }}
    "({walls})" {{ type omegaWallFunction; value uniform {w_in:.4g}; }}
}}
""",
        "0/nut": hdr("volScalarField", "nut") + f"""dimensions [0 2 -1 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "inlet.*" {{ type calculated; value uniform 0; }}
    outlet {{ type calculated; value uniform 0; }}
    "({walls})" {{ type nutUSpaldingWallFunction; value uniform 0; }}
}}
""",
        "constant/transportProperties": hdr("dictionary", "transportProperties") + f"transportModel Newtonian;\nnu {NU:.6g};\n",
        "constant/turbulenceProperties": hdr("dictionary", "turbulenceProperties")
        + "simulationType RAS;\nRAS\n{\n    RASModel kOmegaSST;\n    turbulence on;\n    printCoeffs on;\n}\n",
        "system/controlDict": hdr("dictionary", "controlDict") + f"""application simpleFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime {args.iters};
deltaT 1;
writeControl timeStep;
writeInterval {args.iters};
purgeWrite 2;
writeFormat binary;
writePrecision 8;
writeCompression off;
timeFormat general;
runTimeModifiable true;
functions
{{
    wallShearStress {{ type wallShearStress; libs (fieldFunctionObjects); patches (floor walls{'' if purge else ' slide'}); writeControl writeTime; log false; }}
    yPlus {{ type yPlus; libs (fieldFunctionObjects); writeControl writeTime; log false; }}
    pIn {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name inlet; operation areaAverage; fields (p); writeFields false; writeControl timeStep; writeInterval 20; log false; }}
    qOut {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name outlet; operation sum; fields (phi); writeFields false; writeControl timeStep; writeInterval 20; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 20; fields (U p); probeLocations ((0 0 0.003) (0 0 0.010) (0 0.0375 0.003) (0 -0.0375 0.003) (0 0 0.115)); }}
}}
""",
        "system/fvSchemes": hdr("dictionary", "fvSchemes") + """ddtSchemes { default steadyState; }
gradSchemes { default Gauss linear; grad(U) cellLimited Gauss linear 1; grad(k) cellLimited Gauss linear 1; grad(omega) cellLimited Gauss linear 1; }
divSchemes
{
    default none;
    div(phi,U) bounded Gauss linearUpwind grad(U);
    div(phi,k) bounded Gauss limitedLinear 1;
    div(phi,omega) bounded Gauss limitedLinear 1;
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}
laplacianSchemes { default Gauss linear corrected; }
interpolationSchemes { default linear; }
snGradSchemes { default corrected; }
wallDist { method meshWave; }
""",
        "system/decomposeParDict": hdr("dictionary", "decomposeParDict") + "numberOfSubdomains 2;\nmethod scotch;\n",
        "system/fvSolution": hdr("dictionary", "fvSolution") + """solvers
{
    p { solver GAMG; tolerance 1e-7; relTol 0.05; smoother GaussSeidel; }
    "(U|k|omega)" { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0.1; }
}
SIMPLE
{
    nNonOrthogonalCorrectors 0;
    consistent yes;
    residualControl { p 1e-5; U 1e-6; "(k|omega)" 1e-6; }
}
relaxationFactors
{
    fields { p 1; }
    equations { U 0.7; k 0.6; omega 0.6; }
}
""",
    }
    if args.variant == "fix":
        # perforated plates (about 25 % open, K ~ 18 on the slot velocity) filling each slot's 16 / 20 mm depth:
        # Forchheimer f = K / depth along the flow, and 20x that across it so the plates also straighten the flow
        def screen(zone, axis, depth_m, K=18.0):
            f = [20 * K / depth_m] * 3
            f[axis] = K / depth_m
            return f"""{zone}
{{
    type explicitPorositySource;
    explicitPorositySourceCoeffs
    {{
        type DarcyForchheimer;
        selectionMode cellZone;
        cellZone {zone};
        DarcyForchheimerCoeffs
        {{
            d (0 0 0);
            f ({f[0]:.6g} {f[1]:.6g} {f[2]:.6g});
            coordinateSystem {{ type cartesian; origin (0 0 0); rotation {{ type axes; e1 (1 0 0); e2 (0 1 0); }} }}
        }}
    }}
}}
"""
        files["system/fvOptions"] = hdr("dictionary", "fvOptions") + screen("screenIn", 1, 0.016) + screen("screenOut", 2, 0.020)
    for name, txt in files.items():
        (out / name).write_text(txt)
    (out / "case.foam").write_text("")
    meta = dict(res=args.res, variant=args.variant, upper_lpm=q2 * 60000.0, slide_purge_lpm=args.slide_purge_lpm, q_lpm=args.q_lpm, q_m3s=q, blocks=len(blocks), cells=ncell, lines=dict(x=X, y=Y, z=Z),
                n=dict(x=N[0], y=N[1], z=N[2]), fluid=fluid, solid=solid, rho=RHO, mu=MU, nu=NU,
                slot_v=q / ((2 * MP.INLET_HALF) * 8.0e-6), port_area_m2=a_port, outlet_boot_x_mm=P["_cav"]["xb_o"],
                patches={k_: len(v_) for k_, v_ in patches.items()})
    (out / "case_meta.json").write_text(json.dumps(meta, indent=1))
    print(f"{out}: {len(blocks)} blocks, {ncell} cells, Q = {args.q_lpm} L/min, mean slot velocity {meta['slot_v']:.2f} m/s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--res", choices=("coarse", "fine"), default="fine")
    ap.add_argument("--q-lpm", type=float, default=115.0, help="blower flow, L/min (115 = 2.0 m/s mean in the 120 x 8 slot)")
    ap.add_argument("--iters", type=int, default=1500)
    ap.add_argument("--variant", choices=("baseline", "fix"), default="baseline",
                    help="fix = screens in both slots, wider outlet channel + KF-40 boot, upper window-sweep slot")
    ap.add_argument("--upper-lpm", type=float, default=40.0, help="flow through the upper slot in the 'fix' variant, L/min")
    ap.add_argument("--slide-purge-lpm", type=float, default=0.0,
                    help="argon blown down out of the cover slide's recess (gas-flow.md §7 item 6), L/min; 0 = the slide is a wall")
    ap.add_argument("--outlet-end", choices=("model", "left", "right"), default="model",
                    help="where the outlet boot and its port sit: as in the model (left since 2026-11-23), or mirrored")
    ap.add_argument("--cad-dir", default=str(ROOT / "cad"))
    ap.add_argument("--out", required=True)
    build(ap.parse_args())
