from typing import List, Tuple, Set, Optional, Dict
from queue import PriorityQueue
from railway import RailwayState
import time

def uniform_cost_search(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement Uniform Cost Search to solve the railway shunting problem.
    
    This algorithm explores states in order of their path cost, ensuring that
    the first solution found is optimal in terms of the number of moves. In other words,
    it is A* with a heuristic of 0, equivalent to a breadth-first search.
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    start_time = time.time()
    
    frontier = PriorityQueue()
    # Use a tuple of (cost, id, state) to ensure unique ordering
    frontier.put((0, id(initial_state), initial_state))
    explored: Set[RailwayState] = set()
    nodes_expanded = 0
    max_queue_size = 1
    
    # Keep track of parent states to reconstruct the path
    parent_map: Dict[RailwayState, Optional[RailwayState]] = {initial_state: None}
    
    while not frontier.empty():
        current_cost, _, current_state = frontier.get()
        
        if current_state.is_goal():
            # Reconstruct path
            path = []
            state = current_state
            while state:
                path.append(state)
                state = parent_map[state]
            execution_time = time.time() - start_time
            return path[::-1], nodes_expanded, max_queue_size, execution_time
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in explored:
                frontier.put((neighbor.get_cost(), id(neighbor), neighbor))
                parent_map[neighbor] = current_state
                max_queue_size = max(max_queue_size, frontier.qsize())
    
    execution_time = time.time() - start_time
    return None, nodes_expanded, max_queue_size, execution_time

def a_star_misplaced(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement A* search with misplaced train heuristic.
    
    This algorithm uses the number of misplaced trains as a heuristic to guide
    the search towards the goal state. The heuristic is admissible as it never
    overestimates the cost to reach the goal.
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    start_time = time.time()
    
    frontier = PriorityQueue()
    # Use a tuple of (f_score, id, state) to ensure unique ordering
    frontier.put((initial_state.get_misplaced_heuristic(), id(initial_state), initial_state))
    explored: Set[RailwayState] = set()
    nodes_expanded = 0
    max_queue_size = 1
    
    # Keep track of parent states to reconstruct the path
    parent_map: Dict[RailwayState, Optional[RailwayState]] = {initial_state: None}
    
    while not frontier.empty():
        _, _, current_state = frontier.get()
        
        if current_state.is_goal():
            # Reconstruct path
            path = []
            state = current_state
            while state:
                path.append(state)
                state = parent_map[state]
            execution_time = time.time() - start_time
            return path[::-1], nodes_expanded, max_queue_size, execution_time
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in explored:
                f = neighbor.get_cost() + neighbor.get_misplaced_heuristic()
                frontier.put((f, id(neighbor), neighbor))
                parent_map[neighbor] = current_state
                max_queue_size = max(max_queue_size, frontier.qsize())
    
    execution_time = time.time() - start_time
    return None, nodes_expanded, max_queue_size, execution_time

def a_star_manhattan(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement A* search with Manhattan distance heuristic.
    
    This algorithm uses the sum of Manhattan distances between each train's
    current position and its goal position as a heuristic. This heuristic
    is admissible as it never overestimates the actual cost to reach the goal. 
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    start_time = time.time()
    
    frontier = PriorityQueue()
    # Use a tuple of (f_score, id, state) to ensure unique ordering
    frontier.put((initial_state.get_manhattan_heuristic(), id(initial_state), initial_state))
    explored: Set[RailwayState] = set()
    nodes_expanded = 0
    max_queue_size = 1
    
    # Keep track of parent states to reconstruct the path
    parent_map: Dict[RailwayState, Optional[RailwayState]] = {initial_state: None}
    
    while not frontier.empty():
        _, _, current_state = frontier.get()
        
        if current_state.is_goal():
            # Reconstruct path
            path = []
            state = current_state
            while state:
                path.append(state)
                state = parent_map[state]
            execution_time = time.time() - start_time
            return path[::-1], nodes_expanded, max_queue_size, execution_time
            
        if current_state in explored:
            continue
            
        explored.add(current_state)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in explored:
                f = neighbor.get_cost() + neighbor.get_manhattan_heuristic()
                frontier.put((f, id(neighbor), neighbor))
                parent_map[neighbor] = current_state
                max_queue_size = max(max_queue_size, frontier.qsize())
    
    execution_time = time.time() - start_time
    return None, nodes_expanded, max_queue_size, execution_time 