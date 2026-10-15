import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
})

fig = plt.figure(figsize=(18, 13.5))

c = {
    'calphad':   '#6C3483',
    'powder':    '#1B4F72',
    'strack':    '#21618C',
    'twall':     '#2874A6',
    'dcube':     '#2E86C1',
    'doe':       '#3498DB',
    'mech':      '#E67E22',
    'postproc':  '#D4AC0D',
    'geom':      '#B7950B',
    'indust':    '#CB4335',
    'prod':      '#922B21',
    'pass':      '#27AE60',
    'fail':      '#E74C3C',
    'ht':        '#8E44AD',
    'arrow':     '#7F8C8D',
    'gate_r':    '#C0392B',
    'gate_g':    '#27AE60',
    'gate_p':    '#8E44AD',
    'trad':      '#BDC3C7',
    'phase1':    '#2980B9',
    'phase2':    '#E74C3C',
    'phase1_bg': '#EBF5FB',
    'phase2_bg': '#FDEDEC',
}

# ==============================================================
# LEFT PANEL: Stage-gate funnel
# ==============================================================
ax = fig.add_axes([0.01, 0.05, 0.55, 0.92])
ax.set_xlim(-2, 14)
ax.set_ylim(-1.5, 15)
ax.axis('off')

ax.text(6.0, 14.6, 'Metal AM Alloy Scale-Up Validation', fontsize=16, fontweight='bold',
        ha='center', color='#1A1A2E')
ax.text(6.0, 14.05, 'Stage-Gate Progression  ·  Fail-Fast Funnel  ·  FLAIME Phase I',
        fontsize=9.5, ha='center', color='#555', style='italic')

# Color legend
legend_items = [
    ('Screening', c['calphad']), ('Process Dev.', c['dcube']),
    ('Properties', c['mech']), ('Qualification', c['indust'])
]
for li, (lbl, lcol) in enumerate(legend_items):
    lx = 2.0 + li * 2.8
    ax.add_patch(FancyBboxPatch((lx, 13.45), 0.5, 0.35,
                                boxstyle="round,pad=0.02",
                                facecolor=lcol, edgecolor='none', alpha=0.85))
    ax.text(lx + 0.65, 13.62, lbl, fontsize=6.5, color='#555',
            va='center', ha='left')

stages = [
    {'label': 'CALPHAD / BOFN',   'desc': 'Scheil sim., phase stability, ML pre-screen', 'comps': 5000, 'color': c['calphad'],  'gate': None,                                       'trl': '',     'phase': 1},
    {'label': 'Stage 0: Powder QA','desc': 'PSD, flowability, O₂, moisture (52907)',      'comps': 200,  'color': c['powder'],   'gate': None,                                       'trl': 'TRL 2','phase': 1},
    {'label': 'Stage 1: Single Tracks', 'desc': '5–10 tracks; melt-pool W/D/L stability','comps': 200,  'color': c['strack'],   'gate': None,                                       'trl': '',     'phase': 1},
    {'label': 'Stage 2: Thin Walls','desc': '2–4 walls, 2 orientations; crack screening', 'comps': 140,  'color': c['twall'],    'gate': ('Cracks? (Kou < 0.1)', 'gate_r'),           'trl': '',     'phase': 1},
    {'label': 'Stage 3: Density Cubes','desc': '5–9 cubes (10 mm); Archimedes ≥99.5%',   'comps': 100,  'color': c['dcube'],    'gate': ('ρ_rel ≥ 99.5%?', 'gate_g'),                'trl': 'TRL 3','phase': 1},
    {'label': 'Stage 4: Volumetric DoE','desc': 'P × v × h matrix; process window opt.',  'comps': 60,   'color': c['doe'],      'gate': None,                                       'trl': '',     'phase': 1},
    {'label': 'Stage 5: Mech. Coupons','desc': 'ASTM E8 tensile; YS, UTS, EL, anisotropy','comps': 30,  'color': c['mech'],     'gate': ('Top 3–5 → GA scale-up', 'gate_p'),         'trl': '',     'phase': 1},
    {'label': 'Stage 6: Post-Process', 'desc': 'T5/T6 aging, stress relief, HIP',         'comps': 10,   'color': c['postproc'], 'gate': None,                                       'trl': 'TRL 4','phase': 2},
    {'label': 'Stage 7: Geom. Benchmark','desc': 'ASTM 52902 artifact; RMSE, Ra',         'comps': 8,    'color': c['geom'],     'gate': None,                                       'trl': '',     'phase': 2},
    {'label': 'Stage 8: Industrial Qual.','desc': 'NDE pass/fail, traceability (52930)',   'comps': 4,    'color': c['indust'],   'gate': None,                                       'trl': 'TRL 5','phase': 2},
    {'label': 'Stage 9: Production',     'desc': 'Repeat builds; process freeze (MSFC-3716)','comps': 2, 'color': c['prod'],     'gate': None,                                       'trl': 'TRL 6+','phase': 2},
]

