from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


async def convert_objectid(document: Dict[str, Any]) -> Dict[str, Any]:
    if document and "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    return document


async def convert_objectids_list(
    documents: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    return [await convert_objectid(document) for document in documents]


class UserRequestModel(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserEditReqModel(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

    @model_validator(mode="before")
    def check_at_least_one(cls, values):
        if not values.get("email") and not values.get("username"):
            raise ValueError("At least one of 'email' or 'username' must be provided.")
        return values


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class UserResponseModel(BaseModel):
    id: str
    email: EmailStr
    role: str
    username: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool
    updated_by: Optional[str] = None


class PaginatedUserResponseModel(BaseModel):
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None
    data: List[UserResponseModel]



class ReasonRequestModel(BaseModel):
    reason: str

