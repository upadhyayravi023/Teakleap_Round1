from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch
from mongomock_motor import AsyncMongoMockClient

@pytest.fixture(scope="function", autouse=True)
def mock_mongo():
    mock_client = AsyncMongoMockClient()
    # Inject Mock Client explicitly where lifespan utilizes it
    with patch("app.main.AsyncIOMotorClient", return_value=mock_client):
        yield

@pytest.fixture(scope="function")
def client(mock_mongo):
    with TestClient(app) as c:
        yield c

def test_create_candidate(client):
    response = client.post("/candidates", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "skill": "Python",
        "status": "applied"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert "id" in data

def test_create_candidate_invalid_email(client):
    response = client.post("/candidates", json={
        "name": "Invalid Email",
        "email": "not-an-email",
        "skill": "Python",
        "status": "applied"
    })
    assert response.status_code == 422 # Invalid Data

def test_create_candidate_invalid_status(client):
    response = client.post("/candidates", json={
        "name": "Invalid Status",
        "email": "valid@example.com",
        "skill": "Python",
        "status": "hired" # not in the enum
    })
    assert response.status_code == 422

def test_get_all_candidates(client):
    client.post("/candidates", json={
        "name": "Alice",
        "email": "alice@example.com",
        "skill": "Go",
        "status": "interview"
    })
    response = client.get("/candidates")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_candidates_filtered_by_status(client):
    client.post("/candidates", json={
        "name": "Bob Filter",
        "email": "bob.filter@example.com",
        "skill": "Java",
        "status": "interview"
    })
    response = client.get("/candidates?status=interview")
    assert response.status_code == 200
    for cand in response.json():
        assert cand["status"] == "interview"

def test_update_candidate_status(client):
    create_res = client.post("/candidates", json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "skill": "Java",
        "status": "applied"
    })
    c_id = create_res.json()["id"]

    update_res = client.put(f"/candidates/{c_id}/status", json={
        "status": "interview"
    })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "interview"

def test_update_non_existent_candidate(client):
    update_res = client.put("/candidates/507f1f77bcf86cd799439011/status", json={
        "status": "rejected"
    })
    assert update_res.status_code == 404
