#!/usr/bin/env python3
"""Coaxial radiometry end to end (issue #260, monitoring/optics.md §3).

From a melt-pool surface temperature field, through aluminium's spectral emissivity, the return pupil, the cover slide, the
chamber window, the f-theta, the galvo mirrors (unknown coating: two bounds), the DMSP1000 and the branch's dichroic and
filter, onto four detectors:
  (a) a monochrome IMX296 board (Pi Global Shutter class) at 8 um/px, 10-500 us exposures;
  (b) the Thorlabs PDA36A2 (Si) at each gain;
  (c) an InGaAs photodiode (Thorlabs PDA20CS2) in a 1.55 um band (needs the DMSP1000 replaced);
  (d) a Kron Chronos 2.1-HD at 24 kfps (10 um pixels at 8 um/px on the plate).
It reports signal, SNR, saturation, the lowest temperature each one sees, the two-colour ratio's sensitivity and its error
from aluminium's non-grey emissivity, plume emission against the pool's, and the 1070 nm leakage each channel must block.

    python radiometry.py [--fields PATH_TO_surface_fields.npz]

--fields: worker A's melt-pool model writes analysis/out/monitoring/melt/surface_fields.npz. Accepted layouts (units are
detected from the numbers): 1-D x and y (m, mm or um) and a 2-D temperature array (K) named T, T_K, T_surface or T_<case>;
or a 3-D temperature array (cases x ny x nx) with a 'cases' array of labels. Without it (or if the file is missing) the script
uses its own Eagar-Tsai fields (Gaussian moving source on a semi-infinite body, clipped at boiling).
Writes analysis/out/monitoring/optics/radiometry.json, radiometry.md, radiometry.png.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "analysis" / "out" / "monitoring" / "optics"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))
import parts as PT  # noqa: E402   (vendor data for every part: spec, price, source)

H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
C2 = H * C / KB                                   # 0.014388 m K
EV = 1.602176634e-19
ME, EPS0, NA_ = 9.1093837e-31, 8.8541878128e-12, 6.02214076e23

# ------------------------------------------------------------------------------------------------ material: aluminium
T_SOL, T_LIQ, T_BOIL = 830.0, 869.0, 2743.0        # AlSi10Mg solidus/liquidus (557/596 C, monitoring_optics.py); Al boils at 2743 K (1 atm)
T_LIQ_6061 = 925.0


def eps_liquid_drude(lam_um, T):
    """Normal spectral emissivity of liquid Al from the Drude free-electron model, built from the liquid's measured DC
    resistivity and density (no fitted optical constants): rho_e = 24.2 + 0.0145 (T - 933) uOhm cm (Desai et al. 1984,
    J. Phys. Chem. Ref. Data 13, 1069: 24.2 at the melting point), mass density 2377 - 0.311 (T - 933) kg/m3 (Assael et al.
    2006, J. Phys. Chem. Ref. Data 35, 285), three free electrons per atom."""
    T = np.maximum(T, 933.0)
    rho_e = (24.2 + 0.0145 * (T - 933.0)) * 1e-8
    dens = 2377.0 - 0.311 * (T - 933.0)
    n_e = 3 * dens / 0.0269815 * NA_
    wp2 = n_e * EV ** 2 / (EPS0 * ME)
    gamma = EPS0 * wp2 * rho_e
    w = 2 * math.pi * C / (np.asarray(lam_um) * 1e-6)
    eps = 1 - wp2 / (w * w + 1j * gamma * w)
    N = np.sqrt(eps)
    R = np.abs((N - 1) / (N + 1)) ** 2
    return 1 - R


def planck(lam_um, T):
    """Spectral radiance, W m^-2 sr^-1 nm^-1."""
    lam = np.asarray(lam_um) * 1e-6
    with np.errstate(over="ignore"):
        return 2 * H * C ** 2 / lam ** 5 / np.expm1(C2 / (lam * T)) * 1e-9


# ------------------------------------------------------------------------------------------------ melt-pool fields
def eagar_tsai(P, v, absorptivity=0.3, w0=48e-6, T0=473.0, k=100.0, rho=2500.0, cp=1100.0, nx=360, ny=150, dx=4e-6):
    """Surface temperature of a semi-infinite body under a moving Gaussian source (Eagar & Tsai 1983, Weld. J. 62, 346s),
    clipped at boiling. w0: 1/e2 radius (96 um spot -> 48 um). Mid-range AlSi10Mg properties between solid and liquid
    (k 100 W/m K, rho 2500 kg/m3, cp 1100 J/kg K; solid k ~ 130-170, liquid ~ 90). T0 473 K: the 200 C plate."""
    alpha = k / (rho * cp)
    sig = w0 / 2
    x = (np.arange(nx) - nx * 0.8) * dx                # beam at x = 0, moving +x; the tail runs to -x
    y = (np.arange(ny) - ny // 2) * dx
    X, Y = np.meshgrid(x, y)
    tau = np.geomspace(1e-9, 0.05, 900)
    T = np.zeros_like(X)
    q = absorptivity * P
    pref = q / (math.pi * rho * cp * math.sqrt(4 * math.pi * alpha))
    for i in range(0, X.shape[0], 10):
        xs, ys = X[i:i + 10, :, None], Y[i:i + 10, :, None]
        f = tau ** -0.5 / (2 * alpha * tau + sig ** 2) * np.exp(-((xs - v * tau) ** 2 + ys ** 2) / (4 * alpha * tau + 2 * sig ** 2))
        T[i:i + 10] = np.trapezoid(f, tau, axis=-1)
    T = T0 + pref * T
    return x, y, np.minimum(T, T_BOIL)


OWN_CASES = {"200 W, 0.4 m/s": (200.0, 0.4), "320 W, 1.1 m/s (EOS-equivalent, optics.md 9.1)": (320.0, 1.1),
             "350 W, 0.8 m/s": (350.0, 0.8)}


def load_fields(path):
    """Worker A's surface_fields.npz, if present; otherwise this script's own Eagar-Tsai fields."""
    if path and Path(path).exists():
        z = np.load(path, allow_pickle=True)
        keys = list(z.keys())
        def unit(a):
            s = float(np.nanmax(a) - np.nanmin(a))
            return 1.0 if s < 0.05 else (1e-3 if s < 50 else 1e-6)
        xk = next(k for k in keys if k.lower() in ("x", "x_m", "x_mm", "x_um"))
        yk = next(k for k in keys if k.lower() in ("y", "y_m", "y_mm", "y_um"))
        x, y = z[xk] * unit(z[xk]), z[yk] * unit(z[yk])
        out = {}
        Tk = [k for k in keys if k.lower().startswith("t") and z[k].ndim >= 2]
        for k in Tk:
            a = z[k]
            if a.ndim == 3:
                labels = list(z["cases"]) if "cases" in keys else [f"{k}[{i}]" for i in range(a.shape[0])]
                for lab, t in zip(labels, a):
                    out[str(lab)] = (x, y, np.minimum(np.asarray(t, float), T_BOIL))
            else:
                out[k] = (x, y, np.minimum(np.asarray(a, float), T_BOIL))
        return out, f"{path} (keys {keys})"
    return {k: eagar_tsai(P, v) for k, (P, v) in OWN_CASES.items()}, "own Eagar-Tsai fields (worker A's surface_fields.npz not given)"


# ------------------------------------------------------------------------------------------------ the optical train
def interp(table, lam_nm):
    t = np.array(table, float)
    return np.interp(lam_nm, t[:, 0], t[:, 1], left=t[0, 1], right=t[-1, 1])


def tau_plate(lam_nm, coat_band=(1030, 1100)):
    """One AR(1064)-coated fused-silica plate (window or slide): 0.25 %/surface in its V band, ~3.5 %/surface outside
    (about uncoated; a 1064 V-coat can reflect more or less than bare glass off its band: bound 1-8 %)."""
    lam_nm = np.asarray(lam_nm, float)
    r = np.where((lam_nm >= coat_band[0]) & (lam_nm <= coat_band[1]), 0.0025, 0.035)
    return (1 - r) ** 2


def tau_galvo(lam_nm, case):
    """Two galvo mirrors coated for 1064 nm. 'pass': R 0.95 each everywhere used. 'Kozjek': 750-875 nm 'almost completely
    blocked' (Kozjek et al. 2026, via Edison): R_pair 0.02 there, 0.9 elsewhere. The real curve must be measured (step 2)."""
    lam_nm = np.asarray(lam_nm, float)
    if case == "pass":
        return np.full_like(lam_nm, 0.95 ** 2)
    return np.where((lam_nm >= 750) & (lam_nm <= 875), 0.02, 0.90)


