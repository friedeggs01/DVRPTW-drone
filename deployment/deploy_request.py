from gp.population.individual import *
from data.read_data import *
from priority_gp.decision_var import Decision, Choosing, Routing
from graph.network import Network
from utils.utils import *
from copy import deepcopy

def decision_gp(T):
    result = T
    return result

def choosing_gp(indi: Individual, request: Request, T, network, truck, drone):
    X = Choosing(request, T, truck, drone)
    result = indi.choosing_tree.GetOutput(X)
    return result

def ordering_gp(indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)
    result  = indi.ordering_tree.GetOutput(X)
    return result