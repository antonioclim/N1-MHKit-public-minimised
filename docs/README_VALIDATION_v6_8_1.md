# Public package validation (v6.8.1 figure-1 repair)

Run from the package root:

```bash
python code/public_package_smoke_test.py
python code/validate_public_release.py --root .
python code/figures/generate_all_manuscript_figures.py
python code/validate_public_release.py --root .
```

Expected result: all checks report PASS.
