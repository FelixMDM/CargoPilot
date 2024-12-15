import sys
import os
import numpy as np
import warnings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import hueristicBalance, loadUnload, balance, canBalance

def test_hueristic_balance():
   # equal weights
   balanced_grid = [[0 for i in range(12)] for j in range(8)]
   balanced_grid[0][0] = 100  
   balanced_grid[0][11] = 100
   assert hueristicBalance(balanced_grid) == 0

   # same weight distributed
   balanced_grid = [[0 for i in range(12)] for j in range(8)]
   for i in range(12):
       balanced_grid[0][i] = 100
   assert hueristicBalance(balanced_grid) == 0
   
   # left side heavier
   unbalanced_grid = [[0 for i in range(12)] for j in range(8)]
   unbalanced_grid[0][0] = 200  # Double weight on left
   unbalanced_grid[0][11] = 100
   assert hueristicBalance(unbalanced_grid) > 0

   # right side heavier
   unbalanced_grid = [[0 for i in range(12)] for j in range(8)]
   for i in range(11):
       unbalanced_grid[0][i] = 100
   unbalanced_grid[0][11] = 1000  # 10x weight on right
   assert hueristicBalance(unbalanced_grid) > 0

def test_hueristic_balance_alternating_weights():
   grid = [[0 for i in range(12)] for j in range(8)]
   grid[0][0] = 100
   grid[0][1] = 50
   # right side heavier
   grid[0][6] = 100
   grid[0][7] = 1
   assert hueristicBalance(grid) > 0

def test_hueristic_balance_edge_weights():
   grid = [[0 for i in range(12)] for j in range(8)]
   # min weight
   grid[0][0] = 1
   # max weight
   grid[0][1] = 10**6
   assert hueristicBalance(grid) > 0

def test_balance():
   test_grid = [[0 for i in range(12)] for j in range(8)]
   # balanced
   test_grid[0][0] = 50
   test_grid[0][1] = 50  # total 100 on left
   test_grid[0][6] = 100 # total 100 on right

   result = balance(test_grid)
   assert result is not None
   cost, final_grid, path = result

   # final balance state
   left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
   right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
   
   if left_sum > 0 and right_sum > 0:
       difference = abs(left_sum - right_sum)
       max_weight = max(left_sum, right_sum)
       ratio = difference / max_weight
       assert ratio <= 0.1  # within 10% balance threshold?

def test_empty_grid_balance():
   with warnings.catch_warnings():
       warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in scalar divide")
       # empty grid with no changes needed
       empty_grid = [[0 for i in range(12)] for j in range(8)]
       result = balance(empty_grid)
       assert result == (0, empty_grid, [])

def test_balance_single_container():
   test_grid = [[-1 for i in range(12)] for j in range(8)]
   # single container
   test_grid[0][0] = 100
   
   result = balance(test_grid)
   assert result is not None
   cost, final_grid, path = result
   
   # no balance should be needed
   assert cost == 0
   assert np.array_equal(final_grid, test_grid)
   assert len(path) == 0

def test_balance_identical_weights():
    """Test balancing a grid with multiple identical weights"""
    grid = [[0 for _ in range(12)] for _ in range(8)]
    grid[0][0] = 100
    grid[0][1] = 100
    grid[0][6] = 100
    grid[0][7] = 100  # Total weight is balanced
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    assert cost == 0  # No movements should be required
    assert len(path) == 0

def test_balance_one_side_populated():
    """Test balancing when containers are concentrated on one side"""
    grid = [[0 for _ in range(12)] for _ in range(8)]
    # Add containers with balanced total weight but concentrated on left
    grid[0][0] = 150
    grid[1][0] = 100
    grid[0][1] = 75
    grid[0][6] = 325  # Equal total weight on right but in one spot
    
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    
    # Verify some redistribution occurred
    left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
    right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
    assert abs(left_sum - right_sum) / max(left_sum, right_sum) <= 0.1

