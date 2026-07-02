#!/usr/bin/env python3
"""Generate Figure 1: N1-MHKit artifact architecture.

The layout is intentionally fixed and generated programmatically from CSV source
files. It avoids automatic graph drawing, over-labelled arrows and ambiguous
legend marks. The bottom callout explicitly identifies examples of the public-
minimised package contents.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import INK, LINE, PANEL, BOX, RESTRICTED, WITHHELD, ACCENT, BOX_ALT, save_all

# More generous canvas margins than v6.8; no content touches the right edge.
LAYER_X = {1: 0.045, 2: 0.292, 3: 0.539, 4: 0.786}
PANEL_W = 0.175
PANEL_Y = 0.335
PANEL_H = 0.565
HEADER_H = 0.105
ITEM_H = 0.063

STATUS_FILL = {
    'public': BOX,
    'conditional': '#f9fafb',
    'restricted': RESTRICTED,
    'withheld': WITHHELD,
}

def rounded_box(ax, x, y, w, h, label, face, edge=LINE, lw=0.85, radius=0.016, fontsize=8.1, weight='regular'):
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.007,rounding_size={radius}',
                           linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(patch)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color=INK)
    return patch

def main():
    nodes = pd.read_csv(ROOT / 'figure_sources' / 'figure1_architecture_nodes.csv')
    outputs = pd.read_csv(ROOT / 'figure_sources' / 'figure1_public_outputs.csv')
    fig, ax = plt.subplots(figsize=(12.8, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Four major panels.
    for layer in [1, 2, 3, 4]:
        x = LAYER_X[layer]
        panel = FancyBboxPatch((x, PANEL_Y), PANEL_W, PANEL_H,
                               boxstyle='round,pad=0.011,rounding_size=0.024',
                               linewidth=1.0, edgecolor=LINE, facecolor=PANEL)
        ax.add_patch(panel)
        title = nodes[(nodes.layer == layer) & (nodes.node_type == 'layer_header')].iloc[0]['label']
        rounded_box(ax, x+0.015, PANEL_Y+PANEL_H-HEADER_H-0.014, PANEL_W-0.030,
                    HEADER_H, title, face=ACCENT, lw=0.9, fontsize=8.8, weight='bold')
        items = nodes[(nodes.layer == layer) & (nodes.node_type != 'layer_header')].sort_values('order')
        n = len(items)
        start_y = PANEL_Y + PANEL_H - HEADER_H - 0.080
        gap = 0.078 if n == 4 else 0.088
        for idx, (_, row) in enumerate(items.iterrows()):
            y = start_y - idx*gap - ITEM_H
            face = STATUS_FILL.get(str(row['release_status']), BOX)
            rounded_box(ax, x+0.025, y, PANEL_W-0.050, ITEM_H, row['label'], face=face,
                        lw=0.75, fontsize=7.85)

    # Main flow arrows. They are intentionally unlabelled; the panel headers and
    # caption explain the flow, avoiding the earlier collision of arrow labels with panels.
    arrow_y = 0.615
    for l1, l2 in [(1,2), (2,3), (3,4)]:
        x1 = LAYER_X[l1] + PANEL_W + 0.015
        x2 = LAYER_X[l2] - 0.015
        arrow = FancyArrowPatch((x1, arrow_y), (x2, arrow_y), arrowstyle='-|>',
                                mutation_scale=13, lw=1.05, color=LINE, shrinkA=0, shrinkB=0)
        ax.add_patch(arrow)

    # Public/restricted decision boundary. The label is kept outside the panels and away from the callout.
    boundary_x = 0.760
    ax.plot([boundary_x, boundary_x], [0.310, 0.925], color=LINE, lw=0.8, linestyle=(0,(2,2)))
    ax.text(boundary_x, 0.944, 'release decision boundary', ha='center', va='bottom',
            fontsize=7.0, color=LINE,
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 0.6})

    # Bottom callout explicitly states what the previously ambiguous small squares meant.
    # It is linked semantically by text rather than by a crossing arrow.
    callout_x, callout_y, callout_w, callout_h = 0.292, 0.065, 0.669, 0.145
    callout = FancyBboxPatch((callout_x, callout_y), callout_w, callout_h,
                             boxstyle='round,pad=0.010,rounding_size=0.020',
                             linewidth=0.85, edgecolor=LINE, facecolor='#fbfcfd')
    ax.add_patch(callout)
    ax.text(callout_x+0.020, callout_y+callout_h-0.035,
            'Examples included when the release boundary selects the public-minimised package',
            ha='left', va='center', fontsize=7.9, fontweight='bold', color=INK)
    pill_w = 0.180
    pill_gap = 0.034
    start_x = callout_x + 0.032
    pill_y = callout_y + 0.027
    for i, (_, row) in enumerate(outputs.iterrows()):
        rounded_box(ax, start_x + i*(pill_w+pill_gap), pill_y, pill_w, 0.052, row['label'],
                    face=BOX_ALT, lw=0.65, radius=0.013, fontsize=7.35)

    # Source-layer note to avoid misreading the source panel as public data.
    note = FancyBboxPatch((0.045, 0.070), 0.175, 0.155,
                          boxstyle='round,pad=0.010,rounding_size=0.020',
                          linewidth=0.75, edgecolor=LINE, facecolor='#fbfcfd')
    ax.add_patch(note)
    # Final typography patch: the title and status/body lines are deliberately
    # separated so no line visually touches or overlaps another in the DOCX render.
    ax.text(0.1325, 0.188, 'Source layer', ha='center', va='center',
            fontsize=7.25, fontweight='bold', color=INK)
    ax.text(0.1325, 0.128, 'restricted/withheld', ha='center', va='center',
            fontsize=6.70, color=LINE)
    ax.text(0.1325, 0.102, 'outside public package', ha='center', va='center',
            fontsize=6.70, color=LINE)

    save_all(fig, ROOT / 'figures', 'Figure_1_artifact_architecture_v6_8_1')
    plt.close(fig)

if __name__ == '__main__':
    main()
