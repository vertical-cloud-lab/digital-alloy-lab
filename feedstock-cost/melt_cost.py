"""Feedstock cost of one atomizer charge, by feedstock route (no labour, no shipping or hazmat fees).

Usage: python melt_cost.py

Prices are USD/kg list prices, 2026-11-10. Where each one comes from is in README.md ("Inputs to melt_cost.py").
Master alloys are entered as (USD/kg of master alloy, wt% solute); the carrier metal they bring in is
subtracted from the balance metal.
"""
CHARGES = {
    # name: (charge g, balance element, {element: wt%})
    "Al-3Mn-1Cr-1Zr (FLAIME focus system)": (300, "Al", {"Mn": 3.0, "Cr": 1.0, "Zr": 1.0}),
    "C95800 NAB (Cu-9Al-4.5Ni-4Fe-1.2Mn)": (1000, "Cu", {"Al": 9.0, "Ni": 4.5, "Fe": 4.0, "Mn": 1.2}),
    "C71500 (Cu-30Ni)": (1000, "Cu", {"Ni": 30.0}),
}

ROUTES = {
    # AlloyBot SI Table S1 pellet prices (Kurt J. Lesker evaporation pellets), converted to USD/kg.
    "pellets (AlloyBot SI Table S1)": {
        "Al": 1407, "Cu": 1094, "Mn": 472, "Cr": 362, "Zr": 2055, "Ni": 1774, "Fe": 1422},
    # Balance from bar (6063 rod as bought; C110 rod), additions as lab-grade powder.
    "cups from bar + powders": {
        "Al": 32, "Cu": 34, "Mn": 166, "Cr": 104, "Zr": 252, "Ni": 108, "Fe": 111, "Al_add": 76},
    # Balance from sawn bar, additions as Belmont master alloys (no cup needed).
    "sawn bar + master alloys": {
        "Al": 32, "Cu": 34, "Al_add": 32,
        "Mn@Al": (58, 60), "Cr@Al": (38, 20), "Zr@Al": (60, 10),
        "Ni@Cu": (70, 50), "Fe@Cu": (58, 30), "Mn@Cu": (86, 30)},
}

def cost(charge_g, bal, add, prices):
    total, carrier_g, lines = 0.0, 0.0, []
    for el, wt in add.items():
        g = charge_g * wt / 100
        key = f"{el}@{bal}"
        if key in prices:                       # master alloy
            usd_kg, solute = prices[key]
            m = g / (solute / 100)
            carrier_g += m - g
            total += m / 1000 * usd_kg
        else:                                   # elemental addition
            p = prices.get(f"{el}_add", prices.get(el))
            total += g / 1000 * p
    bal_g = charge_g * (100 - sum(add.values())) / 100 - carrier_g
    total += bal_g / 1000 * prices[bal]
    return total

if __name__ == "__main__":
    for name, (g, bal, add) in CHARGES.items():
        print(f"{name}, {g} g")
        for r, prices in ROUTES.items():
            print(f"    {r:34} ${cost(g, bal, add, prices):8.2f}")
