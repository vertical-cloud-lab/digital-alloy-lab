"""CalculiX checks of the hot-swappable joints (issue #260, PR #266); companion to joint_calcs.py.

H1  plate bayonet at 200 C: the 6061 plate's three lugs and the heater block's ledge under the disc-spring preload chosen in
    joint_calcs.py (M50: 216 N, L75: 530 N) plus a 50 N blade strike at the plate rim. Plate on the block face is a
    compression-only support (active-set iteration on prescribed supports, no contact elements). Reports peak von Mises
    against 6061-T6 yield after long exposure at 204 C (103 MPa) and 225 C (~77 MPa) (ASM / Aluminum Association), and the
    change in flatness of the plate's top face.
H2  build-module body (316L, M50): (i) as modelled, pulled up to the floor by two captive M6 screws (2 x 2,182 N preload,
    joint_calcs.py) with the flange face against the floor as a compression-only support, dowel holes fixed sideways;
    (ii) the same body with a three-lobe flange on a three-groove kinematic seat (balls at r = 58 mm, 0/120/240 deg; each
    ball fixes the axial and tangential direction), preloaded at each ball by 218 N. Both carry gravity plus LC2
    (Z-magnet release, 202 N on the tube end besides the body's own weight). Reports stress, contact/separation and the
    movement of the spigot top (the powder plane).

Geometry: the model at commit REV (every cad/*.py at REV, via git show), so the analysis is stable while the model is
edited. REV was 1c7a977 until 2026-11-22; 9f45d80 since (the module body gained its welded bottom collar and the larger
spigot groove in between, so the M50 numbers moved too).
Helpers (meshing, .inp writing, ccx, .frd reading, rendering) are imported from analysis/fea/fea.py, including its solver
choice: SPOOLES up to 60,000 nodes (the plates), ccx's ITERATIVE CHOLESKY above (the heater blocks and the module body;
with SPOOLES the ~173,000-node L75 block outgrew the 10 GB cap on 2026-11-21). H2, H1 M50 and H1 L75 each run in their
own process.

Run:  OMP_NUM_THREADS=2 xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/analysis/hotswap/hotswap_fea.py [H1 H2]
Out:  analysis/out/hotswap/fea_hotswap.md, fea_hotswap.json, PNGs; scratch in /tmp/fea-hotswap
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPO = ROOT.parent
OUT = ROOT / "analysis" / "out" / "hotswap"
REV = "9f45d80"
SCRATCH = pathlib.Path(os.environ.get("FEA_RUN", "/tmp/fea-hotswap"))
os.environ["FEA_RUN"] = str(SCRATCH)
SNAP = SCRATCH / "snap"
SNAP.mkdir(parents=True, exist_ok=True)
CAD_FILES = [p.rsplit("/", 1)[-1][:-3] for p in subprocess.run(["git", "ls-tree", "--name-only", REV, "desktop-lpbf/cad/"], cwd=REPO,
                                                                 capture_output=True, text=True, check=True).stdout.split() if p.endswith(".py")]
for name in CAD_FILES:              # lpbf_low imports vendor_parts, fasteners, joints, ... from cad/ since 1c7a977
    src = subprocess.run(["git", "show", f"{REV}:desktop-lpbf/cad/{name}.py"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    (SNAP / f"{name}.py").write_text(src)
sys.path.insert(0, str(SNAP))
import lpbf_low as M  # noqa: E402  (snapshot; cached, so fea.py's own import gets the same module)
import module_params as MP  # noqa: E402
import modules_low as ML  # noqa: E402

sys.path.insert(0, str(ROOT / "analysis" / "fea"))
import fea as F  # noqa: E402

F.RUN = SCRATCH
AL200 = dict(E=62.0e3, nu=0.33, rho=2700)          # 6061 at 200 C (MMPDS-type modulus curve, ~10 % below RT; approximate)
SS316 = dict(E=193e3, nu=0.30, rho=7990)
SY_200, SY_225 = 103.0, 77.0                        # 6061-T6 after 10,000 h at temperature (ASM; 225 C interpolated)
SY_316L = 170.0
PRELOAD = {"M50": 216.0, "L75": 530.0}              # joint_calcs.py: bayonet + 97125K111 disc springs (1.25 x requirement)
STRIKE = 50.0
LC2_EXTRA = 217.4 - 1.61 * 9.81                     # LC2 minus the body's own weight (applied by gravity), N
SCREW_FI = 2182.0                                   # joint_calcs.py: captive M6, 0.75 F_p on the reduced shank
KIN_PRE = 218.0                                     # per ball: 3 x LC2 / 3


def safe_render(*a, **k):
    """F.render draws in a child process (render_fea.py), so a VTK/OpenGL failure under Xvfb can't take the solver run down."""
    try:
        F.render(*a, **k)
    except Exception as e:  # noqa: BLE001
        print(f"  render failed for {a[3]} ({e}); results are unaffected")


