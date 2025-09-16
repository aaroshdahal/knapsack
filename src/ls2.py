import sys
import random
import time
import math


class Item:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
        self.value_per_weight = value / weight

def read_input(filename):
    items = []
    with open(filename, 'r') as file:
        n, capacity = map(int, file.readline().split())
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
    
    return total_value, selected_items, trace





# ADD CODE HERE

def bnb(items, capacity):
    pass

def ls1(items, capacity):
    pass


def ls2(items, capacity, start_temp=1000, alpha=0.999, min_temp=1):
    # Randomly initialize a feasible solution
    current_solution = []
    current_weight = 0
    current_value = 0
    for item in items:
        if current_weight + item.weight <= capacity:
            current_solution.append(item.index)
            current_weight += item.weight
            current_value += item.value

    # Start temperature and minimum temperature
    temperature = start_temp

    # Trace for the solution quality over time
    trace = []
    start_time = time.time()

    while temperature > min_temp:
        # Pick a random item from the items list
        candidate = random.choice(items)
        
        # Calculate the impact of adding or removing the item
        if candidate.index in current_solution:
            # Try to remove the item
            new_solution = current_solution.copy()
            new_solution.remove(candidate.index)
            new_weight = current_weight - candidate.weight
            new_value = current_value - candidate.value
        else:
            # Try to add the item if it fits
            if current_weight + candidate.weight <= capacity:
                new_solution = current_solution.copy()
                new_solution.append(candidate.index)
                new_weight = current_weight + candidate.weight
                new_value = current_value + candidate.value
            else:
                continue  # Skip if the item cannot be added

        # Calculate the change in value
        delta_value = new_value - current_value

        # Decide whether to accept the new solution
        if delta_value > 0 or random.random() < math.exp(delta_value / temperature):
            current_solution = new_solution
            current_weight = new_weight
            current_value = new_value
            trace.append((time.time() - start_time, current_value))

        # Cooling down the temperature
        temperature *= alpha

    return current_value, current_solution, trace





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
    elif filename == "small_1":
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
