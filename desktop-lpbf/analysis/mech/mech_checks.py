"""Textbook checks on the low-profile desktop LPBF (issue #260, PR #266): Shigley-style machine elements, the Z
coupling's friction budget, and heat-transfer estimates for the chamber and the cover slide.

  A  Z coupling: every force on the piston and rod (seal friction from Parker's friction charts, break-out after a
     dwell, the rod's pressure force at vacuum, gravity) against what the NdFeB pot magnet can really pull.
  B  Recoater ball screw: critical speed, buckling, DN and life (THK/Shigley formulas).
  C  Screws, latches, hinges: preload and torque for the lid, latch and hinge loads from door_seal_fea.py.
  D  Chamber warm-up over a long build: a lumped thermal network with natural convection (Churchill-Chu, McAdams),
     radiation from bare and anodized aluminium, and the argon loop; with and without a water-cooled floor.
  E  Cover slide: thermal lens from absorbed laser power and the focus shift it causes, vs the Rayleigh range.
  F  Galvo and optics-bridge thermal drift over that warm-up.

Run:  python desktop-lpbf/analysis/mech/mech_checks.py  ->  analysis/out/mech/mech.{md,json}
Pure Python + numpy.
"""
from __future__ import annotations

import json
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "analysis" / "out" / "mech"
LBF, IN = 4.448, 25.4
SIGMA = 5.670e-8

SOURCES = {
    1: "Parker O-Ring Handbook ORD 5700, §5.11-5.14: F = fc Lr + fh Ar; Fig. 5-9 (fc vs compression and hardness), Fig. 5-10 (fh), "
       "break-out up to 3x running friction after a rest (§5.14.1)",
    2: "THK ball screw technical data: critical speed N = lambda * d_r / L^2 * 1e7 (rpm), buckling P = eta * d_r^4 / L^2 * 1e4 (N), "
       "DN <= 70,000; L10 = (Ca / (fw Fa))^3 * 1e6 rev. https://tech.thk.com/en/products/pdf/en_b15_011.pdf",
    3: "Shigley's Mechanical Engineering Design, 10th ed., Ch. 8 (T = K F d, K = 0.2 dry steel; A4-70 proof 450 MPa per ISO 3506-1)",
    4: "Churchill & Chu (1975), Int. J. Heat Mass Transfer 18, 1323 (vertical plates); McAdams (1954) horizontal plates; "
       "emissivity of bare machined 6061 0.05-0.1, black anodize ~0.8 (Incropera, Fundamentals of Heat and Mass Transfer, App. A.11)",
    5: "Thermal lens of an absorbing plate: dioptric power D = P_abs (dn/dT) / (2 pi k w^2) (thin plate, Gaussian beam; e.g. Koechner, "
       "Solid-State Laser Engineering, §7.1); fused silica k = 1.38 W/mK, dn/dT = 9.6e-6 /K at 1064 nm (Corning 7980 data sheet)",
    6: "Focus shift of a measured 400 W system with a contaminated window: -22 to -30 mm (LiM 2017 contribution 31, "
       "https://www.wlt.de/lim/Proceedings2017/Data/PDF/Contribution31_final.pdf), as cited in low-profile.md",
    7: "NdFeB reversible temperature coefficient of Br about -0.12 %/K (grade N42 data, e.g. Arnold Magnetic Technologies); "
       "McMaster 5679K95 pot magnet, 44 lbf, rated to 79 C (modules.md)",
    8: "SCANLAB basiCube / hurrySCAN data sheets: long-term offset drift < 0.3 mrad over 8 h after warm-up, gain drift < 0.1 % over 8 h; "
       "temperature drift: offset < 30 urad/K, gain < 50 ppm/K (typical class values; check the purchased head)",
}


