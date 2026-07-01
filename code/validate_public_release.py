#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
root = Path(__file__).resolve().parents[1]
errors=[]
with (root / "file_checksums_sha256.txt").open() as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'): continue
        h, rel = line.split("  ", 1)
        p=root/rel
        if not p.exists(): errors.append(f"Missing: {rel}"); continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=h: errors.append(f"Checksum mismatch: {rel}")
blocked_suffixes={bytes([46,119,97,118]).decode(), bytes([46,112,100,102]).decode()}
blocked_dirs={"withheld_source_layer", "withheld_intermediate_layer"}
for p in root.rglob('*'):
    rel=p.relative_to(root)
    if any(part in blocked_dirs for part in rel.parts): errors.append(f"Blocked directory present: {rel}")
    if p.is_file() and p.suffix.lower() in blocked_suffixes: errors.append(f"Blocked source-format file present: {rel}")
if errors:
    print("FAIL"); print("\n".join(errors)); sys.exit(1)
print("PASS: public-release integrity audit")
