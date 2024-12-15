import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import hueristicBalance, loadUnload, balance, canBalance

def test_hueristic_balance():
    """Test hueristicBalance function"""
    # Create a balanced grid properly
    balanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    balanced_grid[0][0] = 100  # 100 on left side
    balanced_grid[0][11] = 100  # 100 on right side
    assert hueristicBalance(balanced_grid) == 0  # Should be balanced

    # Create a balanced grid properly
    balanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    balanced_grid[0][0] = 100
    balanced_grid[0][1] = 100
    balanced_grid[0][2] = 100
    balanced_grid[0][3] = 100
    balanced_grid[0][4] = 100
    balanced_grid[0][5] = 100
    balanced_grid[0][6] = 100
    balanced_grid[0][7] = 100
    balanced_grid[0][8] = 100
    balanced_grid[0][9] = 100
    balanced_grid[0][10] = 100
    balanced_grid[0][11] = 100
    assert hueristicBalance(balanced_grid) == 0  # Should be balanced
    
    # Create an unbalanced grid
    unbalanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    unbalanced_grid[0][0] = 200  # Left side heavier
    unbalanced_grid[0][11] = 100  # Right side lighter
    assert hueristicBalance(unbalanced_grid) > 0  # Should be unbalanced

    # Create a balanced grid properly
    unbalanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    unbalanced_grid[0][0] = 100
    unbalanced_grid[0][1] = 100
    unbalanced_grid[0][2] = 100
    unbalanced_grid[0][3] = 100
    unbalanced_grid[0][4] = 100
    unbalanced_grid[0][5] = 100
    unbalanced_grid[0][6] = 100
    unbalanced_grid[0][7] = 100
    unbalanced_grid[0][8] = 100
    unbalanced_grid[0][9] = 100
    unbalanced_grid[0][10] = 100
    unbalanced_grid[0][11] = 1000
    assert hueristicBalance(unbalanced_grid) > 0  # Should be unbalanced (right is heavier)

def test_hueristic_balance_alternating_weights():
    grid = [[0 for _ in range(12)] for _ in range(8)]
    grid[0][0] = 100
    grid[0][1] = 50  # Increase weight on the left
    grid[0][6] = 100
    grid[0][7] = 1   # Smaller weight on the right
    assert hueristicBalance(grid) > 0  # Should detect imbalance

def test_hueristic_balance_edge_weights():
    grid = [[0 for _ in range(12)] for _ in range(8)]
    grid[0][0] = 1  # Minimum weight
    grid[0][1] = 10**6  # Maximum weight
    assert hueristicBalance(grid) > 0  # Should handle extreme weights

def test_balance():
    """Test balance function"""
    # Create a grid with unbalanced but movable containers
    test_grid = [[0 for _ in range(12)] for _ in range(8)]
    # Put two containers on the left side
    test_grid[0][0] = 50
    test_grid[0][1] = 50
    # Put one container on the right side with equal total weight
    test_grid[0][6] = 100

    result = balance(test_grid)
    assert result is not None
    cost, final_grid, path = result

    # Sum up weights on each side
    left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
    right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
    
    # If both sides have weight, check balance
    if left_sum > 0 and right_sum > 0:
        difference = abs(left_sum - right_sum)
        max_weight = max(left_sum, right_sum)
        ratio = difference / max_weight
        print(f"Left sum: {left_sum}, Right sum: {right_sum}, Ratio: {ratio}")
        assert ratio <= 0.1  # Should be within 10%

def test_empty_grid_balance():
    """Test balance function with an empty grid"""
    empty_grid = [[0 for _ in range(12)] for _ in range(8)]
    result = balance(empty_grid)
    assert result == (0, empty_grid, []) 

def test_balance_large_grid():
    large_grid = [[100 for _ in range(24)] for _ in range(16)]  # 16x24 grid
    result = balance(large_grid)
    assert result is not None

def test_invalid_grid_structure():
    # Test with invalid grid dimensions
    grid = [[-1 for _ in range(6)] for _ in range(4)]  # Wrong dimensions
    try:
        result = balance(grid)
        assert False, "Expected exception for malformed grid"
    except IndexError:  # Your code raises IndexError for invalid dimensions
        pass  # Test passes if IndexError is raised

def test_load_unload():
    test_grid = [[-1 for _ in range(12)] for _ in range(8)]  # Initialize with -1 for UNUSED
    test_grid[0][0] = 1  # Container with ID 1 to unload
    
    # Create unload dictionary for container ID 1
    unload_dict = np.zeros(4, dtype=int)  # Match the format in main()
    unload_dict[1] = 1  # Unload one container with ID 1
    
    result = loadUnload(test_grid, unload_dict, 0)  # No containers to load
    assert result is not None
    cost, final_grid, path = result
    assert cost >= 0
    assert len(path) > 0

def test_unload_nonexistent_container():
    grid = [[-1 for _ in range(12)] for _ in range(8)]  # Initialize with UNUSED
    # Create unload dictionary with numpy array
    unload_dict = np.zeros(1000, dtype=int)  # Large enough to hold index 999
    unload_dict[999] = 1  # Try to unload non-existent container
    
    result = loadUnload(grid, unload_dict, 0)
    # Since there are no containers to unload and the requested container doesn't exist,
    # the function should return None
    assert result is None

def test_can_balance():
    """Test the canBalance function with a simple grid"""
    test_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0],  # Equal weights on both sides
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    result, _, _ = canBalance(test_grid)
    assert result == True

    # Test unbalanced grid
    test_grid[1][0] = 200  # Make left side heavier
    result, _, _ = canBalance(test_grid)
    assert result == False
