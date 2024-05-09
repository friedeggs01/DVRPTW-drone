import numpy as np

from graph.requests import Request

class Decision: # quyết định xem request có được chấp nhận hay không
    def __init__(self, r: Request, T):
        self.r = r
        self.T = T # time slot that is happening

class Chosing: # chọn xem request được chấp nhận sẽ gán cho xe nào
    def __init__(self, r, T, truck, drone):
        self.r = r
        self.T = T
        self.truck = truck
        self.drone = drone
        
class Routing: # định tuyến lại đường cho cặp phương tiện truck - drone
    def __init__(self, r, T, truck, drone):
        self.r = r
        self.T = T
        self.truck = truck
        self.drone = drone