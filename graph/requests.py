class Request:
    def __init__(self, request_id, x, y, customer_demand, arrival_time, service_time, tw_start, 
                 tw_end,drone_serve, earliness=None, lateness=None):
        self.x = x
        self.y = y
        self.customer_demand = customer_demand
        self.arrival = arrival_time
        self.service_time = service_time
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.earliness = tw_start - 30
        self.lateness = tw_end + 30
        self.drone_serve = drone_serve # True if drone can serve this customer, else False
        self.serving_start = None
        self.serving_end = None
        self.request_id = request_id