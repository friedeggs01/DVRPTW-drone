from gp.population.individual import *
from data.read_data import *
from priority_gp.decision_var import Decision, Choosing, Ordering
from graph.network import Network
from utils.utils import *
from copy import deepcopy


def decision_gp(indi: Individual, request, T, network):
    X = Decision(request, T, network)
    result = indi.decision_tree.GetOutput(X)
    return result

def choosing_gp(indi: Individual, request: Request, T, network, vehicle_id):
    X = Choosing(request, vehicle_id, T, network)
    result = indi.choosing_tree.GetOutput(X)
    return result

def ordering_gp(indi, request, T, network):
    X = Ordering(request, T, network)
    result = indi.ordering_tree.GetOutput(X)
    return result