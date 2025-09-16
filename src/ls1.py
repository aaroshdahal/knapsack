import sys
import random
import time

class Item:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
        self.value_per_weight = value / weight

def read_input(filename):
    items = []
    with open(filename, 'r') as file:
        n, capacity = map(float, file.readline().split())
        n=int(n)
        for index in range(n):
            value, weight = map(float, file.readline().split())
            items.append(Item(index, value, weight))
    return items, capacity

def write_solution(output, filename, method, cutoff, seed=None):
    if seed:
        sol_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}_{seed}.sol"
    else:
        sol_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}.sol"
    with open(sol_filename, 'w') as file:
        file.write(str(output[0]) + '\n')
        file.write(','.join(map(str, output[1])) + '\n')

def write_trace(trace, filename, method, cutoff, seed=None):
    if seed:
        trace_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}_{seed}.trace"
    else:
        trace_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}.trace"
    with open(trace_filename, 'w') as file:
        for timestamp, quality in trace:
            file.write(f"{timestamp},{quality}\n")


def approx(items, capacity):
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x.value_per_weight, reverse=True)

    # Sort items again by value in descending order
    # items.sort(key=lambda x: x.value, reverse=True)

    total_value = 0
    total_weight = 0
    selected_items = []
    trace = []
    time_start = time.time()
    
    # Loop through
    for item in items:
        if total_weight + item.weight <= capacity:
            total_value += item.value
            total_weight += item.weight
            selected_items.append(item.index)

            trace.append((time.time() - time_start, total_value))
    print(total_weight-capacity)
    print(selected_items)
    return total_value, selected_items, trace





# ADD CODE HERE

def bnb(items, capacity):
    pass

def ls1(items, capacity):
    
    # Initialise solution randomly

    def initialise(items, capacity):
        initial_solution = [random.choice([0, 1]) for _ in range(len(items))]
        '''in case approx algorithm is used for initialisation
        value_weight_ratio = [(item.value / item.weight, item) for item in items]
        value_weight_ratio = sorted(value_weight_ratio, key=lambda x: x[0], reverse=True)
        total_value = 0
        initial_solution = [0] * len(items)
        temp_capacity = capacity
        for ratio, item in value_weight_ratio:
            if item.weight <= temp_capacity:
                initial_solution[item.index] = 1
                total_value += item.value
                temp_capacity -= item.weight
        '''
        return initial_solution
   
    # Evaluate Total Weight and Value of Solution (Penalise for weight exceeding capacity)

    def evaluate(selected_items):
        total_value=0
        total_weight=0
        total_value = sum(items[i].value*selected_items[i] for i in range(len(items)))
        total_weight = sum(items[i].weight*selected_items[i] for i in range(len(items)))
        if total_weight > capacity:
            total_value=-total_weight
        return total_value, total_weight   

    #Generate Neighbors by flipping selection of all combinations of 2 pairs of elements

    def generate_neighbor(solution):
        neighbor=list(solution)
        i,j = random.sample(range(len(items)), 2)
        neighbor[i]=1-neighbor[i]
        neighbor[j]=1-neighbor[j]
        return neighbor

    time_start = time.time()
    
    current_solution = initialise(items,capacity)
    total_value, current_weight = evaluate(current_solution)
    
    trace=[]
    trace.append((time.time() - time_start, total_value))

    # Main loop for local search

    done = False
    counter=0
    
    while not(done):

        original_solution = list(current_solution)
        neighbor = generate_neighbor(current_solution)
        n=len(items)

        neighbor_value, neighbor_weight = evaluate(neighbor)
        if neighbor_value > total_value:
            current_solution = list(neighbor)
            total_value = neighbor_value
            total_weight = neighbor_weight  
            trace.append((time.time() - time_start, total_value))
        counter = counter+1
        
        #if cutoff_time>=900:
        if counter==4000000 or counter ==len(items)**2:
            done = True
        
            
    selected_items = []
    for i in range(len(items)):
        if current_solution[i] == 1:
            selected_items.append(i)
            
    return total_value, selected_items, trace


def ls2(items, capacity):
    pass




def run(filename, method, cutoff_time, seed):
    # Read data
    items, capacity = read_input(filename)

    start_time = time.time()
    
    # Run chosen algorithm
    if method == "bnb":
        value, selected_items, trace = bnb(items, capacity)
        method = "BnB"
    elif method == "approx":
        value, selected_items, trace = approx(items, capacity)
        method = "Approx"
    elif method == "ls1":
        value, selected_items, trace = ls1(items, capacity)
        method = "LS1"
    elif method == "ls2":
        value, selected_items, trace = ls2(items, capacity)
        method = "LS2"
    else:
        print("No such method.\n")
        exit()
    
    end_time = time.time()

    # Write outputs
    filename = filename[8:]
    write_solution((value, selected_items), filename, method, cutoff_time, seed)
    write_trace(trace, filename, method, cutoff_time, seed)

    exec_time = end_time - start_time

    return exec_time

def main():
    # Command line arguments
    filename = sys.argv[sys.argv.index('-inst') + 1]
    method = sys.argv[sys.argv.index('-alg') + 1].lower()
    cutoff_time = int(sys.argv[sys.argv.index('-time') + 1])
    seed = int(sys.argv[sys.argv.index('-seed') + 1])

    # filename = "DATASET\\"  + filename

    random.seed(seed)

    times = []
    if filename == "test":
        for i in range(8):
            filename = "DATASET\\test\\KP_s_0" + str(i+1)
            time = run(filename, method, cutoff_time, seed)
            times.append(time)
        print(times)
    elif filename == "small":
        for i in range(10):
            filename = "DATASET\\small_scale\\small_" + str(i+1)
            time = run(filename, method, cutoff_time, seed)
            times.append(time)
        print(times)
    elif filename == "large":
        for i in range(21):
            filename = "DATASET\\large_scale\\large_" + str(i+1)
            time = run(filename, method, cutoff_time, seed)
            times.append(time)
        print(times)
    else:
        time = run(filename, method, cutoff_time, seed)
        print("Execution time:", time, "seconds")

if __name__ == "__main__":
    main()
