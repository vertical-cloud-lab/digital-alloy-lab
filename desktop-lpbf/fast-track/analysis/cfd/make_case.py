"""Write an OpenFOAM v2406 case for the fast-track machine's gas (issue #260, PR 294), from geom.py's STL.

Mesh: blockMesh fills the enclosure's inside (box 16 x 12 x 8 in., or the cube) with an anisotropic background grid
(~8 x 12 x 4 mm: finer in z, where the jet and the bed are); snappyHexMesh cuts out the solids of geom.py and refines to
level 3 (1.0 x 1.5 x 0.5 mm) round the jet, the nozzle, the collector and the bed, adds 3 prism layers on the bed,
and topoSet/createPatch carve the purge ports (estimates, not in the CAD model) out of the enclosure walls.

Kinds of case (--kind):
  cross    steady cross-flow: simpleFoam, laminar (--model laminar) or k-omega SST (--model sst); the nozzle at
           --nozzle-lpm (27 L/min = 2.5 m/s in the 45 x 4 slot) is the only inlet, the collector's port the only outlet
  purge    steady flow at the purge's flow (simpleFoam, laminar): --purge-lpm through one purge port (--inlet), the
           nozzle at --nozzle-lpm, out through --outlet (collector or a vent)
  scalar   O2 (as T = x_O2 / 0.2095, air = 1; scalarTransportFoam's field is always T) carried by a purge case's frozen flow (scalarTransportFoam, D = 2e-5 m2/s)
  buoyant  argon displacing air with gravity (rhoReactingBuoyantFoam, species O2 N2 Ar, no reactions, isothermal 25 C)

Gas: argon at 25 C and ~+7 mbar: rho 1.65 kg/m3, mu 22.6 uPa s (as PR 266's cases).

Run (writes the case to --out; nothing in the repo):
    /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/geom.py --state FT-1 --out /tmp/ft-cfd/geom/ft1
    /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/make_case.py --geom /tmp/ft-cfd/geom/ft1 --kind cross \
        --model laminar --out /tmp/ft-cfd/cross-lam
    /tmp/tools/capmem 4 bash desktop-lpbf/fast-track/analysis/cfd/run_case.sh /tmp/ft-cfd/cross-lam mesh solve
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import shutil

RHO = 1.65            # kg/m3, Ar at 298 K and ~1020 mbar
MU = 2.26e-5          # Pa s
NU = MU / RHO
D_O2_AR = 2.0e-5      # m2/s, O2 in Ar at 298 K, 1 atm (Chapman-Enskog; ~0.20 cm2/s)
X_O2_AIR = 0.2095

PATCHES_STL = ("inlet", "outlet", "bed", "slide", "nozzle", "collector", "hopper", "blade", "block", "deck",
               "recoater", "pipes", "window", "frame")


def ports(enc):
    """Purge ports on the enclosure walls (estimates; the CAD model has only the nozzle feed and the exhaust
    bulkheads). (x0, x1, y0, y1, z0, z1) in mm, as thin boxes straddling the wall."""
    x0, x1, y0, y1, z0, z1 = enc
    ym = 0.5 * (y0 + y1)
    return {
        # 40 x 40 mm diffuser faces (a sintered-metal or mesh diffuser on the bulkhead), left wall, mid-depth
        "purge_low": (x0 - 1, x0 + 1, ym - 20, ym + 20, z0 + 3, z0 + 43),
        "purge_high": (x0 - 1, x0 + 1, ym - 20, ym + 20, z1 - 43, z1 - 3),
        # 40 x 20 mm vents, right wall, at the back
        "vent_high": (x1 - 1, x1 + 1, y1 - 60, y1 - 20, z1 - 23, z1 - 3),
        "vent_low": (x1 - 1, x1 + 1, y1 - 60, y1 - 20, z0 + 3, z0 + 23),
    }


def hdr(cls, obj, loc=""):
    return ("FoamFile\n{\n    version 2.0;\n    format ascii;\n    class %s;\n%s    object %s;\n}\n"
            % (cls, ('    location "%s";\n' % loc) if loc else "", obj))


def mesh_files(g, res, profile="cross"):
    """blockMeshDict, surfaceFeatureExtractDict, snappyHexMeshDict, topoSetDict, createPatchDict."""
    x0, x1, y0, y1, z0, z1 = g["enclosure"]
    f = {"coarse": 1.6, "medium": 1.0, "fine": 0.8}[res]
    h = (8.0 * f, 12.0 * f, 4.0 * f)
    n = [max(1, round((b - a) / hh)) for (a, b), hh in zip(((x0, x1), (y0, y1), (z0, z1)), h)]
    files = {}
    files["system/blockMeshDict"] = hdr("dictionary", "blockMeshDict", "system") + f"""scale 0.001;
