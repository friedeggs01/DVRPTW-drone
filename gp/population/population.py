from copy import deepcopy
class Population:
    def __init__(self, pop_size, 
                 functions, decision_terminals, ordering_terminals, choosing_terminals, 
                 min_height=2, max_height=8, initialization_max_tree_height=8, 
                 num_of_tour_particips=2, tournament_prob=0.8, crossover_rate=0.9, mutation_rate=0.1):
        self.history = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.decision_terminals = decision_terminals
        self.ordering_terminals = ordering_terminals
        self.choosing_terminals = choosing_terminals
        self.min_height = min_height
        self.max_height = max_height
        self.initialization_max_tree_height = initialization_max_tree_height
        self.indivs = []
        self.num_of_tour_ptiarcips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
    def pre_indi_gen(self, indi_list):
        if len(indi_list) != self.pop_size:
            raise ValueError("The length of the list of individuals is not equal to the population size")
        self.indivs = deepcopy(indi_list)
        
    # def random_init(self):
    #     curr_max_height = self.min_height
    #     init_height_interval = self.pop_size / (self.initialization_max_tree_height - self.min_height + 1)
    #     next_height_interval = init_height_interval
    #     i = 0
    #     pc_check = set()
    #     while i < self.pop_size:
    #         if i >= next_height_interval:
    #             next_height_interval += init_height_interval
    #             curr_max_height += 1
    #         inv = individual_init(self.min_height, curr_max_height, self.determining_tree, self.functions,
    #                               self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
    #         pc_indi = self.situation_surrogate.cal_pc(inv)
    #         pc_indi_tuple = tuple(pc_indi)
    #         if pc_indi_tuple not in pc_check:
    #             pc_check.add(pc_indi_tuple)
    #             inv.pc = pc_indi
    #             self.indivs.append(inv)
    #             i += 1
    #         else:
    #             continue