#!/usr/bin/env python3
"""Render placeholder tiles for PSD and ICP-MS (powder QC).

These are intentionally marked "[placeholder]" to be replaced with
real Malvern Mastersizer PSD and Agilent ICP-MS data once the
in-house instruments are commissioned.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = Path(__file__).parent

# ---------------- PSD placeholder ----------------
def render_psd():
    fig, ax = plt.subplots(figsize=(3.4, 2.4), dpi=200)
    rng = np.random.default_rng(7)
    # Synthetic log-normal PSD around 35 µm (typical AlSi10Mg LPBF feedstock).
    mu, sigma = np.log(35), 0.30
    bins = np.geomspace(5, 200, 32)
    centers = np.sqrt(bins[:-1] * bins[1:])
    pdf = (1 / (centers * sigma * np.sqrt(2 * np.pi))) * \
          np.exp(-((np.log(centers) - mu) ** 2) / (2 * sigma ** 2))
    pdf = pdf / pdf.max() * 100
    pdf_noisy = pdf * (1 + 0.10 * rng.standard_normal(pdf.shape))
    ax.bar(centers, pdf_noisy, width=np.diff(bins), align='center',
           color='#5B8DCB', edgecolor='#274472', linewidth=0.4)
    ax.plot(centers, pdf, '-', color='#C0392B', lw=1.6, label='log-normal fit')
    # D10/D50/D90 indicators
    for d, lbl in [(20, 'D10'), (35, 'D50'), (60, 'D90')]:
        ax.axvline(d, color='#666', ls='--', lw=0.6)
        ax.text(d, 105, lbl, ha='center', fontsize=7, color='#444')
    ax.set_xscale('log')
    ax.set_xlim(8, 180)
    ax.set_ylim(0, 120)
    ax.set_xlabel('Particle size (µm)', fontsize=8)
    ax.set_ylabel('Volume %', fontsize=8)
    ax.set_title('PSD — Malvern Mastersizer', fontsize=9)
    ax.tick_params(labelsize=7)
    ax.legend(loc='upper right', fontsize=6.5, frameon=False)
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / 'psd-placeholder.png', dpi=200,
                facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print(f"[C-PSD] saved psd-placeholder.png")


# ---------------- ICP-MS placeholder ----------------
def render_icp():
    fig, ax = plt.subplots(figsize=(3.4, 2.4), dpi=200)
    elements = ['Al', 'Si', 'Mg', 'Fe', 'Cu', 'Mn', 'Zn']
    nominal  = [88.5, 9.5, 0.45, 0.30, 0.05, 0.10, 0.08]
    measured = [88.7, 9.42, 0.47, 0.31, 0.052, 0.095, 0.082]
    err      = [0.20, 0.08, 0.02, 0.015, 0.005, 0.008, 0.006]
    x = np.arange(len(elements))
    w = 0.38
    ax.bar(x - w/2, nominal, w, color='#BBBBBB', edgecolor='#666',
           linewidth=0.4, label='Nominal')
    ax.bar(x + w/2, measured, w, yerr=err, color='#5BAE6A',
           edgecolor='#22663A', linewidth=0.4, capsize=2.5,
           ecolor='#222', label='ICP-MS measured')
    ax.set_yscale('log')
    ax.set_ylim(0.01, 200)
    ax.set_xticks(x)
    ax.set_xticklabels(elements, fontsize=8)
    ax.set_ylabel('wt %', fontsize=8)
    ax.set_title('ICP-MS composition — Agilent 8900', fontsize=9)
    ax.tick_params(labelsize=7)
    ax.legend(loc='upper right', fontsize=6.5, frameon=False)
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / 'icp-ms-placeholder.png', dpi=200,
                facecolor='white', bbox_inches='tight')
    plt.close(fig)
    print(f"[C-ICP] saved icp-ms-placeholder.png")


if __name__ == "__main__":
    render_psd()
    render_icp()