def train(lam_nm, galvo="pass", fouled_slide=1.0):
    """Transmission from the plate to the coaxial branch's entrance (behind the DMSP1000 position), without the branch."""
    return fouled_slide * tau_plate(lam_nm) ** 2 * interp(PT.FTHETA_T, lam_nm) * tau_galvo(lam_nm, galvo)


# ------------------------------------------------------------------------------------------------ channels
NA_RETURN = {"12 mm": 6.0 / 160.0, "18 mm": 9.0 / 160.0}      # f-theta design beam; the DMSP1000 at 45 deg (one axis)
EPS_SOLID = 0.2                                             # solid Al in LPBF: 0.1-0.35 (monitoring.md §2.3; Edison r8: 0.05-0.15 clean, higher oxidised)
EPS_LEVELS = {"Drude (clean liquid)": None, "0.12 at 1 um (literature midpoint)": 0.12, "0.20 at 1 um (effective, LPBF)": 0.20}


def eps_liquid(lam_um, T, level=None):
    e = eps_liquid_drude(lam_um, T)
    if level is None:
        return e
    return e * level / float(eps_liquid_drude(1.0, 933.0))


def dmsp1000_T(lam_nm):
    return interp(PT.DMSP1000_T, lam_nm)


# Branch layout (monitoring_spec.COAX): cube1 DMSP1000 (as built) -> FESH1000 (shared 1070 nm blocker; the NF1064-44 is left
# out because it also blocks 520-720 nm) -> cube2 plate beamsplitter (R to the camera, -y) -> cube3 DMLP805 (reflects < 790 nm
# to photodiode A, transmits > 825 nm to photodiode B along -x). InGaAs options: (a) a DMSP1180-class pick-off right after cube1,
# fed by the DMSP1000's own 1625-1725 nm leak; (b) the DMSP1000 replaced by a 1064 notch dichroic.
BS_R, BS_T = PT.SPLITTER["R"], PT.SPLITTER["T"]


