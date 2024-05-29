from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from singleObjective.singleObjective import run_SingleObjective
from deployment.evaluation import calFitness_three_policies, calFitness_removeGPvalue
from utils.crossover import *
from utils.mutation import *
import multiprocessing
from data.read_data import *
from utils.initialization import *

if __name__ == '__main__':
    multiprocessing.freeze_support()
    num_pro = 10
    num_train = 10
    pop_size = 30
    max_gen = 20
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.8
    pc = 0.8
    pm = 0.1
    num_neigbor = 10

    crossover_operator_list = [crossover_branch_individual_swap, crossover_sub_tree_swap]
    mutation_operator_list = [mutation_individual_branch_replace, mutation_individual_node_replace, mutation_individual_branch_swap, mutation_value_decision]
    neighborhood_size = 3
    max_NFE = 500
    data_set = [r'data_1_9/nsf_rural_normal_s3.json', r'data_1_9/nsf_uniform_normal_s3.json', r'data_1_9/nsf_uniform_hard_s3.json',
                r'data_1_9/conus_urban_easy_s3.json', r'data_1_9/conus_urban_normal_s3.json', r'data_1_9/conus_urban_hard_s3.json',]
    for data_path in data_set:
        data = Read_data(data_path)
        _ = data.get_info_network()
        function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
        terminal_decision = [ATR(), Const()]
        
        terminal_choosing = [SDR(), DDR(), DCC(), CRS(), CDS(), TRC(...), DRC(...), DRB(...), Const()]
        terminal_routing = [Const()]

        decision_tree = Const()
        routing_tree = ...

        pop = random_population_init(pop_size, min_height, initialization_max_height,
                           function, terminal_decision, terminal_choosing, terminal_routing, decision_tree, routing_tree)
        
        result = run_SingleObjective( data_path, num_pro, pop.indivs, num_train,  
                function, terminal_decision, terminal_choosing, terminal_routing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                crossover_operator_list, mutation_operator_list, calFitness_three_policies, None, 1)