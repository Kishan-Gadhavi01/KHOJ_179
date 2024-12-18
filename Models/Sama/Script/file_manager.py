import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from utils import get_route_files_from_config

PROCESS_MOTORCYCLE = True
PROCESS_PASSENGER = True
PROCESS_PEDESTRIAN = False

def update_data(vehicle_data_dict, conf):
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
        'from': '-29875742',
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