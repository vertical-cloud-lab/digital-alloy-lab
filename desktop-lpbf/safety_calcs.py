#!/usr/bin/env python
"""Safety arithmetic for the desktop LPBF machine (PR #266, issue #260).

Run:  /tmp/venv/bin/python desktop-lpbf/safety_calcs.py   (prints every number quoted in safety.md)

Every input is tagged  [src]  (a published number, source in notes/2026-11-20-safety-sources.md),
[repo] (taken from this folder's own design files) or [assume] (our estimate; change it and re-run).
Nothing here replaces the LSO's hazard analysis, a dust hazard analysis or a tested guard.
"""
from __future__ import annotations

import math

PI = math.pi


def hdr(t: str) -> None:
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


# ----------------------------------------------------------------------------------------------
# 1. LASER
# ----------------------------------------------------------------------------------------------
hdr("1. LASER: MPE, Class 1 limit, NHZ, eyewear OD, window OD")
lam = 1070e-9           # m   [repo] IPG YLR-500-U3-SM-AC
P = 500.0               # W   [repo] nominal CW output
M2 = 1.1                # [repo] IPG max M^2
D_col = 5e-3            # m   [repo] standard IPG collimator, 5 mm beam
f_ft = 0.160            # m   [repo] f-theta lens (low-profile.md)
bare_div = 0.140        # rad full angle, 86 %, bare QBH output [repo quotes/ipg-ylr-500-u3-sm-ac.md]

# MPE at 1070 nm (ANSI Z136.1, as tabulated in the NIU manual, which cites Z136.1-2000):
CA = 5.0   # 1.050-1.400 um [src NIU]
CC = 1.0   # 1.050-1.150 um [src NIU]
mpe_eye_10s = 5.0e-3 * CC                         # W/cm^2, t >= 10 s [src NIU "Case 1"]
mpe_eye_t = lambda t: 9.0 * CC * t ** 0.75 * 1e-3 / t   # W/cm^2 for 18 us..10 s: 9.0 CC t^0.75 mJ/cm^2 [src NIU case 4]
mpe_skin = 0.2 * CA                                # W/cm^2, t >= 10 s [src NIU "Case 2"]
print(f"MPE eye, t >= 10 s            : {mpe_eye_10s*1e3:.2f} mW/cm^2")
print(f"MPE eye, 0.25 s blink (check)  : {mpe_eye_t(0.25)*1e3:.1f} mW/cm^2  (the 10 s value is the one used; IR is not blink-protected)")
print(f"MPE skin, t >= 10 s           : {mpe_skin:.2f} W/cm^2  -> 500 W over 1 cm^2 is {P/mpe_skin:.0f}x the skin MPE")

# Class 1 accessible-emission level ~ MPE x 7 mm pupil (derived; IEC 60825-1 gives the same order, 1.9 mW)
A7 = PI * (0.35) ** 2   # cm^2
AEL1 = mpe_eye_10s * A7
print(f"Class 1 AEL (MPE x 7 mm pupil): {AEL1*1e3:.2f} mW   [derived]")

# Beam geometry
w_in = D_col / 2
w0 = M2 * lam * f_ft / (PI * w_in)
zR = PI * w0 ** 2 / (M2 * lam)
theta_half = w_in / f_ft   # converging / diverging half angle through the f-theta, rad
print(f"Focused spot radius w0         : {w0*1e6:.1f} um (diameter {2*w0*1e6:.0f} um)   Rayleigh range {zR*1e3:.2f} mm")
print(f"Peak irradiance at focus       : {2*P/(PI*w0**2)/1e4:.2e} W/cm^2")
print(f"Beam half-angle through f-theta: {theta_half*1e3:.1f} mrad (full {2*theta_half*1e3:.1f} mrad)")

def nohd(power, phi_full, a=0.0, mpe=mpe_eye_10s):
    """Z136.1-style NOHD: r = (1/phi) * (sqrt(4 P /(pi MPE)) - a); P in W, MPE W/cm^2 -> r in cm."""
    return (math.sqrt(4 * power / (PI * mpe)) - a) / phi_full / 100.0   # m

