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

def get_route_files_from_config(config_path, script_directory):
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

def generate_entries(df, noOfEntries, name, delay=10, from_list=None, to_list=None):
    """
    Generate new sequential entries for the DataFrame ensuring depart times continue from the last entry.
    """
    # Extract prefix and last ID count from the existing DataFrame
    if not df.empty:
        last_id = df['id'].iloc[-1]
        prefix = ''.join([i for i in last_id if not i.isdigit()])
        last_count = int(''.join(filter(str.isdigit, last_id)))
        # Start the delay from the last depart value
        last_depart = float(df['depart'].iloc[-1])
    else:
        # Defaults if the DataFrame is empty
        prefix, last_count, last_depart = "entry", 0, 0.0

    # Determine type based on the passed name
    type_mapping = {
        'motorcycle': 'motorcycle_motorcycle',
        'passenger': 'veh_passenger',
        'pedestrian': 'ped_pedestrian'
    }
    df_type = type_mapping.get(name, 'unknown_type')

    # Fixed fields
    departLane = 'best'

    # Generate entries
    for i in range(1, noOfEntries + 1):
        # Increment the ID
        new_id = f"{prefix}{last_count + i}"
        # Continue depart time sequentially
        new_depart = last_depart + (delay * i)
        from_value = random.choice(from_list) if len(from_list) > 1 else from_list[0]
        to_value = random.choice(to_list) if len(to_list) > 1 else to_list[0]

        # Create the new entry
        new_entry = {
            'id': new_id,
            'type': df_type,
            'depart': f"{new_depart:.2f}",  # Ensure two decimal places
            'departLane': departLane,
            'from': from_value,
            'to': to_value
        }

        # Add additional fields for pedestrians (walk_edges)
        if 'walk_edges' in df.columns:
            new_entry['walk_edges'] = [from_value, to_value]

        yield new_entry

############ //





############ File handling

def update_data(vehicle_data_dict, conf):
    paths = get_route_files_from_config(conf, os.path.dirname(os.path.abspath(__file__)))
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
        'to': '29873850'
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



class DynamicFilledZone:
    def __init__(self, lat, lon, initial_radius, poly_id="zone", color=(255, 0, 0, 127), size_change=False, size_change_rate=0, start_step=0, end_step=None, max_radius=None):
        """
        Initializes the DynamicFilledZone.

        :param lat: Latitude of the center of the zone.
        :param lon: Longitude of the center of the zone.
        :param initial_radius: Initial radius of the zone.
        :param poly_id: ID of the polygon.
        :param color: Color of the polygon.
        :param size_change: Boolean indicating if the size should change over time.
        :param size_change_rate: Rate at which the size changes per step.
        :param start_step: Simulation step at which the zone appears.
        :param end_step: Simulation step at which the zone disappears (optional).
        :param max_radius: Maximum radius the zone can reach (optional).
        """
        self.lat = lat
        self.lon = lon
        self.initial_radius = initial_radius
        self.poly_id = poly_id
        self.color = color
        self.size_change = size_change
        self.size_change_rate = size_change_rate
        self.start_step = start_step
        self.end_step = end_step
        self.max_radius = max_radius
        self.x, self.y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

    def update_zone(self, step):
        if step < self.start_step:
            return
        if self.end_step is not None and step > self.end_step:
            if self.poly_id in traci.polygon.getIDList():
                traci.polygon.remove(self.poly_id)
            return

        current_radius = self.initial_radius
        if self.size_change:
            current_radius += self.size_change_rate * (step - self.start_step)
            if self.max_radius is not None:
                current_radius = min(current_radius, self.max_radius)

        num_points = 72
        circle_points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            point_x = self.x + current_radius * math.cos(angle)
            point_y = self.y + current_radius * math.sin(angle)
            circle_points.append((point_x, point_y))

        if self.poly_id in traci.polygon.getIDList():
            traci.polygon.remove(self.poly_id)

        traci.polygon.add(
            polygonID=self.poly_id,
            shape=circle_points,
            color=self.color,
            fill=True,
            layer=1
        )

