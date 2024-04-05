from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from decision_var import Decision, Chosing
from graph.network import Network
from utils import *
import time 
import multiprocessing     
import csv
import numba as nb
import random

def trainGP(processing_number, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_list, pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    
    time_start = time.time()
    decision_pop = Population(pop_size, function, terminal_decision)
    
    decision_pop.random_init()
    
    decision_best = decision_pop.indivs[0]
    
    print("===Finished initialization===")    
    pool = multiprocessing.Pool(processes=processing_number)
    
    for indi in decision_pop.indivs:
        ...
    
    return time.time()-time_start


def run_proposed(data_path, processing_num, alpha, num_train,  pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    data = Read_data(data_path)
    request_list = data.get_request()
    vehicle = data.get_vehicle()
    node_list = data.get_node()
    link_node = data.get_link()
    
    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    network.add_truck_to_network(vehicle)
    network.add_drone_to_network(vehicle)
    
    
    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_decision = []
    terminal_chosing = []
    
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
        
    best, _ = trainGP(processing_num, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_train, pop_size, min_height, max_height, initialization_max_height, evaluation, max_gen, crossover_rate, mutation_rate)