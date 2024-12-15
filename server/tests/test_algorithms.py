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

def test_unload_nonexistent_container():
   grid = [[-1 for i in range(12)] for j in range(8)]
   # container doesn't exist
   unload_dict = np.zeros(1000, dtype=int)
   unload_dict[999] = 1
   
   # can't be unloaded
   result = loadUnload(grid, unload_dict, 0)
   assert result is None

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