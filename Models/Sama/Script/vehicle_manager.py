import traci

class VehicleManager:
    def __init__(self):
        pass

    def add_vehicle(self, vehicle_id, vehicle_type, depart, from_edge, to_edge, depart_lane="best", speed=0):
        traci.vehicle.add(vehicle_id, routeID="", typeID=vehicle_type, depart=depart, departLane=depart_lane, departSpeed=speed)
        traci.vehicle.changeTarget(vehicle_id, to_edge)
        traci.vehicle.setRoute(vehicle_id, [from_edge, to_edge])

    def get_initial_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[0]

    def set_initial_position(self, vehicle_id, from_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[0] = from_edge
        traci.vehicle.setRoute(vehicle_id, route)

    def get_terminal_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[-1]

    def set_terminal_position(self, vehicle_id, to_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[-1] = to_edge
        traci.vehicle.setRoute(vehicle_id, route)

    def get_speed(self, vehicle_id):
        return traci.vehicle.getSpeed(vehicle_id)

    def set_speed(self, vehicle_id, speed):
        traci.vehicle.setSpeed(vehicle_id, speed)