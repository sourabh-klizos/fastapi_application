from fastapi import APIRouter, HTTPException, status, Depends
from app.database.db import get_db

from app.models.user import UserRequestModel
from app.utils.generate_username import generate_available_username

# from app.database.db import user_collection
from datetime import datetime
from app.utils.hashing import get_hashed_password
from pymongo.collection import Collection

admin_routes = APIRouter(prefix="/api/v1/auth/admin", tags=["admin"])


@admin_routes.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_credential: UserRequestModel, db=Depends(get_db)):

    try:
        user_collection: Collection = db["users"]

        user_dict = user_credential.model_dump()
        user_dict["email"] = user_dict["email"].lower()

        username = user_dict.get("username")
        user_email = user_dict.get("email")

        email_already_exists = await user_collection.find_one({"email": user_email})
        username_already_exists = await user_collection.find_one({"username": username})

        if email_already_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this email",
                headers={},
            )

        if username_already_exists:
            choose_username = await generate_available_username(username, db)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "User already exists with this username",
                    "suggested_usernames": choose_username,
                },
            )

        user_dict["created_at"] = datetime.now()
        user_dict["role"] = "admin"
        user_dict["is_deleted"] = False
        user_dict["updated_at"] = None

        user_dict["password"] = await get_hashed_password(user_dict["password"])
        await user_collection.insert_one(user_dict)

        return {"message": "User account created successfully."}
    
    except HTTPException as http_error:
        raise HTTPException(
            status_code=http_error.status_code,
            detail=http_error.detail,
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
