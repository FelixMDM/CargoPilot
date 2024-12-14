import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import canBalance

def test_basic_addition():
    """Most basic test to verify pytest is working"""
    x = 1
    y = 2
    assert x + y == 3

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