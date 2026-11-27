"""Run ArroyaveLab/microseg_lab's full run_segmentation (classical -> SAM2 round) on CPU,
no LLM, with the SAM2.1 *tiny* checkpoint and a reduced mask budget.

Env (set by the caller): SAM2_ROOT=<sam2 clone>/sam2, SAM2_CKPT=<.../sam2.1_hiera_tiny.pt>,
SAM2_CFG=<sam2 clone>/sam2/configs/sam2.1/sam2.1_hiera_t.yaml

Usage: python -I microseg_sam2_cpu.py <repo_copy_dir> <out_dir> <image> [<mask>]
"""
import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402
import torch  # noqa: E402

torch.set_num_threads(2)
repo, out, img_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
mask_path = sys.argv[4] if len(sys.argv) > 4 else None
sys.path.insert(0, str(repo.resolve()))
out.mkdir(parents=True, exist_ok=True)

from PIL import Image  # noqa: E402

from src import pipeline as P  # noqa: E402
from src.config import AppConfig  # noqa: E402
from src.image_io import load_image_any  # noqa: E402
from src.state import RunSettings  # noqa: E402

cfg = AppConfig()
print("device:", cfg.device(), "| sam2 cfg:", cfg.sam2_paths.config.name, "| ckpt:", cfg.sam2_paths.checkpoint.name, flush=True)
# fast_mode -> 1 SAM round, single-mask output, proposal cap 400; runtime_budget=3 -> at most 120 SAM masks
settings = RunSettings(use_llm=False, use_reviewer=False, use_human_loop=False, fast_mode=True, runtime_budget=3.0)
img = load_image_any(img_path)
t0 = time.time()
res = P.run_segmentation(img, cfg.sam2_paths, settings)
dt = time.time() - t0
summ = {"seconds_total": round(dt, 1), "stages": []}
for h in res["history"]:
    s = h["summary"]
    summ["stages"].append({k: s.get(k) for k in ("stage", "round", "num_proposals", "num_candidate_masks", "num_instances_selected", "union_area_frac")}
                          | {"top_scores": [round(x, 3) for x in s.get("top_scores", [])[:5]]})
u = res["union_mask_u8"] > 0
summ["final_union_area_frac"] = float(u.mean())
summ["final_num_selected"] = len(res["selected"])
if mask_path:
    m = np.array(Image.open(mask_path).convert("L"))
    for pol, ref in (("mask>127", m > 127), ("mask<=127", m <= 127)):
        summ[f"IoU_vs_bundled_mask ({pol})"] = round(float(np.logical_and(u, ref).sum() / (np.logical_or(u, ref).sum() + 1e-9)), 3)
print(json.dumps(summ, indent=1), flush=True)
(out / "microseg_sam2_tiny_cpu_summary.json").write_text(json.dumps(summ, indent=2))
panel = np.concatenate([res["rgb_u8"], res["overlay_union_rgb_u8"], res["history"][-1]["overlay_instances"]], axis=1)
Image.fromarray(panel).save(out / f"microseg_sam2_tiny_cpu_{Path(img_path).stem}.png", optimize=True)
