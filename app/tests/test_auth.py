import pytest
from fastapi.testclient import TestClient
# from main import app, fake_db

from app.main import app
from typing import Dict


fake_db: Dict[str, dict] = {}

class TestSignup:
    @pytest.fixture(autouse=True)
    def clear_db(self):
        """Fixture to clear the fake_db before each test."""
        fake_db.clear()

    @pytest.fixture
    def client(self):
        """Fixture to provide a test client."""
        with TestClient(app) as client:
            yield client

    def test_signup_success(self, client):
        """Test successful user signup."""
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        response = client.post("/api/v1/auth/signup", json=user_data)
        assert response.status_code == 201
        response_data = response.json()
        
        assert response_data["message"] == "User account created successfully."

    def test_signup_duplicate_username(self, client):
        """Test signup with a duplicate username."""
        user_data = {
            "username": "testuser",
            "email": "testuser1@example.com",
            "password": "securepassword123"
        }
        # First signup should succeed
        response = client.post("/api/v1/auth/signup", json=user_data)
        assert response.status_code == 404

        # Second signup with the same username should fail
        response = client.post("/api/v1/auth/signup", json=user_data)
        assert response.json()["detail"]['message'] ==  "User already exists with this username"
        assert response.status_code == 404

    def test_signup_duplicate_email(self, client):
        """Test signup with a duplicate email."""
        user_data1 = {
            "username": "testuser1",
            "email": "t1estuser@example.com",
            "password": "securepassword123"
        }
        user_data2 = {
            "username": "testuser2",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        # First signup should succeed
        response = client.post("/signup", json=user_data1)
        assert response.status_code == 200

        # Second signup with the same email should fail
        response = client.post("/signup", json=user_data2)
        assert response.status_code == 400
  
        assert response.json()["detail"] == "User already exists with this email"

    def test_signup_invalid_data(self, client):
        """Test signup with invalid or incomplete data."""
        user_data = {
            "username": "testuser",
            # Missing email and password
        }
        response = client.post("/signup", json=user_data)
        assert response.status_code == 422  # Unprocessable Entity