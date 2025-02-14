
# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from app.database.db import get_db
# from motor.motor_asyncio import AsyncIOMotorClient
# import pytest_asyncio

# # MongoDB test config
# TEST_DATABASE_URL = "mongodb://localhost:27017/"
# TEST_DB_NAME = "fastapi_test_db"

# # Test version of get_db using AsyncIOMotorClient
# @pytest.fixture
# async def get_test_db():
#     client = AsyncIOMotorClient(TEST_DATABASE_URL)
#     db = client[TEST_DB_NAME]
#     try:
#         yield db
#     finally:
#         client.close()


# app.dependency_overrides[get_db] = get_test_db


# @pytest.fixture
# def client():
#     with TestClient(app) as client:
#         yield client


# # async def clean_users_collection():
# #     db =  get_db()
# #     users_collection = await  db['users']
# #     await users_collection.delete_many({})  
# #     print("Users collection cleaned.")


# # @pytest_asyncio.fixture
# # async def cleanup_db():
# #     """Fixture to automatically clean up the test database after each test."""
# #     db = await get_test_db()
# #     print("-------------------------db" ,db)
# #     await clean_users_collection(db) 
    

# #     yield
   
# #     print("Test finished, cleaning up database...")  
# #     db = await get_test_db()
# #     await clean_users_collection(db) 
# #     print("Test database cleaned.") 
# # # Test cases

# @pytest.mark.asyncio
# async def test_signup_success(client, get_test_db):
#     """Test successful user signup."""
#     user_data = {
#         "email": "bssqews@mail.com",
#         "password": "12wsess3",
#         "username": "aswwewswsdss8",
#     }

#     response = client.post("/api/v1/auth/signup", json=user_data)

#     assert response.status_code == 201
#     db = get_test_db
    
#     clean_users_collection = db['users']
#     await clean_users_collection() 
#     print("database clear is callted")
#     response_data = response.json()
#     assert response_data["message"] == "User account created successfully."


# @pytest.mark.asyncio
# async def test_signup_duplicate_username(client):
#     """Test signup with a duplicate username."""
#     user_data = {
#         "username": "tesdsstuser",
#         "email": "testusse232rs1@example.com",
#         "password": "securepassword123",
#     }

#     user_data_duplicate_username = {
#         "username": "tesdsstuser",
#         "email": "testudsqser@example.com",
#         "password": "securepassword123",
#     }

#     response = client.post("/api/v1/auth/signup", json=user_data)
#     assert response.status_code == 201

#     response = client.post("/api/v1/auth/signup", json=user_data_duplicate_username)
#     assert response.status_code == 409


# @pytest.mark.asyncio
# async def test_signup_duplicate_email(client):
#     """Test signup with a duplicate email."""
#     user_data1 = {
#         "username": "testuser1",
#         "email": "testuser@example.com",
#         "password": "securepassword123",
#     }
#     user_data2 = {
#         "username": "testuser2",
#         "email": "testuser@example.com",
#         "password": "securepassword123",
#     }

#     response = client.post("/api/v1/auth/signup", json=user_data1)
#     assert response.status_code == 201

#     response = client.post("/api/v1/auth/signup", json=user_data2)
#     assert response.status_code == 409


# @pytest.mark.asyncio
# async def test_signup_invalid_data(client):
#     """Test signup with invalid data."""
#     user_data = {"username": "testuser"}
#     response = client.post("/api/v1/auth/signup", json=user_data)

#     assert response.status_code == 422