def module_parts(key):
    got = []

    def add(name, shape, color, step, explode=(0, 0, 0), **kw):
        got.append((name, shape))
    ML.add_build_module(M, add, key, 4)
    return got


def pick(parts, prefix):
    for n, s in parts:
        if n.startswith(prefix):
            return s
    raise KeyError(prefix)


def solve_active_set(job, m, mat, contact_ids, sign, other_bc, loads, extra_sets="", max_it=8, tol=1e-3):
    """Compression-only support on contact_ids (uz = 0) by an active-set loop.
    sign = +1: the support is below (it pushes +z); -1: above (it pushes -z)."""
    active = np.array(sorted(set(map(int, contact_ids))), dtype=np.int64)
    released = np.array([], dtype=np.int64)
    for it in range(max_it):
        F.write_model(job, m, mat, extra_sets + F.nset("CONTACT", active))
        F.append(job, f"*STEP\n*STATIC, SOLVER={F.solver_for(m)}\n*BOUNDARY\nCONTACT,3,3\n" + other_bc + loads +
                 "*NODE FILE\nU,RF\n*EL FILE\nS\n*END STEP\n")
        F.run_ccx(job)
        b = F.read_frd(job)
        U = F.field(m, [x for x in b if x["name"] == "DISP"][-1], 3)
        S = F.field(m, [x for x in b if x["name"] == "STRESS"][-1], 6)
        RF = F.field(m, [x for x in b if x["name"] == "FORC"][-1], 3)
        rf = RF[m["idx"][active], 2] * sign                  # > 0: compression
        uz_rel = U[m["idx"][released], 2] * sign if len(released) else np.array([])
        tens = active[rf < -tol]
        pen = released[uz_rel < -tol * 1e-3] if len(released) else np.array([], dtype=np.int64)
        print(f"  {job} it {it}: {len(active)} in contact, {len(tens)} in tension, {len(pen)} penetrating")
        if len(tens) == 0 and len(pen) == 0:
            break
        active = np.setdiff1d(active, tens)
        active = np.union1d(active, pen)
        released = np.setdiff1d(np.union1d(released, tens), pen)
    return U, S, F.von_mises(S), RF, active, released