phi_col = 4 * M2 * lam / (PI * D_col)
print("\nNominal ocular hazard distance (NOHD), 500 W:")
print(f"  collimated 5 mm beam (head off, or between collimator and galvo): phi = {phi_col*1e3:.2f} mrad -> NOHD = {nohd(P, phi_col, a=0.5)/1e3:.1f} km")
print(f"  through the f-theta, from the focus on the plate (direct)       : phi = {2*theta_half*1e3:.1f} mrad -> NOHD = {nohd(P, 2*theta_half):.2f} m")
rho_spec = 0.9
print(f"  specular off bare Al plate, reflectance {rho_spec:.2f} (assume)    : NOHD = {nohd(rho_spec*P, 2*theta_half):.2f} m from the focus")
print(f"  bare QBH fibre end, fibre unplugged (140 mrad full angle)       : NOHD = {nohd(P, bare_div):.2f} m")
for rho_d in (0.1, 0.5):
    r = math.sqrt(rho_d * P / (PI * mpe_eye_10s)) / 100.0
    print(f"  diffuse (Lambertian) reflectance {rho_d:.1f}, normal viewing           : NHZ radius = {r:.2f} m")
print("  (A scanned beam is not credited: Z136.1 treats a stalled galvo as the stationary beam.)")

# Eyewear and window optical density
def od(power_w, aperture_cm2=A7, mpe=mpe_eye_10s):
    return math.log10(power_w / aperture_cm2 / mpe)

print("\nOptical density needed (OD = log10(H0/MPE), power through a 7 mm pupil):")
for label, pw in (("direct 500 W", 500.0), ("specular 0.9 x 500 W", 450.0), ("alignment at 50 W (assumed minimum stable output)", 50.0),
                  ("alignment at 5 W (attenuated / pilot-only test)", 5.0)):
    print(f"  {label:<52s}: OD >= {od(pw):.2f}  (round up to {math.ceil(od(pw))}; add margin)")
d_ref = 0.30
for rho_d in (0.5,):
    E = rho_d * P / (PI * d_ref ** 2) / 1e4
    print(f"  diffuse reflection at {d_ref*100:.0f} cm, rho {rho_d}: {E:.3f} W/cm^2 -> OD >= {math.log10(E/mpe_eye_10s):.2f}")
print(f"  OD 7 filter on a full 500 W beam transmits {P*1e-7*1e6:.0f} uW = {P*1e-7/AEL1:.3f} x Class 1 AEL "
      f"(margin {AEL1/(P*1e-7):.0f}x). That only holds while the filter survives, see below.")
print(f"  Guard window (stray beam, full 500 W): OD >= {math.log10(P/AEL1):.2f} to stay at Class 1 behind it.")
irr_eyewear = P / A7
print(f"  Power density a 500 W direct beam puts on eyewear (7 mm pupil footprint): {irr_eyewear:.0f} W/cm^2 = {irr_eyewear*1e4/1e3:.0f} kW/m^2.")
print("  Eyewear is tested for a few seconds at its rated power density (EN 207) -> never align at full power with eyewear as the control.")

# ----------------------------------------------------------------------------------------------
# 2. PASSIVE GUARD SURVIVAL (IEC 60825-4 style screening)
# ----------------------------------------------------------------------------------------------
hdr("2. GUARD SURVIVAL under a stationary 500 W beam (screening; the real figure is a test, IEC 60825-4 Annex)")
print("Test times in the IEC 60825-4 committee report quoted by Edison: T1 = 30,000 s, T2 = 100 s, T3 = 10 s ->",
      ", ".join(f"{t:,} s x 500 W = {t*P/1e3:,.0f} kJ" for t in (30000, 100, 10)))

