import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
import pandas as pd
import json
from copy import deepcopy

from .vehicle import *

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.links = []
    
class Link:
    def __init__(self, u, v, dist):
        self.u = u # first node
        self.v = v # second node
        self.dist = dist
    
class Network:
    def __init__(self, customers, links, num_vehicle, truck_capacity, drone_capacity, drone_endurance, requests):
        self.make_span = 0
        self.carbon_emission = {}
        self.WAER = 1.2603 # kg/mile
        self.PGFER = 0.0003773 # kg/Wh
        self.AER = 3.3333 # Wh/mile
        self.nodes = customers
        self.links = links # list of links between nodes
        self.num_vehicle = num_vehicle # number of truck
        self.truck_capacity = truck_capacity
        self.drone_capacity = drone_capacity
        self.drone_endurance = drone_endurance
        
        self.requests = requests
        
        self.trucks = {}
        self.truck_routes = {}
        for i in range(num_vehicle):
            self.trucks[i] = Truck(i, truck_capacity)
            self.truck_routes[i] = []
            
        self.drones = {}
        self.drone_routes = {}
        for i in range(num_vehicle):
            self.drones[i] = Drone(i, drone_capacity)
            self.drone_routes[i] = []

        
    def update_cost(self, vehicle_id):
        
        # calculate lại khí carbon tạo ra bởi cặp truck-drone
        self.carbon_emission[vehicle_id] = 0 
        truck_route = []
        drone_route = []
        pos = []                
        if len(truck_route) < 2:
            current_customer = 0
            next_customer = self.routes[vehicle_id][0]
            self.carbon_emission[vehicle_id] += self.WAER * self.links[current_customer][next_customer]
        else:
            # Extract the route of truck from encode
            index_1000 = self.routes[vehicle_id].index(1000)
            number_after_1000 = self.routes[vehicle_id][index_1000 + 1]
            truck_route = [num for num in self.routes[vehicle_id][:index_1000] if num != number_after_1000]

            # Extract the route of drone from encode
            index_after_number = self.routes[vehicle_id].index(number_after_1000)
            drone_route = []
            if index_after_number > 0:
                drone_route.append(self.routes[vehicle_id][index_after_number - 1])
            drone_route.append(self.routes[vehicle_id][index_after_number])
            if index_after_number < len(self.routes[vehicle_id]) - 1:
                drone_route.append(self.routes[vehicle_id][index_after_number + 1])
            
            # Calculate the carbon emission of each route
            for i in range(len(truck_route)):
                current_customer = truck_route[i]
                next_customer = truck_route[i+1]
                self.carbon_emission[vehicle_id] += self.WAER * self.links[current_customer][next_customer]
            for i in range(drone_route):
                current_customer = drone_route[i]
                next_customer = drone_route[i+1]
                self.carbon_emission[vehicle_id] += self.PGFER * self.AER * self.links[current_customer][next_customer]
            self.carbon_emission[vehicle_id] += self.PGFER * self.AER * self.links[self.routes[vehicle_id][pos[0]-1]][pos[0]]
            self.carbon_emission[vehicle_id] += self.PGFER * self.AER * self.links[self.routes[vehicle_id][pos[-1]]][pos[-1]+1]
        
        return self.carbon_emission[vehicle_id]
        
    def check_constraint(self, request, vehicle_id): # tìm đường đầu tiên thỏa mãn constraint cho request
        network = deepcopy(self)
        for pos in range(len(self.routes[vehicle_id])): 
            if self.check_timewindow(network, pos, request, vehicle_id) == True and self.check_vehiclecapacity(network, pos, request, vehicle_id) == True:
                return True, pos
        return False
    
    def check_timewindow(self, network, pos, request, vehicle_id):
        # request được chèn vào vị trí pos trên tuyến đường của vehicle_id
        truck_route = []
        drone_route = []
    
        # Extract the route of truck from encode
        index_1000 = self.routes[vehicle_id].index(1000)
        number_after_1000 = self.routes[vehicle_id][index_1000 + 1]
        truck_route = [num for num in self.routes[vehicle_id][:index_1000] if num != number_after_1000]

        # Extract the route of drone from encode
        index_after_number = self.routes[vehicle_id].index(number_after_1000)
        drone_route = []
        if index_after_number > 0:
            drone_route.append(self.routes[vehicle_id][index_after_number - 1])
        drone_route.append(self.routes[vehicle_id][index_after_number])
        if index_after_number < len(self.routes[vehicle_id]) - 1:
            drone_route.append(self.routes[vehicle_id][index_after_number + 1])
        
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
        
        
 