# --------------------------------------------------------------------------------------------
# H1: plate lugs and block ledge
# --------------------------------------------------------------------------------------------
def h1(key, R):
    parts = module_parts(key)
    plate = pick(parts, f"Build plate {key}")
    block = pick(parts, f"Heater block {key}")
    m_ = MP.MODULES[key]
    Rp, Rb = m_["plate_d"] / 2, m_["block_d"] / 2
    zb1 = -MP.PLATE_T
    Fpre = PRELOAD[key]
    res = {}

    # ---- plate ----
    m = F.mesh_shape(plate, f"h1_plate_{key}", hmax=2.0, hmin=0.35, curv=16)
    xyz = m["xyz"]
    lug_top = F.surfaces(m, F.planar("z", zb1 - 2.2))
    bottom = F.surfaces(m, F.planar("z", zb1))
    top = F.surfaces(m, F.planar("z", 0.0))
    spig = F.surfaces(m, lambda x0, y0, z0, x1, y1, z1: z0 > zb1 - 4.05 and z1 < zb1 + 0.05 and max(abs(x0), abs(x1), abs(y0), abs(y1)) < 6.05)
    lug_nodes = F.nodes_on(m, lug_top, lambda q: np.hypot(q[:, 0], q[:, 1]) > 5.4)
    sup = F.nodes_on(m, bottom, lambda q: (np.hypot(q[:, 0], q[:, 1]) >= 8.9) & (np.hypot(q[:, 0], q[:, 1]) <= Rb))
    side = F.nodes_on(m, spig, lambda q: np.abs(np.hypot(q[:, 0], q[:, 1]) - 6.0) < 0.05)
    topn = F.nodes_on(m, top)
    q = xyz[m["idx"][topn]]
    rim = topn[(np.hypot(q[:, 0], q[:, 1]) > Rp - 1.0) & (q[:, 0] < 0) & (np.abs(q[:, 1]) < 4.0)]
    for case, strike in (("preload", 0.0), ("preload + 50 N strike", STRIKE)):
        loads = "*CLOAD\n" + F.cload_lines(lug_nodes, (0, 0, -Fpre)) + (F.cload_lines(rim, (strike, 0, 0)) if strike else "")
        job = f"h1_plate_{key}_{'s' if strike else 'p'}"
        U, S, vm, RF, act, rel = solve_active_set(job, m, AL200, sup, +1, "SIDE,1,2\n", loads, F.nset("SIDE", side))
        uz_top = U[m["idx"][topn], 2]
        lugmask = (xyz[:, 2] < zb1 + 0.5) & (np.hypot(xyz[:, 0], xyz[:, 1]) < 9.0)
        i = int(np.argmax(vm))
        il = int(np.argmax(np.where(lugmask, vm, 0)))
        res[f"plate {case}"] = dict(vm_max=float(vm[i]), at=xyz[i].tolist(), vm_lug=float(vm[il]), flatness_um=float((uz_top.max() - uz_top.min()) * 1e3),
                                   contact_frac=float(len(act) / max(len(sup), 1)), F_pre=Fpre, nodes=len(m["ntags"]), solver=F.solver_for(m))
        if strike:
            png = f"h1_plate_{key}.png"
            safe_render(m, U, vm, OUT / png, f"H1 {key} plate, 6061 at 200 C: {Fpre:.0f} N bayonet preload + 50 N strike\n"
                     f"max von Mises {vm[i]:.1f} MPa (lug {vm[il]:.1f}); top-face flatness change {res[f'plate {case}']['flatness_um']:.2f} um",
                     (0.6, -1.0, -0.9), mark=xyz[i], clim=(0, max(SY_225, vm.max())))
            res[f"plate {case}"]["png"] = png
    # ---- block ledge ----
    m = F.mesh_shape(block, f"h1_block_{key}", hmax=2.0, hmin=0.35, curv=16)
    xyz = m["xyz"]
    ledge = F.surfaces(m, F.planar("z", zb1 - 2.0))
    topf = F.surfaces(m, F.planar("z", zb1))
    botf = F.surfaces(m, F.planar("z", zb1 - MP.BLOCK_T))
    lugpos = []
    for a in (0.0, 120.0, 240.0):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        lugpos.append((ca, sa))

    def in_lug(q):
        ok = np.zeros(len(q), bool)
        for ca, sa in lugpos:
            along = q[:, 0] * ca + q[:, 1] * sa
            across = -q[:, 0] * sa + q[:, 1] * ca
            ok |= (along > 5.5) & (along < 8.6) & (np.abs(across) < 3.0)
        return ok
    led = F.nodes_on(m, ledge, in_lug)
    tp = F.nodes_on(m, topf, lambda q: np.hypot(q[:, 0], q[:, 1]) >= 8.9)
    L = ML.block_layout(key)
    pads = F.nodes_on(m, botf, lambda q: np.any([np.hypot(q[:, 0] - rr * math.cos(math.radians(aa)), q[:, 1] - rr * math.sin(math.radians(aa))) < L["sd"] / 2
                                                  for rr, aa in L["standoffs"]], axis=0))
    pin = F.nearest(m, (0.0, -Rb, zb1 - MP.BLOCK_T / 2))
    pin2 = F.nearest(m, (0.0, Rb, zb1 - MP.BLOCK_T / 2))
    job = f"h1_block_{key}"
    F.write_model(job, m, AL200, F.nset("LEDGE", led) + F.nset("TOPF", tp) + F.nset("PADS", pads))
    loads = "*CLOAD\n" + F.cload_lines(led, (0, 0, Fpre)) + F.cload_lines(tp, (0, 0, -Fpre))
    F.append(job, F.static_step(f"PADS,3,3\n{pin},1,2\n{pin2},1,1\n", loads, solver=F.solver_for(m)))
    F.run_ccx(job)
    U, S, vm = F.static_results(m, job)
    i = int(np.argmax(vm))
    png = f"h1_block_{key}.png"
    safe_render(m, U, vm, OUT / png, f"H1 {key} heater-block ledge, 6061 at 200 C: {Fpre:.0f} N from the lugs\nmax von Mises {vm[i]:.1f} MPa",
             (0.5, -0.8, 1.0), mark=xyz[i], clim=(0, max(SY_225, vm.max())))
    res["block ledge"] = dict(vm_max=float(vm[i]), at=xyz[i].tolist(), png=png, F_pre=Fpre, nodes=len(m["ntags"]), solver=F.solver_for(m))
    R[f"H1_{key}"] = res
    return res


