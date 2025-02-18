import pytest
from httpx import AsyncClient
from pymongo.collection import Collection


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient, get_test_db):

    user_data = {
        "email": "bssqews@mail.com",
        "password": "12wsess3",
        "username": "aswwewswsdss8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 201
    db = get_test_db
    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"email": user_data["email"]})


@pytest.mark.asyncio
async def test_signup_duplicate_username(client, get_test_db, test_user):

    user_data_duplicate_username = {
        "username": test_user["username"],
        "email": "testudsqser@example.com",
        "password": "securepassword123",
    }

    response = await client.post(
        "/api/v1/auth/signup", json=user_data_duplicate_username
    )
    assert response.status_code == 409
    response_data = response.json()
    assert (
        response_data["detail"]["message"] == "User already exists with this username"
    )


@pytest.mark.asyncio
async def test_signup_duplicate_email(client, get_test_db, test_user):
    """Test signup with a duplicate email."""

    user_data2 = {
        "username": "testuser2",
        "email": test_user["email"],
        "password": "securepassword123",
    }

    response = await client.post("/api/v1/auth/signup", json=user_data2)
    assert response.status_code == 409
    response_data = response.json()
    assert response_data["detail"] == "User already exists with this email"


@pytest.mark.asyncio
async def test_signup_invalid_data(client, get_test_db):
    """Test signup with invalid data."""
    user_data = {"username": "testuser"}
    response = await client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 422

    user_data = {"username": "testuser", "password": "testpass"}
    response = await client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 422

    user_data = {"username": "testuser", "email": "tdestpass"}
    response = await client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 422

    user_data = {
        "username": "testuser",
        "email": "tdestpass",
        "password": "newpassword",
    }
    response = await client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_admin_signup(client, get_test_db):
    user_data = {
        "email": "bssqews@mail.com",
        "password": "12wsess3",
        "username": "aswwewswsdss8",
    }

    response = await client.post("/api/v1/auth/admin/signup", json=user_data)

    assert response.status_code == 201
    db = get_test_db
    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"email": user_data["email"]})
