import numpy as np
from copy import deepcopy
from .function_operator import *
from gp.population.individual import Individual

def __crossover_branch_individual_swap(individual: Individual, donor: Individual, min_height, max_height, 
                                       decision_tree, ordering_tree, choosing_tree):
    o1 = deepcopy(decision_tree)
    if o1 is None:
    # decision tree crossover
        o1 = crossover_tree_branch_swap(individual.decision_tree, donor.decision_tree, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.decision_tree)

    # ordering tree crossover
    o2 = deepcopy(ordering_tree)
    if o2 is None:
        o2 = crossover_tree_branch_swap(individual.ordering_tree, donor.ordering_tree, max_height)
        height2 = o2.GetHeight()
        if min_height > height2 or height2 > max_height:
            o2 = deepcopy(individual.ordering_tree)

    # choosing tree crossover
    o3 = deepcopy(choosing_tree)
    if o3 is None:
        o3 = crossover_tree_branch_swap(individual.choosing_tree, donor.choosing_tree, max_height)
        height3 = o3.GetHeight()
        if min_height > height3 or height3 > max_height:
            o3 = deepcopy(individual.choosing_tree)
    # both trees crossover
    return Individual(o1, o2, o3)

def crossover_branch_individual_swap(individual1, individual2, min_height, max_height, decision_tree, ordering_tree, choosing_tree):
    print("ordering tree: ", ordering_tree)
    child1 = __crossover_branch_individual_swap(individual1, individual2, min_height, max_height, decision_tree, ordering_tree, choosing_tree)
    child2 = __crossover_branch_individual_swap(individual2, individual1, min_height, max_height, decision_tree, ordering_tree, choosing_tree)
    return child1, child2

def crossover_sub_tree_swap(individual1, individual2, min_height, max_height, decision_tree, ordering_tree, choosing_tree):
    if np.random.rand() < 0.5:
        decision_tree_child1 = deepcopy(individual1.decision_tree)
        decision_tree_child2 = deepcopy(individual2.decision_tree)
    else:
        decision_tree_child1 = deepcopy(individual2.decision_tree)
        decision_tree_child2 = deepcopy(individual1.decision_tree)
    
    if np.random.rand() < 0.5:
        ordering_tree_child1 = deepcopy(individual1.ordering_tree)
        ordering_tree_child2 = deepcopy(individual2.ordering_tree)
    else:
        ordering_tree_child1 = deepcopy(individual2.ordering_tree)
        ordering_tree_child2 = deepcopy(individual1.ordering_tree)
    
    if np.random.rand() < 0.5:
        choosing_tree_child1 = deepcopy(individual1.choosing_tree)
        choosing_tree_child2 = deepcopy(individual2.choosing_tree)
    else:
        choosing_tree_child1 = deepcopy(individual2.choosing_tree)
        choosing_tree_child2 = deepcopy(individual1.choosing_tree)
    child1 = Individual(decision_tree_child1, ordering_tree_child1, choosing_tree_child1)
    child2 = Individual(decision_tree_child2, ordering_tree_child2, choosing_tree_child2)
    return child1, child2