def section_A():
    """Z coupling friction budget (M50)."""
    rod_in = 0.625
    Lr = math.pi * rod_in                                      # rubbing length per rod O-ring, in
    # Parker Fig. 5-9: fc (lb/in) at 25 % compression: 70A 1.6, 80A 3.1, 90A 4.2; linear in compression.
    fc = lambda comp, shore: np.interp(shore, [70, 80, 90], [1.6, 3.1, 4.2]) * comp / 0.25
    comp = (0.17, 0.21, 0.26)                                  # min / nom / max squeeze, seals.py rod gland
    run = [2 * fc(c, 75) * Lr * LBF for c in comp]             # two O-rings in tandem, N (oil-lubricated basis)
    dry = 1.5                                                  # unlubricated or PFPE-greased in argon (assumption)
    breakout = 3.0                                             # Parker: up to 3x running after a dwell
    Ar_in2 = math.pi / 4 * (0.787 ** 2 - 0.625 ** 2)
    fh_vac = 10.0                                              # lb/in2 of projected area near 0-15 psi (Fig. 5-10 intercept)
    F_press_fric = 2 * fh_vac * Ar_in2 * LBF                   # extra friction at full vacuum
    rod_area = math.pi / 4 * (15.875e-3) ** 2
    F_rod_vac = 101325 * rod_area                              # atmosphere pushes the rod into the chamber at vacuum
    F_rod_20 = -2000 * rod_area                                # +20 mbar pushes it out (down)
    circ = math.pi * 50.8
    bore_seal = (0.05 * circ, 0.40 * circ)                     # felt + PTFE scraper, 0.05-0.4 N/mm (assumption, see note)
    wiper = (0.03 * circ, 0.10 * circ)                         # PTFE split-ring rim wiper on its own spring
    m_piston = 0.34                                            # kg, MuJoCo (modules.md §5)
    powder_40 = 0.040 * math.pi / 4 * 0.0508 ** 2 * 1450      # kg of powder and part above a plate at the end of a build
    W = (m_piston + powder_40) * 9.81
    # pot magnet: 196 N rated on thick low-carbon steel at zero gap
    mag_rated = 44 * LBF
    k_430 = (0.55, 0.75)                                       # 430 SS striker vs 1018 (Bsat ~1.5 vs 2.1 T): force ~ B^2 at saturation
    k_T = 1 - 0.0012 * (68 - 20)                               # coupling face at 68 C (thermal FEA) -> ~94 %
    k_gap = (0.73, 1.0)                                        # 0.05 mm of debris/oxide; vendor curves put 0.1 mm at ~27 % for a small pole
    mag_eff = (mag_rated * k_430[0] * k_T * k_gap[0], mag_rated * k_430[1] * k_T * k_gap[1])
    need_run = (run[0] * 1.0 + bore_seal[0] + wiper[0] - W, run[2] * dry + bore_seal[1] + wiper[1] - W)
    need_breakout = (run[1] * dry * breakout + bore_seal[1] * 1.5 + wiper[1] - W, run[2] * dry * breakout + bore_seal[1] * 2 + wiper[1] - W)
    return dict(rod_oring_running_N=run, dry_factor=dry, breakout_factor=breakout, pressure_friction_at_vacuum_N=F_press_fric,
                rod_force_at_vacuum_up_N=F_rod_vac, rod_force_at_20mbar_N=F_rod_20, bore_seal_N=bore_seal, wiper_N=wiper,
                weight_N=W, magnet_rated_N=mag_rated, magnet_effective_N=mag_eff, pull_needed_running_N=need_run,
                pull_needed_breakout_N=need_breakout, margin_running=(mag_eff[0] / need_run[1], mag_eff[1] / need_run[0]),
                margin_breakout=(mag_eff[0] / need_breakout[1], mag_eff[1] / need_breakout[0]))


def section_B():
    """Recoater ball screw, 12 mm x 10 mm lead (McMaster 4566N101 family), BK10/BF10 ends (fixed-supported)."""
    d_r = 9.9                       # root diameter, mm (12 mm nominal, 2.0 mm ball)
    L = 322.0                       # screw length between supports, mm (model)
    lam, eta = 15.1, 10.0           # fixed-supported
    n_c = lam * d_r / L ** 2 * 1e7
    p_buck = eta * d_r ** 4 / L ** 2 * 1e4
    v = 0.150                       # m/s fastest spread / return
    lead = 10.0
    n_max = v * 1000 / lead * 60
    dn = 12 * n_max
    Ca = 2500.0                     # N, dynamic rating of a 12 x 10 nut (THK/HIWIN class value; McMaster lists none)
    Fa = 10.0 + 5.0                 # N, spreading + friction
    fw = 1.5
    L10_rev = (Ca / (fw * Fa)) ** 3 * 1e6
    stroke_per_layer = 2 * 0.206    # m, out and back
    layers_per_rev = lead / 1000 / stroke_per_layer
    L10_layers = L10_rev * layers_per_rev
    return dict(d_root_mm=d_r, L_mm=L, critical_rpm=n_c, buckling_N=p_buck, rpm_at_150mm_s=n_max, DN=dn,
                rpm_margin=n_c * 0.8 / n_max, L10_rev=L10_rev, L10_layers=L10_layers,
                note="fatigue life is effectively unlimited at these loads; life is set by powder getting into the nut and rail")


