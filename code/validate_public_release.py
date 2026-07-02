#!/usr/bin/env python3
"""Validate the v6.8.2 public-minimised release boundary, schemas and checksums."""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, re, sys
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--root', default=None, help='Package root. Defaults to repository root inferred from this script.')
args = parser.parse_args()
root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
blocked_dirs={"withheld_source_layer", "withheld_intermediate_layer", "data_raw", "data_intermediate", "__pycache__"}
blocked_ext={'.wav', '.pyc', '.pyo'}
blocked_file_names={'.DS_Store','Thumbs.db'}
blocked_terms=[
    "zenodo_original", "raw archive", "ECG PDF reports", "phonocardiographic WAV audio",
    "contextual activity notes", "author-participant", "participant_context", "light headache"
]
allowed_context_markers=['excluded','withheld','outside the public release boundary','not part of this public package']
skip_text_scan={
    'code/validate_public_release.py',
    'metadata/schema_public_wide_v6_8_2.json',
    'metadata/schema_public_long_v6_8_2.json',
    'metadata/schema_public_dictionary_v6_8_2.json'
}
manifest=root/'file_checksums_sha256.txt'
if not manifest.exists():
    errors.append('Missing: file_checksums_sha256.txt')
else:
    for line in manifest.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            h, rel = line.split('  ', 1)
        except ValueError:
            errors.append(f'Malformed manifest line: {line}')
            continue
        p=root/rel
        if not p.exists():
            errors.append(f'Missing: {rel}')
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=h:
            errors.append(f'Checksum mismatch: {rel}')
for p in root.rglob('*'):
    rel=p.relative_to(root)
    rel_str=rel.as_posix()
    if any(part in blocked_dirs for part in rel.parts):
        errors.append(f'Blocked directory/cache present: {rel_str}')
    if p.is_file():
        if p.name in blocked_file_names:
            errors.append(f'Blocked OS/cache file present: {rel_str}')
        suffix=p.suffix.lower()
        if suffix in blocked_ext:
            errors.append(f'Blocked binary/cache/source-media file present: {rel_str}')
        if suffix == '.pdf':
            allowed = (rel.parts[0] in {'figures', 'supplementary_figures'} and p.name.startswith('Figure_'))
            if not allowed:
                errors.append(f'Blocked non-figure PDF present: {rel_str}')
        if suffix in {'.md','.txt','.json','.csv','.cff','.py'} and rel_str not in skip_text_scan:
            try: txt=p.read_text(encoding='utf-8')
            except UnicodeDecodeError: txt=''
            low=txt.lower()
            for term in blocked_terms:
                if term.lower() in low and not any(m in low for m in allowed_context_markers):
                    errors.append(f"Potentially unsafe public text term '{term}' in {rel_str}")

def load_json(rel):
    p=root/rel
    if not p.exists():
        errors.append(f'Missing schema: {rel}')
        return None
    return json.loads(p.read_text(encoding='utf-8'))
wide_schema=load_json('metadata/schema_public_wide_v6_8_2.json')
long_schema=load_json('metadata/schema_public_long_v6_8_2.json')
dict_schema=load_json('metadata/schema_public_dictionary_v6_8_2.json')
try:
    wide=pd.read_csv(root/'data_processed_public'/'clean_measurements_wide_public_minimised.csv')
    long=pd.read_csv(root/'data_processed_public'/'clean_measurements_long_public_minimised.csv')
    dd=pd.read_csv(root/'data_processed_public'/'data_dictionary_public_minimised.csv')
except Exception as exc:
    errors.append(f'Unable to read public tables: {exc}')
    wide=long=dd=None
if wide is not None and wide_schema:
    if list(wide.columns)!=wide_schema['required_columns']:
        errors.append('Wide table columns do not match schema_public_wide_v6_8_2.json')
    if len(wide)!=wide_schema['expected_rows']:
        errors.append(f"Wide table row count {len(wide)} != expected {wide_schema['expected_rows']}")
    present=set(wide_schema.get('forbidden_columns', [])).intersection(wide.columns)
    if present:
        errors.append(f'Forbidden wide columns present: {sorted(present)}')
    if not wide['public_session_id'].astype(str).str.match(r'^S[0-9]{3}$').all():
        errors.append('public_session_id does not match S001-style public pattern')
if long is not None and long_schema:
    if list(long.columns)!=long_schema['required_columns']:
        errors.append('Long table columns do not match schema_public_long_v6_8_2.json')
    bad=set(long['variable_name'].dropna().unique())-set(long_schema.get('allowed_variable_names', []))
    if bad:
        errors.append(f'Long table has variable_name values outside schema: {sorted(bad)}')
if dd is not None and dict_schema and wide is not None:
    if list(dd.columns)!=dict_schema['required_columns']:
        errors.append('Data dictionary columns do not match schema_public_dictionary_v6_8_2.json')
    if set(dd['variable_name'])!=set(wide.columns):
        errors.append('Data dictionary variable_name values do not match wide table columns')
if errors:
    print('FAIL')
    print('\n'.join(errors))
    sys.exit(1)
print('PASS: v6.8.2 public-release integrity, schema and boundary audit')
