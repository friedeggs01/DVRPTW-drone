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