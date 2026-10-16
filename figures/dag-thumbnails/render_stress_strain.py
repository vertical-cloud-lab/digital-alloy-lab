#!/usr/bin/env python3
"""Generate a small stress-strain curve PNG used as the ch4 (tensile)
node thumbnail in Fig. 1 DAG. Shows a representative engineering stress-
strain response for an LPBF-fabricated Al alloy with both a baseline
(AlSi10Mg-like) and a higher-strength FLAIME-target curve for visual
context.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "stress_strain.png"


def stress_strain(eps, E=70.0e3, sy=250.0, suts=350.0, eps_uts=0.06, eps_f=0.10):
    """Synthetic engineering stress-strain (MPa).
    Linear elastic to yield, smooth saturating hardening to UTS, then
    linear softening (necking) to fracture. Returns NaN past eps_f.
    """
    eps = np.asarray(eps, dtype=float)
    ey = sy / E
    # Hardening rate chosen so curve smoothly reaches ~suts at eps_uts.
    k = 5.0 / max(eps_uts - ey, 1e-6)
    plastic = sy + (suts - sy) * (1.0 - np.exp(-k * np.maximum(eps - ey, 0.0)))
    sigma = np.where(eps <= ey, E * eps, plastic)
    # Necking: linear drop from UTS to ~0.6*suts at fracture
    drop = (suts - 0.6 * suts) * np.maximum(eps - eps_uts, 0.0) / max(eps_f - eps_uts, 1e-6)
    sigma = np.where(eps > eps_uts, suts - drop, sigma)
    sigma = np.where(eps > eps_f, np.nan, sigma)
    return sigma


def main():
    eps = np.linspace(0, 0.13, 800)
    base   = stress_strain(eps, E=70e3, sy=240, suts=330, eps_uts=0.045, eps_f=0.085)
    flaime = stress_strain(eps, E=72e3, sy=360, suts=470, eps_uts=0.060, eps_f=0.105)

    fig, ax = plt.subplots(figsize=(3.0, 2.2))
    ax.plot(eps * 100, base,  color="#888888", linewidth=1.6,
            label="LPBF AlSi10Mg (baseline)")
    ax.plot(eps * 100, flaime, color="#1f77b4", linewidth=1.8,
            label="FLAIME target")
    ax.set_xlabel("Engineering strain (%)", fontsize=8)
    ax.set_ylabel("Engineering stress (MPa)", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 520)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=6.5, loc="lower right", frameon=False)
    fig.tight_layout(pad=0.2)
    fig.savefig(OUT, dpi=180, facecolor="white", bbox_inches="tight",
                pad_inches=0.05)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
