class Request:
    def __init__(self, customer_id, customer_demand, arrival_time, tw_start=None, tw_end=None, earliness=None, lateness=None, drone_serve = False):
        self.customer_id = customer_id
        self.customer_demand = customer_demand
        self.arrival = arrival_time
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.earliness = earliness
        self.lateness = lateness
        self.drone_serve = drone_serve # True if drone can serve this customer, else False
        