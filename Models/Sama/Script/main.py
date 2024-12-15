import os
import sys
import xml.etree.ElementTree as ET
import traci
from xml.dom import minidom
import sumolib
import math
import pandas as pd
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))



script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

network = sumolib.net.readNet(network_path)

PROCESS_MOTORCYCLE = True
PROCESS_PASSENGER = True
PROCESS_PEDESTRIAN = False

class VehicleManager:
    def __init__(self):
        pass

    def add_vehicle(self, vehicle_id, vehicle_type, depart, from_edge, to_edge, depart_lane="best", speed=0):
        traci.vehicle.add(vehicle_id, routeID="", typeID=vehicle_type, depart=depart, departLane=depart_lane, departSpeed=speed)
        traci.vehicle.changeTarget(vehicle_id, to_edge)
        traci.vehicle.setRoute(vehicle_id, [from_edge, to_edge])

    def get_initial_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[0]

    def set_initial_position(self, vehicle_id, from_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[0] = from_edge
        traci.vehicle.setRoute(vehicle_id, route)

    def get_terminal_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[-1]

    def set_terminal_position(self, vehicle_id, to_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[-1] = to_edge
        traci.vehicle.setRoute(vehicle_id, route)

    def get_speed(self, vehicle_id):
        return traci.vehicle.getSpeed(vehicle_id)

    def set_speed(self, vehicle_id, speed):
        traci.vehicle.setSpeed(vehicle_id, speed)

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

def geo_TO_edges(where, config_file=conf):

    if where:

        lat=where['lat']
        lon=where['lon']
        r=where['radius']

        sumoCmd = ["sumo", "-c", config_file]
       
        try:
            traci.start(sumoCmd)
            x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
            nearest_edge = network.getNeighboringEdges(x, y, r=r, includeJunctions=True, allowFallback=True)
            return nearest_edge
        except Exception as e:
            print(f"Error during conversion: {e}")
            return None
        finally:
            traci.close()
    else:
        return None

   

############ //    




############ Data manipulation  
  
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

############ //     





############ File handling        

def update_data(vehicle_data_dict):
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
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")
    vType = ET.Element('vType', {'id': 'ped_pedestrian', 'vClass': 'pedestrian'})
    root.append(vType)

    person = ET.Element('person', {'id': 'ped0', 'type': 'ped_pedestrian', 'depart': '0.00'})
    walk = ET.Element('walk', {'edges': '29875742 29873850'})
    person.append(walk)
    root.append(person)

def clean_file(root):
    for element in root.findall('trip') + root.findall('person'):
        if not element.get('id'):
            root.remove(element)

############ //




############ File handling        

def create_filled_red_zone(lat, lon, radius, poly_id="red_zone"):
    """
    Creates a filled red circular overlay in SUMO at the given geolocation with the specified radius.
    """
    # Convert geolocation to SUMO Cartesian coordinates
    x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
    
    # Generate points for the circle approximation
    num_points = 72  # Higher values create a smoother circle
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        point_x = x + radius * math.cos(angle)
        point_y = y + radius * math.sin(angle)
        circle_points.append((point_x, point_y))
    
    # Add the polygon to SUMO with a semi-transparent red fill
    traci.polygon.add(
        polygonID=poly_id,
        shape=circle_points,
        color=(255, 0, 0, 127),  # Red color with 50% opacity
        layer=1
    )
    print(f"Filled red zone created with center at ({lat}, {lon}) and radius {radius}.")

def run_simulation(config_file, duration=1000, red_zone_data=None):
    """
    Runs the simulation for the specified duration and optionally creates a red zone.
    """
    sumoCmd = ["sumo-gui", "-c", config_file]
    traci.start(sumoCmd)

    # Create the red zone if data is provided
      # Create the red zone if data is provided
    if red_zone_data:
        print(f"Creating red zone with parameters: {red_zone_data}")
        create_filled_red_zone(
            lat=red_zone_data['lat'],
            lon=red_zone_data['lon'],
            radius=red_zone_data['radius']
        )

    vehicle_paths = {}

    for step in range(duration):
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        for vehicle_id in vehicle_ids:
            position = traci.vehicle.getPosition(vehicle_id)
            if vehicle_id not in vehicle_paths:
                vehicle_paths[vehicle_id] = []
            vehicle_paths[vehicle_id].append(position)
        if step % 100 == 0:
            print(f"Simulation step: {step}")

    # Track vehicle paths
    for vehicle_id in vehicle_paths.keys():
        if vehicle_id in traci.vehicle.getIDList():
            traci.gui.trackVehicle("View #0", vehicle_id)

    traci.close()


if __name__ == "__main__":
    # Define red zone parameters
    red_zone= {
        'lat': 22.349917,
        'lon': 73.173323,
        'radius': 500  # Adjust the radius as needed
    }

    route_files = get_route_files_from_config(conf)
    vehicle_data_dict = gather_data(route_files)
#
    additional_data = {
        'motorcycle': [
            {'id': 'motorcycle1', 'type': 'motorcycle_motorcycle', 'depart': '3599.96', 'departLane': 'best', 'from': '-922051277#0', 'to': '-29874027'}
        ],
        'passenger': [
            {'id': 'veh1', 'type': 'veh_passenger', 'depart': '300.00', 'departLane': 'best', 'from': '-29875742', 'to': '29873850'}
        ],
        'pedestrian': [
            {'id': 'ped1', 'type': 'ped_pedestrian', 'depart': '4.00', 'walk_edges': ['29873850', '29873851']}
        ]
    }

    #for key, value in additional_data.items():
       # vehicle_data_dict.setdefault(key, []).extend(value)

    #update_data(vehicle_data_dict)

    #print(gather_data(route_files))

    # Pass the red zone data to the simulation
    #run_simulation(conf, duration=1000, red_zone_data=red_zone)

    #print(len(geo_TO_edges(where=red_zone)))

sama={ 
    'lat': 22.343487781264088,
    'lon': 73.2003789006782,
    'radius': 10  # safe zone
}
print(len(geo_TO_edges(where=sama)))


