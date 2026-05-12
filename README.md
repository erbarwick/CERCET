**FROM BOX:** unzip station_hour_sample_data.zip into this repo's /data/ folder after cloning if you want to use some sample data I've already downloaded. Otherwise you can use the bulk downloader script to get new data. Ensure it ends up in the `/data/station_hour_sample_data` folder to work properly. See the README in that folder for more info.

The station_metadata folder is also included in the Box, but you probably won't need that since the metadata is already merged into `all_stations_merged.csv`.
## Python setup:
Follow the guides in the `./scripts/` directory of this repository:
- [Installing Python WINDOWS](https://github.com/erbarwick/CERCET/blob/main/guides/Installing%20Python%20WINDOWS.md)
- [Installing Python MAC](https://github.com/erbarwick/CERCET/blob/main/guides/Installing%20Python%20MAC.md)
- [Creating Python virtual environments and installing packages](https://github.com/erbarwick/CERCET/blob/main/guides/Creating%20Python%20virtual%20environments%20and%20installing%20packages.md)

# Caltrans PeMS Data Manager

This repository provides a set of tools to download, parse, extract, and visualize Caltrans Performance Measurement System (PeMS) traffic data. 

**Source code is stored in the `./scripts/` directory** and **all data is stored in the `./data/` directory**.

## How to use this repository 
### Clone the repo
If you don't have `git` installed, follow the guide in the `./guides` folder of this repository: [Installing git on Windows or Mac](https://github.com/erbarwick/CERCET/blob/main/guides/Installing%20git%20on%20Windows%20or%20Mac.md).

Cloning the repository creates a new folder (directory) in whatever folder you run the command in, so keep in mind where you are. Run `pwd` to see your current working directory, then run these commands in Terminal (Mac) or PowerShell (Windows):
```sh
git clone https://github.com/erbarwick/CERCET.git
cd CERCET
```
### Install dependencies
**Guide:** [Creating Python virtual environments and installing packages](https://github.com/erbarwick/CERCET/blob/main/guides/Creating%20Python%20virtual%20environments%20and%20installing%20packages.md)
Before running anything, make sure you have the required Python libraries installed. In the root directory of the cloned repository (or whichever directory contains your `venv`), open Terminal or PowerShell and run:
```bash
python3 -m pip install -r requirements.txt
```
### Downloading new data from PeMS
If you need new data from PeMS, you'll use the bulk downloader at `./scripts/pems_bulk_dl.py`.

Since this script will download a large amount of data and take a long time to run depending on your parameters, I've kept it so you have to input your parameters in the script itself so you are absolutely sure of what you want it to fetch before you run it. If at any time you want to interrupt the script, go into the terminal running the script and press `Control+C` (in Visual Studio Code I believe there's just a button to stop the script).

You will have to edit this script in order to use it. This can be done with any text editor (Notepad, TextEdit, `nano`, `vim`) as long as you save and run the same file. An IDE like Visual Studio Code includes a text editor and you can run it easily in the same window as well.

The part you will have to change is commented out at the bottom of the script:
```python
#files = pems.download_files(
#	start_year=2020,
#	end_year=2026,
#	districts=all_districts,
#	file_types=['station_hour'],
#	months=None,
#	save_path=download_dir
#)
```
To use it, remove the hash (`#`) characters and at the beginning of each line. By default the script will print out all of the available `file_types` options, but I've pasted them below for easy reference. For each row, the first column (e.g. `'fastrak_5min'`) is the one you use for the script. 
You can have multiple `file_types` values if you wish, just put them in a `List` like this: `['station_hour', 'station_day', 'station_raw']` but be aware that this will take a long time and lots of disk space.
```
{'fastrak_5min': 'FasTrak 5-Minute', 
'gn_link_5min': 'Link 5-Minute',
'tmg_volume_day': 'Census Volume Day', 
'reid_hour': 'Re-ID Hour', 
'meta': 'Station Metadata', 
'station_aadt': 'Station AADT', 
'fastrak_locations': 'FasTrak Locations', 
'tmg_trucks_day': 'Census Trucks Day', 
'station_day': 'Station Day', 
'chp_incidents_day': 'CHP Incidents Day', 
'reid_raw': 'Re-ID Raw', 
'station_hour': 'Station Hour', 
'station_raw': 'Station Raw', 
'fastrak_day': 'FasTrak Day', 
'tmg_vclass_hour': 'Census V-Class Hour', 
'station_5min': 'Station 5-Minute', 
'fastrak_hour': 'FasTrak Hour', 
'reid_5min': 'Re-ID 5-Minute', 
'tmg_trucks_hour': 'Census Trucks Hour', 
'tmg_vclass_day': 'Census V-Class Day', 
'reid_locations': 'Re-ID Locations', 
'tmg_station_configs': 'Census Station Configurations', 'chp_incidents_month': 'CHP Incidents Month'}
```

To check if the files you want are available before downloading, uncomment this section and change the parameters.
```python
#files = pems.get_files(
#    start_year=2020,
#    end_year=2026,
#    districts=all_districts,
#    file_types=['station_hour']
#)
```
The other parameters can be changed; replace `start_year` and `end_year` with other integer values, replace `all_districts` with a string list of the Caltrans districts you want (e.g. `districts=['3', '4', '8']`).
`months` is also set to `None` by default to download all-year data, but you can specify specific months in a similar way (string list).

This script cannot filter by station ID or geography; you will have to download more data than you need at first, then use `map_stations.py` or `extract_stations.py` to filter. The files from this script will save to the `data` folder in your cloned repository.

Note: It will prompt you for your PeMS username and password in the terminal. 
### Update station metadata
If you've added new raw metadata text files to `data/station_metadata/`, you need to update the master list so the map and extraction tools have the correct coordinates:
```bash
python scripts/station_parser.py
```
This creates a new `all_stations_merged.csv` in the `data/` folder.

**You likely will not need to run this unless you specified the `meta` file type in the bulk downloader script.**

### Find stations on the map
Launch the interactive map:
```bash
python scripts/map_stations.py
```
After running this, open your web browser and go to `http://127.0.0.1:8050`. Use the sidebar to filter stations. Hover over dots on the map to see their **Station ID**.

### Extract Specific Station Data
Once you know which Station IDs you want to analyze, open `scripts/extract_stations.py` in a text editor.
1. Scroll down to the bottom where it says `if __name__ == "__main__":`.
2. Update the `STATIONS = [601100, 602285, 401137]` list with your desired IDs.
3. Update the `START` and `END` date strings.
4. Run the script:
```bash
python scripts/extract_stations.py
```
The script will print out table containing only the data you requested.

---
## What Each Script Does

All scripts are located in the `scripts/` folder and are configured to use data from the `/data/` folder.

### `pems_bulk_dl.py`
**Purpose:** Downloads raw hourly station data directly from the Caltrans PeMS database.
**How it works:** It asks for your PeMS credentials to log in, checks which files you already have (to avoid duplicate downloads), and saves new compressed text files (`.txt.gz`) into `data/station_hour_sample_data/text_station_hour/`.
Note: Takes a long time, if you're getting a big amount of data make sure you can keep it running for several hours. The script also uses HTTP (not HTTPS) to connect to the PeMS website, meaning your credentials are not encrypted. Because of this, **please ensure you don't use the same password for PeMS as you do for other sites.**

### `station_parser.py`
**Purpose:** Updates the master station list with the newest metadata.
**How it works:** It scans all the text files in `data/station_metadata/` to find the latest latitude, longitude, postmile, and lane configurations for every station. It merges this fresh data with `all_stations.csv` to create `all_stations_merged.csv`. 

### `map_stations.py`
**Purpose:** Creates an interactive web map to help you find and filter stations.
**How it works:** It launches a local Dash web app. You can filter stations by Type, District, Postmile (Absolute or CA), or Lat/Long coordinates.

### `extract_stations.py`
**Purpose:** Define your target stations and dates inside this script. It uses DuckDB to quickly query the Parquet files and return a clean, filtered Pandas DataFrame. It also includes a utility to convert raw `.txt.gz` files into `.parquet` files for faster processing.

---
## Directory Structure & Important Datasets

- **`/scripts/`**: various python scripts
- **`/pems/`**: Contains the internal web-scraping package (`caltrans-pems`) used to download data from the Caltrans website.
- **`/data/`**: The central location for all datasets.
  - `all_stations.csv`: The base list of PeMS stations.
  - `all_stations_merged.csv`: The main dataset for station metadata. This is generated by our scripts and contains the most up-to-date information, coordinates, and postmiles for every station.
  - `station_change_log.csv`: A historical record of changes to station metadata over time.
  - `station_metadata/`: A directory containing raw monthly metadata text files split by Caltrans District (d01 - d12).
  - `station_hour_sample_data/`: Contains the actual hourly traffic data (flow, occupancy, speed).
    - `text_station_hour/`: Raw `.txt.gz` files downloaded directly from PeMS.
    - `parquet_station_hour/`: PeMS downloaded data converted to `.parquet` faster querying in the scripts.
---