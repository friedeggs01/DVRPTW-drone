class Request:
    def __init__(self, customer_id, x, y, customer_demand, arrival_time, service_time, tw_start=None, tw_end=None, earliness=None, lateness=None, drone_serve = False):
        self.x = x
        self.y = y
        self.customer_id = customer_id
        self.customer_demand = customer_demand
        self.arrival = arrival_time
        self.service_time = service_time
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.earliness = earliness
        self.lateness = lateness
        self.drone_serve = drone_serve # True if drone can serve this customer, else False
        self.serving_start = None
        self.serving_end = None