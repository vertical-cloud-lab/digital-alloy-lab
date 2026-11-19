"""How hot 500 C is for each alloy family, and how much faster the volatile elements leave the powder bed at 500 C than
at 200 C (issue #260, PR #266; see preheat-and-plates.md).

1. Homologous temperature: the plate set point against each alloy's solidus (ASM Handbook Vol. 2, "Properties of
   Wrought Aluminum and Aluminum Alloys", and ASM data for the others). A powder bed held near its solidus sinters,
   creeps and ages; one held above it melts.
2. Equilibrium vapour pressure of the pure elements Mg, Zn, Li and Al (Alcock, Itkin and Horrigan, "Vapour pressure
   equations for the metallic elements: 298-2500 K", Canadian Metallurgical Quarterly 23 (1984) 309-313):
       log10(p / atm) = A + B / T + C log10(T)          (T in K)
   In an alloy the element's partial pressure is lower by its activity (roughly its mole fraction for Zn in Al, much
   less for Mg), but the ratio between 500 C and 200 C is what matters here.

Run: python desktop-lpbf/preheat_500.py
"""
import math

ATM = 101325.0

# element: [(T_max_K, A, B, C), ...] in order of temperature range (solid, then liquid)
ALCOCK = {
    "Mg": [(923.0, 8.489, -7813.0, -0.8253)],                 # solid, 298 K to the melting point
    "Zn": [(692.7, 6.102, -6776.0, 0.0), (1000.0, 5.378, -6286.0, 0.0)],
    "Li": [(453.7, 5.667, -8310.0, 0.0), (1000.0, 5.055, -8023.0, 0.0)],
    "Al": [(933.5, 9.459, -17342.0, -0.7927)],
}

# alloy: (solidus C, note)
SOLIDUS = {
    "7075": (477.0, "ASM; 7xxx: Zn, Mg, Cu"),
    "2024": (502.0, "ASM; 2xxx: Cu, Mg"),
    "AlSi10Mg": (557.0, "approx.; Al-Si eutectic 577 C, lowered by Mg"),
    "5083": (574.0, "ASM"),
    "6061": (582.0, "ASM; solution treatment 530 C"),
    "Ti-6Al-4V": (1604.0, "approx.; beta transus ~995 C"),
    "H13 tool steel": (1315.0, "approx."),
}


def p_vap(el, T_c):
    T = T_c + 273.15
    for t_max, A, B, C in ALCOCK[el]:
        if T <= t_max:
            break
    lg = A + B / T + (C * math.log10(T) if C else 0.0)
    return ATM * 10 ** lg


def main():
    print("Set point against the solidus (T / T_solidus in kelvin):")
    print(f"  {'alloy':16s} {'solidus':>8s} {'200 C':>7s} {'400 C':>7s} {'500 C':>7s}   note")
    for a, (ts, note) in SOLIDUS.items():
        r = [(t + 273.15) / (ts + 273.15) for t in (200.0, 400.0, 500.0)]
        flag = "  <- 500 C is above the solidus" if ts < 500 else ""
        print(f"  {a:16s} {ts:7.0f}C {r[0]:7.2f} {r[1]:7.2f} {r[2]:7.2f}   {note}{flag}")
    print("\nEquilibrium vapour pressure of the pure element (Pa) and the rise from 200 C to 500 C:")
    print(f"  {'el':3s} {'25 C':>10s} {'200 C':>10s} {'400 C':>10s} {'500 C':>10s} {'x(500/200)':>12s}")
    for el in ALCOCK:
        p = [p_vap(el, t) for t in (25.0, 200.0, 400.0, 500.0)]
        print(f"  {el:3s} " + " ".join(f"{v:10.2e}" for v in p) + f" {p[3] / p[1]:12.2e}")
    # Zn in 7075 (5.6 wt%) and Mg in 6061 (1.0 wt%) as ideal solutions (an upper bound for Mg, which has a negative
    # deviation in Al), for scale
    for el, wt, mw in (("Zn", 5.6, 65.38), ("Mg", 1.0, 24.305)):
        x = (wt / mw) / (wt / mw + (100 - wt) / 26.98)
        print(f"  {el} at {wt} wt% in Al: mole fraction {x:.3f}; ideal partial pressure at 500 C {x * p_vap(el, 500.0):.2g} Pa, "
              f"at 200 C {x * p_vap(el, 200.0):.2g} Pa")


if __name__ == "__main__":
    main()
