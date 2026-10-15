"""Compositor v5: 4 modular subfigures → final proposal figure. ≥7pt citations."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.image import imread
import os

def compose_figure(subfig_dir='/tmp/fig_workspace',
                   output_path=None, version='v8'):
    paths = {
        'stagegate':   os.path.join(subfig_dir, 'subfig_stagegate.png'),
        'throughput':  os.path.join(subfig_dir, 'subfig_throughput.png'),
        'defects':     os.path.join(subfig_dir, 'subfig_defects.png'),
        'mvs':         os.path.join(subfig_dir, 'subfig_mvs.png'),
    }
    for k, p in paths.items():
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing subfigure: {p}")

    imgs = {k: imread(p) for k, p in paths.items()}

    fig = plt.figure(figsize=(22, 15))

    # Left: Stage-Gate (full height)
    ax_left = fig.add_axes([0.0, 0.03, 0.52, 0.95])
    ax_left.imshow(imgs['stagegate'])
    ax_left.axis('off')
    ax_left.text(0.02, 0.99, '(a)', transform=ax_left.transAxes,
                 fontsize=16, fontweight='bold', va='top', color='#1A1A2E')

    # Right column
    ax_tr = fig.add_axes([0.53, 0.67, 0.46, 0.31])
    ax_tr.imshow(imgs['throughput'])
    ax_tr.axis('off')
    ax_tr.text(0.02, 0.99, '(b)', transform=ax_tr.transAxes,
               fontsize=16, fontweight='bold', va='top', color='#1A1A2E')

    ax_mr = fig.add_axes([0.53, 0.35, 0.46, 0.30])
    ax_mr.imshow(imgs['defects'])
    ax_mr.axis('off')
    ax_mr.text(0.02, 0.99, '(c)', transform=ax_mr.transAxes,
               fontsize=16, fontweight='bold', va='top', color='#1A1A2E')

    ax_br = fig.add_axes([0.53, 0.03, 0.46, 0.30])
    ax_br.imshow(imgs['mvs'])
    ax_br.axis('off')
    ax_br.text(0.02, 0.99, '(d)', transform=ax_br.transAxes,
               fontsize=16, fontweight='bold', va='top', color='#1A1A2E')

    # FIX 3: Larger citation footer (≥7pt) — two lines for readability
    fig.text(0.5, 0.018,
             '[1] Moylan 2014 NIST JRES 119.017  [2] ISO/ASTM 52902–52941  [3] ASTM E8  '
             '[4] Gheysen 2021  [5] Weaver 2021  [6] Vecchio 2021  '
             '[7] Brenner 2025  [8] Leon 2025  [9] NASA MSFC-3716',
             fontsize=7.5, ha='center', color='#888', style='italic')

    if output_path:
        fig.savefig(output_path, dpi=300, facecolor='white', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.2)
        print(f"Saved composite {version} to {output_path}")
    plt.close(fig)

if __name__ == '__main__':
    compose_figure(output_path='/tmp/fig_workspace/composite.png')
