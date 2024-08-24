from .baseline import Node

import numpy as np

###################### CHOOSING TREE #####################

# Static terminal
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
        print("ATR: ", X.r.arrival)
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
        print("SDR: ", X.r.tw_start)
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
        print("TWE: ", X.r.tw_end)
        return X.r.tw_end
    
# distance to the customer being considered
class DCC(Node):
    def __init__(self):
         super(DCC,self).__init__()
    def __repr__(self):
        return "DCC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DCC"
    def getSymbol(self):
        return "DCC"
    def GetOutput(self, X):
        print("DCC: ", X.r.tw_end)
        return X.r.tw_end
    
# customer can ready to served
class CRS(Node):
    def __init__(self):
         super(CRS,self).__init__()
    def __repr__(self):
        return "CRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CRS"
    def getSymbol(self):
        return "CRS"
    def GetOutput(self, X):
        print("CRS: ", X.r.earliness)
        return X.r.earliness

# the amount of time till customer due date
class CDS(Node):
    def __init__(self):
         super(CDS,self).__init__()
    def __repr__(self):
        return "CDS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CDS"
    def getSymbol(self):
        return "CDS"
    def GetOutput(self, X):
        print("CDS: ", X.r.lateness)
        return X.r.lateness

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
        print("TTC: ", X.truck.capacity)
        return X.truck.capacity

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
        print("DTC: ", X.drone.capacity)
        return X.drone.capacity

# drone total battery
class DTB(Node):
    def __init__(self):
         super(DTB,self).__init__()
    def __repr__(self):
        return "DTB"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DTB"
    def getSymbol(self):
        return "DTB"
    def GetOutput(self, X):
        print("DTB: ", X.drone.battery)
        return X.drone.battery
    
# Dynamic terminal
# waiting time of request
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
        print("WTR: ")
        return X.T - X.r.arrival

# due date of request 
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
    
#  truck remain capacity
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
        return X.truck.capacity - X.truck.used_capacity
    
# drone remain capacity at T
# class DRC(Node):
#     def __init__(self):
#          super(DRC,self).__init__()
#     def __repr__(self):
#         return "DRC"
#     def _GetHumanExpressionSpecificNode(self, args):
#         return "DRC"
#     def getSymbol(self):
#         return "DRC"
#     def GetOutput(self, X):
#         return X.drone.remain_capacity[X.T]
    
# drone remain battery at T
# class DRB(Node):
#     def __init__(self):
#          super(DRB,self).__init__()
#     def __repr__(self):
#         return "DRB"
#     def _GetHumanExpressionSpecificNode(self, args):
#         return "DRB"
#     def getSymbol(self):
#         return "DRB"
#     def GetOutput(self, X):
#         return X.drone.remain_capacity[X.T]
    
    
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