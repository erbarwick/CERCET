import pandas as pd
import os
import duckdb
import glob2 as glob
from datetime import datetime
from pathlib import Path
# pyarrow also required for parquet

def fetch_data_duckdb(station_ids, start_date, end_date, metadata_path, parquet_dir):
    # 1. Read metadata to find required districts
    meta_df = pd.read_csv(metadata_path, usecols=['ID', 'District'])
    target_meta = meta_df[meta_df['ID'].isin(station_ids)]

    if target_meta.empty:
        raise ValueError("Station IDs not found in metadata.")

    districts = [f"{int(d):02d}" for d in target_meta['District'].unique()]

    # 2. Generate the required filepaths based on dates and districts.
    months_in_range = pd.period_range(start=start_date, end=end_date, freq='M')

    files_to_query = []
    for district in districts:
        for period in months_in_range:
            filename = f"d{district}_text_station_hour_{period.year}_{period.month:02d}.parquet"
            filepath = os.path.join(parquet_dir, filename)
            if os.path.exists(filepath):
                files_to_query.append(filepath)

    if not files_to_query:
        print("No matching parquet files found for this time range/district.")
        return pd.DataFrame()

    # 3. Use DuckDB to query the files directly using SQL
    print(f"Querying {len(files_to_query)} parquet files with DuckDB...")

    duckdb_file_list = [f"'{f}'" for f in files_to_query]
    files_string = ", ".join(duckdb_file_list)

    stations_tuple = tuple(station_ids)
    if len(station_ids) == 1:
        stations_string = f"({station_ids[0]})"
    else:
        stations_string = str(stations_tuple)

    # 4. Write the SQL query
    sql_query = f"""
        SELECT
            Timestamp,
            Station,
            "Total Flow",
            "Avg Speed"
        FROM read_parquet([{files_string}])
        WHERE Station IN {stations_string}
            AND Timestamp >= '{start_date}'
            AND Timestamp <= '{end_date}'
        ORDER BY Station, Timestamp
    """

    result_df = duckdb.query(sql_query).df()
    return result_df

