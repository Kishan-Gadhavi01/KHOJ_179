import os
import xml.etree.ElementTree as ET
import pandas as pd
import random

from utils import get_route_files_from_config
from file_manager import initialize_file_structure

PROCESS_MOTORCYCLE = True
PROCESS_PASSENGER = True
PROCESS_PEDESTRIAN = False

def gather_data(route_files):
    vehicle_data_dict = {
        'motorcycle': [],
        'passenger': [],
        'pedestrian': []
    }

    for path in route_files:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print(f"File {path} is empty or does not exist. Initializing the structure.")
            initialize_file_structure(path)

        filename = os.path.basename(path)
        key = filename.split('.')[1]

        if key == 'motorcycle' and PROCESS_MOTORCYCLE:
            vehicle_data = extract_data(path)
            vehicle_data_dict['motorcycle'].extend(vehicle_data)
        elif key == 'passenger' and PROCESS_PASSENGER:
            vehicle_data = extract_data(path)
            vehicle_data_dict['passenger'].extend(vehicle_data)
        elif key == 'pedestrian' and PROCESS_PEDESTRIAN:
            vehicle_data = extract_data(path)
            vehicle_data_dict['pedestrian'].extend(vehicle_data)

    return vehicle_data_dict

def extract_data(route_file):
    data = []
    try:
        tree = ET.parse(route_file)
        root = tree.getroot()

        if root.tag == 'routes':
            for trip in root.findall('trip'):
                vehicle_info = {attr: trip.get(attr) for attr in trip.keys()}
                data.append(vehicle_info)

            for person in root.findall('person'):
                pedestrian_info = {attr: person.get(attr) for attr in person.keys()}
                walk = person.find('walk')
                if walk is not None:
                    pedestrian_info['walk_edges'] = walk.get('edges').split()
                data.append(pedestrian_info)
    except ET.ParseError:
        pass
    return data

def make_df(raw_dict):
    dataframes = {}
    for key, value in raw_dict.items():
        if isinstance(value, list):
            try:
                dataframes[key] = pd.DataFrame(value)
            except Exception as e:
                dataframes[key] = None
        else:
            dataframes[key] = None
    return dataframes

def update_column(df_dict, colname, filter_list=None, listt=None):
    for key, df in df_dict.items():
        # Skip empty DataFrames
        if df.empty:
            print(f"Warning: DataFrame with key '{key}' is empty. Skipping.")
            continue

        # Skip DataFrames that don't contain the specified column
        if colname not in df.columns:
            print(f"Warning: Column '{colname}' does not exist in DataFrame with key '{key}'. Skipping.")
            continue

        # Create a mask based on the filter_list
        if filter_list:
            mask = df[colname].isin(filter_list)
        else:
            mask = pd.Series(True, index=df.index)  # Select all rows if no filter_list

        # Update column based on listt
        if isinstance(listt, list):
            if len(listt) > 1:
                # Generate random values for filtered rows
                random_values = [random.choice(listt) for _ in range(mask.sum())]
                df.loc[mask, colname] = random_values
            elif len(listt) == 1:
                # Assign single value from listt
                df.loc[mask, colname] = listt[0]
            else:
                raise ValueError("The 'listt' parameter is an empty list.")
        else:
            # Assign scalar value directly
            df.loc[mask, colname] = listt

        # Update the dictionary with the modified DataFrame
        df_dict[key] = df

    return df_dict