"""Subfigure D: Minimum Viable Validation Set — v5: unified palette, success criteria."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PALETTE = {
    'screen':    '#4C72B0',  'process':   '#55A868',
    'mech':      '#C44E52',  'qual':      '#8172B2',
    'postproc':  '#CCB974',
}

def create_mvs_figure(save_path=None, return_fig=False):
    p = PALETTE
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.0, 10.5)
    ax.axis('off')

    ax.text(5, 10.0, 'Minimum Viable Validation Set',
            fontsize=15, fontweight='bold', ha='center', color='#1A1A2E')
    ax.text(5, 9.35, 'Per new Al alloy  ·  ~$1,000  ·  ~4 calendar days†  ·  Fail-fast order',
            fontsize=9, ha='center', color='#777', style='italic')

    ax.text(0.0, 8.7, 'Step', fontsize=9, ha='left', color='#555', fontweight='bold')
    ax.text(2.5, 8.7, 'Cost', fontsize=10, ha='center', color='#555', fontweight='bold')
    ax.text(6.0, 8.7, 'Time', fontsize=10, ha='center', color='#555', fontweight='bold')
    ax.text(8.8, 8.7, 'Go/No-Go', fontsize=9, ha='center', color='#555', fontweight='bold')

    mvs = [
        ('1. Single Tracks',    '(5–10)',  50,   2,  p['process'],  'Stable melt pool'),
        ('2. Thin Walls',       '(2–4)',  100,   4,  p['process'],  'No cracks (Kou<0.1)'),
        ('3. Density Cubes',    '(5–9)',  200,   4,  p['process'],  'ρ_rel ≥ 99.5%'),
        ('4. Tensile Bars',     '(3–6)',  300,  12,  p['mech'],     'YS/UTS ≥ target'),
        ('5. HT/HIP Coupons',  '(2–3)',  150,   6,  p['postproc'], 'Props improve'),
        ('6. 52902 Benchmark',  '(1)',    200,   4,  p['qual'],     'RMSE < 25 µm'),
    ]

    y0 = 8.0
    dy = 1.15
    bh = 0.38
    max_c = 350
    max_t = 14

    total_cost = 0
    total_hrs = 0
    for i, (name, count, cost, hrs, col, criteria) in enumerate(mvs):
        total_cost += cost
        total_hrs += hrs
        y = y0 - i * dy

        ax.text(0.0, y + 0.22, f'{name}', fontsize=9, color='#333', va='center',
                ha='left', fontweight='bold')
        ax.text(0.0, y - 0.15, count, fontsize=8, color='#888', va='center',
                ha='left', style='italic')

        bw = (cost / max_c) * 3.2
        ax.add_patch(FancyBboxPatch((1.2, y - 0.30), bw, bh,
                                     boxstyle="round,pad=0.04",
                                     facecolor=col, edgecolor='none', alpha=0.80))
        ax.text(1.2 + bw + 0.12, y - 0.12, f'${cost}', fontsize=8,
                color=col, va='center', fontweight='bold')

        tw = (hrs / max_t) * 2.8
        ax.add_patch(FancyBboxPatch((4.8, y - 0.30), tw, bh,
                                     boxstyle="round,pad=0.04",
                                     facecolor=col, edgecolor='none', alpha=0.45))
        ax.text(4.8 + tw + 0.12, y - 0.12, f'{hrs}h', fontsize=8,
                color=col, va='center')

        ax.text(8.8, y, criteria, fontsize=8, color='#555', va='center',
                ha='center', style='italic')

    yt = y0 - len(mvs) * dy + 0.1
    ax.plot([0, 10], [yt + 0.45, yt + 0.45], color='#CCC', linewidth=1.2)
    days = total_hrs / 8
    ax.text(2.5, yt - 0.15, f'TOTAL  ~${total_cost:,}', fontsize=12, fontweight='bold',
            ha='center', color='#1A1A2E')
    ax.text(6.0, yt - 0.15, f'TOTAL  ~{days:.0f} days', fontsize=12, fontweight='bold',
            ha='center', color='#1A1A2E')

    ax.text(5, yt - 0.85, 'Fail-fast: cracks at step 2, density at step 3 -> early go/no-go eliminates >50% before tensile',
            fontsize=8, ha='center', color='#888', style='italic')
    ax.text(5, yt - 1.5,
            '†~4 calendar days incl. scheduling, setup, cooldown; 38 hrs active operation',
            fontsize=8, ha='center', color='#AAA', style='italic')

    fig.tight_layout(pad=0.4)
    if save_path:
        fig.savefig(save_path, dpi=300, facecolor='white', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.2)
        print(f"Saved MVS v5 to {save_path}")
    if return_fig:
        return fig, ax
    plt.close(fig)

if __name__ == '__main__':
    create_mvs_figure('/tmp/fig_workspace/subfig_mvs.png')
