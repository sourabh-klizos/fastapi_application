import pytest
from httpx import AsyncClient
from pymongo.collection import Collection
from typing import Dict


@pytest.mark.asyncio
async def test_get_trash_with_admin_user(
    client: AsyncClient, get_admin_user_token: Dict[str, str], get_test_db
):
    tokens = get_admin_user_token["access_token"]
    headers = {"Authorization": f"Bearer {str(tokens)}"}
    response = await client.get("/api/v1/trash/", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_trash_with_regular_user(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):
    tokens = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {str(tokens)}"}
    response = await client.get("/api/v1/trash/", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_bulk_users(
    client: AsyncClient,
    get_current_user_token: Dict[str, str],
    get_test_db,
    create_bulk_test_users,
):
    tokens = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {str(tokens)}"}

    data_of_users = create_bulk_test_users

    db = get_test_db
    user_collection: Collection = db["users"]

    email_list = [user_details["email"] for user_details in data_of_users]

    users_cursor = user_collection.find({"email": {"$in": email_list}})
    users_list = await users_cursor.to_list()

    user_ids = [str(user["_id"]) for user in users_list]

    payload = {"ids": user_ids, "reason": "testing.."}

    response = await client.post(
        "/api/v1/trash/bulk-delete", json=payload, headers=headers
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_bulk_users_admin(
    client: AsyncClient,
    get_admin_user_token: Dict[str, str],
    get_test_db,
    create_bulk_test_users,
):
    tokens = get_admin_user_token["access_token"]
    headers = {"Authorization": f"Bearer {tokens}"}

    data_of_users = create_bulk_test_users

    db = get_test_db
    user_collection: Collection = db["users"]

    email_list = [user_details["email"] for user_details in data_of_users]

    users_cursor = user_collection.find({"email": {"$in": email_list}})
    users_list = await users_cursor.to_list()

    user_ids = [str(user["_id"]) for user in users_list]

    payload = {"ids": user_ids, "reason": "testing.."}

    response = await client.post(
        "/api/v1/trash/bulk-delete", json=payload, headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["deleted_now"] == user_ids
    assert response_data["alredy_deleted_user"] == []

    response = await client.post(
        "/api/v1/trash/bulk-delete", json=payload, headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["deleted_now"] == []
    assert response_data["alredy_deleted_user"] == user_ids


@pytest.mark.asyncio
async def test_restore_users_admin(
    client: AsyncClient, get_admin_user_token: Dict[str, str], get_test_db
):
    tokens = get_admin_user_token["access_token"]
    headers = {"Authorization": f"Bearer {tokens}"}

    db = get_test_db
    user_collection: Collection = db["users"]
    user_payload = {
        "email": "new@mail.com",
        "password": "12wsess3",
        "username": "news8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_id = await user_collection.find_one({"email": user_payload["email"]})
    user_id = str(user_id["_id"])

    data = {"reason": "testing"}

    response = await client.delete(
        f"/api/v1/auth/users/{user_id}", headers=headers, params=data
    )

    assert response.status_code == 204

    response = await client.put(f"/api/v1/trash/restore/{user_id}", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_restore_users_with_regular_user(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):
    tokens = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {tokens}"}

    db = get_test_db
    user_collection: Collection = db["users"]
    user_payload = {
        "email": "new1@mail.com",
        "password": "12wsess3",
        "username": "n1ews8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_id = await user_collection.find_one({"email": user_payload["email"]})
    user_id = str(user_id["_id"])

    data = {"reason": "testing"}

    response = await client.delete(
        f"/api/v1/auth/users/{user_id}", headers=headers, params=data
    )

    assert response.status_code == 403

    response = await client.put(f"/api/v1/trash/restore/{user_id}", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_permanent_delete_users_admin(
    client: AsyncClient, get_admin_user_token: Dict[str, str], get_test_db
):
    tokens = get_admin_user_token["access_token"]
    headers = {"Authorization": f"Bearer {tokens}"}

    db = get_test_db
    user_collection: Collection = db["users"]
    user_payload = {
        "email": "new12@mail.com",
        "password": "12wsess3",
        "username": "n12ews8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_id = await user_collection.find_one({"email": user_payload["email"]})
    user_id = str(user_id["_id"])

    data = {"reason": "testing"}

    response = await client.delete(
        f"/api/v1/auth/users/{user_id}", headers=headers, params=data
    )

    assert response.status_code == 204

    response = await client.delete(
        f"/api/v1/trash/permanent/delete/{user_id}", headers=headers
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_permanent_delete_users_with_regular_user(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):
    tokens = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {tokens}"}

    db = get_test_db
    user_collection: Collection = db["users"]
    user_payload = {
        "email": "nesw12@mail.com",
        "password": "12wsssess3",
        "username": "n12esws8",
    }

    response = await client.post("/api/v1/auth/signup", json=user_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["message"] == "User account created successfully."

    user_id = await user_collection.find_one({"email": user_payload["email"]})
    user_id = str(user_id["_id"])

    data = {"reason": "testing"}

    response = await client.delete(
        f"/api/v1/auth/users/{user_id}", headers=headers, params=data
    )

    assert response.status_code == 403

    response = await client.delete(
        f"/api/v1/trash/permanent/delete/{user_id}", headers=headers
    )
    assert response.status_code == 403
