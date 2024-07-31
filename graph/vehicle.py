
class Truck:
    def __init__(self, id, capacity, velocity = 35):
        self.id = id
        self.capacity = capacity
        self.velocity = velocity
        self.position = {}
        self.remain_capacity = {}
        for t in range(1000):
            self.remain_capacity[t] = self.capacity
            print("self.remain_capaciy[t]: ", self.remain_capacity[t])
    
class Drone:
    def __init__(self, id, capacity, battery = 30, time_launch = 1, time_receive = 1, velocity = 50):
        self.id = id
        self.capacity = capacity
        self.battery = battery
        self.time_launch = time_launch
        self.time_receive = time_receive
        self.velocity = velocity