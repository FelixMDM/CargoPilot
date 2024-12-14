import sys
import os
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

#def test_single_container_balance():
#    """Test balance function with a single container"""
#    grid = [[0 for _ in range(12)] for _ in range(8)]
#    grid[0][0] = 100
#    result = balance(grid)
#    assert result is not None
#    cost, final_grid, path = result
#    assert cost == 0  # Already balanced

def test_balance_large_grid():
    large_grid = [[100 for _ in range(24)] for _ in range(16)]  # 16x24 grid
    result = balance(large_grid)
    assert result is not None

# def test_invalid_grid_structure():
#     malformed_grid = [[100, 0], [0, 0, 100]]  # Rows have different lengths
#     try:
#         result = balance(malformed_grid)
#         assert False, "Expected exception for malformed grid"
#     except Exception as e:
#         assert isinstance(e, ValueError) or isinstance(e, IndexError)

# def test_load_unload():
#     test_grid = [[0 for _ in range(12)] for _ in range(8)]
#     test_grid[0][0] = 1  # Container to unload
    
#     # Ensure that the unload dictionary is checked for the key before unloading
#    unload_dict = {"1": 1}  # Unload one container
#    if str(test_grid[0][0]) in unload_dict:  # Convert to str if keys are stored as strings
#         result = loadUnload(test_grid, unload_dict, 0)
#         assert result is not None
#         cost, final_grid, path = result
#         assert cost >= 0
#         assert len(path) > 0
#     else:
#         assert False, "Unload dictionary does not contain the key for the container to be unloaded."

# def test_unload_nonexistent_container():
#     grid = [[0 for _ in range(12)] for _ in range(8)]
#     result = loadUnload(grid, {"999": 1}, 0)  # Unload non-existent container ID
#     assert result is None  # Should handle it gracefully, expecting None or similar return

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
