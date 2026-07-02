#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
root = Path(__file__).resolve().parents[1]
wide = pd.read_csv(root / "data_processed_public" / "clean_measurements_wide_public_minimised.csv")
long = pd.read_csv(root / "data_processed_public" / "clean_measurements_long_public_minimised.csv")
dd = pd.read_csv(root / "data_processed_public" / "data_dictionary_public_minimised.csv")
assert len(wide) == 52, f"Expected 52 public sessions, got {len(wide)}"
assert {"public_session_id", "day_index", "time_of_day_category"}.issubset(wide.columns)
assert wide["public_session_id"].astype(str).str.match(r"^S[0-9]{3}$").all()
assert {"public_session_id", "day_index", "time_of_day_category", "variable_name", "value"}.issubset(long.columns)
assert set(dd["variable_name"]) == set(wide.columns)
print("PASS: v6.8.2 public-minimised package smoke test")
