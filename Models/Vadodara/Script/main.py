import os
import sys
import traci
import sumolib
import math
import random
import numpy as np


# Set the SUMO_HOME environment variable if not already done
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

# Define the paths for network and configuration files
script_directory = os.path.dirname(os.path.abspath(__file__))
network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

# Read the network file into SUMO network object
network = sumolib.net.readNet(network_path)

# VehicleManager class to handle vehicle operations like adding vehicles, getting/setting positions and speed
class VehicleManager:
    def __init__(self):
        pass

    # Adds a vehicle to the simulation with the given properties
    def add_vehicle(self, vehicle_id, vehicle_type, depart, from_edge, to_edge, depart_lane="best", speed=0):
        traci.vehicle.add(vehicle_id, routeID="", typeID=vehicle_type, depart=depart, departLane=depart_lane, departSpeed=speed)
        traci.vehicle.changeTarget(vehicle_id, to_edge)
        traci.vehicle.setRoute(vehicle_id, [from_edge, to_edge])

    # Gets the initial position (first edge) of a vehicle
    def get_initial_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[0]

    # Sets the initial position (first edge) of a vehicle
    def set_initial_position(self, vehicle_id, from_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[0] = from_edge
        traci.vehicle.setRoute(vehicle_id, route)

    # Gets the terminal position (last edge) of a vehicle
    def get_terminal_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[-1]

    # Sets the terminal position (last edge) of a vehicle
    def set_terminal_position(self, vehicle_id, to_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[-1] = to_edge
        traci.vehicle.setRoute(vehicle_id, route)

    # Gets the current speed of the vehicle
    def get_speed(self, vehicle_id):
        return traci.vehicle.getSpeed(vehicle_id)

    # Sets the speed of the vehicle
    def set_speed(self, vehicle_id, speed):
        traci.vehicle.setSpeed(vehicle_id, speed)



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

# Function to create a filled red zone (for restricted areas) using geographic coordinates and a radius
def create_filled_red_zone(lat, lon, radius, poly_id="red_zone"):
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
        color=(255, 0, 0, 127),  # RGBA color (red)
        layer=1
    )
    print(f"Filled red zone created with center at ({lat}, {lon}) and radius {radius}.")

# Function to create a filled zone (can be used for safe zones or other designated areas)
def create_filled_zone(lat, lon, radius, poly_id="zone", color=(255, 0, 0, 127)):
    x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

    # Generate points for the circle approximation
    num_points = 72  # Higher values create a smoother circle
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        point_x = x + radius * math.cos(angle)
        point_y = y + radius * math.sin(angle)
        circle_points.append((point_x, point_y))

    # Add the polygon to SUMO
    traci.polygon.add(
        polygonID=poly_id,
        shape=circle_points,
        color=color,  # Color can be customized
        fill=True,
        layer=1
    )
    print(f"Filled zone created with center at ({lat}, {lon}) and radius {radius}.")

# Dictionary to store the path (trail) of each vehicle
vehicle_trails = {}

# Function to update the trail of a single vehicle as a polygon
def update_vehicle_trail(veh_id, path, color):
    polygon_id = f"trail_{veh_id}"

    # Remove existing polygon if exists
    if polygon_id in traci.polygon.getIDList():
        traci.polygon.remove(polygon_id)

    # Add the new trail polygon
    traci.polygon.add(
        polygonID=polygon_id,
        shape=path,
        color=color,
        layer=10,  # High layer to ensure it's visible on top
        fill=False
    )

# Function to update the trails of all vehicles dynamically
def update_vehicle_trails():
    """
    Tracks and visualizes the vehicle trail (route) dynamically as polygons.
    """
    for veh_id in traci.vehicle.getIDList():
        position = traci.vehicle.getPosition(veh_id)  # Get current position (x, y)

        # Store positions in vehicle_trails dictionary
        if veh_id not in vehicle_trails:
            vehicle_trails[veh_id] = [position]
        else:
            vehicle_trails[veh_id].append(position)

        # Limit the trail length for performance optimization (e.g., 100 points max)
        if len(vehicle_trails[veh_id]) > 100:
            vehicle_trails[veh_id] = vehicle_trails[veh_id][-100:]

        # Add polygon for the trail (removes old one to update)
        polygon_id = f"trail_{veh_id}"
        if polygon_id in traci.polygon.getIDList():
            traci.polygon.remove(polygon_id)  # Remove previous polygon

        # Add the new trail polygon
        traci.polygon.add(
            polygonID=polygon_id,
            shape=vehicle_trails[veh_id],
            color=(0, 255, 0, 100),  # Green color with some transparency
            layer=1,
            fill=False
        )

# Main simulation function
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
                max_radius=2000,  # example maximum radius
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
            start_step=50,  # example start step
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
            start_step=100,
            #end_step=800,
            max_radius=500,
            poly_id=f"water_logging_zone_{entry['id']}",  # Use the defined ID
            color=(0, 0, 255, 127)  # Blue
        )
        dynamic_zones.append(water_logging_zone)
  
    
    for step in range(duration):
        traci.simulationStep()

        for dynamic_zone in dynamic_zones:
            dynamic_zone.update_zone(step)

            #update_vehicle_trails()
        if step % 100 == 0:
            print(f"Simulation step: {step}")

    

    traci.close()


def calculate_evacuation_time_in_seconds(first_departure_step, last_arrival_step, step_length):
    if first_departure_step > last_arrival_step:
        raise ValueError("Departure step cannot be greater than arrival step.")

    steps = last_arrival_step - first_departure_step
    evacuation_time_seconds = steps * step_length

    return evacuation_time_seconds



if __name__ == "__main__":
    # Define the red zone parameters (restricted areas)
    red_zones = [
        { # siddharth bungalows , sama
            'lat': 22.33779597622535,
            'lon': 73.20539458409085,
            'radius': 1000  # Adjust the radius as needed
        },
        { # random near
            'lat':22.321066599415307,
            'lon': 73.19607730306171,
            'radius': 1000
        }
    ]

    # Define safe zone parameters (areas where vehicles are allowed to go freely)
    green_zone = { # laxmipura
        'lat': 22.328303179158446,
        'lon': 73.1471742709198,
        'radius': 300  # Adjust radius as needed
    }

    
    water_logging_data = [
    {
        'id': 1,  # Add unique ID
        'lat': 22.33779597622535,
        'lon': 73.19607730306171,
        'radius': 50
}
    ]

  

    # Run the simulation with the defined red and safe zones
    run_simulation(conf, duration=1000, red_zone_data=red_zones, safe_zone_data=green_zone, water_logging_data= water_logging_data)
    evacuation_time_seconds = calculate_evacuation_time_in_seconds(
        0,
        728,
        0.02
    )

    print(f"Evacuation Time: {evacuation_time_seconds} seconds")