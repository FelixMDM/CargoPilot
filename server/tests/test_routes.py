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

def test_loadUnload_endpoint():
    """Test the balance endpoint"""
    client = app.test_client()
    response = client.get('/loadUnload')
    assert response.status_code == 200

def test_download_logs_endpoint():
    """Test the balance endpoint"""
    client = app.test_client()
    response = client.get('/download-logs')
    assert response.status_code == 200

def test_invalid_log_payload():
    client = app.test_client()
    response = client.post('/log', json={}, content_type='application/json')  # Missing fields
    assert response.status_code == 200  # Accepts incomplete payloads
    assert b"status" in response.data  # Check that it responds with a success message

def test_duplicate_log_messages():
    client = app.test_client()
    test_data = {
        "level": "info",
        "component": "test",
        "message": "test message"
    }
    response1 = client.post('/log', json=test_data, content_type='application/json')
    response2 = client.post('/log', json=test_data, content_type='application/json')
    assert response1.status_code == 200
    assert response2.status_code == 200

def test_large_log_message():
    client = app.test_client()
    large_message = "a" * 10000  # 10,000 characters
    test_data = {
        "level": "info",
        "component": "test",
        "message": large_message
    }
    response = client.post('/log', json=test_data, content_type='application/json')
    assert response.status_code == 200

def test_missing_file_upload():
    client = app.test_client()
    response = client.post('/uploadManifest', content_type='multipart/form-data')  # No file
    assert response.status_code == 500
    assert b"Upload operation failed" in response.data