def fesh(lam):
    return 10 ** -interp(PT.FESH1000_OD, lam)


def filt(key):
    return PT.FILTERS[key]


def dmsp950_t(l):
    return interp(PT.DMSP950_T, l)


def dmsp950_r(l):
    return interp(PT.DMSP950_R, l)


def fesh0950(l):
    return 10 ** -interp(PT.FESH0950_OD, l)


def felh0900(l):
    return np.where(np.asarray(l) >= 902.0, filt("LP900"), 1e-4)     # step model of a 900 nm long-pass (data not read)


# Baseline (all dichroic): cube2 DMSP950 reflects 955-990 nm to the camera, transmits < 930 nm to cube3 (DMLP805): PD-A FBH700-40
# (reflected), PD-B FBH900-40 (transmitted). Alternative: cube2 a BSW26 50:50 plate, camera FBH850-10 or FBH700-10.
CH = {
    "PD-A 700/40 (PDA36A2)": dict(det="PDA36A2", band=(700, 40), branch=lambda l: dmsp950_t(l) * interp(PT.DMLP805_R, l) * filt("700/40") * 0.98 * fesh(l)),
    "PD-B 900/40 (PDA36A2)": dict(det="PDA36A2", band=(900, 40), branch=lambda l: dmsp950_t(l) * interp(PT.DMLP805_T, l) * filt("900/40") * 0.98 * fesh(l)),
    "camera 955-990 (IMX296)": dict(det="IMX296 mono", band=(975, 50), branch=lambda l: dmsp950_r(l) * 0.98 * fesh(l) ** 2),
    "camera 955-990 (Chronos 2.1-HD)": dict(det="Chronos 2.1-HD mono", band=(975, 50), branch=lambda l: dmsp950_r(l) * 0.98 * fesh(l) ** 2),
    "alt: camera 850/10, 50:50 plate (IMX296)": dict(det="IMX296 mono", band=(850, 10), branch=lambda l: BS_R * filt("850/10") * 0.98 * fesh(l)),
    "alt: camera 700/10, 50:50 plate (IMX296)": dict(det="IMX296 mono", band=(700, 10), branch=lambda l: BS_R * filt("700/10") * 0.98 * fesh(l)),
    "alt: PD 850/40 behind the 50:50 plate (PDA36A2)": dict(det="PDA36A2", band=(850, 40), branch=lambda l: BS_T * interp(PT.DMLP805_T, l) * filt("850/40") * 0.98 * fesh(l)),
    "InGaAs 1625-1725 behind the DMSP1000 (PDA20CS2)": dict(det="PDA20CS2", band=(1675, 100),
                                                          branch=lambda l: PT.PICKOFF_1180_R * filt("LP1250") * 0.98),
    "InGaAs 1550/12, notch dichroic for the DMSP1000 (PDA20CS2)": dict(det="PDA20CS2", band=(1550, 12), ingaas=True,
                                                                      branch=lambda l: PT.PICKOFF_1180_R * filt("1550/12") * 0.98),
}


def weights(ch, galvo="pass"):
    """(lam grid nm, weight per nm) for a channel: train x branch x response, the band a top hat at the filter's FWHM."""
    c, fw = ch["band"]
    lam = np.linspace(c - fw / 2, c + fw / 2, 41)
    d = PT.DET[ch["det"]]
    tr = train(lam, galvo)
    tr = tr * (PT.NOTCH_DICHROIC_T if ch.get("ingaas") else dmsp1000_T(lam))
    if d["kind"] == "photodiode":
        resp = interp(d["resp"], lam)                      # A/W
    else:
        resp = interp(d["qe"], lam) * lam * 1e-9 / (H * C)  # electrons per joule
    return lam, tr * ch["branch"](lam) * resp


