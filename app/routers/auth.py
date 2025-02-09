from fastapi import   APIRouter , HTTPException , status , Depends
from typing import Any, Dict, List

from app.models.user import UserRequestModel , UserLoginModel , UserEditReqModel
from app.utils.generate_username import generate_available_username

from app.database.db import user_collection , trash_collection
from datetime import datetime

from app.utils.jwt_handler import create_access_token , create_refresh_token 
from app.utils.hashing import get_hashed_password, verify_password
from app.utils.get_current_logged_in_user import get_current_user_id
from app.utils.convert_bson_id_str import  convert_objectids_list ,convert_objectid
from bson import ObjectId


auth_routes = APIRouter(
    prefix="/api/v1/auth"
)



@auth_routes.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_credential:UserRequestModel):

    user_dict = user_credential.model_dump()    
    user_dict['email'] = user_dict['email'].lower()
    user_dict['username'] = user_dict['username'].lower()

    username = user_dict.get("username")
    user_email = user_dict.get("email")

    email_already_exists =  await user_collection.find_one({"email" : user_email} )
    username_already_exists = await user_collection.find_one({"username" :username } )

    if email_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this email"
        )
    
    if username_already_exists:
        choose_username = await generate_available_username(username)    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={    "message" :"User already exists with this username" ,
                        "suggested_usernames" :choose_username
                    }
        )    
    
    user_dict['created_at'] = datetime.now()
    user_dict['role'] = "regular"
    user_dict['is_deleted'] = False
    # user_dict['deleted_by'] = "None"

    user_dict['password'] = await get_hashed_password(user_dict['password'])
    await user_collection.insert_one(user_dict)
    
    return {"message": "User account created successfully."}


@auth_routes.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user_credential:UserLoginModel):
    user_dict = user_credential.model_dump()    
    email = user_dict['email'].lower()
    password = user_dict.get("password")


    user_instance = await user_collection.find_one({"email" : email})
    if not user_instance:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    hashed_password = user_instance.get("password")
    check_password = await verify_password(password, hashed_password)

    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=  "Incorrect email or password"
        )

    user_id = str(user_instance.get("_id"))
    access_token = await create_access_token(user_id)
    refresh_token = await create_refresh_token(user_id)

    return {
        "access_token":access_token,
        "refresh_token":refresh_token
        }







@auth_routes.get("/users", status_code=status.HTTP_200_OK)
async def retrive_active_users(current_user = Depends(get_current_user_id)):#need to paginate
    users_cursor = user_collection.find({"is_deleted": False}, {"password":0})
    users_list = await users_cursor.to_list(length=None)
    users = await convert_objectids_list(users_list)
    return {
        "users" :users
    }


@auth_routes.get("/users/{user_id}")
async def get_user_detail(user_id:str, current_user = Depends(get_current_user_id)):
    user = await user_collection.find_one({"_id": ObjectId(user_id)}, {"password":0})
    user = await convert_objectid(user)
    return {"data" : user}


@auth_routes.put("/users/{user_id}")
async def get_user_detail(data :UserEditReqModel ,user_id:str, current_user = Depends(get_current_user_id)):
    # print("data", data)
    dict_data = data.model_dump()

    data_to_update = dict()
    if "email" in dict_data and dict_data['email'] is not None:
        data_to_update['email'] = dict_data['email'].lower()
    if "username" in dict_data and dict_data['username'] is not None:
        data_to_update['username'] = dict_data['username'].lower()

    is_admin_user = False
    logged_in_user = await user_collection.find_one({"_id":ObjectId(current_user)})

    if logged_in_user and logged_in_user['role'] == "admin":
        is_admin_user = True

    if current_user == user_id or is_admin_user:
        # user = await user_collection.find_one({"_id":ObjectId(user_id)})
        print(data_to_update)
        await user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data_to_update})
        user =  await user_collection.find_one({"_id":ObjectId(user_id)}, {"password":0})


        user_data = await convert_objectid(user)
        
    return {"data":user_data}



@auth_routes.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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
            trash = {
                "user_id":user_id,
                "deleted_by" :current_user,
                "deleted_at" : datetime.now()
            }

            await trash_collection.insert_one(trash)
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



