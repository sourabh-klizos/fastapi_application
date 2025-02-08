from fastapi import   APIRouter , HTTPException , status, Response

from app.models.user import UserRequestModel , UserLoginModel
from app.utils.generate_username import generate_available_username

from app.database.db import user_collection

from app.utils.jwt_handler import create_access_token , create_refresh_token 
from app.utils.hashing import get_hashed_password, verify_password


auth_routes = APIRouter(
    prefix="/api/v1/auth"
)



@auth_routes.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_credential:UserRequestModel):

    user_dict = user_credential.model_dump()    
    user_dict['email'] = user_dict['email'].lower()

    username = user_dict.get("username")
    user_email = user_dict.get("email")

    email_already_exists =  await user_collection.find_one({"email" : user_email} )
    username_already_exists = await user_collection.find_one({"username" :username } )

    if email_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists with this email" , headers={}
        )
    
    if username_already_exists:
        choose_username = await generate_available_username(username)    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"message" :"User already exists with this username" ,
                "suggested_usernames" :choose_username} 
            
        )    
    
    user_dict['password'] = await get_hashed_password(user_dict['password'])
    user_instance = await user_collection.insert_one(user_dict)
    
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



