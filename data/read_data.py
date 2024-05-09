import json
from graph.network import Node, Link
from graph.requests import Request
from graph.vehicle import Truck, Drone
from utils.utils import get_info_link, get_info_server, get_info_vnf

class Read_data:
    def __init__(self, PATH):
        with open(PATH) as f:
            self.data = json.load(f)
        
    def get_V(self):
        ...
        return 
    
    def get_E(self):
        link_list = []

        return link_list
    
    def get_F(self):
        vnf_list = []

        return vnf_list
    
    def get_R(self):
        r_list = []

        return r_list
    
    def get_info_network(self):
        server_list = self.get_V()
        link_list = self.get_E()
        vnf_list = self.get_F()
        print(len(server_list), len(link_list), len(vnf_list))
        ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server = get_info_server(server_list)
        ram_max_vnf, cpu_max_vnf, mem_max_vnf = get_info_vnf(vnf_list)
        max_bandwidth = get_info_link(link_list)
        return ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server, ram_max_vnf, cpu_max_vnf, mem_max_vnf, max_bandwidth
