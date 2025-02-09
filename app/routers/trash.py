from fastapi import APIRouter, status, HTTPException , Depends , Security

from fastapi.security import OAuth2PasswordBearer
from app.utils.get_current_logged_in_user import get_current_user_id
from app.database.db import user_collection
from bson import ObjectId







trash_routes = APIRouter(
    prefix="/api/v1/trash"
)



@trash_routes.post("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_user(user_id : str, current_user =Depends(get_current_user_id)):

    is_admin_user = False
    logged_in_user = await user_collection.find_one({"_id":ObjectId(current_user)})

    if logged_in_user and logged_in_user['role'] == "admin":
        is_admin_user = True

    if current_user == user_id or is_admin_user:
        user = await user_collection.find_one({"_id":ObjectId(user_id)})
        if user:
            if user['is_deleted']:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Alredy Deleted"
            )

            condition = {"_id": ObjectId(user_id)}
            update = {"$set": {"is_deleted": True}}

            user = await user_collection.update_one(condition,update)
            return

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Doesn't Exists"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to performe this action"
            )



