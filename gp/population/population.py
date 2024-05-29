from copy import deepcopy
class Population:
    def __init__(self, pop_size, 
                 functions, decision_terminals, choosing_terminals, 
                 min_depth=2, max_depth=8, initialization_max_tree_depth=8, 
                 num_of_tour_particips=2, tournament_prob=0.8, crossover_rate=0.9, mutation_rate=0.1):
        self.history = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.decision_terminals = decision_terminals
        self.choosing_terminals = choosing_terminals
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.initialization_max_tree_depth = initialization_max_tree_depth
        self.indivs = []
        self.num_of_tour_ptiarcips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
    def pre_indi_gen(self, indi_list):
        if len(indi_list) != self.pop_size:
            raise ValueError("The length of the list of individuals is not equal to the population size")
        self.indivs = deepcopy(indi_list)
        
    def random_init(self):
        curr_max_depth = self.min_height
        init_depth_interval = self.pop_size / (self.initialization_max_tree_height - self.min_height + 1)
        next_depth_interval = init_depth_interval
        i = 0
        pc_check = set()
        while i < self.pop_size:
            if i >= next_depth_interval:
                next_depth_interval += init_depth_interval
                curr_max_depth += 1
            inv = individual_init(self.min_height, curr_max_depth, self.determining_tree, self.functions,
                                  self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
            pc_indi = self.situation_surrogate.cal_pc(inv)
            pc_indi_tuple = tuple(pc_indi)
            if pc_indi_tuple not in pc_check:
                pc_check.add(pc_indi_tuple)
                inv.pc = pc_indi
                self.indivs.append(inv)
                i += 1
            else:
                continue