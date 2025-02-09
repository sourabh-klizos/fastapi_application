from pydantic import BaseModel, EmailStr
from typing import Optional , List, Dict, Any
from datetime import datetime



async def convert_objectid(document: Dict[str,Any]) -> Dict[str, Any]:
    if document and "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    return document



async def convert_objectids_list(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [ await convert_objectid(document) for document in documents]





class UserRequestModel(BaseModel):

    email: EmailStr
    username:str
    password: str
    # created_at: datetime = datetime.now()



    

# class UserResModel(UserRequestModel):
#     id:str
#     email: EmailStr
#     username:str
#     role:str





# class UserResModel(UserRequestModel):
#     id:str
#     updated_at: Optional[datetime] = None
#     is_deleted: bool = False



class UserLoginModel(BaseModel):
    email: EmailStr
    password: str






class RefreshTokenReqModel(BaseModel):
    refresh_token: str
    