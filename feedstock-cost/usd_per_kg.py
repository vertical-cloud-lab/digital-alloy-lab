"""USD/kg for feedstock list prices: reads prices.csv, computes mass from pack size or geometry, prints a table.

Columns: element,alloy,form,vendor,product,purity,diameter_mm,length_m,pack_kg,price_usd,source,date
Mass is pack_kg when given; otherwise pi/4 * d^2 * L * density for wire and rod.
"""
import csv, math, sys
RHO = dict(Al=2.70, Cu=8.96, Ni=8.908, Mg=1.738, Si=2.329, Zn=7.14, Mn=7.21, Fe=7.874, Sn=7.287, Ti=4.506,
           Zr=6.52, Cr=7.19, Sc=2.985, Ce=6.77)
ALLOY_RHO = {"6061": 2.70, "C11000": 8.94, "C95400": 7.45, "C95500": 7.53, "ER1100": 2.71, "ER4043": 2.68,
             "ER4047": 2.66, "ERCu": 8.9, "ERCuNiAl": 7.6, "ERCuAl-A3": 7.5, "ERCuSi-A": 8.5}

def mass_kg(r):
    if r["pack_kg"]:
        return float(r["pack_kg"])
    d_cm = float(r["diameter_mm"]) / 10
    L_cm = float(r["length_m"]) * 100
    rho = ALLOY_RHO.get(r["alloy"]) or RHO[r["element"]]
    return math.pi / 4 * d_cm ** 2 * L_cm * rho / 1000

def rows(path):
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            m = mass_kg(r)
            r["mass_kg"] = m
            r["usd_per_kg"] = float(r["price_usd"]) / m
            yield r

if __name__ == "__main__":
    for r in rows(sys.argv[1] if len(sys.argv) > 1 else str(__import__("pathlib").Path(__file__).with_name("prices.csv"))):
        print(f'{r["element"]:3} {r["form"]:8} {r["vendor"][:14]:14} {r["product"][:60]:60} '
              f'{r["mass_kg"]*1000:9.1f} g  ${float(r["price_usd"]):9,.2f}  ${r["usd_per_kg"]:10,.0f}/kg')