vertices ( ({x0} {y0} {z0}) ({x1} {y0} {z0}) ({x1} {y1} {z0}) ({x0} {y1} {z0})
           ({x0} {y0} {z1}) ({x1} {y0} {z1}) ({x1} {y1} {z1}) ({x0} {y1} {z1}) );
blocks ( hex (0 1 2 3 4 5 6 7) ({n[0]} {n[1]} {n[2]}) simpleGrading (1 1 1) );
edges ();
boundary ( walls {{ type wall; faces ( (0 3 2 1) (4 5 6 7) (0 4 7 3) (1 2 6 5) (0 1 5 4) (3 7 6 2) ); }} );
"""
    files["system/surfaceFeatureExtractDict"] = hdr("dictionary", "surfaceFeatureExtractDict", "system") + """ft.stl
{
    extractionMethod extractFromSurface;
    includedAngle 150;
    subsetFeatures { nonManifoldEdges no; openEdges yes; }
    writeObj no;
}
"""
    zb = g["zb"]
    sl, co = g["slot"], g["collector"]
    m = 1e-3
    jet = ((-sl["w"] / 2 - 8) * m, (sl["y_inlet"] - 1) * m, (zb - 2) * m,
           (sl["w"] / 2 + 8) * m, (co["y_outlet"] + 1) * m, (zb + max(sl["z0"] + sl["h"], co["z1"]) + 5) * m)
    near = (-50 * m, -55 * m, (zb - 2) * m, 55 * m, 50 * m, (zb + 30) * m)
    zs = g["z_slide"]
    top = (-45 * m, -45 * m, (zs - 12) * m, 45 * m, 45 * m, (z1 + 1) * m)
    regions = "\n".join(f"            {r} {{ name {r}; }}" for r in PATCHES_STL if r in g["regions"])
    lv = dict(inlet=3, outlet=3, bed=3, nozzle=3, collector=3, blade=3, hopper=2, block=2, pipes=2, window=1, slide=2,
              deck=1, recoater=1, frame=1)
    if profile == "purge":          # box-scale purge runs: no jet refinement, so the time step is set by the box flow
        lv = {k: min(v, 3 if k in ("inlet", "outlet", "nozzle", "collector") else 1) for k, v in lv.items()}
    rs = "\n".join(f"                {r} {{ level ({lv[r]} {lv[r]}); patchInfo {{ type {'patch' if r in ('inlet', 'outlet') else 'wall'}; }} }}"
                   for r in PATCHES_STL if r in g["regions"])
    loc = ((x0 + 25.3) * m, (y1 - 15.7) * m, (z1 - 30.1) * m)
    regs = ("        jet  { mode inside; levels ((1e15 3)); }\n        near { mode inside; levels ((1e15 2)); }\n"
            "        top  { mode inside; levels ((1e15 1)); }") if profile == "cross" else "        top  { mode inside; levels ((1e15 1)); }"
    layers = "addLayers true;" if profile == "cross" else "addLayers false;"
    files["system/snappyHexMeshDict"] = hdr("dictionary", "snappyHexMeshDict", "system") + f"""castellatedMesh true;