# --------------------------------------------------------------------------------------------
# H2: build-module body on the floor
# --------------------------------------------------------------------------------------------
def three_lobe_body(key):
    """Module body with the two x-tabs and two y-lugs replaced by three lobes at 0/120/240 deg for a kinematic seat."""
    m_ = MP.MODULES[key]
    R_, W = m_["bore"] / 2, m_["wall"]
    zf = -MP.FLOOR_T
    pr = MP.PORT_D / 2
    z_stop = ML.zlevels()["z_stop"]
    spig = M.tube(pr - MP.SPIGOT_FIT, R_, (0, 0, zf), "z", MP.FLOOR_T)
    spig = spig.cut(M.tube(pr, pr - 2.9, (0, 0, zf + 4.0), "z", 3.6))
    lobes = []
    for a in (0.0, 120.0, 240.0):
        lb = M.rbox(30.0, 66.0, -12.0, 12.0, zf - MP.FLANGE_T, zf, 6).rotate(M.V(0, 0, 0), M.V(0, 0, 1), a)
        lobes.append(lb)
    fl = M.fuse([M.cyl(MP.FLANGE_D / 2, (0, 0, zf - MP.FLANGE_T), "z", MP.FLANGE_T)] + lobes)
    fl = fl.cut(M.cyl(R_, (0, 0, zf - MP.FLANGE_T - 1), "z", MP.FLANGE_T + 2))
    tb = M.tube(R_ + W, R_, (0, 0, z_stop), "z", (zf - MP.FLANGE_T) - z_stop)
    return M.fuse([spig, fl, tb])