n = len(stages)
y_top = 12.8
row_h = 0.68
gap = 0.40
bar_x = 0.5
bar_w = 8.5
max_comps = 5000
count_x = bar_x + bar_w + 0.3
count_max_w = 3.0

# Phase I/II boundary position
phase_boundary_idx = 7  # Between Stage 5 (idx 6) and Stage 6 (idx 7)
phase_boundary_y = y_top - (phase_boundary_idx - 0.5) * (row_h + gap)

# Phase background shading — bolder boundary
ax.add_patch(FancyBboxPatch((bar_x - 0.5, phase_boundary_y + 0.05),
                             count_x + count_max_w + 1.2 - bar_x + 0.5,
                             y_top + 0.5 - phase_boundary_y - 0.05,
                             boxstyle="round,pad=0.1",
                             facecolor=c['phase1_bg'], edgecolor='none',
                             alpha=0.5, zorder=0))
ax.add_patch(FancyBboxPatch((bar_x - 0.5, y_top - n * (row_h + gap) - 0.3),
                             count_x + count_max_w + 1.2 - bar_x + 0.5,
                             phase_boundary_y - 0.05 - (y_top - n * (row_h + gap) - 0.3),
                             boxstyle="round,pad=0.1",
                             facecolor=c['phase2_bg'], edgecolor='none',
                             alpha=0.4, zorder=0))

for i, s in enumerate(stages):
    y = y_top - i * (row_h + gap)
    ymid = y - row_h / 2

    box = FancyBboxPatch((bar_x, y - row_h), bar_w, row_h,
                         boxstyle="round,pad=0.05",
                         facecolor=s['color'], edgecolor='white',
                         linewidth=1.3, alpha=0.90, zorder=3)
    ax.add_patch(box)

    ax.text(bar_x + 0.25, ymid, s['label'], fontsize=8.0, fontweight='bold',
            color='white', va='center', ha='left', zorder=4)
    ax.text(bar_x + bar_w - 0.25, ymid, s['desc'], fontsize=7.0, color='white',
            va='center', ha='right', style='italic', zorder=4, alpha=0.95)

    # Composition count bar
    cw = (s['comps'] / max_comps) * count_max_w
    cw = max(cw, 0.35)
    ax.add_patch(FancyBboxPatch((count_x, y - row_h + 0.05), cw, row_h - 0.10,
                                boxstyle="round,pad=0.03",
                                facecolor=s['color'], edgecolor='none', alpha=0.4, zorder=3))
    comp_str = f"{s['comps']:,}" if s['comps'] >= 1000 else str(s['comps'])
    ax.text(count_x + cw + 0.15, ymid, comp_str, fontsize=7.5,
            color=s['color'], va='center', ha='left', fontweight='bold')

    if s['trl']:
        ax.text(13.5, ymid, s['trl'], fontsize=7.5, color='#888',
                va='center', ha='center', fontweight='bold', style='italic')

    if i < n - 1:
        ax.annotate('', xy=(bar_x + bar_w / 2, y - row_h - gap + 0.06),
                    xytext=(bar_x + bar_w / 2, y - row_h - 0.06),
                    arrowprops=dict(arrowstyle='->', color=c['arrow'],
                                   lw=1.2, mutation_scale=11), zorder=2)

    if s['gate']:
        text, gcol = s['gate']
        gy = y - row_h - gap / 2
        gx = -0.5
        ax.add_patch(FancyBboxPatch((gx - 1.0, gy - 0.22), 2.4, 0.44,
                                    boxstyle="round,pad=0.06",
                                    facecolor='white', edgecolor=c[gcol],
                                    linewidth=1.2, alpha=0.95, zorder=5))
        ax.text(gx + 0.2, gy, text, fontsize=6.2, fontweight='bold', color=c[gcol],
                ha='center', va='center', zorder=6)
        ax.plot([gx + 1.4, bar_x], [gy, gy], color=c[gcol],
                linewidth=0.8, linestyle='--', alpha=0.4, zorder=2)