def convert_txt_to_parquet(source_dir, dest_dir):
    """Converts PeMS txt.gz files to optimized Parquet files."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    col_names = [
        'Timestamp', 'Station', 'District', 'Route', 'Direction of Travel', 'Lane Type', 'Station Length', 'Samples', '% Observed', 'Total Flow', 'Avg Occupancy', 'Avg Speed', 'Delay (V_t=35)', 'Delay (V_t=40)', 'Delay (V_t=45)', 'Delay (V_t=50)', 'Delay (V_t=55)', 'Delay (V_t=60)',
        'Lane 1 Flow', 'Lane 1 Avg Occ', 'Lane 1 Avg Speed',
        'Lane 2 Flow', 'Lane 2 Avg Occ', 'Lane 2 Avg Speed',
        'Lane 3 Flow', 'Lane 3 Avg Occ', 'Lane 3 Avg Speed',
        'Lane 4 Flow', 'Lane 4 Avg Occ', 'Lane 4 Avg Speed',
        'Lane 5 Flow', 'Lane 5 Avg Occ', 'Lane 5 Avg Speed',
        'Lane 6 Flow', 'Lane 6 Avg Occ', 'Lane 6 Avg Speed',
        'Lane 7 Flow', 'Lane 7 Avg Occ', 'Lane 7 Avg Speed',
        'Lane 8 Flow', 'Lane 8 Avg Occ', 'Lane 8 Avg Speed'
    ]

    file_list = glob.glob(os.path.join(source_dir, "*.txt.gz"))
    print(f"Found {len(file_list)} files to convert.")

    for filepath in file_list:
        filename = os.path.basename(filepath)
        parquet_filename = filename.replace('.txt.gz', '.parquet')
        parquet_path = os.path.join(dest_dir, parquet_filename)

        if os.path.exists(parquet_path):
            continue

        print(f"Converting {filename}...")
        try:
            df = pd.read_csv(filepath, names=col_names, on_bad_lines='skip', low_memory=False)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
        except Exception as e:
            print(f"Error converting {filename}: {e}")

def fetch_station_data(station_ids, start_date, end_date, metadata_path, data_dir):
    """Fetches hourly station data for specific stations and date ranges."""
    print(f"Fetching data for {len(station_ids)} stations from {start_date} to {end_date}...")

    meta_df = pd.read_csv(metadata_path, usecols=['ID', 'District'])

    target_meta = meta_df[meta_df['ID'].isin(station_ids)]
    if target_meta.empty:
        raise ValueError("None of the provided Station IDs were found in the metadata.")

    districts = target_meta['District'].unique()
    formatted_districts = [f"{int(d):02d}" for d in districts]

    months_in_range = pd.period_range(start=start_date, end=end_date, freq='M')

    col_names = [
        'Timestamp', 'Station', 'District', 'Route', 'Direction of Travel', 'Lane Type', 'Station Length', 'Samples', '% Observed', 'Total Flow', 'Avg Occupancy', 'Avg Speed', 'Delay (V_t=35)', 'Delay (V_t=40)', 'Delay (V_t=45)', 'Delay (V_t=50)', 'Delay (V_t=55)', 'Delay (V_t=60)',
        'Lane 1 Flow', 'Lane 1 Avg Occ', 'Lane 1 Avg Speed',
        'Lane 2 Flow', 'Lane 2 Avg Occ', 'Lane 2 Avg Speed',
        'Lane 3 Flow', 'Lane 3 Avg Occ', 'Lane 3 Avg Speed',
        'Lane 4 Flow', 'Lane 4 Avg Occ', 'Lane 4 Avg Speed',
        'Lane 5 Flow', 'Lane 5 Avg Occ', 'Lane 5 Avg Speed',
        'Lane 6 Flow', 'Lane 6 Avg Occ', 'Lane 6 Avg Speed',
        'Lane 7 Flow', 'Lane 7 Avg Occ', 'Lane 7 Avg Speed',
        'Lane 8 Flow', 'Lane 8 Avg Occ', 'Lane 8 Avg Speed'
    ]
    cols_to_keep = ['Timestamp', 'Station', 'Total Flow', 'Avg Speed']

    all_filtered_data = []

    for district in formatted_districts:
        for period in months_in_range:
            year = period.year
            month = f"{period.month:02d}"

            filename = f"d{district}_text_station_hour_{year}_{month}.txt.gz"
            filepath = os.path.join(data_dir, filename)

            if not os.path.exists(filepath):
                continue

            try:
                chunk_iterator = pd.read_csv(
                    filepath,
                    names=col_names,
                    usecols=cols_to_keep,
                    chunksize=100000,
                    on_bad_lines='skip'
                )

                for chunk in chunk_iterator:
                    filtered_chunk = chunk[chunk['Station'].isin(station_ids)]
                    if not filtered_chunk.empty:
                        all_filtered_data.append(filtered_chunk)

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    if not all_filtered_data:
        return pd.DataFrame()

    final_df = pd.concat(all_filtered_data, ignore_index=True)
    final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp'])

    mask = (final_df['Timestamp'] >= start_date) & (final_df['Timestamp'] <= end_date)
    final_df = final_df.loc[mask]

    return final_df


if __name__ == "__main__":
    # PATH CONFIGURATION 
    SCRIPT_DIR = Path(__file__).resolve().parent
    DATA_DIR = SCRIPT_DIR.parent / 'data'

    META_FILE = DATA_DIR / 'all_stations_merged.csv'
    DATA_FOLDER = DATA_DIR / 'station_hour_sample_data' / 'text_station_hour'
    PARQUET_FOLDER = DATA_DIR / 'station_hour_sample_data' / 'parquet_station_hour'

    # CSV -> Parquet conversion (uncomment to run)
    # convert_txt_to_parquet(DATA_FOLDER, PARQUET_FOLDER)

    # Parameters to define
    STATIONS = [601100, 602285, 401137] # Define as many station IDs as you want in this list.
    START = '2020-07-01 00:00:00' # Define start and end dates, but keep this format.
    END = '2021-07-01 23:59:59'

    result_df = fetch_data_duckdb(STATIONS, START, END, META_FILE, PARQUET_FOLDER)

    print("\nExtraction complete.")
    print(result_df)
