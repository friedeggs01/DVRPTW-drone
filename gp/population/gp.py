from copy import deepcopy
import numpy as np
from numpy.random import randint
import time

class Individual:
    def __init__(self, chromosomes, default_fitness=-float('inf')):
        self.fitness = default_fitness
        self.chromosomes = chromosomes
        self.reject = 0
        self.cost = np.inf

class Population:
    def __init__(self, pop_size,functions,terminals,min_height,max_height,initialization_max_tree_height, evaluation):
        self.history = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.terminals = terminals
        self.min_height = min_height
        self.max_height = max_height
        self.initialization_max_tree_height = initialization_max_tree_height
        self.indivs = []
        self.evaluation = evaluation