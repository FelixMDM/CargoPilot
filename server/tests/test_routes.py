# tests/test_routes.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from server import app

def test_log_endpoint():
    """Test the log endpoint"""
    client = app.test_client()
    test_data = {
        "level": "info",
        "component": "test",
        "message": "test message"
    }
    response = client.post('/log', 
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 200

def test_test_endpoint():
    """Test the test endpoint"""
    client = app.test_client()
    response = client.get('/test')
    assert response.status_code == 200
    assert b'message' in response.data

def test_balance_endpoint():
    """Test the balance endpoint"""
    client = app.test_client()
    response = client.get('/balance')
    assert response.status_code == 200