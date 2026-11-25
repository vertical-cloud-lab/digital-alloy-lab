"""OpenFOAM case for the plume / spatter / window-fouling study (issue #260; monitoring/plume.md).

Extends analysis/cfd/make_case.py (imported, not edited) with what the monitoring hardware adds to the gas volume:
  - the viewport bores from cad/monitoring_spec.py (read at run time), each a recess in its wall with its own patch:
      LW  left-wall side viewport: Ø25 clear bore in the -x wall, cover slide at the bottom of a --lw-depth recess -> lwSlide
      BW  back-wall light window: Ø20 bore through the whole +y wall, window on the outer face               -> bwWindow
      LP  steep lid port: Ø20 bore in the lid, cover slide at the bottom of a --lp-depth recess               -> lpSlide
      LC  the layer camera's existing Ø30 bore through the lid (optics.md §8.5), window at the lid's top face  -> lcWindow
    plus the laser cover slide as before (patch 'slide').
  - an optional argon purge across the LW cover slide (--lw-purge-lpm, 1-5 L/min): a 1.5 mm slot along the top edge of the
    LW recess, next to the slide, blowing down across its face (patch 'inletLW'; a wall when the purge is off).
  - the recoater in the lasing state: blade and carriage at the end of the stroke (x_end = +100), where monitoring_views.py
    and the layer cycle put it while the laser runs (gas-flow.md's runs had it at the park position, x -106, which would also
    block the LW view).
  - finer cells around the LW recess (1.5 mm in x next to the wall, 2 mm in y and z over the recess).
Everything else (mesh logic, schemes, the 'fix' layout's screens, wide outlet and upper slot) is make_case.py's. Each grid
interval pair is one blockMesh block, as there.

Run (case written to --out; nothing in the repo):
    /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/make_case_plume.py --variant fix --q-lpm 200 --upper-lpm 40 \
        --iters 800 --out /tmp/plume/p200
    desktop-lpbf/analysis/cfd/run_case.sh /tmp/plume/p200
The full sequence is in monitoring/plume.md ("Re-running").
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                         # desktop-lpbf/
_spec = importlib.util.spec_from_file_location("make_case", ROOT / "analysis" / "cfd" / "make_case.py")
MC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MC)

WINDOW_PATCHES = ("slide", "lwSlide", "bwWindow", "lpSlide", "lcWindow")


def load_spec(cad_dir):
    s = importlib.util.spec_from_file_location("monitoring_spec", pathlib.Path(cad_dir) / "monitoring_spec.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def crossing(centre, target, coord, value):
    """Point on the line centre -> target where coordinate `coord` (0, 1, 2) equals value."""
    t = (value - centre[coord]) / (target[coord] - centre[coord])
    return tuple(c + t * (g - c) for c, g in zip(centre, target))


def viewport_boxes(MS, P, lw_depth, lp_depth):
    """Recess boxes (x0, x1, y0, y1, z0, z1) for the viewports, and where their window / slide face is."""
    ix, iy, iz = P["ch_x"] / 2, P["ch_y"] / 2, P["ch_z"]
    wall = P["wall"]
    lid_t = 16.0                                                     # lid z 120..136 (monitoring_spec docstring)
    tgt = MS.TARGET
    V = MS.VIEWPORTS
    out = {}
    # LW: -x wall. The bore runs on the line of sight (12.9 deg below horizontal, 7 deg off the wall normal); as a box normal
    # to the wall, centred where the axis crosses the middle of the recess.
    c = V["LW"]["centre"]
    s = V["LW"]["clear_d"] * math.sqrt(math.pi) / 2                  # Ø25 as a 22.2 mm square of the same area
    p = crossing(c, tgt, 0, -ix - lw_depth / 2)
    out["LW"] = dict(box=(-ix - lw_depth, -ix, p[1] - s / 2, p[1] + s / 2, p[2] - s / 2, p[2] + s / 2),
                     face_axis=0, face_at=-ix - lw_depth, patch="lwSlide", area_mm2=s * s)
    # BW: +y wall, window on the outer face (y = iy + wall)
    c = V["BW"]["centre"]
    s = V["BW"]["clear_d"] * math.sqrt(math.pi) / 2
    p = crossing(c, tgt, 1, iy + wall / 2)
    out["BW"] = dict(box=(p[0] - s / 2, p[0] + s / 2, iy, iy + wall, p[2] - s / 2, p[2] + s / 2),
                     face_axis=1, face_at=iy + wall, patch="bwWindow", area_mm2=s * s)
    # LP: lid, slide at the bottom of the recess
    c = V["LP"]["centre"]
    s = V["LP"]["clear_d"] * math.sqrt(math.pi) / 2
    p = crossing(c, tgt, 2, iz + lp_depth / 2)
    out["LP"] = dict(box=(p[0] - s / 2, p[0] + s / 2, p[1] - s / 2, p[1] + s / 2, iz, iz + lp_depth),
                     face_axis=2, face_at=iz + lp_depth, patch="lpSlide", area_mm2=s * s)
    # LC: the layer camera's Ø30 bore on its line of sight through the lid (lpbf_low.py, optics.md §8.5); the window sits higher
    # in the boss, so the lid's top face stands in for it
    c = (75.0, -45.0, 136.0)
    s = 30.0 * math.sqrt(math.pi) / 2
    p = crossing(c, tgt, 2, iz + lid_t / 2)
    out["LC"] = dict(box=(p[0] - s / 2, p[0] + s / 2, p[1] - s / 2, p[1] + s / 2, iz, iz + lid_t),
                     face_axis=2, face_at=iz + lid_t, patch="lcWindow", area_mm2=s * s)
    for d in out.values():                                           # 0.1 mm grid, so the mesh lines and the patch tests agree
        d["box"] = tuple(round(c, 1) for c in d["box"])
    return out


def build(args):
    MP, P = MC.load_params(pathlib.Path(args.cad_dir))
    MS = load_spec(args.cad_dir)
    if args.recoater == "lasing":
        P["x_park"] = P["x_end"]                                      # geometry() places the blade, arm and carriage at x_park
    fluid, solid = MC.geometry(MP, P, args.variant, args.floor_slot_width)
    vp = viewport_boxes(MS, P, args.lw_depth, args.lp_depth)
    for k, v in vp.items():
        fluid[f"viewport {k}"] = v["box"]
    lw = vp["LW"]["box"]
    purge_w = 1.5
    purge_box = (lw[0], lw[0] + purge_w, lw[2], lw[3], lw[5], lw[5])   # strip of the recess's top face next to the slide
    # an extra grid line so the purge strip is its own column of cells
    fluid["_lw purge line"] = (lw[0] + purge_w, lw[0] + purge_w, lw[2], lw[2], lw[4], lw[4])
    ix = P["ch_x"] / 2

    def spacing(axis, c, res):
        h = MC.spacing(axis, c, res)
        if axis == 0 and -ix - args.lw_depth - 1 <= c <= -ix + 12:
            return min(h, 1.5)
        if axis == 1 and lw[2] - 6 <= c <= lw[3] + 6:
            return min(h, 2.0)
        if axis == 2 and lw[4] - 6 <= c <= lw[5] + 6:
            return min(h, 2.0)
        return h

    X, Y, Z = (MC.lines({k: v for k, v in fluid.items()}, solid, a) for a in range(3))
    fluid.pop("_lw purge line")
    N = [[max(1, math.ceil((L[i + 1] - L[i]) / spacing(a, 0.5 * (L[i] + L[i + 1]), args.res) - 1e-9)) for i in range(len(L) - 1)]
         for a, L in enumerate((X, Y, Z))]
    nx, ny, nz = len(X) - 1, len(Y) - 1, len(Z) - 1
    inside = MC.inside

    def is_fluid(i, j, k):
        if not (0 <= i < nx and 0 <= j < ny and 0 <= k < nz):
            return False
        p = (0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1]))
        return any(inside(b, p) for b in fluid.values()) and not any(inside(b, p) for b in solid.values())

    F = {(i, j, k) for i in range(nx) for j in range(ny) for k in range(nz) if is_fluid(i, j, k)}
    vid, verts = {}, []

    def v(i, j, k):
        key = (i, j, k)
        if key not in vid:
            vid[key] = len(verts)
            verts.append((X[i], Y[j], Z[k]))
        return vid[key]

    blocks, ncell = [], 0
    zones = {"screenIn": fluid["inlet slot"], "screenOut": fluid["outlet slot"]} if args.variant == "fix" else {}
    for (i, j, k) in sorted(F, key=lambda t: (t[2], t[1], t[0])):
        h = [v(i, j, k), v(i + 1, j, k), v(i + 1, j + 1, k), v(i, j + 1, k),
             v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)]
        pc = (0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1]))
        zn = next((zname for zname, zb in zones.items() if inside(zb, pc)), "")
        blocks.append((h, (N[0][i], N[1][j], N[2][k]), zn))
        ncell += N[0][i] * N[1][j] * N[2][k]

    purge = args.lw_purge_lpm > 0
    patches = {"inlet": [], "inlet2": [], "outlet": [], "floor": [], "slide": [], "lwSlide": [], "bwWindow": [], "lpSlide": [],
               "lcWindow": [], "lwPurge": []}
    pname = "lwPurge"                                                # a patch when the purge runs, a wall when it is off
    up = fluid.get("upper slot")
    port = fluid["inlet port"]
    boot = fluid["outlet boot"]
    eps = 1e-6
    for (i, j, k) in F:
        xc, yc, zc = 0.5 * (X[i] + X[i + 1]), 0.5 * (Y[j] + Y[j + 1]), 0.5 * (Z[k] + Z[k + 1])
        if j == ny - 1 and port[0] < xc < port[1] and port[4] < zc < port[5]:
            patches["inlet"].append((v(i, j + 1, k), v(i, j + 1, k + 1), v(i + 1, j + 1, k + 1), v(i + 1, j + 1, k)))
        if up and abs(Y[j + 1] - up[3]) < 1e-9 and up[0] < xc < up[1] and up[4] < zc < up[5]:
            patches["inlet2"].append((v(i, j + 1, k), v(i, j + 1, k + 1), v(i + 1, j + 1, k + 1), v(i + 1, j + 1, k)))
        if k == 0 and boot[0] < xc < boot[1] and boot[2] < yc < boot[3]:
            patches["outlet"].append((v(i, j, k), v(i, j + 1, k), v(i + 1, j + 1, k), v(i + 1, j, k)))
        if abs(Z[k]) < 1e-9 and not is_fluid(i, j, k - 1):
            patches["floor"].append((v(i, j, k), v(i, j + 1, k), v(i + 1, j + 1, k), v(i + 1, j, k)))
        if abs(Z[k + 1] - (P["ch_z"] + 6.0)) < 1e-9 and abs(xc) < 25 and abs(yc) < 25 and not is_fluid(i, j, k + 1):
            patches["slide"].append((v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)))
        for key, d in vp.items():
            b = d["box"]
            if not inside(b, (xc, yc, zc)):
                continue
            if d["face_axis"] == 0 and abs(X[i] - d["face_at"]) < 1e-9 and not is_fluid(i - 1, j, k):        # -x face
                patches[d["patch"]].append((v(i, j, k), v(i, j, k + 1), v(i, j + 1, k + 1), v(i, j + 1, k)))
            if d["face_axis"] == 1 and abs(Y[j + 1] - d["face_at"]) < 1e-9 and not is_fluid(i, j + 1, k):    # +y face
                patches[d["patch"]].append((v(i, j + 1, k), v(i, j + 1, k + 1), v(i + 1, j + 1, k + 1), v(i + 1, j + 1, k)))
            if d["face_axis"] == 2 and abs(Z[k + 1] - d["face_at"]) < 1e-9 and not is_fluid(i, j, k + 1):    # +z face
                patches[d["patch"]].append((v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)))
        if (abs(Z[k + 1] - purge_box[5]) < 1e-9 and purge_box[0] - eps < X[i] and X[i + 1] < purge_box[1] + eps
                and purge_box[2] < yc < purge_box[3] and not is_fluid(i, j, k + 1)):
            patches[pname].append((v(i, j, k + 1), v(i + 1, j, k + 1), v(i + 1, j + 1, k + 1), v(i, j + 1, k + 1)))

    out = pathlib.Path(args.out)
    for d in ("system", "constant", "0"):
        (out / d).mkdir(parents=True, exist_ok=True)
    hdr = lambda cls, obj, loc="": ("FoamFile\n{\n    version 2.0;\n    format ascii;\n    class %s;\n%s    object %s;\n}\n"
                                     % (cls, ('    location "%s";\n' % loc) if loc else "", obj))
    inlets = ("inlet", "inlet2", "outlet") + (("lwPurge",) if purge else ())
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
            typ = "patch" if name in inlets else "wall"
            f.write("    %s\n    {\n        type %s;\n        faces\n        (\n" % (name, typ))
            f.write("".join("            (%d %d %d %d)\n" % fc for fc in faces))
            f.write("        );\n    }\n")
        f.write(");\n\ndefaultPatch { name walls; type wall; }\n\nmergePatchPairs ();\n")

    q = args.q_lpm / 60000.0
    q2 = args.upper_lpm / 60000.0 if args.variant == "fix" else 0.0
    q4 = args.lw_purge_lpm / 60000.0
    a_port = (port[1] - port[0]) * (port[5] - port[4]) * 1e-6
    k_in = 1.5 * (0.05 * q / a_port) ** 2
    w_in = math.sqrt(k_in) / (0.09 ** 0.25 * 0.07 * 0.0254)
    wall_names = ["walls", "floor"] + list(WINDOW_PATCHES) + ([] if purge else ["lwPurge"])
    walls = "|".join(wall_names)
    purge_u = f"    lwPurge {{ type flowRateInletVelocity; volumetricFlowRate constant {q4:.6g}; extrapolateProfile no; value uniform (0 0 0); }}\n" if purge else ""
    pg = lambda txt: (f"    lwPurge {{ {txt} }}\n" if purge else "")
    files = {
        "0/U": hdr("volVectorField", "U") + f"""dimensions [0 1 -1 0 0 0 0];
