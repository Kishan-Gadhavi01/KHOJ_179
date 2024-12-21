from tripmanager import *

# Red zones: These are high-risk zones where we want to track vehicle movement
red_zones = [
    { # Siddharth Bungalows, Sama
        'lat': 22.33779597622535,
        'lon': 73.20539458409085,
        'radius': 1000  # Adjust the radius as needed (in meters)
    },
    { # Random location near other zone
        'lat': 22.321066599415307,
        'lon': 73.19607730306171,
        'radius': 1000  # Adjust the radius as needed (in meters)
    }
]

# Define safe zone parameters: This is the low-risk zone (Green Zone) where we expect safe movement
green_zone = { # Laxmipura
    'lat': 22.328303179158446,
    'lon': 73.1471742709198,
    'radius': 300  # Adjust the radius as needed (in meters)
}

# Assuming red_zones and green_zone are already defined
Redges = [geo_to_edges(where=zone) for zone in red_zones]
# Flatten the list (since geo_to_edges returns a dictionary)
RMedges = [*Redges[0]['motorcycle'], *Redges[1]['motorcycle']]
RPedges = [*Redges[0]['passenger'], *Redges[1]['passenger']]
print(f"Red zone edges for motorcycles: {len(RMedges)}")
print(f"Red zone edges for passengers: {len(RPedges)}")

green_zone_edges = geo_to_edges(where=green_zone)
GMedges = green_zone_edges['motorcycle']
GPedges = green_zone_edges['passenger']
print(f"Green zone edges for motorcycles: {len(GMedges)}")
print(f"Green zone edges for passengers: {len(GPedges)}")

# Get route files from the SUMO configuration file (conf is assumed to be predefined)
route_files = get_route_files_from_config(conf)
print(f"Route files: {route_files}")  # Print the route files being processed for logging

# Gather vehicle data from the route files
vehicle_data_dict = gather_data(route_files)
print("Vehicle data gathered.")  # Log successful data gathering

# Convert gathered data into DataFrames for easier processing
df = make_df(vehicle_data_dict)
print("DataFrames created for each vehicle type.")  # Log successful DataFrame creation

# # Assuming 'network' is already defined, get all available edges in the network
# all_edges = network.getEdges()
# print(f"All edges in the network: {all_edges}")  # Log all edges in the network for debugging

# Extract the edge IDs from the network's edges
# edge_ids = [edge.getID() for edge in all_edges]
# print(f"Edge IDs extracted: {edge_ids}")  # Log the edge IDs extracted for transparency

# Generate new entries for 'motorcycle' vehicles (adding 10 new motorcycles)
new_motorcycle = list(generate_entries(
    df['motorcycle'],       # Existing motorcycle data
    noOfEntries=200,         # Number of new entries to generate
    name='motorcycle',      # Type of vehicle being added
    delay=2.5,               # Delay between vehicle departures in seconds
    from_list=RMedges,     # Possible 'from' edges (start locations)
    to_list=GMedges        # Possible 'to' edges (destination locations)
))
print(f"Generated new motorcycle entries: {len(new_motorcycle)}")  # Log the number of new entries

# Generate new entries for 'passenger' vehicles (adding 10 new passengers)
new_passenger = list(generate_entries(
    df['passenger'],        # Existing passenger data
    noOfEntries=200,         # Number of new entries to generate
    name='passenger',       # Type of vehicle being added
    delay=2.5,               # Delay between vehicle departures in seconds
    from_list=RPedges,     # Possible 'from' edges (start locations)
    to_list=GPedges        # Possible 'to' edges (destination locations)
))
print(f"Generated new passenger entries: {len(new_passenger)}")  # Log the number of new entries

# Append the new motorcycle entries to the existing 'motorcycle' DataFrame
df['motorcycle'] = pd.concat(
    [df['motorcycle'], pd.DataFrame(new_motorcycle)],  # Combine old and new motorcycle entries
    ignore_index=True  # Reset index after concatenation
)
print("Motorcycle entries updated.")  # Log the update of the motorcycle DataFrame

# Append the new passenger entries to the existing 'passenger' DataFrame
df['passenger'] = pd.concat(
    [df['passenger'], pd.DataFrame(new_passenger)],  # Combine old and new passenger entries
    ignore_index=True  # Reset index after concatenation
)
print("Passenger entries updated.")  # Log the update of the passenger DataFrame

# Convert the updated DataFrames back into dictionaries of records (list of dictionaries for each vehicle type)
dfd = {key: dff.to_dict(orient="records") for key, dff in df.items()}
print("DataFrames converted to dictionary format.")  # Log the successful conversion

# Update the route data with the new entries
update_data(dfd)
print("Route data updated successfully.")  # Log the successful update of the route data
