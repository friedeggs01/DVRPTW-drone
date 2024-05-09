import numpy as np
class Individual:
    def __init__(self, decision_tree, choosing_tree, routing_tree):
        self.decision_tree = decision_tree
        self.choosing_tree = choosing_tree
        self.routing_tree = routing_tree
        self.objective = None