def h2(key, R):
    parts = module_parts(key)
    zf = -MP.FLOOR_T
    z_stop = ML.zlevels()["z_stop"]
    res = {}
    for variant in ("screws", "kinematic"):
        body = pick(parts, f"Build module {key}: spigot") if variant == "screws" else three_lobe_body(key)
        m = F.mesh_shape(body, f"h2_{variant}_{key}", hmax=3.0, hmin=0.8, curv=12)
        xyz = m["xyz"]
        topface = F.surfaces(m, F.planar("z", zf))
        botface = F.surfaces(m, F.planar("z", zf - MP.FLANGE_T))
        tube_end = F.surfaces(m, F.planar("z", z_stop))
        spig_top = F.surfaces(m, F.planar("z", 0.0))
        tub = F.nodes_on(m, tube_end)
        st = F.nodes_on(m, spig_top)
        grav = "*DLOAD\nEALL,GRAV,9810.,0.,0.,-1.\n"
        if variant == "screws":
            cont = F.nodes_on(m, topface, lambda q: np.hypot(q[:, 0], q[:, 1]) > MP.PORT_D / 2 - MP.SPIGOT_FIT + 0.01)
            heads = [F.nodes_on(m, botface, lambda q, s=s: (np.hypot(q[:, 0] - s * MP.SCREW_X, q[:, 1]) > 3.4) & (np.hypot(q[:, 0] - s * MP.SCREW_X, q[:, 1]) < 5.0))
                     for s in (-1, 1)]
            q = xyz[m["idx"][m["ntags"]]]
            dow = m["ntags"][(np.abs(np.hypot(q[:, 0], np.abs(q[:, 1]) - MP.DOWEL_Y) - 3.0) < 0.05) & (q[:, 2] < zf + 0.01) & (q[:, 2] > zf - MP.FLANGE_T - 0.01)]
            loads = "*CLOAD\n" + "".join(F.cload_lines(hn, (0, 0, SCREW_FI)) for hn in heads) + F.cload_lines(tub, (0, 0, -LC2_EXTRA)) + grav
            U, S, vm, RF, act, rel = solve_active_set(f"h2_screws_{key}", m, SS316, cont, -1, "DOW,1,2\n", loads, F.nset("DOW", dow))
            gap = (-U[m["idx"][rel], 2]).max() * 1e3 if len(rel) else 0.0
            res["screws"] = dict(contact_frac=float(len(act) / len(cont)), max_gap_um=float(gap))
        else:
            balls = []
            for a in (0.0, 120.0, 240.0):
                bx, by = 58.0 * math.cos(math.radians(a)), 58.0 * math.sin(math.radians(a))
                balls.append(F.nodes_on(m, topface, lambda q, bx=bx, by=by: np.hypot(q[:, 0] - bx, q[:, 1] - by) < 1.2))
                if len(balls[-1]) < 3:
                    balls[-1] = np.array([F.nearest(m, (bx, by, zf))])
            pre = [F.nodes_on(m, botface, lambda q, a=a: np.hypot(q[:, 0] - 58.0 * math.cos(math.radians(a)), q[:, 1] - 58.0 * math.sin(math.radians(a))) < 5.0)
                   for a in (0.0, 120.0, 240.0)]
            allb = np.concatenate(balls)
            job = f"h2_kinematic_{key}"
            F.write_model(job, m, SS316, F.nset("BALLS", allb) + "*TRANSFORM, NSET=BALLS, TYPE=C\n0.,0.,0.,0.,0.,1.\n")
            loads = "*CLOAD\n" + "".join(F.cload_lines(p, (0, 0, KIN_PRE)) for p in pre) + F.cload_lines(tub, (0, 0, -LC2_EXTRA)) + grav
            # preload goes in at the lobe underside and out through the ball (support); the supports fix axial + tangential
            F.append(job, f"*STEP\n*STATIC, SOLVER={F.solver_for(m)}\n*BOUNDARY\nBALLS,2,3\n" + loads + "*NODE FILE\nU,RF\n*EL FILE\nS\n*END STEP\n")
            F.run_ccx(job)
            b = F.read_frd(job)
            U = F.field(m, [x for x in b if x["name"] == "DISP"][-1], 3)
            S = F.field(m, [x for x in b if x["name"] == "STRESS"][-1], 6)
            vm = F.von_mises(S)
            res["kinematic"] = dict(ball_r=58.0, preload_per_ball=KIN_PRE)
        uzs = U[m["idx"][st], 2]
        i = int(np.argmax(vm))
        flmask = (xyz[:, 2] <= zf + 0.01) & (xyz[:, 2] >= zf - MP.FLANGE_T - 0.01)
        ifl = int(np.argmax(np.where(flmask, vm, 0)))
        res[variant].update(nodes=len(m["ntags"]), solver=F.solver_for(m), vm_max=float(vm[i]), at=xyz[i].tolist(), vm_flange=float(vm[ifl]), spigot_top_uz_mean_um=float(uzs.mean() * 1e3),
                            spigot_top_uz_range_um=float((uzs.max() - uzs.min()) * 1e3), sy=SY_316L)
        png = f"h2_{variant}_{key}.png"
        title = ("H2 M50 module body, 316L: 2 captive M6 at 2.18 kN + gravity + LC2" if variant == "screws" else
                 "H2 M50 module body, 316L, three-lobe flange on a 3-groove kinematic seat (218 N per ball) + gravity + LC2")
        safe_render(m, U, vm, OUT / png, f"{title}\nmax von Mises {vm[i]:.1f} MPa; spigot top moves {uzs.mean() * 1e3:.2f} um "
                 f"(range {(uzs.max() - uzs.min()) * 1e3:.2f} um)", (0.9, -1.2, -0.7), mark=xyz[i])
        res[variant]["png"] = png
    R[f"H2_{key}"] = res
    return res