class WaterLoggingZone:
    def __init__(self, lat, lon, initial_radius, poly_id="water_zone", color=(0, 0, 255, 127), size_change=False, size_change_rate=0, start_step=0, end_step=None, max_radius=None):
        """
        Initializes the WaterLoggingZone.
        """
        self.lat = lat
        self.lon = lon
        self.initial_radius = initial_radius
        self.poly_id = poly_id
        self.color = color
        self.size_change = size_change
        self.size_change_rate = size_change_rate
        self.start_step = start_step
        self.end_step = end_step
        self.max_radius = max_radius
        self.x, self.y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        self.perlin_offsets = [random.uniform(0, 100) for _ in range(360)]  # Perlin noise offsets for each angle

    def _perlin_noise(self, angle_index):
        """Generate smooth radius variation using Perlin noise."""
        return (np.sin(self.perlin_offsets[angle_index] + angle_index * 0.1) + 1) / 2  # Normalize to [0, 1]

    def update_zone(self, step):
        """Updates the zone and its size."""
        if step < self.start_step:
            return
        if self.end_step is not None and step > self.end_step:
            if self.poly_id in traci.polygon.getIDList():
                traci.polygon.remove(self.poly_id)
            return

        # Calculate current radius
        current_radius = self.initial_radius
        if self.size_change:
            current_radius += self.size_change_rate * (step - self.start_step)
            if self.max_radius is not None:
                current_radius = min(current_radius, self.max_radius)

        num_points = 52  # More points for a smoother circle
        polygon_points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            radius_variation = current_radius * (0.9 + 0.2 * self._perlin_noise(i))  # Controlled radius variation
            point_x = self.x + radius_variation * math.cos(angle)
            point_y = self.y + radius_variation * math.sin(angle)
            polygon_points.append((point_x, point_y))

        # Update or create the polygon
        if self.poly_id in traci.polygon.getIDList():
            traci.polygon.remove(self.poly_id)

        traci.polygon.add(
            polygonID=self.poly_id,
            shape=polygon_points,
            color=self.color,
            fill=True,
            layer=10
        )


# dictionary to store traveled paths for each vehicle
vehicle_trails = {}

def update_vehicle_trail(veh_id, path, color):
    """
    Updates a vehicle's trail polygon in the simulation.
    """
    # Generate the polygon points for the entire path
    polygon_id = f"trail_{veh_id}"

    # Check and remove existing polygon for the vehicle
    if polygon_id in traci.polygon.getIDList():
        traci.polygon.remove(polygon_id)

    # Add a new polygon with the updated path
    traci.polygon.add(
        polygonID=polygon_id,
        shape=path,  # Pass the path with all recorded positions
        color=color,
        layer=10,  # High layer to ensure it's visible on top
        fill=False  # Optional: Set to True if you want filled areas
    )

def update_vehicle_trails():
    for veh_id in traci.vehicle.getIDList():
        position = traci.vehicle.getPosition(veh_id)  # (x, y)

        if veh_id not in vehicle_trails:
            vehicle_trails[veh_id] = [position]
        else:
            vehicle_trails[veh_id].append(position)

        trail_points = vehicle_trails[veh_id]

        if len(trail_points) > 70:  # Limit to 50 points for performance
            trail_points = trail_points[-70:]
            vehicle_trails[veh_id] = trail_points

        polygon_id = f"trail_{veh_id}"
        if polygon_id in traci.polygon.getIDList():
            traci.polygon.remove(polygon_id)

        traci.polygon.add(
            polygonID=polygon_id,
            shape=trail_points,
            color=(0, 255, 0, 100),  # Green
            layer=10,
            fill=False
        )

# Algorithm to reach the destination in the shortest time possible using Dijkstra's algorithm rather than the shortest path algorithm in SUMO by default.

def compute_safe_zone_center(safe_zone_data):
    return (safe_zone_data['lat'], safe_zone_data['lon'])

