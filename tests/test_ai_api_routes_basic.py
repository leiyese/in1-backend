import pytest
import json

# Uses the 'client' fixture from conftest.py


def test_ai_api_call_wrong_method(client):
    """Test GET request fails for the endpoint."""
    response = client.get("/ai_model")
    assert response.status_code == 405


def test_ai_api_call_no_json(client):
    """Test request without JSON content type."""
    response = client.post("/ai_model", data="plain text")
    assert response.status_code == 415


def test_ai_api_call_empty_json(client):
    """Test request with empty JSON object."""
    response = client.post("/ai_model", json={})
    assert response.status_code >= 400


def test_ai_api_call_missing_model_type(client):
    """Test request missing the model_type field."""
    response = client.post("/ai_model", json={"prompt": "test", "system": "test"})
    assert response.status_code >= 400


def test_ai_api_call_missing_prompt(client):
    """Test request missing the prompt field."""
    response = client.post("/ai_model", json={"model_type": "gemini", "system": "test"})
    assert response.status_code >= 400
