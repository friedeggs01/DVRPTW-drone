from copy import deepcopy
import numpy as np
from graph.network import Network
from graph.requests import Request



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


def cal_finished_service_time(network: Network, request_list, vehicle_id, route):
    service_time = np.zeros(len(request_list) + 1) # thời gian hoàn thành phục vụ
    planning_route, truck_route, drone_route = decode_route(route)

    for pos in range(0, len(planning_route)):
        if pos == 0: # vị trí đầu tiên truck đi từ depot
            service_time[planning_route[pos]] = cal_distance(None, request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity\
                                                + request_list[planning_route[pos]].service_time
            continue
        if planning_route[pos] in drone_route:
            if planning_route[pos-1] in drone_route:
                service_time[planning_route[pos]] = service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity\
                    + request_list[planning_route[pos]].service_time
            elif planning_route[pos-1] in truck_route:
                service_time[planning_route[pos]] = service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity\
                    + network.drones[vehicle_id].time_launch + request_list[planning_route[pos]].service_time # từ drone xuất phát từ truck thì mới cần + launch_time
        elif planning_route[pos] in truck_route:
            pre_pos = pos - 1
            while planning_route[pre_pos] in drone_route:
                pre_pos = pre_pos - 1
            if pre_pos == pos - 1:
                service_time[planning_route[pos]] = service_time[planning_route[pos-1]]\
                    + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity \
                    + request_list[planning_route[pos]].service_time
            else: # hoặc là truck phải chờ drone, hoặc drone xong và phải chờ truck
                service_time[planning_route[pos]] = max(service_time[planning_route[pos - 1]] + cal_distance(request_list[planning_route[pos -1]], request_list[planning_route[pos]])/network.drones[vehicle_id].velocity + network.drones[vehicle_id].time_receive,\
                                                         service_time[planning_route[pre_pos]] + cal_distance(request_list[planning_route[pre_pos]], request_list[planning_route[pos]])/network.trucks[vehicle_id].velocity)\
                                                         + request_list[planning_route[pos]].service_time
    return service_time


def check_each_request_timewindow(request, finish_service_time):
    if (finish_service_time <= request.tw_end) and (finish_service_time - request.service_time >= request.tw_start):
        return True
    else:
        return False

def check_timewindow_route(network, request_list, vehicle_id, start_check, route):
    service_time = cal_finished_service_time(network, request_list, vehicle_id, route)
    planning_route, truck_route, drone_route = decode_route(route)
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

    
def check_vehiclecapacity(network, pos, request, vehicle_id):
    # trừ dần capacity của xe
    for cus in range(len(network.routes[vehicle_id])):
        if network.trucks[vehicle_id].remain_capacity > network.requests[cus].customer_demand:
            network.trucks[vehicle_id].remain_capacity -= network.requests[cus].customer_demand
        else:
            return False
    return True  