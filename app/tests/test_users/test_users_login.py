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
async def test_get_users(client:AsyncClient , get_current_user_token: Dict[str, str]):
    tokens = get_current_user_token
    headers = {
        "Authorization" : "Bearer" +" "+ tokens["access_token"]
    }

    response = await client.get("/api/v1/auth/users", headers=headers)
    assert response.status_code == 200
    print(response)