from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Train:
    """
    Represents a train in the railway system.
    
    Attributes:
        id (str): Unique identifier for the train
        position (Tuple[int, int]): Current position as (track_number, position_in_track)
            track_number: 0 for main track, 1+ for sidings
            position_in_track: Position within the track (0-based)
    """
    id: str
    position: Tuple[int, int]

class RailwayState:
    """
    Represents a state in the Railway Shunting problem.
    
    This class maintains the current state of the railway system, including:
    - The order of trains on the main track
    - The order of trains in each siding
    - The desired goal order
    
    The class provides methods for:
    - Generating valid next states
    - Checking if the current state is a goal state
    - Calculating various heuristics for search algorithms
    - Computing the cost of the current path
    """
    
    def __init__(self, 
                 main_track: List[str],
                 sidings: List[List[str]],
                 goal_order: List[str]) -> None:
        """
        Initialize a new railway state.
        
        Args:
            main_track: List of train IDs on the main track, ordered from front to back
            sidings: List of lists, each inner list represents a siding with train IDs
                    ordered from front to back
            goal_order: Desired order of trains on the main track
        
        Raises:
            ValueError: If any train ID appears more than once in the system
        """
        self.main_track = main_track
        self.sidings = sidings
        self.goal_order = goal_order
        self.num_sidings = len(sidings)
        
        # Validate that no train appears more than once
        all_trains = main_track + [train for siding in sidings for train in siding]
        if len(all_trains) != len(set(all_trains)):
            raise ValueError("Each train ID must appear exactly once in the system")
    
    def __eq__(self, other: Any) -> bool:
        """
        Check if two states are equal.
        
        Args:
            other: Another object to compare with
            
        Returns:
            bool: True if the states are equal, False otherwise
        """
        if not isinstance(other, RailwayState):
            return False
        return (self.main_track == other.main_track and 
                self.sidings == other.sidings)
    
    def __hash__(self) -> int:
        """
        Generate a hash value for the state.
        
        Returns:
            int: Hash value based on the current state
        """
        return hash((tuple(self.main_track), 
                    tuple(tuple(siding) for siding in self.sidings)))
    
    def __lt__(self, other: 'RailwayState') -> bool:
        """
        Compare states based on their cost for priority queue ordering.
        
        Args:
            other: Another RailwayState to compare with
            
        Returns:
            bool: True if this state's cost is less than the other state's cost
            
        Raises:
            NotImplementedError: If other is not a RailwayState
        """
        if not isinstance(other, RailwayState):
            return NotImplemented
        return self.get_cost() < other.get_cost()
    
    def get_neighbors(self) -> List['RailwayState']:
        """
        Generate all valid next states by moving trains.
        
        Rules:
        1. Can only move the first train from the main track to any siding
        2. Can only move the last train from a siding back to the main track
        3. Each siding has a maximum capacity of 3 trains
        
        Returns:
            List[RailwayState]: List of all valid next states
        """
        neighbors = []
        
        # Move from main track to siding
        if self.main_track:
            train = self.main_track[0]  # Can only move the first train
            for i, siding in enumerate(self.sidings):
                if len(siding) < 3:  # Maximum 3 trains per siding
                    new_state = deepcopy(self)
                    new_state.main_track.pop(0)
                    new_state.sidings[i].append(train)
                    neighbors.append(new_state)
        
        # Move from siding to main track
        for i, siding in enumerate(self.sidings):
            if siding:
                new_state = deepcopy(self)
                train = new_state.sidings[i].pop()
                new_state.main_track.insert(0, train)
                neighbors.append(new_state)
        
        return neighbors
    
    def is_goal(self) -> bool:
        """
        Check if the current state matches the goal order.
        
        Returns:
            bool: True if the main track matches the goal order, False otherwise
        """
        return self.main_track == self.goal_order
    
    def get_cost(self) -> int:
        """
        Calculate the cost of the current path.
        
        The cost is defined as the number of moves made so far,
        which is equal to the total number of trains in the system.
        
        Returns:
            int: Total number of trains in the system
        """
        return len(self.main_track) + sum(len(siding) for siding in self.sidings)
    
    def get_misplaced_heuristic(self) -> int:
        """
        Calculate the misplaced train heuristic.
        
        This heuristic counts the number of trains that are not in their
        correct position in the main track compared to the goal order.
        
        Returns:
            int: Number of misplaced trains
        """
        misplaced = 0
        for i, train in enumerate(self.main_track):
            if i >= len(self.goal_order) or train != self.goal_order[i]:
                misplaced += 1
        return misplaced
    
    def get_manhattan_heuristic(self) -> int:
        """
        Calculate the Manhattan distance heuristic.
        
        This heuristic computes the sum of Manhattan distances between
        each train's current position and its goal position.
        
        Returns:
            int: Sum of Manhattan distances for all trains
        """
        total_distance = 0
        
        # Create a mapping of current positions
        current_positions: Dict[str, Tuple[int, int]] = {}
        for i, train in enumerate(self.main_track):
            current_positions[train] = (0, i)  # (track, position)
        
        for i, siding in enumerate(self.sidings):
            for j, train in enumerate(siding):
                current_positions[train] = (i + 1, j)
        
        # Calculate distance to goal positions
        for i, train in enumerate(self.goal_order):
            if train in current_positions:
                current_track, current_pos = current_positions[train]
                goal_track, goal_pos = 0, i
                distance = abs(current_track - goal_track) + abs(current_pos - goal_pos)
                total_distance += distance
        
        return total_distance
    
    def print_state(self) -> None:
        """
        Print the current state in a human-readable format.
        
        The output shows:
        - The current order of trains on the main track
        - The current order of trains in each siding
        - The desired goal order
        """
        print("\nCurrent Railway State:")
        print("Main Track:", " → ".join(self.main_track))
        for i, siding in enumerate(self.sidings):
            print(f"Siding {i+1}:", " → ".join(siding))
        print("\nGoal Order:", " → ".join(self.goal_order)) 