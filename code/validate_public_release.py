#!/usr/bin/env python3
"""Validate the public-minimised release boundary and checksums."""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parents[1]
errors=[]

# Manifest verification
with (root / "file_checksums_sha256.txt").open() as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        h, rel = line.split("  ", 1)
        p=root/rel
        if not p.exists():
            errors.append(f"Missing: {rel}")
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=h:
            errors.append(f"Checksum mismatch: {rel}")

blocked_dirs={"withheld_source_layer", "withheld_intermediate_layer", "data_raw", "data_intermediate"}
blocked_terms=[
    "zenodo_original", "raw archive", "ECG PDF reports", "phonocardiographic WAV audio",
    "contextual activity notes", "author-participant", "participant_context"
]

for p in root.rglob('*'):
    rel=p.relative_to(root)
    rel_str=rel.as_posix()
    if any(part in blocked_dirs for part in rel.parts):
        errors.append(f"Blocked directory present: {rel_str}")
    if p.is_file():
        suffix=p.suffix.lower()
        # WAV is always disallowed in public release.
        if suffix == '.wav':
            errors.append(f"Blocked source-audio file present: {rel_str}")
        # PDF is allowed only for generated figure artwork in figures folders.
        if suffix == '.pdf':
            allowed = (rel.parts[0] in {"figures", "supplementary_figures"} and p.name.startswith('Figure_'))
            if not allowed:
                errors.append(f"Blocked non-figure PDF present: {rel_str}")
        if suffix in {'.md', '.txt', '.json', '.csv', '.cff', '.py'}:
            try:
                txt=p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                txt=''
            for term in blocked_terms:
                if term in txt and 'excluded' not in txt.lower() and 'withheld' not in txt.lower():
                    errors.append(f"Potentially unsafe public text term '{term}' in {rel_str}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print("PASS: public-release integrity and boundary audit")