# Column headers
ax.text(count_x + count_max_w / 2, y_top + 0.25, '# Compositions', fontsize=7.5,
        color='#888', ha='center', fontweight='bold')
ax.text(13.5, y_top + 0.25, 'TRL', fontsize=7.5, color='#888',
        ha='center', fontweight='bold')

# Phase I/II boundary — BOLD, full-width
ax.plot([bar_x - 0.5, count_x + count_max_w + 1.0], [phase_boundary_y, phase_boundary_y],
        color=c['phase1'], linewidth=2.5, linestyle='--', alpha=0.7, zorder=6)

# Phase labels (in background shading)
ax.text(13.2, (y_top + phase_boundary_y) / 2 + 0.2, 'PHASE I\nSCOPE',
        fontsize=8.5, color=c['phase1'], ha='center', va='center',
        fontweight='bold', alpha=0.6, linespacing=0.85)
ax.text(13.2, (phase_boundary_y + y_top - n * (row_h + gap)) / 2,
        'PHASE II',
        fontsize=8.5, color=c['phase2'], ha='center', va='center',
        fontweight='bold', alpha=0.5)

# BOFN feedback arrow
arrow_x = bar_x - 0.4
ax.annotate('', xy=(arrow_x, y_top - 0.35),
            xytext=(arrow_x, y_top - 6 * (row_h + gap) - 0.35),
            arrowprops=dict(arrowstyle='->', color=c['ht'],
                           lw=2.0, mutation_scale=14,
                           connectionstyle='arc3,rad=0.2'), zorder=1)
ax.text(arrow_x - 0.6, y_top - 3 * (row_h + gap) - row_h / 2,
        'BOFN\nFeedback',
        fontsize=6.5, color=c['ht'], ha='center', va='center',
        fontweight='bold', rotation=90, linespacing=0.85)

# ==============================================================
# TOP RIGHT: Throughput comparison
# ==============================================================
ax_cmp = fig.add_axes([0.58, 0.72, 0.40, 0.24])
ax_cmp.set_xlim(0, 10)
ax_cmp.set_ylim(0, 6)
ax_cmp.axis('off')

ax_cmp.text(5, 5.7, 'Key Innovation: Throughput Advantage', fontsize=12,
            fontweight='bold', ha='center', color='#1A1A2E')

# Traditional
ax_cmp.add_patch(FancyBboxPatch((0.1, 3.2), 4.3, 2.0,
                                 boxstyle="round,pad=0.12",
                                 facecolor=c['trad'], edgecolor='#95A5A6',
                                 linewidth=1.5, alpha=0.25))
ax_cmp.text(2.25, 4.9, 'Traditional', fontsize=9, fontweight='bold',
            ha='center', color='#555')
ax_cmp.text(2.25, 4.3, '~18 months / alloy', fontsize=10.5, ha='center',
            color='#777', fontweight='bold')
ax_cmp.text(2.25, 3.7, '~$50K–500K / alloy', fontsize=10.5, ha='center',
            color='#777', fontweight='bold')

ax_cmp.annotate('', xy=(5.0, 4.2), xytext=(4.6, 4.2),
                arrowprops=dict(arrowstyle='->', color='#27AE60',
                               lw=3.5, mutation_scale=22))

# FLAIME (FIXED: consistent $1,000 and ~4 days)
ax_cmp.add_patch(FancyBboxPatch((5.5, 3.2), 4.3, 2.0,
                                 boxstyle="round,pad=0.12",
                                 facecolor='#27AE60', edgecolor='#27AE60',
                                 linewidth=1.5, alpha=0.12))
ax_cmp.text(7.65, 4.9, 'FLAIME Stage-Gate', fontsize=9, fontweight='bold',
            ha='center', color='#27AE60')