mats = {
    # name: (rho kg/m3, c J/kgK, Tmelt C, L J/kg, k W/mK, absorptance_cold, absorptance_molten, thickness m)
    "Al 5052 1.6 mm (BOM S9 guard)": (2680, 900, 607, 389e3, 138, 0.08, 0.40, 1.6e-3),
    "Al 5052 3.0 mm":                (2680, 900, 607, 389e3, 138, 0.08, 0.40, 3.0e-3),
    "Steel 304 1.5 mm":              (8000, 500, 1400, 270e3, 16, 0.35, 0.60, 1.5e-3),
    "Steel mild 2.0 mm (galv.)":     (7850, 490, 1500, 270e3, 50, 0.35, 0.60, 2.0e-3),
}
T0 = 20.0
R_sheet = 0.25  # m, assumed distance to a heat sink / panel edge for the thin-sheet steady state
print(f"{'case':<32s}{'z from focus':>13s}{'w (mm)':>8s}{'E (W/cm2)':>11s}{'t_1D_min (s)':>14s}{'dT cold a':>11s}{'dT hot a':>10s}  verdict")
cap = lambda x: f">{x:.0f}" if x > 9999 else f"{x:.0f}"
for name, (rho, c, Tm, L, k, a_cold, a_hot, d) in mats.items():
    e_vol = rho * (c * (Tm - T0) + L)                 # J/m3 to bring to melt and melt
    for z in (0.0, 0.05, 0.15, 0.30, 0.50):
        w = math.sqrt(w0 ** 2 + (theta_half * z) ** 2) if z > 0 else w0
        E = 2 * P / (PI * w ** 2)                      # W/m2 peak
        # lower bound on burn-through time: no lateral conduction, all of the thickness molten, hot (molten) absorptance
        t1d = e_vol * d / (a_hot * E)
        # thin-sheet steady-state centre rise (log solution, heat sunk at R_sheet, no convection credit), at cold and hot absorptance
        a_eff = max(w, d)
        f = (math.log(R_sheet / a_eff) + 0.5) / (2 * PI * k * d)
        dT_c, dT_h = a_cold * P * f, a_hot * P * f
        verdict = "melts even at cold absorptance" if T0 + dT_c > Tm else ("melts once absorptance rises" if T0 + dT_h > Tm else "does not melt (steady state)")
        print(f"{name:<32s}{z*1e3:>10.0f} mm{w*1e3:>8.3f}{E/1e4:>11.3g}{t1d:>14.3g}{cap(dT_c):>11s}{cap(dT_h):>10s}  {verdict}")
print("Reading: at and near the focus every sheet is breached in well under a second (t_1D is a LOWER bound, no conduction). Defocused to w >= 5 mm\n"
      "the 1.6 mm Al sheet takes seconds by the 1-D bound, and the thin-sheet steady state says it melts only if its absorptance rises from the cold\n"
      "0.08 toward 0.4 (oxide, soot, spatter, discolouration). Mild/galvanised steel and 304 melt even at their cold absorptance. A test, not this table, decides.")
print("The repo's polycarbonate viewing panel (Uvex P1P10) is rated 102 kW/m^2 for 100 s (T2) [repo low-profile.md]:")
for z in (0.05, 0.15, 0.30, 0.50):
    w = math.sqrt(w0 ** 2 + (theta_half * z) ** 2)
    for frac, lab in ((1.0, "direct"), (0.1, "10 % specular")):
        E = frac * 2 * P / (PI * w ** 2) / 1e3     # kW/m2
        print(f"   z = {z*1e3:3.0f} mm from focus, {lab:<13s}: {E:10.0f} kW/m^2  = {E/102:8.1f} x the PC rating")

# Interlock response energy
for t_ms, lab in ((1, "laser inhibit (12 us gate, 1 ms with wiring)"), (20, "safety relay + shutter, 20 ms"), (100, "slow path, 100 ms")):
    print(f"Energy delivered to a stationary spot before the beam stops: {lab:<46s} {P*t_ms/1e3:6.1f} J  (T3 budget 5,000 J)")

