import os
import sys
import pandas as pd

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(os.getcwd())))
from pems.handler import PeMSHandler

# PeMS credentials
print("NOTE: This program will be accessing the PeMS site via http, which is unencrypted. Please make sure you do not use a password that you share with other sites.")

pems_user = input("Enter PeMS username/email: ")
pems_pass = input("Enter PeMS password: ")

# Connect to PeMS
pems = PeMSHandler(username=pems_user, password=pems_pass)

# Dictionary containing descriptions for labels 
pems_ref = pems.label_reference
print(pems_ref)

# View available file types
# pems.get_file_types()

# {'fastrak_5min': 'FasTrak 5-Minute', 'gn_link_5min': 'Link 5-Minute', 'tmg_volume_day': 'Census Volume Day', 'reid_hour': 'Re-ID Hour', 'meta': 'Station Metadata', 'station_aadt': 'Station AADT', 'fastrak_locations': 'FasTrak Locations', 'tmg_trucks_day': 'Census Trucks Day', 'station_day': 'Station Day', 'chp_incidents_day': 'CHP Incidents Day', 'reid_raw': 'Re-ID Raw', 'station_hour': 'Station Hour', 'station_raw': 'Station Raw', 'fastrak_day': 'FasTrak Day', 'tmg_vclass_hour': 'Census V-Class Hour', 'station_5min': 'Station 5-Minute', 'fastrak_hour': 'FasTrak Hour', 'reid_5min': 'Re-ID 5-Minute', 'tmg_trucks_hour': 'Census Trucks Hour', 'tmg_vclass_day': 'Census V-Class Day', 'reid_locations': 'Re-ID Locations', 'tmg_station_configs': 'Census Station Configurations', 'chp_incidents_month': 'CHP Incidents Month'}

# View available districts for a file type
# pems.get_districts(file_type="meta")

all_districts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']


# Define parameters to use for querying the PeMS site
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

files = pems.download_files(
    start_year=2020,
    end_year=2026,
    districts=all_districts,
    file_types=['station_hour'],
    months=None
)

# pems.download_files(
#     start_year=2000,
#     end_year=2026,
#     districts=all_districts,
#     file_types=['meta'],
#     months=None
# )

# print(pd.DataFrame(files).head())


