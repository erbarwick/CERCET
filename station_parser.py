# Parses all Caltrans PeMS station metadata files from the station_metadata/
# directory, builds a full change log of historical station records, and merges
# the latest values (keyed on station ID) into the existing all_stations.csv.
# Existing values are never overwritten — metadata only fills gaps.
# Outputs: all_stations_merged.csv and station_change_log.csv

import pandas as pd
import os
import re
from pathlib import Path

os.chdir('/Volumes/WAVE/VAULT_WAVE/Research/CERCET/data')

# Load existing stations df
df = pd.read_csv('all_stations.csv', sep='\t', engine='python', on_bad_lines='skip')

# ── 1. Parse all metadata files ──────────────────────────────────────────────
META_ROOT = Path('station_metadata')

def parse_date_from_filename(fname):
    """Extract date from e.g. d03_text_meta_2024_04_08.txt"""
    m = re.search(r'(\d{4})_(\d{2})_(\d{2})', fname)
    if m:
        return pd.Timestamp(f"{m.group(1)}-{m.group(2)}-{m.group(3)}")
    return pd.NaT

all_records = []

for district_dir in sorted(META_ROOT.iterdir()):
    if not district_dir.is_dir():
        continue
    for fpath in sorted(district_dir.glob('*.txt')):
        file_date = parse_date_from_filename(fpath.name)
        try:
            tmp = pd.read_csv(
                fpath, sep='\t', engine='python',
                on_bad_lines='skip' 
            )
            tmp.columns = tmp.columns.str.strip()
            tmp['_file_date'] = file_date
            tmp['_source_file'] = fpath.name
            all_records.append(tmp)
        except Exception as e:
            print(f"Skipping {fpath.name}: {e}")

print(f"Parsed {len(all_records)} files")
meta_df = pd.concat(all_records, ignore_index=True)
print(f"Total metadata rows: {len(meta_df)}")

# ── 2. Normalise the ID column ────────────────────────────────────────────────
meta_df['ID'] = pd.to_numeric(meta_df['ID'], errors='coerce')
meta_df.dropna(subset=['ID'], inplace=True)
meta_df['ID'] = meta_df['ID'].astype(int)

# ── 3. Build change log (all historical records per station) ──────────────────
change_log = (
    meta_df
    .sort_values(['ID', '_file_date'])
    .reset_index(drop=True)
)
change_log.to_csv('station_change_log.csv', index=False)
print("Change log saved → station_change_log.csv")

# ── 4. Keep only the newest record per station ────────────────────────────────
meta_latest = (
    meta_df
    .sort_values('_file_date', ascending=False)
    .drop_duplicates(subset='ID', keep='first')
    .reset_index(drop=True)
)
print(f"Unique stations in metadata: {len(meta_latest)}")

# ── 5. Merge onto existing df (non-destructive) ───────────────────────────────
# Columns to bring in from metadata (add/extend only — never overwrite)
META_NEW_COLS = ['Latitude', 'Longitude', 'Dir', 'State_PM', 'Abs_PM',
                 'Length', 'Type', 'Lanes', 'Name', 'User_ID_1',
                 '_file_date', '_source_file']

# Only keep cols that actually exist in meta_latest
META_NEW_COLS = [c for c in META_NEW_COLS if c in meta_latest.columns]

df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
df.dropna(subset=['ID'], inplace=True)
df['ID'] = df['ID'].astype(int)

meta_slim = meta_latest[['ID'] + META_NEW_COLS].copy()

# Left join — existing rows preserved, new cols added with suffix _meta
df_merged = df.merge(meta_slim, on='ID', how='left', suffixes=('', '_meta'))

# For each overlapping col, fill NaN in original with value from _meta version
for col in META_NEW_COLS:
    meta_col = col + '_meta'
    if meta_col in df_merged.columns:
        # Fill gaps in original; never overwrite existing values
        df_merged[col] = df_merged[col].combine_first(df_merged[meta_col])
        df_merged.drop(columns=[meta_col], inplace=True)

print(f"\nMerged df shape: {df_merged.shape}")
print(df_merged[['ID', 'Fwy', 'Latitude', 'Longitude', 'Dir']].head(10))

# ── 6. Save ───────────────────────────────────────────────────────────────────
df_merged.to_csv('all_stations_merged.csv', index=False)
print("\nSaved → all_stations_merged.csv")
