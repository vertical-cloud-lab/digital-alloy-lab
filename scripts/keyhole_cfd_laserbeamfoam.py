"""laserbeamFoam runs at the AM module's melt-pool points, and their post-processing (issue #235).

The keyhole write-up (arroyave-orchid-tools/keyhole-alternatives/README.md) named an open thermal-fluid
code as the only open way to get keyhole-mode pool width and length, with laserbeamFoam
(github.com/laserbeamfoam/LaserbeamFoam, GPL-3.0; Flint et al. 2023, SoftwareX 21, 101299,
doi:10.1016/j.softx.2022.101299) first. This script writes laserbeamFoam cases at the points where the
in-house Thermo-Calc AM-module results have a 3D melt-pool render, plus one more map point:

* ``alsi10mg``: AlSi10Mg, 250 W, 0.9 m/s, Gaussian 1/e^2 radius 40 um, 150 C plate (render; map: no defect);
* ``alsi10mg_350W``: the same at 350 W, the next grid point the AM map calls keyhole at 0.9 m/s;
* ``blend``: BYU AA1100 + Si + AlSi10Mg blend (Al-24Si), 375 W, 0.4 m/s, 45 um, 30 C plate (render; keyhole).

It then reads the fields back and measures the melt pool (liquid metal above the liquidus, and above the
solidus) and the keyhole (gas below the original surface) at each write, and the absorbed power from the
solver log; and it draws the time histories and sections.

Choices, kept the same as the cheap models in scripts/keyhole_open_models.py where they overlap:

* k 110 W/m/K, rho 2650 kg/m^3 and c_p 1040 J/kg/K, constant, for solid and liquid alike;
* liquidus/solidus from MatCalc mc_al (868.6/842.7 K AlSi10Mg, 1019.3/846.7 K blend);
* latent heat of fusion from the mass-weighted pure-element values (Al 397 kJ/kg, Si 1790 kJ/kg);
* pure-Al vapour (T_b 2743 K, 10.9 MJ/kg, 26.98 g/mol) for recoil pressure and evaporative cooling;
* liquid Al-Si surface tension 0.86 N/m, dsigma/dT -3.5e-4 N/m/K, kinematic viscosity 4.9e-7 m^2/s;
* absorptivity, one of two ways:
  - by default laserbeamFoam traces rays and takes each bounce's absorption from the Fresnel equations
    with a Drude permittivity (free-electron density 1.81e29 m^-3, three electrons per Al atom; liquid
    electrical resistivity 4.0e-7 Ohm m, or ``--elec-resistivity``), at 1070 nm;
  - with ``--absorbed-fraction A`` the beam power is set to A*P and every ray deposits all of it where it
    first meets the metal, which fixes the absorbed power at the AM module's;
* bare plate, no powder layer; full 3D domain (the ray tracing has no symmetry-plane reflection).

The mesh is uniform and coarse (``--dx``), because the runs had to fit on a 4-vCPU runner.

Usage (OpenFOAM v2506 sourced, laserbeamFoam built; the committed cases are in
arroyave-orchid-tools/keyhole-alternatives/cfd/cases/):

    python scripts/keyhole_cfd_laserbeamfoam.py setup --case blend --dx 17.5e-6 --end-time 1.6e-3 \
        --absorbed-fraction 0.3841 --out /tmp/cfd/blend-matchedA
    (cd /tmp/cfd/blend-matchedA && ./Allrun 2)   # blockMesh, setFields, decomposePar, mpirun -np 2
    (cd /tmp/cfd/blend-matchedA && reconstructPar -fields '(T alpha.metal U)')
    python scripts/keyhole_cfd_laserbeamfoam.py post --case-dir /tmp/cfd/blend-matchedA --out <dir>
    python scripts/keyhole_cfd_laserbeamfoam.py figures --post-dir <dir> --case-dirs /tmp/cfd/<run> ... --out <dir>
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import textwrap

import numpy as np

HEADER = """/*--------------------------------*- C++ -*----------------------------------*\\
  Written by scripts/keyhole_cfd_laserbeamfoam.py (digital-alloy-lab, issue #235)
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       {cls};
    object      {obj};
}}
"""

L_FUSION_AL = 3.97e5  # J/kg
L_FUSION_SI = 1.79e6  # J/kg

CASES = {
    "alsi10mg": {
        "label": "AlSi10Mg, 250 W, 0.9 m/s, 40 um beam, 150 C plate",
        "short": "AlSi10Mg, 250 W, 0.9 m/s",
        "P": 250.0, "v": 0.9, "r0": 40e-6, "T0": 423.15,
        "T_l": 868.6, "T_s": 842.7, "Si": 0.100,
        # domain (m): track along +x, beam along +y (down), z across
        "Lx": 1.0e-3, "Lz": 0.40e-3, "metal_depth": 0.35e-3, "x_start": 0.10e-3,
        # AM-module render (#238): peak 3044 K; no length scale; A read off its colour bar 0.31
        "am": {"A": 0.3074, "peak_T_K": 3044.0},
    },
    # the next AlSi10Mg grid point the AM module calls keyhole at 0.9 m/s (its boundary there is ~293 W)
    "alsi10mg_350W": {
        "label": "AlSi10Mg, 350 W, 0.9 m/s, 40 um beam, 150 C plate",
        "short": "AlSi10Mg, 350 W, 0.9 m/s",
        "P": 350.0, "v": 0.9, "r0": 40e-6, "T0": 423.15,
        "T_l": 868.6, "T_s": 842.7, "Si": 0.100,
        "Lx": 1.0e-3, "Lz": 0.40e-3, "metal_depth": 0.45e-3, "x_start": 0.10e-3,
        # no render at this point; the AM map calls it keyhole. A is the one read off the 250 W render.
        "am": {"A": 0.3074, "map_class": "keyhole"},
    },
    "blend": {
        "label": "BYU blend (Al-24Si), 375 W, 0.4 m/s, 45 um beam, 30 C plate",
        "short": "Blend (Al-24Si), 375 W, 0.4 m/s",
        "P": 375.0, "v": 0.4, "r0": 45e-6, "T0": 303.15,
        "T_l": 1019.3, "T_s": 846.7, "Si": 0.243,
        "Lx": 1.3e-3, "Lz": 0.64e-3, "metal_depth": 0.60e-3, "x_start": 0.15e-3,
        # AM-module render (#238): pool depth 349 um, length 1470 um, half-width 231 um, peak 3119 K, A 0.38
        "am": {"A": 0.3841, "peak_T_K": 3119.0, "pool_depth_um": 349.0, "pool_length_um": 1470.0,
               "pool_halfwidth_um": 231.0},
    },
}

PROPS = {
    "k": 110.0, "rho": 2650.0, "cp": 1040.0,
    "nu": 4.9e-7, "beta": 1.0e-4,
    "sigma": 0.86, "dsigma_dT": -3.5e-4,
    "T_vap": 2743.0, "L_vap": 1.09e7, "M": 0.02698,
    "e_num_density": 1.81e29, "elec_resistivity": 4.0e-7, "wavelength": 1.07e-6,
    "emissivity": 0.1,
}


def _w(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def latent_heat(si: float) -> float:
    return (1.0 - si) * L_FUSION_AL + si * L_FUSION_SI


def geometry(c: dict, dx: float) -> dict:
    n_gas = 4
    gas = n_gas * dx
    nx = int(round(c["Lx"] / dx))
    nz = int(round(c["Lz"] / dx))
    n_metal = int(round(c["metal_depth"] / dx))
    ny = n_gas + n_metal
    return {"dx": dx, "nx": nx, "ny": ny, "nz": nz, "y_surface": gas, "Lx": nx * dx, "Ly": ny * dx,
            "Lz": nz * dx, "y_laser": 0.5 * gas}


def setup(case: str, dx: float, end_time: float, write_interval: float, out: pathlib.Path,
          n_proc: int, max_co: float, absorbed_fraction: float | None = None,
          elec_resistivity: float | None = None) -> None:
    """Write a case. With ``absorbed_fraction`` A, the laser power is set to A*P and every ray deposits all
    of its power where it first meets the metal (maxRayBounces 1, action deposit), so the absorbed power
    is fixed at A*P whatever the keyhole does. Without it, each bounce absorbs its Fresnel fraction and
    reflects the rest, so the absorptivity comes out of the ray tracing."""
    c = CASES[case]
    g = geometry(c, dx)
    p = dict(PROPS)
    if elec_resistivity is not None:
        p["elec_resistivity"] = elec_resistivity
    out.mkdir(parents=True, exist_ok=True)
    x0 = c["x_start"]
    x1 = x0 + c["v"] * end_time
    if x1 > g["Lx"] - 1.5 * c["r0"]:
        raise SystemExit(f"beam would leave the domain: x1 = {x1 * 1e3:.3f} mm, Lx = {g['Lx'] * 1e3:.3f} mm")
    z0 = -0.5 * g["Lz"]
    z1 = 0.5 * g["Lz"]
    T0 = c["T0"]

    _w(out / "system" / "blockMeshDict", HEADER.format(cls="dictionary", obj="blockMeshDict") + textwrap.dedent(f"""\
        convertToMeters 1;
        vertices
        (
            (0 0 {z0:.6e}) ({g['Lx']:.6e} 0 {z0:.6e}) ({g['Lx']:.6e} {g['Ly']:.6e} {z0:.6e}) (0 {g['Ly']:.6e} {z0:.6e})
            (0 0 {z1:.6e}) ({g['Lx']:.6e} 0 {z1:.6e}) ({g['Lx']:.6e} {g['Ly']:.6e} {z1:.6e}) (0 {g['Ly']:.6e} {z1:.6e})
        );
        blocks ( hex (0 1 2 3 4 5 6 7) ({g['nx']} {g['ny']} {g['nz']}) simpleGrading (1 1 1) );
        edges ();
        boundary
        (
            lowerWall    {{ type wall;  faces ((3 7 6 2)); }}
            atmosphere   {{ type patch; faces ((1 5 4 0)); }}
            rightWall    {{ type patch; faces ((1 2 6 5)); }}
            leftWall     {{ type patch; faces ((0 4 7 3)); }}
            frontAndBack {{ type patch; faces ((0 3 2 1) (5 6 7 4)); }}
        );
        mergePatchPairs ();
        """))

    _w(out / "system" / "setFieldsDict", HEADER.format(cls="dictionary", obj="setFieldsDict") + textwrap.dedent(f"""\
        defaultFieldValues ( volScalarFieldValue alpha.metal 0 );
        regions
        (
            boxToCell
            {{
                box (-1 {g['y_surface']:.6e} -1) (1 1 1);
                fieldValues ( volScalarFieldValue alpha.metal 1 );
            }}
        );
        """))

    _w(out / "system" / "controlDict", HEADER.format(cls="dictionary", obj="controlDict") + textwrap.dedent(f"""\
        application     laserbeamFoam;
        startFrom       latestTime;
        startTime       0;
        stopAt          endTime;
        endTime         {end_time:.6e};
        deltaT          1e-9;
        writeControl    adjustableRunTime;
        writeInterval   {write_interval:.6e};
        purgeWrite      0;
        writeFormat     ascii;
        writePrecision  7;
        writeCompression off;
        timeFormat      general;
        timePrecision   8;
        runTimeModifiable yes;
        adjustTimeStep  yes;
        maxCo           {max_co};
        maxAlphaCo      {max_co};
        maxDeltaT       5e-7;
        """))

    _w(out / "system" / "decomposeParDict", HEADER.format(cls="dictionary", obj="decomposeParDict") + textwrap.dedent(f"""\
        numberOfSubdomains {n_proc};
        method          scotch;
        """))

    _w(out / "system" / "fvSchemes", HEADER.format(cls="dictionary", obj="fvSchemes") + textwrap.dedent("""\
        ddtSchemes { default Euler; }
        gradSchemes { default Gauss linear; }
        divSchemes
        {
            div(rhoPhi,U)   Gauss linearUpwind grad(U);
            div(phi,alpha)  Gauss vanLeer;
            div(phirb,alpha) Gauss linear;
            div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
            div(rhoPhi,epsilon1) Gauss linear;
            div(rhophicp,T)   Gauss upwind;
        }
        laplacianSchemes { default Gauss linear corrected; }
        interpolationSchemes { default linear; }
        snGradSchemes { default corrected; }
        """))

    _w(out / "system" / "fvSolution", HEADER.format(cls="dictionary", obj="fvSolution") + textwrap.dedent("""\
        solvers
        {
            "alpha.metal.*"
            {
                nAlphaCorr      2;
                nAlphaSubCycles 1;
                cAlpha          1;
                MULESCorr       yes;
                nLimiterIter    5;
                solver          smoothSolver;
                smoother        symGaussSeidel;
                tolerance       1e-8;
                relTol          0;
            }
            "pcorr.*" { solver PCG; preconditioner DIC; tolerance 1e-5; relTol 0; }
            p_rgh { solver PCG; preconditioner DIC; tolerance 1e-07; relTol 0.05; }
            p_rghFinal { $p_rgh; relTol 0; }
            U { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-06; relTol 0; }
            T { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-9; relTol 0; }
            TFinal { $T; }
        }
        MELTING
        {
            minTempCorrector 1;
            maxTempCorrector 20;
            epsilonTolerance 1e-6;
            epsilonRelaxation 0.9;
            damperSwitch true;
        }
        PIMPLE
        {
            momentumPredictor   no;
            nOuterCorrectors    1;
            nCorrectors         3;
            nNonOrthogonalCorrectors 0;
        }
        relaxationFactors { equations { ".*" 1; } }
        """))

    _w(out / "constant" / "g", HEADER.format(cls="uniformDimensionedVectorField", obj="g") + textwrap.dedent("""\
        dimensions      [0 1 -2 0 0 0 0];
        value           (0 9.81 0);
        """))
    _w(out / "constant" / "turbulenceProperties", HEADER.format(cls="dictionary", obj="turbulenceProperties")
       + "simulationType  laminar;\n")
    _w(out / "constant" / "timeVsLaserPosition",
       f"(\n    (0 ({x0:.6e} {g['y_laser']:.6e} 0))\n    ({end_time:.6e} ({x1:.6e} {g['y_laser']:.6e} 0))\n)\n")
    P_set = c["P"] if absorbed_fraction is None else c["P"] * absorbed_fraction
    _w(out / "constant" / "timeVsLaserPower", f"(\n    (0 {P_set:.6g})\n    (1 {P_set:.6g})\n)\n")
    bounce = ("" if absorbed_fraction is None else
              "maxRayBounces   1;\nmaxRayBounceAction deposit;   // all of each ray's power goes in at its first hit\n")
    _w(out / "constant" / "LaserProperties", HEADER.format(cls="dictionary", obj="LaserProperties") + textwrap.dedent(f"""\
        timeVsLaserPosition {{ file "$FOAM_CASE/constant/timeVsLaserPosition"; outOfBounds clamp; }}
        timeVsLaserPower {{ file "$FOAM_CASE/constant/timeVsLaserPower"; outOfBounds clamp; }}
        V_incident      (0 1 0);
        laserRadius     {c['r0']:.6e};
        N_sub_divisions 1;
        nRadial         20;
        nAngular        72;
        wavelength      {p['wavelength']:.6e};
        e_num_density   {p['e_num_density']:.6e};
        Radius_Flavour  2.0;
        useLocalSearch  true;
        """) + bounce)
    _w(out / "constant" / "transportProperties", HEADER.format(cls="dictionary", obj="transportProperties") + textwrap.dedent(f"""\
        interfaceTrackingScheme MULES;
        phases          (metal gas);
        metal
        {{
            transportModel  Newtonian;
            nu              {p['nu']:.6e};
            rho             {p['rho']};
            Tsolidus        {c['T_s']};
            Tliquidus       {c['T_l']};
            LatentHeat      {latent_heat(c['Si']):.6e};
            beta            {p['beta']:.6e};
            poly_kappa      ({p['k']} 0 0 0 0 0 0 0);
            poly_cp         ({p['cp']} 0 0 0 0 0 0 0);
            Elec_conductivity {1.0 / p['elec_resistivity']:.6e};
        }}
        gas
        {{
            transportModel  Newtonian;
            nu              1.48e-05;
            rho             1;
            poly_kappa      (0.04 0 0 0 0 0 0 0);
            poly_cp         (520 0 0 0 0 0 0 0);
            Tsolidus        1.0;
            Tliquidus       10.0;
            LatentHeat      1;
            beta            4.0e-5;
        }}
        emS             {p['emissivity']};
        emL             {p['emissivity']};
        TRef            TRef [0 0 0 1 0 0 0] {T0};
        sigma           {p['sigma']};
        Marangoni_Constant {p['dsigma_dT']:.6e};
        p0              1e5;
        Tvap            {p['T_vap']};
        Mm              {p['M']};
        LatentHeatVap   {p['L_vap']:.6e};
        """))

    def field(name, cls, dims, internal, bcs):
        body = "\n".join(f"    {patch}\n    {{\n" + "\n".join(f"        {line}" for line in lines) + "\n    }"
                         for patch, lines in bcs.items())
        return (HEADER.format(cls=cls, obj=name)
                + f"dimensions      {dims};\ninternalField   {internal};\nboundaryField\n{{\n{body}\n}}\n")

    walls = ["lowerWall", "rightWall", "leftWall", "frontAndBack"]
    T_bcs = {w: ["type zeroGradient;"] for w in walls}
    T_bcs["lowerWall"] = ["type fixedValue;", f"value uniform {T0};"]
    T_bcs["atmosphere"] = ["type zeroGradient;"]
    U_bcs = {w: ["type slip;"] for w in walls}
    U_bcs["atmosphere"] = ["type pressureInletOutletVelocity;", "value uniform (0 0 0);"]
    p_bcs = {w: ["type fixedFluxPressure;", "value uniform 0;"] for w in walls}
    p_bcs["atmosphere"] = ["type totalPressure;", "p0 uniform 0;", "value uniform 0;"]
    a_bcs = {w: ["type zeroGradient;"] for w in walls}
    a_bcs["atmosphere"] = ["type inletOutlet;", "inletValue uniform 0;", "value uniform 0;"]
    l_bcs = {w: ["type fixedValue;", "value uniform -1.0;"] for w in walls}
    l_bcs["atmosphere"] = ["type fixedValue;", "value uniform 1.0;"]
    init = out / "initial"
    _w(init / "T", field("T", "volScalarField", "[0 0 0 1 0 0 0]", f"uniform {T0}", T_bcs))
    _w(init / "U", field("U", "volVectorField", "[0 1 -1 0 0 0 0]", "uniform (0 0 0)", U_bcs))
    _w(init / "p_rgh", field("p_rgh", "volScalarField", "[1 -1 -2 0 0 0 0]", "uniform 0", p_bcs))
    _w(init / "alpha.metal", field("alpha.metal", "volScalarField", "[0 0 0 0 0 0 0]", "uniform 0", a_bcs))
    _w(init / "Laser_boundary", field("Laser_boundary", "volScalarField", "[0 0 0 0 0 0 0]", "uniform 0", l_bcs))

    allrun = textwrap.dedent("""\
        #!/bin/bash
        # usage: ./Allrun [nProc]   (nProc 1 runs in serial)
        cd "${0%/*}" || exit 1
        NP=${1:-1}
        rm -rf 0 && cp -r initial 0
        blockMesh > log.blockMesh 2>&1 || exit 1
        setFields > log.setFields 2>&1 || exit 1
        postProcess -func writeCellCentres -time 0 > log.writeCellCentres 2>&1
        # With maxRayBounces set, laserbeamFoam prints a four-line warning for every ray at every step
        # (~0.6 MB per step); they carry nothing the summary needs, so they are dropped from the log.
        FILTER='^(--> FOAM Warning : *$|    From bool Foam::laserRayParticle::move|    in file laserRayParticle.C|    Terminating ray )'
        if [ "$NP" -gt 1 ]; then
            decomposePar -force > log.decomposePar 2>&1 || exit 1
            mpirun --oversubscribe -np "$NP" laserbeamFoam -parallel 2>&1 | grep -v -E "$FILTER" > log.laserbeamFoam
        else
            laserbeamFoam 2>&1 | grep -v -E "$FILTER" > log.laserbeamFoam
        fi
        """)
    _w(out / "Allrun", allrun)
    (out / "Allrun").chmod(0o755)
    meta = {"case": case, **{k: v for k, v in c.items() if k != "am"}, "am_module": c["am"], "props": p,
            "latent_heat": latent_heat(c["Si"]), "geometry": g, "end_time": end_time,
            "write_interval": write_interval, "x_end": x1, "n_proc": n_proc, "maxCo": max_co,
            "absorbed_fraction": absorbed_fraction, "laser_power_set": P_set}
    _w(out / "case.json", json.dumps(meta, indent=2))
    print(f"{case}: {g['nx']} x {g['ny']} x {g['nz']} = {g['nx'] * g['ny'] * g['nz']} cells at {dx * 1e6:.1f} um; "
          f"beam {x0 * 1e3:.3f} -> {x1 * 1e3:.3f} mm over {end_time * 1e3:.2f} ms")


# ----------------------------------------------------------------------------------------------------
# post-processing


def read_internal(path: pathlib.Path) -> np.ndarray:
    """Read an ASCII OpenFOAM volScalarField/volVectorField internalField (uniform or nonuniform)."""
    text = path.read_text()
    m = re.search(r"internalField\s+uniform\s+([^;]+);", text)
    if m:
        val = m.group(1).strip()
        return np.array([float(x) for x in val.strip("()").split()]) if val.startswith("(") else np.array(float(val))
    m = re.search(r"internalField\s+nonuniform\s+List<(\w+)>\s*(\d+)\s*\(", text)
    if not m:
        raise ValueError(f"no internalField in {path}")
    kind, n = m.group(1), int(m.group(2))
    start = m.end()
    if kind == "scalar":
        arr = np.fromstring(text[start:start + 40 * n], sep="\n", count=n)
        return arr
    body = text[start:]
    vals = re.findall(r"\(([^()]+)\)", body[: 120 * n])[:n]
    return np.array([[float(x) for x in v.split()] for v in vals])


def _crossing(a: float, b: float, fa: float, fb: float, level: float) -> float:
    """Linear interpolation of the position where f crosses level between (a, fa) and (b, fb)."""
    if fb == fa:
        return b
    return a + (level - fa) * (b - a) / (fb - fa)


def pool_metrics(T: np.ndarray, alpha: np.ndarray, g: dict, c: dict, x_beam: float) -> dict:
    """Melt-pool and keyhole size from cell-centred fields on the uniform blockMesh grid.

    Arrays are reshaped to (nz, ny, nx): OpenFOAM's blockMesh numbers cells x fastest, then y, then z.
    The pool is the connected region of liquid metal (alpha >= 0.5 and T >= liquidus) that contains the
    liquid cell nearest the beam, so detached spatter does not count. Its extents are interpolated to the
    liquidus between a liquid cell and a solid metal neighbour; where the neighbour is gas, the pool ends at
    the cell face. The keyhole is gas (alpha < 0.5) below the original surface plane within 4 r0 of the beam.
    """
    from scipy import ndimage

    nx, ny, nz, dx = g["nx"], g["ny"], g["nz"], g["dx"]
    T3 = T.reshape(nz, ny, nx)
    a3 = alpha.reshape(nz, ny, nx)
    xc = (np.arange(nx) + 0.5) * dx
    yc = (np.arange(ny) + 0.5) * dx
    zc = -0.5 * g["Lz"] + (np.arange(nz) + 0.5) * dx
    ys = g["y_surface"]
    js = int(round(ys / dx))  # first metal row
    T_l = c["T_l"]
    metal = a3 >= 0.5
    out = {"x_beam_mm": x_beam * 1e3, "T_max_K": float(T3[metal].max()) if metal.any() else float("nan")}
    # keyhole: gas cells below the original surface, near the beam, connected to the gas above the surface
    near = np.abs(xc - x_beam) < 4 * c["r0"]
    gas = ~metal
    lab, _ = ndimage.label(gas)
    open_labels = set(np.unique(lab[:, :js, :])) - {0}
    gas_open = np.isin(lab, list(open_labels))
    gas_below = gas_open & (yc[None, :, None] > ys) & near[None, None, :]
    out["keyhole_depth_um"] = 0.0
    out["keyhole_width_surface_um"] = 0.0
    out["keyhole_width_q1_um"] = 0.0
    out["keyhole_width_mid_um"] = 0.0
    if gas_below.any():
        kk, jj, ii = np.nonzero(gas_below)
        j = jj.max()
        sel = jj == j
        k0, i0 = kk[sel][0], ii[sel][0]
        y_bottom = yc[j] + 0.5 * dx
        if j + 1 < ny and metal[k0, j + 1, i0]:
            y_bottom = _crossing(yc[j], yc[j + 1], a3[k0, j, i0], a3[k0, j + 1, i0], 0.5)
        out["keyhole_depth_um"] = (y_bottom - ys) * 1e6
        out["keyhole_x_um_rel_beam"] = float((xc[i0] - x_beam) * 1e6)
        row = gas_below[:, js, :]
        out["keyhole_width_surface_um"] = float(row.any(axis=1).sum() * dx * 1e6)
        # widths across the track (z) at a quarter and half of the keyhole depth: the surface opening also takes in
        # any shallow depression of the pool surface around the keyhole
        for name, frac in (("q1", 0.25), ("mid", 0.5)):
            jq = int(round(js + frac * (j - js)))
            rowq = gas_below[:, jq, :]
            out[f"keyhole_width_{name}_um"] = float(rowq.any(axis=1).sum() * dx * 1e6)
    out.update(_pool_extent(T3, metal, T_l, xc, yc, zc, ys, dx, x_beam, ""))
    # the same at the solidus: the blend's mushy range is 170 K wide, and which edge the AM module draws is not stated
    out.update(_pool_extent(T3, metal, c["T_s"], xc, yc, zc, ys, dx, x_beam, "_solidus"))
    return out


def _pool_extent(T3, metal, level, xc, yc, zc, ys, dx, x_beam, sfx: str) -> dict:
    from scipy import ndimage

    nz, ny, nx = T3.shape
    out: dict = {}
    T_l = level
    liquid_all = metal & (T3 >= T_l)
    if not liquid_all.any():
        return {f"pool_depth{sfx}_um": 0.0, f"pool_width{sfx}_um": 0.0, f"pool_length{sfx}_um": 0.0}
    lab, n = ndimage.label(liquid_all)
    kk, jj, ii = np.nonzero(liquid_all)
    d2 = (xc[ii] - x_beam) ** 2 + (yc[jj] - ys) ** 2 + zc[kk] ** 2
    keep = lab[kk[np.argmin(d2)], jj[np.argmin(d2)], ii[np.argmin(d2)]]
    liquid = lab == keep
    kk, jj, ii = np.nonzero(liquid)
    solid_metal = metal & ~liquid

    def edge(k, j, i, axis, step, coord):
        """Liquidus position past cell (k, j, i) along axis in direction step."""
        idx = [k, j, i]
        idx[axis] += step
        n_ax = (nz, ny, nx)[axis]
        if not (0 <= idx[axis] < n_ax):
            return coord[(k, j, i)[axis]] + step * 0.5 * dx
        k2, j2, i2 = idx
        if solid_metal[k2, j2, i2]:
            return _crossing(coord[(k, j, i)[axis]], coord[idx[axis]], T3[k, j, i], T3[k2, j2, i2], T_l)
        return coord[(k, j, i)[axis]] + step * 0.5 * dx

    jmax = jj.max()
    out[f"pool_depth{sfx}_um"] = (max(edge(k, j, i, 1, +1, yc) for k, j, i in zip(kk, jj, ii) if j == jmax) - ys) * 1e6
    zs = [abs(edge(k, j, i, 0, -1, zc)) for k, j, i in zip(kk, jj, ii) if k == kk.min()]
    zs += [abs(edge(k, j, i, 0, +1, zc)) for k, j, i in zip(kk, jj, ii) if k == kk.max()]
    out[f"pool_width{sfx}_um"] = 2 * max(zs) * 1e6
    x_front = max(edge(k, j, i, 2, +1, xc) for k, j, i in zip(kk, jj, ii) if i == ii.max())
    x_back = min(edge(k, j, i, 2, -1, xc) for k, j, i in zip(kk, jj, ii) if i == ii.min())
    out[f"pool_length{sfx}_um"] = (x_front - x_back) * 1e6
    if not sfx:
        out["pool_front_um_rel_beam"] = (x_front - x_beam) * 1e6
        out["pool_back_um_rel_beam"] = (x_back - x_beam) * 1e6
        out["pool_back_touches_domain_start"] = bool(ii.min() == 0)
        out["pool_volume_mm3"] = float(liquid.sum() * dx ** 3 * 1e9)
        out["n_liquid_regions"] = int(n)
    return out


def parse_log(log: pathlib.Path) -> list[dict]:
    """Time, time step and total absorbed (deposited) laser power from a laserbeamFoam log, read as a stream
    (an unfiltered log grows by ~0.6 MB a step)."""
    with log.open(errors="replace") as fh:
        lines = (ln.rstrip("\n") for ln in fh if ln[:4] in ("Time", "delt", "    ", "Exec"))
        return _parse_lines(lines)


def _parse_lines(lines) -> list[dict]:
    rows: list[dict] = []
    t = dt = None
    for line in lines:
        if line.startswith("Time = "):
            try:
                t = float(line.split("=")[1])
            except ValueError:
                t = None
        elif line.startswith("deltaT = "):
            try:
                dt = float(line.split("=")[1])
            except ValueError:
                pass
        elif "Total Q deposited:" in line and t is not None:
            rows.append({"t": t, "dt": dt, "Q": float(line.split(":")[1])})
        elif line.startswith("ExecutionTime") and rows:
            m = re.search(r"ExecutionTime = ([\d.eE+-]+) s", line)
            if m:
                rows[-1]["wall_s"] = float(m.group(1))
    return rows


def time_dirs(case_dir: pathlib.Path) -> list[tuple[float, pathlib.Path]]:
    """Reconstructed time directories with T and alpha.metal, latest last."""
    times = []
    for p in case_dir.iterdir():
        if p.is_dir() and re.fullmatch(r"[\d.eE+-]+", p.name) and float(p.name) > 0:
            if (p / "T").exists() and (p / "alpha.metal").exists():
                times.append((float(p.name), p))
    return sorted(times)


def post(case_dir: pathlib.Path, out: pathlib.Path) -> dict:
    meta = json.loads((case_dir / "case.json").read_text())
    run = case_dir.name
    c = CASES[meta["case"]]
    g = meta["geometry"]
    rows = []
    for t, p in time_dirs(case_dir):
        T = read_internal(p / "T")
        a = read_internal(p / "alpha.metal")
        if T.size != g["nx"] * g["ny"] * g["nz"]:
            continue
        x_beam = c["x_start"] + c["v"] * t
        rows.append({"t_ms": t * 1e3, **pool_metrics(T, a, g, c, x_beam)})
    log_rows = parse_log(case_dir / "log.laserbeamFoam") if (case_dir / "log.laserbeamFoam").exists() else []
    out.mkdir(parents=True, exist_ok=True)
    import pandas as pd

    df = pd.DataFrame(rows)
    df.to_csv(out / f"{run}-pool-vs-time.csv", index=False, float_format="%.4g")
    ldf = pd.DataFrame(log_rows)
    if not ldf.empty:
        # a restarted run repeats the steps after its last write; keep the later copy of each
        ldf = ldf.drop_duplicates("t", keep="last").sort_values("t").reset_index(drop=True)
        ldf["A_eff"] = ldf["Q"] / c["P"]
        step = max(1, len(ldf) // 2000)  # thin the per-step log to ~2000 rows for the repo
        ldf.iloc[::step].to_csv(out / f"{run}-absorbed-power-vs-time.csv", index=False, float_format="%.5g")
    summary = {"run": run, "case": meta["case"], "label": c["label"], "meta": meta, "n_steps": len(ldf),
               "t_end_reached_ms": float(ldf["t"].max() * 1e3) if not ldf.empty else None,
               "wall_s": float(ldf["wall_s"].dropna().max()) if "wall_s" in ldf else None}
    if not ldf.empty:
        t_max = ldf["t"].max()
        late = ldf[ldf["t"] > 0.5 * t_max]
        summary["A_eff_mean_second_half"] = float(late["A_eff"].mean())
        summary["A_eff_std_second_half"] = float(late["A_eff"].std())
        summary["A_eff_first_step"] = float(ldf["A_eff"].iloc[0])
        summary["dt_median_s"] = float(ldf["dt"].median())
        summary["dt_min_s"] = float(ldf["dt"].min())
    if not df.empty:
        summary["last_write"] = df.iloc[-1].to_dict()
        late = df[df["t_ms"] >= 0.5 * df["t_ms"].max()]
        summary["second_half_of_writes"] = {
            k: {"mean": float(late[k].mean()), "min": float(late[k].min()), "max": float(late[k].max())}
            for k in ["T_max_K", "keyhole_depth_um", "keyhole_width_surface_um", "keyhole_width_q1_um",
                      "keyhole_width_mid_um", "pool_depth_um", "pool_width_um", "pool_length_um",
                      "pool_depth_solidus_um", "pool_width_solidus_um", "pool_length_solidus_um"] if k in late}
    (out / f"{run}-summary.json").write_text(json.dumps(summary, indent=2, default=float))
    print(json.dumps({k: v for k, v in summary.items() if k != "meta"}, indent=2, default=float))
    return summary


# ----------------------------------------------------------------------------------------------------
# figures

INK, INK2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
RUN_COLOURS = {"fresnel": "#2a78d6", "matchedA": "#eb6834", "fresnel_hot": "#eda100"}  # categorical slots 1, 2, 4
GAN_COLOUR = "#1baf7a"  # categorical slot 3
RUN_LABELS = {"fresnel": "laserbeamFoam, Fresnel ray tracing (40 µΩ cm)", "matchedA": "laserbeamFoam, AM module's A·P",
              "fresnel_hot": "laserbeamFoam, Fresnel ray tracing (65 µΩ cm)"}
SEQ_BLUE = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def _variant(run: str) -> str:
    if "matchedA" in run:
        return "matchedA"
    return "fresnel_hot" if "rho65" in run else "fresnel"


def plot_histories(post_dir: pathlib.Path, runs: list[str], out_png: pathlib.Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    cases = sorted({json.loads((post_dir / f"{r}-summary.json").read_text())["case"] for r in runs},
                   key=lambda k: list(CASES).index(k))
    panels = [("A_eff", "absorbed fraction of P"), ("keyhole_depth_um", "keyhole depth (µm)"),
              ("pool_depth_um", "pool depth (µm)"), ("pool_width_um", "pool width (µm)"),
              ("pool_length_um", "pool length (µm)")]
    fig, axes = plt.subplots(len(cases), len(panels), figsize=(3.0 * len(panels), 2.7 * len(cases)),
                             squeeze=False, facecolor=SURFACE)
    for row, case in enumerate(cases):
        c = CASES[case]
        am = c["am"]
        am_ref = {"A_eff": am.get("A"), "pool_depth_um": am.get("pool_depth_um"),
                  "pool_width_um": 2 * am["pool_halfwidth_um"] if "pool_halfwidth_um" in am else None,
                  "pool_length_um": am.get("pool_length_um")}
        for col, (key, ylabel) in enumerate(panels):
            ax = axes[row, col]
            ax.set_facecolor(SURFACE)
            for r in runs:
                s = json.loads((post_dir / f"{r}-summary.json").read_text())
                if s["case"] != case:
                    continue
                colour = RUN_COLOURS[_variant(r)]
                ls = (0, (4, 2)) if r.endswith("25um") else "-"
                if key == "A_eff":
                    f = post_dir / f"{r}-absorbed-power-vs-time.csv"
                    if not f.exists():
                        continue
                    d = pd.read_csv(f)
                    # 10 µs bin means: the per-step value flickers as the keyhole wall moves
                    d = d.groupby((d["t"] / 1e-5).astype(int)).agg(t=("t", "mean"), A_eff=("A_eff", "mean"))
                    ax.plot(d["t"] * 1e3, d["A_eff"], color=colour, lw=1.5, ls=ls)
                else:
                    d = pd.read_csv(post_dir / f"{r}-pool-vs-time.csv")
                    if key in d:
                        ax.plot(d["t_ms"], d[key], color=colour, lw=2, ls=ls, marker="o" if ls == "-" else None, ms=3)
            if key == "keyhole_depth_um":
                # Gan et al. 2021's depth law at the AM module's absorptivity, for comparison with the matched-A run
                ke = am["A"] * c["P"] / ((c["T_l"] - c["T0"]) * math.pi * PROPS["rho"] * PROPS["cp"]
                                         * math.sqrt(PROPS["k"] / (PROPS["rho"] * PROPS["cp"]) * c["v"] * c["r0"] ** 3))
                e_gan = max(0.0, 0.4 * (ke - 1.4)) * c["r0"] * 1e6
                ax.axhline(e_gan, color=GAN_COLOUR, ls=(0, (1.5, 1.5)), lw=1.6)
                ax.annotate("Gan et al. law, AM module's A", xy=(0.02, e_gan), xycoords=("axes fraction", "data"),
                            xytext=(0, 3), textcoords="offset points", fontsize=7, color=INK2)
            ref = am_ref.get(key)
            if ref:
                ax.axhline(ref, color=INK2, ls=(0, (5, 3)), lw=1.2)
                ax.annotate("AM module", xy=(0.02, ref), xycoords=("axes fraction", "data"), xytext=(0, 3),
                            textcoords="offset points", fontsize=7, color=INK2)
            ax.set_xlabel("time (ms)", fontsize=8, color=INK2)
            ax.set_ylabel(ylabel if key != "A_eff" else ylabel + " (10 µs means)", fontsize=8, color=INK2)
            ax.tick_params(labelsize=7, colors=INK2)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.grid(color="#e6e5e1", lw=0.5)
            ax.set_ylim(bottom=0)
            if col == 0:
                ax.set_title(c["short"], fontsize=8.5, loc="left", color=INK)
    present = {_variant(r) for r in runs}
    handles = [plt.Line2D([], [], color=RUN_COLOURS[v], lw=2, label=RUN_LABELS[v])
               for v in ("fresnel", "fresnel_hot", "matchedA") if v in present]
    if any(r.endswith("25um") for r in runs):
        handles.append(plt.Line2D([], [], color=RUN_COLOURS["matchedA"], lw=2, ls=(0, (4, 2)),
                                  label="laserbeamFoam, AM module's A·P, 25 µm cells"))
    handles.append(plt.Line2D([], [], color=INK2, ls=(0, (5, 3)), lw=1.2, label="AM module (Thermo-Calc), read off its render"))
    handles.append(plt.Line2D([], [], color=GAN_COLOUR, ls=(0, (1.5, 1.5)), lw=1.6,
                              label="Gan et al. 2021 keyhole depth law at the AM module's A"))
    fig.legend(handles=handles, loc="upper center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.75 / fig.get_figheight()))
    fig.savefig(out_png, dpi=150)
    plt.close(fig)


def plot_sections(case_dirs: list[pathlib.Path], out_png: pathlib.Path) -> None:
    """Longitudinal (z = 0) and transverse (widest pool) sections at each run's last write."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list("seq_blue", SEQ_BLUE)
    fig, axes = plt.subplots(len(case_dirs), 2, figsize=(12, 3.4 * len(case_dirs)), squeeze=False,
                             gridspec_kw={"width_ratios": [2.0, 1.0], "hspace": 0.55}, facecolor=SURFACE)
    for row, cd in enumerate(case_dirs):
        meta = json.loads((cd / "case.json").read_text())
        c = CASES[meta["case"]]
        g = meta["geometry"]
        t, p = time_dirs(cd)[-1]
        T3 = read_internal(p / "T").reshape(g["nz"], g["ny"], g["nx"])
        a3 = read_internal(p / "alpha.metal").reshape(g["nz"], g["ny"], g["nx"])
        dx = g["dx"]
        xc = (np.arange(g["nx"]) + 0.5) * dx
        yc = (np.arange(g["ny"]) + 0.5) * dx
        zc = -0.5 * g["Lz"] + (np.arange(g["nz"]) + 0.5) * dx
        ys = g["y_surface"]
        x_beam = c["x_start"] + c["v"] * t
        depth = (yc - ys) * 1e6
        Tm = np.where(a3 >= 0.5, T3, np.nan)
        vmax = 3200.0
        k0 = g["nz"] // 2
        # longitudinal section, x relative to the beam
        ax = axes[row, 0]
        X = (xc - x_beam) * 1e6
        sec = 0.5 * (Tm[k0 - 1] + Tm[k0]) if g["nz"] % 2 == 0 else Tm[k0]
        asec = 0.5 * (a3[k0 - 1] + a3[k0]) if g["nz"] % 2 == 0 else a3[k0]
        Tsec = 0.5 * (T3[k0 - 1] + T3[k0]) if g["nz"] % 2 == 0 else T3[k0]
        im = ax.pcolormesh(X, depth, sec, cmap=cmap, vmin=c["T0"], vmax=vmax, shading="nearest")
        ax.contour(X, depth, np.where(asec >= 0.5, Tsec, c["T0"]), levels=[c["T_l"]], colors=["#eb6834"], linewidths=1.8)
        ax.contour(X, depth, asec, levels=[0.5], colors=[INK], linewidths=1.0)
        am = c["am"]
        if "pool_depth_um" in am:
            ax.axhline(am["pool_depth_um"], color=INK2, ls=(0, (5, 3)), lw=1.1)
            ax.annotate(f"AM module: depth {am['pool_depth_um']:.0f} µm; its pool ends "
                        f"{am['pool_length_um'] / 1000:.2f} mm behind the beam, off this plot",
                        xy=(X.min() + 20, am["pool_depth_um"]), xytext=(0, 3),
                        textcoords="offset points", fontsize=7, color=INK2)
        ax.set_xlim(X.min(), X.max())
        ax.set_ylim(depth.max(), depth.min())
        ax.set_aspect("equal")
        ax.set_xlabel("x − beam position (µm)", fontsize=8, color=INK2)
        ax.set_ylabel("depth below plate (µm)", fontsize=8, color=INK2)
        short_variant = {"fresnel": "own Fresnel A, 40 µΩ cm", "fresnel_hot": "own Fresnel A, 65 µΩ cm",
                         "matchedA": "absorbed power = AM module's A·P"}[_variant(cd.name)]
        ax.set_title(f"{c['short']} | {short_variant} | {dx * 1e6:g} µm cells | t = {t * 1e3:.2f} ms",
                     fontsize=8.5, loc="left", color=INK)
        ax.tick_params(labelsize=7, colors=INK2)
        # transverse section through the deepest point of the pool (under the keyhole)
        liquid = (a3 >= 0.5) & (T3 >= c["T_l"])
        if liquid.any():
            _, jj_, ii_ = np.nonzero(liquid)
            i_w = int(ii_[np.argmax(jj_)])
        else:
            i_w = int(np.argmin(np.abs(xc - x_beam)))
        ax2 = axes[row, 1]
        Z = zc * 1e6
        ax2.pcolormesh(Z, depth, Tm[:, :, i_w].T, cmap=cmap, vmin=c["T0"], vmax=vmax, shading="nearest")
        ax2.contour(Z, depth, np.where(a3[:, :, i_w] >= 0.5, T3[:, :, i_w], c["T0"]).T, levels=[c["T_l"]],
                    colors=["#eb6834"], linewidths=1.8)
        ax2.contour(Z, depth, a3[:, :, i_w].T, levels=[0.5], colors=[INK], linewidths=1.0)
        if "pool_halfwidth_um" in am:
            for zz in (-am["pool_halfwidth_um"], am["pool_halfwidth_um"]):
                ax2.axvline(zz, color=INK2, ls=(0, (5, 3)), lw=1.1)
            ax2.axhline(am["pool_depth_um"], color=INK2, ls=(0, (5, 3)), lw=1.1)
        ax2.set_xlim(Z.min(), Z.max())
        ax2.set_ylim(depth.max(), depth.min())
        ax2.set_aspect("equal")
        ax2.set_xlabel(f"z (µm), at x − beam = {(xc[i_w] - x_beam) * 1e6:.0f} µm", fontsize=8, color=INK2)
        ax2.tick_params(labelsize=7, colors=INK2)
    fig.subplots_adjust(top=1 - 0.55 / fig.get_figheight(), bottom=0.9 / fig.get_figheight())
    cax = fig.add_axes([0.3, 0.25 / fig.get_figheight(), 0.4, 0.12 / fig.get_figheight()])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("metal temperature (K)", fontsize=8, color=INK2)
    cb.ax.tick_params(labelsize=7, colors=INK2)
    handles = [plt.Line2D([], [], color="#eb6834", lw=1.8, label="liquidus (pool edge)"),
               plt.Line2D([], [], color=INK, lw=1.0, label="metal surface (keyhole wall)"),
               plt.Line2D([], [], color=INK2, ls=(0, (5, 3)), lw=1.1, label="AM module pool depth / length / half-width")]
    fig.legend(handles=handles, loc="upper center", ncol=3, fontsize=8, frameon=False)
    fig.savefig(out_png, dpi=150, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup", help="write a laserbeamFoam case")
    s.add_argument("--case", choices=sorted(CASES), required=True)
    s.add_argument("--dx", type=float, default=15e-6, help="uniform cell size, m")
    s.add_argument("--end-time", type=float, required=True, help="simulated time, s")
    s.add_argument("--write-interval", type=float, default=1e-4)
    s.add_argument("--n-proc", type=int, default=2)
    s.add_argument("--max-co", type=float, default=0.3)
    s.add_argument("--elec-resistivity", type=float, default=None,
                   help="liquid electrical resistivity for the Drude model, Ohm m (default 4.0e-7)")
    s.add_argument("--absorbed-fraction", type=float, default=None,
                   help="fix the absorbed power at this fraction of P (first-hit deposition)")
    s.add_argument("--out", type=pathlib.Path, required=True)
    p = sub.add_parser("post", help="measure the pool and keyhole at each write time")
    p.add_argument("--case-dir", type=pathlib.Path, required=True)
    p.add_argument("--out", type=pathlib.Path, required=True)
    f = sub.add_parser("figures", help="time histories and sections of finished (reconstructed) runs")
    f.add_argument("--post-dir", type=pathlib.Path, required=True)
    f.add_argument("--case-dirs", type=pathlib.Path, nargs="+", required=True)
    f.add_argument("--sections", nargs="*", default=None,
                   help="run names to draw sections for (default: all of --case-dirs)")
    f.add_argument("--out", type=pathlib.Path, required=True)
    args = ap.parse_args()
    if args.cmd == "figures":
        runs = [d.name for d in args.case_dirs]
        plot_histories(args.post_dir, runs, args.out / "cfd-histories.png")
        sec = [d for d in args.case_dirs if args.sections is None or d.name in args.sections]
        plot_sections(sec, args.out / "cfd-sections.png")
        return
    if args.cmd == "setup":
        setup(args.case, args.dx, args.end_time, args.write_interval, args.out, args.n_proc, args.max_co,
              args.absorbed_fraction, args.elec_resistivity)
    else:
        post(args.case_dir, args.out)


if __name__ == "__main__":
    main()
