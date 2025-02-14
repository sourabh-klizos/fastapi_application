from fastapi import FastAPI, Depends

from motor.motor_asyncio import AsyncIOMotorClient
from motor import motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# client = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")

# database = client['fast_api_db']
# user_collection = database['users']
# refresh_token_collection = database['refresh_tokens']
# trash_collection = database['trash']


# data = await db["mycollection"].find_one({"name": "test"})


DATABASE_URL = os.getenv("DATABASE_URL")
DB_NAME = os.getenv("DB_NAME")


# async def get_production_db():
#     client = AsyncIOMotorClient("mongodb://localhost:27017/")
#     db = client["production_db"]
#     return db

# # Dependency to get the database
# async def get_db():
#     return await get_production_db()


async def get_db():

    client = AsyncIOMotorClient(DATABASE_URL)
    db = client[DB_NAME]
    try:
        yield db
    finally:
        client.close()
