from gp.population.individual import *
from data.read_data import *
from priority_gp.decision_var import Decision, Choosing, Ordering
from graph.network import Network
from utils.utils import *
from copy import deepcopy

# input là những cái mà terminal cần


def decision_gp(T):
    result = T
    return result

def choosing_gp(indi: Individual, request: Request, T, network, truck, drone):
    X = Choosing(request, T, truck, drone)
    result = indi.choosing_tree.GetOutput(X)
    return result

def ordering_gp(indi, request, T, network):
    # X = Ordering(request, T, truck, drone)
    # result = indi.choosing_tree.GetOutput(X)
    # return result
    return 1