class Problem:
    def __init__(self, mode='file', file_path=None):
        self.N = 0  # Number of locations
        self.weight = []  # Adjacency matrix (distances between locations)
        self.trailer = []  # Location and time to attach the trailer
        self.truck = []  # List of trucks and their starting locations
        self.requests = []  # List of transportation requests
        
        if mode == 'file' and file_path:
            self.read_input_from_file(file_path)
        elif mode == 'manual':
            self.read_input_from_compiler()
        else:
            raise ValueError("Invalid mode or missing file_path.")

    def read_input_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        self.process_input_lines(lines)

    def read_input_from_compiler(self):
        lines = []
        # Read number of locations
        lines.append(input())
        
        # Read distances
        lines.append(input())
        for _ in range(int(lines[0].split()[-1]) ** 2):
            lines.append(input())
        
        # Read trailer information
        lines.append(input())
        
        # Read truck information
        lines.append(input())
        num_trucks = int(lines[-1].split()[-1])
        for _ in range(num_trucks):
            lines.append(input())
        
        # Read transportation requests
        while True:
            line = input()
            if line.strip() == "#":
                break
            lines.append(line)
        lines.append('#')

        self.process_input_lines(lines)

    def process_input_lines(self, lines):
        # Read number of locations
        self.N = int(lines[0].split()[-1])
        
        # Initialize the weight (adjacency) matrix with zeros
        self.weight = [[0] * (self.N+1) for _ in range(self.N+1)] #truy cap khong can -1
        
        # Read distance information
        i = 2  # Starting line for distances
        for _ in range(self.N * self.N):
            from_node, to_node, distance = map(int, lines[i].split())
            self.weight[from_node][to_node] = distance
            i += 1
        
        # Read trailer information
        trailer_info = lines[i].split()
        self.trailer.append(int(trailer_info[1])) #[0] is locatiom
        self.trailer.append(int(trailer_info[2])) #[1] is duration
        i += 1
        
        # Read truck information
        num_trucks = int(lines[i].split()[-1])
        i += 1
        self.truck = [0 for _ in range(num_trucks+1)] #truy cap khong can -1
        for _ in range(num_trucks):
            truck_id, start_location = map(int, lines[i].split())
            self.truck[truck_id] = start_location
            i += 1
        
        # Read transportation requests
        while lines[i].strip() != '#':
            request_info = lines[i].split()
            temp = [0,0]

            if request_info[4] == 'PICKUP_CONTAINER':
                temp[0] = 1
            
            if request_info[7] == 'DROP_CONTAINER_TRAILER':
                temp[1] = 1

            if request_info[4] == 'PICKUP_CONTAINER_TRAILER' and request_info[7] == 'DROP_CONTAINER':
                type = 0
            elif request_info[4] == 'PICKUP_CONTAINER_TRAILER' and request_info[7] == 'DROP_CONTAINER_TRAILER':
                type = 1
            elif request_info[4] == 'PICKUP_CONTAINER' and request_info[7] == 'DROP_CONTAINER':
                type = 2
            else:
                type = 3
                
            

            request = {
                'id': int(request_info[1]), #id
                'size': int(request_info[2]), #type of container, 20 or 40

                'pick_l': int(request_info[3]), #pickup location
                'pick_a': temp[0], #0 if need trailer, 1 if not need
                'pick_d': int(request_info[5]), #service pickup time

                'drop_l': int(request_info[6]), #drop location
                'drop_a': temp[1], #0 if no need to return trailer, 1 if need to return trailer
                'drop_d': int(request_info[8]), #service drop time

                'type': type

                #Example: REQ 2 40 5 PICKUP_CONTAINER_TRAILER 300 7 DROP_CONTAINER 600
            }
            self.requests.append(request)
            i += 1

import random
from copy import deepcopy

alpha = 5

