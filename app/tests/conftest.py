import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from app.main import app
from app.database.db import get_db
from typing import Dict

from httpx import ASGITransport


TEST_DATABASE_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_db"


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
    app.dependency_overrides[get_db] = lambda: get_test_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    """Fixture to provide an HTTPX client for API testing."""
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def test_user(client: AsyncClient, get_test_db: AsyncIOMotorClient):
    """Fixture to create and clean up a test user."""
    payload = {
        "email": "test@gmail.com",
        "password": "test1234",
        "username": "test_sourabh",
    }
    response = await client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    yield payload

    db = get_test_db
    user_collection: Collection = db["users"]
    await user_collection.find_one_and_delete({"email": payload["email"]})


@pytest_asyncio.fixture
async def get_current_user_token(test_user: Dict[str, str], client: AsyncClient):
    login_payload = {"email": test_user["email"], "password": test_user["password"]}
    login_response = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    json_data = login_response.json()
    assert "access_token" in json_data and "refresh_token" in json_data

    yield json_data


# from app.tests.config import get_test_db, client


# TEST_DATABASE_URL = "mongodb://localhost:27017/"
# TEST_DB_NAME = "fastapi_test_db"

# TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
# TEST_DB_NAME = os.getenv("TEST_DB_NAME")


# @pytest_asyncio.fixture
# async def get_test_db():
#     client = AsyncIOMotorClient(TEST_DATABASE_URL)
#     db = client[TEST_DB_NAME]
#     try:
#         yield db
#     finally:
#         client.close()


# @pytest_asyncio.fixture(autouse=True)
# async def override_get_db(get_test_db):
#     """Fixture to override FastAPI's get_db dependency for all tests."""
#     test_db = get_test_db
#     app.dependency_overrides[get_db] = lambda: test_db
#     yield
#     app.dependency_overrides.clear()


# @pytest_asyncio.fixture
# async def client():
#     async with AsyncClient(
#         transport=ASGITransport(app), base_url="http://test"
#     ) as client:
#         yield client