def section_C(door):
    """Screws and closures."""
    As_M5, As_M4, As_M3 = 14.2, 8.78, 5.03
    proof_A4_70 = 450.0
    K = 0.2
    def torque(F, d):
        return K * F * d / 1000
    lid_or = 4103.0                          # N, seals.py lid O-ring at 25 %
    lid_per = lid_or / 20
    out = dict(lid_oring_per_screw_N=lid_per, lid_overpressure_per_screw_N=2000 * 0.302 * 0.212 / 20,
               lid_preload_recommended_N=2500.0, lid_torque_Nm=torque(2500, 5), lid_preload_max_N=0.75 * As_M5 * proof_A4_70,
               lid_torque_max_Nm=torque(0.75 * As_M5 * proof_A4_70, 5),
               window_ring_screws=dict(n=6, size="M3", oring_N=294.0, preload_each_N=294 / 6 * 1.5, torque_Nm=torque(294 / 6 * 1.5, 3)),
               galling="316 screws in 18-8 helical inserts gall; the lid and window screws sit outside the seal, so use anti-seize there, or silver-plated / Nitronic 60 screws")
    if door:
        pin_area = math.pi / 4 * 5.0 ** 2
        for c in door["cases"]:
            key = "door_" + c.get("case", str(c["cord"]).replace(".", "p"))
            out[key] = dict(label=c.get("label", ""), latch_each_N=c["latch_load_each_N"], latch_rating_N=800 * LBF,
                            latch_sf=800 * LBF / c["latch_load_each_N"], hinge_each_N=c["hinge_load_each_N"],
                            hinge_pin_shear_MPa=c["hinge_load_each_N"] / (2 * pin_area), squeeze_lost_um=c["lost_max_um"],
                            squeeze_pct=(c.get("squeeze_min_pct"), c.get("squeeze_max_pct")), sf_yield=c.get("sf_yield"))
        if "geometry" in door:
            out["latch_bracket"] = latch_bracket(door)
    return out


def latch_bracket(door):
    """The latch's pull reaches the door through a bracket whose foot sits on the ear's front face, while the pull line is outboard of
    the foot (door_seal_fea.json: positions read from cad/lpbf_low.py). Shigley-style checks of the bracket plate, the foot's screws
    (not drawn: 2 x M5 A4-70 into the 15 mm ear assumed) and the ear, at the design case's latch load."""
    G = door["geometry"]
    L = G["latches"][0]
    c = max(door["cases"], key=lambda k: k["latch_load_each_N"])       # the highest latch load of the door cases (the top preload)
    F = c["latch_load_each_N"]
    bb = L["bracket_bbox"]
    t = L["plate_t"]                                                   # 6 mm plate
    x_plate_mid = abs(bb[3] if L["sx"] > 0 else bb[0]) - t / 2         # plate mid-plane |x|
    x_pull = abs(L["x_pull"])
    fx0, fx1 = sorted(abs(v) for v in L["foot_x"])
    fz0, fz1 = L["foot_z"]
    h_plate = bb[5] - bb[2]                                            # plate height (z)
    e_plate = x_pull - x_plate_mid
    M_plate = F * e_plate                                              # N mm, out-of-plane bending of the plate where it meets the foot
    sig_plate = M_plate / (h_plate * t ** 2 / 6) + F / (h_plate * t)
    # foot: tips about its outer edge (fx1); the screws at the foot's middle hold the inner part down
    x_s = (fx0 + fx1) / 2
    T = F * (x_pull - fx1) / (fx1 - x_s)                               # screw tension (both screws), N
    C_edge = F + T                                                     # compression at the outer edge, N
    As, proof, K = 14.2, 450.0, 0.2
    Fi = 0.75 * As * proof * 0.75                                      # preload, 75 % of proof less 25 % for torque scatter (Shigley 8-31)
    kb_frac = 0.25                                                     # joint constant C = kb / (kb + km), aluminium members (Shigley Table 8-8 range)
    n_sep = Fi / ((1 - kb_frac) * T / 2)                               # separation factor per screw (Shigley 8-29)
    n_load = (0.9 * As * proof - Fi) / (kb_frac * T / 2)               # load factor per screw
    # ear: cantilever from the door's edge (x 124) to the pull line
    x_root = 124.0
    M_ear = F * (x_pull - x_root)
    t_door = 15.0
    sig_ear = M_ear / ((fz1 - fz0) * t_door ** 2 / 6)
    sy = 276.0
    return dict(latch_load_N=F, pull_line_x=x_pull, plate_mid_x=x_plate_mid, plate_t=t, plate_h=h_plate, e_plate_mm=e_plate,
                plate_sigma_MPa=sig_plate, plate_sf=sy / sig_plate, foot_x=(fx0, fx1), screw_x=x_s, screw_tension_N=T, edge_compression_N=C_edge,
                screw_preload_N=Fi, screw_torque_Nm=K * Fi * 5 / 1000, screw_sep_factor=n_sep, screw_load_factor=n_load,
                ear_moment_Nmm=M_ear, ear_sigma_MPa=sig_ear, ear_sf=sy / sig_ear,
                note="brackets' screws not drawn: 2 x M5 A4-70 into the ear assumed (6061, >= 8 mm engagement or a helical insert)")