snap true;
{layers}
geometry
{{
    ft.stl
    {{
        type triSurfaceMesh;
        name ft;
        regions
        {{
{regions}
        }}
    }}
    jet  {{ type searchableBox; min ({jet[0]:.6g} {jet[1]:.6g} {jet[2]:.6g}); max ({jet[3]:.6g} {jet[4]:.6g} {jet[5]:.6g}); }}
    near {{ type searchableBox; min ({near[0]:.6g} {near[1]:.6g} {near[2]:.6g}); max ({near[3]:.6g} {near[4]:.6g} {near[5]:.6g}); }}
    top  {{ type searchableBox; min ({top[0]:.6g} {top[1]:.6g} {top[2]:.6g}); max ({top[3]:.6g} {top[4]:.6g} {top[5]:.6g}); }}
}};
castellatedMeshControls
{{
    maxLocalCells 3000000;
    maxGlobalCells 6000000;
    minRefinementCells 5;
    maxLoadUnbalance 0.10;
    nCellsBetweenLevels 3;
    features ( {{ file "ft.eMesh"; level 1; }} );
    refinementSurfaces
    {{
        ft
        {{
            level (1 1);
            regions
            {{
{rs}
            }}
        }}
    }}
    resolveFeatureAngle 30;
    refinementRegions
    {{
{regs}
    }}
    locationInMesh ({loc[0]:.6g} {loc[1]:.6g} {loc[2]:.6g});
    allowFreeStandingZoneFaces true;
}}
snapControls
{{
    nSmoothPatch 3;
    tolerance 2.0;
    nSolveIter 50;
    nRelaxIter 5;
    nFeatureSnapIter 10;
    implicitFeatureSnap false;
    explicitFeatureSnap true;
    multiRegionFeatureSnap false;
}}
addLayersControls
{{
    relativeSizes true;
    layers {{ bed {{ nSurfaceLayers 3; }} }}
    expansionRatio 1.3;
    finalLayerThickness 0.45;
    minThickness 0.1;
    nGrow 0;
    featureAngle 100;
    slipFeatureAngle 30;
    nRelaxIter 3;
    nSmoothSurfaceNormals 1;
    nSmoothNormals 3;
    nSmoothThickness 10;
    maxFaceThicknessRatio 0.5;
    maxThicknessToMedialRatio 0.3;
    minMedialAxisAngle 90;
    nBufferCellsNoExtrude 0;
    nLayerIter 50;
}}
meshQualityControls
{{
    maxNonOrtho 65;
    maxBoundarySkewness 20;
    maxInternalSkewness 4;
    maxConcave 80;
    minVol 1e-16;
    minTetQuality 1e-15;
    minArea -1;
    minTwist 0.02;
    minDeterminant 0.001;
    minFaceWeight 0.05;
    minVolRatio 0.01;
    minTriangleTwist -1;
    nSmoothScale 4;
    errorReduction 0.75;
    relaxed {{ maxNonOrtho 75; }}
}}
mergeTolerance 1e-6;
"""
    P = ports(g["enclosure"])
    actions = "\n".join(f"    {{ name {k}Faces; type faceSet; action new; source boxToFace; box ({b[0] * m:.6g} {b[2] * m:.6g} {b[4] * m:.6g}) ({b[1] * m:.6g} {b[3] * m:.6g} {b[5] * m:.6g}); }}\n"
                        f"    {{ name {k}Faces; type faceSet; action subset; source patchToFace; patch walls; }}"
                        for k, b in P.items())
    files["system/topoSetDict"] = hdr("dictionary", "topoSetDict", "system") + f"actions\n(\n{actions}\n);\n"
    cp = "\n".join(f"    {{ name {k}; patchInfo {{ type patch; }} constructFrom set; set {k}Faces; }}" for k in P)
    files["system/createPatchDict"] = hdr("dictionary", "createPatchDict", "system") + f"pointSync false;\npatches\n(\n{cp}\n);\n"
    files["system/meshQualityDict"] = hdr("dictionary", "meshQualityDict", "system") + \
        '#includeEtc "caseDicts/mesh/generation/meshQualityDict"\n'
    return files, dict(background_cells=n, background_h_mm=[round((b - a) / k, 3) for (a, b), k in
                                                             zip(((x0, x1), (y0, y1), (z0, z1)), n)])


WALLS = '"(walls|bed|slide|nozzle|collector|hopper|blade|block|deck|recoater|pipes|window|frame)"'
PORTS = ("purge_low", "purge_high", "vent_high", "vent_low")


def flow_setup(a):
    """{patch: L/min in} for inlets and the outlet's name, by kind."""
    if a.kind == "cross":
        return {"inlet": a.nozzle_lpm}, "outlet"
    ins = {"inlet": a.nozzle_lpm} if a.nozzle_lpm > 0 else {}          # nozzle off: its patch is a closed wall
    if a.inlet != "none":
        ins[a.inlet] = a.purge_lpm
    return ins, a.outlet


def u_p_files(a, g):
    ins, out = flow_setup(a)
    closed = [p for p in ("inlet", "outlet") + PORTS if p not in ins and p != out]
    ub = []
    for p, q in ins.items():
        ub.append(f"    {p} {{ type flowRateInletVelocity; volumetricFlowRate constant {q / 60000.0:.6g}; extrapolateProfile no; value uniform (0 0 0); }}")
    ub.append(f"    {out} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}")
    for p in closed:
        ub.append(f"    {p} {{ type noSlip; }}")
    ub.append(f"    {WALLS} {{ type noSlip; }}")
    pb = [f'    "({"|".join(list(ins) + closed)})" {{ type zeroGradient; }}', f"    {out} {{ type fixedValue; value uniform 0; }}",
          f"    {WALLS} {{ type zeroGradient; }}"]
    U = hdr("volVectorField", "U") + "dimensions [0 1 -1 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField\n{\n" + "\n".join(ub) + "\n}\n"
    p = hdr("volScalarField", "p") + "dimensions [0 2 -2 0 0 0 0];\ninternalField uniform 0;\nboundaryField\n{\n" + "\n".join(pb) + "\n}\n"
    return {"0/U": U, "0/p": p}, ins, out, closed


