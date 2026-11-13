"""Render bom.csv as a markdown table with low/high totals. Run: python desktop-lpbf/bom_table.py"""
import csv, pathlib
rows = list(csv.DictReader(open(pathlib.Path(__file__).with_name("bom.csv"))))
lo = hi = 0.0
print("| ID | Subsystem | Item | Candidate | Qty | Unit (USD) | Basis |")
print("|---|---|---|---|---|---|---|")
for r in rows:
    q = float(r["qty"]); a = float(r["unit_low_usd"]); b = float(r["unit_high_usd"])
    lo += q * a; hi += q * b
    unit = f"{a:,.0f}" if a == b else f"{a:,.0f}–{b:,.0f}"
    print(f"| {r['id']} | {r['subsystem']} | {r['item']} | {r['candidate']} | {r['qty']} | {unit} | {r['price_basis']} |")
print(f"\n**Total: ${lo:,.0f} – ${hi:,.0f}** (low = cheapest listed option for every line; high = premium option)")
