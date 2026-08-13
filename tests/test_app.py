import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the root endpoint returns correct message and HTTP 200"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Harness Cloud Delivery Demo"
    assert data["platform"] == "Harness Cloud CI/CD"


def test_health_endpoint(client):
    """Test health check returns healthy status for Harness deployment verification"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["checks"]["uptime"] == "ok"


def test_version_endpoint(client):
    """Test version endpoint returns application version metadata"""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert "commit" in data
