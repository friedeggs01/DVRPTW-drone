from gp.node.function import *
from gp.node.terminal import *
from graph.network import Network
from data.read_data import Read_data
from .trainGP import *
import time

def runGP(data_path=None, num_train=30, ):
    data = Read_data(data_path)
    request_list = data.get_R()
    vehicle_list = data.get_V()
    node_list = data.get_N()
    link_list = data.get_L()
    
    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_list)
    
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else:
            request_test.append(request)  
            
    time_start = time.time()  
    _ = trainGP()
    time_end = time.time()
         