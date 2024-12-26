import os
import sys
import traci
import time
from collections import defaultdict
start_time = time.time()

# Set the SUMO_HOME environment variable if not already done
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

# Define the paths for network and configuration files
script_directory = os.path.dirname(os.path.abspath(__file__))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

def get_active_edges(threshold=0):
    """
    Retrieve the vehicle IDs present on each edge, filtered by a minimum threshold.
    """
    vehicle_ids = traci.vehicle.getIDList()
    edge_vehicle_map = defaultdict(list)

    for vehicle_id in vehicle_ids:
        edge_id = traci.vehicle.getRoadID(vehicle_id)
        edge_vehicle_map[edge_id].append(vehicle_id)

    return {edge: vehicles for edge, vehicles in edge_vehicle_map.items() if len(vehicles) > threshold}

# Function to run the simulation with error handling
def run_simulation(config_file, duration=1000):
    """
    Run the SUMO simulation for a fixed number of steps.
    The simulation will always be closed in a 'finally' block.
    """
    sumoCmd = ["sumo", "-c", config_file]
    traci.simulation.findRoute()
    try:
        traci.start(sumoCmd)
        for step in range(duration):
            traci.simulationStep()

            # Print vehicle counts every 100 steps
            if (step + 1) % 100 == 0:
                print(f"Simulation step: {step + 1}")
                edge_vehicle_count = get_active_edges()

                # Print edge names and vehicle counts for each active edge
                for edge_id, vehicles in edge_vehicle_count.items():
                    edge_name = edge_id  # Get the edge name
                    print(f"  Edge {edge_name} has {len(vehicles)} vehicles")
    except traci.exceptions.TraCIException as e:
        print(f"Error occurred during the simulation: {e}")
    
    finally:
        traci.close()
        print("SUMO simulation closed.")

# Main script execution
if __name__ == "__main__":
    # Run the simulation with the defined configuration file and fixed number of steps
    run_simulation(conf,2500)

    # Calculate and display the total runtime
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Total runtime: {total_runtime:.2f} seconds.")