# ----------------------------------------------------------------------------------------------
# 3. ARGON
# ----------------------------------------------------------------------------------------------
hdr("3. ARGON: inventory, release into the room and the Kardex bay, O2 after release")
V_chamber = 0.280 * 0.190 * 0.120 * 1e3     # L [repo] inside 280 x 190 x 120 mm
V_loop = 10.0                                # L [repo low-profile.md: "closed 10 L loop"], includes cyclone, HEPA housing, hoses
V_modules = 2.0                              # L [assume] build cylinder voids, reservoir headspace, overflow jar
V_machine = V_chamber + V_loop + V_modules
print(f"Chamber {V_chamber:.2f} L + loop {V_loop:.0f} L + voids {V_modules:.0f} L = {V_machine:.1f} L of argon at +20 mbar "
      f"(x1.02 = {V_machine*1.02:.1f} L at ambient)")
purge_cycles = 3
per_build = purge_cycles * V_chamber + V_machine
print(f"Per start-up: {purge_cycles} backfill/pump cycles ({purge_cycles*V_chamber:.0f} L) + final loop fill = about {per_build:.0f} L of argon through the pump exhaust. "
      f"Pump-down and end-of-build venting are small beside a supply fault.")

sources = {
    "machine inventory (chamber + loop + voids)": V_machine / 1e3,
    "80 ft3 cylinder (Airgas size 80, ~85 scf)": 85 * 0.0283168,
    "125 ft3 cylinder (~126 scf)": 126 * 0.0283168,
    "200 ft3 cylinder (~250 scf)": 250 * 0.0283168,
    "300 ft3 cylinder (~336 scf)": 336 * 0.0283168,
    "180 L liquid cylinder (~5,048 scf gas equivalent)": 5048 * 0.0283168,
}
vol_room = 30.0   # m3 [assume, same hypothetical room as Edison]
# Shuttle XP 500 enclosure: 2.83 x 3.12 x 3.95 m [repo heat.md, from byu-vcl PR 318]
V_shuttle_gross = 2.83 * 3.12 * 3.95
free_frac = 0.70  # [assume] fraction of the gross volume that is air (trays, frame and drives take the rest)
V_shuttle = V_shuttle_gross * free_frac
V_bay = 2.450 * 0.864 * 0.695   # tray (2450 x 864) x bay height 695 mm [repo low-profile.md]
V_bay_free = V_bay * 0.5        # [assume] half the bay is machine
print(f"\nShuttle XP 500 enclosure gross {V_shuttle_gross:.1f} m^3 [repo]; free air ~{V_shuttle:.1f} m^3 (assume {free_frac:.0%}); one tray bay {V_bay:.2f} m^3, free ~{V_bay_free:.2f} m^3")
print("(Kardex publishes no interior air volume. Ask Kardex; the bay is open to the lift shaft, so the bay figure is only the first-minutes case.)")

def o2_after(Vs_m3, Vroom_m3, o2_0=20.95):
    """Well-mixed room, constant volume, argon added and mixture leaving: C = C0 exp(-Vs/V)."""
    return o2_0 * math.exp(-Vs_m3 / Vroom_m3)

for tag, Vr in (("lab room 30 m^3 (assume)", vol_room), ("Shuttle free air", V_shuttle), ("one tray bay, still air", V_bay_free)):
    print(f"\nArgon needed to reach O2 limits in {tag} ({Vr:.1f} m^3), no ventilation, perfectly mixed:")
    for lim in (20.0, 19.5, 17.0, 16.0, 12.0):
        print(f"   {lim:>4.1f} % O2 needs {Vr*math.log(20.95/lim):7.3f} m^3 of argon")
    for s, v in sources.items():
        print(f"   release of {s:<52s} ({v:7.2f} m^3) -> O2 = {o2_after(v, Vr):5.1f} %")

# Stratified pool inside the Shuttle (argon is 1.38 x air): depth over the shaft floor
floor = 2.83 * 3.12 * 0.5   # m^2 [assume 50 % of the footprint is open shaft floor]
for s in ("machine inventory (chamber + loop + voids)", "80 ft3 cylinder (Airgas size 80, ~85 scf)"):
    v = sources[s]
    print(f"\nPool depth if {s.split(' (')[0]} settles on the Shuttle floor ({floor:.1f} m^2): {v/floor*1e3:.0f} mm of near-pure argon (0 % O2) before it mixes")