def h_nat_vertical(dT, L, T_amb=296.0):
    """Churchill-Chu, laminar+turbulent, air."""
    Tf = T_amb + dT / 2
    nu, k, Pr = 1.6e-5 * (Tf / 300) ** 1.7, 0.0263 * (Tf / 300) ** 0.8, 0.707
    Ra = 9.81 / Tf * dT * L ** 3 / nu ** 2 * Pr
    Nu = (0.825 + 0.387 * Ra ** (1 / 6) / (1 + (0.492 / Pr) ** (9 / 16)) ** (8 / 27)) ** 2
    return Nu * k / L


def h_nat_top(dT, L, T_amb=296.0):
    Tf = T_amb + dT / 2
    nu, k, Pr = 1.6e-5 * (Tf / 300) ** 1.7, 0.0263 * (Tf / 300) ** 0.8, 0.707
    Ra = 9.81 / Tf * dT * L ** 3 / nu ** 2 * Pr
    return (0.54 * Ra ** 0.25 if Ra < 1e7 else 0.15 * Ra ** (1 / 3)) * k / L


def section_D():
    """Chamber warm-up: lumped network, 10-hour build. Geometry from lpbf_low.P (outer 312 x 222 x 156 incl. lid)."""
    Lx, Ly, Lz = 0.312, 0.222, 0.156
    A_side = 2 * (Lx + Ly) * Lz
    A_top = Lx * Ly
    m_al = 2700 * (0.312 * 0.222 * 0.156 - 0.280 * 0.190 * 0.120) + 0.9      # body + lid shell + door, kg
    C = m_al * 900.0
    # heat in: heater loss into the chamber (modules.md: 42-92 W at the build start), laser average power x (1 - fraction
    # leaving with the loop gas); the bed absorbs ~60 % and conducts it into the module and floor; the reflected ~40 % lands
    # on walls and lid. Average laser power: 350 W x 30 % duty (recoat-dominated small plates).
    P_laser_avg = 350 * 0.30
    cases = {}
    for name, eps, P_heat, cooled in (("bare outside, M50 heater 72 W", 0.07, 72.0, False),
                                      ("black-anodized outside", 0.80, 72.0, False),
                                      ("bare, L75 (92 W)", 0.07, 92.0, False),
                                      ("bare + water-cooled floor plate (UA 15 W/K)", 0.07, 72.0, True)):
        Q = P_heat + P_laser_avg
        T = 296.0
        dt = 10.0
        hist = []
        loop_UA = 100 / 60 / 1000 * 1.66 * 520     # 100 L/min argon cooled back to ambient in the loop, W/K
        for k in range(int(10 * 3600 / dt)):
            dT = T - 296.0
            h_v = h_nat_vertical(max(dT, 0.1), Lz)
            h_t = h_nat_top(max(dT, 0.1), (Lx * Ly) / (2 * (Lx + Ly)))
            h_r = 4 * eps * SIGMA * ((T + 296) / 2) ** 3
            UA = A_side * (h_v + h_r) + A_top * (h_t + h_r) + loop_UA + 0.5 + (15.0 if cooled else 0.0)   # 0.5 W/K through the legs
            T += dt * (Q - UA * dT) / C
            if k % int(600 / dt) == 0:
                hist.append(round(T - 273.15, 1))
        cases[name] = dict(Q_W=Q, UA_end_W_K=UA, T_end_C=T - 273.15, T_10min_steps=hist, tau_min=C / UA / 60)
    return dict(mass_al_kg=m_al, P_laser_avg_W=P_laser_avg, cases=cases,
                consequences="pot magnet (79 C rating) under the floor, camera and Pi HQ electronics (~50 C), load cell, inductive sensors (70 C), "
                             "recoater servo, the module's spigot O-ring (84 C at a 60 C chamber), optics drift")


