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
from app.tests.test_utils.get_users_data import generate_fake_users
# from app.tests.conftest import  create_bulk_test_users, clean_up_test_users , get_admin_user_token, test_admin_user













@pytest.mark.asyncio
async def test_get_users_with_regulat_user(client:AsyncClient , get_current_user_token: Dict[str, str], get_test_db):
    tokens = get_current_user_token
    headers = {
        "Authorization" : f"Bearer {tokens["access_token"]}"
    }
    response = await client.get("/api/v1/auth/users", headers=headers)
    assert response.status_code == 403





@pytest.mark.asyncio
async def test_get_users(client:AsyncClient , get_admin_user_token: Dict[str, str], get_test_db):
    tokens = get_admin_user_token
    headers = {
        "Authorization" : f"Bearer {tokens["access_token"]}"
    }

    db = get_test_db
    users_collection: Collection = db['users']

    response = await client.get("/api/v1/auth/users", headers=headers)
    assert response.status_code == 200

    query = {"is_deleted": False}
    users =  await users_collection.find(query).to_list()

    response_data = response.json()
    assert response_data['total'] == len(users)

    
    

@pytest.mark.asyncio
async def test_search_user(client, get_test_db,get_admin_user_token,  create_bulk_test_users):

    tokens = get_admin_user_token
    headers = {
        "Authorization" :  f"Bearer {tokens["access_token"]}"
    }

    data_to_create =  create_bulk_test_users

    username = data_to_create[0]['username']

    response = await client.get(f"/api/v1/auth/users?q={username}", headers=headers)
    assert response.status_code == 200
    response_data = response.json()

   
    assert response_data['total'] == 1

    


