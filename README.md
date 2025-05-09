# Railway Shunting Problem Solver

This project implements various search algorithms to solve the Railway Shunting Problem, where trains need to be rearranged using sidings to achieve a desired order.

## Project Structure

```
.
├── main.py              # Main program entry point
├── railway.py           # Core railway state and logic
├── search.py            # Search algorithm implementations
├── benchmarks.py        # Predefined puzzle configurations
├── visualize.py         # Visualization and statistics
├── requirements.txt     # Project dependencies
└── results/             # Output directory for visualizations
```

## Features

- Multiple search algorithms:
  - Uniform Cost Search (UCS)
  - A* with Misplaced Train heuristic
  - A* with Manhattan Distance heuristic
- Interactive puzzle selection:
  - Choose from predefined benchmark puzzles
  - Create custom puzzles
- Comprehensive performance analysis:
  - Path length comparison
  - Nodes expanded
  - Execution time
  - Search efficiency
- Visual output:
  - Performance comparison plots
  - Algorithm efficiency plots
  - Detailed solution paths
  - Summary statistics

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program:
```bash
python main.py
```

### Program Flow

1. Choose between benchmark puzzles or custom puzzle:
   - Benchmark puzzles: Predefined configurations of varying difficulty
   - Custom puzzle: Define your own initial state and goal

2. For benchmark puzzles:
   - Select from available puzzles (easy, medium, hard)
   - View puzzle description and expected solution depth

3. For custom puzzles:
   - Enter main track configuration
   - Specify number of sidings
   - Enter train positions in each siding
   - Define goal order

4. View results:
   - Initial state and goal order
   - Solution paths for each algorithm
   - Performance comparison table
   - Visualizations saved in results directory

### Output

The program generates:
1. Console output:
   - Initial state and goal configuration
   - Step-by-step solution paths
   - Performance comparison table

2. Results directory (timestamped):
   - Performance comparison plots
   - Algorithm efficiency plots
   - Summary statistics

## Benchmark Puzzles

### Easy Puzzles
- `easy1`: Already solved (0 moves)
- `easy2`: Simple swap (2 moves)

### Medium Puzzles
- `medium1`: Requires use of both sidings (4 moves)
- `medium2`: Three sidings, more options (6 moves)

### Hard Puzzles
- `hard1`: Reverse order, four trains (8 moves)
- `hard2`: Complex shuffle, four trains (10 moves)

## Dependencies

- Python 3.6+
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- pytest == 7.4.0 (for testing)