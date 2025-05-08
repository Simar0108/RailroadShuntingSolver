from typing import Dict, Any, Callable, Optional
from railway import RailwayState
from search import uniform_cost_search, a_star_misplaced, a_star_manhattan
from benchmarks import list_benchmarks, get_benchmark
from visualize import (
    plot_performance_comparison,
    plot_algorithm_efficiency,
    save_summary_statistics,
)

def get_user_input(prompt: str, valid_fn: Optional[Callable[[str], bool]] = None) -> str:
    while True:
        value = input(prompt)
        if valid_fn is None or valid_fn(value):
            return value
        print("Invalid input, please try again.")

def create_initial_state() -> RailwayState:
    print("\nWould you like to use a benchmark puzzle or enter a custom puzzle?")
    print("1. Use a benchmark puzzle")
    print("2. Enter a custom puzzle")
    choice = get_user_input("Enter 1 or 2: ", lambda x: x in {"1", "2"})
    if choice == "1":
        list_benchmarks()
        name = get_user_input("\nEnter the name of the benchmark puzzle: ", lambda x: get_benchmark(x) is not None)
        config = get_benchmark(name)
        print(f"\nSelected puzzle: {name}")
        state = RailwayState(
            main_track=config["main_track"],
            sidings=config["sidings"],
            goal_order=config["goal_order"],
        )
        state.name = name  # Set the puzzle name
        return state
    else:
        main_track = input("Enter the main track as a space-separated list (e.g., 3 1 2): ").split()
        num_sidings = int(get_user_input("How many sidings? (e.g., 2): ", lambda x: x.isdigit() and int(x) > 0))
        sidings = []
        for i in range(num_sidings):
            siding = input(f"Enter siding {i+1} as a space-separated list (or leave blank): ").split()
            sidings.append(siding)
        goal_order = input("Enter the goal order as a space-separated list: ").split()
        state = RailwayState(main_track=main_track, sidings=sidings, goal_order=goal_order)
        state.name = "custom"
        return state

def print_comparison_table(results: Dict[str, Dict[str, Any]]):
    """Print a comparison table of all algorithms' performance."""
    print("\n=== Performance Comparison ===")
    print("Algorithm".ljust(15) + "Path Length".ljust(15) + "Nodes Expanded".ljust(15) + 
          "Max Queue".ljust(15) + "Time (s)".ljust(15) + "Nodes/s")
    print("-" * 75)
    
    for algo, metrics in results.items():
        print(f"{algo.ljust(15)}{str(metrics['path_length']).ljust(15)}"
              f"{str(metrics['nodes_expanded']).ljust(15)}"
              f"{str(metrics['max_queue_size']).ljust(15)}"
              f"{f'{metrics['execution_time']:.4f}'.ljust(15)}"
              f"{f'{metrics['nodes_per_second']:.2f}'}")

def print_solution(algorithm: str, result: Dict[str, Any]):
    print(f"\n=== {algorithm} ===")
    if result["path"] is None:
        print("No solution found.")
        return
    print(f"Path length: {result['path_length']}")
    print(f"Nodes expanded: {result['nodes_expanded']}")
    print(f"Max queue size: {result['max_queue_size']}")
    print(f"Execution time: {result['execution_time']:.4f} seconds")
    print(f"Nodes per second: {result['nodes_per_second']:.2f}")
    print("\nSolution path:")
    for step, state in enumerate(result["path"]):
        print(f"Step {step}:")
        print("Main Track:", " → ".join(state.main_track))
        for i, siding in enumerate(state.sidings):
            print(f"Siding {i+1}:", " → ".join(siding))
        print()  # Add blank line between steps

def run_searches(initial_state: RailwayState, verbose: bool = True) -> Dict[str, Dict[str, Any]]:
    results = {}
    algorithms = {
        "UCS": uniform_cost_search,
        "A* Misplaced": a_star_misplaced,
        "A* Manhattan": a_star_manhattan,
    }
    for name, func in algorithms.items():
        path, nodes_expanded, max_queue_size, exec_time = func(initial_state)
        path_length = len(path) - 1 if path else 0
        nodes_per_second = nodes_expanded / exec_time if exec_time > 0 else 0
        results[name] = {
            "path": path,
            "path_length": path_length,
            "nodes_expanded": nodes_expanded,
            "max_queue_size": max_queue_size,
            "execution_time": exec_time,
            "nodes_per_second": nodes_per_second,
        }
        if verbose:
            print_solution(name, results[name])
    return results

def main():
    print("Welcome to the Railway Shunting Problem Solver!")
    initial_state = create_initial_state()
    print("\nInitial State:")
    print("Main Track:", " → ".join(initial_state.main_track))
    for i, siding in enumerate(initial_state.sidings):
        print(f"Siding {i+1}:", " → ".join(siding))
    print("\nGoal Order:", " → ".join(initial_state.goal_order))
    print()
    results = run_searches(initial_state)
    print_comparison_table(results)  # Add comparison table
    puzzle_name = initial_state.name  # Use the name we set earlier
    plot_performance_comparison(results, puzzle_name)
    plot_algorithm_efficiency(results, puzzle_name)
    save_summary_statistics(results, puzzle_name)
    print("\nResults and visualizations have been saved in the results/ directory.")

if __name__ == "__main__":
    main()