def lut(ch, galvo="pass", level=None, Ts=np.linspace(600, T_BOIL, 400)):
    """Signal per unit area and solid angle (A or e-/s per m2 sr) against temperature, liquid and solid."""
    lam, w = weights(ch, galvo)
    liq = np.array([np.trapezoid(eps_liquid(lam / 1000, t, level) * planck(lam / 1000, t) * w, lam) for t in Ts])
    sol = np.array([EPS_SOLID * np.trapezoid(planck(lam / 1000, t) * w, lam) for t in Ts])
    return Ts, liq, sol


def signal_map(T, lt):
    Ts, liq, sol = lt
    s = np.where(T >= T_LIQ, np.interp(T, Ts, liq), np.interp(T, Ts, sol))
    return np.where(T > 600, s, 0.0)


def pd_numbers(I, d, Rpk):
    """Photodiode: output voltage and SNR at each gain for photocurrent I (A)."""
    out = {}
    for g, (G, bw, nep) in d["gains"].items():
        V = I * G
        i_n = nep * Rpk * math.sqrt(bw)
        out[g] = dict(V=V, saturated=V > d["out_max_V"], snr=I / i_n, bandwidth_Hz=bw)
    return out


def t_min_uniform(lt, need, area_m2, omega, liquid_ok=True):
    """Lowest temperature at which a uniform patch of area_m2 gives signal >= need (same units as lt x area x omega)."""
    Ts, liq, sol = lt
    s = np.where(Ts >= T_LIQ, liq, sol) * area_m2 * omega
    ok = np.nonzero(s >= need)[0]
    return float(Ts[ok[0]]) if len(ok) else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fields", default=str(ROOT / "analysis" / "out" / "monitoring" / "melt" / "surface_fields.npz"))
    a = ap.parse_args(argv)
    fields, fsrc = load_fields(a.fields)
    R = dict(fields_source=fsrc, assumptions=dict(
        eps_liquid="Drude from liquid Al's DC resistivity (Desai 1984) and density (Assael 2006), scaled to the level named; "
                   "Edison r8-coaxial-radiometry: 0.10-0.15 at 1 um for clean liquid Al, 0.15-0.25 effective in LPBF",
        eps_solid=EPS_SOLID, train="slide and window (3.5 %/surface off their 1064 V-coat), f-theta (Thorlabs FTH100-1064 curve), "
        "two galvo mirrors (pass: 0.90; Kozjek/Hooper: 0.02 at 750-875 nm), DMSP1000 (Thorlabs data)",
        splitter=PT.SPLITTER, shared_blocker="FESH1000 (OD 5.4-6.0 at 1064-1100 nm)", fov_photodiodes_mm=PT.FOV_PD_MM), cases={}, channels={})
    na = NA_RETURN["12 mm"]
    omega = math.pi * na ** 2
    luts = {(k, g, lv): lut(ch, g, EPS_LEVELS[lv]) for k, ch in CH.items() for g in ("pass", "Kozjek")
            for lv in EPS_LEVELS}
    LV0 = "0.12 at 1 um (literature midpoint)"
    for name, (x, y, T) in fields.items():
        X, Y = np.meshgrid(x, y)
        dA = (x[1] - x[0]) * (y[1] - y[0])
        liq = T >= T_LIQ
        case = dict(T_peak_K=float(T.max()), liquid_area_mm2=float(liq.sum() * dA * 1e6),
                    liquid_length_mm=float(np.ptp(X[liq]) * 1e3) if liq.any() else 0.0,
                    liquid_width_mm=float(np.ptp(Y[liq]) * 1e3) if liq.any() else 0.0, channels={})
        fov = np.hypot(X, Y) <= PT.FOV_PD_MM * 1e-3 / 2
        for k, ch in CH.items():
            d = PT.DET[ch["det"]]
            rec = {}
            for g in ("pass", "Kozjek"):
                for lv in EPS_LEVELS:
                    smap = signal_map(T, luts[(k, g, lv)])
                    if d["kind"] == "photodiode":
                        I = float((smap * fov).sum() * dA * omega)
                        Rpk = max(r for _, r in d["resp"])
                        rec[f"{g} | {lv}"] = dict(photocurrent_A=I, gains=pd_numbers(I, d, Rpk))
                    else:
                        # camera pixels of 8 um on the plate: 2 x 2 blocks of the 4 um grid (the own fields' spacing)
                        nb = max(1, int(round(8e-6 / (x[1] - x[0]))))
                        h, w_ = (smap.shape[0] // nb) * nb, (smap.shape[1] // nb) * nb
                        px = smap[:h, :w_].reshape(h // nb, nb, w_ // nb, nb).mean(axis=(1, 3))
                        rate = px * (8e-6) ** 2 * omega           # e-/s per pixel
                        ex = {}
                        for t_us in (10, 50, 100, 500):
                            Ne = rate * t_us * 1e-6
                            rn = math.hypot(d["read_e"], d["fwc_e"] / 2 ** d["bits"] / math.sqrt(12))
                            snr = Ne / np.sqrt(Ne + rn ** 2)
                            ex[t_us] = dict(peak_e=float(Ne.max()), saturated=bool(Ne.max() > d["fwc_e"]),
                                            peak_snr=float(snr.max()), px_snr_over_3=int((snr >= 3).sum()),
                                            area_snr3_mm2=float((snr >= 3).sum() * 64e-6), liquid_px=int(liq.sum() * dA / 64e-12))
                        rec[f"{g} | {lv}"] = dict(peak_rate_e_per_s=float(rate.max()), t_sat_us=float(d["fwc_e"] / rate.max() * 1e6), exposures=ex)
            case["channels"][k] = rec
        # two-colour: PD-A / PD-B (700/40 over 900/40), grey calibration with the same throughput
        tc = {}
        for g in ("pass", "Kozjek"):
            for lv in EPS_LEVELS:
                sa = case["channels"]["PD-A 700/40 (PDA36A2)"][f"{g} | {lv}"]["photocurrent_A"]
                sb = case["channels"]["PD-B 900/40 (PDA36A2)"][f"{g} | {lv}"]["photocurrent_A"]
                tc[f"{g} | {lv}"] = dict(ratio=sa / sb, T_ratio_K=t_from_ratio(sa / sb, g))
        case["two_colour"] = tc
        R["cases"][name] = case
    R["two_colour"] = two_colour_tables()
    R["t_min"] = t_min_tables(omega, luts, LV0)
    R["plume"] = plume_tables(fields, omega)
    R["leak_1070"] = leak_tables(fields, omega, luts, LV0)
    (OUT / "radiometry.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    write_md(R)
    plot(R, fields, luts, LV0)
    return R


def grey_ratio(T, galvo="pass"):
    la, wa = weights(CH["PD-A 700/40 (PDA36A2)"], galvo)
    lb, wb = weights(CH["PD-B 900/40 (PDA36A2)"], galvo)
    return np.trapezoid(planck(la / 1000, T) * wa, la) / np.trapezoid(planck(lb / 1000, T) * wb, lb)


def t_from_ratio(r, galvo="pass"):
    Ts = np.linspace(700, 4000, 1500)
    rr = np.array([grey_ratio(t, galvo) for t in Ts])
    return float(np.interp(r, rr, Ts))


def two_colour_tables():
    """Sensitivity of the 700/950 ratio, and the temperature error from non-grey emissivity (Wien form)."""
    out = dict(pair_nm=[700, 900], sensitivity=[], non_grey=[])
    l1, l2 = 0.700, 0.900
    for T in (1000.0, 1500.0, 2000.0, 2500.0):
        r0, r1 = grey_ratio(T), grey_ratio(T + 1.0)
        dlnr = math.log(r1 / r0)
        out["sensitivity"].append(dict(T_K=T, dlnR_per_K=dlnr, dT_for_1pct_ratio_K=0.01 / dlnr))
        e_d = float(eps_liquid_drude(l1, T) / eps_liquid_drude(l2, T))
        row = dict(T_K=T, drude_eps700_over_eps950=e_d)
        for lab, er in (("Drude", e_d), ("+5 %", 1.05), ("-5 %", 0.95), ("+10 %", 1.10), ("-10 %", 0.90)):
            # Wien: 1/T_ratio = 1/T - ln(eps1/eps2) / (c2 (1/l1 - 1/l2)); a higher eps at the short band reads hot
            Tr = 1 / (1 / T - math.log(er) / (C2 * 1e6 * (1 / l1 - 1 / l2)))
            row[lab] = Tr - T
        out["non_grey"].append(row)
    # other pairs, same non-greyness: how the error scales with the spacing
    out["pairs_error_K_at_2000K_for_5pct"] = {f"{a}/{b}": 2000.0 ** 2 * math.log(1.05) / (C2 * 1e6 * (1 / (a / 1000) - 1 / (b / 1000)))
                                               for a, b in ((700, 900), (700, 950), (650, 950), (850, 950), (700, 850), (900, 1650), (700, 1650))}
    return out


def t_min_tables(omega, luts, lv):
    """Lowest temperature each detector sees: camera pixel (SNR 3 in one frame), photodiode (SNR 3 at each gain's bandwidth)
    for a solid patch filling the field stop and for a liquid patch of 0.05 mm2."""
    out = {}
    for k, ch in CH.items():
        d = PT.DET[ch["det"]]
        for g in ("pass", "Kozjek"):
            lt = luts[(k, g, lv)]
            if d["kind"] == "camera":
                rn = math.hypot(d["read_e"], d["fwc_e"] / 2 ** d["bits"] / math.sqrt(12))
                need = (9 + math.sqrt(81 + 36 * rn * rn)) / 2       # electrons for SNR 3
                row = {}
                for t_us in (10, 100, 500):
                    row[f"{t_us} us"] = t_min_uniform(lt, need / (t_us * 1e-6), (8e-6) ** 2, omega)
                out[f"{k} | {g}"] = row
            else:
                Rpk = max(r for _, r in d["resp"])
                row = {}
                for gdb in (20, 40, 60):
                    G, bw, nep = d["gains"][gdb]
                    need = 3 * nep * Rpk * math.sqrt(bw)
                    row[f"{gdb} dB: solid fills the field stop"] = t_min_uniform(
                        (lt[0], lt[2], lt[2]), need, math.pi * (PT.FOV_PD_MM * 1e-3 / 2) ** 2, omega)
                    row[f"{gdb} dB: 0.05 mm2 of liquid"] = t_min_uniform((lt[0], lt[1], lt[1]), need, 0.05e-6, omega)
                out[f"{k} | {g}"] = row
    return out


def plume_tables(fields, omega):
    """Plume emission against the pool's, per band: an optically thin plume column (optical depth tau) at T_p over a projected
    area A_p in the field stop, emitting tau x B(T_p) (grey condensate/vapour continuum; lines excluded by the band choice)."""
    out = []
    x, y, T = next(iter(fields.values()))
    X, Y = np.meshgrid(x, y)
    dA = (x[1] - x[0]) * (y[1] - y[0])
    for k in ("PD-A 700/40 (PDA36A2)", "PD-B 900/40 (PDA36A2)", "InGaAs 1550/12, notch dichroic for the DMSP1000 (PDA20CS2)"):
        lam, w = weights(CH[k])
        lt = lut(CH[k], "pass", 0.12)
        fov = np.hypot(X, Y) <= PT.FOV_PD_MM * 1e-3 / 2
        pool = float((signal_map(T, lt) * fov).sum() * dA)
        for Tp in (2000.0, 2700.0, 3360.0):
            for tau in (1e-3, 1e-2, 1e-1):
                Ap = math.pi * (0.15e-3) ** 2                 # a Ø0.3 mm column, seen from above along its length (assumed)
                pl = tau * np.trapezoid(planck(lam / 1000, Tp) * w, lam) * Ap
                out.append(dict(channel=k, T_plume_K=Tp, optical_depth=tau, plume_over_pool=pl / pool))
    return out


def leak_tables(fields, omega, luts, lv):
    """1070 nm reaching each detector. Diffuse: a Lambertian return (reflectance 0.7, a bound) from the spot into the f-theta's
    NA; specular: the cat's-eye bound from beam_path.md (441 W back into the lens at the field centre, R 0.9). Then the galvo
    (R 0.99 x 2), the DMSP1000's leak at 1070 nm (Thorlabs data) and each channel's own optics at 1070 nm (their data; a bandpass
    filter's out-of-band blocking is PT.FILTER_OD_1070). Compared with the channel's melt-pool signal (photodiodes: whole field
    stop; cameras: the peak pixel at 100 us, the leak spread over the laser spot's image, ~150 px diffuse or ~9 px specular)."""
    out = dict(dmsp1000_T_1070=float(dmsp1000_T(1070.0)), fesh1000_OD_1070=float(interp(PT.FESH1000_OD, 1070.0)),
               filter_OD_1070=PT.FILTER_OD_1070, rows=[])
    x, y, T = next(iter(fields.values()))
    X, Y = np.meshgrid(x, y)
    dA = (x[1] - x[0]) * (y[1] - y[0])
    fov = np.hypot(X, Y) <= PT.FOV_PD_MM * 1e-3 / 2
    for case, P_lens, npx in (("diffuse, reflectance 0.7 (bound), 12 mm pupil", 500 * 0.7 * NA_RETURN["12 mm"] ** 2, 150),
                              ("diffuse, 18 mm pupil", 500 * 0.7 * NA_RETURN["18 mm"] ** 2, 150),
                              ("specular cat's eye at the field centre (bound, beam_path.md)", 441.0, 9)):
        into_branch = P_lens * 0.99 ** 2 * float(dmsp1000_T(1070.0))
        r = dict(case=case, W_into_lens=P_lens, W_into_branch=into_branch, channels={})
        for k, ch in CH.items():
            if "InGaAs" in k:
                continue
            d = PT.DET[ch["det"]]
            t = float(ch["branch"](np.array([1070.0]))[0]) * (10 ** -PT.FILTER_OD_1070 if "/40" in k or "/10" in k else 1.0)
            P = into_branch * t
            if d["kind"] == "photodiode":
                sig = float((signal_map(T, luts[(k, "pass", lv)]) * fov).sum() * dA * omega)
                leak = P * interp(d["resp"], 1070.0)
                r["channels"][k] = dict(W=P, leak_over_signal=leak / sig)
            else:
                qe = float(interp(d["qe"], 1070.0))
                e_px = P * qe / (H * C / 1.07e-6) / npx * 100e-6
                peak = float(np.max(signal_map(T, luts[(k, "pass", lv)]))) * (8e-6) ** 2 * omega * 100e-6
                r["channels"][k] = dict(W=P, e_per_px_100us=e_px, leak_over_peak_pixel=e_px / peak)
        out["rows"].append(r)
    return out


def write_md(R):
    L = ["# Coaxial radiometry (generated by analysis/monitoring/optics/radiometry.py)", "", f"Fields: {R['fields_source']}.", ""]
    L += ["| case | T peak (K) | liquid area (mm2) | liquid length x width (mm) |", "|---|---:|---:|---|"]
    for n, c in R["cases"].items():
        L.append(f"| {n} | {c['T_peak_K']:.0f} | {c['liquid_area_mm2']:.3f} | {c['liquid_length_mm']:.2f} x {c['liquid_width_mm']:.2f} |")
    lv = "0.12 at 1 um (literature midpoint)"
    L += ["", "## Photodiodes: photocurrent and SNR (12 mm pupil, field stop Ø%.1f mm on the plate, liquid emissivity %s)" % (PT.FOV_PD_MM, lv), "",
          "| case | channel | galvo | photocurrent | 40 dB (150 kHz): V, SNR | 20 dB (1 MHz): V, SNR | 60 dB (11 kHz): V, SNR |", "|---|---|---|---:|---|---|---|"]
    for n, c in R["cases"].items():
        for k, rec in c["channels"].items():
            if "PD" not in k and "InGaAs" not in k:
                continue
            for g in ("pass", "Kozjek"):
                q = rec[f"{g} | {lv}"]
                gg = q["gains"]
                L.append(f"| {n} | {k} | {g} | {q['photocurrent_A'] * 1e9:.1f} nA | {gg[40]['V']:.3g} V, {gg[40]['snr']:.0f}{' SAT' if gg[40]['saturated'] else ''} | "
                         f"{gg[20]['V']:.3g} V, {gg[20]['snr']:.0f} | {gg[60]['V']:.3g} V, {gg[60]['snr']:.0f}{' SAT' if gg[60]['saturated'] else ''} |")
    L += ["", "## Cameras: peak pixel at 8 um/px (12 mm pupil)", "",
          "| case | channel | galvo | peak e-/s | full well in (us) | 10 us: peak e-, SNR, mm2 at SNR>=3 | 100 us | 500 us |", "|---|---|---|---:|---:|---|---|---|"]
    for n, c in R["cases"].items():
        for k, rec in c["channels"].items():
            if "camera" not in k:
                continue
            for g in ("pass", "Kozjek"):
                q = rec[f"{g} | {lv}"]
                e = q["exposures"]
                f = lambda t: f"{e[t]['peak_e']:.0f}, {e[t]['peak_snr']:.0f}, {e[t]['area_snr3_mm2']:.3f}{' SAT' if e[t]['saturated'] else ''}"
                L.append(f"| {n} | {k} | {g} | {q['peak_rate_e_per_s']:.3g} | {q['t_sat_us']:.0f} | {f(10)} | {f(100)} | {f(500)} |")
    L += ["", "## Two-colour (700/40 over 900/40 nm, photodiodes)", "", "| case | galvo | emissivity | ratio T (K) | T peak (K) |", "|---|---|---|---:|---:|"]
    for n, c in R["cases"].items():
        for kk, v in c["two_colour"].items():
            g, lvv = kk.split(" | ")
            L.append(f"| {n} | {g} | {lvv} | {v['T_ratio_K']:.0f} | {c['T_peak_K']:.0f} |")
    tc = R["two_colour"]
    L += ["", "| T (K) | dlnR/dT (1/K) | dT for a 1 % ratio error (K) |", "|---:|---:|---:|"]
    L += [f"| {s['T_K']:.0f} | {s['dlnR_per_K']:.2e} | {s['dT_for_1pct_ratio_K']:.1f} |" for s in tc["sensitivity"]]
    L += ["", "| T (K) | Drude eps700/eps950 | error, Drude (K) | +5 % | -5 % | +10 % | -10 % |", "|---:|---:|---:|---:|---:|---:|---:|"]
    L += [f"| {r['T_K']:.0f} | {r['drude_eps700_over_eps950']:.3f} | {r['Drude']:+.0f} | {r['+5 %']:+.0f} | {r['-5 %']:+.0f} | {r['+10 %']:+.0f} | {r['-10 %']:+.0f} |" for r in tc["non_grey"]]
    L += ["", "Error at 2000 K for a 5 % emissivity difference, by band pair: " + "; ".join(f"{k}: {v:.0f} K" for k, v in tc["pairs_error_K_at_2000K_for_5pct"].items()), ""]
    L += ["## Lowest temperature seen (SNR 3)", ""]
    keys_cam = [k for k in R["t_min"] if "camera" in k]
    keys_pd = [k for k in R["t_min"] if "camera" not in k]
    if keys_cam:
        cols = list(R["t_min"][keys_cam[0]].keys())
        L += ["| camera pixel, uniform liquid/solid | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
        L += [f"| {k} | " + " | ".join(f"{(R['t_min'][k][c] or float('nan')):.0f} K" for c in cols) + " |" for k in keys_cam]
    if keys_pd:
        cols = list(R["t_min"][keys_pd[0]].keys())
        L += ["", "| photodiode | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
        L += [f"| {k} | " + " | ".join(("%.0f K" % R['t_min'][k][c]) if R['t_min'][k][c] else "-" for c in cols) + " |" for k in keys_pd]
    L += ["", "## Plume emission against the pool (field stop Ø%.1f mm)" % PT.FOV_PD_MM, "", "| channel | T plume (K) | optical depth | plume / pool |", "|---|---:|---:|---:|"]
    L += [f"| {r['channel']} | {r['T_plume_K']:.0f} | {r['optical_depth']:g} | {r['plume_over_pool']:.3g} |" for r in R["plume"]]
    lk = R["leak_1070"]
    L += ["", f"## 1070 nm reaching each channel (DMSP1000 T at 1070 nm = {lk['dmsp1000_T_1070']:.2g}, OD {-math.log10(lk['dmsp1000_T_1070']):.1f}; "
          f"FESH1000 OD {lk['fesh1000_OD_1070']:.1f}; bandpass out-of-band OD {lk['filter_OD_1070']})", "",
          "| case | W into the lens | W into the branch | " + " | ".join(next(iter(lk["rows"]))["channels"]) + " |",
          "|---|---:|---:|" + "---:|" * len(next(iter(lk["rows"]))["channels"])]
    for r in lk["rows"]:
        cells = []
        for k, v in r["channels"].items():
            cells.append(f"{v['leak_over_signal']:.1e} of signal" if "leak_over_signal" in v else f"{v['leak_over_peak_pixel']:.1e} of peak px")
        L.append(f"| {r['case']} | {r['W_into_lens']:.3g} | {r['W_into_branch']:.3g} | " + " | ".join(cells) + " |")
    (OUT / "radiometry.md").write_text("\n".join(L) + "\n")


def plot(R, fields, luts, lv):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.3))
    name, (x, y, T) = next(iter(fields.items()))
    im = ax[0].imshow(T, extent=[x[0] * 1e3, x[-1] * 1e3, y[0] * 1e3, y[-1] * 1e3], origin="lower", cmap="inferno", aspect="equal")
    ax[0].contour(x * 1e3, y * 1e3, T, levels=[T_LIQ], colors="c", linewidths=0.8)
    th = np.linspace(0, 2 * np.pi, 100)
    ax[0].plot(PT.FOV_PD_MM / 2 * np.cos(th), PT.FOV_PD_MM / 2 * np.sin(th), "w--", lw=0.8)
    ax[0].set_title(f"{name}: surface T (K); cyan = liquidus; dashed = PD field stop", fontsize=9)
    ax[0].set_xlabel("x (mm), beam at 0 moving +x")
    fig.colorbar(im, ax=ax[0], shrink=0.8)
    Ts = np.linspace(700, T_BOIL, 300)
    omega = math.pi * NA_RETURN["12 mm"] ** 2
    for k, c in (("camera 955-990 (IMX296)", "#d62728"), ("alt: camera 850/10, 50:50 plate (IMX296)", "#ff7f0e"), ("alt: camera 700/10, 50:50 plate (IMX296)", "#1f77b4")):
        lt = luts[(k, "pass", lv)]
        s = np.interp(Ts, lt[0], lt[1]) * (8e-6) ** 2 * omega * 100e-6
        ax[1].semilogy(Ts, s, color=c, label=k.replace(" (IMX296)", "").replace("alt: ", "") + ", liquid, 100 us")
        lt2 = luts[(k, "Kozjek", lv)]
        if "850/10" in k:
            ax[1].semilogy(Ts, np.interp(Ts, lt2[0], lt2[1]) * (8e-6) ** 2 * omega * 100e-6, ":", color=c, label="850/10 if the galvo blocks 750-875 nm")
    d = PT.DET["IMX296 mono"]
    ax[1].axhline(d["fwc_e"], color="k", lw=0.8)
    ax[1].text(800, d["fwc_e"] * 1.2, "full well", fontsize=8)
    ax[1].axhline(12.7, color="0.4", lw=0.8, ls="--")
    ax[1].text(800, 15, "SNR 3", fontsize=8)
    ax[1].axvline(T_LIQ, color="c", lw=0.8)
    ax[1].set_ylim(1e-1, 1e6)
    ax[1].set_xlabel("uniform temperature (K)")
    ax[1].set_ylabel("electrons per 8 um pixel in 100 us")
    ax[1].set_title("IMX296 pixel signal through the coaxial path (liquid eps 0.12 at 1 um)", fontsize=9)
    ax[1].legend(fontsize=7)
    ax[1].grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(OUT / "radiometry.png", dpi=130)


if __name__ == "__main__":
    main()
