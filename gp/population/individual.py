import numpy as np
class Individual:
    def __init__(self, decision_tree, ordering_tree, choosing_tree):
        self.decision_tree = decision_tree
        self.ordering_tree = ordering_tree
        self.choosing_tree = choosing_tree
        self.objectives = None
        


