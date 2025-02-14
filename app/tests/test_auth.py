import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pymongo.collection import Collection

# from app.tests.config import get_test_db, client


# MongoDB test config
TEST_DATABASE_URL = "mongodb://localhost:27017/"
TEST_DB_NAME = "fastapi_test_db"


# Test version of get_db using AsyncIOMotorClient
@pytest_asyncio.fixture
async def get_test_db():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    db = client[TEST_DB_NAME]
    try:
        yield db
    finally:
        client.close()


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(get_test_db):
    """Fixture to override FastAPI's get_db dependency for all tests."""
    test_db = get_test_db
    app.dependency_overrides[get_db] = lambda: test_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_signup_success(client, get_test_db):
    """Test successful user signup."""
    user_data = {
        "email": "bssqews@mail.com",
        "password": "12wsess3",
        "username": "aswwewswsdss8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 201
    db = get_test_db

    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"email": user_data["email"]})
    response_data = response.json()
    assert response_data["message"] == "User account created successfully."


@pytest.mark.asyncio
async def test_signup_duplicate_username(client, get_test_db):
    """Test signup with a duplicate username."""
    user_data = {
        "username": "tesdsstuser",
        "email": "testusse232rs1@example.com",
        "password": "securepassword123",
    }

    user_data_duplicate_username = {
        "username": "tesdsstuser",
        "email": "testudsqser@example.com",
        "password": "securepassword123",
    }

    response = await client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 201

    response = await client.post(
        "/api/v1/auth/signup", json=user_data_duplicate_username
    )
    assert response.status_code == 409

    db = get_test_db
    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"username": user_data["username"]})


@pytest.mark.asyncio
async def test_signup_duplicate_email(client, get_test_db):
    """Test signup with a duplicate email."""
    user_data1 = {
        "username": "testuser1",
        "email": "testuser@example.com",
        "password": "securepassword123",
    }
    user_data2 = {
        "username": "testuser2",
        "email": "testuser@example.com",
        "password": "securepassword123",
    }

    response = await client.post("/api/v1/auth/signup", json=user_data1)
    assert response.status_code == 201

    response = await client.post("/api/v1/auth/signup", json=user_data2)
    assert response.status_code == 409

    db = get_test_db
    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"email": user_data1["email"]})


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
