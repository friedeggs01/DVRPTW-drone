from gp.node.function import *
from gp.node.terminal import *
from copy import deepcopy
from gp.population.individual import *
from data.read_data import *
from utils.utils import *
from .deploy_request import *
from graph.network import Network
import math

def calFitness_three_policies(indi: Individual, network: Network, request_list, duration, end_system_time):
    # storing processing history
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    sum_request = len(request_list_copy)
    T = 0
    num_reject = 0 # number of reject request
    carbon_sum = 0 # sum of cost of all request that excuted
    request_queue = []
    while T <= end_system_time:
        new_request = get_request_list(request_list_copy, T, duration)
        request_queue.extend(new_request)

        processing_request_list = []
        for request in request_queue:
            if T + request.service_time > request.tw_end:
                num_reject += 1
                continue
            processing_request_list.append(request)
        
        # Calculate value of GP for each request
        accepted_request = []
        for request in processing_request_list:
            # decide the request is accepted or rejected
            value_of_decision_gp = decision_gp(T)
            if value_of_decision_gp < 0:
                reject = reject + 1
                continue
            accepted_request.append(request)
        
        # Order of accepted requests
        ordered_requests = []
        for request in accepted_request:
            value_ordering_gp = ordering_gp(indi, request, T, network_copy, network_copy.requests)
            ordered_requests.append((request, value_ordering_gp))
        ordered_requests.sort(key=lambda x: x[1], reverse=True)

        request_queue = []
        # Processing each request
        for request, value_ordering_gp in ordered_requests:
            vehicle_priority = []
            for vehicle_id in range(1, network_copy.num_vehicle + 1):
                gp_value = choosing_gp(indi, request, T, network_copy, network_copy.trucks[vehicle_id], network_copy.drones[vehicle_id])
                vehicle_priority.append((vehicle_id, gp_value))
            vehicle_priority.sort(key=lambda x: x[1], reverse=True)
            for vehicle_id, _ in vehicle_priority:
                # Insert function
            
            
        T = T + duration
    return cost_sum


def cal_carbon_emission(network: Network, routes):
    carbon_emission = 0
    planning_route, truck_route, drone_route = decode_route(routes)
    truck_route_length = 0
    drone_route_length = 0
    for pos in range(1, len(truck_route)):
        truck_route_length += cal_distance(network.requests[truck_route[pos-1]], network.requests[truck_route[pos]])
    truck_route_length += cal_distance(None, network.requests[truck_route[0]])
    truck_route_length += cal_distance(network.requests[truck_route[-1]], None)

    pre_pos = 0
    for pos in range(1, len(planning_route)):
        if planning_route[pos] in truck_route:
            pre_pos = pos
        else:
            while planning_route[pos] in drone_route:
                pos = pos + 1
            for i in range(pre_pos, pos):
                drone_route_length += cal_distance(network.requests[planning_route[i]], network.requests[planning_route[i+1]])
            pre_pos = pos
    carbon_emission = network.WAER * truck_route_length + network.PGFER * network.AER * drone_route_length
    return carbon_emission

def insert_request(network: Network, vehicle_id, request, T):



            