def turb_files(a, ins, out, closed):
    if a.model == "laminar":
        return {"constant/turbulenceProperties": hdr("dictionary", "turbulenceProperties") + "simulationType laminar;\n"}
    q = ins["inlet"] / 60000.0
    a_in = 45e-3 * 4e-3
    k_in = 1.5 * (0.05 * q / a_in) ** 2
    lm = 0.07 * 4e-3
    w_in = math.sqrt(k_in) / (0.09 ** 0.25 * lm)
    allin = "|".join(ins)
    shut = "|".join(closed)
    fl = {}
    # closed ports are 'patch' type (carved by createPatch), so no wall functions there: zero gradient, nut 0
    closed_kw = f'    "({shut})" {{ type zeroGradient; }}\n' if shut else ""
    for name, val, inbc, wall in (("k", k_in, f"turbulentIntensityKineticEnergyInlet; intensity 0.05; value uniform {k_in:.4g}", "kqRWallFunction"),
                                  ("omega", w_in, f"turbulentMixingLengthFrequencyInlet; mixingLength {lm:.4g}; value uniform {w_in:.4g}", "omegaWallFunction")):
        dim = "[0 2 -2 0 0 0 0]" if name == "k" else "[0 0 -1 0 0 0 0]"
        fl[f"0/{name}"] = hdr("volScalarField", name) + f"""dimensions {dim};
internalField uniform {val:.4g};
boundaryField
{{
    "({allin})" {{ type {inbc}; }}
    {out} {{ type inletOutlet; inletValue uniform {val:.4g}; value uniform {val:.4g}; }}
    {WALLS} {{ type {wall}; value uniform {val:.4g}; }}
{closed_kw}}}
"""
    fl["0/nut"] = hdr("volScalarField", "nut") + f"""dimensions [0 2 -1 0 0 0 0];
internalField uniform 0;
boundaryField
{{
    "({allin}|{out})" {{ type calculated; value uniform 0; }}
    {WALLS} {{ type nutLowReWallFunction; value uniform 0; }}
{'    "(' + shut + ')" { type calculated; value uniform 0; }' if shut else ''}
}}
"""
    fl["constant/turbulenceProperties"] = hdr("dictionary", "turbulenceProperties") + \
        "simulationType RAS;\nRAS\n{\n    RASModel kOmegaSST;\n    turbulence on;\n    printCoeffs on;\n}\n"
    return fl


