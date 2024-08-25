from data.read_data import *
from graph.network import Network
from utils.utils import *
from gp.population.population import *
import multiprocessing     
import random
from utils.initialization import individual_init


class SingleObjectivePopulation(Population):
    def __init__(self, pop_size, functions, decision_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                ):
        super().__init__(pop_size, 
                 functions, decision_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 )

   
    def gen_offspring(self, crossover_operator_list, mutation_operator_list):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            # print("indi1: ", indi1)
            # print("indi1.decision_tree: ", indi1.decision_tree.GetHumanExpression())
            # print("indi1.ordering_tree: ", indi1.ordering_tree.GetHumanExpression())
            # print("indi1.choosing_tree: ", indi1.choosing_tree.GetHumanExpression())
            if np.random.random() < self.crossover_rate:
                for crossover_operator in crossover_operator_list:
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height, indi1.decision_tree, indi1.ordering_tree, indi1.choosing_tree)
                    offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, 
                                                self.decision_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, indi1.decision_tree)
                    mutant2 = mutation_operator(indi2, self.functions, 
                                                self.decision_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, indi1.decision_tree)
                    offspring.extend([mutant1, mutant2])
            if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
                indi = individual_init(self.min_height, self.max_height,  self.functions,
                                    self.decision_terminals, self.ordering_terminals, self.choosing_terminals,  indi1.decision_tree)
                offspring.append(indi)
        return offspring
    
    def natural_selection(self, alpha):
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        self.indivs = self.indivs[:self.pop_size]
    
    def take_best(self, alpha):
        print("self.indivs[0]: ", self.indivs[0])
        print("First individual's objectives: ", self.indivs[0].objectives[0])
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        return self.indivs[0]


def trainSingleObjective(processing_number, indi_list, network, request_list,
                functions, terminal_decision,terminal_ordering, terminal_choosing, 
                pop_size, max_gen, min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, ordering_tree, 
                alpha, duration, start_system_time, end_system_time):
    print("Số request:", len(request_list))
    pop = SingleObjectivePopulation(pop_size, functions, terminal_decision, terminal_ordering, 
                                    terminal_choosing, min_height, max_height, initialization_max_height, 
                                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate)

    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []

    for indi in pop.indivs:
        indi.objectives[0], indi.objectives[1] = calFitness(indi, network, request_list, duration, start_system_time, end_system_time)
    print("Khởi tạo xong ")  
    print("pop: ", pop)
    best = pop.take_best(alpha)
    print("The he 0:")
    print(best.objectives)    
    for i in range(max_gen):
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0], indi.objectives[1] = value
  
        pop.indivs.extend(offspring)
        pop.natural_selection(alpha)
        best = pop.take_best(alpha)   
        print("The he ", i+1)
        print(best.objectives)      
    pool.close()
    return best

def run_SingleObjective(data_path, processing_num, 
                num_vehicle, truck_capacity, drone_capacity, drone_endurance,
                indi_list, num_train,  
                functions, terminal_decision, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, decision_tree, alpha,
                duration, start_train, end_train, end_test):
    reader = Read_data()
    request_list = reader.read_request(data_path) 
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
            
    network = Network(request_train, num_vehicle, truck_capacity, drone_capacity, drone_endurance)
    best = trainSingleObjective(processing_num, indi_list, network, request_train,
                    functions, terminal_decision,terminal_ordering,  terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                    crossover_operator_list, mutation_operator_list, calFitness, decision_tree, alpha,
                    duration, start_train, end_train)

    carbon_sum, accepted_request = calFitness(best, network, request_test)
    return  True