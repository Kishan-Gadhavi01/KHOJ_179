import os
import sys
import xml.etree.ElementTree as ET
import traci
import sumolib

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

network = sumolib.net.readNet(network_path)

def get_route_files_from_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    input_section = root.find('input')
    if input_section is not None:
        route_files_tag = input_section.find("route-files")
        if route_files_tag is not None:
            route_files = route_files_tag.get('value').split(',')
            return [os.path.abspath(os.path.join(script_directory, "..", route_file.strip())) for route_file in route_files]
    return []

def generate_vehicle_data_dict(route_files, v=False):
    vehicle_data_dict = {}
    for path in route_files:
        key = path.split('.')[1]
        vehicle_data = extract_data(path)   
        if key in vehicle_data_dict:
            vehicle_data_dict[key].extend(vehicle_data)
        else:
            vehicle_data_dict[key] = vehicle_data        
            print(f"Current key: {key}, entries: {len(vehicle_data)}")
    return vehicle_data_dict

def extract_data(route_file):
    data = []
    tree = ET.parse(route_file)
    root = tree.getroot()
    if root.tag == 'routes':
        if root.findall('trip'):
            for trip in root.findall('trip'):
                vehicle_info = {
                    'id': trip.get('id'),
                    'type': trip.get('type'),
                    'depart_time': trip.get('depart'),
                    'from_edge': trip.get('from'),
                    'to_edge': trip.get('to'),
                    'depart_lane': trip.get('departLane', 'best')
                }
                data.append(vehicle_info)
        elif root.findall('person'):
            for person in root.findall('person'):
                pedestrian_info = {
                    'id': person.get('id'),
                    'type': person.get('type'),
                    'depart_time': person.get('depart'),
                    'walk_edges': person.find('walk').get('edges').split()
                }
                data.append(pedestrian_info)
    return data

def geo_to_cartesian(lat, lon, config_file):
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

def geo_TO_edges(lat, lon, config_file):
    sumoCmd = ["sumo", "-c", config_file]
    try:
        traci.start(sumoCmd)
        x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        nearest_edge = network.getNeighboringEdges(x, y, r=10, includeJunctions=True, allowFallback=True)
        return nearest_edge
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
    finally:
        traci.close()

if __name__ == "__main__":
    latitude = 22.349917 #cordinate avalable in map
    longitude = 73.173323 #cordinate avalable in map
    #geo_to_cartesian(latitude,longitude,conf)
    #edges=geo_TO_edges(latitude,longitude,conf)
    #print(edges) # Not sorted acording to docstring
    route_files = get_route_files_from_config(conf)
    vehicle_data_dict = generate_vehicle_data_dict(route_files)
    print(list(vehicle_data_dict.items())[2])
