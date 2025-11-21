import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # First, sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again (should fail)
    response2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response2.status_code == 404
