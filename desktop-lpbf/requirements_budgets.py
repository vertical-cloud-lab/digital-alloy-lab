"""Order-of-magnitude sizing for the requirements in requirements-later.md (issue #260, PR #266).

Run: python desktop-lpbf/requirements_budgets.py
Covers the heated plate, swappable plate and hopper sizes, and the lid/window geometry a later
multi-laser upgrade needs. Every input is a named assumption; change them and re-run. These are
lumped estimates to size parts and reserve space, not a thermal or optical design.
"""
import math

SIGMA = 5.670e-8                     # W/m^2/K^4
T_AMB = 25.0                         # C, chamber walls and gas

# --- Heated plate: plate + heater block on ceramic standoffs, inside the build cylinder ----------
rho_al, c_al = 2700.0, 900.0         # 6061 plate and heater block
plate_t, block_t = 0.010, 0.015      # m
eps_bed = 0.5                        # powder-covered plate (bare Al is ~0.1)
k_ar, mu_ar, rho_ar, pr_ar = 0.018, 2.3e-5, 1.6, 0.67   # argon near room temperature
v_flow = 2.0                         # m/s cross-flow over the plate
k_macor, n_post, d_post, l_post = 1.46, 3, 0.008, 0.015  # Macor standoffs under the heater block
rho_ss, c_ss, k_ss = 8000.0, 500.0, 16.0   # 316 build cylinder
CYL = {"lpbf_low.py: 2 in. honed tube, Ø50.8 bore, 60.3 OD": (0.0603, 0.00475, 0.0508),
       "lpbf_model.py: Ø53.8 bore, 57.15 OD": (0.05715, 0.001675, 0.0538)}
hot_len = 0.060                       # m of cylinder wall between the plate and the floor flange
ramp_s = 15 * 60                      # heat-up time to design for
open_below = 50.0                     # C, door interlock: no air on hot Al powder


def plate_budget(d, t_set, cyl=next(iter(CYL.values()))):
    cyl_od, cyl_wall, bore = cyl
    a = math.pi * d * d / 4
    m = rho_al * a * (plate_t + block_t)
    dt = t_set - T_AMB
    re = rho_ar * v_flow * d / mu_ar
    h = 0.664 * re ** 0.5 * pr_ar ** (1 / 3) * k_ar / d           # laminar flat plate
    tk, ta = t_set + 273.15, T_AMB + 273.15
    q_rad = eps_bed * SIGMA * a * (tk ** 4 - ta ** 4)
    q_conv = h * a * dt
    q_post = k_macor * n_post * math.pi * d_post ** 2 / 4 / l_post * dt
    cyl_a = math.pi / 4 * (cyl_od ** 2 - (cyl_od - 2 * cyl_wall) ** 2) * (d / bore)  # wall scales with bore
    q_cyl = k_ss * cyl_a / hot_len * dt                            # wall runs hot near the plate
    q_loss = q_rad + q_conv + q_post + q_cyl
    e_heat = m * c_al * dt
    p_heater = e_heat / ramp_s + q_loss
    # passive cool-down: plate + block + nearby cylinder wall, linearised conductances
    c_tot = m * c_al + rho_ss * cyl_a * hot_len * c_ss
    g = q_loss / dt
    t_cool = c_tot / g * math.log(dt / (open_below - T_AMB))
    return m, q_rad, q_conv, q_post, q_cyl, q_loss, p_heater, t_cool


print(f"Heated plate (Al plate 10 mm + Al heater block 15 mm, 3 Macor posts, argon at 2 m/s; cylinder of {next(iter(CYL))})")
print(f"{'plate':>6} {'T set':>6} {'mass':>6} {'rad':>5} {'conv':>5} {'posts':>5} {'cyl':>5} {'loss':>5} {'heater':>7} {'cool to 50 C':>12}")
for d_mm in (25, 50, 75):
    for t_set in (200, 500):
        m, qr, qc, qp, qy, ql, ph, tc = plate_budget(d_mm / 1000, t_set)
        print(f"{'Ø%d' % d_mm:>6} {t_set:>4} C {m * 1000:>4.0f} g {qr:>4.0f}W {qc:>4.0f}W {qp:>4.0f}W {qy:>4.0f}W "
              f"{ql:>4.0f}W {ph:>5.0f} W {tc / 60:>9.0f} min")
name, cyl = list(CYL.items())[1]
for t_set in (200, 500):
    *_, ql, ph, tc = plate_budget(0.05, t_set, cyl)
    print(f"  with the {name} cylinder, Ø50 at {t_set} C: loss {ql:.0f} W, heater {ph:.0f} W, cool-down {tc / 60:.0f} min")
for t_set in (200, 500):
    grow = 23e-6 * (t_set - T_AMB) * 53.0
    print(f"Ø53 Al plate grows {grow:.2f} mm in diameter at {t_set} C (model: Ø53.8 bore, 0.4 mm radial clearance cold)")

