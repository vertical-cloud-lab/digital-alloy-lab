"""Subfigure A: Stage-Gate Funnel — v6: enlarged BOFN callout, ≥9pt gate text."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

PALETTE = {
    'screen':    '#4C72B0',  'process':   '#55A868',
    'mech':      '#C44E52',  'qual':      '#8172B2',
    'postproc':  '#CCB974',  'arrow':     '#8C8C8C',
    'gate_crit': '#C44E52',  'gate_go': '#55A868',  'gate_sel': '#8172B2',
    'phase1':    '#4C72B0',  'phase2':   '#C44E52',
    'phase1_bg': '#EDF2F9',  'phase2_bg': '#FAEAEA',
    'bofn':      '#8172B2',
}

def create_stagegate_figure(save_path=None, return_fig=False):
    p = PALETTE
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(-5.5, 15.5)
    ax.set_ylim(-2.5, 17.0)
    ax.axis('off')

    ax.text(5.5, 16.5, 'Metal AM Alloy Validation Funnel',
            fontsize=20, fontweight='bold', ha='center', color='#1A1A2E')
    ax.text(5.5, 15.8, 'Stage-Gate Progression  ·  Fail-Fast  ·  FLAIME Phase I/II',
            fontsize=11, ha='center', color='#555', style='italic')

    legend_items = [
        ('Screening', p['screen']), ('Process Dev', p['process']),
        ('Mechanical', p['mech']), ('Post-Process', p['postproc']),
        ('Qualification', p['qual'])
    ]
    for li, (lbl, lcol) in enumerate(legend_items):
        lx = -0.5 + li * 3.2
        ax.add_patch(FancyBboxPatch((lx, 15.1), 0.5, 0.35,
                                    boxstyle="round,pad=0.03",
                                    facecolor=lcol, edgecolor='none', alpha=0.85))
        ax.text(lx + 0.7, 15.27, lbl, fontsize=8.5, color='#555',
                va='center', ha='left')

    stages = [
        {'label': 'CALPHAD / BOFN',        'desc': 'Scheil, phase stability, ML',       'comps': 5000, 'color': p['screen'],   'gate': None,                                 'trl': '',      'phase': 1},
        {'label': 'Stage 0  Powder QA',     'desc': 'PSD, flow, O₂ (ISO 52907)',         'comps': 200,  'color': p['screen'],   'gate': ('Quality gate*', 'gate_go'),           'trl': 'TRL 2', 'phase': 1},
        {'label': 'Stage 1  Single Tracks',  'desc': '5–10 tracks · melt-pool W/D/L',    'comps': 190,  'color': p['process'],  'gate': None,                                 'trl': '',      'phase': 1},
        {'label': 'Stage 2  Thin Walls',     'desc': '2–4 walls · crack screening',       'comps': 140,  'color': p['process'],  'gate': ('Kou < 0.1?', 'gate_crit'),           'trl': '',      'phase': 1},
        {'label': 'Stage 3  Density Cubes',  'desc': '10 mm cubes · ≥99.5%',              'comps': 100,  'color': p['process'],  'gate': ('ρ_rel ≥ 99.5%?', 'gate_go'),          'trl': 'TRL 3', 'phase': 1},
        {'label': 'Stage 4  Volumetric DoE', 'desc': 'P × v × h matrix',                  'comps': 60,   'color': p['process'],  'gate': None,                                 'trl': '',      'phase': 1},
        {'label': 'Stage 5  Mech. Coupons',  'desc': 'ASTM E8 · YS, UTS, EL',            'comps': 30,   'color': p['mech'],     'gate': ('Top 3–5 → GA', 'gate_sel'),           'trl': '',      'phase': 1},
        {'label': 'Stage 6  Post-Process',   'desc': 'T5/T6, stress relief, HIP',         'comps': 10,   'color': p['postproc'], 'gate': None,                                 'trl': 'TRL 4', 'phase': 2},
        {'label': 'Stage 7  Geom. Bench.',   'desc': 'ISO 52902 · RMSE, Ra',              'comps': 8,    'color': p['qual'],     'gate': None,                                 'trl': '',      'phase': 2},
        {'label': 'Stage 8  Indust. Qual.',  'desc': 'NDE, traceability (52930)',          'comps': 4,    'color': p['qual'],     'gate': None,                                 'trl': 'TRL 5', 'phase': 2},
        {'label': 'Stage 9  Production',     'desc': 'Freeze (MSFC-3716)',                 'comps': 2,    'color': p['qual'],     'gate': None,                                 'trl': 'TRL 6+','phase': 2},
    ]

    n = len(stages)
    y_top = 14.2
    row_h = 0.78
    gap = 0.37
    bar_x = 1.0
    bar_w = 9.0
    max_comps = 5000
    count_x = bar_x + bar_w + 0.4
    count_max_w = 3.2

    phase_boundary_idx = 7
    phase_boundary_y = y_top - (phase_boundary_idx - 0.5) * (row_h + gap)

    bg_left = bar_x - 0.8
    bg_right = count_x + count_max_w + 1.8
    bg_w = bg_right - bg_left
    ax.add_patch(FancyBboxPatch((bg_left, phase_boundary_y + 0.05),
                                 bg_w, y_top + 0.5 - phase_boundary_y - 0.05,
                                 boxstyle="round,pad=0.12",
                                 facecolor=p['phase1_bg'], edgecolor='none',
                                 alpha=0.55, zorder=0))
    ax.add_patch(FancyBboxPatch((bg_left, y_top - n * (row_h + gap) - 0.5),
                                 bg_w,
                                 phase_boundary_y - 0.05 - (y_top - n * (row_h + gap) - 0.5),
                                 boxstyle="round,pad=0.12",
                                 facecolor=p['phase2_bg'], edgecolor='none',
                                 alpha=0.45, zorder=0))

    for i, s in enumerate(stages):
        y = y_top - i * (row_h + gap)
        ymid = y - row_h / 2

        box = FancyBboxPatch((bar_x, y - row_h), bar_w, row_h,
                             boxstyle="round,pad=0.06",
                             facecolor=s['color'], edgecolor='white',
                             linewidth=1.3, alpha=0.90, zorder=3)
        ax.add_patch(box)

        ax.text(bar_x + 0.3, ymid + 0.03, s['label'], fontsize=10.5, fontweight='bold',
                color='white', va='center', ha='left', zorder=4)
        ax.text(bar_x + bar_w - 0.3, ymid - 0.01, s['desc'], fontsize=8.5, color='white',
                va='center', ha='right', style='italic', zorder=4, alpha=0.92)

        cw = (s['comps'] / max_comps) * count_max_w
        cw = max(cw, 0.40)
        ax.add_patch(FancyBboxPatch((count_x, y - row_h + 0.06), cw, row_h - 0.12,
                                    boxstyle="round,pad=0.04",
                                    facecolor=s['color'], edgecolor='none',
                                    alpha=0.30, zorder=3))
        comp_str = f"{s['comps']:,}" if s['comps'] >= 1000 else str(s['comps'])
        ax.text(count_x + cw + 0.18, ymid, comp_str, fontsize=9,
                color=s['color'], va='center', ha='left', fontweight='bold')

        if s['trl']:
            ax.text(15.0, ymid, s['trl'], fontsize=9, color='#888',
                    va='center', ha='center', fontweight='bold', style='italic')

        if i < n - 1:
            ax.annotate('', xy=(bar_x + bar_w / 2, y - row_h - gap + 0.06),
                        xytext=(bar_x + bar_w / 2, y - row_h - 0.06),
                        arrowprops=dict(arrowstyle='->', color=p['arrow'],
                                       lw=1.1, mutation_scale=10), zorder=2)

        # FIX 1: Larger gate labels (≥9pt)
        if s['gate']:
            text, gcol = s['gate']
            gy = y - row_h - gap / 2
            gx = -1.2
            ax.add_patch(FancyBboxPatch((gx - 1.5, gy - 0.30), 3.2, 0.60,
                                        boxstyle="round,pad=0.08",
                                        facecolor='white', edgecolor=p[gcol],
                                        linewidth=2.0, alpha=0.95, zorder=5))
            ax.text(gx + 0.1, gy, text, fontsize=9, fontweight='bold', color=p[gcol],
                    ha='center', va='center', zorder=6)
            ax.plot([gx + 1.7, bar_x], [gy, gy], color=p[gcol],
                    linewidth=1.0, linestyle='--', alpha=0.4, zorder=2)

    ax.text(count_x + count_max_w / 2, y_top + 0.45, '# Compositions', fontsize=9.5,
            color='#888', ha='center', fontweight='bold')
    ax.text(15.0, y_top + 0.45, 'TRL', fontsize=9.5, color='#888',
            ha='center', fontweight='bold')

    ax.plot([bg_left, bg_right], [phase_boundary_y, phase_boundary_y],
            color=p['phase1'], linewidth=2.5, linestyle='--', alpha=0.6, zorder=6)

    ax.text(14.7, (y_top + phase_boundary_y) / 2 + 0.1, 'PHASE I',
            fontsize=10, color=p['phase1'], ha='center', va='center',
            fontweight='bold', alpha=0.55)
    ax.text(14.7, (phase_boundary_y + y_top - n * (row_h + gap)) / 2,
            'PHASE II', fontsize=10, color=p['phase2'], ha='center', va='center',
            fontweight='bold', alpha=0.45)

    # FIX 1: ENLARGED BOFN CALLOUT (≥9pt throughout)
    bofn_x = bar_x - 0.6
    bofn_top = y_top - 0.2
    bofn_bot = y_top - 6 * (row_h + gap) - 0.2
    ax.annotate('', xy=(bofn_x, bofn_top),
                xytext=(bofn_x, bofn_bot),
                arrowprops=dict(arrowstyle='->', color=p['bofn'],
                               lw=3.5, mutation_scale=18,
                               connectionstyle='arc3,rad=0.25'), zorder=7)

    bofn_cy = (bofn_top + bofn_bot) / 2
    # Larger box
    ax.add_patch(FancyBboxPatch((-5.2, bofn_cy - 1.1), 4.0, 2.2,
                                 boxstyle="round,pad=0.12",
                                 facecolor=p['bofn'], edgecolor=p['bofn'],
                                 linewidth=2.0, alpha=0.08, zorder=5))
    ax.add_patch(FancyBboxPatch((-5.2, bofn_cy - 1.1), 4.0, 2.2,
                                 boxstyle="round,pad=0.12",
                                 facecolor='none', edgecolor=p['bofn'],
                                 linewidth=2.0, zorder=5))
    ax.text(-3.2, bofn_cy + 0.55, 'BOFN', fontsize=14, fontweight='bold',
            color=p['bofn'], ha='center', va='center', zorder=6)
    ax.text(-3.2, bofn_cy + 0.05, 'Active Learning Loop', fontsize=10,
            color=p['bofn'], ha='center', va='center', zorder=6)
    ax.text(-3.2, bofn_cy - 0.45, 'AI selects next compositions\nusing all prior stage data', fontsize=9,
            color='#555', ha='center', va='center', zorder=6, linespacing=1.1)
    ax.text(-3.2, bofn_cy - 0.90, '→ 3× more efficient\nthan random screening', fontsize=8.5,
            color=p['bofn'], ha='center', va='center', zorder=6, style='italic',
            fontweight='bold', linespacing=1.0)

    ax.text(bar_x, -1.8, '*Quality gate: filters defective powder lots, not compositions',
            fontsize=8, color='#AAA', style='italic')

    fig.tight_layout(pad=0.3)
    if save_path:
        fig.savefig(save_path, dpi=300, facecolor='white', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.15)
        print(f"Saved stagegate v6 to {save_path}")
    if return_fig:
        return fig, ax
    plt.close(fig)

if __name__ == '__main__':
    create_stagegate_figure('/tmp/fig_workspace/subfig_stagegate.png')