ax_cmp.text(7.65, 4.3, '~4 days / alloy', fontsize=10.5, ha='center',
            color='#1E8449', fontweight='bold')
ax_cmp.text(7.65, 3.7, '~$1,000 / alloy', fontsize=10.5, ha='center',
            color='#1E8449', fontweight='bold')

ax_cmp.text(4.8, 5.25, '~135×\nfaster', fontsize=9, fontweight='bold',
            ha='center', va='center', color='#27AE60', linespacing=0.85)

# ROI math
ax_cmp.text(5, 2.7, 'Phase I:  200 alloys × $1K = $200K    vs.    200 × $50K = $10M+    →    50× cost reduction',
            fontsize=7.5, ha='center', color='#1A1A2E', fontweight='bold')
ax_cmp.text(5, 2.2, 'Enables ≥200 compositions in 9 months via BOFN-guided fail-fast funnel',
            fontsize=7.5, ha='center', color='#555', style='italic')

# HT box
ax_cmp.add_patch(FancyBboxPatch((0.1, 0.4), 9.7, 1.4,
                                 boxstyle="round,pad=0.10",
                                 facecolor=c['ht'], edgecolor=c['ht'],
                                 linewidth=1, alpha=0.08))
ax_cmp.text(5.0, 1.45, '⚡  High-Throughput Acceleration', fontsize=8,
            fontweight='bold', ha='center', color=c['ht'])
ax_cmp.text(5.0, 0.85,
            'Combinatorial LPBF builds (Weaver 2021, 5× speedup)  ·  HT-READ mini-libraries (Vecchio 2021)\n'
            '3–4 compositions per build plate  ·  Mini-cubes + microhardness as rapid go/no-go gate',
            fontsize=6.5, ha='center', color='#666', linespacing=1.4)

# ==============================================================
# MIDDLE RIGHT: Al Defect Hierarchy
# ==============================================================
ax2 = fig.add_axes([0.58, 0.38, 0.40, 0.32])
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

ax2.text(5, 9.5, 'Al Alloy Defect Screening Hierarchy', fontsize=11,
         fontweight='bold', ha='center', color='#1A1A2E')
ax2.text(5, 8.95, 'Priority-ordered  ·  Mapped to screening stages',
         fontsize=7.5, ha='center', color='#777', style='italic')

defects = [
    ('CRITICAL', 'Hot Cracking',    '2xxx/7xxx, novel Al-Cu-X',   'Stage 2',  '#C0392B'),
    ('HIGH',     'H₂ Porosity',     'Spherical; moisture + melt', 'Stage 0–1','#E67E22'),
    ('HIGH',     'Al₂O₃ Inclusions','~4 nm films on powder',     'Stage 0–1','#E67E22'),
    ('HIGH',     'Residual Stress',  'Distortion, delamination',  'Stage 6',  '#E67E22'),
    ('MODERATE', 'Keyhole Pores',    'Excess energy density',     'Stage 1',  '#F39C12'),
    ('MODERATE', 'Lack of Fusion',   'Insufficient melt overlap', 'Stage 3',  '#F39C12'),
    ('MODERATE', 'Volatile Loss',    'Mg, Zn, Mn evaporation',   'Stage 5',  '#F39C12'),
]

for i, (sev, name, desc, stage, col) in enumerate(defects):
    y = 8.0 - i * 1.08
    ax2.add_patch(FancyBboxPatch((0.0, y - 0.22), 1.7, 0.44,
                                  boxstyle="round,pad=0.05",
                                  facecolor=col, edgecolor='none', alpha=0.88))
    ax2.text(0.85, y, sev, fontsize=6.5, fontweight='bold', color='white',
             ha='center', va='center')
    ax2.text(2.0, y + 0.05, name, fontsize=7.5, color='#1A1A2E',
             va='center', ha='left', fontweight='bold')
    ax2.text(2.0, y - 0.28, desc, fontsize=6, color='#888',
             va='center', ha='left', style='italic')
    ax2.text(9.8, y, f'→ {stage}', fontsize=6.5, color=col,
             va='center', ha='right', fontweight='bold')

# ==============================================================
# BOTTOM RIGHT: Minimum Viable Validation Set (FIXED: consistent times)
# ==============================================================
ax3 = fig.add_axes([0.58, 0.05, 0.40, 0.31])
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.axis('off')

