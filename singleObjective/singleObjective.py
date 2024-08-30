from data.read_data import *
from graph.network import Network
from utils.utils import *
from gp.population.population import *
import multiprocessing     
import random
import os
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
                 

   # Em sửa lại hàm gen_offspring khi tham số truyền vào có 3 biến decision_tree, ordering_tree, choosing_tree
   # Sửa trong 2 file crossover và mutation 
   # Để nếu tree = None thì sẽ tạo ra cây mới nếu không sẽ không học cây đó
   # Hiện tại a đang để học 3 cây
   # A sửa đổi và bổ sung các terminal mới, thay đổi class Decision, Choosing, Ordering


    def gen_offspring(self, crossover_operator_list, mutation_operator_list, decision_tree, ordering_tree, choosing_tree):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            if np.random.random() < self.crossover_rate:
                for crossover_operator in crossover_operator_list:
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height, decision_tree, ordering_tree, choosing_tree)
                    offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, 
                                                self.decision_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, decision_tree, ordering_tree, choosing_tree)
                    mutant2 = mutation_operator(indi2, self.functions, 
                                                self.decision_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, decision_tree, ordering_tree, choosing_tree)
                    offspring.extend([mutant1, mutant2])
            if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
                indi = individual_init(self.min_height, self.max_height,  self.functions,
                                    self.decision_terminals, self.ordering_terminals, self.choosing_terminals,  decision_tree, ordering_tree, choosing_tree)
                offspring.append(indi)
        return offspring
    
    def natural_selection(self):
        self.indivs.sort(key=lambda x: x.fitness)
        self.indivs = self.indivs[:self.pop_size]
        return self.indivs[0]


def trainSingleObjective(data_path, processing_number, indi_list, network, request_list,
                functions, terminal_decision,terminal_ordering, terminal_choosing, 
                pop_size, max_gen, min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness,
                alpha, duration, start_system_time, end_system_time, 
                decision_tree, ordering_tree, choosing_tree, carbon_upper, reject_upper):
    
    pop = SingleObjectivePopulation(pop_size, functions, terminal_decision, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, initialization_max_height, 
                                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate)

    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []

    for indi in pop.indivs:
        arg.append((indi, network, request_list, duration, start_system_time, end_system_time))
    result = pool.starmap(calFitness, arg)

    # for indi in pop.indivs:
    #     indi.objectives[0], indi.objectives[1] = calFitness(indi, network, request_list, duration, start_system_time, end_system_time)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0], indi.objectives[1] = value
        indi.cal_fitness_indi(alpha, carbon_upper, reject_upper)
    
    # for indi in pop.indivs:
    #     print(indi.objectives)
    
    best_indi = pop.natural_selection()
    print("Generation 0:", best_indi.objectives)
    
    # Save result
    file_name = f'result\\{data_path}'
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    with open(file_name, "a") as file:
        file.write(f"Generation 0: {best_indi.objectives}\n")

    for i in range(max_gen):
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list, 
                                      decision_tree, ordering_tree, choosing_tree)
        
        # print(len(offspring))
        # for indi in offspring:
        #     indi.objectives[0], indi.objectives[1] = calFitness(indi, network, request_list, duration, start_system_time, end_system_time)
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, duration, start_system_time, end_system_time))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0], indi.objectives[1] = value
            indi.cal_fitness_indi(alpha, carbon_upper, reject_upper)
  
        pop.indivs.extend(offspring)
        best = pop.natural_selection()
        # best = pop.take_best()   
        print("The he " + str(i+1) + ":", best.objectives)  
        
        # Save result
        file_name = f'result\\{data_path}'
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        with open(file_name, "a") as file:
            file.write(f"Generation {str(i+1)}: {best_indi.objectives}\n")  
    pool.close()
    return best

def run_SingleObjective(data_path, processing_num, 
                num_vehicle, truck_capacity, drone_capacity, drone_endurance,
                indi_list,  
                functions, terminal_decision, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, 
                decision_tree, ordering_tree, choosing_tree, 
                alpha, duration, start_train, end_train, end_test):
    reader = Read_data()
    request_list = reader.read_request(data_path)      
    network = Network(request_list, num_vehicle, truck_capacity, drone_capacity, drone_endurance)

    # sum_max_dis = 0
    # for i in range (len(request_list)):
    #     max_each_request = 0
    #     for j in range(len(request_list)):
    #         if i != j:
    #             max_each_request = max(max_each_request, cal_distance(request_list[i], request_list[j]))
    #     sum_max_dis += max_each_request
    # depo_max = 0
    # for i in range(len(request_list)):
    #     depo_max = max(depo_max, cal_distance(None, request_list[i]))
    # sum_max_dis  = sum_max_dis + 2*depo_max*network.num_vehicle
    # carbon_upper = sum_max_dis/network.trucks[0].velocity*network.WAER
    # reject_upper = len(request_list)
    # print("Carbon upper: ", carbon_upper)
    # print("Reject upper: ", reject_upper)
    carbon_upper = 100000
    reject_upper = 1000
    best = trainSingleObjective(data_path, processing_num, indi_list, network, request_list,
                functions, terminal_decision,terminal_ordering, terminal_choosing, 
                pop_size, max_gen, min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness,
                alpha, duration, start_train, end_train, 
                decision_tree, ordering_tree, choosing_tree, carbon_upper, reject_upper)
    return  best.objectives