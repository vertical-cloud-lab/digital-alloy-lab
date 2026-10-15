"""Subfigure C: Al Alloy Defect Hierarchy — v5: unified palette, cross-panel linkage."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PALETTE = {
    'screen':    '#4C72B0',  'process':   '#55A868',
    'mech':      '#C44E52',  'qual':      '#8172B2',
    'postproc':  '#CCB974',
}
SEV_COLORS = {
    'CRITICAL':  '#C44E52',  # muted red (= mech color)
    'HIGH':      '#DD8452',  # orange
    'MODERATE':  '#4C72B0',  # steel blue (= screen color, accessible)
}

def create_defects_figure(save_path=None, return_fig=False):
    p = PALETTE
    s = SEV_COLORS
    # Map stage labels to stage colors from panel (a)
    stage_colors = {
        'Stage 2': p['process'],  'Stage 0': p['screen'],
        'Stage 1': p['process'],  'Stage 6': p['postproc'],
        'Stage 3': p['process'],  'Stage 5': p['mech'],
    }

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5, 9.5, 'Al Alloy Defect Screening Hierarchy',
            fontsize=15, fontweight='bold', ha='center', color='#1A1A2E')
    ax.text(5, 8.9, 'Priority-ordered  ·  Mapped to fail-fast stages in panel (a)',
            fontsize=9, ha='center', color='#777', style='italic')

    defects = [
        ('CRITICAL', 'Hot Cracking (Solidification)',   'Kou < 0.1; 2xxx/7xxx, Al-Cu-X',          'Stage 2: Thin Walls',     'Stage 2'),
        ('HIGH',     'H₂ Porosity (Spherical)',         'Moisture + melt dissolution',              'Stage 0–1: Powder/Track', 'Stage 0'),
        ('HIGH',     'Al₂O₃ Oxide Inclusions',         '~4 nm native film; entrained',             'Stage 0–1: Powder/Track', 'Stage 0'),
        ('HIGH',     'Residual Stress / Distortion',    'Thermal gradients → warp',                 'Stage 6: Post-Process',   'Stage 6'),
        ('MODERATE', 'Keyhole Porosity',                'Excess energy density; vapor depression',   'Stage 1: Single Tracks',  'Stage 1'),
        ('MODERATE', 'Lack-of-Fusion Porosity',         'Insufficient overlap; irregular voids',     'Stage 3: Density Cubes',  'Stage 3'),
        ('MODERATE', 'Volatile Element Loss',           'Mg, Zn, Mn evaporation',                   'Stage 5: Mech. Test',     'Stage 5'),
    ]

    sep_after = [0, 3]

    for i, (sev, name, desc, stage_label, stage_key) in enumerate(defects):
        y = 7.95 - i * 1.08

        if i % 2 == 0:
            ax.add_patch(FancyBboxPatch((0.05, y - 0.44), 9.9, 0.88,
                                         boxstyle="round,pad=0.02",
                                         facecolor='#F8F9F9', edgecolor='none'))

        sev_col = s[sev]
        stg_col = stage_colors.get(stage_key, '#666')

        badge_w = 1.8
        ax.add_patch(FancyBboxPatch((0.15, y - 0.28), badge_w, 0.56,
                                     boxstyle="round,pad=0.06",
                                     facecolor=sev_col, edgecolor='none', alpha=0.90))
        ax.text(0.15 + badge_w / 2, y, sev, fontsize=8, fontweight='bold',
                color='white', ha='center', va='center')

        ax.text(2.2, y + 0.10, name, fontsize=9.5, color='#1A1A2E',
                va='center', ha='left', fontweight='bold')
        ax.text(2.2, y - 0.30, desc, fontsize=8, color='#888',
                va='center', ha='left', style='italic')

        ax.add_patch(FancyBboxPatch((7.1, y - 0.22), 2.75, 0.44,
                                     boxstyle="round,pad=0.05",
                                     facecolor=stg_col, edgecolor='none', alpha=0.15))
        ax.text(8.47, y, f'→  {stage_label}', fontsize=8, color=stg_col,
                va='center', ha='center', fontweight='bold')

        if i in sep_after:
            sep_y = y - 0.58
            ax.plot([0.15, 9.85], [sep_y, sep_y], color='#DDD',
                    linewidth=0.8, linestyle='-')

    fig.tight_layout(pad=0.4)
    if save_path:
        fig.savefig(save_path, dpi=300, facecolor='white', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.15)
        print(f"Saved defects v5 to {save_path}")
    if return_fig:
        return fig, ax
    plt.close(fig)

if __name__ == '__main__':
    create_defects_figure('/tmp/fig_workspace/subfig_defects.png')