def steady_files(a, g):
    files, ins, out, closed = u_p_files(a, g)
    files.update(turb_files(a, ins, out, closed))
    files["constant/transportProperties"] = hdr("dictionary", "transportProperties") + f"transportModel Newtonian;\nnu {NU:.6g};\n"
    zb = g["zb"]
    probes = " ".join(f"(0 0 {(zb + z) * 1e-3:.6g})" for z in (1, 3, 5)) + \
        f" (0 -0.015 {(zb + 3) * 1e-3:.6g}) (0 0.015 {(zb + 3) * 1e-3:.6g}) (0 0 {(g['z_slide'] - 2) * 1e-3:.6g})"
    turb_fo = "    yPlus { type yPlus; libs (fieldFunctionObjects); writeControl writeTime; log false; }\n" if a.model == "sst" else ""
    files["system/controlDict"] = hdr("dictionary", "controlDict") + f"""application simpleFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime {a.iters};
deltaT 1;
writeControl timeStep;
writeInterval {a.iters};
purgeWrite 2;
writeFormat binary;
writePrecision 8;
writeCompression off;
timeFormat general;
runTimeModifiable true;
functions
{{
    wallShearStress {{ type wallShearStress; libs (fieldFunctionObjects); patches (bed slide); writeControl writeTime; log false; }}
{turb_fo}    pIn {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name inlet; operation areaAverage; fields (p); writeFields false; writeControl timeStep; writeInterval 10; log false; }}
    qOut {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name {out}; operation sum; fields (phi); writeFields false; writeControl timeStep; writeInterval 10; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 10; fields (U p); probeLocations ({probes}); }}
}}
"""
    div_t = "    div(phi,k) bounded Gauss limitedLinear 1;\n    div(phi,omega) bounded Gauss limitedLinear 1;\n" if a.model == "sst" else ""
    files["system/fvSchemes"] = hdr("dictionary", "fvSchemes") + f"""ddtSchemes {{ default steadyState; }}
gradSchemes {{ default Gauss linear; grad(U) cellLimited Gauss linear 1; grad(k) cellLimited Gauss linear 1; grad(omega) cellLimited Gauss linear 1; }}
divSchemes
{{
    default none;
    div(phi,U) bounded Gauss linearUpwind grad(U);
{div_t}    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}}
laplacianSchemes {{ default Gauss linear limited corrected 0.5; }}
interpolationSchemes {{ default linear; }}
snGradSchemes {{ default limited corrected 0.5; }}
wallDist {{ method meshWave; }}
"""
    files["system/fvSolution"] = hdr("dictionary", "fvSolution") + """solvers
{
    p { solver GAMG; tolerance 1e-8; relTol 0.05; smoother GaussSeidel; }
    "(U|k|omega)" { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-9; relTol 0.1; }
}
SIMPLE
{
    nNonOrthogonalCorrectors 1;
    consistent yes;
    residualControl { p 1e-6; U 1e-7; "(k|omega)" 1e-7; }
}
relaxationFactors
{
    fields { p 1; }
    equations { U 0.7; k 0.6; omega 0.6; }
}
"""
    if a.transient:
        # pimpleFoam from a steady solution (run_case.sh 'map'), time-averaged after --avg-from s: U, p and the bed shear
        files["system/controlDict"] = hdr("dictionary", "controlDict") + f"""application pimpleFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime {a.t_end};
deltaT 2e-4;
adjustTimeStep yes;
maxCo {a.max_co};
maxDeltaT 1e-3;
writeControl adjustableRunTime;
writeInterval {a.t_write};
purgeWrite 2;
writeFormat binary;
writePrecision 8;
writeCompression off;
timeFormat general;
runTimeModifiable true;
functions
{{
    wallShearStress {{ type wallShearStress; libs (fieldFunctionObjects); patches (bed slide); writeControl writeTime; log false; }}
    avg {{ type fieldAverage; libs (fieldFunctionObjects); timeStart {a.avg_from}; writeControl writeTime;
          fields ( U {{ mean on; prime2Mean off; base time; }} p {{ mean on; prime2Mean off; base time; }}
                   wallShearStress {{ mean on; prime2Mean off; base time; }} ); }}
{turb_fo}    pIn {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name inlet; operation areaAverage; fields (p); writeFields false; writeControl timeStep; writeInterval 5; log false; }}
    qOut {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name {out}; operation sum; fields (phi); writeFields false; writeControl timeStep; writeInterval 5; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 5; fields (U p); probeLocations ({probes}); }}
}}
"""
        files["system/fvSchemes"] = files["system/fvSchemes"].replace("ddtSchemes { default steadyState; }", "ddtSchemes { default backward; }").replace(
            "div(phi,U) bounded Gauss linearUpwind grad(U);", "div(phi,U) Gauss linearUpwind grad(U);").replace(
            "div(phi,k) bounded", "div(phi,k)").replace("div(phi,omega) bounded", "div(phi,omega)")
        files["system/fvSolution"] = hdr("dictionary", "fvSolution") + """solvers
{
    p { solver GAMG; tolerance 1e-7; relTol 0.01; smoother GaussSeidel; }
    pFinal { $p; relTol 0; }
    "(U|k|omega)" { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0.05; }
    "(U|k|omega)Final" { $U; relTol 0; }
}
PIMPLE
{
    momentumPredictor yes;
    nOuterCorrectors 1;
    nCorrectors 2;
    nNonOrthogonalCorrectors 1;
}
"""
    return files, dict(inlets=ins, outlet=out, closed=closed)


