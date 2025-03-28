import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_process_revit_query():
    test_data = {
        "prompt": "Analyze this wall structure",
        "revit_elements": {
            "walls": [
                {
                    "id": 1,
                    "type": "Basic Wall",
                    "length": 10.0,
                    "height": 3.0
                }
            ]
        },
        "project_info": {
            "project_name": "Test Project",
            "project_number": "123"
        }
    }
    
    response = client.post("/process_revit_query", json=test_data)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "suggested_actions" in response.json()

def test_invalid_request():
    test_data = {
        "prompt": ""  # Empty prompt should be invalid
    }
    
    response = client.post("/process_revit_query", json=test_data)
    assert response.status_code == 422  # Validation error 