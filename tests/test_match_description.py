from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_match_description_valid():
    response = client.post("/semantic/match_description", json={"query": "Transfer from Emma Brown"})
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert "total_number_of_tokens_used" in data

def test_match_description_empty():
    response = client.post("/semantic/match_description", json={"query": ""})
    assert response.status_code == 400