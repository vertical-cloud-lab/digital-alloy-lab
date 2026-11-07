"""Headless driver for the classical (no-SAM, no-LLM) path of ArroyaveLab/microseg_lab.

Usage: python -I microseg_classical.py <repo_copy_dir> <out_dir> <image> [<image> ...] [--mask <mask>]

It (1) checks whether pipeline.run_segmentation can run without SAM2 (it can't: it builds
SAM2Wrapper unconditionally), then (2) runs the classical stage by calling the repo's own
functions in the same order run_segmentation does, with fallback_plan() (what the app uses
when there is no OpenAI key / use_llm=False).
"""
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import sys
import time
from pathlib import Path

import numpy as np

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
args = sys.argv[3:]
mask_path = None
if "--mask" in args:
    i = args.index("--mask")
    mask_path = args[i + 1]
    args = args[:i] + args[i + 2:]
images = args
sys.path.insert(0, str(repo))
out.mkdir(parents=True, exist_ok=True)

from PIL import Image  # noqa: E402

from src import pipeline as P  # noqa: E402
from src.config import AppConfig  # noqa: E402
from src.image_io import load_image_any, maybe_downsample  # noqa: E402
from src.llm_agent import fallback_plan  # noqa: E402
from src.modules import sanitize_plan  # noqa: E402
from src.state import RunSettings  # noqa: E402

results = {}

# (1) Does the public entry point run without SAM2?
cfg = AppConfig()
settings = RunSettings(use_llm=False, use_reviewer=False, use_human_loop=False)
img0 = load_image_any(images[0])
try:
    P.run_segmentation(img0, cfg.sam2_paths, settings)
    results["run_segmentation_without_sam2"] = "ran"
except Exception as e:  # expected: SAM2 root not found
    results["run_segmentation_without_sam2"] = f"{type(e).__name__}: {e}"
print("run_segmentation without SAM2 ->", results["run_segmentation_without_sam2"], flush=True)


def classical(image_rgb, downsample_max=1024):
    t0 = time.time()
    img, scale = maybe_downsample(image_rgb, downsample_max)
    gray_u8 = P.preprocess_micrograph(img, clahe=True, denoise=True)
    rgb_u8 = P.ensure_rgb_uint8(gray_u8)
    plan = sanitize_plan(fallback_plan())
    cands = P.run_classical_stage(gray_u8, plan)
    cands.sort(key=lambda c: c.total, reverse=True)
    by_t = P.group_cands_by_target(cands)
    sel_by_t = P.select_per_target(by_t, plan)
    sel = [c for lst in sel_by_t.values() for c in lst]
    unions = P.union_by_target(sel_by_t, gray_u8)
    union = P.union_mask(list(unions.values())) if unions else np.zeros_like(gray_u8, dtype=np.uint8)
    good = P.classical_good_enough(sel, union, settings)
    overlay = P.draw_boundary(P.overlay_mask_rgb(rgb_u8, union, alpha=0.35), union)
    inst = P.overlay_instances(rgb_u8, [c.mask_u8 for c in sel[:35]], alpha=0.30, seed=0)
    dt = time.time() - t0
    summ = {
        "input_shape": list(image_rgb.shape),
        "processed_shape": list(gray_u8.shape),
        "downsample_scale": float(scale),
        "targets": [t.get("name") for t in plan["targets"]],
        "modules": sorted({m.get("module") if isinstance(m, dict) else str(m) for t in plan["targets"] for m in t.get("suggest_modules", [])}),
        "num_candidates": len(cands),
        "num_selected": len(sel),
        "selected_by_target": {k: len(v) for k, v in sel_by_t.items()},
        "union_area_frac": float((union > 0).mean()),
        "top_scores": [round(float(c.total), 3) for c in sel[:5]],
        "classical_good_enough (would skip SAM)": bool(good),
        "seconds": round(dt, 2),
    }
    return summ, union, overlay, inst


for f in images:
    name = Path(f).stem
    img = load_image_any(f)
    summ, union, overlay, inst = classical(img)
    if mask_path and name in Path(mask_path).stem:
        m = np.array(Image.open(mask_path).convert("L"))
        if m.shape != union.shape:
            m = np.array(Image.fromarray(m).resize(union.shape[::-1], Image.NEAREST))
        for pol, ref in (("mask>127", m > 127), ("mask<=127", m <= 127)):
            u = union > 0
            inter = np.logical_and(u, ref).sum()
            iou = inter / (np.logical_or(u, ref).sum() + 1e-9)
            summ[f"IoU_vs_bundled_mask ({pol}, frac={ref.mean():.3f})"] = round(float(iou), 3)
    results[name] = summ
    print(name, json.dumps(summ), flush=True)
    panel = np.concatenate([P.ensure_rgb_uint8(P.preprocess_micrograph(maybe_downsample(img, 1024)[0])), overlay, inst], axis=1)
    im = Image.fromarray(panel)
    if im.width > 1800:
        im = im.resize((1800, int(im.height * 1800 / im.width)))
    im.save(out / f"microseg_classical_{name}.png", optimize=True)

(out / "microseg_classical_summary.json").write_text(json.dumps(results, indent=2))