# Leak flow rates: how fast does a failed supply fill the space?
gamma, Rg, Tg = 5 / 3, 8.314 / 0.039948, 293.0
def choked_flow_lpm(d_mm, p_bar_abs, cd=0.7):
    A = PI * (d_mm * 1e-3) ** 2 / 4
    mdot = cd * A * p_bar_abs * 1e5 * math.sqrt(gamma / (Rg * Tg)) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1)))
    rho_std = 1.65  # kg/m3 argon at 21 C, 1 atm
    return mdot / rho_std * 1e3 * 60
print("\nChoked (sonic) argon flow through an orifice, Cd 0.7, standard L/min:")
for d, p in ((0.5, 7), (1.0, 7), (2.0, 7), (4.0, 7), (4.0, 150), (1.0, 150)):
    q = choked_flow_lpm(d, p + 1)
    print(f"   d = {d:3.1f} mm at {p:3d} bar gauge : {q:9.0f} L/min -> {q*60/1e3:7.1f} m^3/h  (fills the 30 m^3 room to 19.5 % in {vol_room*math.log(20.95/19.5)*1e3/q:7.1f} min)")
print("   A free 1/4 in. line from a full cylinder (4 mm bore, 150 bar) empties a size-300 cylinder in minutes: restrict the flow at the source.")

# Ventilation that holds the O2 limit for a steady argon leak q: q/(q+Qv) <= (20.95-19.5)/20.95
frac = (20.95 - 19.5) / 20.95
print(f"\nVentilation to hold >= 19.5 % O2 against a steady argon leak q: Qv >= q (1/{frac:.4f} - 1) = {(1/frac-1):.1f} x q  (steady state, perfect mixing)")
for q in (12, 47, 188, 753):
    print(f"   leak {q:4d} L/min -> ventilation >= {q*(1/frac-1):7.0f} L/min = {q*(1/frac-1)*0.06:7.0f} m^3/h")
Q_heat = 1200.0 / (1.2 * 1005.0 * 5.0)   # m3/s of air for a 5 K rise at 1.2 kW (heat.md option 2: ducted exhaust)
print(f"   The Shuttle heat duct (1.2 kW, 5 K rise) already moves {Q_heat*3600:.0f} m^3/h = {Q_heat*6e4:.0f} L/min: it holds 19.5 % against a leak of {Q_heat*6e4/(1/frac-1):.0f} L/min "
      "(a 4 mm orifice at 7 bar), but ONLY if the duct runs whenever argon can flow and it exhausts outside the Shuttle.")

# Relief valve sizing
hdr("3b. OVERPRESSURE RELIEF for the argon chamber")
door_area = 2445 / 101325.0   # m^2, from the repo's 2,445 N vacuum force on the door (seals.md)
lid_force_vac = 5907.0        # N [repo seals.md, lid at full vacuum]
for p_mbar in (20, 34.5, 50, 100, 200):
    print(f"   +{p_mbar:>5.1f} mbar over the door ({door_area*1e4:.0f} cm^2): {p_mbar*100*door_area:6.0f} N  (2 draw latches rated 2 x 3558 N)")
print("   McMaster 4277T52 (0.5 psi = 34.5 mbar, +/-20 % set accuracy, fully open at ~+10 % of set, 'Cv not rated'): "
      f"opens {34.5*0.8:.0f}-{34.5*1.2:.0f} mbar, fully open {34.5*0.8*1.1:.0f}-{34.5*1.2*1.1:.0f} mbar, i.e. above the +20 mbar operating point with ~40 % margin, "
      "but its capacity is not rated.")

def kv_needed(q_lpm_std, dp_bar=0.05, p2_bar=1.013, rho_n=1.784, T=293.0):
    """ISA/IEC 60534 low-dP gas: Q_N[m3/h] = 514 Kv sqrt(dp*p2/(rho_N*T))."""
    qn = q_lpm_std * 60 / 1e3
    return qn / (514 * math.sqrt(dp_bar * p2_bar / (rho_n * T)))
