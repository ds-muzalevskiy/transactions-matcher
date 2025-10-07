from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_match_transaction_valid():
    response = client.get("/transactions/match/RAZbbmLX")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total_number_of_matches" in data

def test_match_transaction_invalid():
    response = client.get("/transactions/match/INVALID")
    assert response.status_code == 404