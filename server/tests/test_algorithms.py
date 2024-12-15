import sys
import os
import numpy as np
import warnings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import hueristicBalance, loadUnload, balance, canBalance

def test_hueristic_balance():
   """Test different balance scenarios with hueristicBalance function"""
   # Test basic equal weight scenario
   balanced_grid = [[0 for _ in range(12)] for _ in range(8)]
   balanced_grid[0][0] = 100  
   balanced_grid[0][11] = 100
   assert hueristicBalance(balanced_grid) == 0

   # Test completely uniform weight distribution
   balanced_grid = [[0 for _ in range(12)] for _ in range(8)]
   for i in range(12):
       balanced_grid[0][i] = 100
   assert hueristicBalance(balanced_grid) == 0
   
   # Test significant weight imbalance
   unbalanced_grid = [[0 for _ in range(12)] for _ in range(8)]
   unbalanced_grid[0][0] = 200  # Double weight on left
   unbalanced_grid[0][11] = 100
   assert hueristicBalance(unbalanced_grid) > 0

   # Test extreme right-side imbalance
   unbalanced_grid = [[0 for _ in range(12)] for _ in range(8)]
   for i in range(11):
       unbalanced_grid[0][i] = 100
   unbalanced_grid[0][11] = 1000  # 10x weight on right
   assert hueristicBalance(unbalanced_grid) > 0

def test_hueristic_balance_alternating_weights():
   """Test balance function with alternating weight patterns"""
   grid = [[0 for _ in range(12)] for _ in range(8)]
   # Set up alternating pattern on left side
   grid[0][0] = 100
   grid[0][1] = 50
   # Create imbalance on right side
   grid[0][6] = 100
   grid[0][7] = 1  # Significant weight difference
   assert hueristicBalance(grid) > 0

def test_hueristic_balance_edge_weights():
   """Test balance function with extreme weight differences"""
   grid = [[0 for _ in range(12)] for _ in range(8)]
   # Test minimum possible weight
   grid[0][0] = 1
   # Test very large weight to check handling of extremes
   grid[0][1] = 10**6
   assert hueristicBalance(grid) > 0

def test_balance():
   """Test balance function with practical container arrangement"""
   test_grid = [[0 for _ in range(12)] for _ in range(8)]
   # Set up initial imbalanced state
   test_grid[0][0] = 50
   test_grid[0][1] = 50  # Total 100 on left
   test_grid[0][6] = 100 # Single 100 on right

   result = balance(test_grid)
   assert result is not None
   cost, final_grid, path = result

   # Calculate final balance state
   left_sum = sum(final_grid[j][i] for j in range(8) for i in range(6))
   right_sum = sum(final_grid[j][i] for j in range(8) for i in range(6, 12))
   
   if left_sum > 0 and right_sum > 0:
       difference = abs(left_sum - right_sum)
       max_weight = max(left_sum, right_sum)
       ratio = difference / max_weight
       assert ratio <= 0.1  # Verify within 10% balance threshold

def test_empty_grid_balance():
   """Test balance function behavior with empty grid"""
   with warnings.catch_warnings():
       warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in scalar divide")
       # Create empty grid and verify no changes needed
       empty_grid = [[0 for _ in range(12)] for _ in range(8)]
       result = balance(empty_grid)
       assert result == (0, empty_grid, [])

def test_balance_large_grid():
   """Test balance function with oversized grid dimensions"""
   # Create grid larger than standard ship dimensions
   large_grid = [[100 for _ in range(24)] for _ in range(16)]
   # Verify algorithm can handle larger dimensions
   result = balance(large_grid)
   assert result is not None

def test_balance_single_container():
   """Test balance function with single container edge case"""
   test_grid = [[-1 for _ in range(12)] for _ in range(8)]
   # Place single container at origin
   test_grid[0][0] = 100
   
   result = balance(test_grid)
   assert result is not None
   cost, final_grid, path = result
   
   # Verify no balancing needed for single container
   assert cost == 0
   assert np.array_equal(final_grid, test_grid)
   assert len(path) == 0

def test_invalid_grid_structure():
   """Test balance function handling of invalid grid dimensions"""
   # Create intentionally malformed grid
   grid = [[-1 for _ in range(6)] for _ in range(4)]
   try:
       result = balance(grid)
       assert False, "Expected exception for malformed grid"
   except IndexError:  
       pass  # Correct error caught

def test_load_unload():
   """Test basic load/unload operation sequence"""
   test_grid = [[-1 for _ in range(12)] for _ in range(8)]
   # Place single container to unload
   test_grid[0][0] = 1
   
   # Set up unload request
   unload_dict = np.zeros(4, dtype=int)
   unload_dict[1] = 1  # Request to unload container ID 1
   
   # Verify successful unload operation
   result = loadUnload(test_grid, unload_dict, 0)
   assert result is not None
   cost, final_grid, path = result
   assert cost >= 0
   assert len(path) > 0

def test_unload_nonexistent_container():
   """Test unload behavior with non-existent container"""
   grid = [[-1 for _ in range(12)] for _ in range(8)]
   # Create unload request for container that doesn't exist
   unload_dict = np.zeros(1000, dtype=int)
   unload_dict[999] = 1  # Request impossible container
   
   # Verify graceful handling of impossible request
   result = loadUnload(grid, unload_dict, 0)
   assert result is None

def test_can_balance():
   """Test canBalance function's weight distribution analysis"""
   # Create balanced initial state
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

   # Test detection of significant imbalance
   test_grid[1][0] = 200  # Double weight on left side
   result, _, _ = canBalance(test_grid)
   assert result == False