JOBS = {"H2": ("H2_M50", lambda R: h2("M50", R)), "H1:M50": ("H1_M50", lambda R: h1("M50", R)), "H1:L75": ("H1_L75", lambda R: h1("L75", R))}


def run_job(job, jpath):
    """One job in this process: the previous result for its key is kept under R["previous"] if it came from another commit."""
    key, fn = JOBS[job]
    R = json.loads(jpath.read_text()) if jpath.exists() else {}
    for k in ("H2_M50", "H1_M50", "H1_L75"):         # results from before per-result revs carry the file's single rev
        if k in R and "rev" not in R[k] and not str(R.get("rev", "")).startswith("mixed"):
            R[k]["rev"] = R["rev"]
    old = R.get(key)
    if old and old.get("rev") != REV:
        R.setdefault("previous", {})[key] = dict(old, rev=old.get("rev", "unknown"))
    fn(R)
    R[key]["rev"] = REV
    jpath.write_text(json.dumps(R, indent=1))


def main():
    args = sys.argv[1:] or ["H1", "H2"]          # "report" rewrites fea_hotswap.md from the json without solving
    jobs = []
    for a in args:
        jobs += ["H1:M50", "H1:L75"] if a == "H1" else [a] if a in JOBS else []
    OUT.mkdir(parents=True, exist_ok=True)
    jpath = OUT / "fea_hotswap.json"
    failed = []
    if len(jobs) > 1:                             # each job in its own process: memory is returned in between
        failed = [j for j in jobs if subprocess.run([sys.executable, __file__, j]).returncode != 0]
    elif jobs:
        run_job(jobs[0], jpath)
    R = json.loads(jpath.read_text()) if jpath.exists() else {}
    revs = {R[k].get("rev", R.get("rev")) for k in ("H2_M50", "H1_M50", "H1_L75") if k in R}
    R["rev"] = revs.pop() if len(revs) == 1 else "mixed: " + ", ".join(sorted(revs))
    jpath.write_text(json.dumps(R, indent=1))
    write_md(R)
    if failed:
        sys.exit(f"failed: {' '.join(failed)}")


