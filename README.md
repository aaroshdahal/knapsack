# CSE 6140 Algorithms Project: Knapsack Problem

This repository contains implementations of four different algorithms for solving the 0-1 Knapsack Problem, developed as part of a CSE 6140 (Algorithms) course project at Georgia Institute of Technology.

## Authors

- **Aarosh Dahal** - School of Civil and Environmental Engineering, Georgia Institute of Technology
- **Praful Patil** - School of Civil and Environmental Engineering, Georgia Institute of Technology
- **Joshua Wood Reeves** - School of Computer Science, Georgia Institute of Technology
- **Adam Siffel** - School of Mechanical Engineering, Georgia Institute of Technology

## Problem Description

The Knapsack Problem is a classic NP-Complete problem in combinatorial optimization. Given a knapsack with weight capacity `W` and `n` items, each with value `vi` and weight `wi`, the goal is to select a subset of items that maximizes total value without exceeding the weight limit.

## Algorithms Implemented

This project implements and compares four different approaches:

1. **Branch and Bound** - Exact algorithm that guarantees optimal solution
2. **Approximation** - Greedy algorithm with 2-approximation guarantee
3. **Local Search 1 (Hill Climbing)** - Iterative improvement using random swaps
4. **Local Search 2 (Simulated Annealing)** - Probabilistic local search with cooling schedule

## Project Structure

```
cse6140_algorithms/
├── src/                          # Source code
│   ├── ks_algorithms.py         # Main algorithm implementations
│   ├── ls1.py                   # Local Search 1 (Hill Climbing)
│   ├── ls2.py                   # Local Search 2 (Simulated Annealing)
│   └── README.txt               # Original usage instructions
├── output/                       # Algorithm outputs
│   ├── approximation/           # Approximation algorithm results
│   ├── branch_and_bound/        # Branch and bound results
│   ├── local_search_1/          # Hill climbing results
│   └── local_search_2/          # Simulated annealing results
├── docs/                        # Documentation
│   └── project_report.pdf       # Comprehensive project report
└── README.md                    # This file
```

## Usage

### Basic Usage

```bash
python src/ks_algorithms.py -inst <filename> -alg <method> -time <cutoff> -seed <seed>
```

### Parameters

- `<filename>`: Dataset file path (assumes data in `DATASET/` directory)
  - Format: `"DATASET/small_scale/small_1"`
  - Special options: `test`, `small`, `large` (runs all respective datasets)
- `<method>`: Algorithm choice
  - `BnB`: Branch and Bound
  - `Approx`: Approximation algorithm
  - `LS1`: Local Search 1 (Hill Climbing)
  - `LS2`: Local Search 2 (Simulated Annealing)
- `<cutoff>`: Time limit in seconds
- `<seed>`: Random seed for reproducible results

### Example Commands

```bash
# Run Branch and Bound on small dataset with 30 minute cutoff
python src/ks_algorithms.py -inst DATASET/small_scale/small_1 -alg BnB -time 1800 -seed 42

# Run all algorithms on large datasets
python src/ks_algorithms.py -inst large -alg Approx -time 600 -seed 123
```

## Requirements

- Python 3.x
- Must have output folder structure with subfolders: `test`, `small_scale`, `large_scale`

## Results Summary

Based on empirical evaluation:

- **Branch and Bound**: Achieves optimal solutions but computationally expensive for large datasets
- **Approximation**: Best balance of speed and accuracy, with relative errors typically under 4%
- **Local Search 1**: Struggles with larger datasets, relative errors up to 30%
- **Local Search 2**: Good performance on small datasets but deteriorates on larger instances

## Output Format

Results are saved to the `output/` directory organized by algorithm type, containing solution quality and runtime information for each test case.

## Documentation

For detailed algorithm descriptions, complexity analysis, empirical evaluation, and comprehensive results, see the full project report in `docs/project_report.pdf`.

## License

This project was developed for academic purposes as part of CSE 6140 at Georgia Institute of Technology.