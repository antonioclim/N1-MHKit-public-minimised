#!/usr/bin/env python3
"""Generate Figure 1: N1-MHKit artifact architecture.

Input: figure_sources/figure1_architecture_nodes.csv and
figure_sources/figure1_architecture_edges.csv. Output: vector and high-resolution
raster figure files. The layout is fixed intentionally to provide publication-
quality artwork rather than an automatic graph drawing.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import INK, LINE, PANEL, BOX, RESTRICTED, WITHHELD, ACCENT, save_all

LAYER_X = {1: 0.06, 2: 0.31, 3: 0.56, 4: 0.81}
PANEL_W = 0.19
PANEL_H = 0.78
PANEL_Y = 0.12
HEADER_H = 0.115

STATUS_FILL = {
    'public': BOX,
    'conditional': '#f9fafb',
    'restricted': RESTRICTED,
    'withheld': WITHHELD,
}

def rounded_box(ax, x, y, w, h, label, face, edge=LINE, lw=0.85, radius=0.018, fontsize=8.5, weight='regular'):
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.008,rounding_size={radius}',
                           linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=fontsize, fontweight=weight, color=INK)
    return patch

def main():
    nodes = pd.read_csv(ROOT / 'figure_sources' / 'figure1_architecture_nodes.csv')
    fig, ax = plt.subplots(figsize=(12.4, 3.43))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    layer_titles = []
    for layer in [1, 2, 3, 4]:
        x = LAYER_X[layer]
        panel = FancyBboxPatch((x, PANEL_Y), PANEL_W, PANEL_H, boxstyle='round,pad=0.012,rounding_size=0.025',
                               linewidth=1.0, edgecolor=LINE, facecolor=PANEL)
        ax.add_patch(panel)
        title = nodes[(nodes.layer == layer) & (nodes.node_type == 'layer_header')].iloc[0]['label']
        rounded_box(ax, x+0.018, PANEL_Y+PANEL_H-HEADER_H-0.018, PANEL_W-0.036, HEADER_H, title,
                    face=ACCENT, lw=0.9, fontsize=9, weight='bold')
        layer_titles.append((x+PANEL_W/2, PANEL_Y+PANEL_H-HEADER_H/2-0.018))
        items = nodes[(nodes.layer == layer) & (nodes.node_type != 'layer_header')].sort_values('order')
        n=len(items)
        start_y = PANEL_Y + PANEL_H - HEADER_H - 0.09
        gap = 0.105 if n==3 else 0.09
        box_h = 0.075
        for idx, (_, row) in enumerate(items.iterrows()):
            y = start_y - idx*gap - box_h
            face=STATUS_FILL.get(str(row['release_status']), BOX)
            rounded_box(ax, x+0.028, y, PANEL_W-0.056, box_h, row['label'], face=face, lw=0.75, fontsize=8.2)

    # Major flow arrows between panels, avoiding node-to-node clutter
    for l1, l2, label in [(1,2,'curate'), (2,3,'evaluate'), (3,4,'release gate')]:
        x1=LAYER_X[l1]+PANEL_W+0.006; x2=LAYER_X[l2]-0.006; y=0.515
        arrow = FancyArrowPatch((x1, y), (x2, y), arrowstyle='-|>', mutation_scale=12,
                                lw=1.1, color=LINE, shrinkA=0, shrinkB=0)
        ax.add_patch(arrow)
        ax.text((x1+x2)/2, y+0.035, label, ha='center', va='center', fontsize=7.7, color=LINE)

    # Boundary note
    ax.plot([0.787, 0.787], [0.08, 0.94], color=LINE, lw=0.7, linestyle=(0,(2,2)))
    ax.text(0.787, 0.055, 'public/restricted boundary', ha='center', va='top', fontsize=7.3, color=LINE)

    # Legend
    legend_elems = [
        Line2D([0],[0], marker='s', color='none', markerfacecolor=BOX, markeredgecolor=LINE, markersize=8, label='public documentation/code'),
        Line2D([0],[0], marker='s', color='none', markerfacecolor=RESTRICTED, markeredgecolor=LINE, markersize=8, label='restricted or conditional evidence'),
        Line2D([0],[0], marker='s', color='none', markerfacecolor=WITHHELD, markeredgecolor=LINE, markersize=8, label='withheld sensitive object'),
    ]
    ax.legend(handles=legend_elems, loc='lower left', bbox_to_anchor=(0.055, -0.005), frameon=False, fontsize=7.2, ncol=3, handletextpad=0.4, columnspacing=1.2)

    save_all(fig, ROOT / 'figures', 'Figure_1_artifact_architecture_v6_7')
    plt.close(fig)

if __name__ == '__main__':
    main()
