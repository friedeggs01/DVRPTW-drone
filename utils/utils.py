from copy import deepcopy
import numpy as np

def get_request_run(request_list, reject, T):
    #print("get request run")
    request_processing = []
    request_reject = []
    for request in request_list:
        if request.arrival == T :
            if request.lifetime > T:
                request_processing.append(request)
            else:
                reject += 1
                request_reject.append(request)
    

            
    return request_processing, request_reject, reject