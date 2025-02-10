from fastapi import APIRouter , HTTPException , status
from app.utils.jwt_handler import create_access_token
from app.database.db import refresh_token_collection
from app.models.user import RefreshTokenReqModel
from app.utils.jwt_handler import decode_jwt

access_routes= APIRouter(
    prefix="/api/v1/refresh",
    tags=['obtain_access_by_refresh_token']
) 




@access_routes.post("/", status_code=status.HTTP_200_OK)
async def get_access_token(refresh_token:RefreshTokenReqModel):
    refresh_token = refresh_token.model_dump()
    
    decoded_refresh = await decode_jwt(refresh_token.get('refresh_token'), "refresh_token")
    if not decoded_refresh:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Not a valid refresh token"
    )

    user_id = decoded_refresh['user_id']

    stored_refresh_token =  await refresh_token_collection.find_one({"user_id" : user_id})

    if  stored_refresh_token['refresh_token'] == refresh_token['refresh_token']:
        access_token = await create_access_token(user_id=user_id)
        return {"access_token":access_token}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perfome this operation"
    )



    