internalField uniform (0 0 0);
boundaryField
{{
    inlet {{ type flowRateInletVelocity; volumetricFlowRate constant {q:.6g}; extrapolateProfile no; value uniform (0 0 0); }}
    inlet2 {{ type flowRateInletVelocity; volumetricFlowRate constant {q2:.6g}; extrapolateProfile no; value uniform (0 0 0); }}
{purge_u}    outlet {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}
    "({walls})" {{ type noSlip; }}
}}
""",
        "0/p": hdr("volScalarField", "p") + f"""dimensions [0 2 -2 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "inlet.*" {{ type zeroGradient; }}
{pg("type zeroGradient;")}    outlet {{ type fixedValue; value uniform 0; }}
    "({walls})" {{ type zeroGradient; }}
}}
""",
        "0/k": hdr("volScalarField", "k") + f"""dimensions [0 2 -2 0 0 0 0];
internalField uniform {k_in:.4g};
boundaryField
{{
    "inlet.*" {{ type turbulentIntensityKineticEnergyInlet; intensity 0.05; value uniform {k_in:.4g}; }}
{pg(f"type turbulentIntensityKineticEnergyInlet; intensity 0.05; value uniform {k_in:.4g};")}    outlet {{ type inletOutlet; inletValue uniform {k_in:.4g}; value uniform {k_in:.4g}; }}
    "({walls})" {{ type kqRWallFunction; value uniform {k_in:.4g}; }}
}}
""",
        "0/omega": hdr("volScalarField", "omega") + f"""dimensions [0 0 -1 0 0 0 0];
