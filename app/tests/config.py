from app.main import app
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from httpx import AsyncClient, ASGITransport


TEST_DATABASE_URL = "mongodb://localhost:27017/"
TEST_DB_NAME = "fastapi_test_db"


@pytest_asyncio.fixture
async def get_test_db():
    """Fixture to provide a test database."""
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    db = client[TEST_DB_NAME]
    try:
        yield db  # ✅ Correctly yielding the database instance
    finally:
        client.close()


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(get_test_db):
    """Fixture to override FastAPI's get_db dependency globally."""
    test_db = await get_test_db  # ✅ Await to get the actual database instance
    app.dependency_overrides[get_db] = (
        lambda: test_db
    )  # ✅ Now it properly injects the instance
    yield
    app.dependency_overrides.clear()  # ✅ Clean up after tests


@pytest_asyncio.fixture
async def client():
    """Fixture to create an async HTTP client for testing."""
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client
