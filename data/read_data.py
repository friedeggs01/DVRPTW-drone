from graph.requests import Request
import pandas as pd

class Read_data:  
    def read_request(self, PATH):
        data_frame = pd.read_csv(PATH)
        request_list = []
        for iter, row in data_frame.iterrows():
            request = Request(iter + 1, row['x'], row['y'], row['demand'], row['time'], row['servicetime'],\
                              row['open'], row['close'], row['drone_serve'])
            request_list.append(request)
        return request_list