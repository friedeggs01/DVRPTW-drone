from run import run_proposed
import csv
import numpy as np
if __name__ == '__main__':
    path_nsf = [r'./data_1_9/nsf_centers_easy_s3.json',r'./data_1_9/nsf_centers_hard_s3.json', r'./data_1_9/nsf_centers_normal_s3.json',
                r'./data_1_9/nsf_rural_easy_s3.json', r'./data_1_9/nsf_rural_hard_s3.json', r'./data_1_9/nsf_rural_normal_s3.json', 
                r'./data_1_9/nsf_uniform_easy_s3.json', r'./data_1_9/nsf_uniform_hard_s3.json', r'./data_1_9/nsf_uniform_normal_s3.json',
                r'./data_1_9/nsf_urban_easy_s3.json',r'./data_1_9/nsf_urban_hard_s3.json', r'./data_1_9/nsf_urban_normal_s3.json']
    processing_num = 10
    num_train = 10
    pop_size =5
    min_height = 2 
    max_height = 8 
    initialization_max_height = 4
    evaluation = 100
    max_gen = 50
    crossover_rate = 0.8
    mutation_rate = 0.15
    alpha_list = np.arange(0, 1.01, 0.02)
    for path in path_nsf:
        print(path)
        for alpha in alpha_list:
            fitness, rejected, cost, proc, sum_gen, fitness_train, time_train, fitness_history = run_proposed(path, processing_num, alpha, num_train, pop_size, min_height, max_height, 
                                                                                                            initialization_max_height, evaluation, max_gen, crossover_rate, mutation_rate)
            print("GP", fitness, rejected, cost)
            
            pathname = "./Result_MOO/" + path[11:-5] + ".csv"
            with open(pathname, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["dataset","alpha", "fitness", "rejected", "cost", "fitness_train", "time_train"])
                writer.writerow([path[11:-5], alpha, fitness, rejected, cost, fitness_train, time_train])