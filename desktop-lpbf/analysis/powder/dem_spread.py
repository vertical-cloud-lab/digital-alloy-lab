"""DEM of one recoater pass for the desktop LPBF (issue #260): LIGGGHTS 3.8, one core.

A 1.5 mm HSS blade with a full-radius (R 0.75 mm) "wide" nose pushes a dosed pile of AlSi10Mg-type powder over a
rough substrate (fixed 30 um bumps on a flat wall, standing in for the last lased layer). The domain is periodic
across the blade (y). Hertz-Mindlin with a softened Young's modulus, SJKR cohesion scaled so the pull-off force of
every size pair matches JKR for the chosen work of adhesion, EPSD2 rolling resistance, the real PSD cut at 20 um.

Re-run (each case writes /tmp/powder/<case>/, runs LIGGGHTS under /tmp/capmem 3 with OMP_NUM_THREADS=1, then writes
desktop-lpbf/analysis/out/powder/<case>.json):
    /tmp/venv/bin/python desktop-lpbf/analysis/powder/dem_spread.py run --gap 60 --speed 50 --coh low
    /tmp/venv/bin/python desktop-lpbf/analysis/powder/dem_spread.py run --gap 100 --speed 150 --coh high --E 2.5e6
    /tmp/venv/bin/python desktop-lpbf/analysis/powder/dem_spread.py post --case g60_v50_low     # post-process only
    /tmp/venv/bin/python desktop-lpbf/analysis/powder/dem_spread.py table                       # results table (md)
The LIGGGHTS input written for each case is also copied to desktop-lpbf/analysis/powder/inputs/.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "out", "powder"))
WORK = "/tmp/powder"

# ---------------------------------------------------------------- material (sources in powder-spreading.md) ------
RHO = 2680.0          # kg/m3, AlSi10Mg (Ye 2026; Girnth 2024: 2670)
E_REAL = 75e9         # Pa, AlSi10Mg (Girnth 2024, Ye 2026)
NU = 0.30             # Poisson ratio (Ye 2026; Girnth 0.33)
E_SIM = 0.5e6         # Pa, softened modulus used in the DEM (justified in powder-spreading.md, checked in each json)
REST = 0.60           # restitution (Girnth 0.54 measured, Ye 0.64)
MU = 0.50             # sliding friction p-p and p-wall (Girnth 0.20 smooth .. 0.45 rough; Ye 0.67)
MU_R = 0.10           # rolling friction, EPSD2 (Girnth 0.02-0.12; Ye 0.09)
GAMMA = {"low": 0.2e-3, "high": 1.0e-3}   # J/m2, work of adhesion in the JKR pull-off F = 1.5*pi*Gamma*R*
G = 9.81

# ---------------------------------------------------------------- PSD -----------------------------------------------
# Gas-atomised AlSi10Mg-type, volume-based log-normal: D50 36 um, sigma_ln 0.36 (D10 ~23, D90 ~57 um before the
# 15-63 um sieve cut). The DEM keeps 20-63 um: the 15-20 um tail (~4 % of the mass, ~20 % of the particles) is cut.
D50_UM, SIG_LN = 36.0, 0.36
CUT_REAL = (15.0, 63.0)
EDGES_UM = [20.0, 25.0, 30.0, 36.0, 43.0, 52.0, 63.0]
NBIN = len(EDGES_UM) - 1
T_BUMP, T_WALL = NBIN + 1, NBIN + 2           # atom/wall types: 1..6 powder bins, 7 substrate bumps, 8 walls+blade
NTYPES = NBIN + 2

# ---------------------------------------------------------------- geometry (m) ----------------------------------
W = 0.40e-3           # periodic width across the blade (~7 D90)
R_NOSE = 0.75e-3      # full-radius nose of the 1.5 mm blade
XC0 = 0.80e-3         # blade bottom point (nose centre) at the start
TRAVEL = 3.0e-3       # blade travel
LX = 5.8e-3
ZLO, ZHI = -0.03e-3, 2.4e-3
D_BUMP, Z_BUMP, COVER_BUMP = 30e-6, -5e-6, 0.35   # substrate bumps: 30 um spheres, centres 5 um below z=0
DOSE = 1.8            # pile solid volume / (0.5 x gap x travel x width): budgets.py's dose factor at 50 % packing
PRIMES = [15485863, 15485867, 32452843, 32452867, 49979687, 49979693, 67867967, 67867979, 86028121, 86028157,
          104395301, 104395303, 122949823, 122949829, 141650939, 141650963]


def _phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def cdf_vol(d_um):
    """Volume (mass) fraction finer than d for the un-sieved log-normal."""
    return _phi(math.log(d_um / D50_UM) / SIG_LN)


def psd_bins():
    """Mass fraction and representative diameter (volume-weighted, from a fine sub-grid) of each DEM bin."""
    fr, dr = [], []
    for lo, hi in zip(EDGES_UM[:-1], EDGES_UM[1:]):
        fr.append(cdf_vol(hi) - cdf_vol(lo))
        d = np.linspace(lo, hi, 201)
        w = np.diff([cdf_vol(x) for x in d])
        dm = 0.5 * (d[1:] + d[:-1])
        # mass-weighted number distribution in the bin -> the diameter whose cube is the mean cube by number
        n = w / dm ** 3
        dr.append(float((np.sum(n * dm ** 3) / np.sum(n)) ** (1 / 3)))
    fr = np.array(fr) / sum(fr)
    return fr, np.array(dr)


def e_star(E):
    return E / (2.0 * (1.0 - NU ** 2))


def k_sjkr(gamma, E, rstar):
    """SJKR cohesion energy density (J/m3) whose pull-off force equals JKR's 1.5*pi*Gamma*R* at modulus E.

    LIGGGHTS SJKR: F_coh = k * A, A = pi a^2 ~ 2 pi R* delta. With Hertz repulsion (4/3) E* sqrt(R*) delta^1.5 the
    largest net pull is (2/3) pi^3 k^3 R*^2 / E*^2. Setting it equal to 1.5 pi Gamma R* gives
    k = (9 Gamma E*^2 / (4 pi^2 R*))^(1/3), i.e. k scales as E^(2/3) when E is softened.
    """
    es = e_star(E)
    return (9.0 * gamma * es ** 2 / (4.0 * math.pi ** 2 * rstar)) ** (1.0 / 3.0)


def delta_eq(gamma, E, rstar):
    """Equilibrium overlap of an unloaded SJKR contact (m)."""
    k = k_sjkr(gamma, E, rstar)
    return 9.0 / 4.0 * math.pi ** 2 * k ** 2 * rstar / e_star(E) ** 2


def rayleigh(r, E):
    gmod = E / (2.0 * (1.0 + NU))
    return math.pi * r * math.sqrt(RHO / gmod) / (0.1631 * NU + 0.8766)


def hertz_tc(r1, r2, v, E):
    """Hertz contact duration of two spheres closing at v."""
    m1, m2 = RHO * 4 / 3 * math.pi * r1 ** 3, RHO * 4 / 3 * math.pi * r2 ** 3
    ms, rs = m1 * m2 / (m1 + m2), r1 * r2 / (r1 + r2)
    return 2.87 * (ms ** 2 / (rs * e_star(E) ** 2 * v)) ** 0.2


def case_name(gap_um, v_mms, coh, E):
    tag = f"g{gap_um:g}_v{v_mms:g}_{coh}"
    if abs(E - E_SIM) / E_SIM > 1e-6:
        tag += f"_E{E / 1e6:g}MPa"
    return tag


# ---------------------------------------------------------------- input files -----------------------------------
def write_blade_stl(path, gap):
    """Blade cross-section in x-z (full semicircular nose + straight faces), extruded over y in [0, W]."""
    zc = gap + R_NOSE
    ztop = gap + R_NOSE + 1.2e-3
    n = 48
    prof = [(XC0 - R_NOSE, ztop), (XC0 - R_NOSE, zc)]
    for i in range(1, n):
        a = math.pi + math.pi * i / n          # from the trailing side, under the bottom, to the leading side
        prof.append((XC0 + R_NOSE * math.cos(a), zc + R_NOSE * math.sin(a)))
    prof += [(XC0 + R_NOSE, zc), (XC0 + R_NOSE, ztop), (XC0 - R_NOSE, ztop)]
    tris = []
    for (x1, z1), (x2, z2) in zip(prof[:-1], prof[1:]):
        a, b, c, d = (x1, 0.0, z1), (x2, 0.0, z2), (x2, W, z2), (x1, W, z1)
        tris += [(a, b, c), (a, c, d)]
    with open(path, "w") as f:
        f.write("solid blade\n")
        for t in tris:
            p = np.array(t)
            nrm = np.cross(p[1] - p[0], p[2] - p[0])
            nrm = nrm / (np.linalg.norm(nrm) + 1e-30)
            f.write(f" facet normal {nrm[0]:.6e} {nrm[1]:.6e} {nrm[2]:.6e}\n  outer loop\n")
            for v in t:
                f.write(f"   vertex {v[0]:.9e} {v[1]:.9e} {v[2]:.9e}\n")
            f.write("  endloop\n endfacet\n")
        f.write("endsolid blade\n")


def substrate_bumps(seed=1):
    """Random non-overlapping 30 um bumps (periodic in y) at 35 % projected cover."""
    rng = np.random.default_rng(seed)
    rb = D_BUMP / 2
    rc = math.sqrt(rb ** 2 - Z_BUMP ** 2)            # footprint radius at z = 0
    target = int(COVER_BUMP * LX * W / (math.pi * rc ** 2))
    pts = []
    cell = 2 * rb
    grid = {}
    tries = 0
    while len(pts) < target and tries < 200000:
        tries += 1
        x = rng.uniform(rb, LX - rb)
        y = rng.uniform(0, W)
        ix, iy = int(x / cell), int(y / cell)
        ok = True
        for jx in (ix - 1, ix, ix + 1):
            for jy in (iy - 1, iy, iy + 1):
                for (px, py) in grid.get((jx, jy % int(math.ceil(W / cell))), []):
                    dy = abs(py - y)
                    dy = min(dy, W - dy)
                    if (px - x) ** 2 + dy ** 2 < (2 * rb) ** 2:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            pts.append((x, y))
            grid.setdefault((ix, iy % int(math.ceil(W / cell))), []).append((x, y))
    return np.array(pts)


def write_data(path, bumps):
    with open(path, "w") as f:
        f.write("LIGGGHTS data file: substrate bumps (type %d)\n\n" % T_BUMP)
        f.write(f"{len(bumps)} atoms\n{NTYPES} atom types\n\n")
        f.write(f"0.0 {LX:.9e} xlo xhi\n0.0 {W:.9e} ylo yhi\n{ZLO:.9e} {ZHI:.9e} zlo zhi\n\nAtoms\n\n")
        for i, (x, y) in enumerate(bumps, 1):
            f.write(f"{i} {T_BUMP} {D_BUMP:.6e} {RHO:.1f} {x:.9e} {y:.9e} {Z_BUMP:.9e}\n")


def pair_matrix(fn):
    vals = []
    for i in range(1, NTYPES + 1):
        for j in range(1, NTYPES + 1):
            vals.append(fn(i, j))
    return " ".join(f"{v:.6g}" for v in vals)


def write_input(cdir, gap, v, coh, E, ndump_frames):
    fr, dr = psd_bins()
    rr = dr * 0.5e-6                                   # radii (m) per bin
    gamma = GAMMA[coh]

    def rad(t):
        if t <= NBIN:
            return rr[t - 1]
        if t == T_BUMP:
            return D_BUMP / 2
        return None                                    # flat wall

    def kfun(i, j):
        ri, rj = rad(i), rad(j)
        if ri is None and rj is None:
            return 0.0
        if ri is None or rj is None:
            rs = ri if rj is None else rj
        else:
            rs = ri * rj / (ri + rj)
        return k_sjkr(gamma, E, rs)

    rmin = rr.min()
    t_r = rayleigh(rmin, E)
    dt = 0.20 * t_r
    t_settle_hi, t_settle_lo = 2.5e-3, 1.5e-3
    t_spread = TRAVEL / v
    t_relax = 1.5e-3
    n_hi, n_lo = int(t_settle_hi / dt), int(t_settle_lo / dt)
    n_spread, n_relax = int(round(t_spread / dt)), int(t_relax / dt)
    n_dump = max(1, n_spread // ndump_frames)
    n_thermo = max(1, n_spread // 100)

    # dosed pile: solid volume DOSE * 0.5 * gap * travel * W, inserted at 30 % solids in front of the blade
    v_solid = DOSE * 0.5 * gap * TRAVEL * W
    x0p = XC0 + R_NOSE + 5e-6
    l_pile = 0.80e-3
    z0p = 13e-6
    h_ins = v_solid / (0.30 * l_pile * W)
    z1p = z0p + h_ins

    lines = []
    A = lines.append
    A(f"# desktop-lpbf powder spreading, generated by dem_spread.py: gap {gap*1e6:g} um, blade {v*1e3:g} mm/s, "
      f"cohesion {coh} (Gamma {gamma*1e3:g} mJ/m2), E_sim {E:.3g} Pa")
    A("atom_style granular\natom_modify map array\nboundary f p f\nnewton off\ncommunicate single vel yes\nunits si\nsoft_particles yes")
    A("processors 1 1 1")
    A("read_data substrate.data")
    A(f"neighbor {0.25 * 2 * rr.max():.4e} bin\nneigh_modify delay 0 exclude type {T_BUMP} {T_BUMP}")
    A(f"fix m1 all property/global youngsModulus peratomtype {' '.join([f'{E:.6g}'] * NTYPES)}")
    A(f"fix m2 all property/global poissonsRatio peratomtype {' '.join([f'{NU}'] * NTYPES)}")
    A(f"fix m3 all property/global coefficientRestitution peratomtypepair {NTYPES} {pair_matrix(lambda i, j: REST)}")
    A(f"fix m4 all property/global coefficientFriction peratomtypepair {NTYPES} {pair_matrix(lambda i, j: MU)}")
    A(f"fix m5 all property/global coefficientRollingFriction peratomtypepair {NTYPES} {pair_matrix(lambda i, j: MU_R)}")
    A(f"fix m6 all property/global cohesionEnergyDensity peratomtypepair {NTYPES} {pair_matrix(kfun)}")
    A("pair_style gran model hertz tangential history cohesion sjkr rolling_friction epsd2\npair_coeff * *")
    A(f"timestep {dt:.6e}")
    A(f"fix gravi all gravity {10 * G:.4f} vector 0.0 0.0 -1.0")
    A(f"group powder type {' '.join(str(t) for t in range(1, NBIN + 1))}")
    A(f"fix zwall powder wall/gran model hertz tangential history cohesion sjkr rolling_friction epsd2 primitive type {T_WALL} zplane 0.0")
    A(f"fix xw0 powder wall/gran model hertz tangential history rolling_friction epsd2 primitive type {T_WALL} xplane 0.0")
    A(f"fix xw1 powder wall/gran model hertz tangential history rolling_friction epsd2 primitive type {T_WALL} xplane {LX:.6e}")
    A(f"fix blade all mesh/surface/stress file blade.stl type {T_WALL}")
    A("fix bladewall powder wall/gran model hertz tangential history cohesion sjkr rolling_friction epsd2 mesh n_meshes 1 meshes blade")
    for b in range(NBIN):
        A(f"fix pts{b+1} powder particletemplate/sphere {PRIMES[b]} atom_type {b+1} density constant {RHO:.1f} radius constant {rr[b]:.6e} volume_limit 1e-18")
    A(f"fix pdd powder particledistribution/discrete/massbased {PRIMES[NBIN]} {NBIN} " +
      " ".join(f"pts{b+1} {fr[b]:.6f}" for b in range(NBIN)))
    A(f"region pile block {x0p:.6e} {x0p + l_pile:.6e} 0.0 {W:.6e} {z0p:.6e} {z1p:.6e} units box")
    A(f"fix ins powder insert/pack seed {PRIMES[NBIN+1]} distributiontemplate pdd vel constant 0. 0. -0.05 "
      f"insert_every once overlapcheck yes all_in yes volumefraction_region 0.30 region pile ntry_mc 20000")
    A("fix integr powder nve/sphere")
    A("compute kep powder ke\ncompute rke powder erotate/sphere")
    A(f"fix tscheck powder check/timestep/gran {max(1, n_spread // 10)} 0.2 0.2")
    A("thermo_style custom step time atoms c_kep c_rke f_blade[1] f_blade[2] f_blade[3]")
    A(f"thermo {n_thermo}\nthermo_modify lost ignore norm no")
    A(f"# settle the pile: {t_settle_hi*1e3:g} ms at 10 g, {t_settle_lo*1e3:g} ms at 1 g")
    A(f"run {n_hi}")
    A(f"unfix gravi\nfix gravi all gravity {G:.4f} vector 0.0 0.0 -1.0")
    A(f"run {n_lo}")
    A("unfix ins")
    A(f"dump d1 all custom {n_dump} dump/d_*.txt id type x y z radius vx vy vz")
    A(f"dump_modify d1 sort id")
    A(f"fix bf all ave/time 1 {max(1, n_thermo // 4)} {n_thermo} f_blade[1] f_blade[2] f_blade[3] file blade_force.txt")
    A(f"# spread: {TRAVEL*1e3:g} mm at {v*1e3:g} mm/s")
    A(f"fix mv all move/mesh mesh blade linear {v:.6e} 0.0 0.0")
    A(f"run {n_spread}")
    A("unfix mv")
    A(f"run {n_relax}")
    A("undump d1")
    A("dump dfin all custom 1 final.txt id type x y z radius vx vy vz\ndump_modify dfin sort id")
    A("run 1")
    with open(os.path.join(cdir, "in.spread"), "w") as f:
        f.write("\n".join(lines) + "\n")

    meta = dict(gap_m=gap, v_ms=v, coh=coh, gamma=gamma, E_sim=E, dt=dt, rayleigh_rmin=t_r, rmin=float(rmin),
                rmax=float(rr.max()), n_settle=n_hi + n_lo, n_spread=n_spread, n_relax=n_relax, n_dump=n_dump,
                n_thermo=n_thermo, pile=dict(x0=x0p, x1=x0p + l_pile, z0=z0p, z1=z1p, v_solid=v_solid),
                bins_d_um=dr.tolist(), bins_mass_frac=fr.tolist(),
                k_matrix={f"{i}-{j}": kfun(i, j) for i in range(1, NTYPES + 1) for j in range(i, NTYPES + 1)})
    with open(os.path.join(cdir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    return meta


def setup(gap_um, v_mms, coh, E, frames):
    name = case_name(gap_um, v_mms, coh, E)
    cdir = os.path.join(WORK, name)
    if os.path.isdir(cdir):
        shutil.rmtree(cdir)
    os.makedirs(os.path.join(cdir, "dump"))
    gap, v = gap_um * 1e-6, v_mms * 1e-3
    write_blade_stl(os.path.join(cdir, "blade.stl"), gap)
    write_data(os.path.join(cdir, "substrate.data"), substrate_bumps())
    meta = write_input(cdir, gap, v, coh, E, frames)
    os.makedirs(os.path.join(HERE, "inputs"), exist_ok=True)
    shutil.copy(os.path.join(cdir, "in.spread"), os.path.join(HERE, "inputs", f"in.{name}"))
    return name, cdir, meta


def run_case(gap_um, v_mms, coh, E, frames=40, cap_gb=3):
    name, cdir, meta = setup(gap_um, v_mms, coh, E, frames)
    env = dict(os.environ, OMP_NUM_THREADS="1")
    t0 = time.time()
    with open(os.path.join(cdir, "stdout.txt"), "w") as fo:
        p = subprocess.run(["/tmp/capmem", str(cap_gb), "liggghts", "-in", "in.spread", "-log", "log.liggghts"],
                           cwd=cdir, stdout=fo, stderr=subprocess.STDOUT, env=env)
    wall = time.time() - t0
    with open(os.path.join(cdir, "wall.json"), "w") as f:
        json.dump(dict(wall_s=wall, returncode=p.returncode), f)
    print(f"{name}: LIGGGHTS exit {p.returncode} after {wall/60:.1f} min", flush=True)
    if p.returncode != 0:
        os.system(f"tail -20 {cdir}/stdout.txt")
        return name
    post(name)
    return name


# ---------------------------------------------------------------- post-processing --------------------------------
def read_dump(path):
    with open(path) as f:
        lines = f.readlines()
    step = int(lines[1])
    n = int(lines[3])
    hdr = lines[8].split()[2:]
    arr = np.loadtxt(lines[9:9 + n]).reshape(n, -1)
    return step, {k: arr[:, i] for i, k in enumerate(hdr)}


def cap_volume(r, zc, zlo, zhi):
    """Volume of a sphere (radius r, centre height zc) between zlo and zhi (vectorised)."""
    def below(h):  # volume of the part of the sphere below the plane z = zc + h  (h in [-r, r])
        h = np.clip(h, -r, r)
        return np.pi * (r + h) ** 2 * (3 * r - (r + h)) / 3.0
    return below(zhi - zc) - below(zlo - zc)


def mass_dx(d_um, vol):
    """Volume-weighted D10/D50/D90 (um) of a set of particles."""
    if len(d_um) == 0:
        return [float("nan")] * 3
    o = np.argsort(d_um)
    c = np.cumsum(vol[o]) / np.sum(vol)
    return [float(np.interp(q, c, d_um[o])) for q in (0.1, 0.5, 0.9)]


def height_map(x, y, z, r, x0, x1, px):
    nx, ny = int(round((x1 - x0) / px)), int(round(W / px))
    hm = np.full((ny, nx), -np.inf)
    xs = x0 + (np.arange(nx) + 0.5) * px
    ys = (np.arange(ny) + 0.5) * px
    sel = (x + r > x0) & (x - r < x1)
    for xi, yi, zi, ri in zip(x[sel], y[sel], z[sel], r[sel]):
        ix0, ix1 = max(0, int((xi - ri - x0) / px)), min(nx, int((xi + ri - x0) / px) + 2)
        if ix1 <= ix0:
            continue
        iy0, iy1 = int(math.floor((yi - ri) / px)), int(math.floor((yi + ri) / px)) + 2
        iys = np.arange(iy0, iy1)
        yy = (iys + 0.5) * px
        dyy = yy - yi
        xx = xs[ix0:ix1]
        d2 = (xx[None, :] - xi) ** 2 + dyy[:, None] ** 2
        hz = np.where(d2 < ri * ri, zi + np.sqrt(np.clip(ri * ri - d2, 0, None)), -np.inf)
        rows = np.mod(iys, ny)
        for k, row in enumerate(rows):
            hm[row, ix0:ix1] = np.maximum(hm[row, ix0:ix1], hz[k])
    return hm


def post(name):
    from scipy import ndimage
    cdir = os.path.join(WORK, name)
    meta = json.load(open(os.path.join(cdir, "meta.json")))
    gap, v = meta["gap_m"], meta["v_ms"]
    _, d = read_dump(os.path.join(cdir, "final.txt"))
    typ = d["type"].astype(int)
    pw = typ <= NBIN
    x, y, z, r = d["x"], d["y"], d["z"], d["radius"]
    dia_um = 2e6 * r
    volp = 4.0 / 3.0 * np.pi * r ** 3

    # layer zone: from 0.3 mm past the blade's starting leading face to 0.25 mm behind its final bottom point
    xm0 = XC0 + R_NOSE + 0.30e-3
    xm1 = XC0 + TRAVEL - 0.25e-3
    area = (xm1 - xm0) * W
    inx = (x >= xm0) & (x < xm1)
    p = pw & inx
    v_layer = float(np.sum(cap_volume(r[p], z[p], 0.0, gap)))
    v_all = float(np.sum(volp[p]))
    v_above = float(np.sum(cap_volume(r[p], z[p], gap, 1.0)))
    b = (typ == T_BUMP) & inx
    v_bump = float(np.sum(cap_volume(r[b], z[b], 0.0, gap)))
    phi = v_layer / (area * gap - v_bump)
    h_solid = v_all / area                                        # solid-equivalent layer (m)

    # height map (2.5 um pixels): coverage, empty patches, roughness
    px = 2.5e-6
    hm_p = height_map(x[pw], y[pw], z[pw], r[pw], xm0, xm1, px)
    hm_b = height_map(x[typ == T_BUMP], y[typ == T_BUMP], z[typ == T_BUMP], r[typ == T_BUMP], xm0, xm1, px)
    covered = np.isfinite(hm_p)
    coverage = float(covered.mean())
    # empty patch: an uncovered pixel farther than D50/2 from any covered pixel (a D50 disc fits in the hole)
    big = np.vstack([~covered] * 3)                               # periodic in y
    dist = ndimage.distance_transform_edt(big)[covered.shape[0]:2 * covered.shape[0]] * px
    empty_d50 = float((dist > 0.5 * D50_UM * 1e-6).mean())
    empty_d90 = float((dist > 0.5 * 57e-6).mean())
    surf = np.where(covered, hm_p, np.maximum(np.where(np.isfinite(hm_b), hm_b, 0.0), 0.0))
    sa = float(np.mean(np.abs(surf - surf.mean())))
    sq = float(np.sqrt(np.mean((surf - surf.mean()) ** 2)))

    # thickness profile along x (0.1 mm bins): solid-equivalent thickness
    nb = int((xm1 - xm0) / 0.1e-3)
    edges = np.linspace(xm0, xm0 + nb * 0.1e-3, nb + 1)
    prof = []
    for a0, a1 in zip(edges[:-1], edges[1:]):
        s = pw & (x >= a0) & (x < a1)
        prof.append(float(np.sum(volp[s]) / ((a1 - a0) * W) * 1e6))

    # segregation: deposited layer vs feed (all powder) vs what is left in front of the blade
    feed = mass_dx(dia_um[pw], volp[pw])
    lay = mass_dx(dia_um[p], volp[p])
    rest = pw & (x > XC0 + TRAVEL)
    left = mass_dx(dia_um[rest], volp[rest])
    coarse = lambda s: float(np.sum(volp[s & (dia_um > 43)]) / max(np.sum(volp[s]), 1e-30))
    fine = lambda s: float(np.sum(volp[s & (dia_um < 30)]) / max(np.sum(volp[s]), 1e-30))
    d43 = lambda s: float(np.sum(volp[s] * dia_um[s]) / max(np.sum(volp[s]), 1e-30))
    binfr = lambda s: [float(np.sum(volp[s & (typ == t)]) / max(np.sum(volp[s]), 1e-30)) for t in range(1, NBIN + 1)]
    # jammed: powder contacts squeezed by more than 5 % of the smaller diameter (computed below with the overlaps)
    # deposited fraction of the dose
    v_feed = float(np.sum(volp[pw]))
    v_dep = float(np.sum(volp[pw & (x < XC0 + TRAVEL)]))
    dose_used = v_dep / (0.5 * gap * TRAVEL * W)

    # blade force (time-averaged, N per m of blade); steady window = middle half of the travel
    bf = np.loadtxt(os.path.join(cdir, "blade_force.txt"), comments="#")
    t_steps = bf[:, 0]
    t0 = meta["n_settle"]
    tt = (t_steps - t0) * meta["dt"]
    t_sp = TRAVEL / v
    win = (tt > 0.25 * t_sp) & (tt < 0.75 * t_sp)
    fx, fz = bf[win, 1] / W, bf[win, 3] / W
    pile_w = meta["pile"]["v_solid"] * RHO * G / W                # pile weight per m of blade at the start (N/m)

    # overlaps (from the final state): largest powder-powder overlap relative to the smaller diameter
    from scipy.spatial import cKDTree
    pts = np.c_[x[pw], np.mod(y[pw], W), z[pw]]
    tree = cKDTree(pts, boxsize=[1e3, W, 1e3])
    pairs = tree.query_pairs(2 * r.max(), output_type="ndarray")
    rp = r[pw]
    dd = np.linalg.norm(np.c_[pts[pairs[:, 0], 0] - pts[pairs[:, 1], 0],
                              (lambda a: a - W * np.round(a / W))(pts[pairs[:, 0], 1] - pts[pairs[:, 1], 1]),
                              pts[pairs[:, 0], 2] - pts[pairs[:, 1], 2]], axis=1)
    ov = rp[pairs[:, 0]] + rp[pairs[:, 1]] - dd
    rel = ov / (2 * np.minimum(rp[pairs[:, 0]], rp[pairs[:, 1]]))
    contact = ov > 0

    log = open(os.path.join(cdir, "log.liggghts")).read()
    loops = [float(m) for m in re.findall(r"Loop time of ([0-9.eE+-]+) on", log)]
    ts_warn = len(re.findall(r"(?i)warning.*time ?step", log))
    rayl = re.findall(r"(?i)rayleigh time[^\n]*", log)[-3:]
    wall = json.load(open(os.path.join(cdir, "wall.json")))

    res = dict(
        case=name, gap_um=gap * 1e6, v_mms=v * 1e3, cohesion=meta["coh"], gamma_mJm2=meta["gamma"] * 1e3,
        E_sim_MPa=meta["E_sim"] / 1e6, gap_over_D50=gap * 1e6 / D50_UM, gap_over_D90=gap * 1e6 / 57.0,
        n_powder=int(pw.sum()), n_bumps=int((typ == T_BUMP).sum()),
        zone_mm=[xm0 * 1e3, xm1 * 1e3], packing_fraction=phi, solid_equiv_thickness_um=h_solid * 1e6,
        solid_above_gap_um=v_above / area * 1e6,
        coverage=coverage, empty_patch_fraction_D50=empty_d50, empty_patch_fraction_D90=empty_d90,
        surface_mean_um=float(surf.mean() * 1e6), Sa_um=sa * 1e6, Sq_um=sq * 1e6,
        thickness_profile_um=prof,
        D10_50_90_feed_um=feed, D10_50_90_layer_um=lay, D10_50_90_leftover_um=left,
        coarse_gt43_feed=coarse(pw), coarse_gt43_layer=coarse(p), fine_lt30_feed=fine(pw), fine_lt30_layer=fine(p),
        coarse_gt43_leftover=coarse(rest), D43_feed_um=d43(pw), D43_layer_um=d43(p), D43_leftover_um=d43(rest),
        bin_mass_frac_feed=binfr(pw), bin_mass_frac_layer=binfr(p), bin_mass_frac_leftover=binfr(rest),
        n_contacts_over_5pct=int(np.sum(rel > 0.05)),
        dose_factor_used=dose_used, dose_factor_given=DOSE, leftover_fraction=1 - v_dep / v_feed,
        blade_Fx_N_per_m=float(np.mean(fx)) if len(fx) else None, blade_Fz_N_per_m=float(np.mean(fz)) if len(fz) else None,
        blade_Fx_sd_N_per_m=float(np.std(fx)) if len(fx) else None, blade_Fz_sd_N_per_m=float(np.std(fz)) if len(fz) else None,
        pile_weight_N_per_m=pile_w,
        max_overlap_rel=float(rel[contact].max()) if contact.any() else 0.0,
        p99_overlap_rel=float(np.percentile(rel[contact], 99)) if contact.any() else 0.0,
        dt_s=meta["dt"], rayleigh_rmin_s=meta["rayleigh_rmin"], dt_over_rayleigh=meta["dt"] / meta["rayleigh_rmin"],
        hertz_tc_D50_at_v_s=hertz_tc(18e-6, 18e-6, v, meta["E_sim"]), time_per_D50_at_v_s=36e-6 / v,
        steps=meta["n_settle"] + meta["n_spread"] + meta["n_relax"], loop_times_s=loops, wall_s=wall["wall_s"],
        timestep_warnings=ts_warn, liggghts_timestep_check=rayl,
    )
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{name}.json"), "w") as f:
        json.dump(res, f, indent=1)
    np.save(os.path.join(cdir, "heightmap.npy"), surf)
    np.save(os.path.join(cdir, "covered.npy"), covered)
    print(json.dumps({k: res[k] for k in ("case", "packing_fraction", "solid_equiv_thickness_um", "coverage",
                                          "empty_patch_fraction_D50", "Sa_um", "D10_50_90_layer_um",
                                          "blade_Fx_N_per_m", "blade_Fz_N_per_m", "max_overlap_rel", "wall_s")}))
    return res


def table():
    rows = []
    for fn in sorted(os.listdir(OUT)):
        if fn.endswith(".json") and fn.startswith("g"):
            rows.append(json.load(open(os.path.join(OUT, fn))))
    rows.sort(key=lambda r: (r["E_sim_MPa"], r["cohesion"], r["gap_um"], r["v_mms"]))
    hdr = ("| case | gap (µm) | gap/D90 | v (mm/s) | Γ (mJ/m²) | packing in gap | solid-equiv. layer (µm) | coverage | "
           "empty ≥ D50 | Sa (µm) | D[4,3] layer / feed (µm) | coarse > 43 µm, layer / feed | dose used | "
           "blade Fx, Fz (mN/m) | max overlap | run time (min) |")
    out = [hdr, "|" + "---|" * 16]
    for r in rows:
        out.append(f"| {r['case']} | {r['gap_um']:.0f} | {r['gap_over_D90']:.2f} | {r['v_mms']:.0f} | {r['gamma_mJm2']:.1f} | "
                   f"{r['packing_fraction']:.3f} | {r['solid_equiv_thickness_um']:.1f} | {r['coverage']:.3f} | "
                   f"{r['empty_patch_fraction_D50']:.3f} | {r['Sa_um']:.1f} | {r['D43_layer_um']:.1f} / "
                   f"{r['D43_feed_um']:.1f} | {r['coarse_gt43_layer']:.2f} / {r['coarse_gt43_feed']:.2f} | "
                   f"{r['dose_factor_used']:.2f} | {r['blade_Fx_N_per_m']*1e3:.1f}, {r['blade_Fz_N_per_m']*1e3:.1f} | "
                   f"{r['max_overlap_rel']*100:.1f} % | {r['wall_s']/60:.1f} |")
    txt = "\n".join(out) + "\n"
    with open(os.path.join(OUT, "dem_results.md"), "w") as f:
        f.write("# DEM results (generated by `analysis/powder/dem_spread.py table`)\n\n" + txt)
    print(txt)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "post", "table", "setup"])
    ap.add_argument("--gap", type=float, default=60.0, help="blade gap above the substrate mid-plane (um)")
    ap.add_argument("--speed", type=float, default=50.0, help="blade speed (mm/s)")
    ap.add_argument("--coh", choices=list(GAMMA), default="low")
    ap.add_argument("--E", type=float, default=E_SIM)
    ap.add_argument("--frames", type=int, default=40)
    ap.add_argument("--case")
    a = ap.parse_args()
    if a.cmd == "run":
        run_case(a.gap, a.speed, a.coh, a.E, a.frames)
    elif a.cmd == "setup":
        print(setup(a.gap, a.speed, a.coh, a.E, a.frames)[2])
    elif a.cmd == "post":
        post(a.case)
    else:
        table()
