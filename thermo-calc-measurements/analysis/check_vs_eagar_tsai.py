#!/usr/bin/env python3
"""Cross-check melt_pool_calibration.TrackField against ArroyaveLab's eagar-tsai package
(pip install eagar-tsai; 0.6.0 used here, the version PR #238 tested). Slow: ~80 s per point
for the package at 1 um resolution.

eagar-tsai's ``beam_diameter`` is 2*sigma (sigma = Gaussian standard deviation), which equals our
1/e^2 radius r0, and its ambient temperature is fixed at 298 K.

Result on 2026-11-14 (AlSi10Mg-like inputs from PR #249, T_l = 867 K):
    P=200 v=0.8 eta=0.31: package W=172.0 D=80.0 um | ours W=173.1 D=80.2 um
    P=300 v=1.2 eta=0.31: package W=192.0 D=90.0 um | ours W=192.2 D=90.9 um
    P=150 v=0.4 eta=0.40: package W=204.0 D=97.0 um | ours W=205.6 D=97.2 um
"""
from eagar_tsai import BeamParameters, MaterialProperties, SimulationDomain, compute_single_point

import melt_pool_calibration as mp

k, rho, cp, Tl, T0 = 110.0, 2650.0, 1040.0, 867.0, 298.0
r0 = 40e-6
for P, v, eta in [(200, 0.8, 0.31), (300, 1.2, 0.31), (150, 0.4, 0.40)]:
    res = compute_single_point(
        BeamParameters(beam_diameter=r0, power=P, velocity=v, absorptivity=eta),
        MaterialProperties(liquidus_temperature=Tl, thermal_conductivity=k, density=rho, specific_heat=cp),
        SimulationDomain(x_length_um=1500, y_length_um=300, z_depth_um=250, spatial_resolution_um=1.0),
        full_field=False)
    W, D = mp.TrackField(v, r0, k, rho, cp).pool(eta, P, Tl - T0)
    print(f"P={P} v={v} eta={eta}: package W={res.width_um:.1f} D={res.depth_um:.1f} um | "
          f"ours W={W * 1e6:.1f} D={D * 1e6:.1f} um")