class GeneticAlgorithm:
    def __init__(self, problem, population_size=35, generations=25):
        self.problem = problem
        self.distances = self.problem.weight
        self.population_size = population_size
        self.generations = generations
        self.population = self.initialize_population()

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            # Generate a random solution
            solution = self.generate_random_solution()
            population.append(solution)
        return population

    def generate_random_solution(self):
        # Initialize the solution with shuffled requests
        solution = [x + 1 for x in range(len(self.problem.requests))]
        random.shuffle(solution)

        # Determine the number of zeros to insert
        num_zeros = len(self.problem.truck) - 2
        if num_zeros <= 0:
            # print("Solution without zeros:", solution)
            return solution

        for _ in range(num_zeros):
            available_positions = []

            # Iterate through possible insertion points
            for i in range(1, len(solution)):
                # Check if inserting at position 'i' won't place a '0' next to another '0'
                if solution[i - 1] != 0 and (i < len(solution) and solution[i] != 0):
                    available_positions.append(i)

            if not available_positions:
                raise ValueError("No available positions to insert 0 without violating constraints.")

            # Randomly select a valid position to insert '0'
            pos = random.choice(available_positions)
            solution.insert(pos, 0)
            # print(f"Inserted 0 at position {pos}: {solution}")

        # print("Final solution:", solution)
        return solution
    
    def remove_consecutive_zeros(self, lst):
        # Initialize an empty result list
        result = [0]
        
        # Iterate through the original list
        for i in range(len(lst)):
            # Add the current element to the result if it's not a zero or if the previous element is not a zero
            if lst[i] != 0 or (i > 0 and lst[i - 1] != 0):
                result.append(lst[i])
        
        return result

    def fitness(self, solution):
        decode = self.add_trailer(solution)

        latest = 0
        total = 0
        travel_time = 0
        c = 1

        location = self.problem.truck[c]
        depot = self.problem.truck[c]
        trailer = self.problem.truck[0]
        trailer_time = self.problem.truck[1]

        latest_max = 0

        decode = self.remove_consecutive_zeros(decode)

        # print("HERE DECODE: ", decode)

        for i in range(1, len(decode)-1):
            prev = decode[i-1]
            request = decode[i]

            if request == 0:
                travel_time += self.distances[location][depot]
                total += travel_time
                latest_max = max(latest_max, latest)

                c= c+1
                location = self.problem.truck[c]
                depot = self.problem.truck[c]
            
            elif request == -1:
                travel_time += self.distances[location][trailer]
                latest += self.distances[location][trailer] + trailer_time
                location = trailer 

            else:
                r = self.problem.requests[request-1]
                pickup = r["pick_l"]
                drop = r["drop_l"]

                travel_time += self.distances[location][pickup]
                latest += self.distances[location][pickup] 
                latest += r["pick_d"]

                travel_time += self.distances[pickup][drop]
                latest += self.distances[pickup][drop] 
                latest += + r["drop_d"]

                location = drop

            travel_time += self.distances[location][depot]
            total += travel_time
            latest_max = max(latest_max, latest)

        
        F1 = latest_max
        F2 = total

        fitness_value = F1 * alpha + F2  # Example weight: prioritize F1, but include F2

        return fitness_value

    def add_trailer(self, solution):
        truck_routes = []  # Start with one truck's route (extend for multiple trucks if needed)
        has_trailer = False  # Track if a truck has the trailer

        truck_routes.append(0)

        for i in range(len(solution)):
            if solution[i] == 0:
                if has_trailer:
                    truck_routes.append(-1) #go drop trailer
                truck_routes.append(0) #go to depot
                has_trailer = False
                continue
            request = self.problem.requests[solution[i]-1]
            # pickup_point = request["pick_l"]
            # drop_point = request["drop_l"]
            req_type = request["type"]  # Request type: 0, 1, 2, or 3

            # next_request = self.problem.requests[solution[i]]
            # next_req_type = next_request["type"]

            if req_type == 0:  # Already has trailer, keep trailer
                if has_trailer:
                    truck_routes.append(-1) #go drop trailer
            
                truck_routes.append(solution[i])
                has_trailer = True
                
                # truck_routes[0].append((pickup_point, "PICKUP_CONTAINER", req_id))
                # truck_routes[0].append((drop_point, "DROP_CONTAINER", req_id))
                # has_trailer = True
            elif req_type == 1:  # Has trailer, must leave it at the drop
                if has_trailer:
                    truck_routes.append(-1) #go drop trailer
                truck_routes.append(solution[i])
                has_trailer = False

                # truck_routes[0].append((pickup_point, "PICKUP_CONTAINER", req_id))
                # truck_routes[0].append((drop_point, "DROP_CONTAINER_LEAVE_TRAILER", req_id))
                # has_trailer = False
            elif req_type == 2:  # Must pick trailer from the trailer location, keep trailer
                if not has_trailer:
                    truck_routes.append(-1) #go pick trailer
                truck_routes.append(solution[i])
                has_trailer = True

                # if not has_trailer:
                #     truck_routes[0].append((self.problem.trailer['l'], "PICKUP_TRAILER"))
                #     has_trailer = True
                # truck_routes[0].append((pickup_point, "PICKUP_CONTAINER", req_id))
                # truck_routes[0].append((drop_point, "DROP_CONTAINER", req_id))
            elif req_type == 3:  # Must pick and leave the trailer
                if not has_trailer:
                    truck_routes.append(-1) #go pick trailer
                truck_routes.append(solution[i])
                has_trailer = False

                # if not has_trailer:
                #     truck_routes[0].append((self.problem.trailer['l'], "PICKUP_TRAILER"))
                #     has_trailer = True
                # truck_routes[0].append((pickup_point, "PICKUP_CONTAINER", req_id))
                # truck_routes[0].append((drop_point, "DROP_CONTAINER_LEAVE_TRAILER", req_id))
                # has_trailer = False

        # If truck has a trailer at the end, return it
        if has_trailer:
            truck_routes.append(-1)
            # truck_routes[0].append((self.problem.trailer['l'], "RETURN_TRAILER"))

        truck_routes.append(0)
        # truck_routes[0].append((0, "STOP"))  # Return to depot

        return truck_routes

    def print_solution(self, solution):
        print(solution)

    def print_final_solution(self):
        solution = self.add_trailer(self.best_solution)
        solution = self.remove_consecutive_zeros(solution)

        c = 0
        encode_request = [[]]
        encode = self.remove_consecutive_zeros(self.best_solution)
        for i in range(1, len(encode)):
            if encode[i] == 0:
                c+=1
                encode_request.append([])
            else:
                encode_request[c].append(encode[i])
        
        print(f"ROUTES {len(encode_request)}")
        for j, route in enumerate(encode_request):
            print(f"TRUCK {j+1}")
            has_trailer = False
            for r in route:
                request = self.problem.requests[r - 1]
                
                if request["pick_a"] == 0:
                    pickup_action = "PICKUP_CONTAINER_TRAILER"
                else: pickup_action = "PICKUP_CONTAINER"

                if request["drop_a"] == 0:
                    drop_action = "DROP_CONTAINER"
                else: drop_action = "DROP_CONTAINER_TRAILER"

                if request['type'] == 0:
                    if has_trailer:
                        print(f"{self.problem.trailer[0]} DROP_TRAILER")
                    print(f'{request["pick_l"]} {pickup_action} {request["id"]}')
                    print(f'{request["drop_l"]} {drop_action} {request["id"]}')
                    has_trailer = True

                if request['type'] == 1:
                    if has_trailer:
                        print(f"{self.problem.trailer[0]} DROP_TRAILER")
                    print(f'{request["pick_l"]} {pickup_action} {request["id"]}')
                    print(f'{request["drop_l"]} {drop_action} {request["id"]}')
                    has_trailer = False

                if request['type'] == 2:
                    if not has_trailer:
                        print(f"{self.problem.trailer[0]} PICKUP_TRAILER")
                    print(f'{request["pick_l"]} {pickup_action} {request["id"]}')
                    print(f'{request["drop_l"]} {drop_action} {request["id"]}')
                    has_trailer = True

                if request['type'] == 3:
                    if not has_trailer:
                        print(f"{self.problem.trailer[0]} PICKUP_TRAILER")
                    print(f'{request["pick_l"]} {pickup_action} {request["id"]}')
                    print(f'{request["drop_l"]} {drop_action} {request["id"]}')
                    has_trailer = False
                    
            if has_trailer:
                print(f"{self.problem.trailer[0]} DROP_TRAILER")


            print(f"{self.problem.truck[j+1]} STOP")

            print("#")

    def pmx_crossover(self, parent1, parent2):
        # Partially Mapped Crossover (PMX)
        size = len(parent1)
        
        # Choose two crossover points randomly
        cx_point1 = random.randint(1, size - 3)  # Avoid positions too close to edges
        cx_point2 = random.randint(cx_point1 + 1, size - 2)  # Ensure cx_point2 > cx_point1
        
        def pmx_single(p1, p2):
            child = [-1] * size  # Initialize child with -1 (temporary placeholder)
            
            # Copy the segment between crossover points from the first parent
            child[cx_point1:cx_point2] = p1[cx_point1:cx_point2]
            
            # Mapping process to ensure no duplicate values
            for i in range(cx_point1, cx_point2):
                if p2[i] not in child:
                    val = p2[i]
                    idx = i
                    # Resolve conflicts using the mapping from parent1 to parent2
                    while child[idx] != -1:
                        idx = p1.index(p2[idx])
                    child[idx] = val
            
            # Fill in the remaining spots with non-conflicting elements from p2
            for i in range(size):
                if child[i] == -1:
                    child[i] = p2[i]
            
            return child
        
        child1 = pmx_single(parent1, parent2)
        child2 = pmx_single(parent2, parent1)
        
        return child1, child2

    def mutate(self, solution, mutation_rate=0.1):
        # Swap two random requests with a given mutation probability
        if random.random() < mutation_rate:
            i, j = random.sample(range(1, len(solution) - 1), 2)
            solution[i], solution[j] = solution[j], solution[i]
        return solution

    def tournament_selection(self, population):
        # Tournament selection: select two parents from the population
        tournament_size = 3
        parents = random.sample(population, tournament_size)
        parents.sort(key=lambda sol: self.fitness(sol))
        return parents[0], parents[1]
    
    def elitism_selection(self, population):
        # Elitism selection: select two parents from the top-performing individuals
        population.sort(key=lambda sol: self.fitness(sol))
        return population[0], population[1]  # Select the two best individuals

    def local_search(self, solution):
        # Swap two random requests with a given mutation probability:
        i, j = random.sample(range(1, len(solution) - 1), 2)
        new_solution = deepcopy(solution)
        for _ in range(5):
            new_solution[i], new_solution[j] = solution[j], solution[i]
            if self.fitness(solution) < self.fitness(new_solution):
                return new_solution
        return solution
    
    def evolve(self):
        for generation in range(self.generations):
            new_population = []

            # Selection, Crossover, and Mutation
            for _ in range(self.population_size // 2):  # Generate population/2 children
                parent1, parent2 = self.tournament_selection(self.population)
                # print(parent1, parent2)
                child1, child2 = self.pmx_crossover(parent1, parent2)
                # print(child1, child2)
                # raise Exception
                child1, child2 = (parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                child1 = self.local_search(child1)
                child2 = self.local_search(child2)
                # print(child1,child2)
                new_population.extend([child1, child2])

            # Fitness evaluation and replacement of old population
            self.population = sorted(new_population, key=lambda sol: self.fitness(sol))[:self.population_size]

        # Return the best solution found
        self.best_solution = sorted(self.population, key=lambda sol: self.fitness(sol))[0]

# Load input data using the Problem class
# problem = Problem(mode='file', file_path='E:\D\HOCDIBANTRE\DVRP-hwng\\tiki\input.txt')
problem = Problem(mode='manual')

# Run the genetic algorithm
ga = GeneticAlgorithm(problem)
ga.evolve()

ga.print_final_solution()
# print(ga.fitness(ga.best_solution))

# print(ga.fitness(ga.best_solution))
# print(ga.fitness([1,5,0,2,4,0,3]))
