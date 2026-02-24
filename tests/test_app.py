import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "description" in data["Basketball"]
    assert "participants" in data["Basketball"]

def test_signup_successful():
    response = client.post("/activities/Basketball/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@example.com for Basketball" in data["message"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Tennis Club/signup", params={"email": "duplicate@example.com"})
    # Try again
    response = client.post("/activities/Tennis Club/signup", params={"email": "duplicate@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_successful():
    # First signup
    client.post("/activities/Art Studio/signup", params={"email": "unregister@example.com"})
    # Then unregister
    response = client.delete("/activities/Art Studio/unregister", params={"email": "unregister@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@example.com from Art Studio" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Drama Club/unregister", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent Activity/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]