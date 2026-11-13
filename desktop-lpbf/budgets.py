"""Back-of-envelope sizing for the desktop LPBF concept (issue #260).

Run: python desktop-lpbf/budgets.py
Every input is a named assumption at the top; change them and re-run.
"""
import math

# --- Build and powder -------------------------------------------------------
plate_d_mm = 50.0          # round build plate (reduced-volume insert); 50 mm = Aconity MINI-class
layer_um = 30.0            # layer thickness
build_h_mm = 15.0          # tall enough for density cubes + small tensile coupons
dose_factor = 1.8          # powder dosed per layer / powder that lands on the plate (1.5-2 typical)
rho_solid = 2.68           # g/cm^3, AlSi10Mg
packing_bed = 0.50         # relative density of the spread layer
packing_hopper = 0.55      # tap-ish density in the hopper

area_cm2 = math.pi * (plate_d_mm / 20) ** 2
layers = build_h_mm * 1000 / layer_um
bed_g_per_layer = area_cm2 * layer_um * 1e-4 * rho_solid * packing_bed
dosed_g_per_layer = bed_g_per_layer * dose_factor
build_powder_g = dosed_g_per_layer * layers
hopper_cm3 = build_powder_g / (rho_solid * packing_hopper)

# --- Gas: vacuum-purge-backfill ------------------------------------------------
o2_air_ppm = 209_460
p_atm_mbar = 1013.0
def cycles_to(target_ppm, p_base_mbar):
    """Ideal dilution; ignores outgassing, leaks and moisture desorption."""
    return math.ceil(math.log(o2_air_ppm / target_ppm) / math.log(p_atm_mbar / p_base_mbar))

chamber_l = 6.0            # e.g. ~200 x 150 x 200 mm process chamber, internal
flow_purge_l = chamber_l * math.log(o2_air_ppm / 100)  # well-mixed flow purge to 100 ppm

# --- Cross-flow -------------------------------------------------------------
nozzle_w_mm, nozzle_h_mm, v_ms = 70.0, 8.0, 2.0
crossflow_lpm = nozzle_w_mm * nozzle_h_mm * 1e-6 * v_ms * 60_000

# --- Gantry vs galvo: what it takes to scan one hatch vector at constant speed -----
v_scan = 1.0               # m/s, typical Al LPBF scan speed (0.8-1.6 m/s)
hatch_len_mm = 10.0        # vector length inside a 10 mm cube
a_gantry = 10.0            # m/s^2, a stiff servo/linear-motor gantry (~1 g)
a_galvo_equiv = 2000.0     # m/s^2 at the focal plane (galvo mirrors reach this easily)
def accel_dist_mm(v, a):
    return v * v / (2 * a) * 1000

print(f"Plate {plate_d_mm:.0f} mm dia = {area_cm2:.1f} cm^2; {layers:.0f} layers of {layer_um:.0f} um for {build_h_mm:.0f} mm")
print(f"Powder per layer: {bed_g_per_layer:.2f} g on the plate, {dosed_g_per_layer:.2f} g dosed")
print(f"Powder per build: {build_powder_g:.0f} g -> hopper of {hopper_cm3:.0f} cm^3 (+ margin)")
for p in (1.0, 10.0, 130.0):
    print(f"Vacuum-purge to 100 ppm from base {p:g} mbar: {cycles_to(100, p)} cycle(s); to 10 ppm: {cycles_to(10, p)}")
print(f"Well-mixed flow purge of a {chamber_l:.0f} L chamber to 100 ppm: {flow_purge_l:.0f} L Ar (~{math.log(o2_air_ppm/100):.1f} volume changes)")
print(f"Cross-flow {nozzle_w_mm:.0f} x {nozzle_h_mm:.0f} mm nozzle at {v_ms} m/s: {crossflow_lpm:.0f} L/min (recirculated, not vented)")
print(f"Accel distance to {v_scan} m/s: gantry at {a_gantry} m/s^2 -> {accel_dist_mm(v_scan, a_gantry):.0f} mm each end; "
      f"galvo-equivalent {a_galvo_equiv:.0f} m/s^2 -> {accel_dist_mm(v_scan, a_galvo_equiv):.2f} mm")
t_gantry = hatch_len_mm/1000/v_scan + 2*v_scan/a_gantry
print(f"One {hatch_len_mm:.0f} mm hatch at {v_scan} m/s with turnaround: gantry ~{t_gantry*1000:.0f} ms vs {hatch_len_mm/v_scan:.0f} ms of laser-on time")
