import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
import pandas as pd
import json

from .vehicle import *

class Node:
    def __init__(self, id):
        self.id = id
        self.links = []
    
class Link:
    def __init__(self, u, v, truck_dist, drone_dist):
        self.u = u # first node
        self.v = v # second node
        self.truck_dist = truck_dist
        self.drone_dist = drone_dist
    
class Network:
    def __init__(self):
        self.make_span = 0
        self.carbon_emission = 0
        self.nodes = {} # list of all nodes
        self.links = [] # list of links between nodes
        self.trucks = {} # list of trucks 
        self.drones = {} # list of drones
        
        
    def add_depot_node(self, id):
        depot_node = Node(id)
        self.nodes[id] = depot_node
        
    def add_customer_node(self, id, tw_start, tw_end, earliness, lateness):
        customer_node = Node(id, tw_start, tw_end, earliness, lateness)
        self.nodes[id] = customer_node
        
    def add_node_to_network(self, node_list):
        for node in node_list:
            if node.id == 0:
                self.add_depot_node(node.id)
            else:
                self.add_customer_node(node.id, node.tw_start, node.tw_end, node.earliness, node.lateness)
    
    def add_link(self, u, v, truck_dist, drone_dist):
        u = self.nodes[u]
        v = self.nodes[v]
        link = Link(u, v, truck_dist, drone_dist)
        self.links.append(link)
        link.u.links.append(link)
        link.v.links.append(link)
    
    def add_link_to_network(self, link_list):
        for link in link_list:
            self.add_link(link.u, link.v, link.truck_dist, link.drone_dist)
            
    def add_vehicle_to_network(self, trucks):
        for truck in trucks:
            ...
 