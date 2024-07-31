from gp.node.function import *
from gp.node.terminal import *
from copy import deepcopy
# from gp.population.gp import *
from gp.population.individual import *
from data.read_data import *
from utils.utils import *
from .deploy_request import *
from graph.network import Network

import math

def calFitness_three_policies(indi: Individual, network: Network, request_list):
    # storing processing history
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    sum_request = len(request_list_copy)

    # Execution time slot
    T = request_list_copy[0].arrival
    reject = 0 # number of reject request
    cost_sum = 0 # sum of cost of all request that excuted 
    while len(request_list_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_list_copy, 0, T)
        for request in request_processing:
            request_list_copy.remove(request)
        for request in reject_request:
            request_list_copy.remove(request)
        reject = reject + reject1 # number of rejected request

        request_decision = []
        # Calculate value of GP for each request
        for request in request_processing:
            
            # decide the request is accepted or rejected
            value_of_decision_gp = decision_gp(T)
            if value_of_decision_gp < 0:
                reject = reject + 1
                continue
            
            # choose the truck-drone own the highest gp-value
            value_of_choosing_gp = {}
            for i in range(network_copy.num_vehicle):
                value_of_choosing_gp[i] = (choosing_gp(indi, request, T, network_copy, network_copy.trucks[i], network_copy.drones[i]))
                print("=====value_of_choosing_gp[i]======= ", value_of_choosing_gp[i])
            veh_with_highest_value = max(value_of_choosing_gp, key=value_of_choosing_gp.get)
            
            # find the route by insert new customer into existed route of the truck-drone
            print("request.customer_id: ", request.customer_id)
            print("network.routes[veh_with_highest_value]: ", network.routes[veh_with_highest_value])
            
            if len(network.routes[veh_with_highest_value]) < 2:
                index = network.routes[veh_with_highest_value].index(10000) # idea là ban đầu khởi tạo tất cả sẽ có 10000, nếu phương tiện chưa thăm chỗ nào thì gán customer đấy cho truck trước tiên
                network.routes[veh_with_highest_value].insert(index, request.customer_id)
                print("network.routes[veh_with_highest_value] after insert: ", network.routes[veh_with_highest_value])
                
                if (len(network.routes[veh_with_highest_value]) == 2): # chỉ có một customer, thời gian bắt đầu phục vụ sẽ bằng thời gian đi từ kho tới chỗ customer ấy
                    request.serving_start = network.links[0][network.routes[veh_with_highest_value][0]] / network.trucks[veh_with_highest_value].velocity
                if (len(network.routes[veh_with_highest_value]) == 3): # có hai customer nên thời gian bắt đầu phục vụ của customer thứ hai sẽ bằng thời gian đi từ 0->cus1->cus2
                    request.serving_start = (network.links[0][network.routes[veh_with_highest_value][0]] + network.links[network.routes[veh_with_highest_value][0]][network.routes[veh_with_highest_value][1]]) / network.trucks[veh_with_highest_value].velocity
                request.serving_end = request.serving_start + request.service_time
                
                for t in range(math.floor(request.serving_start), math.ceil(request.serving_end)):
                    print("network.trucks[veh_with_highest_value].remain_capacity[t]: ", network.trucks[veh_with_highest_value].remain_capacity[t])
                    network.trucks[veh_with_highest_value].remain_capacity[t] -= request.customer_demand
                cost_sum += network.update_cost(veh_with_highest_value)
            elif request.drone_serve == True and network.check_constraint(request, veh_with_highest_value):
                index = network.routes[veh_with_highest_value].index(10000)
                network.routes[veh_with_highest_value].insert(index, request.customer_id)
                network.routes[veh_with_highest_value].append(request.customer_id)
            elif network.check_constraint(request):
                network.routes[veh_with_highest_value].append(request.customer_id)
                cost_sum += network.update()
            
        T = T + 1
    return cost_sum



# route [2, 3, 4, 5, 6, 1000, 4]