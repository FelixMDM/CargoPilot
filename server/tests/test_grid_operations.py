# tests/test_grid_operations.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import manifestToGrid
from read_manifest import Container

def test_manifest_to_grid():
    """Test manifestToGrid function"""
    # Create a simple test grid with Container objects
    test_containers = [[Container("NAN", 0) for _ in range(12)] for _ in range(8)]
    
    # Set test values
    test_containers[0][0] = Container("NAN", 0)
    test_containers[0][1] = Container("UNUSED", 0)
    test_containers[0][2] = Container("Test", 100)
    
    # Debug prints
    print(f"Container [0][2] name: {test_containers[0][2].get_name()}")
    print(f"Container [0][2] weight: {test_containers[0][2].get_weight()}")
    
    numerical_grid = manifestToGrid(test_containers)
    
    # Debug prints
    print(f"Numerical grid [0][2]: {numerical_grid[0][2]}")
    
    # Check grid values
    assert numerical_grid[0][0] == -1  # NAN becomes -1
    assert numerical_grid[0][1] == -1  # UNUSED becomes -1
    assert numerical_grid[0][2] == 100  # Regular container shows weight