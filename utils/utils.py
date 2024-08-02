from copy import deepcopy
import numpy as np

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

def decode_route(routes):
    # Extract the route of truck from encode
    index_1000 = routes.index(1000)
    print("routes: ", routes)
    # đoạn này phải check thêm là nếu không có number after 1000
    list_after_1000 = routes[index_1000 + 1:]
    truck_route = [num for num in routes[:index_1000] if num != list_after_1000]
    drone_routes = []
    
    # Extract the route of drone from encode
    for i in range(len(list_after_1000)):
        index_after_number = routes.index(list_after_1000[i])
        drone_route = []
        if index_after_number > 0:
            drone_route.append(routes[index_after_number - 1])
        drone_route.append(routes[index_after_number])
        if index_after_number < len(routes) - 1:
            drone_route.append(routes[index_after_number + 1])
        drone_routes.append(drone_route)
    return truck_route, drone_routes



def check_customer_timewindow(request, start_time, end_time):
    if request.tw_start <= start_time and request.tw_end >= end_time:
        return True
    return False

def check_timewindow_insert(network, pos, request, vehicle_id, truck_asign):
    # Xác định vị trị của xe trong yêu cầu
    new_route = network.routes[vehicle_id]

    # Lấy hành trình cũ


    if truck_asign == 1:
        # Insert new customer with specific position
        new_route.insert(pos, request.customer_id)
    else:
        new_route.insert(pos, request.customer_id)
        new_route.apeend(request.customer_id)
    
    index_1000 = new_route.index(1000)
    planning_route = new_route[:index_1000]
    truck_route, drone_route = decode(new_route)

    move_to_pos = 0
    for pos_before in range(0, pos):
        customer = planning_route[pos_before]
        if customer in drone_route:
            move_to_pos += network.links[planning_route[pos_before]][planning_route[pos_before+1]] * network.PGFER * network.AER
        else:
            move_to_pos += network.links[planning_route[pos_before]][planning_route[pos_before+1]]


    for pos_after in range(pos, len(planning_route)):











    
    # Insert new customer with specific position
    truck_route.insert(pos, request.customer_id)
    
    for i, cus in enumerate(truck_route):
        # start_ser thời gian kết thúc phục vụ khách hàng cũ + thời gian di chuyển đến khách hàng mới
        if i == 0:
            start_ser = network.links[network.routes[vehicle_id][pos[0]-1]][pos[0]] / network.truck
        else:
            start_ser = network.links[network.routes[vehicle_id][pos[-1]]][pos[-1]+1]
        end_ser = start_ser + network.requests[network.routes[vehicle_id]].service_time
        if start_ser < network.requests[network.routes[vehicle_id]].earliness:
            return False
        if end_ser > network.requests[network.routes[vehicle_id]].lateness:
            return False 
    return True
    
def check_vehiclecapacity(network, pos, request, vehicle_id):
    # trừ dần capacity của xe
    for cus in range(len(network.routes[vehicle_id])):
        if network.trucks[vehicle_id].remain_capacity > network.requests[cus].customer_demand:
            network.trucks[vehicle_id].remain_capacity -= network.requests[cus].customer_demand
        else:
            return False
    return True  