def get_network_state():
    # get real-time vehicle count per edge and other traffic conditions
    network_state = {}
    for edge_id in traci.edge.getIDList():
        # real-time vehicle count for each edge
        vehicle_count = traci.edge.getLastStepVehicleNumber(edge_id)
        congestion_factor = compute_congestion_factor(vehicle_count, edge_id)
        network_state[edge_id] = congestion_factor  # store the traffic congestion factor for each edge
    return network_state

def compute_congestion_factor(vehicle_count, edge_id):
    """
    calculates the congestion factor for a given edge.
    higher vehicle counts (traffic) result in higher congestion factor.
    """
    max_capacity = traci.edge.getLaneNumber(edge_id) * 20  # approximate number of vehicles that can fit in the lanes
    congestion_factor = (vehicle_count / max_capacity) ** 2  # squared term penalizes more congested roads
    return max(congestion_factor, 1)  # minimum congestion factor is 1 (free-flow traffic)

def reroute_vehicle(vehicle_id, destination, network_state):
    current_edge = traci.vehicle.getRoadID(vehicle_id)

    all_routes = traci.simulation.getRoutes(current_edge, destination)

    optimal_route = None
    min_travel_time = float('inf')

    for route in all_routes:
        total_cost = 0
        total_distance = 0
        blocked = False

        for edge in route:
            congestion_factor = network_state.get(edge, 5)  # default to 1 (free-flow)
            edge_length = traci.edge.getLength(edge)  # get length of the edge
            total_distance += edge_length

            # penalize routes with higher congestion factor
            total_cost += congestion_factor * edge_length

            # check for potential blockages or incidents
            if is_edge_blocked(edge):
                blocked = True
                break

        if blocked:
            continue

        # include distance factor in the total cost for a more balanced path finding
        adjusted_travel_time = total_cost + total_distance * random.random()

        if adjusted_travel_time < min_travel_time:
            min_travel_time = adjusted_travel_time
            optimal_route = route

    if optimal_route:
        traci.vehicle.setRoute(vehicle_id, optimal_route)  # set the best route considering traffic

def is_edge_blocked(edge_id):
    """
    determines whether an edge is blocked due to an incident, traffic accident, or a roadblock.
    """
    # hypothetically check an incident-based condition here
    return random.choice([True, False])

def run_simulation(config_file, duration=1000, red_zone_data=None, safe_zone_data=None, water_logging_data=None, vehicle_data_dict=None):
    sumoCmd = ["sumo-gui", "-c", config_file]
    traci.start(sumoCmd)

    dynamic_zones = []
    if red_zone_data:
        for i, red_zone in enumerate(red_zone_data):
            print(f"Creating red zone {i+1} with parameters: {red_zone}")
            dynamic_zone = DynamicFilledZone(
                lat=red_zone['lat'],
                lon=red_zone['lon'],
                initial_radius=red_zone['radius'],
                size_change=True,  # enable size change if needed
                size_change_rate=1,  # change rate per step
                start_step=50,  # example start step
                # end_step=800,  # example end step
                max_radius=650,  # example maximum radius
                poly_id=f"red_zone_{i+1}",
                color=(255, 0, 0, 127)  # Red
            )
            dynamic_zones.append(dynamic_zone)

    if safe_zone_data:
        print(f"Creating safe zone with parameters: {safe_zone_data}")
        dynamic_zone = DynamicFilledZone(
            lat=safe_zone_data['lat'],
            lon=safe_zone_data['lon'],
            initial_radius=safe_zone_data['radius'],
            size_change=False,  # enable size change if needed
            size_change_rate=1,  # change rate per step
            start_step=100,  # example start step
            # end_step=200,
            poly_id="safe_zone",
            color=(0, 255, 0, 127)  # Green
        )
        dynamic_zones.append(dynamic_zone)

    for entry in water_logging_data:
        water_logging_zone = WaterLoggingZone(
            lat=entry['lat'],
            lon=entry['lon'],
            initial_radius=entry['radius'],
            size_change=True,
            size_change_rate=1,
            start_step=200,
            end_step=800,
            max_radius=500,
            poly_id=f"water_logging_zone_{entry['id']}",  # Use the defined ID
            color=(0, 0, 255, 127)  # Blue
        )
        dynamic_zones.append(water_logging_zone)

    vehicle_paths = {}
    vehicle_colors = {}

    passenger_ids = [v['id'] for v in vehicle_data_dict.get('passenger', [])]
    network_state = get_network_state()

    for step in range(duration):
        traci.simulationStep()

        for dynamic_zone in dynamic_zones:
            dynamic_zone.update_zone(step)

        vehicle_ids = traci.vehicle.getIDList()
        for vehicle_id in vehicle_ids:
            position = traci.vehicle.getPosition(vehicle_id)
            x, y = traci.simulation.convertGeo(position[0], position[1], fromGeo=False)
            nearest_edge = network.getNeighboringEdges(x, y, r=10)
            if nearest_edge:
                destination_edge = nearest_edge[0][0].getID()  # edge ID
                reroute_vehicle(vehicle_id, destination_edge, network_state)

            if vehicle_id not in vehicle_paths:
                vehicle_paths[vehicle_id] = []
                vehicle_colors[vehicle_id] = (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255), 255)
            vehicle_paths[vehicle_id].append(position)

            if len(vehicle_paths[vehicle_id]) > 100:
                vehicle_paths[vehicle_id].pop(0)
            # update_vehicle_trail(vehicle_id, vehicle_paths[vehicle_id], vehicle_colors[vehicle_id])
            update_vehicle_trails()
        if step % 100 == 0:
            print(f"Simulation step: {step}")

    for vehicle_id in vehicle_paths.keys():
        if vehicle_id in traci.vehicle.getIDList():
            traci.gui.trackVehicle("View #0", vehicle_id)

    traci.close()


