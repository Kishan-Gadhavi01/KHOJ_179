import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci
import sumolib

script_directory = os.path.dirname(os.path.abspath(__file__))

network_path = os.path.abspath(os.path.join(script_directory, "../osm.net.xml.gz"))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))

network = sumolib.net.readNet(network_path)

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


def geo_TO_edges(lat, lon, config_file):
    sumoCmd = ["sumo", "-c", config_file]
    try:
        traci.start(sumoCmd)
        
        x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        print(f"X is {x}, Y is {y}")
        nearest_edge = network.getNeighboringEdges(x, y, r=10, includeJunctions=True, allowFallback=True)
        
        return nearest_edge
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
    finally:
        traci.close()

if __name__ == "__main__":
    latitude = 22.349917 #cordinate avalable in map
    longitude = 73.173323 #cordinate avalable in map
    geo_to_cartesian(latitude,longitude,conf)
    print()
    edges=geo_TO_edges(latitude,longitude,conf)
    print(edges) # Not sorted acording to docstring
 
