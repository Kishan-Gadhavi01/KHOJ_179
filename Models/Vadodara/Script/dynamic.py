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

def get_jammed_active_edges(speed_threshold=5):
    
    vehicle_ids = traci.vehicle.getIDList()
    jammed_edges = set()  

    for vehicle_id in vehicle_ids:
        edge_id = traci.vehicle.getRoadID(vehicle_id)
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)  
        if vehicle_speed < speed_threshold:  
            jammed_edges.add(edge_id)

    return list(jammed_edges) 

def TrafficHandler(speed_threshold=5):
    vehicle_ids = traci.vehicle.getIDList()
    
    for vehicle_id in vehicle_ids:
        # Get the current speed of the vehicle
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)

        # Get the current road/edge the vehicle is on
        current_edge = traci.vehicle.getRoadID(vehicle_id)

        # Get the vehicle's current route (if any)
        current_route = traci.vehicle.getRoute(vehicle_id)

        # Check if the vehicle's speed is below the threshold and it's not on its starting edge
        if vehicle_speed <= speed_threshold:
            print(f"Threshold Alert: Vehicle {vehicle_id} is moving slowly: {vehicle_speed} m/s")
            
            if current_route:
                # Check if the vehicle is still on the first edge of its route (starting point)
                start_edge = current_route[0]  # Get the first edge of the route (start point)
                
                if current_edge != start_edge:
                    # If the vehicle is not on its starting edge, attempt to find an alternate route
                    destination_edge = current_route[-1]  # Get the last edge of the current route (destination)
                    
                    # Find an alternative route to the destination from the current edge
                    alternative_route = traci.simulation.findRoute(current_edge, destination_edge)
                    
                    if alternative_route.edges:
                        # Set the new route for the vehicle
                        traci.vehicle.setRoute(vehicle_id, alternative_route.edges)
                        print(f"Rerouted vehicle {vehicle_id} from {current_edge} to {destination_edge}: {alternative_route.edges}")
                    else:
                        print(f"No valid alternate route found for vehicle {vehicle_id} from {current_edge} to {destination_edge}")
                else:
                    print(f"Vehicle {vehicle_id} is still at the start edge {start_edge}. Not rerouting.")
         

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
    sumoCmd = ["sumo-gui", "-c", config_file]
    #traci.simulation.findRoute()
    try:
        traci.start(sumoCmd)
        for step in range(duration):
            traci.simulationStep()
            # if step == 10:
            #     traci.edge.setDisallowed("361899464#0", ["motorcycle","passenger"])

            # Print vehicle counts every 100 steps
            if  step % 10 == 0:
                TrafficHandler(speed_threshold=1)
                            
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