def write_md(R):
    prev = R.get("previous", {})
    md = ["# CalculiX checks of the hot-swappable joints", "",
          f"Generated by [`analysis/hotswap/hotswap_fea.py`](../../hotswap/hotswap_fea.py) from the model at commit {R['rev']}. C3D10 (gmsh), ccx: SPOOLES up to 60,000 nodes, "
          "ITERATIVE CHOLESKY above (the module body and the heater blocks). Contact is modelled as compression-only prescribed supports, solved by an active-set loop (no contact elements).", ""]
    for key in ("M50", "L75"):
        r = R.get(f"H1_{key}")
        if not r:
            continue
        md += [f"## H1 {key}: bayonet lugs and ledge, 6061 at 200 °C (E 62 GPa), preload {r['block ledge']['F_pre']:.0f} N", "",
               "| case | peak von Mises, MPa | in the lugs, MPa | vs 103 MPa (204 °C, 10,000 h) / 77 MPa (225 °C) | top-face flatness change, µm | plate face in contact |",
               "|---|---|---|---|---|---|"]
        for c in ("preload", "preload + 50 N strike"):
            x = r[f"plate {c}"]
            md.append(f"| plate, {c} | {x['vm_max']:.1f} | {x['vm_lug']:.1f} | {SY_200 / max(x['vm_lug'], 1e-9):.2f} / {SY_225 / max(x['vm_lug'], 1e-9):.2f} | "
                      f"{x['flatness_um']:.2f} | {100 * x['contact_frac']:.0f} % |")
        x = r["block ledge"]
        md.append(f"| block ledge | {x['vm_max']:.1f} | – | {SY_200 / x['vm_max']:.2f} / {SY_225 / x['vm_max']:.2f} | – | – |")
        o = prev.get(f"H1_{key}")
        if o:
            a, b = o["plate preload + 50 N strike"], r["plate preload + 50 N strike"]
            md += ["", f"Against the run on the model at {o['rev']}: lugs {a['vm_lug']:.1f} → {b['vm_lug']:.1f} MPa, flatness change with the strike "
                   f"{a['flatness_um']:.2f} → {b['flatness_um']:.2f} µm, ledge {o['block ledge']['vm_max']:.1f} → {x['vm_max']:.1f} MPa."]
        md += [""] + [f"![]({q})" for q in (r['plate preload + 50 N strike']['png'], x['png']) if (OUT / q).exists()] + [""]
    r = R.get("H2_M50")
    if r:
        md += ["## H2 M50 module body (316L) on the chamber floor, gravity + LC2", "",
               "| hold | peak von Mises, MPa | in the flange, MPa | vs S_y 170 (316L) | spigot top moves, µm (mean / range) | contact |",
               "|---|---|---|---|---|---|"]
        s = r["screws"]
        md.append(f"| 2 captive M6, 2 × 2,182 N | {s['vm_max']:.1f} | {s['vm_flange']:.1f} | {SY_316L / s['vm_flange']:.2f} | {s['spigot_top_uz_mean_um']:.2f} / {s['spigot_top_uz_range_um']:.2f} | "
                  f"{100 * s['contact_frac']:.0f} % of the flange face; max gap {s['max_gap_um']:.2f} µm |")
        k = r["kinematic"]
        md.append(f"| 3-groove kinematic seat, 218 N per ball | {k['vm_max']:.1f} | {k['vm_flange']:.1f} | {SY_316L / k['vm_flange']:.2f} | {k['spigot_top_uz_mean_um']:.2f} / {k['spigot_top_uz_range_um']:.2f} | "
                  "3 balls (axial + tangential fixed) |")
        o = prev.get("H2_M50")
        if o:
            md += ["", f"Against the run on the model at {o['rev']} (before the module body's welded bottom collar and the wider spigot groove): flange "
                   f"{o['screws']['vm_flange']:.1f} → {s['vm_flange']:.1f} MPa with the screws, {o['kinematic']['vm_flange']:.1f} → {k['vm_flange']:.1f} MPa on the kinematic seat; "
                   f"spigot top {o['screws']['spigot_top_uz_mean_um']:.2f} → {s['spigot_top_uz_mean_um']:.2f} µm."]
        md += [""] + [f"![]({q})" for q in (s['png'], k['png']) if (OUT / q).exists()] + [""]
    (OUT / "fea_hotswap.md").write_text("\n".join(md) + "\n")
    print("wrote", OUT / "fea_hotswap.md")


if __name__ == "__main__":
    main()
