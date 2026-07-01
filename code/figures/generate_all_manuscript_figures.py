#!/usr/bin/env python3
"""Regenerate all manuscript and supplementary figures for N1-MHKit."""
from pathlib import Path
import subprocess, sys

HERE = Path(__file__).resolve().parent
scripts = [
    'generate_figure1_artifact_architecture.py',
    'generate_figure2_schema_first_model.py',
    'generate_figure_s1_device_agreement.py',
]
for script in scripts:
    subprocess.run([sys.executable, str(HERE/script)], check=True)
print('PASS: regenerated Figure 1, Figure 2 and Figure S1')