def scalar_files(a, g):
    """scalarTransportFoam on a solved purge case's U and phi (copied in by run_case.sh's 'scalar' step)."""
    ins, out = flow_setup(a)
    closed = [p for p in ("inlet", "outlet") + PORTS if p not in ins and p != out]
    cb = [f'    "({"|".join(ins)})" {{ type fixedValue; value uniform 0; }}',
          f"    {out} {{ type inletOutlet; inletValue uniform 0; value uniform 1; }}",
          f'    "({WALLS[2:-2]}{"|" + "|".join(closed) if closed else ""})" {{ type zeroGradient; }}']
    files = {"0/T": hdr("volScalarField", "T") + "dimensions [0 0 0 0 0 0 0];\ninternalField uniform 1;\nboundaryField\n{\n" + "\n".join(cb) + "\n}\n"}
    zb = g["zb"]
    pts = f"(0 0 {(zb + 1) * 1e-3:.6g}) (0 0 {(zb + 5) * 1e-3:.6g}) (0 0 {(g['z_slide'] - 2) * 1e-3:.6g})"
    files["system/controlDict"] = hdr("dictionary", "controlDict") + f"""application scalarTransportFoam;
startFrom startTime;
startTime 0;
stopAt endTime;
endTime {a.t_end};
deltaT {a.dt};
writeControl runTime;
writeInterval {a.t_write};
purgeWrite 0;
writeFormat binary;
writePrecision 8;
writeCompression off;
timeFormat general;
runTimeModifiable true;
functions
{{
    boxAvg {{ type volFieldValue; libs (fieldFunctionObjects); fields (T); operation volAverage; regionType all; writeFields false; writeControl timeStep; writeInterval 2; log false; }}
    exhaust {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name {out}; operation weightedAverage; weightField phi; fields (T); writeFields false; writeControl timeStep; writeInterval 2; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 2; fields (T); probeLocations ({pts}); }}
}}
"""
    files["constant/transportProperties"] = hdr("dictionary", "transportProperties") + f"DT {D_O2_AR:g};\n"
    files["system/fvSchemes"] = hdr("dictionary", "fvSchemes") + """ddtSchemes { default Euler; }
gradSchemes { default Gauss linear; }
divSchemes { default none; div(phi,T) Gauss limitedLinear01 1; }
laplacianSchemes { default Gauss linear limited corrected 0.5; }
interpolationSchemes { default linear; }
snGradSchemes { default limited corrected 0.5; }
"""
    files["system/fvSolution"] = hdr("dictionary", "fvSolution") + """solvers
{
    T { solver PBiCGStab; preconditioner DILU; tolerance 1e-11; relTol 0; }
}
SIMPLE { nNonOrthogonalCorrectors 1; }
"""
    return files, dict(inlets=ins, outlet=out, closed=closed)


