"""Cross-check scripts/keyhole_open_models.py against lpbf_map 2.0.1 (commit 32a5089) on the same inputs."""
import math, sys
import numpy as np
sys.path.insert(0, "/tmp/lpbfmap/src-lpbf/src")
from lpbf_map import Material, ProcessParameters, MeltPool
from lpbf_map.meltpool import _calculate_gladush_smurov_depth
from lpbf_map.defects.keyhole_gan import KeyholeGanCriterion
from lpbf_map.defects.keyhole_king import KeyholeKingCriterion
mat = dict(name="AlSi10Mg-blend-props", density=2650.0, specific_heat=1040.0, thermal_conductivity=110.0,
           boiling_temperature=2743.0, melting_temperature=1019.3, absorptivity=0.3841, electrical_resistivity=1e-7)
m = Material.from_dict(mat, name="blend")
alpha = 110.0 / (2650.0 * 1040.0)
print("lpbf_map thermal_diffusivity:", float(m.thermal_diffusivity), "ours:", alpha)
for P, v in [(375.0, 0.4), (250.0, 0.8), (200.0, 1.2)]:
    md = dict(absorptivity=0.3841, thermal_conductivity=110.0, boiling_temperature=2743.0, thermal_diffusivity=alpha)
    gs = _calculate_gladush_smurov_depth(P, v, 45e-6, md)
    ours = 0.3841 * P / (2 * math.pi * 110.0 * 2743.0) * math.log((45e-6 + alpha / v) / 45e-6)
    print(f"P={P} v={v}: lpbf_map GS depth {gs*1e6:.2f} um, ours {ours*1e6:.2f} um")
# Gan and King criteria as lpbf_map implements them, at 30 C ambient, across speed at fixed power
for v in [0.4, 0.8, 1.6, 3.2]:
    params = ProcessParameters(laser_power=300.0, scan_speed=v, beam_radius=45e-6, ambient_temperature=303.15)
    pool = MeltPool(material=m, parameters=params)
    gan = KeyholeGanCriterion().check(pool, None) if True else None
    king = KeyholeKingCriterion().check(pool, None)
    ke = 0.3841 * 300 / ((1019.3 - 303.15) * math.pi * 2650 * 1040 * math.sqrt(alpha * v * (45e-6) ** 3))
    print(f"300 W, v={v} m/s: our Ke={ke:.2f} -> lpbf_map Gan flag {gan} (Ke>6: {ke>6}); lpbf_map King flag {king}")
pth = (1019.3 - 303.15) * math.pi * 110.0 * 45e-6 / 0.3841 * (2743.0 / 1019.3)
print(f"lpbf_map King threshold power (speed-independent): {pth:.1f} W")