print("\nRelief capacity needed so the chamber stays <= +50 mbar when the supply fails open (Kv, m^3/h of water at 1 bar):")
for q in (30, 100, 300, 1000, 3000):
    kv = kv_needed(q)
    print(f"   inflow {q:5d} L/min (std) -> Kv >= {kv:6.2f}  (Cv >= {kv/0.865:6.2f})")
print("   Design rule: limit the worst-case inflow with a critical-flow (sonic) orifice sized for the purge (~30-60 L/min), "
      "then size ONE relief for that flow with margin, and a second independent device (burst disc / spring relief) for the rest.")

# ----------------------------------------------------------------------------------------------
# 4. VACUUM / IMPLOSION
# ----------------------------------------------------------------------------------------------
hdr("4. VACUUM LOADS, WINDOW AND IMPLOSION (cross-checks seals.md and analysis/out/fea)")
patm = 101325.0
a_win = 0.048 / 2   # m, support diameter 48 mm [repo FEA]
t_win = 0.008       # m [repo: O50.8 x 8 fused silica]
nu = 0.17
sigma = 3 * (3 + nu) / 8 * patm * (a_win / t_win) ** 2
mor = 52.4e6        # Pa [repo fea.md, design strength used]
print(f"Fused-silica window O50.8 x 8, simply supported on O48: peak stress {sigma/1e6:.2f} MPa (repo FEA 1.15, Roark 1.08); SF vs 52.4 MPa = {mor/sigma:.0f}")
print(f"Force on the window at full vacuum: {patm*PI*a_win**2:.0f} N")
t_req = lambda sf: a_win * math.sqrt(3 * (3 + nu) / 8 * patm * sf / mor)
print(f"Thinnest window for SF 6 / 10: {t_req(6)*1e3:.1f} / {t_req(10)*1e3:.1f} mm  (repo says 2.9 mm for SF 6)")
A_lid = 0.280 * 0.190
print(f"Atmosphere on the 280 x 190 lid footprint: {patm*A_lid/1e3:.1f} kN (repo seals.md counts 5.9 kN with the gland); door 2.4 kN")
E_im = patm * V_chamber / 1e3
print(f"Energy released if the evacuated chamber (6.4 L) fills suddenly: ~{E_im:.0f} J (p*V, upper bound); stored elastic energy of a flat glass window failing is much less, "
      f"but fragments need a shield or retention ring: Robinson (ORNL 1980, cited by Edison) designs viewing windows for the greatest vacuum the pump can pull.")
print("Pump-down lifts powder (repo seals.md): the safety side of that is dust clouds in the pump exhaust: fit a particle trap on the pump inlet.")

# ----------------------------------------------------------------------------------------------
# 5. ALUMINIUM POWDER AND CONDENSATE
# ----------------------------------------------------------------------------------------------
hdr("5. ALUMINIUM POWDER: explosion parameters, inventory, condensate oxidation heat")
print("Published AlSi10Mg values [src Sun 2023, via Edison]: Pmax 0.61 MPa (6.1 bar), Kst 15.10 MPa m/s (151 bar m/s, St 1), MIE 80 mJ (Hartmann tube).")
print("Other published Al: alloys MIE 13-23 mJ, pure Al 4 mJ, Pmax 5-7 bar, dP/dt 250-360 bar/s [src search extract]; atomised Al Kst 64-274 bar m/s, Pmax 3.3-11.8 bar,")
print("   Kst < 100 for > 38 um; filter-collected Al D50 ~5 um MIE < 3 mJ; LPBF condensate MIE < 1 mJ [src EOS notice via Fabbaloo]; filter Kst 2-3 x bulk feed [src Edison/Scotton].")
cube_root = lambda v: v ** (1 / 3)
for kst in (151, 250, 450):
    print(f"   Kst {kst} bar m/s in a 1 m^3 vessel gives (dP/dt)max = {kst/cube_root(1):.0f} bar/s; in the 6.4 L chamber it is {kst/cube_root(V_chamber/1e3):.0f} bar/s")
