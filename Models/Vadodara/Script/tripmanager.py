import os 
import sys
import xml.etree.ElementTree as ET
import traci
from xml.dom import minidom
import sumolib
import math
import pandas as pd
import random
import numpy as np

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

network = sumolib.net.readNet(network_path)

PROCESS_MOTORCYCLE = True
PROCESS_PASSENGER = True
PROCESS_PEDESTRIAN = False
# Functions for file handling and data manipulation

def get_route_files_from_config(config_path):
    """
    Extracts route file paths from a SUMO configuration file.
    
    Args:
        config_path (str): Path to the SUMO configuration file.

    Returns:
        list: List of absolute paths to the route files mentioned in the configuration.
    """
    tree = ET.parse(config_path)
    root = tree.getroot()
    input_section = root.find('input')
    if input_section is not None:
        route_files_tag = input_section.find("route-files")
        if route_files_tag is not None:
            route_files = route_files_tag.get('value').split(',')
            return [os.path.abspath(os.path.join(script_directory, "..", route_file.strip())) for route_file in route_files]
    return []


def gather_data(route_files):
    """
    Gathers vehicle and pedestrian data from multiple route files.
    
    Args:
        route_files (list): List of paths to the route files.

    Returns:
        dict: Dictionary containing categorized vehicle and pedestrian data.
    """
    vehicle_data_dict = {'motorcycle': [], 'passenger': [], 'pedestrian': []}

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
    """
    Extracts trip and pedestrian data from a route file.
    
    Args:
        route_file (str): Path to the route file.

    Returns:
        list: List of dictionaries containing data for trips or pedestrians.
    """
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


def geo_to_cartesian(lat, lon, config_file):
    """
    Converts geographical coordinates to Cartesian coordinates using SUMO.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        config_file (str): Path to the SUMO configuration file.

    Returns:
        tuple: Cartesian coordinates (x, y) or None in case of error.
    """
    sumoCmd = ["sumo", "-c", config_file]
    try:
        traci.start(sumoCmd)
        x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        return x, y
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
    finally:
        traci.close()


def geo_to_edges(where, config_file=conf, network=network):
    """
    Finds the nearest edges within a radius of geographical coordinates and filters by allowed vehicle classes ('motorcycle' or 'passenger').

    Args:
        where (dict): Dictionary with keys 'lat', 'lon', and 'radius'.
        config_file (str): Path to the SUMO configuration file.
        network (sumolib.net.Net): The SUMO network object.

    Returns:
        dict: Dictionary containing filtered edges for both 'motorcycle' and 'passenger' vehicle classes.
    """
    if where:
        lat = where['lat']
        lon = where['lon']
        r = where['radius']
        sumoCmd = ["sumo", "-c", config_file]

        try:
            # Start SUMO simulation
            traci.start(sumoCmd)

            # Convert geographical coordinates to simulation coordinates
            x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

            # Find neighboring edges within the specified radius
            neighboring_edges = network.getNeighboringEdges(x, y, r=r, includeJunctions=True, allowFallback=True)

            # Initialize dictionaries to hold filtered edges for each vclass
            filtered_edges = {
                'motorcycle': [],
                'passenger': []
            }

            # Iterate through edges and filter based on vehicle classes
            for edge, _ in neighboring_edges:
                edge_obj = network.getEdge(edge.getID())
                
                # Check if the edge allows 'motorcycle'
                if edge_obj.allows('motorcycle'):
                    filtered_edges['motorcycle'].append(edge.getID())
                
                # Check if the edge allows 'passenger'
                if edge_obj.allows('passenger'):
                    filtered_edges['passenger'].append(edge.getID())

            return filtered_edges

        except Exception as e:
            print(f"Error during edge filtering: {e}")
            return {'motorcycle': [], 'passenger': []}

        finally:
            traci.close()
    else:
        return {'motorcycle': [], 'passenger': []}



