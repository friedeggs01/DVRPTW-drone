import numpy as np

from graph.requests import Request
from utils.utils import cal_distance, decode_route

class Decision: # quyết định xem request có được chấp nhận hay không
    def __init__(self, r: Request, T, network):
        self.r = r
        self.T = T # time slot that is happening
        min_distance = cal_distance(None, r)
        for vehicle_id in range(network.num_vehicle):
            planning_route, _, _ = decode_route(network.routes[vehicle_id])
            for pos in range(len(planning_route)):
                min_distance = min(min_distance, cal_distance(network.requests[planning_route[pos]], r))
        self.min_distance = min_distance

        max_cap = 0
        for vehicle_id in range(network.num_vehicle):
            planning_route, _, _ = decode_route(network.routes[vehicle_id])
            remaining_capacity = network.trucks[vehicle_id].capacity
            for pos in range(len(planning_route)):
                remaining_capacity -= network.requests[planning_route[pos]].customer_demand
            max_cap = max(max_cap, remaining_capacity)
        self.max_cap = max_cap
    

class Ordering:
    def __init__(self, r, T, network):
        self.r = r
        self.T = T
        min_distance = cal_distance(None, r)
        for vehicle_id in range(network.num_vehicle):
            planning_route, _, _ = decode_route(network.routes[vehicle_id])
            for pos in range(len(planning_route)):
                min_distance = min(min_distance, cal_distance(network.requests[planning_route[pos]], r))
        self.min_distance = min_distance

class Choosing: # chọn xem request được chấp nhận sẽ gán cho xe nào
    def __init__(self, r, vehicle_id, T, network):
        self.T = T
        self.network = network
        self.remaining_capacity = network.trucks[vehicle_id].capacity
        planning_route, truck_route, drone_route = decode_route(network.routes[vehicle_id])
        for pos in range(len(truck_route)):
            self.remaining_capacity -= network.requests[truck_route[pos]].customer_demand
        
        self.dis_sum = 0
        for pos in range(len(planning_route)-1):
            self.dis_sum += cal_distance(network.requests[planning_route[pos]], network.requests[planning_route[pos+1]])
        if len(planning_route) > 0:
            self.dis_sum += cal_distance(None, network.requests[planning_route[0]])
            self.dis_sum += cal_distance(network.requests[planning_route[-1]], None)
        self.numberCustomer = len(planning_route)
        self.min_distance = cal_distance(None, r)
        for pos in range(len(planning_route)):
            self.min_distance = min(self.min_distance, cal_distance(network.requests[planning_route[pos]], r))




