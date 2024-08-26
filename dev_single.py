from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from singleObjective.singleObjective import run_SingleObjective
from deployment.evaluation import calFitness_three_policies
from utils.crossover import *
from utils.mutation import *
import multiprocessing
from data.read_data import *
from utils.initialization import *
    

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
num_vehicle = 3
truck_capacity = 1300
drone_capacity = 10
drone_endurance = 30

crossover_operator_list = [crossover_branch_individual_swap]
mutation_operator_list = [mutation_individual_branch_replace]
neighborhood_size = 3
max_NFE = 500
data_path = r"data\benchmark_data\100\h100c101.csv"
read_data = Read_data()
request_list = read_data.read_request(r"data\benchmark_data\100\h100c101.csv")
alpha = 0.5
duration = 10
start_train = 0
end_train = 100
end_test = 1000


