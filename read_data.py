import json
from graph.network import Node, Link
from graph.requests import Request
from graph.vehicle import Truck, Drone

class Read_data:
    def __init__(self, PATH):
        with open(PATH) as f:
            self.data = json.load(f)
            
    def get_node(self):
        ...
    
    def get_link(self):
        ...
        
    def get_vehicle(self):
        ...
        
    def get_request(self):
        ...