internalField uniform {w_in:.4g};
boundaryField
{{
    "inlet.*" {{ type turbulentMixingLengthFrequencyInlet; mixingLength {0.07 * 0.0254:.4g}; value uniform {w_in:.4g}; }}
{pg(f"type turbulentMixingLengthFrequencyInlet; mixingLength 0.0005; value uniform {w_in:.4g};")}    outlet {{ type inletOutlet; inletValue uniform {w_in:.4g}; value uniform {w_in:.4g}; }}
    "({walls})" {{ type omegaWallFunction; value uniform {w_in:.4g}; }}
}}
""",
        "0/nut": hdr("volScalarField", "nut") + f"""dimensions [0 2 -1 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "inlet.*" {{ type calculated; value uniform 0; }}
{pg("type calculated; value uniform 0;")}    outlet {{ type calculated; value uniform 0; }}
    "({walls})" {{ type nutUSpaldingWallFunction; value uniform 0; }}
}}
""",
        "constant/transportProperties": hdr("dictionary", "transportProperties") + f"transportModel Newtonian;\nnu {MC.NU:.6g};\n",
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
    wallShearStress {{ type wallShearStress; libs (fieldFunctionObjects); patches (floor walls {' '.join(WINDOW_PATCHES)}); writeControl writeTime; log false; }}
    yPlus {{ type yPlus; libs (fieldFunctionObjects); writeControl writeTime; log false; }}
    pIn {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name inlet; operation areaAverage; fields (p); writeFields false; writeControl timeStep; writeInterval 20; log false; }}
    qOut {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name outlet; operation sum; fields (phi); writeFields false; writeControl timeStep; writeInterval 20; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 20; fields (U p); probeLocations ((0 0 0.003) (0 0 0.010) (0 0.0375 0.003) (0 -0.0375 0.003) (0 0 0.115) (-0.135 -0.018 0.032) (-0.142 -0.018 0.032) (-0.054 -0.072 0.118)); }}
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
    meta = dict(res=args.res, variant=args.variant, upper_lpm=q2 * 60000.0, slide_purge_lpm=0.0, lw_purge_lpm=args.lw_purge_lpm,
                q_lpm=args.q_lpm, q_m3s=q, recoater=args.recoater, x_recoater=P["x_park"], lw_depth=args.lw_depth,
                lp_depth=args.lp_depth, blocks=len(blocks), cells=ncell, lines=dict(x=X, y=Y, z=Z),
                n=dict(x=N[0], y=N[1], z=N[2]), fluid=fluid, solid=solid, rho=MC.RHO, mu=MC.MU, nu=MC.NU,
                slot_v=q / ((2 * MP.INLET_HALF) * 8.0e-6), port_area_m2=a_port, outlet_boot_x_mm=P["_cav"]["xb_o"],
                viewports={k: dict(box=d["box"], patch=d["patch"], face_axis=d["face_axis"], face_at=d["face_at"], area_mm2=d["area_mm2"])
                           for k, d in vp.items()},
                laser_slide=dict(box=(-20.0, 20.0, -20.0, 20.0, P["ch_z"] + 5.0, P["ch_z"] + 6.0), patch="slide", face_axis=2,
                                 face_at=P["ch_z"] + 6.0, area_mm2=1600.0),
                lw_purge=dict(box=purge_box, patch=pname, area_mm2=purge_w * (lw[3] - lw[2])),
                patches={k_: len(v_) for k_, v_ in patches.items()})
    (out / "case_meta.json").write_text(json.dumps(meta, indent=1))
    print(f"{out}: {len(blocks)} blocks, {ncell} cells, Q = {args.q_lpm} + {q2 * 60000:g} L/min, LW purge {args.lw_purge_lpm:g} L/min, "
          f"recoater at x {P['x_park']:g}; patches " + ", ".join(f"{k} {len(v)}" for k, v in patches.items()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--res", choices=("coarse", "fine"), default="coarse")
    ap.add_argument("--q-lpm", type=float, default=200.0)
    ap.add_argument("--iters", type=int, default=800)
    ap.add_argument("--variant", choices=("baseline", "fix"), default="fix")
    ap.add_argument("--upper-lpm", type=float, default=40.0)
    ap.add_argument("--floor-slot-width", type=float, default=0.0)
    ap.add_argument("--lw-purge-lpm", type=float, default=0.0, help="argon across the LW cover slide, L/min (0 = off)")
    ap.add_argument("--lw-depth", type=float, default=4.0, help="LW cover slide's depth below the wall's inner face, mm (assumed)")
    ap.add_argument("--lp-depth", type=float, default=4.0, help="LP cover slide's depth above the lid's inner face, mm (assumed)")
    ap.add_argument("--recoater", choices=("lasing", "park"), default="lasing")
    ap.add_argument("--cad-dir", default=str(ROOT / "cad"))
    ap.add_argument("--out", required=True)
    build(ap.parse_args())
