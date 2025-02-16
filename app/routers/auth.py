from typing import Any, Dict, List, Optional
from app.utils.is_valid_object_id import PyObjectId

from fastapi import APIRouter, HTTPException, status, Depends, Query
from datetime import datetime
from bson import ObjectId
from app.models.user import (
    UserRequestModel,
    UserLoginModel,
    UserEditReqModel,
    UserResponseModel,
    PaginatedUserResponseModel,
    ReasonRequestModel,
)
from app.utils.generate_username import generate_available_username

# from app.database.db import user_collection , trash_collection
from app.utils.jwt_handler import create_access_token, create_refresh_token
from app.utils.hashing import get_hashed_password, verify_password
from app.utils.get_current_logged_in_user import get_current_user_id
from app.utils.convert_bson_id_str import convert_objectid
from app.models.jwt_token import TokenResponseModel
from app.utils.paginator import paginate_query
from app.database.db import get_db
from pymongo.collection import Collection
from app.utils.is_admin import is_logged_in_and_admin

auth_routes = APIRouter(prefix="/api/v1/auth", tags=["user"])


@auth_routes.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_credential: UserRequestModel, db=Depends(get_db)):

    user_collection: Collection = db["users"]

    user_dict = user_credential.model_dump()

    user_dict["email"] = user_dict["email"].lower()
    user_dict["username"] = user_dict["username"].lower()

    username = user_dict.get("username")
    user_email = user_dict.get("email")
    email_already_exists = await user_collection.find_one({"email": user_email})
    username_already_exists = await user_collection.find_one({"username": username})
    if email_already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this email",
        )

    if username_already_exists:
        choose_username = await generate_available_username(username, db)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "User already exists with this username",
                "suggested_usernames": choose_username,
            },
        )

    user_dict["created_at"] = datetime.now()
    user_dict["role"] = "regular"
    user_dict["is_deleted"] = False
    user_dict["updated_at"] = None
    user_dict["password"] = await get_hashed_password(user_dict["password"])

    await user_collection.insert_one(user_dict)

    print("account created ---------------------------------successfully")
    return {"message": "User account created successfully."}


@auth_routes.post(
    "/login", status_code=status.HTTP_200_OK, response_model=TokenResponseModel
)
async def user_login(user_credential: UserLoginModel, db=Depends(get_db)):
    user_collection: Collection = db["users"]

    user_dict = user_credential.model_dump()
    email = user_dict["email"].lower()
    password = user_dict.get("password")

    user_instance = await user_collection.find_one({"email": email})
    if not user_instance:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    hashed_password = user_instance.get("password")
    check_password = await verify_password(password, hashed_password)

    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    user_id = str(user_instance.get("_id"))

    access_token = await create_access_token(user_id)
    refresh_token = await create_refresh_token(user_id=user_id, db=db)
    response = {"access_token": access_token, "refresh_token": refresh_token}
    return response


@auth_routes.get(
    "/users", response_model=PaginatedUserResponseModel, status_code=status.HTTP_200_OK
)
async def retrive_active_users(
    current_user=Depends(get_current_user_id),
    page: int = Query(1, ge=1),
    per_page: Optional[int] = Query(10, ge=1, le=30),
    q: Optional[str] = Query(None),
    db=Depends(get_db),
):
    
    user_collection: Collection = db["users"]
    
    logged_in_user = await user_collection.find_one({"_id": ObjectId(current_user)})    
    is_admin_user = await is_logged_in_and_admin(logged_in_user, raise_error=True)

    query = {"is_deleted": False}
    exclude_fields = {"password": 0}

    if q is not None:
        query["username"] = {"$regex": q, "$options": "i"}

    try:
        paginated_response = await paginate_query(
            query=query,
            exclude_fields=exclude_fields,
            collection=user_collection,
            page=page,
            per_page=per_page,
        )

        return paginated_response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@auth_routes.get("/users/{user_id}", response_model=UserResponseModel)
async def get_user_detail(
    user_id: PyObjectId, current_user=Depends(get_current_user_id), db=Depends(get_db)
):
    user_collection: Collection = db["users"]

    logged_in_user = await user_collection.find_one({"_id": ObjectId(current_user)})
    is_admin_user = await is_logged_in_and_admin(logged_in_user, raise_error=False)
  
    if current_user == user_id or is_admin_user:
        user = await user_collection.find_one(
            {"_id": ObjectId(user_id), "is_deleted": False}, {"password": 0}
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user = await convert_objectid(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have access to perfome this action",
        )

    

@auth_routes.put(
    "/users/{user_id}", response_model=UserResponseModel, status_code=status.HTTP_200_OK
)
async def get_user_detail(
    data: UserEditReqModel,
    user_id: PyObjectId,
    current_user=Depends(get_current_user_id),
    db=Depends(get_db),
):

    user_collection: Collection = db["users"]
    dict_data = data.model_dump()

    data_to_update = dict()
    if "email" in dict_data and dict_data["email"] is not None:
        email_alredy_exits = await user_collection.find_one(
            {"email": dict_data["email"].lower()}
        )

        if email_alredy_exits:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email Alredy Exists"
            )

        data_to_update["email"] = dict_data["email"].lower()

    if "username" in dict_data and dict_data["username"] is not None:
        username_alredy_exists = await user_collection.find_one(
            {"username": dict_data["username"].lower()}
        )
        if username_alredy_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username Alredy Exists"
            )
        data_to_update["username"] = dict_data["username"].lower()

    logged_in_user = await user_collection.find_one({"_id": ObjectId(current_user)})

    is_admin_user = await is_logged_in_and_admin(logged_in_user, raise_error=False)

    if current_user == user_id or is_admin_user:
        data_to_update["updated_at"] = datetime.now()
        data_to_update["updated_by"] = str(current_user)

        await user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": data_to_update}
        )
        user = await user_collection.find_one(
            {"_id": ObjectId(user_id)}, {"password": 0}
        )

        user_data = await convert_objectid(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have access to perfome this action",
        )

    return user_data


@auth_routes.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_user(
    user_id: PyObjectId,
    # reason: ReasonRequestModel,
    current_user=Depends(get_current_user_id),
    db=Depends(get_db),
    reason:str = Query()

):
    user_collection: Collection = db["users"]
    trash_collection: Collection = db["trash"]
    # print(reason, "=========================")
    # reason = reason.model_dump()
    # reason = reason.get("reason")

    logged_in_user = await user_collection.find_one({"_id": ObjectId(current_user)})
    is_admin_user = await is_logged_in_and_admin(logged_in_user, raise_error=False)

    if current_user == user_id or is_admin_user:
        user = await user_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Doesn't Exists"
            )

        if user:
            if user.get("is_deleted"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Alredy Deleted"
                )

            condition = {"_id": ObjectId(user_id)}
            update = {"$set": {"is_deleted": True}}

            user = await user_collection.update_one(condition, update)
            trash = {
                "user_id": user_id,
                "deleted_by": current_user,
                "deleted_at": datetime.now(),
                "reason": reason,
            }

            await trash_collection.insert_one(trash)
            print("created  trash ------------------------------=========================" 
                  )
            return

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Doesn't Exists"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to performe this action",
        )
