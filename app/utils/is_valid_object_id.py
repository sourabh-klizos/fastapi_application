from bson import ObjectId
from fastapi import HTTPException, status


async def validate_valid_object_id(id: str):
    if not id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing user id in url"
        )
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=" Not a valid ObjectId"
        )
