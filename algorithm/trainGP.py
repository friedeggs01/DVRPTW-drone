import multiprocessing     
import random
import numpy as np

from data.read_data import *
from graph.network import Network
from utils.utils import *
from gp.population.population import *
from utils.initialization import individual_init
from utils.selection import natural_selection


class GPPopulation(Population):
    def __init__(self, pop_size, 
                 functions, decision_terminals, choosing_terminals, 
                 min_depth, max_depth, initialization_max_tree_depth, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate):
        super().__init__(self, pop_size, 
                 functions, decision_terminals, choosing_terminals, 
                 min_depth, max_depth, initialization_max_tree_depth, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate)
        
    def gen_offspring(self, crossover_operator_list, mutation_operator_list):    
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
        if np.random.random() < self.crossover_rate:
            for crossover_operator in crossover_operator_list:
                children1, children2 = crossover_operator(indi1, indi2, self.min_depth, self.max_depth)
                offspring.extend([children1, children2])
        if np.random.random() < self.mutation_rate:
            for mutation_operator in mutation_operator_list:   
                children1 = mutation_operator(indi1, self.functions, self.decision_terminals, self.choosing_terminals, self.min_depth, self.max_depth)
                children2 = mutation_operator(indi2, self.functions, self.decision_terminals, self.choosing_terminals, self.min_depth, self.max_depth)
                offspring.extend([children1, children2])
        if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
            indi = individual_init(self.min_depth, self.max_depth,  self.functions,
                                   self.decision_terminals, self.ordering_terminals, self.choosing_terminals,  self.decision_tree)
            offspring.append(indi)
        return offspring
    def natural_selection(self, alpha):
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        self.indivs = self.indivs[:self.pop_size]
        
    def take_best(self, alpha):
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        return self.indivs[0]	 

def trainGP(processing_number=5, indi_list, network, request_list, vehicle_list,
            functions, decision_terminals, choosing_terminals,
            pop_size, max_gen, min_depth, max_depth, initialization_max_depth,
            num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
            crossover_operator_list, mutation_operator_list, calFitness, decision_tree, ):
    
    pop = GPPopulation(pop_size, 
                 functions, decision_terminals, choosing_terminals, 
                 min_depth, max_depth, initialization_max_depth, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate)
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    result = pool.starmap(calFitness, arg)
    print("====Finished initialization====")
    
    best = pop.take_best(alpha)
    print("The he 0:")
    print(best.objecitves)
    
    for i in range(max_gen):
        offspring = pop.gen_offspring(crossover_operator_list, mutation_list
                                      
                                      )
    
    print("The he ", i+1)
    print(best.objectives, best.reject, best.cost) 
    pool.close()
    return best