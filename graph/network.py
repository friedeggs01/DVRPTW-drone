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
    def __init__(self, request_list, num_vehicle, truck_capacity, drone_capacity, drone_endurance):
        self.make_span = 0
        self.carbon_emission = {}
        self.WAER = 1.2603 # kg/mile
        self.PGFER = 0.0003773 # kg/Wh
        self.AER = 3.3333 # Wh/mile
        # self.nodes = customers
        # self.links = links # list of links between nodes
        self.num_vehicle = num_vehicle # number of truck
        self.truck_capacity = truck_capacity
        self.drone_capacity = drone_capacity
        self.drone_endurance = drone_endurance
        self.pre_service_time = None
        self.requests = request_list
        
        self.trucks = {}
        self.routes = {}
        for i in range(num_vehicle):
            self.trucks[i] = Truck(i, truck_capacity)
            
        self.drones = {}
        for i in range(num_vehicle):
            self.drones[i] = Drone(i, drone_capacity)
            
        for i in range(num_vehicle):
            self.routes[i] = [1000]
        
    def check_constraint(self, request, vehicle_id): # tìm đường đầu tiên thỏa mãn constraint cho request
        network = deepcopy(self)
        for pos in range(len(self.routes[vehicle_id])): 
            if self.check_timewindow(network, pos, request, vehicle_id) == True and self.check_vehiclecapacity(network, pos, request, vehicle_id) == True:
                return True, pos
        return False
    
    def update_pre_service_time(self, service_time):
        self.pre_service_time = service_time
        
 