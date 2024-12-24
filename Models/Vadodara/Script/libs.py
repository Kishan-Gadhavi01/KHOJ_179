import libsumo
import traci  # Import TraCI for GUI and real-time control
import os

# Define the script directory and the paths to the network and configuration files
script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

# Function to get vehicle counts on each edge using libsumo
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

# Function to run the simulation for a fixed number of steps using libsumo and TraCI for GUI control
def run_simulation(num_steps=2500):
    # Start SUMO with GUI mode (using TraCI)
    traci.start(["sumo-gui", "-c", conf])  # This launches SUMO with the GUI
    
    # Load the simulation with libsumo
    libsumo.simulation.load(["-c", conf])

    try:
        # Loop over a predefined number of simulation steps
        for step in range(num_steps):
            # Perform one simulation step using libsumo
            libsumo.simulation.step()

            # Perform one simulation step using TraCI to update the GUI
            traci.simulationStep()  # This keeps the GUI updated with each step

            # Print vehicle counts every 100 steps
            o=True
            if (step + 1) % 100 == 0:
              
                edge_vehicle_count = get_vehicle_counts_by_edge()
                
                # Print vehicle counts for each edge at the specified step
                print(f"Step {step + 1}/{num_steps}:")
                for edge_id, count in edge_vehicle_count.items():
                    print(f"  Edge {edge_id} has {count} vehicles")

    finally:
        # Close the simulation once all steps are completed
        libsumo.simulation.close()
        traci.close()

if __name__ == "__main__":
    # Run the simulation for a specified number of steps (e.g., 2500)
    run_simulation()