# Powder inventory
rho_bulk = 1.4   # g/cm3 [assume] AlSi10Mg apparent density
for name, cm3 in (("S reservoir", 38), ("M reservoir", 97), ("L reservoir", 233)):
    m = cm3 * rho_bulk
    print(f"   {name} {cm3} cm^3 -> {m:.0f} g;  if all dispersed in the 30 m^3 room: {m/vol_room:.1f} g/m^3;  in the chamber (6.4 L): {m/V_chamber:.0f} g/L")
print("   Housekeeping: NFPA 652 layer criterion is about 1/32 in (0.8 mm) over 5 % of the area [assume value recalled, check the edition]. "
      f"0.8 mm x 1.4 g/cm^3 = {0.08*rho_bulk*10:.1f} kg/m^2, so 0.33 kg spread thin covers {0.33/(0.08*rho_bulk*10):.1f} m^2 at that depth.")
# Condensate oxidation
dH_Al = 1675.7e3 / (2 * 26.98e-3)   # J/kg Al (2 Al + 1.5 O2 -> Al2O3, dHf = -1675.7 kJ/mol)
print(f"\nOxidation heat of Al: {dH_Al/1e6:.1f} MJ/kg [thermochemistry].  10 g of condensate fully oxidised: {10e-3*dH_Al/1e3:.0f} kJ; heat per mole O2: {1675.7/1.5:.0f} kJ/mol O2.")
for q_air in (0.1, 0.3, 1.0, 3.0):
    n_o2 = 0.2095 * q_air / 24.0     # mol/min at 21 C
    W = n_o2 * 1675.7e3 / 1.5 / 60
    print(f"   air bled in at {q_air:4.1f} L/min, all O2 consumed in the cake: {W:6.0f} W")
h, area, dT_ok = 10.0, 0.10, 50.0
print(f"   A 0.1 m^2 steel housing at {dT_ok:.0f} K above ambient sheds ~{h*area*dT_ok:.0f} W by natural convection ({h:.0f} W/m^2K) -> keep the first air bleed <= ~0.3 L/min, "
      "or better step the oxygen up in argon (0.1 %, 1 %, 5 %, 21 %) watching a thermocouple in the cake [assume; set the real steps in the DHA].")
print("   Hydrogen from Al + water: 2 Al + 6 H2O -> 2 Al(OH)3 + 3 H2: " f"{3*22.4/(2*26.98):.2f} L H2 per g Al (STP), so 100 g of wet fines can give {100*3*22.4/(2*26.98):.0f} L H2.")
print("   Grounding: bonded path resistance <= 10 ohm to building ground, < 1 megohm to ground for conductive hoses/containers [src: NFPA 77 values as commonly quoted; check].")
print("   Respirator: P100 (HEPA 99.97 % at 0.3 um) or N100/R100 for metal dust and condensate [src OSHA 1910.134 definition]; "
      "full-facepiece APF 50 [src OSHA 1910.134 Table 1]; a P100 supplies no oxygen.")
print("   Storage: keep powder in closed, grounded, dry containers; aluminium and magnesium powders away from water, acids, oxidisers; keep Mg-bearing separate. Limits are set by BYU Fire Marshal / IFC H-occupancy control areas.")

# ----------------------------------------------------------------------------------------------
# 6. HOT PLATE
# ----------------------------------------------------------------------------------------------
hdr("6. HOT PLATE")
for name, mass_kg in (("S25 plate+block", 0.12), ("M50 plate+block", 0.27), ("L75 plate+block", 0.60)):   # [assume] 6061 masses
    E = mass_kg * 900 * (200 - 25)
    print(f"   {name}: {mass_kg:.2f} kg at 200 C stores {E/1e3:5.1f} kJ above 25 C")
