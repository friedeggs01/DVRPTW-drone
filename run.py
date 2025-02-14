import os
from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from singleObjective.singleObjective import run_SingleObjective
from deployment.evaluation import calFitness_three_policies
from utils.crossover import *
from utils.mutation import *
import multiprocessing
from utils.initialization import *

# Function to collect file paths
def collect_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            formatted_path = os.path.join(folder_path, relative_path)
            file_paths.append(formatted_path)
    return file_paths

if __name__ == "__main__":
    folder_path = "data"
    file_paths = collect_file_paths(folder_path)

    # Filter out unwanted files
    list_file_path = [path for path in file_paths if path not in [
        'data\\dvrptw-setting.txt',
        'data\\read_data.py',
        'data\\__pycache__\\read_data.cpython-311.pyc'
    ]]

    # Algorithm parameters
    num_pro = 10
    pop_size = 100
    max_gen = 50
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.8
    pc = 0.8
    pm = 0.1

    # Vehicle parameters
    num_vehicle_100 = [3, 5, 10]
    num_vehicle_1000 = [20, 50, 100]
    truck_capacity = 1300
    drone_capacity = 10
    drone_endurance = 30

    # Reproduction operators
    crossover_operator_list = [crossover_branch_individual_swap]
    mutation_operator_list = [mutation_individual_branch_replace]

    # Data parameters
    alpha = 0.5
    duration = 10
    start_train = 0
    end_train = 2000
    end_test = end_train

    # Node of tree
    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_decision = [MVC(), ATR(), SDR(), TWE(), WTR(), DDR(), DEM(), PN(), ST(), MD(), Const()]
    terminal_ordering = [ATR(), SDR(), TWE(), WTR(), DDR(), DEM(), PN(), ST(), MD(), Const()]
    terminal_choosing = [TTC(), DTC(), TRC(), PL(), NC(), MDV(), Const()]

    # Execute the main loop for each data file
    for data_path in list_file_path:
        print("data_path: ", data_path)
        if '1000' in data_path:
            for veh in num_vehicle_1000:
                decision_tree = None
                ordering_tree = None
                choosing_tree = None

                indi_list = random_population_init(pop_size, min_height, initialization_max_height,
                                    function, terminal_decision, terminal_ordering, terminal_choosing, 
                                    decision_tree, ordering_tree, choosing_tree)

                result, res_gen = run_SingleObjective(data_path, num_pro, 
                                veh, truck_capacity, drone_capacity, drone_endurance,
                                indi_list,  
                                function, terminal_decision, terminal_ordering, terminal_choosing, 
                                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                                num_of_tour_particips, tournament_prob, pc, pm,
                                crossover_operator_list, mutation_operator_list, calFitness_three_policies, 
                                decision_tree, ordering_tree, choosing_tree, 
                                alpha, duration, start_train, end_train, end_test)
            
                file_name = f'result\\{veh}\\{data_path}'
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                print("result file: ", file_name)
                with open(file_name, "a") as file:
                    for res in res_gen:
                        res = ' '.join(map(str, res))
                        file.write(res + '\n') 
        else:
            for veh in num_vehicle_100:
                decision_tree = None
                ordering_tree = None
                choosing_tree = None

                indi_list = random_population_init(pop_size, min_height, initialization_max_height,
                                    function, terminal_decision, terminal_ordering, terminal_choosing, 
                                    decision_tree, ordering_tree, choosing_tree)

                result, res_gen = run_SingleObjective(data_path, num_pro, 
                                veh, truck_capacity, drone_capacity, drone_endurance,
                                indi_list,  
                                function, terminal_decision, terminal_ordering, terminal_choosing, 
                                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                                num_of_tour_particips, tournament_prob, pc, pm,
                                crossover_operator_list, mutation_operator_list, calFitness_three_policies, 
                                decision_tree, ordering_tree, choosing_tree, 
                                alpha, duration, start_train, end_train, end_test)
            
                file_name = f'result\\{veh}\\{data_path}'
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
                print("result file: ", file_name)
                with open(file_name, "a") as file:
                    for res in res_gen:
                        res = ' '.join(map(str, res))  
                        file.write(res + '\n')  
