import traci
import math
import random

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

def geo_TO_edges(where, network, config_file):
    if where:
        lat = where['lat']
        lon = where['lon']
        r = where['radius']

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

def create_filled_red_zone(lat, lon, radius, poly_id="red_zone"):
    x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
    num_points = 72
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        point_x = x + radius * math.cos(angle)
        point_y = y + radius * math.sin(angle)
        circle_points.append((point_x, point_y))

    traci.polygon.add(
        polygonID=poly_id,
        shape=circle_points,
        color=(255, 0, 0, 127),
        fill=True,
        layer=1
    )
    print(f"Filled red zone created with center at ({lat}, {lon}) and radius {radius}.")

def run_simulation(config_file, duration=1000, red_zone_data=None):
    sumoCmd = ["sumo-gui", "-c", config_file]
    traci.start(sumoCmd)

    if red_zone_data:
        print(f"Creating red zone with parameters: {red_zone_data}")
        create_filled_red_zone(
            lat=red_zone_data['lat'],
            lon=red_zone_data['lon'],
            radius=red_zone_data['radius']
        )

    vehicle_paths = {}
    vehicle_colors = {}

    for step in range(duration):
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        for vehicle_id in vehicle_ids:
            position = traci.vehicle.getPosition(vehicle_id)
            if vehicle_id not in vehicle_paths:
                vehicle_paths[vehicle_id] = []
                vehicle_colors[vehicle_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            vehicle_paths[vehicle_id].append(position)
            if len(vehicle_paths[vehicle_id]) > 100:
                vehicle_paths[vehicle_id].pop(0)
            traci.polygon.add(
                polygonID=f"trail_{vehicle_id}_{step}",
                shape=vehicle_paths[vehicle_id],
                color=vehicle_colors[vehicle_id],
                fill=False,
                layer=2
            )
        if step % 100 == 0:
            print(f"Simulation step: {step}")

    for vehicle_id in vehicle_paths.keys():
        if vehicle_id in traci.vehicle.getIDList():
            traci.gui.trackVehicle("View #0", vehicle_id)

    traci.close()