@pytest.mark.asyncio
async def test_limit_no_of_records(client, get_test_db,get_admin_user_token,  create_bulk_test_users):

    tokens = get_admin_user_token
    headers = {
        "Authorization" :  f"Bearer {tokens["access_token"]}"
    }

    data_to_create =  create_bulk_test_users
    username = data_to_create[0]['username']
    response = await client.get(f"/api/v1/auth/users?per_page=4", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    data_length = len(response_data['data'])
    assert data_length == 4

    



@pytest.mark.asyncio
async def test_get_current_user_detail(client, test_user, get_test_db,get_current_user_token):
    tokens = get_current_user_token
    headers = {
        "Authorization" :  f"Bearer {tokens["access_token"]}"
    }

    db = get_test_db
    user_collection: Collection = db["users"]
    user_id = await user_collection.find_one({"email":test_user['email']}, {"_id" : 1})
    str_user_id = str(user_id['_id'])
    response = await client.get(f"/api/v1/auth/users/{str_user_id}", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['email'] == test_user['email']






@pytest.mark.asyncio
async def test_access_other_user(client, test_user, get_test_db,get_current_user_token):
    tokens = get_current_user_token
    headers = {
        "Authorization" :  f"Bearer {tokens["access_token"]}"
    }
    
    other_user_detail = {
        "email": "other@gmail.com",
        "password": "test1234",
        "username": "other_sourabh",
    }
    response = await client.post("/api/v1/auth/signup", json=other_user_detail)
    assert response.status_code == 201
    response_data = response.json()

    db = get_test_db
    user_collection: Collection = db["users"]

    other_user_id = await user_collection.find_one({"email":other_user_detail['email']}, {"_id" : 1})
    str_other_user_id = str(other_user_id['_id'])
    response = await client.get(f"/api/v1/auth/users/{str_other_user_id}", headers=headers)

    assert response.status_code == 403
    response_data = response.json()






@pytest.mark.asyncio
async def test_access_other_user(client, test_user, get_test_db,get_admin_user_token):
    tokens = get_admin_user_token
    headers = {
        "Authorization" :  "Bearer" +" "+ tokens["access_token"]
    }
    
    other_user_detail = {
        "email": "other@gmail.com",
        "password": "test1234",
        "username": "other_sourabh",
    }
    response = await client.post("/api/v1/auth/signup", json=other_user_detail)
    assert response.status_code == 201
    response_data = response.json()

    db = get_test_db
    user_collection: Collection = db["users"]

    other_user_id = await user_collection.find_one({"email":other_user_detail['email']}, {"_id" : 1})
    str_other_user_id = str(other_user_id['_id'])
    response = await client.get(f"/api/v1/auth/users/{str_other_user_id}", headers=headers)

    assert response.status_code == 200
    response_data = response.json()








@pytest.mark.asyncio
async def test_get_current_user_detail(client, test_user, get_test_db,get_current_user_token):
    tokens = get_current_user_token
    headers = {
        "Authorization" :  "Bearer" +" "+ tokens["access_token"]
    }
    
    db = get_test_db
    user_collection: Collection = db["users"]
    user_id = await user_collection.find_one({"email":test_user['email']}, {"_id" : 1})
    str_user_id = str(user_id['_id'])
    response = await client.get(f"/api/v1/auth/users/{str_user_id}", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['email'] == test_user['email']









@pytest.mark.asyncio
async def test_update_user_detail_success(client, get_test_db, get_admin_user_token, test_user):
    token = get_admin_user_token['access_token']


    data = {"email": "test123@example.com", "username": "24new_username"}
    headers = {"Authorization": f"Bearer {token}"}
    
    db = get_test_db
    user_collection: Collection = db["users"]

    user_id = await user_collection.find_one({"email":test_user['email']}, {"_id" : 1})
    str_user_id = str(user_id['_id'])
    print(str_user_id)

    response = await client.put(f"/api/v1/auth/users/{str_user_id}", headers=headers, json=data)

    assert response.status_code == 200
    response_data = response.json()


    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"] 














@pytest.mark.asyncio
async def test_update_self_user_detail(client, get_test_db, get_current_user_token, test_user):
    token = get_current_user_token['access_token']


    data = {"email": "test123463@example.com", "username": "24ne4w_username"}
    headers = {"Authorization": f"Bearer {token}"}
    
    db = get_test_db
    user_collection: Collection = db["users"]

    user_id = await user_collection.find_one({"email":test_user['email']}, {"_id" : 1})
    str_user_id = str(user_id['_id'])

    response = await client.put(f"/api/v1/auth/users/{str_user_id}", headers=headers, json=data)

    assert response.status_code == 200
    response_data = response.json()


    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"] 




@pytest.mark.asyncio
async def test_update_other_user_detail_without_admin_previllage(client, get_test_db, get_current_user_token, test_user):
    token = get_current_user_token['access_token']

    other_user_detail = {
        "email": "othe1r@gmail.com",
        "password": "te2st1234",
        "username": "oth2er_sourabh",
    }

    data = {"email": "test1233463@example.com", "username": "24ne4w3_username"}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.post("/api/v1/auth/signup", json=other_user_detail)
    assert response.status_code == 201
    response_data = response.json()

    db = get_test_db
    user_collection: Collection = db["users"]

    other_user_id = await user_collection.find_one({"email":other_user_detail['email']}, {"_id" : 1})
    str_other_user_id = str(other_user_id['_id'])

    response = await client.put(f"/api/v1/auth/users/{str_other_user_id}", headers=headers, json=data)

    assert response.status_code == 403
   














@pytest.mark.asyncio
async def test_delete_user(client, get_test_db, get_current_user_token, test_user):
    token = get_current_user_token['access_token']


    headers = {"Authorization": f"Bearer {token}"}
    
    db = get_test_db
    user_collection: Collection = db["users"]
    data = { "reason" :"testing"  }
    user_id = await user_collection.find_one({"email":test_user['email']}, {"_id" : 1})
    str_user_id = str(user_id['_id'])
    print(user_id)
    response = await client.delete(f"/api/v1/auth/users/{str_user_id}", headers=headers, json=data)

    assert response.status_code == 204
