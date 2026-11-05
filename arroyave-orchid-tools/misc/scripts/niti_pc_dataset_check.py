"""Check Phase-Compatibility-Model-NiTi's Lambda2Model rule against its own data.csv, and measure
how far HEACalculator 2.x's delta drifts from the 'Delta' column stored in data.csv (made with 1.x).

Usage: python -I niti_pc_dataset_check.py <repo copy dir> <out_dir>
"""
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo))
from helper import Lambda2Model  # noqa: E402
from HEACalculator import HEACalculator  # noqa: E402

df = pd.read_csv(repo / "data.csv")
print("rows:", len(df), "| Transformation labels:", df["Transformation"].value_counts(dropna=False).to_dict())

# rule from Lambda2Model.determine_type_and_lambda, applied to the dataset's own feature column
pred = df["avg_first_ion_en_divi_voro_coord"].apply(lambda x: Lambda2Model.determine_type_and_lambda(x))
df["pred_type"] = [p[0] for p in pred]
df["pred_lambda2"] = [p[1] for p in pred]
lab = df["Transformation"].astype(str).str.replace("prime", "'", regex=False)
m = lab.isin(["B19", "B19'"])
acc = float((df.loc[m, "pred_type"] == lab[m]).mean())
print(f"type accuracy on labelled rows: {acc:.3f} (n={int(m.sum())})")
print(pd.crosstab(lab[m], df.loc[m, "pred_type"], rownames=["label"], colnames=["predicted"]))
l2 = pd.to_numeric(df["lambda2_combined"], errors="coerce")
mm = l2.notna()
mae = float((df.loc[mm, "pred_lambda2"] - l2[mm]).abs().mean())
print(f"lambda2 MAE vs lambda2_combined: {mae:.4f} (n={int(mm.sum())})")

# HEACalculator 2.x delta vs stored Delta (1.x)
d2 = []
for f in df["composition"]:
    try:
        d2.append(HEACalculator(f).get_dict()["delta"])
    except Exception:
        d2.append(np.nan)
df["delta_heacalc_2x"] = d2
diff = df["delta_heacalc_2x"] - pd.to_numeric(df["Delta"], errors="coerce")
print(f"delta(2.x) - Delta(stored): mean {diff.mean():+.3f}, min {diff.min():+.3f}, max {diff.max():+.3f} (percentage points), n={int(diff.notna().sum())}")
r = float(np.corrcoef(df["delta_heacalc_2x"][diff.notna()], pd.to_numeric(df["Delta"], errors="coerce")[diff.notna()])[0, 1])
print(f"Pearson r between the two: {r:.4f}")
json.dump({"n_rows": len(df), "type_accuracy": acc, "n_typed": int(m.sum()), "lambda2_MAE": mae, "n_lambda2": int(mm.sum()),
           "delta_drift_mean_pp": float(diff.mean()), "delta_drift_min_pp": float(diff.min()), "delta_drift_max_pp": float(diff.max()),
           "delta_corr": r}, open(out / "niti_phase_compat_dataset_check.json", "w"), indent=2)
