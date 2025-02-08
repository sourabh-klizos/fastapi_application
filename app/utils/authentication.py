import bcrypt
from jose import jwt

from datetime import datetime ,timedelta , timezone
from uuid import uuid4
from app.database.db import refresh_token_collection


SECRET_KEY = "bGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
ALGORITHM = "HS256"




async def get_hashed_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


async def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)




async def create_access_token(user_id:str, minutes:int=None) -> dict:

    if not minutes:
        minutes = 30

    payload_to_encode = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc)  + timedelta(minutes=minutes), 
        'iat': datetime.now(timezone.utc)  , 
        'jti': str(uuid4()),  
        'typ': "access_token"  
    }


    access_token = jwt.encode(payload_to_encode, SECRET_KEY, ALGORITHM)

    return access_token





async def create_refresh_token(user_id:str, hours:int=None) -> dict:
    if not hours:
        hours = 24 * 7 

    payload_to_encode = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc)  + timedelta(hours=hours), 
        'iat': datetime.now(timezone.utc) , 
        'jti': str(uuid4()),  
        'typ': "refresh_token"  
    }


    refresh_token = jwt.encode(payload_to_encode, SECRET_KEY,ALGORITHM)



    # await refresh_token_collection.insert_one({
    #     "user_id": user_id,
    #     "refresh_token":refresh_token,
    #     "jti" : payload_to_encode['jti'] # added a unique identifier for token just for safe case
    # })

    condation =  {"user_id" : user_id}
    update = {
            "$set": {
                "user_id" : user_id,
                "refresh_token" : refresh_token,
                "jti" : payload_to_encode['jti']
            }
        }

    data = await refresh_token_collection.update_one(
        condation,
        update,
        upsert=True
    )

    # existing_user = await refresh_token_collection.find_one({"user_id": user_id})
    # if existing_user:
    #     return existing_user  # Return the existing document

    # # Create a new document if not found
    # new_user = {
    #             "user_id" : user_id,
    #             "refresh_token" : refresh_token,
    #             "jti" : payload_to_encode['jti']
    # }
    # await refresh_token_collection.insert_one(new_user)
    # print(data)
 
    return refresh_token





async def decode_jwt(access_token: str) -> dict:
    try:

        decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        return decoded_token['user_id']

    except Exception as  e:
        print(f"Error decoding token: {e}")
        return None

