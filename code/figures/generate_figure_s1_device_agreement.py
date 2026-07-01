#!/usr/bin/env python3
"""Generate Supplementary Figure S1 from public-minimised paired values.

The plot is a provenance/data-quality illustration. It must not be interpreted as
clinical validation, medical-device validation, or population-level analysis.
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import INK, LINE, save_all

def main():
    cfg = json.loads((ROOT / 'figure_sources' / 'figure_s1_device_agreement_config.json').read_text(encoding='utf-8'))
    df = pd.read_csv(ROOT / cfg['input_csv'])
    ref = cfg['reference_column']; comp = cfg['comparison_column']
    pair = df[['public_session_id', ref, comp]].dropna().copy()
    pair['session_order'] = np.arange(1, len(pair)+1)
    pair['difference'] = pair[ref] - pair[comp]
    mean_diff = pair['difference'].mean()

    fig, ax = plt.subplots(figsize=(7.15, 5.20))
    ax.axhline(0, color=LINE, lw=0.85, linestyle=(0,(2,2)), zorder=0)
    ax.axhline(mean_diff, color=INK, lw=1.0, linestyle='-', zorder=0)
    ax.scatter(pair['session_order'], pair['difference'], s=22, facecolor='white', edgecolor=INK, linewidth=0.8, zorder=3)
    ax.plot(pair['session_order'], pair['difference'], color='#9aa3aa', lw=0.55, zorder=2)
    ax.set_xlabel('Paired public session order')
    ax.set_ylabel('SBP difference (mmHg)')
    ax.set_xlim(0.5, max(1, len(pair))+0.5)
    ypad=max(4, pair['difference'].abs().max()*0.14)
    ax.set_ylim(pair['difference'].min()-ypad, pair['difference'].max()+ypad)
    ax.text(0.985, 0.965, f'n={len(pair)} paired records; mean difference={mean_diff:.1f} mmHg',
            transform=ax.transAxes, ha='right', va='top', fontsize=7.6, color=LINE,
            bbox={'facecolor':'white', 'edgecolor':'none', 'pad':1.2, 'alpha':0.95})
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color(LINE); ax.spines['bottom'].set_color(LINE)
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(axis='y', color='#e2e6ea', linewidth=0.45)
    save_all(fig, ROOT / 'supplementary_figures', 'Figure_S1_provenance_paired_sbp_v6_7')
    plt.close(fig)

if __name__ == '__main__':
    main()
