import os
import sys
import traci
import sumolib
import random
from data_manager import gather_data, make_df, update_column
from file_manager import update_data, initialize_file_structure
from vehicle_manager import VehicleManager
from simulation_manager import run_simulation, geo_TO_edges
from utils import get_route_files_from_config

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

network = sumolib.net.readNet(network_path)

if __name__ == "__main__":
    # Define red zone parameters
    red_zone = {
        'lat': 22.349917,
        'lon': 73.173323,
        'radius': 500  # Adjust the radius as needed
    }

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

    #for key, value in additional_data.items():
       # vehicle_data_dict.setdefault(key, []).extend(value)

    #update_data(vehicle_data_dict, conf)

    #print(gather_data(route_files))

    # Pass the red zone data to the simulation

    #print(len(geo_TO_edges(where=red_zone, config_file=conf)))

    sama = {
        'lat': 22.343487781264088,
        'lon': 73.2003789006782,
        'radius': 10  # safe zone
    }

    print(geo_TO_edges(where=sama, config_file=conf))

    df = make_df(vehicle_data_dict)
    print(df["motorcycle"])
    print(df["passenger"])

    update_column(df, "to", filter_list=None, listt=["1293567960"])
    print(df["motorcycle"])
    print(df["passenger"])
    dfd = {key: dff.to_dict(orient="records") for key, dff in df.items()}
    print(dfd["passenger"])
    update_data(dfd, conf)
    run_simulation(conf, duration=1000, red_zone_data=red_zone)