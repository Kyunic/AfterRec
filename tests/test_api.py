from fastapi.testclient import TestClient

from recforgetbench.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_capabilities_do_not_claim_real_models():
    response = client.get("/api/v1/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["production_experiments_available"] is False
    assert all(item["status"] != "ready" for item in data["components"])
