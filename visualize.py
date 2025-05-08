import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any
import os
from datetime import datetime

def ensure_results_dir() -> str:
    """Create a results directory with timestamp if it doesn't exist."""
    if not os.path.exists('results'):
        os.makedirs('results')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join('results', f'run_{timestamp}')
    
    # If directory exists, append a counter to make it unique
    counter = 1
    while os.path.exists(results_dir):
        results_dir = os.path.join('results', f'run_{timestamp}_{counter}')
        counter += 1
    
    os.makedirs(results_dir)
    return results_dir

def plot_performance_comparison(results: Dict[str, Dict[str, Any]], puzzle_name: str) -> str:
    """Create a comprehensive visualization of algorithm performance."""
    results_dir = ensure_results_dir()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(f'Performance Comparison for Puzzle: {puzzle_name}', fontsize=16)
    
    # 1. Path Length Comparison
    plt.subplot(2, 2, 1)
    algorithms = list(results.keys())
    path_lengths = [results[algo]['path_length'] for algo in algorithms]
    bars = plt.bar(algorithms, path_lengths)
    plt.title('Path Length Comparison')
    plt.ylabel('Number of Moves')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom')
    
    # 2. Nodes Expanded
    plt.subplot(2, 2, 2)
    nodes_expanded = [results[algo]['nodes_expanded'] for algo in algorithms]
    bars = plt.bar(algorithms, nodes_expanded)
    plt.title('Nodes Expanded')
    plt.ylabel('Number of Nodes')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom')
    
    # 3. Execution Time
    plt.subplot(2, 2, 3)
    execution_times = [results[algo]['execution_time'] for algo in algorithms]
    bars = plt.bar(algorithms, execution_times)
    plt.title('Execution Time')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom')
    
    # 4. Nodes per Second
    plt.subplot(2, 2, 4)
    nodes_per_sec = [results[algo]['nodes_per_second'] for algo in algorithms]
    bars = plt.bar(algorithms, nodes_per_sec)
    plt.title('Search Speed')
    plt.ylabel('Nodes/Second')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plot_path = os.path.join(results_dir, f'performance_{puzzle_name}.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return results_dir

def plot_algorithm_efficiency(results: Dict[str, Dict[str, Any]], puzzle_name: str) -> str:
    """Create a scatter plot showing the trade-off between solution quality and computational cost."""
    results_dir = ensure_results_dir()
    
    plt.figure(figsize=(10, 6))
    
    algorithms = list(results.keys())
    path_lengths = [results[algo]['path_length'] for algo in algorithms]
    nodes_expanded = [results[algo]['nodes_expanded'] for algo in algorithms]
    
    plt.scatter(path_lengths, nodes_expanded, s=200, alpha=0.6)
    
    for i, algo in enumerate(algorithms):
        plt.annotate(algo, 
                    (path_lengths[i], nodes_expanded[i]),
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
    
    plt.title(f'Algorithm Efficiency for Puzzle: {puzzle_name}')
    plt.xlabel('Solution Path Length')
    plt.ylabel('Nodes Expanded')
    plt.grid(True)
    
    # Add a trend line
    z = np.polyfit(path_lengths, nodes_expanded, 1)
    p = np.poly1d(z)
    plt.plot(path_lengths, p(path_lengths), "r--", alpha=0.8)
    
    plot_path = os.path.join(results_dir, f'efficiency_{puzzle_name}.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return results_dir

def save_summary_statistics(results: Dict[str, Dict[str, Any]], puzzle_name: str) -> str:
    """Save a text file with summary statistics for each algorithm."""
    results_dir = ensure_results_dir()
    stats_path = os.path.join(results_dir, f'stats_{puzzle_name}.txt')
    
    with open(stats_path, 'w') as f:
        f.write(f"Summary Statistics for Puzzle: {puzzle_name}\n")
        f.write("=" * 50 + "\n\n")
        
        for algo, metrics in results.items():
            f.write(f"Algorithm: {algo}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Path Length: {metrics['path_length']}\n")
            f.write(f"Nodes Expanded: {metrics['nodes_expanded']}\n")
            f.write(f"Max Queue Size: {metrics['max_queue_size']}\n")
            f.write(f"Execution Time: {metrics['execution_time']:.4f} seconds\n")
            f.write(f"Nodes per Second: {metrics['nodes_per_second']:.2f}\n\n")
    
    return results_dir 