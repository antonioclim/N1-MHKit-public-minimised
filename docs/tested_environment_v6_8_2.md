# Tested environment (v6.8.2 JCIS compliance)

The public-package audit was executed in the container environment used for preparation of the v6.8.2 figure-1-repair release.

Tested Python/runtime stack in this audit:

- Python: 3.13.5
- pandas: 2.2.3

Matplotlib and NumPy versions are reported by `code/requirements-lock-v6_8_2.txt` where installed. Figure rendering may differ at the byte level across platforms, but the supplied PDF/SVG/PNG/TIFF files are the audited publication-ready exports.
