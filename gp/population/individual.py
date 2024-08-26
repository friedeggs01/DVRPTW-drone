import numpy as np
class Individual:
    def __init__(self, decision_tree, ordering_tree, choosing_tree):
        self.decision_tree = decision_tree
        self.ordering_tree = ordering_tree
        self.choosing_tree = choosing_tree
        self.objectives = [0, 0]

    def cal_fitness_indi(self, alpha, carbon_upper, reject_upper):
        self.fitness = self.objectives[0]/carbon_upper*alpha + self.objectives[1]/reject_upper*(1-alpha)


