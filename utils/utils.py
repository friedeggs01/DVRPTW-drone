from copy import deepcopy
import numpy as np
from graph.network import Network
from graph.requests import Request
import time


def cal_distance(r1: Request, r2: Request):
    if r1 is None:
        return np.sqrt(r2.x**2 + r2.y**2)
    if r2 is None:
        return np.sqrt(r1.x**2 + r1.y**2)
    return np.sqrt((r1.x - r2.x)**2 + (r1.y - r2.y)**2)


def decode_route(routes):
    # Extract the route of truck from encode
    index_1000 = routes.index(1000)
    # đoạn này phải check thêm là nếu không có number after 1000
    planning_route = routes[:index_1000]
    drone_route = routes[index_1000 + 1:]
    truck_route = [num for num in routes[:index_1000] if num not in drone_route]
    return planning_route, truck_route, drone_route




def cal_finished_service_time(network: Network, request_list, vehicle_id, new_route, pre_service_time, T):
    pre_service_time = deepcopy(pre_service_time)
    if pre_service_time is None:
        service_time = np.zeros(len(request_list) + 1) # thời gian hoàn thành phục vụ
    else:
        service_time = pre_service_time
    planning_route, truck_route, drone_route = decode_route(new_route)
    start_check_point = 0
    for pos in range(1, len(planning_route)):
        if pre_service_time[planning_route[pos]] > T:
            break
        start_check_point = pos
    for pos in range(start_check_point, len(planning_route)):
        if pos == 0: # vị trí đầu tiên truck đi từ depot
            service_time[planning_route[pos]] = max(cal_distance(None, request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity\
                                                + request_list[planning_route[pos]].service_time, request_list[planning_route[pos]].tw_start + request_list[planning_route[pos]].service_time)
            continue
        if planning_route[pos] in drone_route:
            if planning_route[pos-1] in drone_route:
                service_time[planning_route[pos]] = max(service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity\
                    + request_list[planning_route[pos]].service_time, request_list[planning_route[pos]].tw_start + request_list[planning_route[pos]].service_time)
            elif planning_route[pos-1] in truck_route:
                service_time[planning_route[pos]] = max(service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity\
                    + network.drones[vehicle_id].time_launch + request_list[planning_route[pos]].service_time, request_list[planning_route[pos]].tw_start + request_list[planning_route[pos]].service_time)
        elif planning_route[pos] in truck_route:
            pre_pos = pos - 1
            while planning_route[pre_pos] in drone_route:
                pre_pos = pre_pos - 1
            if pre_pos == pos - 1:
                service_time[planning_route[pos]] = max(service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity \
                    + request_list[planning_route[pos]].service_time, request_list[planning_route[pos]].tw_start + request_list[planning_route[pos]].service_time)
            else: # hoặc là truck phải chờ drone, hoặc drone xong và phải chờ truck
                service_time[planning_route[pos]] = max(max(service_time[planning_route[pos - 1]] + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity + network.drones[vehicle_id].time_receive,\
                                                         service_time[planning_route[pre_pos]] + cal_distance(request_list[planning_route[pre_pos]], request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity)\
                                                         + request_list[planning_route[pos]].service_time, request_list[planning_route[pos]].tw_start + request_list[planning_route[pos]].service_time)
    return service_time


def check_each_request_timewindow(request, finish_service_time):
    # print("Thong tin check time window")
    # print("finish_service_time: ", finish_service_time)
    # print("request.tw_start: ", request.tw_start)
    # print("request.tw_end: ", request.tw_end)


    if finish_service_time == 0:
        return True
    if (finish_service_time <= request.tw_end) and (finish_service_time - request.service_time >= request.tw_start):
        return True
    else:
        # print("Thong tin check time window")
        # print("finish_service_time: ", finish_service_time)
        # print("request.tw_start: ", request.tw_start)
        # print("request.tw_end: ", request.tw_end)
        # print("request.service_time: ", request.service_time)
        # time.sleep(2)
        return False

def check_timewindow_route(network, request_list, vehicle_id, start_check, new_route, T):
    service_time = cal_finished_service_time(network, request_list, vehicle_id, new_route, network.pre_service_time, T)
    # print("service_time: ", service_time)
    # time.sleep(2)
    planning_route, truck_route, drone_route = decode_route(new_route)
    # print("check timewindow route")
    # print("planning_route: ", planning_route)
    # print("service_time: ", service_time)
    # print("start_check and len planning_route: ", start_check, len(planning_route))
    for pos in range(start_check, len(planning_route)):
        if check_each_request_timewindow(request_list[pos], service_time[pos]) == False:
            return False
    return True
    
def get_request_run(request_list, reject, T):
    #print("get request run")
    request_processing = []
    request_reject = []
    for request in request_list:
        if request.arrival == T :
            if request.tw_end > T:
                request_processing.append(request)
            else:
                reject += 1
                request_reject.append(request)      
    return request_processing, request_reject, reject 

def get_request_list(arg_request_list, T, duration):
    request_list = []
    for request in arg_request_list:
        if (request.arrival >= T - duration) and (request.arrival < T):
            request_list.append(request)
    return request_list

def check_insert(network, vehicle_id, request, pos, truck_asign, T):
    planning_route, truck_route, drone_route = decode_route(network.routes[vehicle_id])

    if len(planning_route) == 0:
        finished_time = max(cal_distance(None, request) / network.trucks[vehicle_id].velocity + request.service_time,\
                            request.tw_start + request.service_time)
        if check_each_request_timewindow(request, finished_time) == False:
            return False
        

    if truck_asign == 1:
        # check capacity of truck
        if network.trucks[vehicle_id].used_capacity + request.customer_demand > network.trucks[vehicle_id].capacity:
            return False
        # check timewindow
        new_route = deepcopy(network.routes[vehicle_id])
        new_route.insert(pos, request.request_id)
        if check_timewindow_route(network, network.requests, vehicle_id, pos, new_route, T) == False:
            # print("check timewindow false")
            return False
        return new_route
    else:
        if request.drone_serve == 0:
            return False
        # check capacity of truck and drone
        if (pos == 0) or (pos == len(planning_route)):
            return False
        if network.trucks[vehicle_id].used_capacity + request.customer_demand > network.trucks[vehicle_id].capacity:
            return False
        new_route = deepcopy(network.routes[vehicle_id])
        new_route.insert(pos, request.request_id)
        new_route.append(request.request_id)
        if (new_route[pos - 1] in drone_route) or(new_route[pos + 1] in drone_route):
            pre_pos = pos - 1
            while new_route[pre_pos] in drone_route:
                pre_pos = pre_pos - 1
            after_pos = pos + 1
            while new_route[after_pos] in drone_route:
                after_pos = after_pos + 1
            sum_demand_drone_segement = 0
            for i in range(pre_pos + 1, after_pos):
                sum_demand_drone_segement += network.requests[new_route[i]].customer_demand
            # network.drones[vehicle_id].rema
            if sum_demand_drone_segement > network.drones[vehicle_id].capacity:
                return False
        else:
            if request.customer_demand > network.drones[vehicle_id].capacity:
                return False
        # check timewindow
        if check_timewindow_route(network, network.requests, vehicle_id, pos, new_route, T) == False:
            return False
        return new_route
        
            


