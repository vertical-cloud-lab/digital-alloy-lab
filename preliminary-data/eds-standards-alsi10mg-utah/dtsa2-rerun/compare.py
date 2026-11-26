"""Compare the headless DTSA-II re-run with the student's DTSA-II results, and summarize.

Reads ../dtsa2-results.csv (transcribed from the student's reports) and the CSVs that
RerunDTSA2.java wrote here. Writes comparison.csv and prints the tables in README.md.
Standard library only.  Run:  python3 compare.py   (run.sh calls it)
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ELMS = ["O", "Mg", "Al", "Si"]


def rows(path):
    return {r["run"]: r for r in csv.DictReader(open(path, newline=""))}


student = rows(HERE.parent / "dtsa2-results.csv")
entered = rows(HERE / "as-entered.csv")
mgo = rows(HERE / "mgo.csv")
broad = rows(HERE / "broadened.csv")

# 1. Does the re-run reproduce the student's numbers?
out, worst = [], {"sum": 0.0, **{e: 0.0 for e in ELMS}}
for run, s in student.items():
    r = entered[run]
    row = {"run": run, "beam_kV": r["beam_kV"], "mg_standard_entered_as": r["mg_standard_entered_as"]}
    d = float(r["analytical_sum"]) - float(s["analytical_sum"])
    worst["sum"] = max(worst["sum"], abs(d))
    row.update(sum_student=s["analytical_sum"], sum_rerun=r["analytical_sum"], sum_diff=f"{d:+.4f}")
    for e in ELMS:
        d = float(r[f"{e}_wt_norm"]) - float(s[f"{e}_wt"])
        worst[e] = max(worst[e], abs(d))
        row.update({f"{e}_student": s[f"{e}_wt"], f"{e}_rerun": f"{float(r[e + '_wt_norm']):.2f}", f"{e}_diff": f"{d:+.3f}"})
    out.append(row)
with open(HERE / "comparison.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print("Re-run vs the student's DTSA-II results (normalized wt %, 2 decimals as reported):")
print("  largest |difference|: " + ", ".join(f"{k} {v:.3f}" for k, v in worst.items()))


def line(label, r):
    return (f"  {label:30s} {r['beam_kV']:>3s} kV  total {float(r['analytical_sum']):.3f}  "
            + "  ".join(f"{e} {float(r[e + '_wt_norm']):6.2f}" for e in ELMS))


# 2. MgO entered as MgO in trials 11 and 14.
print("\nTrials 11 and 14, Mg row entered as pure Mg (student) and as MgO:")
for run in ["trial11_1", "trial14_1"]:
    print(line(run + ", pure Mg", entered[run]))
    print(line(run + ", MgO", mgo[run]))

# 3. The 0.96 us runs against broadened standards.
print("\n0.96 us runs: native standards / standards broadened to 135.5 eV:")
for run, r in broad.items():
    if r["amp_time_us"] != "0.96":
        continue
    print(line(run + ", native", mgo[run]))
    print(line(run + ", broadened", r))

# 4. Checks on sobol_exp_1_1.
print("\nChecks on sobol_exp_1_1:")
print(line("as measured (128 eV detector)", mgo["sobol_exp_1_1"]))
for name in ["unknown-broadened", "both-broadened", "detector-120", "detector-135.5", "detector-145"]:
    for run, r in rows(HERE / "checks" / f"{name}.csv").items():
        print(line(f"{name}: {run}", r))
