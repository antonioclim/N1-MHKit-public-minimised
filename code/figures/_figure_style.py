#!/usr/bin/env python3
"""Shared visual settings for N1-MHKit manuscript figures.

These helpers use deterministic, non-generative, programmatic rendering. No
AI image-generation tool is used or required.
"""
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

BG = '#ffffff'
INK = '#1f2933'
LINE = '#5b6770'
PANEL = '#f7f8fa'
BOX = '#ffffff'
BOX_ALT = '#eef2f6'
RESTRICTED = '#f3f4f6'
WITHHELD = '#eceff1'
ACCENT = '#d8dee6'

mpl.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9,
    'axes.edgecolor': LINE,
    'axes.labelcolor': INK,
    'xtick.color': INK,
    'ytick.color': INK,
    'text.color': INK,
    'figure.facecolor': BG,
    'savefig.facecolor': BG,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'svg.hashsalt': 'n1mhkit-v6-8-2-jcis-compliance',
})

def save_all(fig, out_dir: Path, stem: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    metadata = {'Creator': 'N1-MHKit programmatic figure script', 'Title': stem}
    fig.savefig(out_dir / f'{stem}.png', dpi=600, bbox_inches='tight', pad_inches=0.03, metadata=metadata)
    try:
        fig.savefig(out_dir / f'{stem}.tiff', dpi=1200, bbox_inches='tight', pad_inches=0.03, pil_kwargs={'compression': 'tiff_lzw'})
    except TypeError:
        fig.savefig(out_dir / f'{stem}.tiff', dpi=1200, bbox_inches='tight', pad_inches=0.03)
    
    svg_path = out_dir / f'{stem}.svg'
    fig.savefig(svg_path, bbox_inches='tight', pad_inches=0.03, metadata=metadata)
    # Matplotlib may insert a render-time dc:date into SVG. Replace it with a
    # fixed value so that repeated figure generation is auditable.
    try:
        txt = svg_path.read_text(encoding='utf-8')
        import re
        txt = re.sub(r'<dc:date>.*?</dc:date>', '<dc:date>2026-07-01T00:00:00</dc:date>', txt)
        svg_path.write_text(txt, encoding='utf-8')
    except Exception:
        pass
    try:
        fig.savefig(out_dir / f'{stem}.pdf', bbox_inches='tight', pad_inches=0.03, metadata={'Creator': metadata['Creator'], 'Title': metadata['Title'], 'CreationDate': None, 'ModDate': None})
    except Exception:
        fig.savefig(out_dir / f'{stem}.pdf', bbox_inches='tight', pad_inches=0.03)