# --- Swappable plate sizes: what each size needs from the powder, recoat and gas systems ------------
layer_um, build_h, dose_factor = 30.0, 15.0, 1.8
rho_solid, pack_bed, pack_hop = 2.68, 0.50, 0.55          # AlSi10Mg, as in budgets.py
nozzle_h, v_noz, margin = 8.0, 2.0, 20.0                  # mm, m/s, mm each side
field_mm = 156.7                                          # Thorlabs FTH254-1064 scan field
print("\nSwappable plate sizes (30 um layers, 1.8 dose factor, AlSi10Mg)")
print(f"{'plate':>6} {'g/layer':>8} {'15 mm build':>11} {'full 40 mm':>10} {'hopper 15/40 mm':>16} {'blade':>6} {'nozzle':>7} {'flow':>8}")
for d_mm in (25, 50, 75, 100):
    a_cm2 = math.pi * (d_mm / 20) ** 2
    g_layer = a_cm2 * layer_um * 1e-4 * rho_solid * pack_bed * dose_factor
    g15 = g_layer * build_h * 1000 / layer_um
    g40 = g15 * 40 / build_h
    hop15, hop40 = (g / (rho_solid * pack_hop) for g in (g15, g40))
    blade = d_mm + 2 * margin
    lpm = blade * nozzle_h * 1e-6 * v_noz * 60_000
    fits = "in field" if d_mm * math.sqrt(2) <= field_mm or d_mm <= field_mm else "OUT of field"
    print(f"{'Ø%d' % d_mm:>6} {g_layer:>6.2f} g {g15:>8.0f} g {g40:>8.0f} g {hop15:>7.0f}/{hop40:<4.0f} cm3 "
          f"{blade:>4.0f}mm {blade:>4.0f}mm {lpm:>4.0f} L/min  ({fits})")

# --- Hoppers: can one load cell weigh a single dose across cartridge sizes? -------------------------
cell_fs_g, cell_err = 5000.0, 2e-4                         # 5 kg cell, 0.02 % of full scale combined error
print(f"\nLoad cell under the cartridge: 5 kg cell, ±{cell_fs_g * cell_err:.1f} g combined error")
for d_mm in (25, 50, 75):
    g_layer = math.pi * (d_mm / 20) ** 2 * layer_um * 1e-4 * rho_solid * pack_bed * dose_factor
    print(f"  Ø{d_mm}: one dose is {g_layer:.2f} g, so a dose is resolved only over ~{cell_fs_g * cell_err / g_layer * 3:.0f} layers (3 sigma)")

# --- Multi-laser later: heads side by side over a small plate --------------------------------------
# Two optics options are on this PR: the tall model (cad/lpbf_model.py, FTH254-1064) and the low-profile
# layout (cad/lpbf_low.py, FTH160-1064). Window height = lid top + window seat, read off each model.
LENSES = {
    "FTH254 (lpbf_model.py)": dict(f=254.0, wd=301.2, field=156.7, housing=120.0, z_win=189.0),
    "FTH160 (lpbf_low.py)": dict(f=160.0, wd=182.5, field=110.6, housing=90.0, z_win=148.0),
}
beam_d, r_plate = 5.0, 25.0                                  # collimated beam at the lens; Ø50 plate


def head_footprint(d, wd, z_win):
    """Window footprint (x range, mm) of a head at x = d covering the whole Ø50 plate.
    Rays are drawn from a point on the lens axis at the working distance, which overstates the
    footprint of a real f-theta lens (its chief rays lean further in), so this errs large."""
    s = z_win / wd
    xs = [x + (d - x) * s for x in (-r_plate, r_plate)]
    half_beam = beam_d / 2 * s
    return min(xs) - half_beam, max(xs) + half_beam


def window_t_mm(d_clear_mm, sf=4.0, mr_psi=7600.0, p_psi=14.7):
    """Unclamped circular window under 1 atm (Edmund/Thorlabs vacuum-window formula), fused silica."""
    r_in = d_clear_mm / 2 / 25.4
    return math.sqrt(1.1 * p_psi * r_in ** 2 * sf / mr_psi) * 25.4


for name, L in LENSES.items():
    reach = L["field"] / 2 - r_plate
    print(f"\nMulti-laser, {name}: f {L['f']:.0f} mm, WD {L['wd']} mm, field {L['field']} mm, window {L['z_win']:.0f} mm above the powder, Ø50 plate")
    print(f"{'head offset':>11} {'worst incidence':>15} {'spot stretch':>12} {'window footprint x':>20} {'whole plate':>11}")
    for d in (0, 30, 45, 60):
        worst = math.degrees((abs(d) + r_plate) / L["f"])      # f-theta: chief-ray angle = field radius / f
        x0, x1 = head_footprint(d, L["wd"], L["z_win"])
        print(f"{d:>8} mm {worst:>12.1f} deg {1 / math.cos(math.radians(worst)):>11.3f}x {x0:>8.0f} to {x1:>4.0f} mm "
              f"{'yes' if abs(d) <= reach else 'no':>11}")
    pitch = L["housing"]
    shared = max(0.0, 2 * (L["field"] / 2 - pitch / 2))
    x0, x1 = head_footprint(pitch / 2, L["wd"], L["z_win"])
    print(f"A head reaches the whole plate only within ±{reach:.0f} mm of centre. Two housings (Ø{pitch:.0f}) side by side "
          f"at ±{pitch / 2:.0f} mm share a {shared:.0f} mm band ({shared / 50:.0%} of the plate width) and need one "
          f"Ø{2 * x1 + 6:.0f} mm window, or two Ø{x1 - x0 + 6:.0f} mm windows on {x0 + x1:.0f} mm centres")
print()
for dc in (25, 48, 75, 100):
    print(f"Fused-silica window, Ø{dc} mm clear, 1 atm, SF 4: ≥ {window_t_mm(dc):.1f} mm thick")
