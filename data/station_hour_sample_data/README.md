# What this directory should look like:
You MUST start with at least one populated data directory here, whether in parquet form or txt.gz form. 
If you start with the `text_station_hour/` directory full of files downloaded using the PeMS bulk downloader tool, there is a line at the bottom of the `extract_stations.py` you can uncomment before running to run the txt.gz -> parquet tool. The parquet format is used by the script because it is much faster than parsing the txt.gz files.
The `.tsv` containing the fields for the downloaded dataset is not necessary for the scripts to function, but is kept here for reference.

`./parquet_station_hour/` (extractor script contains functionality to generate this parquet directory and its files if you give it the txt.gz directory)
    | dXX_text_station_hour_YYYY_MM.parquet
    | dXX_text_station_hour_YYYY_MM.parquet
    | dXX_text_station_hour_YYYY_MM.parquet
    | ...
`./text_station_hour/` (contains direct downloads from PeMS)
    | dXX_text_station_hour_YYYY_MM.txt.gz
    | dXX_text_station_hour_YYYY_MM.txt.gz
    | dXX_text_station_hour_YYYY_MM.txt.gz
    | ...
`./text_station_hour_fields.tsv` 
