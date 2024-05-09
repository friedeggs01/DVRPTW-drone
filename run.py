from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from priority_gp.decision_var import Decision, Chosing
from graph.network import Network
from utils import *
import time 
import multiprocessing     
import csv
import numba as nb
import random

def trainGP(processing_number, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_list, pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    fitness_history = {}
    fitness_history['decision'] = []
    fitness_history['chosing'] = []
    
    time_start = time.time()
    
    decision_pop = Population(pop_size , function, terminal_decision, min_height, max_height, initialization_max_height, evaluation)
    chosing_pop = Population(pop_size , function, terminal_chosing, min_height, max_height, initialization_max_height, evaluation)
    
    decision_pop.random_init()
    chosing_pop.random_init()
    
    decision_best = decision_pop.indivs[0]
    chosing_best = chosing_pop.indivs[0]

    
    print("===Finished initialization===")    
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in decision_pop.indivs:
        ...
    
    print("====Calculate initialize fitness is done====")
    
    for i in range(max_gen):
        decision_offspring = decision_pop.reproduction(crossover_rate, mutation_rate)
        chosing_offspring = chosing_pop.reproduction(crossover_rate, mutation_rate)
        
        arg = []
        for indi in decision_offspring:
            arg.append()
        
        result = ...
        
        decision_pop.indivs.extend(decision_offspring)
        
        decision_pop.natural_selection()
        
    pool.close()    
    return decision_best, decision_best.fitness, time.time()-time_start

def calFitness_removeGPvalue(alpha, decision_indi, chosing_indi, network, request_test, vnf_list):
    network_copy = deepcopy(network)
    request_test_copy = deepcopy(request_test)
    
    # Execution time slot
    T = request_test_copy[0].arrival
    reject = 0 # number of reject request
    
    while len(request_test_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_test_copy, 0, T)
        for request in request_processing:
            request_test_copy.remove(request)
        for request in reject_request:
            request_test_copy.remove(request)
        reject = reject + reject1
        
        # Calculate value of GP for each request
        for request in request_processing:
        
        T = T + 1
    return ...



def run_proposed(data_path, processing_num, alpha, num_train,  pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    data = Read_data(data_path)
    request_list = data.get_request()
    vehicle = data.get_vehicle()
    node_list = data.get_node()
    link_node = data.get_link()
    
    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    network.add_vehicle_to_network(vehicle)
    
    
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
        
    decision_best, chosing_best, sum_gen, fitness_train, time_train, fitness_history = trainGP(processing_num, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_train, pop_size, min_height, max_height, initialization_max_height, evaluation, max_gen, crossover_rate, mutation_rate)

    fitness, reject, cost, proc = calFitness_removeGPvalue(alpha, decision_best, chosing_best, network, request_test)
    return fitness, reject, cost, proc, sum_gen, fitness_train, time_train, fitness_history