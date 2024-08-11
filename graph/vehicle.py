
class Truck:
    def __init__(self, id, capacity, velocity = 35):
        self.id = id
        self.capacity = capacity
        self.velocity = velocity
        self.used_capacity = None
    def update_used_capacity(self, request):
        self.used_capacity += request.customer_demand
    
class Drone:
    def __init__(self, id, capacity, battery = 30, time_launch = 1, time_receive = 1, velocity = 50):
        self.id = id
        self.capacity = capacity
        self.battery = battery
        self.time_launch = time_launch
        self.time_receive = time_receive
        self.velocity = velocity
        self.remain_capacity = {}
        self.remain_battery = {}