from typing import List, Dict, Optional, TypedDict, Set
from dataclasses import dataclass
import json
import os

class PuzzleConfig(TypedDict):
    """Type definition for puzzle configuration."""
    main_track: List[str]
    sidings: List[List[str]]
    goal_order: List[str]
    description: str
    difficulty: str
    expected_depth: int

@dataclass
class PuzzleValidation:
    """Validation results for a puzzle configuration."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

def validate_puzzle(puzzle: PuzzleConfig) -> PuzzleValidation:
    """
    Validates a puzzle configuration.
    
    Args:
        puzzle: The puzzle configuration to validate
        
    Returns:
        PuzzleValidation object containing validation results
    """
    errors = []
    warnings = []
    
    # Checks if the puzzle has all the required fields
    required_fields = ['main_track', 'sidings', 'goal_order', 'description', 'difficulty', 'expected_depth']
    for field in required_fields:
        if field not in puzzle:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return PuzzleValidation(False, errors, warnings)
    
    # Checks if the main track is not empty and if all the trains are strings
    if not puzzle['main_track']:
        errors.append("Main track cannot be empty")
    if not all(isinstance(train, str) for train in puzzle['main_track']):
        errors.append("All trains in main track must be strings")
    
    # Checks if the sidings are not empty and if all the sidings are lists
    if not puzzle['sidings']:
        errors.append("At least one siding is required")
    if not all(isinstance(siding, list) for siding in puzzle['sidings']):
        errors.append("All sidings must be lists")
    if not all(all(isinstance(train, str) for train in siding) for siding in puzzle['sidings']):
        errors.append("All trains in sidings must be strings")
    if not all(len(siding) <= 3 for siding in puzzle['sidings']):
        errors.append("Each siding can hold at most 3 trains")
    
    # Checks if the goal order is not empty and if all the trains are strings
    if not puzzle['goal_order']:
        errors.append("Goal order cannot be empty")
    if not all(isinstance(train, str) for train in puzzle['goal_order']):
        errors.append("All trains in goal order must be strings")
    
    # Checks if each train ID appears exactly once
    all_trains = puzzle['main_track'] + [train for siding in puzzle['sidings'] for train in siding]
    if len(all_trains) != len(set(all_trains)):
        errors.append("Each train ID must appear exactly once")
    
    # Checks if the goal order contains all trains
    if set(puzzle['goal_order']) != set(all_trains):
        errors.append("Goal order must contain exactly the same trains as the initial state")
    
    # Checks if the difficulty is one of the valid difficulties
    valid_difficulties = {'easy', 'medium', 'hard'}
    if puzzle['difficulty'] not in valid_difficulties:
        errors.append(f"Difficulty must be one of: {', '.join(valid_difficulties)}")
    
    # Checks if the expected depth is a non-negative integer
    if not isinstance(puzzle['expected_depth'], int) or puzzle['expected_depth'] < 0:
        errors.append("Expected depth must be a non-negative integer")
    
    # Adds warnings for potential issues
    if len(puzzle['sidings']) > 3:
        warnings.append("More than 3 sidings may make the puzzle too easy")
    if len(puzzle['main_track']) > 5:
        warnings.append("More than 5 trains may make the puzzle too complex")
    
    return PuzzleValidation(len(errors) == 0, errors, warnings)

# Each puzzle is a dict with keys: 'main_track', 'sidings', 'goal_order', 'difficulty', 'expected_depth'
BENCHMARKS: Dict[str, PuzzleConfig] = {
    'easy1': {
        'main_track': ['1', '2', '3'],
        'sidings': [[], []],
        'goal_order': ['1', '2', '3'],
        'difficulty': 'easy',
        'expected_depth': 0
    },
    'easy2': {
        'main_track': ['2', '1', '3'],
        'sidings': [[], []],
        'goal_order': ['1', '2', '3'],
        'difficulty': 'easy',
        'expected_depth': 2
    },
    'medium1': {
        'main_track': ['3', '1', '2'],
        'sidings': [[], []],
        'goal_order': ['1', '2', '3'],
        'difficulty': 'medium',
        'expected_depth': 4
    },
    'medium2': {
        'main_track': ['2', '3', '1'],
        'sidings': [[], [], []],
        'goal_order': ['1', '2', '3'],
        'difficulty': 'medium',
        'expected_depth': 6
    },
    'hard1': {
        'main_track': ['4', '3', '2', '1'],
        'sidings': [[], [], []],
        'goal_order': ['1', '2', '3', '4'],
        'difficulty': 'hard',
        'expected_depth': 8
    },
    'hard2': {
        'main_track': ['2', '4', '1', '3'],
        'sidings': [[], [], []],
        'goal_order': ['1', '2', '3', '4'],
        'difficulty': 'hard',
        'expected_depth': 10
    },
}

def list_benchmarks() -> None:
    """
    Print a formatted list of available benchmark puzzles.
    
    The output includes:
    - Puzzle name
    - Difficulty level
    - Initial state
    - Goal state
    - Expected solution depth
    """
    print("Available Railway Shunting Benchmarks:")
    print("-" * 80)
    
    # Groups puzzles by difficulty
    by_difficulty: Dict[str, List[tuple[str, PuzzleConfig]]] = {
        'easy': [],
        'medium': [],
        'hard': []
    }
    
    for name, puzzle in BENCHMARKS.items():
        by_difficulty[puzzle['difficulty']].append((name, puzzle))
    
    # Prints puzzles by difficulty
    for difficulty in ['easy', 'medium', 'hard']:
        if by_difficulty[difficulty]:
            print(f"\n{difficulty.upper()} PUZZLES:")
            for name, puzzle in sorted(by_difficulty[difficulty]):
                print(f"\n  {name}:")
                print(f"    Initial State: {' → '.join(puzzle['main_track'])}")
                print(f"    Goal State: {' → '.join(puzzle['goal_order'])}")
                print(f"    Expected Depth: {puzzle['expected_depth']} moves")
                print(f"    Sidings: {len(puzzle['sidings'])}")

def get_benchmark(name: str) -> Optional[PuzzleConfig]:
    """
    Get a benchmark puzzle by name.
    
    Args:
        name: Name of the benchmark puzzle
        
    Returns:
        Puzzle configuration if found, None otherwise
    """
    puzzle = BENCHMARKS.get(name)
    if puzzle:
        # Validate the puzzle before returning
        validation = validate_puzzle(puzzle)
        if not validation.is_valid:
            print(f"Warning: Puzzle '{name}' has validation errors:")
            for error in validation.errors:
                print(f"  - {error}")
            for warning in validation.warnings:
                print(f"  - Warning: {warning}")
    return puzzle

def save_benchmarks(filename: str = "benchmarks.json") -> None:
    """
    Save the benchmark puzzles to a JSON file.
    
    Args:
        filename: Name of the file to save to
    """
    try:
        with open(filename, 'w') as f:
            json.dump(BENCHMARKS, f, indent=2)
    except Exception as e:
        print(f"Error saving benchmarks: {str(e)}")

def load_benchmarks(filename: str = "benchmarks.json") -> bool:
    """
    Load benchmark puzzles from a JSON file.
    
    Args:
        filename: Name of the file to load from
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(filename):
            return False
            
        with open(filename, 'r') as f:
            loaded_benchmarks = json.load(f)
            
        # Validates all puzzles
        for name, puzzle in loaded_benchmarks.items():
            validation = validate_puzzle(puzzle)
            if not validation.is_valid:
                print(f"Error: Invalid puzzle '{name}':")
                for error in validation.errors:
                    print(f"  - {error}")
                return False
                
        # Updates the global BENCHMARKS
        global BENCHMARKS
        BENCHMARKS = loaded_benchmarks
        return True
    except Exception as e:
        print(f"Error loading benchmarks: {str(e)}")
        return False 