def section_E():
    """Cover-slide thermal lens."""
    k, dndT = 1.38, 9.6e-6
    f = 0.160
    D_beam = 3.2e-3
    z_slide, z_lens = 0.145, 0.1825
    w = D_beam / 2 * (z_slide / z_lens)          # beam radius on the slide (converging cone), m
    zR = 3.7e-3
    rows = []
    for P in (200.0, 350.0, 500.0):
        for a in (5e-5, 5e-4, 5e-3):
            Pabs = a * P
            Dth = Pabs * dndT / (2 * math.pi * k * w ** 2)
            dz = f ** 2 * Dth                       # thin added lens next to the focusing lens: dz ~ f^2 D
            rows.append(dict(P_W=P, absorption=a, P_abs_W=Pabs, D_per_m=Dth, focus_shift_mm=1000 * dz, x_Rayleigh=dz / zR))
    # slide material: optical-path thermo-optic coefficient dS/dT = dn/dT + (n - 1)(1 + nu) alpha, lens power ~ dS/dT / k
    mats = {"fused silica (Corning 7980)": dict(k=1.38, dndT=9.6e-6, n=1.45, nu=0.16, a=0.52e-6),
            "sapphire (c-plane)": dict(k=27.0, dndT=13.1e-6, n=1.755, nu=0.27, a=5.3e-6),
            "N-FK51A (Schott)": dict(k=0.91, dndT=-6.6e-6, n=1.48, nu=0.29, a=12.7e-6),
            "CaF2": dict(k=9.71, dndT=-10.6e-6, n=1.43, nu=0.26, a=18.85e-6)}
    mrows = []
    for name, m in mats.items():
        dS = m["dndT"] + (m["n"] - 1) * (1 + m["nu"]) * m["a"]
        Dth = 0.005 * 400 * abs(dS) / (2 * math.pi * m["k"] * w ** 2)
        mrows.append(dict(material=name, dSdT=dS, k=m["k"], shift_mm_400W_0p5pct=1000 * f ** 2 * Dth))
    return dict(w_on_slide_mm=1000 * w, rows=rows, materials=mrows,
                check="literature: -22 to -30 mm at 400 W with ~0.5 % absorption on fused silica; N-FK51A ~-1.3 mm in the same model [6]")


