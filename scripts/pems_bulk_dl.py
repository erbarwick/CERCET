import os
import sys
import pandas as pd
from pathlib import Path

# ── PATH CONFIGURATION ───────────────────────────────────────────────────────
# 1. Find the script's directory (.../scripts)
SCRIPT_DIR = Path(__file__).resolve().parent

# 2. Find the root directory of the repo (one level up)
BASE_DIR = SCRIPT_DIR.parent

# 3. Target the specific directory containing the pems Python package
PEMS_MODULE_DIR = BASE_DIR / 'pems' / 'caltrans-pems'

# Add that specific directory to sys.path so Python finds the nested 'pems' folder
sys.path.insert(0, str(PEMS_MODULE_DIR))

# Local imports (from ../pems/caltrans-pems/pems/)
from pems.handler import PeMSHandler

# PeMS credentials
print("NOTE: This program will be accessing the PeMS site via http, which is unencrypted.")
print("Please make sure you do not use a password that you share with other sites.")

pems_user = input("Enter PeMS username/email: ")
pems_pass = input("Enter PeMS password: ")

# Connect to PeMS
pems = PeMSHandler(username=pems_user, password=pems_pass)

# Dictionary containing descriptions for labels 
pems_ref = pems.label_reference
print(pems_ref)

all_districts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

def inputParams():
    return

# View summary of available files for (start_year, end_year, districts, file_types) query
pems.get_file_types()

files = pems.get_files(
    start_year=2020,
    end_year=2026,
    districts=all_districts,
    file_types=['station_hour']
)

# Optional: explicitly define where you want the downloads to go in your new structure
download_dir = str(BASE_DIR / 'data' / 'station_hour_sample_data' / 'text_station_hour')

# files = pems.download_files(
#     start_year=2020,
#     end_year=2026,
#     districts=all_districts,
#     file_types=['station_hour'],
#     months=None,
#     save_path=download_dir
# )

# print(pd.DataFrame(files).head())
