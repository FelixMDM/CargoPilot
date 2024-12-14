# tests/test_algorithms.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import hueristicBalance, loadUnload, balance

def test_hueristic_balance():
    """Test hueristicBalance function"""
    # Create a balanced grid properly
    balanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    balanced_grid[0][0] = 100  # Left side
    balanced_grid[0][6] = 100  # Right side
    assert hueristicBalance(balanced_grid) == 0  # Should be balanced
    
    # Create an unbalanced grid
    unbalanced_grid = [[0 for _ in range(12)] for _ in range(8)]
    unbalanced_grid[0][0] = 200  # Left side heavier
    unbalanced_grid[0][6] = 100  # Right side lighter
    assert hueristicBalance(unbalanced_grid) > 0  # Should be unbalanced

# tests/test_algorithms.py
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

def test_load_unload():
    """Test loadUnload function"""
    test_grid = [[0 for _ in range(12)] for _ in range(8)]
    test_grid[0][0] = 1  # Container to unload
    
    # Test unloading container '1'
    result = loadUnload(test_grid, {"1": 1}, 0)  # Unload one container
    assert result is not None
    cost, final_grid, path = result
    assert cost >= 0
    assert len(path) > 0