def make_df(raw_dict):
    """
    Converts raw data dictionary to pandas DataFrames.
    
    Args:
        raw_dict (dict): Dictionary containing raw data lists.

    Returns:
        dict: Dictionary of pandas DataFrames.
    """
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
    """
    Updates a specified column in DataFrames based on filtering and new values.
    
    Args:
        df_dict (dict): Dictionary of pandas DataFrames.
        colname (str): Column name to update.
        filter_list (list): List of values to filter rows by.
        listt (list or scalar): New values to update with.

    Returns:
        dict: Updated dictionary of pandas DataFrames.
    """
    for key, df in df_dict.items():
        if df.empty:
            print(f"Warning: DataFrame with key '{key}' is empty. Skipping.")
            continue

        if colname not in df.columns:
            print(f"Warning: Column '{colname}' does not exist in DataFrame with key '{key}'. Skipping.")
            continue

        if filter_list:
            mask = df[colname].isin(filter_list)
        else:
            mask = pd.Series(True, index=df.index)

        if isinstance(listt, list):
            if len(listt) > 1:
                random_values = [random.choice(listt) for _ in range(mask.sum())]
                df.loc[mask, colname] = random_values
            elif len(listt) == 1:
                df.loc[mask, colname] = listt[0]
            else:
                raise ValueError("The 'listt' parameter is an empty list.")
        else:
            df.loc[mask, colname] = listt

        df_dict[key] = df

    return df_dict

def generate_entries(df, noOfEntries, name, delay=10, from_list=None, to_list=None):
    """
    Generate new sequential entries for the DataFrame ensuring depart times continue from the last entry.

    Args:
        df (DataFrame): Existing pandas DataFrame containing vehicle/person data.
        noOfEntries (int): Number of new entries to generate.
        name (str): Type of entity ('motorcycle', 'passenger', 'pedestrian').
        delay (int): Time interval between subsequent departures.
        from_list (list): List of starting points (e.g., edges).
        to_list (list): List of destination points (e.g., edges).

    Yields:
        dict: New entry for each vehicle/person.
    """
    if not df.empty:
        last_id = df['id'].iloc[-1]
        prefix = ''.join([i for i in last_id if not i.isdigit()])
        last_count = int(''.join(filter(str.isdigit, last_id)))
        last_depart = float(df['depart'].iloc[-1])
    else:
        prefix, last_count, last_depart = "entry", 0, 0.0

    type_mapping = {
        'motorcycle': 'motorcycle_motorcycle',
        'passenger': 'veh_passenger',
        'pedestrian': 'ped_pedestrian'
    }
    df_type = type_mapping.get(name, 'unknown_type')

    departLane = 'best'

    for i in range(1, noOfEntries + 1):
        new_id = f"{prefix}{last_count + i}"
        new_depart = last_depart + (delay * i)
        from_value = random.choice(from_list) if len(from_list) > 1 else from_list[0]
        to_value = random.choice(to_list) if len(to_list) > 1 else to_list[0]

        new_entry = {
            'id': new_id,
            'type': df_type,
            'depart': f"{new_depart:.2f}",
            'departLane': departLane,
            'from': from_value,
            'to': to_value
        }

        if 'walk_edges' in df.columns:
            new_entry['walk_edges'] = [from_value, to_value]

        yield new_entry


def update_data(vehicle_data_dict):
    """
    Updates the route files with modified or new vehicle/pedestrian data.

    Args:
        vehicle_data_dict (dict): Dictionary containing updated vehicle/pedestrian data categorized by type.
    """
    paths = get_route_files_from_config(conf)
    for key, updated_items in vehicle_data_dict.items():
        if (key == 'motorcycle' and PROCESS_MOTORCYCLE) or \
           (key == 'passenger' and PROCESS_PASSENGER) or \
           (key == 'pedestrian' and PROCESS_PEDESTRIAN):
            for path in paths:
                if key in os.path.basename(path):
                    if os.path.exists(path) and os.path.getsize(path) == 0:
                        print(f"File {path} is empty, creating structure.")
                        initialize_file_structure(path)
                    update_file(path, updated_items)


