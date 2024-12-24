# Import the libsumo module
import libsumo
import os 
script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))


def get_vehicle_counts_by_edge():
    # Get the list of all vehicles in the simulation
    vehicle_ids = libsumo.vehicle.getIDList()
    
    # Create a dictionary to store vehicle counts per edge
    edge_vehicle_count = {}
    
    for vehicle_id in vehicle_ids:
        # Get the edge where the vehicle is currently located
        edge_id = libsumo.vehicle.getRoadID(vehicle_id)
        
        # Increment the count for that edge
        if edge_id not in edge_vehicle_count:
            edge_vehicle_count[edge_id] = 0
        edge_vehicle_count[edge_id] += 1
    
    return edge_vehicle_count

def run_simulation():
    libsumo.simulation.load(["-c", conf])

    try:
        # Simulation loop
        while libsumo.simulation.getMinExpectedNumber() > 0:
            # Perform one simulation step
            libsumo.simulation.step()

            # Get the count of vehicles on each edge
            edge_vehicle_count = get_vehicle_counts_by_edge()
            
            # Print vehicle counts for each edge
            for edge_id, count in edge_vehicle_count.items():
                print(f"Edge {edge_id} has {count} vehicles")

    finally:
        libsumo.simulation.close()

if __name__ == "__main__":
    run_simulation()
