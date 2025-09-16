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
        file.write(str(int(output[0])) + '\n')
        file.write(','.join(map(str, output[1])) + '\n')

def write_trace(trace, filename, method, cutoff, seed=None):
    if seed:
        trace_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}_{seed}.trace"
    else:
        trace_filename = f"output\{filename.split('.')[0]}_{method}_{cutoff}.trace"
    with open(trace_filename, 'w') as file:
        for timestamp, quality in trace:
            file.write(f"{timestamp},{int(quality)}\n")


def approx(items, capacity):
    time_start = time.time()
    
    # Greedy approach 1: sort by density
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x.value_per_weight, reverse=True)

    total_value_1 = 0
    total_weight_1 = 0
    selected_items_1 = []
    trace_1 = []
    
    # Loop through
    for item in items:
        if total_weight_1 + item.weight <= capacity:
            total_value_1 += item.value
            total_weight_1 += item.weight
            selected_items_1.append(item.index)

            trace_1.append((time.time() - time_start, total_value_1))
    
    time_start = time.time()

    # Greedy approach 2: sort by value
    # Sort items again by value in descending order
    items.sort(key=lambda x: x.value, reverse=True)

    total_value_2 = 0
    total_weight_2 = 0
    selected_items_2 = []
    trace_2 = []

    # Loop through
    for item in items:
        if total_weight_2 + item.weight <= capacity:
            total_value_2 += item.value
            total_weight_2 += item.weight
            selected_items_2.append(item.index)

            trace_2.append((time.time() - time_start, total_value_2))
    
    if total_value_1 > total_value_2:
        return total_value_1, selected_items_1, trace_1
    else:
        return total_value_2, selected_items_2, trace_2






# ADD CODE HERE

def bnb(items, capacity):
    pass

def ls1(items, capacity):
    pass

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

    return value, exec_time

def main():
    # Command line arguments
    filename = sys.argv[sys.argv.index('-inst') + 1]
    method = sys.argv[sys.argv.index('-alg') + 1].lower()
    cutoff_time = int(sys.argv[sys.argv.index('-time') + 1])
    seed = int(sys.argv[sys.argv.index('-seed') + 1])

    random.seed(seed)

    values = []
    times = []
    if filename == "test":
        for i in range(8):
            filename = "DATASET\\test\\KP_s_0" + str(i+1)
            value, time = run(filename, method, cutoff_time, seed)
            values.append(value)
            times.append(time)
        print(values)
        print(times)
    elif filename == "small":
        for i in range(10):
            filename = "DATASET\\small_scale\\small_" + str(i+1)
            value, time = run(filename, method, cutoff_time, seed)
            values.append(value)
            times.append(time)
        print(values)
        print(times)
    elif filename == "large":
        for i in range(21):
            filename = "DATASET\\large_scale\\large_" + str(i+1)
            value, time = run(filename, method, cutoff_time, seed)
            values.append(value)
            times.append(time)
        print(values)
        print(times)
    else:
        value, time = run(filename, method, cutoff_time, seed)
        print("Value:", value)
        print("Execution time:", time, "seconds")

if __name__ == "__main__":
    main()
