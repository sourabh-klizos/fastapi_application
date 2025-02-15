import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import get_db
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pymongo.collection import Collection
import os
from typing import Dict


@pytest.mark.asyncio
async def test_login_success(
    client: AsyncClient, get_test_db: AsyncIOMotorClient, test_user: dict
) -> None:

    login_payload = {"email": test_user["email"], "password": test_user["password"]}
    login_response = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    json_data = login_response.json()
    assert "access_token" in json_data and "refresh_token" in json_data


@pytest.mark.asyncio
async def test_login_with_wrong_credentials(
    client: AsyncClient, get_test_db: AsyncIOMotorClient, test_user: Dict[str, str]
):

    login_payload = {
        "email": "example12334@gmail.com",
        "password": test_user["password"],
    }
    login_response = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 401

    login_response_json = login_response.json()

    assert login_response_json.get("detail") == "Incorrect email or password"

    login_payload = {"email": test_user["email"], "password": "wrongpassword"}
    login_response = await client.post("/api/v1/auth/login", json=login_payload)

    assert login_response.status_code == 401

    login_response_json = login_response.json()

    assert login_response_json.get("detail") == "Incorrect email or password"