print("   Contact-burn thresholds (ISO 13732-1 / ASTM C1055 order of magnitude, recalled, check): bare metal ~ 55-60 C for 10 s, ~ 65-70 C for 1 s; so the 50 C release is a "
      "conservative gate. FEA cool-down to 50 C: 15 / 28 / 40 min (S25 / M50 / L75) [repo modules.md].")
print("   Interlock layers: (1) control TC, (2) edge TC, (3) independent limit TC into the CN708 limit controller (latching), (4) 240 C thermal cutoff in the heater circuit [repo].")

# ----------------------------------------------------------------------------------------------
# 7. ELECTRICAL
# ----------------------------------------------------------------------------------------------
hdr("7. ELECTRICAL")
print(f"   IPG YLR-500: 1.7 kW / 1.9 kVA max at 200-240 VAC -> {1900/240:.1f} A at 240 V ({1900/208:.1f} A at 208 V) [repo quote].")
print(f"   Tray input, worst case 500 W CW (heat.md): 2.7 kW -> {2700/240:.1f} A at 240 V; dock legs limited to 24 A.")
print(f"   24 V heater bus: L75 5 x 50 W = 250 W -> {250/24:.1f} A; 350 W supply at full load {350/24:.1f} A. A 24 V DC supply is SELV, but a shorted cartridge lead is a fire hazard: "
      "fuse each heater leg (about 2x the 2.1 A load) and size the wire for the supply's short-circuit current.")
print("   Stored energy to lock out: laser PSU capacitors (wait the vendor's discharge time), scanner and servo drive capacitors, pump motor, argon at +20 mbar and at cylinder pressure, "
      "vacuum, pneumatic clamps, the lift tray, and the 200 C plate (thermal).")

# ----------------------------------------------------------------------------------------------
# 8. ROBOT
# ----------------------------------------------------------------------------------------------
hdr("8. ROBOT AND MOBILE BASE")
print("   UR12e: payload 12.5 kg, reach 1300 mm, max TCP speed 4 m/s [src UR page]; MiR250: max speed 2 m/s, payload up to 250 kg [src MiR page].")
m_arm_eff, m_tool, m_payload = 10.0, 2.0, 1.0   # kg [assume] effective moving mass at the TCP: arm share + gripper + plate/module
m_eff = m_arm_eff + m_tool + m_payload
for v in (0.10, 0.25, 0.50, 1.0):
    print(f"   TCP at {v:4.2f} m/s, effective mass {m_eff:.0f} kg: kinetic energy {0.5*m_eff*v*v:5.2f} J, peak contact force of an undamped spring-mass impact, F = v sqrt(k m), with k = 150 N/mm [assume] ~ {v*math.sqrt(150e3*m_eff):6.0f} N")
print("   ISO/TS 15066 Annex A limits use body-region spring constants and force/pressure thresholds (29 regions); this script does not reproduce them: take the numbers from the standard. "
      "Pinning against a hot plate or an edge is a clamping hazard that no force limit makes acceptable.")
print("\n   Mobile-base stopping distance, s = v*t_r + v^2/(2a)  (t_r 0.3 s, a 0.5 m/s^2 [assume]; get the MiR figures from the vendor):")
for v in (0.3, 0.8, 1.2, 2.0):
    s = v * 0.3 + v * v / (2 * 0.5)
    print(f"      v = {v:3.1f} m/s -> {s:5.2f} m")
print("   ISO 13855 form for a presence-sensing device: S = K T + C, K = 1600 mm/s (walking, S > 500 mm) or 2000 mm/s (hand, fine resolution) [src Keyence/Datalogic via search]. "
      "Example: T = 0.3 s, C = 850 mm for a 40-70 mm resolution device: S = " f"{1.6*0.3*1000+850:.0f} mm.")
print("   Hand-off permissive (all must be TRUE before the arm may open the guard or move into the machine): laser emission off and shutter closed, "
      "key switch in REMOTE-SAFE, plate < 50 C, chamber at ambient and argon valve closed, O2 >= 20.5 % in bay and room, VLM tray locked and stationary, MiR docked and brakes on.")
print("\nDone.")