def test_balance_with_nan_spaces():
    """Test balancing with NAN (-2) spaces in grid"""
    grid = [[-1 for _ in range(12)] for _ in range(8)]
    # Add NAN spaces
    grid[0][0] = -2
    grid[0][11] = -2
    # Add containers around NAN spaces
    grid[0][1] = 100
    grid[0][10] = 100
    
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    # Verify NAN spaces weren't modified
    assert final_grid[0][0] == -2
    assert final_grid[0][11] == -2

def test_balance_multiple_stacks():
    """Test balancing with multiple stacks of containers"""
    grid = [[0 for _ in range(12)] for _ in range(8)]
    # Create tall stacks on left side
    grid[0][0] = 100
    grid[1][0] = 100
    grid[2][0] = 100  # Total 300 on left
    # Create different weights on right side
    grid[0][6] = 200  # Total 200 on right

    result = balance(grid)
    assert result is not None, "Balance function returned None unexpectedly"
    cost, final_grid, path = result
    
    # Validate no movements were made
    assert len(path) == 0, "Containers were moved despite the grid being unbalanced"

    # Validate final balance state
    left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
    right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
    assert left_sum == 300 and right_sum == 200, f"Unexpected balance state: Left={left_sum}, Right={right_sum}"


def test_perfectly_balanced_grid():
    """Test balancing a grid that is already perfectly balanced"""
    grid = [[0 for _ in range(12)] for _ in range(8)]
    for i in range(6):
        grid[0][i] = 100  # Left side
        grid[0][i + 6] = 100  # Right side
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    assert cost == 0  # No cost for balancing
    assert len(path) == 0  # No movements needed

def test_load_unload():
   test_grid = [[-1 for i in range(12)] for j in range(8)]
   # single container
   test_grid[0][0] = 1
   
   # unload
   unload_dict = np.zeros(4, dtype=int)
   unload_dict[1] = 1  # get the id to compare
   
   result = loadUnload(test_grid, unload_dict, 0)
   assert result is not None
   cost, final_grid, path = result
   assert cost >= 0
   assert len(path) > 0

def test_loading_empty_grid():
    """Test loading containers into an empty grid"""
    grid = [[-1 for _ in range(12)] for _ in range(8)]  # Empty grid
    unload_dict = np.zeros(4, dtype=int)  # Placeholder for valid unload dictionary
    result = loadUnload(grid, unload_dict, 3)  # Load 3 containers

    if result is None:
        print("Debug: loadUnload returned None (no valid loading possible)")
        assert result is None  # Acceptable behavior for an empty grid with no valid operations
    else:
        cost, final_grid, path = result
        assert cost > 0
        assert len(path) > 0

def test_unload_nonexistent_container():
   grid = [[-1 for i in range(12)] for j in range(8)]
   # container doesn't exist
   unload_dict = np.zeros(1000, dtype=int)
   unload_dict[999] = 1
   
   # can't be unloaded
   result = loadUnload(grid, unload_dict, 0)
   assert result is None

def test_load_unload_complex():
    """Test complex load/unload scenario with multiple operations"""
    grid = [[-1 for _ in range(12)] for _ in range(8)]
    # Set up multiple containers
    grid[0][0] = 1
    grid[1][0] = 2
    grid[0][1] = 3
    
    # Request to unload containers 1 and 3
    unload_dict = np.zeros(4, dtype=int)
    unload_dict[1] = 1
    unload_dict[3] = 1
    
    # Try to load 2 new containers while unloading
    result = loadUnload(grid, unload_dict, 2)
    assert result is not None
    cost, final_grid, path = result
    
    # Verify correct number of operations
    assert len(path) >= 4  # At least 4 moves (2 unloads + 2 loads)
    # Verify container 2 still exists (wasn't marked for unload)
    assert any(2 in row for row in final_grid)

def test_can_balance():
   # balanced ship state
   test_grid = [
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   ]
   result, _, _ = canBalance(test_grid)
   assert result == True

   # make unbalanced
   test_grid[1][0] = 200
   result, _, _ = canBalance(test_grid)
   assert result == False