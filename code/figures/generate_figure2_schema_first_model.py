#!/usr/bin/env python3
"""Generate Figure 2: schema-first curated data model.

Input: figure_sources/figure2_schema_entities.csv and
figure_sources/figure2_schema_relationships.csv. The figure is a fixed-layout
conceptual schema, not a clinical model and not a FHIR compliance claim.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import INK, LINE, PANEL, BOX, BOX_ALT, ACCENT, save_all

def box(ax, xy, w, h, text, face=BOX, weight='regular', fontsize=9, lw=0.85):
    x,y=xy
    p=FancyBboxPatch((x,y), w,h, boxstyle='round,pad=0.01,rounding_size=0.025',
                     linewidth=lw, edgecolor=LINE, facecolor=face)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fontsize, fontweight=weight, color=INK)
    return p

def arrow(ax, start, end, text=None, text_offset=(0,0)):
    a=FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=11, lw=0.95, color=LINE, shrinkA=4, shrinkB=4)
    ax.add_patch(a)
    if text:
        ax.text((start[0]+end[0])/2 + text_offset[0], (start[1]+end[1])/2 + text_offset[1], text, ha='center', va='center', fontsize=7.2, color=LINE)

def main():
    # Read sources for provenance; fixed coordinates intentionally preserve design quality.
    entities = pd.read_csv(ROOT / 'figure_sources' / 'figure2_schema_entities.csv')
    relationships = pd.read_csv(ROOT / 'figure_sources' / 'figure2_schema_relationships.csv')
    fig, ax = plt.subplots(figsize=(9.3, 5.0))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')

    # Backbone entities
    package = box(ax, (0.355,0.83), 0.29,0.09, 'Curated package', face=ACCENT, weight='bold', fontsize=10)
    session = box(ax, (0.38,0.67), 0.24,0.085, 'Public session', face=BOX, weight='bold')
    meas = box(ax, (0.35,0.48), 0.30,0.105, 'Measurement record', face=BOX, weight='bold')
    arrow(ax, (0.5,0.83), (0.5,0.755), 'contains', (0.055,0.0))
    arrow(ax, (0.5,0.67), (0.5,0.585), 'has', (0.032,0.0))

    # Attribute row
    labels = [('Variable',0.055),('Unit',0.205),('Device source',0.355),('Measurement\nlevel',0.505),('QC flag',0.655),('Release tier',0.805)]
    for label,x in labels:
        b = box(ax, (x,0.205), 0.135,0.09, label, face=BOX_ALT, fontsize=8.4, lw=0.8)
        arrow(ax, (0.5,0.48), (x+0.0675,0.295))

    # Side notes as controlled, non-clinical boundaries
    side = FancyBboxPatch((0.055,0.035),0.89,0.085,boxstyle='round,pad=0.01,rounding_size=0.02', linewidth=0.75, edgecolor=LINE, facecolor=PANEL)
    ax.add_patch(side)
    ax.text(0.5,0.078,'Schema-first curation preserves provenance and release tier; no clinical or standards-compliance claim.',
            ha='center', va='center', fontsize=8.0, color=INK)

    # Contextual labels
    ax.text(0.13,0.405,'public-minimised\nview', ha='center', va='center', fontsize=7.4, color=LINE)
    ax.plot([0.21,0.79], [0.38,0.38], color=LINE, lw=0.6, linestyle=(0,(2,2)))
    ax.text(0.79,0.405,'metadata-bound\nattributes', ha='center', va='center', fontsize=7.4, color=LINE)

    save_all(fig, ROOT / 'figures', 'Figure_2_schema_first_model_v6_8_2')
    plt.close(fig)

if __name__ == '__main__':
    main()
