from typing import List, Tuple, Set, Optional, Dict, Callable
from queue import PriorityQueue, Queue
from railway import RailwayState
import time

def general_search(initial_state: RailwayState, queueing_function: Callable) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    General search algorithm that can be used to implement various search strategies
    by providing different queueing functions. Follows the algorithm from the lecture slides.
    
    Args:
        initial_state: The starting state of the railway system
        queueing_function: Function that determines how to add nodes to the frontier
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    start_time = time.time()
    
    # Initialize the frontier with the initial state
    frontier = queueing_function.make_queue(initial_state)
    explored: Set[RailwayState] = set()
    nodes_expanded = 0
    max_queue_size = 1
    
    # Keep track of parent states to reconstruct the path
    parent_map: Dict[RailwayState, Optional[RailwayState]] = {initial_state: None}
    
    while not frontier.empty():
        current_state = frontier.get()
        
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
        
        # Expand the current node and add children to frontier
        neighbors = current_state.get_neighbors()
        frontier = queueing_function.add_to_frontier(frontier, neighbors, explored, parent_map, current_state)
        max_queue_size = max(max_queue_size, frontier.qsize())
    
    execution_time = time.time() - start_time
    return None, nodes_expanded, max_queue_size, execution_time

class UniformCostQueueing:
    @staticmethod
    def make_queue(initial_state: RailwayState) -> PriorityQueue:
        queue = PriorityQueue()
        queue.put((0, id(initial_state), initial_state))
        return queue
    
    @staticmethod
    def add_to_frontier(frontier: PriorityQueue, neighbors: List[RailwayState], 
                       explored: Set[RailwayState], parent_map: Dict[RailwayState, Optional[RailwayState]], 
                       current_state: RailwayState) -> PriorityQueue:
        for neighbor in neighbors:
            if neighbor not in explored:
                frontier.put((neighbor.get_cost(), id(neighbor), neighbor))
                parent_map[neighbor] = current_state
        return frontier

class AStarMisplacedQueueing:
    @staticmethod
    def make_queue(initial_state: RailwayState) -> PriorityQueue:
        queue = PriorityQueue()
        queue.put((initial_state.get_misplaced_heuristic(), id(initial_state), initial_state))
        return queue
    
    @staticmethod
    def add_to_frontier(frontier: PriorityQueue, neighbors: List[RailwayState], 
                       explored: Set[RailwayState], parent_map: Dict[RailwayState, Optional[RailwayState]], 
                       current_state: RailwayState) -> PriorityQueue:
        for neighbor in neighbors:
            if neighbor not in explored:
                f = neighbor.get_cost() + neighbor.get_misplaced_heuristic()
                frontier.put((f, id(neighbor), neighbor))
                parent_map[neighbor] = current_state
        return frontier

class AStarManhattanQueueing:
    @staticmethod
    def make_queue(initial_state: RailwayState) -> PriorityQueue:
        queue = PriorityQueue()
        queue.put((initial_state.get_manhattan_heuristic(), id(initial_state), initial_state))
        return queue
    
    @staticmethod
    def add_to_frontier(frontier: PriorityQueue, neighbors: List[RailwayState], 
                       explored: Set[RailwayState], parent_map: Dict[RailwayState, Optional[RailwayState]], 
                       current_state: RailwayState) -> PriorityQueue:
        for neighbor in neighbors:
            if neighbor not in explored:
                f = neighbor.get_cost() + neighbor.get_manhattan_heuristic()
                frontier.put((f, id(neighbor), neighbor))
                parent_map[neighbor] = current_state
        return frontier

def uniform_cost_search(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement Uniform Cost Search to solve the railway shunting problem.
    
    This algorithm explores states in order of their path cost, ensuring that
    the first solution found is optimal in terms of the number of moves.
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    return general_search(initial_state, UniformCostQueueing)

def a_star_misplaced(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement A* search with misplaced train heuristic.
    
    This algorithm uses the number of misplaced trains as a heuristic to guide
    the search towards the goal state.
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    return general_search(initial_state, AStarMisplacedQueueing)

def a_star_manhattan(initial_state: RailwayState) -> Tuple[Optional[List[RailwayState]], int, int, float]:
    """
    Implement A* search with Manhattan distance heuristic.
    
    This algorithm uses the sum of Manhattan distances between each train's
    current position and its goal position as a heuristic.
    
    Args:
        initial_state: The starting state of the railway system
        
    Returns:
        Tuple containing:
        - List of states representing the solution path (None if no solution found)
        - Number of nodes expanded during search
        - Maximum size of the frontier queue
        - Execution time in seconds
    """
    return general_search(initial_state, AStarManhattanQueueing) 