def calculate_evacuation_time_in_seconds(first_departure_step, last_arrival_step, step_length):
    if first_departure_step > last_arrival_step:
        raise ValueError("Departure step cannot be greater than arrival step.")

    steps = last_arrival_step - first_departure_step
    evacuation_time_seconds = steps * step_length

    return evacuation_time_seconds






if __name__ == "__main__":
    # Define red zone parameters
    red_zones = [
        {
            'lat': 22.349917,
            'lon': 73.173323,
            'radius': 500  # Adjust the radius as needed
        },
        {
            'lat':22.335588,
            'lon': 73.177759,
            'radius': 300  # Adjust the radius as needed
        }
    ]

    route_files = get_route_files_from_config(conf, script_directory)
    vehicle_data_dict = gather_data(route_files)


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

    df = make_df(vehicle_data_dict)
    print(df["motorcycle"])
    print(df["passenger"])


    green_zone = {
        'lat': 22.343487781264088,
        'lon': 73.2003789006782,
        'radius': 100  # safe zone
    }

    water_logging_data = [
    {
        'id': 1,  # Add unique ID
        'lat': 22.343487781264088,
        'lon': 73.2003789006782,
        'radius': 50
    },
    {
        'id': 2,  # Add unique ID
        'lat': 22.350479,
        'lon': 73.172299,
        'radius': 50
    },
    {
        'id': 3,  # Add unique ID
        'lat': 22.334077,
        'lon': 73.179913,
        'radius': 50
    }
    ]

    Redges = [geo_TO_edges(where=zone) for zone in red_zones]
    gedges = geo_TO_edges(where=green_zone)


    print(geo_TO_edges(where=green_zone, config_file=conf))

    df = make_df(vehicle_data_dict)
    print(df["motorcycle"])
    print(df["passenger"])

    update_column(df, "to", filter_list=None, listt=["1293567960"])
    print(df["motorcycle"])
    print(df["passenger"])
    dfd = {key: dff.to_dict(orient="records") for key, dff in df.items()}
    print(dfd["passenger"])
    update_data(dfd, conf)
    run_simulation(conf, duration=1000, red_zone_data=red_zones, safe_zone_data=green_zone, water_logging_data= water_logging_data, vehicle_data_dict=vehicle_data_dict)
    evacuation_time_seconds = calculate_evacuation_time_in_seconds(
        0,
        728,
        0.02
    )

    print(f"Evacuation Time: {evacuation_time_seconds} seconds")