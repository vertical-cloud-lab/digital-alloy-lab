"""Back-of-envelope pour numbers for the 27 and 28 Oct 2026 630 bronze (C63000) atomizer runs (#219).

Pressures are taken as gauge (relative to the room) for both the crucible and the chamber, as the
training and the Oct 21 run notes suggest; chamber held at 150 mbar. Inputs are rough; the point is
the ratios between the Oct 27 and Oct 28 settings, not the absolute values.
"""
import math

G = 9.81
RHO = 6900.0        # kg/m3, liquid C63000 near 1300 C (solid 7580 at room temperature)
SIGMA = 1.15        # N/m, liquid Cu-10Al (Cu ~1.30, Al lowers it)
THETA = 140.0       # deg, NAB on hBN, non-wetting
CD = 0.7            # nozzle discharge coefficient
CRUCIBLE_ID = 0.050 # m, assumed for the 225 cm3 crucible
CHAMBER = 0.150     # bar gauge


def head_mbar(mass_g):
    vol = mass_g / 1000 / RHO
    h = vol / (math.pi * CRUCIBLE_ID ** 2 / 4)
    return RHO * G * h / 100, h * 100


def capillary_mbar(bore_mm):
    return 4 * SIGMA * abs(math.cos(math.radians(THETA))) / (bore_mm / 1000) / 100


def flow_gps(p_crucible_bar, mass_g, bore_mm):
    dp = (p_crucible_bar - CHAMBER) * 1000 + head_mbar(mass_g)[0] - capillary_mbar(bore_mm)
    if dp <= 0:
        return 0.0, dp
    v = math.sqrt(2 * dp * 100 / RHO)
    area = math.pi * (bore_mm / 1000) ** 2 / 4
    return CD * area * v * RHO * 1000, dp


def drain_time_s(p_crucible_bar, mass_g, bore_mm, dt=0.5):
    m, t = mass_g, 0.0
    while m > 5 and t < 3600:
        q, _ = flow_gps(p_crucible_bar, m, bore_mm)
        if q == 0:
            return None, m
        m -= q * dt
        t += dt
    return t, m


def capillary_wavelength_um(f_hz, rho=RHO, sigma=SIGMA):
    return (8 * math.pi * sigma / (rho * f_hz ** 2)) ** (1 / 3) * 1e6


if __name__ == "__main__":
    print("## Metallostatic head (crucible ID %.0f mm)" % (CRUCIBLE_ID * 1000))
    for m in (1080, 858, 430):
        hm, hc = head_mbar(m)
        print("  %4d g: melt height %.1f cm, head %.0f mbar" % (m, hc, hm))
    print("\n## Capillary pressure to push NAB into a non-wetting bore")
    for d in (0.5, 0.7, 1.0):
        print("  %.1f mm: %.0f mbar" % (d, capillary_mbar(d)))
    print("\n## Net push and flow at the start of the pour")
    cases = [("Oct 27: graining 0.19 bar, 1080 g", 0.19, 1080), ("Oct 27: turbo 1.5 bar, 1080 g", 1.5, 1080),
             ("Oct 28: graining 0.23 bar, 858 g", 0.23, 858), ("Oct 28: back to 0.19 bar, ~430 g left", 0.19, 430),
             ("Oct 28: turbo 1.5 bar, 858 g", 1.5, 858)]
    for bore in (0.5, 1.0):
        print("  bore %.1f mm" % bore)
        for label, p, m in cases:
            q, dp = flow_gps(p, m, bore)
            print("    %-40s net %+5.0f mbar  flow %.1f g/s" % (label, dp, q))
    print("\n## Time to drain the charge at a fixed setting (stops when the net push reaches zero)")
    for bore in (0.5, 1.0):
        for label, p, m in [("0.23 bar, 858 g", 0.23, 858), ("0.19 bar, 1080 g", 0.19, 1080), ("turbo 1.5 bar, 858 g", 1.5, 858)]:
            t, left = drain_time_s(p, m, bore)
            print("  bore %.1f mm, %-22s %s" % (bore, label, ("%.0f s" % t) if t else "stops with %.0f g left" % left))
    print("\n## Capillary wavelength and Lang d50 = 0.34 lambda at 40 kHz")
    for name, rho, sig in (("C63000", RHO, SIGMA), ("aluminium", 2375.0, 0.87)):
        lam = capillary_wavelength_um(40e3, rho, sig)
        print("  %-10s lambda %.0f um, d50 %.0f um" % (name, lam, 0.34 * lam))
    print("\n## Argon: cylinder pressure %d -> %d psi in one run = %d psi (training notes: 100-160 psi per run)"
          % (1500, 1150, 350))


def bore_for_drain_time(p_bar, mass_g, target_s):
    lo, hi = 0.2, 2.0
    for _ in range(40):
        mid = (lo + hi) / 2
        t, _left = drain_time_s(p_bar, mass_g, mid)
        if t is None or t > target_s:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def report_observed():
    print("\n## Observed pours (display 'Min. Grain' and narration)")
    obs = [("Oct 27, turbo held (1.48 bar on the display at 2.6 and 3.5 min)", 1080, 3.5 * 60),
           ("Oct 28, graining (0.30 bar on the display at 0.8 min; notes say 0.23)", 858, 47 * 60 + 3, )]
    print("  Oct 27: 1080 g in ~3.5 min = %.1f g/s average" % (1080 / 210))
    print("  Oct 28:  858 g in ~3.7 min = %.1f g/s average (if it all drained)" % (858 / 223))
    for p in (0.23, 0.30):
        print("  Oct 28 at %.2f bar: a non-wetting bore of ~%.2f mm drains 858 g in 223 s" % (p, bore_for_drain_time(p, 858, 223)))
    print("  Oct 27 at 1.48 bar: a non-wetting bore of ~%.2f mm drains 1080 g in 210 s" % bore_for_drain_time(1.48, 1080, 210))
    for label, p, bore in (("Oct 27, 1.48 bar", 1.48, 0.5), ("Oct 28, 0.30 bar", 0.30, 0.5), ("Oct 28, 0.23 bar", 0.23, 0.5)):
        dp = (p - CHAMBER) * 1000 - capillary_mbar(bore)
        print("  jet speed leaving a %.1f mm bore, %s: %.1f m/s" % (bore, label, math.sqrt(2 * max(dp, 0) * 100 / RHO)))


if __name__ == "__main__":
    report_observed()
