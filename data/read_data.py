from graph.network import Node, Link, Network
from graph.requests import Request
from graph.vehicle import Truck, Drone
import numpy as np

class Read_data:
    def __init__(self):
        self.num_vehicle = None
        self.truck_capacity = None
        self.network = None
        self.drone_capacity = None
        self.drone_endurance = None
        
    def read(self, PATH):
        customers = {}
        requests = []
        with open(PATH, 'r') as f:
            all = f.readlines()
        for i in range(len(all)): #nhap du lieu, tao file cac request, customer
            if all[i] == 'NUMBER     CAPACITY    DRONE-CAPACITY    DRONE-ENDURANCE    \n':
                self.num_vehicle, self.truck_capacity, self.drone_capacity, self.drone_endurance = map(int,all[i+1].strip().split())
                # print(self.num_vehicle, self.truck_capacity, self.drone_capacity, self.drone_endurance)
            if all[i] == 'CUSTOMER\n':
                arrival_time = 0
                while (i+4)<len(all):
                    # print(i, len(all))
                    arrival_time += 1
                    # print(arrival_time)
                    num, x, y, demand, tw_start, tw_end, service_time, drone_served = map(int,all[i+3].strip().split())
                    # print(num, x, y, demand, tw_start, tw_end, service_time, drone_served)

                    req = Request(customer_id= int(num),x= x, y= y, customer_demand= demand,arrival_time=arrival_time, service_time=service_time, tw_start= tw_start, tw_end= tw_end, earliness=tw_start-60, lateness=tw_end+60, drone_serve=drone_served)
                    requests.append(req) 
                    node = Node(id = int(num), x=x, y=y)
                    customers[int(num)] = node
                    i=i+1
                break 
        
        # calculate distance
        links = np.zeros((num+1, num+1))
        for i in range (num+1):
            for j in range (num+1):
                # print(i, j, requests[i].x, requests[i].y)
                dist = np.sqrt((requests[i].x - requests[j].x)**2 + (requests[i].y - requests[j].y)**2)
                links[i][j] = dist
                links[j][i] = dist
        self.network = Network(customers, links, self.num_vehicle, self.truck_capacity, self.drone_capacity, self.drone_endurance, requests)
        #bo depot ra khoi request
        requests.remove(requests[0])
        return self.network, requests    