def buoyant_files(a, g):
    """rhoReactingBuoyantFoam: O2, N2, Ar, no reactions, 25 C, gravity -z. Species diffuse with Sc = 1 (mu)."""
    ins, out = flow_setup(a)
    closed = [p for p in ("inlet", "outlet") + PORTS if p not in ins and p != out]
    allin = "|".join(ins)
    wall_re = WALLS[2:-2] + ("|" + "|".join(closed) if closed else "")
    f = {}
    ub = [f"    {p} {{ type flowRateInletVelocity; volumetricFlowRate constant {q / 60000.0:.6g}; extrapolateProfile no; value uniform (0 0 0); }}" for p, q in ins.items()]
    # outflow only (the exhaust's check valve): with pressureInletOutletVelocity and a uniform static pressure, the
    # 0.3 Pa hydrostatic head across a 20 mm vent beat the ~0.15 Pa that drives the outflow and air flowed back in at
    # the vent's top (seen in the first low-inlet run)
    ub += [f"    {out} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}", f'    "({wall_re})" {{ type noSlip; }}']
    f["0/U"] = hdr("volVectorField", "U") + "dimensions [0 1 -1 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField\n{\n" + "\n".join(ub) + "\n}\n"
    p0 = 101325.0 + 700.0
    f["0/p"] = hdr("volScalarField", "p") + f"""dimensions [1 -1 -2 0 0 0 0];
internalField uniform {p0};
boundaryField
{{
    "({allin}|{wall_re})" {{ type calculated; value uniform {p0}; }}
    {out} {{ type calculated; value uniform {p0}; }}
}}
"""
    f["0/p_rgh"] = hdr("volScalarField", "p_rgh") + f"""dimensions [1 -1 -2 0 0 0 0];
internalField uniform {p0};
boundaryField
{{
    "({allin}|{wall_re})" {{ type fixedFluxPressure; value uniform {p0}; }}
    {out} {{ type prghPressure; p uniform {p0}; value uniform {p0}; }}
}}
"""
    f["0/T"] = hdr("volScalarField", "T") + f"""dimensions [0 0 0 1 0 0 0];
internalField uniform 298.15;
boundaryField
{{
    "({allin})" {{ type fixedValue; value uniform 298.15; }}
    {out} {{ type inletOutlet; inletValue uniform 298.15; value uniform 298.15; }}
    "({wall_re})" {{ type zeroGradient; }}
}}
"""
    # air by mass: O2 0.2314, N2 0.7552, Ar 0.0134 (dry air); the inlets are pure argon
    for sp, air, inl in (("O2", 0.2314, 0.0), ("N2", 0.7552, 0.0), ("Ar", 0.0134, 1.0), ("Ydefault", 0.0, 0.0)):
        f[f"0/{sp}"] = hdr("volScalarField", sp) + f"""dimensions [0 0 0 0 0 0 0];
internalField uniform {air};
boundaryField
{{
    "({allin})" {{ type fixedValue; value uniform {inl}; }}
    {out} {{ type inletOutlet; inletValue uniform {inl}; value uniform {air}; }}
    "({wall_re})" {{ type zeroGradient; }}
}}
"""
    f["0/alphat"] = hdr("volScalarField", "alphat") + """dimensions [1 -1 -1 0 0 0 0];
internalField uniform 0;
boundaryField { ".*" { type calculated; value uniform 0; } }
"""
    f["constant/g"] = hdr("uniformDimensionedVectorField", "g") + "dimensions [0 1 -2 0 0 0 0];\nvalue (0 0 -9.81);\n"
    f["constant/turbulenceProperties"] = hdr("dictionary", "turbulenceProperties") + "simulationType laminar;\n"
    f["constant/chemistryProperties"] = hdr("dictionary", "chemistryProperties") + """chemistryType { solver none; }
chemistry off;
initialChemicalTimeStep 1e-7;
"""
    f["constant/combustionProperties"] = hdr("dictionary", "combustionProperties") + "combustionModel none;\n"
    f["constant/reactions"] = "species ( O2 N2 Ar );\nreactions {}\n"
    # JANAF coefficients (OpenFOAM's thermoData), Sutherland viscosity; Ar's As/Ts fitted to 22.6 uPa s at 298 K
    f["constant/thermo.compressibleGas"] = """O2
{
    specie { molWeight 31.9988; }
    thermodynamics { Tlow 200; Thigh 5000; Tcommon 1000;
        highCpCoeffs ( 3.69758 0.00061352 -1.25884e-07 1.77528e-11 -1.13644e-15 -1233.93 3.18917 );
        lowCpCoeffs ( 3.21294 0.00112749 -5.75615e-07 1.31388e-09 -8.76855e-13 -1005.25 6.03474 ); }
    transport { As 1.67212e-06; Ts 170.672; }
}
N2
{
    specie { molWeight 28.0134; }
    thermodynamics { Tlow 200; Thigh 5000; Tcommon 1000;
        highCpCoeffs ( 2.92664 0.00148798 -5.68476e-07 1.0097e-10 -6.75335e-15 -922.798 5.98053 );
        lowCpCoeffs ( 3.29868 0.00140824 -3.96322e-06 5.64152e-09 -2.44486e-12 -1020.9 3.95037 ); }
    transport { As 1.67212e-06; Ts 170.672; }
}
Ar
{
    specie { molWeight 39.948; }
    thermodynamics { Tlow 200; Thigh 5000; Tcommon 1000;
        highCpCoeffs ( 2.5 0 0 0 0 -745.375 4.366 );
        lowCpCoeffs ( 2.5 0 0 0 0 -745.375 4.366 ); }
    transport { As 1.93e-06; Ts 144.0; }
}
"""
    f["constant/thermophysicalProperties"] = hdr("dictionary", "thermophysicalProperties") + """thermoType
{
    type heRhoThermo;
    mixture reactingMixture;
    transport sutherland;
    thermo janaf;
    energy sensibleEnthalpy;
    equationOfState perfectGas;
    specie specie;
}
dpdt no;
inertSpecie N2;
chemistryReader foamChemistryReader;
foamChemistryFile "<constant>/reactions";
foamChemistryThermoFile "<constant>/thermo.compressibleGas";
"""
    zb = g["zb"]
    pts = f"(0 0 {(zb + 1) * 1e-3:.6g}) (0 0 {(zb + 5) * 1e-3:.6g}) (0 0 {(g['z_slide'] - 2) * 1e-3:.6g})"
    f["system/controlDict"] = hdr("dictionary", "controlDict") + f"""application rhoReactingBuoyantFoam;
startFrom latestTime;
startTime 0;
stopAt endTime;
endTime {a.t_end};
deltaT 0.002;
writeControl adjustableRunTime;
writeInterval {a.t_write};
purgeWrite 0;
writeFormat binary;
writePrecision 8;
writeCompression off;
timeFormat general;
runTimeModifiable true;
adjustTimeStep yes;
maxCo {a.max_co};
maxDeltaT 0.25;
functions
{{
    boxAvg {{ type volFieldValue; libs (fieldFunctionObjects); fields (O2 N2 Ar); operation volAverage; regionType all; writeFields false; writeControl timeStep; writeInterval 5; log false; }}
    exhaust {{ type surfaceFieldValue; libs (fieldFunctionObjects); regionType patch; name {out}; operation weightedAverage; weightField phi; fields (O2 N2 Ar); writeFields false; writeControl timeStep; writeInterval 5; log false; }}
    probes {{ type probes; libs (sampling); writeControl timeStep; writeInterval 5; fields (O2 Ar U); probeLocations ({pts}); }}
}}
"""
    f["system/fvSchemes"] = hdr("dictionary", "fvSchemes") + """ddtSchemes { default Euler; }
gradSchemes { default Gauss linear; }
divSchemes
{
    default none;
    div(phi,U) Gauss limitedLinearV 1;
    div(phi,Yi_h) Gauss limitedLinear01 1;
    div(phi,K) Gauss linear;
    div(phid,p) Gauss limitedLinear 1;
    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}
laplacianSchemes { default Gauss linear limited corrected 0.5; }
interpolationSchemes { default linear; }
snGradSchemes { default limited corrected 0.5; }
fluxRequired { default no; p_rgh; }
"""
    f["system/fvSolution"] = hdr("dictionary", "fvSolution") + """solvers
{
    "rho.*" { solver diagonal; }
    p_rgh { solver GAMG; smoother GaussSeidel; tolerance 1e-5; relTol 0.01; maxIter 100; }
    p_rghFinal { $p_rgh; tolerance 1e-5; relTol 0.001; }
    "(U|h|e|k|epsilon|Yi)" { solver PBiCGStab; preconditioner DILU; tolerance 1e-9; relTol 0.05; }
    "(U|h|e|k|epsilon|Yi)Final" { $U; relTol 0; }
}
PIMPLE
{
    momentumPredictor yes;
    nOuterCorrectors 2;
    nCorrectors 2;
    nNonOrthogonalCorrectors 1;
}
relaxationFactors { equations { ".*" 1; } }
"""
    return f, dict(inlets=ins, outlet=out, closed=closed)


