import numpy as np
from .function_operator import *
from gp.population.individual import Individual
from utils.utils import *

def mutation_individual_branch_replace(individual: Individual, functions, 
                                       terminal_decision, terminal_ordering, terminal_choosing, 
                                       min_height, max_height,
                                       decision_tree, ordering_tree, choosing_tree):
    o1 = deepcopy(decision_tree)
    if o1 is None:
    # decision tree mutation
        o1 = mutation_tree_branch_replace(individual.decision_tree, functions, terminal_decision,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.decision_tree)
    
    # ordering tree mutation
    o2 = deepcopy(ordering_tree)
    if o2 is None:
        o2 = mutation_tree_branch_replace(individual.ordering_tree, functions, terminal_ordering,
                        min_height, max_height)
        height2 = o2.GetHeight()
        if min_height > height2 or height2 > max_height:
            o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = deepcopy(choosing_tree)
    if o3 is None:
        o3 = mutation_tree_branch_replace(individual.choosing_tree, functions, terminal_choosing,
                        min_height, max_height)
        height3 = o3.GetHeight()
        if min_height > height3 or height3 > max_height:
            o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)

def mutation_individual_node_replace(individual: Individual, functions, 
                                    terminal_decision, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, decision_tree):
    o1 = deepcopy(decision_tree)
    if o1 is None:
        # decision tree mutation
        o1 = mutation_tree_node_replace(individual.decision_tree, functions, terminal_decision,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.decision_tree)
    # ordering tree mutation
    o2 = mutation_tree_node_replace(individual.ordering_tree, functions, terminal_ordering,
                    min_height, max_height)
    height2 = o2.GetHeight()
    if min_height > height2 or height2 > max_height:
        o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = mutation_tree_node_replace(individual.choosing_tree, functions, terminal_choosing,
                    min_height, max_height)
    height3 = o3.GetHeight()
    if min_height > height3 or height3 > max_height:
        o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)


def mutation_individual_branch_swap(individual: Individual, functions, 
                                    terminal_decision, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, decision_tree):
    o1 = deepcopy(decision_tree)
    if o1 is None:
    # decision tree mutation
        o1 = mutation_tree_branch_swap(individual.decision_tree, functions, terminal_decision,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.decision_tree)
    # ordering tree mutation
    o2 = mutation_tree_branch_swap(individual.ordering_tree, functions, terminal_ordering,
                    min_height, max_height)
    height2 = o2.GetHeight()
    if min_height > height2 or height2 > max_height:
        o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = mutation_tree_branch_swap(individual.choosing_tree, functions, terminal_choosing,
                    min_height, max_height)
    height3 = o3.GetHeight()
    if min_height > height3 or height3 > max_height:
        o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)


def mutation_value_decision(individual: Individual, functions,
                               terminal_decision, terminal_ordering, terminal_choosing,
                               min_height, max_height, decision_tree):
    decision_tree = deepcopy(individual.decision_tree)
    ordering_tree = deepcopy(individual.ordering_tree)
    choosing_tree = deepcopy(individual.choosing_tree)
    node = find_node(decision_tree, "Const")
    if node != None:
        node.mutate_value()

    node1 = find_node(ordering_tree, "Const")
    if node1 != None:
        node1.mutate_value()
    node2 = find_node(choosing_tree, "Const")
    if node2 != None:
        node2.mutate_value()
    
    return Individual(decision_tree, ordering_tree, choosing_tree)