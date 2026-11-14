"""Synthetic-data checks for the analysis scripts: each recovers a known answer.

    cd thermo-calc-measurements/analysis && python -m pytest -q test_analysis.py
"""
import json
import math

import numpy as np
import pytest

import conductivity as cond
import density_porosity as dens
import dsc_solidification as dsc
import espei_export as ee
import kinetics as kin
import melt_pool_calibration as mp
import xrd_lattice as xrd


def test_dsc_recovers_latent_heat_and_liquidus():
    tr, _ = dsc.synthetic_trace(L=390.0, tau=3.0)
    res, cur = dsc.analyse(tr["T_C"], tr["heat_flow"], 10.0, 560.0, 662.0, t=tr["time_s"], tau=3.0)
    assert res.latent_heat_J_per_g == pytest.approx(390.0, rel=0.01)
    assert res.liquidus_C == pytest.approx(640.0, abs=0.5)      # lag-corrected end of melting
    assert res.solidus_C == pytest.approx(577.0, abs=0.5)       # eutectic onset
    Tm = np.linspace(560, 660, 400)
    cmp = dsc.compare_with_model(cur["T_of_fs"], cur["fs_grid"], Tm, dsc.scheil_fs(Tm))
    assert max(abs(x) for x in cmp["dT_meas_minus_model_K"][:8]) < 1.0


def test_dsc_lag_uncorrected_overestimates_liquidus():
    tr, _ = dsc.synthetic_trace(L=390.0, tau=3.0)
    res, _ = dsc.analyse(tr["T_C"], tr["heat_flow"], 10.0, 560.0, 662.0, t=tr["time_s"], tau=None)
    assert res.liquidus_C > 640.5


def test_dsc_tau_estimate_from_pure_metal_peak():
    t = np.arange(0, 200, 0.1)
    q = np.where(t < 50, 0.0, np.exp(-(t - 50) / 4.0))
    assert dsc.estimate_tau(t, q) == pytest.approx(4.0, rel=0.05)


def test_rate_extrapolation():
    T0, s = dsc.extrapolate_to_zero_rate([5, 10, 20], [641.0, 642.0, 644.0])
    assert T0 == pytest.approx(640.0, abs=0.01)


def test_melt_pool_fit_recovers_absorptivity():
    eta = mp.demo(eta_true=0.31)
    assert eta == pytest.approx(0.31, abs=0.02)


def test_keyhole_number_scales_as_inverse_sqrt_v():
    k1 = mp.keyhole_number(0.3, 200, 0.5, 40e-6, 110, 2650, 1040, 444)
    k2 = mp.keyhole_number(0.3, 200, 2.0, 40e-6, 110, 2650, 1040, 444)
    assert k1 / k2 == pytest.approx(2.0, rel=1e-9)


def test_archimedes_and_water_density():
    assert dens.water_density(20.0) * 1000 == pytest.approx(998.2067, abs=0.001)
    assert dens.water_density(4.0) * 1000 == pytest.approx(999.975, abs=0.001)
    r, ip, true_frac = dens.demo()
    assert r["porosity"] == pytest.approx(0.010, abs=1e-4)
    assert ip["pore_area_fraction"] == pytest.approx(true_frac, rel=0.02)


def test_conductivity_conversions():
    assert cond.iacs_to_resistivity(100.0) == pytest.approx(1.7241)
    assert cond.resistivity_to_iacs(cond.iacs_to_resistivity(42.0)) == pytest.approx(42.0)
    A, B = cond.fit_smith_palmer([3.5, 4.2, 5.0, 6.1],
                                 [0.92 * cond.L0 * 293.15 / (r * 1e-8) + 9.0 for r in [3.5, 4.2, 5.0, 6.1]])
    assert (A, B) == (pytest.approx(0.92), pytest.approx(9.0))


def test_kinetics():
    out = kin.demo()
    assert out["kissinger"]["Ea_kJ_mol"] == pytest.approx(120.0, rel=1e-3)
    assert out["jmak"]["n"] == pytest.approx(1.2, abs=0.1)
    assert out["arrhenius_peak_aging"]["Q_kJ_mol"] == pytest.approx(90.0, rel=1e-3)
    g = kin.lsw_gamma(K_m3_s=1e-30, T_K=573.0, D_m2_s=1e-19, c_e_mol_m3=10.0, Vm_m3_mol=1e-5)
    K_back = 8 * g * 10.0 * 1e-10 * 1e-19 / (9 * kin.R * 573.0)
    assert K_back == pytest.approx(1e-30)


def test_nelson_riley_removes_displacement_error():
    res, naive = xrd.demo(a_true=4.0560, displacement_um=50.0)
    assert res["a0_A"] == pytest.approx(4.0560, abs=2e-4)
    assert abs(naive - 4.0560) > abs(res["a0_A"] - 4.0560)


def test_espei_export_shape():
    ds = ee.to_espei(ee.DEMO_ROWS, dependent="AL", reference="VCL-demo")
    d = ds["AL-MN-ZR"]
    assert d["output"] == "ZPF" and len(d["values"]) == len(d["conditions"]["T"]) == 2
    liquidus = d["values"][0]
    assert liquidus[0][0] == "LIQUID" and liquidus[1][2] == [None, None]
    espei_datasets = pytest.importorskip("espei.datasets")
    espei_datasets.check_dataset(json.loads(json.dumps(d)))