def build(a):
    g = json.loads((pathlib.Path(a.geom) / "geom.json").read_text())
    out = pathlib.Path(a.out)
    for d in ("system", "constant/triSurface", "0"):
        (out / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(pathlib.Path(a.geom) / "ft.stl", out / "constant/triSurface/ft.stl")
    files, mesh_meta = mesh_files(g, a.res, a.profile)
    if a.kind in ("cross", "purge"):
        f2, fm = steady_files(a, g)
    elif a.kind == "scalar":
        f2, fm = scalar_files(a, g)
    else:
        f2, fm = buoyant_files(a, g)
    files.update(f2)
    files["system/decomposeParDict"] = hdr("dictionary", "decomposeParDict") + "numberOfSubdomains 2;\nmethod scotch;\n"
    for name, txt in files.items():
        (out / name).write_text(txt)
    (out / "case.foam").write_text("")
    meta = dict(kind=a.kind, model=a.model, res=a.res, transient=a.transient, avg_from=a.avg_from, geom=g, ports=ports(g["enclosure"]), rho=RHO, mu=MU, nu=NU,
                nozzle_lpm=a.nozzle_lpm, purge_lpm=a.purge_lpm if a.kind != "cross" else 0.0, **mesh_meta, **fm)
    (out / "case_meta.json").write_text(json.dumps(meta, indent=1, default=float))
    print(f"{out}: {a.kind} {a.model} {a.res}; background {mesh_meta['background_cells']} cells of {mesh_meta['background_h_mm']} mm; "
          f"in {fm['inlets']} L/min, out {fm['outlet']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--geom", required=True, help="folder written by geom.py (ft.stl, geom.json)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kind", choices=("cross", "purge", "scalar", "buoyant"), default="cross")
    ap.add_argument("--model", choices=("laminar", "sst"), default="laminar")
    ap.add_argument("--res", choices=("coarse", "medium", "fine"), default="medium")
    ap.add_argument("--nozzle-lpm", type=float, default=27.0)
    ap.add_argument("--purge-lpm", type=float, default=15.0)
    ap.add_argument("--inlet", choices=("none",) + PORTS[:2], default="none", help="purge port used as an inlet")
    ap.add_argument("--outlet", choices=("outlet",) + PORTS[2:], default="outlet", help="the exhaust: the collector's port or a vent")
    ap.add_argument("--iters", type=int, default=2000)
    ap.add_argument("--t-end", type=float, default=2700.0)
    ap.add_argument("--t-write", type=float, default=300.0)
    ap.add_argument("--dt", type=float, default=0.5)
    ap.add_argument("--max-co", type=float, default=4.0)
    ap.add_argument("--profile", choices=("cross", "purge"), default="cross",
                    help="mesh: 'cross' refines the jet to 0.5 mm with bed layers; 'purge' is box-scale only (buoyant runs)")
    ap.add_argument("--transient", action="store_true", help="cross/purge: pimpleFoam with time-averaging instead of simpleFoam")
    ap.add_argument("--avg-from", type=float, default=0.1, help="transient: start of the time average, s")
    build(ap.parse_args())
