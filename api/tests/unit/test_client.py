import pytest

def test_example(client):
    response = client.get("/api/lessons")
    assert response.status_code == 200
