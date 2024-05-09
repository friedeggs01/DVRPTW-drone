import numpy as np
import random
from numpy.random import randint
from copy import deepcopy
from gp.population.individual import Individual

def GenerateRandomTree(functions, terminals, max_depth, curr_depth=0, method='grow', min_depth=2):
    if curr_depth == max_depth:
        idx = randint(len(terminals))
        n = deepcopy( terminals[idx] )
    else:
        if method == 'grow' and curr_depth	>= min_depth:
            term_n_funs = terminals + functions
            idx = randint( len(term_n_funs) )
            n = deepcopy( term_n_funs[idx] )
        elif method == 'full' or (method == 'grow' and curr_depth < min_depth):
            idx = randint(len(functions))
            n = deepcopy( functions[idx] )
        else:
            raise ValueError('Unrecognized tree generation method')

        for i in range(n.arity):
            c = GenerateRandomTree(functions, terminals, max_depth, curr_depth=curr_depth + 1, 
                                        method=method, min_depth=min_depth )
            n.AppendChild( c ) # do not use n.children.append because that won't set the n as parent node of c
    return n

# Random individual initialization
def invidiual_init(min_depth, curr_max_depth, decision_tree,
                   functions, decision_terminals, choosing_terminals):
    if decision_tree is None:
        decision_tree = GenerateRandomTree(functions, decision_terminals, curr_max_depth,
                                           curr_height=0,
                                           method = 'grow' if np.random.random() < 0.5 else 'full',
                                           min_depth=min_depth)
    decision_tree = deepcopy(decision_tree)
    choosing_tree = GenerateRandomTree(functions, choosing_terminals, curr_max_depth,
                                       curr_depth=0,  method='grow' if np.random.random() < 0.5 else 'full',
                                       min_depth=min_depth) 
    inv = Individual(decision_tree, choosing_tree)
    return inv

# Random population initialization
def  population_init(popsize, individuals, functions, terminals, max_depth):
    indi_list = []
    curr_max_depth = min_depth
    init_depth_interval = popsize / ()
    return indi_list