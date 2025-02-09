from motor import motor_asyncio




client = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")

database = client['fast_api_db']
user_collection = database['users']
refresh_token_collection = database['refresh_tokens']
trash_collection = database['trash']


