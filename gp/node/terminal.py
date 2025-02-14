from .baseline import Node

import numpy as np

###################### ORDERING/DECISION TREE #####################
# Only for decision tree
# Maximum capacity of vehicle
class MVC(Node):
    def __init__(self):
         super(MVC,self).__init__()
    def __repr__(self):
        return "MVC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MVC"
    def getSymbol(self):
        return "MVC"
    def GetOutput(self, X):
        return X.max_cap


# Arrival time of request
class ATR(Node):
    def __init__(self):
         super(ATR,self).__init__()
    def __repr__(self):
        return "ATR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ATR"
    def getSymbol(self):
        return "ATR"
    def GetOutput(self, X):
        return X.r.arrival

# Start date of request
class SDR(Node):
    def __init__(self):
         super(SDR,self).__init__()
    def __repr__(self):
        return "SDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "SDR"
    def getSymbol(self):
        return "SDR"
    def GetOutput(self, X):
        return X.r.tw_start

# Time window end of request
class TWE(Node):
    def __init__(self):
         super(TWE,self).__init__()
    def __repr__(self):
        return "TWE"
    def _GetHumanExpressionSpecificNode(self, args):
        return "TWE"
    def getSymbol(self):
        return "TWE"
    def GetOutput(self, X):
        return X.r.tw_end

# Waiting time to ready of customer
class WTR(Node):
    def __init__(self):
         super(WTR,self).__init__()
    def __repr__(self):
        return "WTR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "WTR"
    def getSymbol(self):
        return "WTR"
    def GetOutput(self, X):
        if X.T >= X.r.tw_start:
            return 0
        return X.r.tw_start - X.T

# Due date of request
class DDR(Node):
    def __init__(self):
         super(DDR,self).__init__()
    def __repr__(self):
        return "DDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DDR"
    def getSymbol(self):
        return "DDR"
    def GetOutput(self, X):
        return X.r.tw_end - X.T
    
# Demand of request
class DEM(Node):
    def __init__(self):
         super(DEM,self).__init__()
    def __repr__(self):
        return "DEM"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DEM"
    def getSymbol(self):
        return "DEM"
    def GetOutput(self, X):
        return X.r.customer_demand

# Waiting time of request
class PN(Node):
    def __init__(self):
         super(PN,self).__init__()
    def __repr__(self):
        return "PN"
    def _GetHumanExpressionSpecificNode(self, args):
        return "PN"
    def getSymbol(self):
        return "PN"
    def GetOutput(self, X):
        return X.T - X.r.arrival

# Service time of request
class ST(Node):
    def __init__(self):
         super(ST,self).__init__()
    def __repr__(self):
        return "ST"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ST"
    def getSymbol(self):
        return "ST"
    def GetOutput(self, X):
        return X.r.service_time

# Minimum distance to go to customer
class MD(Node):
    def __init__(self):
         super(MD,self).__init__()
    def __repr__(self):
        return "MD"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MD"
    def getSymbol(self):
        return "MD"
    def GetOutput(self, X):
        return X.min_distance


############################ CHOOSING TREE ############################

# truck total capacity
class TTC(Node):
    def __init__(self):
         super(TTC,self).__init__()
    def __repr__(self):
        return "TTC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "TTC"
    def getSymbol(self):
        return "TTC"
    def GetOutput(self, X):
        # print("TTC: ", X.truck.capacity)
        return X.network.truck_capacity

# drone total capacity
class DTC(Node):
    def __init__(self):
         super(DTC,self).__init__()
    def __repr__(self):
        return "DTC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DTC"
    def getSymbol(self):
        return "DTC"
    def GetOutput(self, X):
        # print("DTC: ", X.drone.capacity)
        return X.network.drone_capacity

# truck remain capacity
class TRC(Node):
    def __init__(self):
         super(TRC,self).__init__()
    def __repr__(self):
        return "TRC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "TRC"
    def getSymbol(self):
        return "TRC"
    def GetOutput(self, X):
        return X.remaining_capacity
    
# path length
class PL(Node):
    def __init__(self):
         super(PL,self).__init__()
    def __repr__(self):
        return "PL"
    def _GetHumanExpressionSpecificNode(self, args):
        return "PL"
    def getSymbol(self):
        return "PL"
    def GetOutput(self, X):
        return X.dis_sum
    
# number of customers
class NC(Node):
    def __init__(self):
         super(NC,self).__init__()
    def __repr__(self):
        return "NC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "NC"
    def getSymbol(self):
        return "NC"
    def GetOutput(self, X):
        return X.numberCustomer 
    
# minimum distance of vehicle to go to customer
class MDV(Node):
    def __init__(self):
         super(MDV,self).__init__()
    def __repr__(self):
        return "MDV"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MDV"
    def getSymbol(self):
        return "MDV"
    def GetOutput(self, X):
        return X.min_distance

    
    
 ##############################################################   
class Rand(Node):
    def __init__(self):
        super(Rand, self).__init__()
    def __repr__(self):
        return "Rand"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Rand"
    def getSymbol(self):
        return "Rand"
    def GetOutput(self, X):
        return np.random.rand()
    
class ZeroNode(Node):
    def __init__(self):
        super(ZeroNode, self).__init__()
    def __repr__(self):
        return "ZeroNode"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ZeroNode"
    def getSymbol(self):
        return "ZeroNode"
    def GetOutput(self, X):
        return 0
    
class OneNode(Node):
    def __init__(self):
        super(OneNode, self).__init__()
    def __repr__(self):
        return "OneNode"
    def _GetHumanExpressionSpecificNode(self, args):
        return "OneNode"
    def getSymbol(self):
        return "OneNode"
    def GetOutput(self, X):
        return 1
      
class Const(Node):
    def __init__(self):
        super(Const, self).__init__()
        self.value = np.random.uniform(0, 1)
    def __repr__(self):
        return "Const"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Const"
    def getSymbol(self):
        return "Const"
    def GetOutput(self, X):
        return self.value
    def GetSurrogateOutput(self, X):
        return self.value 

    def mutate_value(self):
        self.value = self.value + np.random.normal(0, 0.1)           

####################################################################

