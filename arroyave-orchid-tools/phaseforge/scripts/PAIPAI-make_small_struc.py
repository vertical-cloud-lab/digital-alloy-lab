"""Write a small PAIPAI input (struc.in format of example/struc.in) for a CPU smoke test.

example/struc.in: 5x5x5 conventional BCC cells (a = 3.3 A), 250 metal sites
(Nb113 Ta63 Ti37 Hf37), 375 octahedral (face-centre) interstitial sites, B2 O2.
This writes the same layout for n x n x n cells, e.g. n = 2: 16 metal sites
(Nb7 Ta4 Ti3 Hf2), 24 interstitial sites, B1 O1 -> 18 atoms.
Usage: python PAIPAI-make_small_struc.py <out> [n]
"""
import sys

out = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
a = 3.3
metal = []
inter = []
for i in range(n):
    for j in range(n):
        for k in range(n):
            metal.append((i / n, j / n, k / n))
            metal.append(((i + 0.5) / n, (j + 0.5) / n, (k + 0.5) / n))
            inter.append((i / n, (j + 0.5) / n, (k + 0.5) / n))
            inter.append(((i + 0.5) / n, j / n, (k + 0.5) / n))
            inter.append(((i + 0.5) / n, (j + 0.5) / n, k / n))
nm = len(metal)
fr = [113 / 250, 63 / 250, 37 / 250, 37 / 250]
counts = [round(f * nm) for f in fr]
counts[0] += nm - sum(counts)
L = n * a
lines = ["BCC", "1.0",
         f"   {L:.10f}   0.0000000000   0.0000000000",
         f"   0.0000000000   {L:.10f}   0.0000000000",
         f"   0.0000000000   0.0000000000   {L:.10f}",
         "Nb Ta Ti Hf", " ".join(map(str, counts)), "B O", "1 1", str(len(inter)), "Shuffle", "Direct"]
lines += [f"   {x:.9f}   {y:.9f}   {z:.9f}" for x, y, z in metal + inter]
open(out, "w").write("\n".join(lines) + "\n")
print(f"wrote {out}: {nm} metal sites {counts}, {len(inter)} interstitial sites, B1 O1")
