from gp.node.function import *
from gp.node.terminal import *
from copy import deepcopy
from gp.population.individual import *
from data.read_data import *
from utils.utils import *
from .deploy_request import *
from graph.network import Network
import math
import time

def calFitness_three_policies(indi: Individual, network: Network, request_list, 
                              duration, start_system_time, end_system_time):
    # storing processing history
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    T = start_system_time
    num_reject = 0 # number of reject request
    carbon_sum = 0 # sum of cost of all request that excuted
    # request_queue = []
    while T <= end_system_time:
        new_request = get_request_list(request_list_copy, T, duration)
        # request_queue.extend(new_request)

        processing_request_list = []
        for request in new_request:
            if T + request.service_time > request.tw_end:
                num_reject += 1
                request.served = 1
                continue
            processing_request_list.append(request)
        # print("request_queue: ", request_queue)
        # Calculate value of GP for each request
        accepted_request = []
        for request in processing_request_list:
            # decide the request is accepted or rejected
            value_of_decision_gp = decision_gp(indi, request, T, network_copy)
            if value_of_decision_gp < 0:
                num_reject = num_reject + 1
                request.served = 1
                continue
            accepted_request.append(request)
        # print("accepted_request: ", accepted_request)
        # Order of accepted requests
        ordered_requests = []
        for request in accepted_request:
            value_ordering_gp = ordering_gp(indi, request, T, network_copy)
            ordered_requests.append((request, value_ordering_gp))
        # print("non-ordered_requests: ", ordered_requests)
        ordered_requests.sort(key=lambda x: x[1], reverse=True)
        # print("ordered_requests: ", ordered_requests)
        request_queue = []
        # Processing each request
        for request, value_ordering_gp in ordered_requests:
            # print("=====================================================")
            # print("request: ", request.request_id)
            vehicle_priority = []
            for vehicle_id in range(network_copy.num_vehicle):
                gp_value = choosing_gp(indi, request, T, network_copy, vehicle_id)
                # print("choosing_gp_value: ", gp_value)
                vehicle_priority.append((vehicle_id, gp_value))
            # print("non-vehicle_priority: ", vehicle_priority)
            vehicle_priority.sort(key=lambda x: x[1], reverse=True)
            # print("vehicle_priority: ", vehicle_priority)
            accepted = False
            for vehicle_id, _ in vehicle_priority:
                # Insert function
                new_route, pos = insert_request(network_copy, vehicle_id, request, T)
                # print("new_route after insert: ", new_route, vehicle_id, request.request_id)
                if new_route == False:
                    continue
                network_copy.routes[vehicle_id] = new_route
                request.served = 1
                accepted = True
                # print("pre_service_time: ", network_copy.pre_service_time)
                service_time = cal_finished_service_time(network_copy, request_list, vehicle_id, new_route, network_copy.pre_service_time, T)
                
                network_copy.update_pre_service_time(service_time)
                break
            if accepted == False:
                request.push_time +=T
                # request_queue.append(request)   
        T = T + duration
    # print("Route")
    for vehicle_id in range(network_copy.num_vehicle):
        # print(network_copy.routes[vehicle_id])
        carbon_sum += cal_carbon_emission(network_copy, network_copy.routes[vehicle_id])
    return carbon_sum, num_reject


def cal_carbon_emission(network: Network, routes):
    # print("+++++++++++++++++Tinh carbon emission+++++++++++++++++++++")
    # print("routes: ", routes)
    carbon_emission = 0
    planning_route, truck_route, drone_route = decode_route(routes)
    truck_route_length = 0
    # print("truck_route: ", truck_route)
    # print("drone_route: ", drone_route)
    # print("planning_route: ", planning_route)

    drone_route_length = 0
    if len(truck_route) == 0:
        return 0
    for pos in range(1, len(truck_route)):
        truck_route_length += cal_distance(network.requests[truck_route[pos-1]], network.requests[truck_route[pos]])
    
    truck_route_length += cal_distance(None, network.requests[truck_route[0]])
    truck_route_length += cal_distance(network.requests[truck_route[-1]], None)

    pre_pos = 0
    for pos in range(1, len(planning_route)):
        if planning_route[pos] in truck_route:
            pre_pos = pos
        else:
            #Co luc sai
            # print("pos: ", pos, planning_route, drone_route)
            while planning_route[pos] in drone_route:
                pos = pos + 1
            for i in range(pre_pos, pos):
                drone_route_length += cal_distance(network.requests[planning_route[i]], network.requests[planning_route[i+1]])
            pre_pos = pos
    carbon_emission = network.WAER * truck_route_length + network.PGFER * network.AER * drone_route_length
    return carbon_emission

def insert_request(network: Network, vehicle_id, request, T):
    planning_route, truck_route, drone_route = decode_route(network.routes[vehicle_id])
    # print("planning_route: ", planning_route)
    start_insert = 0
    for pos in range(len(planning_route)):
        if network.pre_service_time[planning_route[pos]] >= T:
            start_insert = pos
            break
    # insert to truck
    priority_insert_truck = []
    for pos in range(start_insert, len(planning_route) + 1):
        new_route = check_insert(network, vehicle_id, request, pos, 1, T)
        if new_route == False:
            continue
        else:
            carbon_emission = cal_carbon_emission(network, new_route)
            priority_insert_truck.append((pos, carbon_emission))
    
    # insert to drone
    priority_insert_drone = []
    for pos in range(start_insert, len(planning_route) + 1):
        new_route = check_insert(network, vehicle_id, request, pos, 0, T)
        if new_route == False:
            continue
        else:
            carbon_emission = cal_carbon_emission(network, new_route)
            priority_insert_drone.append((pos, carbon_emission))
    # print("priority_insert_truck: ", priority_insert_truck)
    # print("priority_insert_drone: ", priority_insert_drone)
    # time.sleep(5)
    if len(priority_insert_truck) == 0 and len(priority_insert_drone) == 0:
        return False, False

    if len(priority_insert_truck) == 0:
        priority_insert_drone.sort(key=lambda x: x[1])
        pos = priority_insert_drone[0][0]
        new_route = check_insert(network, vehicle_id, request, pos, 0, T)
        return new_route, pos
    if len(priority_insert_drone) == 0:
        priority_insert_truck.sort(key=lambda x: x[1])
        pos = priority_insert_truck[0][0]
        new_route = check_insert(network, vehicle_id, request, pos, 1, T)
        return new_route, pos

    priority_insert_truck.sort(key=lambda x: x[1])
    priority_insert_drone.sort(key=lambda x: x[1])
    if priority_insert_truck[0][1] < priority_insert_drone[0][1]:
        pos = priority_insert_truck[0][0]
        new_route = check_insert(network, vehicle_id, request, pos, 1, T)
        return new_route, pos
    else:
        pos = priority_insert_drone[0][0]
        new_route = check_insert(network, vehicle_id, request, pos, 0, T)
        return new_route, pos
    