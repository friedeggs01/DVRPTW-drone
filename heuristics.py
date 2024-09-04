from gp.node.function import *
from gp.node.terminal import *
from deployment.evaluation import calFitness_three_policies
from gp.population.individual import *
from data.read_data import *
from graph.network import Network
from utils.utils import *
import os




# Function to collect file paths
def collect_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            formatted_path = os.path.join(folder_path, relative_path)
            file_paths.append(formatted_path)
    return file_paths
### Tạo Heuristic
# Heu1: decision: all (OneNode()), ordering: đến trước phục vụ trước (ZeroNode - ATR), choosing: xe ở gần nhất (ZeroNode - MDV)

decision_heu1 =OneNode()
ordering_heu1 = SubNode()
ordering_heu1.AppendChild(ZeroNode())
ordering_heu1.AppendChild(ATR())
choosing_heu1 = SubNode()
choosing_heu1.AppendChild(ZeroNode())
choosing_heu1.AppendChild(MDV())
indi_heu1 = Individual(decision_heu1, ordering_heu1, choosing_heu1)

# Heu2: decision: all (OneNode()), ordering: đến trước phục vụ trước (ZeroNode - ATR), choosing: xe còn nhiều capacity nhất (TRC)
decision_heu2 = OneNode()
ordering_heu2 = SubNode()
ordering_heu2.AppendChild(ZeroNode())
ordering_heu2.AppendChild(ATR())
choosing_heu2 = TRC()
indi_heu2 = Individual(decision_heu2, ordering_heu2, choosing_heu2)

# Heu3: decision: all (OneNode()), ordering: còn lại ít thời gian nhất phục vụ trước (ZeroNode - DDR), choosing: xe ở gần nhất (ZeroNode - MDV)
decision_heu3 = OneNode()
ordering_heu3 = SubNode()
ordering_heu3.AppendChild(ZeroNode())
ordering_heu3.AppendChild(DDR())
choosing_heu3 = SubNode()
choosing_heu3.AppendChild(ZeroNode())
choosing_heu3.AppendChild(MDV())
indi_heu3 = Individual(decision_heu3, ordering_heu3, choosing_heu3)

# Heu4: decision: all (OneNode()), ordering: còn lại ít thời gian nhất phục vụ trước (ZeroNode - DDR), choosing: xe còn nhiều capacity nhất (TRC)
decision_heu4 = OneNode()
ordering_heu4 = SubNode()
ordering_heu4.AppendChild(ZeroNode())
ordering_heu4.AppendChild(DDR())
choosing_heu4 = TRC()
indi_heu4 = Individual(decision_heu4, ordering_heu4, choosing_heu4)

# Heu5: decision: all (OneNode()), ordering: thời gian chờ ít nhất phục vụ trước (ZeroNode - WTR), choosing: xe ở gần nhất (ZeroNode - MDV)
decision_heu5 = OneNode()
ordering_heu5 = SubNode()
ordering_heu5.AppendChild(ZeroNode())
ordering_heu5.AppendChild(WTR())
choosing_heu5 = SubNode()
choosing_heu5.AppendChild(ZeroNode())
choosing_heu5.AppendChild(MDV())
indi_heu5 = Individual(decision_heu5, ordering_heu5, choosing_heu5)

# Heu6: decision: all (OneNode()), ordering: thời gian chờ ít nhất phục vụ trước (ZeroNode - WTR), choosing: xe còn nhiều capacity nhất (TRC)
decision_heu6 = OneNode()
ordering_heu6 = SubNode()
ordering_heu6.AppendChild(ZeroNode())
ordering_heu6.AppendChild(WTR())
choosing_heu6 = TRC()
indi_heu6 = Individual(decision_heu6, ordering_heu6, choosing_heu6)


num_vehicle_list = [3, 5, 10]
truck_capacity = 1300
drone_capacity = 10
drone_endurance = 30
duration = 10
start_train = 0
end_train = 1000
end_test = 1000

folder_path = "data/100"
file_paths = collect_file_paths(folder_path)

# Filter out unwanted files
list_file_path = [path for path in file_paths if path not in [
    'data/dvrptw-setting.txt',
    'data/read_data.py',
    'data/__pycache__/read_data.cpython-311.pyc'
]]

data_store = "Heuristic_result.csv"
if os.path.exists(data_store):
    os.remove(data_store)
with open(data_store, 'w') as f:
    f.write("data_path, num_vehicle, carbon_heu1, reject_heu1, carbon_heu2, reject_heu2, carbon_heu3, reject_heu3, carbon_heu4, reject_heu4, carbon_heu5, reject_heu5, carbon_heu6, reject_heu6\n")

for data_path in list_file_path:
    print("data_path: ", data_path)
    for num_vehicle in num_vehicle_list:
        reader = Read_data()
        request_list = reader.read_request(data_path)      
        network = Network(request_list, num_vehicle, truck_capacity, drone_capacity, drone_endurance)

        sum_max_dis = 0
        for i in range (len(request_list)):
            max_each_request = 0
            for j in range(len(request_list)):
                if i != j:
                    max_each_request = max(max_each_request, cal_distance(request_list[i], request_list[j]))
            sum_max_dis += max_each_request
        depo_max = 0
        for i in range(len(request_list)):
            depo_max = max(depo_max, cal_distance(None, request_list[i]))
        sum_max_dis  = sum_max_dis + 2*depo_max*network.num_vehicle
        carbon_upper = sum_max_dis*network.WAER
        reject_upper = len(request_list)

        obj1_heu1, obj2_heu1 = calFitness_three_policies(indi_heu1, network, request_list, duration, start_train, end_train)
        obj1_heu2, obj2_heu2 = calFitness_three_policies(indi_heu2, network, request_list, duration, start_train, end_train)
        obj1_heu3, obj2_heu3 = calFitness_three_policies(indi_heu3, network, request_list, duration, start_train, end_train)
        obj1_heu4, obj2_heu4 = calFitness_three_policies(indi_heu4, network, request_list, duration, start_train, end_train)
        obj1_heu5, obj2_heu5 = calFitness_three_policies(indi_heu5, network, request_list, duration, start_train, end_train)
        obj1_heu6, obj2_heu6 = calFitness_three_policies(indi_heu6, network, request_list, duration, start_train, end_train)

        with open(data_store, 'a') as f:
            f.write("{},{},{},{}, {},{}, {},{}, {},{}, {},{}, {},{}\n".format(data_path[-12:], num_vehicle, obj1_heu1, obj2_heu1, obj1_heu2, obj2_heu2, obj1_heu3, obj2_heu3, obj1_heu4, obj2_heu4, obj1_heu5, obj2_heu5, obj1_heu6, obj2_heu6))
