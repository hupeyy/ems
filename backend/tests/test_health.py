from fastapi.testclient import TestClient
from app.main import app

def test_health_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_endpoint_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_endpoint_returns_json_content_type():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

