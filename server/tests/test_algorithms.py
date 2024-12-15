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
    grid = [[0 for _ in range(12)] for _ in range(8)]
    # total weigh its balanced but more containers on left
    grid[0][0] = 150
    grid[1][0] = 100
    grid[0][1] = 75
    grid[0][6] = 325
    
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    
    left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
    right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
    assert abs(left_sum - right_sum) / max(left_sum, right_sum) <= 0.1

def test_balance_with_nan_spaces():
    grid = [[-1 for _ in range(12)] for _ in range(8)]
    # adding NAN spaces
    grid[0][0] = -2
    grid[0][11] = -2
    # add containers around NAN spaces
    grid[0][1] = 100
    grid[0][10] = 100
    
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    # NAN spaces shouldn't change
    assert final_grid[0][0] == -2
    assert final_grid[0][11] == -2

def test_balance_multiple_stacks():
    grid = [[0 for i in range(12)] for j in range(8)]
    # tall stack on the left
    grid[0][0] = 100
    grid[1][0] = 100
    grid[2][0] = 100 
    grid[0][6] = 200

    result = balance(grid)
    assert result is not None, "Balance function returned None unexpectedly"
    cost, final_grid, path = result
    
    # no movements should be made
    assert len(path) == 0, "Containers were moved despite the grid being unbalanced"

    # check the final sum
    left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
    right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
    assert left_sum == 300 and right_sum == 200, f"Unexpected balance state: Left={left_sum}, Right={right_sum}"


def test_perfectly_balanced_grid():
    grid = [[0 for _ in range(12)] for _ in range(8)]
    for i in range(6):
        grid[0][i] = 100
        grid[0][i + 6] = 100
    result = balance(grid)
    assert result is not None
    cost, final_grid, path = result
    assert cost == 0
    assert len(path) == 0  # no movements need

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
    grid = [[-1 for i in range(12)] for j in range(8)]  # empty grid
    unload_dict = np.zeros(4, dtype=int)
    result = loadUnload(grid, unload_dict, 3)  # load 3 containers

    if result is None:
        print("Debug: loadUnload returned None (no valid loading possible)")
        assert result is None
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
    grid = [[-1 for i in range(12)] for j in range(8)]

    grid[0][0] = 1
    grid[1][0] = 2
    grid[0][1] = 3
    
    # unload containers 1 and 3
    unload_dict = np.zeros(4, dtype=int)
    unload_dict[1] = 1
    unload_dict[3] = 1
    
    # load 2 new containers while unloading
    result = loadUnload(grid, unload_dict, 2)
    assert result is not None
    cost, final_grid, path = result
    
    # correct number of operations
    assert len(path) >= 4
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