ax3.text(5, 9.5, 'Minimum Viable Validation Set', fontsize=11,
         fontweight='bold', ha='center', color='#1A1A2E')
ax3.text(5, 9.0, 'Per new Al alloy  ·  ~$1,000  ·  ~4 days  ·  Fail-fast order',
         fontsize=7.5, ha='center', color='#777', style='italic')

mvs = [
    ('❶  Single Tracks (5–10)',    50,   2,  c['strack']),
    ('❷  Thin Walls (2–4)',       100,   4,  c['twall']),
    ('❸  Density Cubes (5–9)',    200,   4,  c['dcube']),
    ('❹  Tensile Bars (3–6)',     300,  12,  c['mech']),
    ('❺  HT / HIP Coupons (2–3)',150,   6,  c['postproc']),
    ('❻  52902 Benchmark (1)',    200,   4,  c['geom']),
]

y0 = 8.0
dy = 1.05
bh = 0.35
max_c = 350
max_t = 14

ax3.text(2.2, y0 + 0.55, 'Cost', fontsize=8, ha='center', color='#555', fontweight='bold')
ax3.text(7.8, y0 + 0.55, 'Time', fontsize=8, ha='center', color='#555', fontweight='bold')

total_cost = 0
total_hrs = 0
for i, (name, cost, hrs, col) in enumerate(mvs):
    total_cost += cost
    total_hrs += hrs
    y = y0 - i * dy
    ax3.text(0.0, y + 0.18, name, fontsize=7.3, color='#333', va='center',
             ha='left', fontweight='bold')
    bw = (cost / max_c) * 3.5
    ax3.add_patch(FancyBboxPatch((0.4, y - 0.32), bw, bh,
                                  boxstyle="round,pad=0.03",
                                  facecolor=col, edgecolor='none', alpha=0.75))
    ax3.text(0.4 + bw + 0.12, y - 0.16, f'${cost}', fontsize=6.8,
             color=col, va='center', fontweight='bold')
    tw = (hrs / max_t) * 3.5
    ax3.add_patch(FancyBboxPatch((5.8, y - 0.32), tw, bh,
                                  boxstyle="round,pad=0.03",
                                  facecolor=col, edgecolor='none', alpha=0.45))
    ax3.text(5.8 + tw + 0.12, y - 0.16, f'{hrs} hrs', fontsize=6.3,
             color=col, va='center')

yt = y0 - 6 * dy + 0.3
ax3.plot([0, 10], [yt + 0.35, yt + 0.35], color='#DDD', linewidth=0.8)
days = total_hrs / 8
ax3.text(2.2, yt, f'TOTAL  ~${total_cost:,}', fontsize=9.5, fontweight='bold',
         ha='center', color='#1A1A2E')
ax3.text(7.8, yt, f'TOTAL  ~{days:.0f} days', fontsize=9.5, fontweight='bold',
         ha='center', color='#1A1A2E')

# ==============================================================
# Footer
# ==============================================================
fig.text(0.5, 0.005,
         'Sources: Moylan et al. 2014 (NIST JRES 119.017)  ·  ISO/ASTM 52902, 52904, 52907, 52930, 52936-1  ·  ASTM E8/E8M, F3318, B311  ·  '
         'Gheysen et al. 2021 (Mat. & Des.)  ·  Kumar et al. 2021 (RPJ)  ·  '
         'Weaver et al. 2021 (Mat. & Des.)  ·  Vecchio et al. 2021 (Acta Mat.)  ·  '
         'Brenner & Nedeljkovic-Groha 2025 (Appl. Sci.)  ·  Leon et al. 2025 (JMMP)  ·  NASA MSFC-STD-3716',
         fontsize=6.5, ha='center', color='#999', style='italic')

outpath = '/home/runner/work/digital-alloy-lab-private/digital-alloy-lab-private/edison-trajectories/fig-am-scaleup-validation-progression.png'
fig.savefig(outpath, dpi=300, facecolor='white', edgecolor='none')
print(f"Saved v5 (final) to {outpath}")
print(f"Total cost: ${total_cost}, Total hours: {total_hrs}, Total days: {days:.0f}")
