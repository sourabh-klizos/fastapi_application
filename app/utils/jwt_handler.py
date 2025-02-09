
from jose import jwt

from datetime import datetime ,timedelta , timezone
from uuid import uuid4
from app.database.db import refresh_token_collection


SECRET_KEY = "bGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
ALGORITHM = "HS256"






async def create_access_token(user_id:str, minutes:int=None) -> dict:

    if not minutes:
        minutes = 30

    payload_to_encode = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc)  + timedelta(minutes=minutes), 
        'iat': datetime.now(timezone.utc), 
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

    condition = {"user_id": user_id} 
    update = {
        "$set": {
            "refresh_token": refresh_token,
            "jti": payload_to_encode['jti']
        }
    }

    await refresh_token_collection.find_one_and_update(condition,update,upsert=True)

    return refresh_token





async def decode_jwt(access_token: str) -> dict:
    try:

        decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token['typ'] == "access_token":
            return decoded_token

    except Exception as  e:
        # print(f"Error decoding token: {e}")
        return None