def section_F(D):
    dT = D["cases"]["bare outside, M50 heater 72 W"]["T_end_C"] - 23.0
    posts = 60e-3 * 23.6e-6 * dT
    galvo_offset = 30e-6 * dT * 0.160
    return dict(chamber_rise_K=dT, bridge_post_growth_um=1e6 * posts, galvo_offset_drift_um=1e6 * galvo_offset,
                note="focus moves by the post growth (≪ the ±3.7 mm Rayleigh range); the galvo's offset drift is comparable to a hatch spacing "
                     "over a warm-up, so calibrate warm or re-register on fiducials each few hours")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dj = ROOT / "analysis" / "out" / "seals" / "door_seal_fea.json"
    door = json.loads(dj.read_text()) if dj.exists() else None
    R = dict(A=section_A(), B=section_B(), C=section_C(door), D=section_D(), E=section_E(), sources=SOURCES)
    R["F"] = section_F(R["D"])
    (OUT / "mech.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    A, B, C, D, E, Fd = R["A"], R["B"], R["C"], R["D"], R["E"], R["F"]
    f = lambda t: "–".join(f"{x:.0f}" for x in t)
    L = ["# Machine-element and heat-transfer checks (from `analysis/mech/mech_checks.py`)", "",
         "## A. Z coupling: can the pot magnet pull the piston down?", "",
         "| Force on the piston and rod (M50) | N |", "|---|---|",
         f"| 2 × 2-114 rod O-rings, running (Parker Fig. 5-9, 75A, 17–26 % squeeze, oil basis) | {f(A['rod_oring_running_N'])} |",
         f"| same, dry or PFPE-greased in argon (×{A['dry_factor']}) and after a dwell (break-out up to ×{A['breakout_factor']}) | up to {A['rod_oring_running_N'][2] * A['dry_factor'] * A['breakout_factor']:.0f} |",
         f"| bore seal (felt + PTFE scraper, 0.05–0.4 N/mm, assumed) | {f(A['bore_seal_N'])} |",
         f"| plate rim wiper (0.03–0.1 N/mm, assumed) | {f(A['wiper_N'])} |",
         f"| atmosphere on the rod at full vacuum (pushes it up) | {A['rod_force_at_vacuum_up_N']:.0f} |",
         f"| piston + stack + 40 mm of powder (helps) | −{A['weight_N']:.0f} |",
         f"| **pull needed to lower a layer, running** | **{f(A['pull_needed_running_N'])}** |",
         f"| **pull needed after a dwell (break-out)** | **{f(A['pull_needed_breakout_N'])}** |",
         f"| pot magnet 5679K95, rated on thick mild steel | {A['magnet_rated_N']:.0f} |",
         f"| same on a 430 SS striker at 68 °C with 0–0.05 mm of debris | **{f(A['magnet_effective_N'])}** |",
         "", f"Margin (magnet / need): running {A['margin_running'][0]:.2f}–{A['margin_running'][1]:.2f}; after a dwell {A['margin_breakout'][0]:.2f}–{A['margin_breakout'][1]:.2f}. "
         "Below 1 the plate stays put while the arm drops, the magnet lets go, and the next layer is spread onto an unlowered plate.", "",
         "## B. Recoater ball screw (12 × 10, fixed-supported, THK formulas)", "",
         f"Critical speed {B['critical_rpm']:.0f} rpm vs {B['rpm_at_150mm_s']:.0f} rpm at 150 mm/s (margin {B['rpm_margin']:.0f}× at 80 %); "
         f"buckling {B['buckling_N'] / 1000:.1f} kN vs ~15 N; DN {B['DN']:.0f} (limit 70,000); L10 {B['L10_rev']:.1e} rev ≈ {B['L10_layers']:.1e} layers. {B['note']}.", "",
         "## C. Screws, latches, hinges", "",
         f"Lid: the O-ring needs {C['lid_oring_per_screw_N']:.0f} N per screw and +20 mbar adds {C['lid_overpressure_per_screw_N']:.0f} N. Recommend {C['lid_preload_recommended_N']:.0f} N preload "
         f"({C['lid_torque_Nm']:.1f} N·m, K = 0.2); A4-70's 75 % of proof is {C['lid_preload_max_N']:.0f} N ({C['lid_torque_max_Nm']:.1f} N·m). "
         f"Window ring: 6 × M3 at {C['window_ring_screws']['torque_Nm']:.2f} N·m to a metal stop. {C['galling']}.", ""]
    L += ["Door latches and hinges, from the CalculiX door model (`door_seal_fea.md`; 1.78 mm cord at 25 %, +20 mbar):", ""]
    for k in sorted(x for x in C if x.startswith("door_")):
        d = C[k]
        sq = d.get("squeeze_pct") or (None, None)
        sqt = f"squeeze {sq[0]:.1f}–{sq[1]:.1f} % along the gland, " if sq[0] is not None else ""
        L.append(f"- case {k.replace('door_', '')} ({d['label']}): each latch {d['latch_each_N']:.0f} N (rating {d['latch_rating_N']:.0f} N, SF {d['latch_sf']:.1f}); "
                 f"each hinge {d['hinge_each_N']:.0f} N, Ø5 pin in double shear {d['hinge_pin_shear_MPa']:.1f} MPa; {sqt}squeeze lost up to {d['squeeze_lost_um']:.0f} µm"
                 + (f"; door, ears and brackets SF {d['sf_yield']:.1f} on yield" if d.get("sf_yield") else ""))
    if "latch_bracket" in C:
        b = C["latch_bracket"]
        L += ["", f"Latch brackets at {b['latch_load_N']:.0f} N per latch, the highest latch load of the door cases (the pull line at x ±{b['pull_line_x']:.0f} is "
              f"{b['e_plate_mm']:.0f} mm outboard of the 6 mm plate's mid-plane and {b['pull_line_x'] - b['foot_x'][1]:.0f} mm outboard of the foot):", "",
              f"- plate ({b['plate_t']:.0f} × {b['plate_h']:.0f} mm section), out-of-plane bending plus tension: {b['plate_sigma_MPa']:.1f} MPa, SF {b['plate_sf']:.1f} on 6061-T6 yield;",
              f"- foot: it tips about its outer edge, so the screws (at x ±{b['screw_x']:.0f}) carry {b['screw_tension_N']:.0f} N together and the edge "
              f"{b['edge_compression_N']:.0f} N. With 2 × M5 A4-70 (assumed; {b['note'].split(': ')[1]}) at {b['screw_preload_N']:.0f} N preload "
              f"({b['screw_torque_Nm']:.1f} N·m, K = 0.2): separation factor {b['screw_sep_factor']:.1f}, load factor {b['screw_load_factor']:.0f} (Shigley 8-28, 8-29, C = 0.25);",
              f"- ear as a cantilever from the door's edge to the pull line: {b['ear_moment_Nmm'] / 1000:.1f} N·m, {b['ear_sigma_MPa']:.1f} MPa, SF {b['ear_sf']:.0f}."]
    L += ["", "## D. Chamber warm-up over a 10 h build (lumped; natural convection + radiation + argon loop)", "",
          f"Aluminium shell {D['mass_al_kg']:.1f} kg; laser average {D['P_laser_avg_W']:.0f} W (350 W × 30 % duty), all of it ending as heat in the chamber or module.", "",
          "| Case | Heat in (W) | UA at the end (W/K) | Time constant (min) | Chamber after 10 h (°C) |", "|---|---|---|---|---|"]
    for n, c in D["cases"].items():
        L.append(f"| {n} | {c['Q_W']:.0f} | {c['UA_end_W_K']:.1f} | {c['tau_min']:.0f} | **{c['T_end_C']:.0f}** |")
    L += ["", f"Affected: {D['consequences']}.", "",
          f"## E. Cover-slide thermal lens (beam radius on the slide {E['w_on_slide_mm']:.2f} mm)", "",
          "| Laser (W) | Absorption | Absorbed (W) | Focus shift (mm) | × Rayleigh range |", "|---|---|---|---|---|"]
    for r in E["rows"]:
        L.append(f"| {r['P_W']:.0f} | {100 * r['absorption']:.3f} % | {r['P_abs_W']:.3f} | {r['focus_shift_mm']:.1f} | {r['x_Rayleigh']:.1f} |")
    L += ["", "Slide material at 400 W and 0.5 % absorption (Corning, Crystran and Schott data; dS/dT = dn/dT + (n − 1)(1 + ν)α):", "",
          "| Material | dS/dT (1/K) | k (W/m·K) | Focus shift (mm) |", "|---|---|---|---|"]
    for r in E["materials"]:
        L.append(f"| {r['material']} | {r['dSdT']:.2e} | {r['k']:.2f} | {r['shift_mm_400W_0p5pct']:.1f} |")
    L += ["", f"Check: {E['check']}.", "",
          "## F. Thermal drift of the optics over the warm-up", "",
          f"Chamber +{Fd['chamber_rise_K']:.0f} K: bridge posts grow {Fd['bridge_post_growth_um']:.0f} µm; galvo offset drift ~{Fd['galvo_offset_drift_um']:.0f} µm at the plate. {Fd['note']}.", "",
          "## Sources", ""]
    for k, v in SOURCES.items():
        L.append(f"{k}. {v}")
    (OUT / "mech.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
