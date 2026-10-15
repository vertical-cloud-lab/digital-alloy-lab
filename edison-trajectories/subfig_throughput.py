"""Subfigure B: Throughput Comparison — v5: absolute metrics first, unified palette."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PALETTE = {
    'screen':    '#4C72B0',  'process':   '#55A868',
    'mech':      '#C44E52',  'qual':      '#8172B2',
    'postproc':  '#CCB974',  'flaime':    '#55A868',
    'trad':      '#BDC3C7',
}

def create_throughput_figure(save_path=None, return_fig=False):
    p = PALETTE
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 10.5)
    ax.axis('off')

    ax.text(5, 10.0, 'FLAIME Throughput Innovation',
            fontsize=16, fontweight='bold', ha='center', color='#1A1A2E')

    # Lead with ABSOLUTE metrics (Fix 3)
    ax.add_patch(FancyBboxPatch((1.5, 8.8), 7.0, 0.85,
                                 boxstyle="round,pad=0.10",
                                 facecolor=p['flaime'], edgecolor=p['flaime'],
                                 linewidth=2, alpha=0.10))
    ax.text(5, 9.35, '~$1,000 and ~4 calendar days per alloy screening decision',
            fontsize=11, fontweight='bold', ha='center', color='#145A32')
    ax.text(5, 8.95, 'vs. traditional: ~$50K–$500K and ~18 months for full qualification',
            fontsize=8.5, ha='center', color='#777', style='italic')

    # Comparison boxes
    ax.add_patch(FancyBboxPatch((0.3, 5.6), 4.0, 2.8,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#F2F3F4', edgecolor='#95A5A6',
                                 linewidth=1.5))
    ax.text(2.3, 8.0, 'Traditional', fontsize=12, fontweight='bold',
            ha='center', color='#555')
    ax.text(2.3, 7.2, '~18 months', fontsize=14, ha='center',
            color='#777', fontweight='bold')
    ax.text(2.3, 6.4, '~$50K–$500K', fontsize=11, ha='center', color='#999')
    ax.text(2.3, 5.9, 'full qualification', fontsize=8, ha='center',
            color='#AAA', style='italic')

    ax.annotate('', xy=(5.2, 7.0), xytext=(4.6, 7.0),
                arrowprops=dict(arrowstyle='->', color=p['flaime'],
                               lw=4.0, mutation_scale=24))

    ax.add_patch(FancyBboxPatch((5.7, 5.6), 4.0, 2.8,
                                 boxstyle="round,pad=0.15",
                                 facecolor=p['flaime'], edgecolor=p['flaime'],
                                 linewidth=2.0, alpha=0.12))
    ax.add_patch(FancyBboxPatch((5.7, 5.6), 4.0, 2.8,
                                 boxstyle="round,pad=0.15",
                                 facecolor='none', edgecolor=p['flaime'],
                                 linewidth=2.0))
    ax.text(7.7, 8.0, 'FLAIME Stage-Gate', fontsize=12, fontweight='bold',
            ha='center', color=p['flaime'])
    ax.text(7.7, 7.2, '~4 days', fontsize=14, ha='center',
            color='#145A32', fontweight='bold')
    ax.text(7.7, 6.4, '~$1,000', fontsize=11, ha='center', color=p['flaime'])
    ax.text(7.7, 5.9, 'screening decision', fontsize=8, ha='center',
            color='#27AE60', style='italic')

    # Fold comparison — secondary
    ax.text(5.0, 5.15, '~135× faster to first decision  ·  50–500× lower cost (conservative)',
            fontsize=8.5, ha='center', color='#666', style='italic')

    # ROI math
    ax.add_patch(FancyBboxPatch((0.3, 3.5), 9.4, 1.3,
                                 boxstyle="round,pad=0.10",
                                 facecolor='#1A1A2E', edgecolor='none', alpha=0.04))
    ax.text(5.0, 4.45, 'Phase I ROI  (using $50K lower bound — conservative)',
            fontsize=8.5, fontweight='bold', ha='center', color='#1A1A2E')
    ax.text(5.0, 3.85, '200 alloys × $1K = $200K     vs.     200 × $50K = $10M+     →  50× cost reduction',
            fontsize=9, ha='center', color='#333', fontweight='bold')

    # HT acceleration
    ax.add_patch(FancyBboxPatch((0.3, 0.0), 9.4, 3.0,
                                 boxstyle="round,pad=0.12",
                                 facecolor=p['qual'], edgecolor=p['qual'],
                                 linewidth=1, alpha=0.06))
    ax.text(5.0, 2.65, 'High-Throughput Acceleration Methods',
            fontsize=10, fontweight='bold', ha='center', color=p['qual'])

    ht_items = [
        ('Combinatorial LPBF builds', 'Weaver 2021 — 5× throughput'),
        ('HT-READ mini-libraries', 'Vecchio 2021 — 16 samples/mount'),
        ('Mini-cube rapid screening', '3–4 compositions per build plate'),
    ]
    for j, (title, cite) in enumerate(ht_items):
        y = 1.95 - j * 0.60
        ax.text(0.8, y, '•', fontsize=12, color=p['qual'], va='center', ha='center')
        ax.text(1.3, y, f'{title}  —  {cite}', fontsize=8.5, color='#444',
                va='center', ha='left')

    fig.tight_layout(pad=0.5)
    if save_path:
        fig.savefig(save_path, dpi=300, facecolor='white', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.2)
        print(f"Saved throughput v5 to {save_path}")
    if return_fig:
        return fig, ax
    plt.close(fig)

if __name__ == '__main__':
    create_throughput_figure('/tmp/fig_workspace/subfig_throughput.png')
