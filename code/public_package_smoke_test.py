#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
root = Path(__file__).resolve().parents[1]
wide = pd.read_csv(root / "data_processed_public" / "clean_measurements_wide_public_minimised.csv")
long = pd.read_csv(root / "data_processed_public" / "clean_measurements_long_public_minimised.csv")
dd = pd.read_csv(root / "data_processed_public" / "data_dictionary_public_minimised.csv")
assert len(wide) == 52, f"Expected 52 public sessions, got {len(wide)}"
assert {"public_session_id", "day_index"}.issubset(wide.columns)
assert {"public_session_id", "day_index", "variable_name", "value"}.issubset(long.columns)
assert "variable_name" in dd.columns and dd["variable_name"].notna().all()
print("PASS: public-minimised package smoke test")