def update_file(file_path, updated_items):
    """
    Updates an individual route file with the provided data.

    Args:
        file_path (str): Path to the route file.
        updated_items (list or dict): Updated data to be added to the file.
    """
    print(f"Updating file: {file_path}")

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"File {file_path} is empty, creating structure.")
        initialize_file_structure(file_path)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        print(f"File {file_path} is malformed, creating structure.")
        initialize_file_structure(file_path)
        tree = ET.parse(file_path)
        root = tree.getroot()

    clean_file(root)

    if isinstance(updated_items, list):
        updated_items_dict = {item['id']: item for item in updated_items}
    else:
        updated_items_dict = {updated_items['id']: updated_items}

    trips_to_remove = []
    for element in root.findall('trip'):
        element_id = element.get('id')
        if element_id not in updated_items_dict:
            trips_to_remove.append(element)
        else:
            updated_data = updated_items_dict.pop(element_id)
            for key, value in updated_data.items():
                if key != "walk_edges":
                    element.set(key, value)

    for trip in trips_to_remove:
        root.remove(trip)

    for new_item in updated_items_dict.values():
        if 'walk_edges' not in new_item:
            new_element = ET.Element('trip')
            for key, value in new_item.items():
                if key != "walk_edges":
                    new_element.set(key, value)
            root.append(new_element)

    for new_item in updated_items_dict.values():
        if 'walk_edges' in new_item:
            existing_person = root.find(f".//person[@id='{new_item['id']}']")

            if existing_person is not None:
                root.remove(existing_person)

            new_element = ET.Element('person', {'id': new_item['id'], 'type': new_item['type'], 'depart': new_item['depart']})
            walk_element = ET.Element('walk', {'edges': " ".join(new_item['walk_edges'])})
            new_element.append(walk_element)
            root.append(new_element)

    xml_str = ET.tostring(root, 'utf-8')
    try:
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
        lines = pretty_xml_str.splitlines()
        if lines[0].startswith('<?xml'):
            lines = lines[1:]
        lines = [line.rstrip() for line in lines if line.strip()]

        with open(file_path, 'w') as file:
            file.write("\n".join(lines) + "\n")
        print(f"File {file_path} updated successfully.")
    except Exception as e:
        print(f"Error during writing formatted XML: {e}")


def initialize_file_structure(file_path):
    """
    Initializes the structure of a route file based on its type.

    Args:
        file_path (str): Path to the route file.
    """
    root = ET.Element('routes')

    if "motorcycle" in file_path and PROCESS_MOTORCYCLE:
        create_motorcycle_structure(root)
    elif "passenger" in file_path and PROCESS_PASSENGER:
        create_passenger_structure(root)
    elif "pedestrian" in file_path and PROCESS_PEDESTRIAN:
        create_pedestrian_structure(root)
    else:
        print(f"Skipping initialization for {file_path}.")

    tree = ET.ElementTree(root)
    tree.write(file_path)


def create_motorcycle_structure(root):
    """
    Creates the base structure for motorcycle routes.

    Args:
        root (Element): Root XML element to append the structure to.
    """
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")
    vType = ET.Element('vType', {'id': 'motorcycle_motorcycle', 'vClass': 'motorcycle'})
    root.append(vType)

    trip = ET.Element('trip', {
        'id': 'motorcycle0',
        'type': 'motorcycle_motorcycle',
        'depart': '0.00',
        'departLane': 'best',
        'from': '-29875672#0',
        'to': '29873772#5'
    })
    root.append(trip)


def create_passenger_structure(root):
    """
    Creates the base structure for passenger vehicle routes.

    Args:
        root (Element): Root XML element to append the structure to.
    """
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")
    vType = ET.Element('vType', {'id': 'veh_passenger', 'vClass': 'passenger'})
    root.append(vType)

    trip = ET.Element('trip', {
        'id': 'veh0',
        'type': 'veh_passenger',
        'depart': '0.00',
        'departLane': 'best',
        'from': '29875742',
        'to': '-29873850'
    })
    root.append(trip)


def create_pedestrian_structure(root):
    """
    Creates the base structure for pedestrian routes.

    Args:
        root (Element): Root XML element to append the structure to.
    """
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")
    vType = ET.Element('vType', {'id': 'ped_pedestrian', 'vClass': 'pedestrian'})
    root.append(vType)

    person = ET.Element('person', {'id': 'ped0', 'type': 'ped_pedestrian', 'depart': '0.00'})
    walk = ET.Element('walk', {'edges': '29875742 29873850'})
    person.append(walk)
    root.append(person)


def clean_file(root):
    """
    Removes any invalid or empty trips/persons from the XML root element.

    Args:
        root (Element): Root XML element to clean.
    """
    for element in root.findall('trip') + root.findall('person'):
        if not element.get('id'):
            root.remove(element)

