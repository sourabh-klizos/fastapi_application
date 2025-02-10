from fastapi import APIRouter, status, HTTPException , Depends , Security, Query

from fastapi.security import OAuth2PasswordBearer
from app.utils.get_current_logged_in_user import get_current_user_id
from app.database.db import user_collection, trash_collection
from bson import ObjectId
from datetime import datetime
from app.utils.convert_bson_id_str import convert_objectids_list
from app.models.trash import TrashResponseModel, PaginatedTrashResponseModel, BulkTrashIds
from typing import List , Optional
from app.utils.paginator import paginate_query
from app.utils.str_to_bson import convert_str_object_id



trash_routes = APIRouter(
    prefix="/api/v1/trash",
    tags=['trash']
)



@trash_routes.get("/", response_model=PaginatedTrashResponseModel, status_code=status.HTTP_200_OK)
async def view_trash(
    user_id=Depends(get_current_user_id),
    page: int = Query(1, ge=1), 
    per_page: Optional[int] = Query(10, ge=1, le=20),
):
    
    try:
        logged_in_user = await user_collection.find_one({"_id": ObjectId(user_id)})

        if logged_in_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if logged_in_user['role'] != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to perform this action"
            )

        response = await paginate_query(
            collection=trash_collection,
            query={},
            exclude_fields={},
            page=page,
            per_page=per_page 
        )
        
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
        
    




@trash_routes.post("/bulk-delete", status_code=status.HTTP_200_OK)

async def bulk_delete(trash_ids:BulkTrashIds, current_user_id = Depends(get_current_user_id)):
    logged_in_user = await user_collection.find_one({"_id":ObjectId(current_user_id)})

    if logged_in_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    if logged_in_user['role'] != "admin":
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to perform this action"
            )
  

    trash_ids = trash_ids.model_dump()
    alredy_deleted_user = list()
    deleted_users = list()

    trash_id_list = await  convert_str_object_id(trash_ids['ids'])
    for id in trash_id_list:
        user = await user_collection.find_one({"_id":id})
        if user and not user['is_deleted']:
            await  user_collection.update_one({"_id":id}, {"$set":{"is_deleted" :True}})

            await trash_collection.insert_one({
                "user_id": str(id), 
                "deleted_by" :str(current_user_id),
                "deleted_at" : datetime.now()
                })
            
            deleted_users.append(str(id))
        else:
            alredy_deleted_user.append(str(id))


    return {
        "alredy_deleted_user" : alredy_deleted_user,
        "deleted_now" : deleted_users
    }
 



@trash_routes.put("/restore/{user_id}", status_code=status.HTTP_200_OK)
async def restore_user(user_id:str,current_user= Depends(get_current_user_id)):
    try:
        logged_in_user = await user_collection.find_one({"_id":ObjectId(current_user)})

        if logged_in_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        if logged_in_user['role'] != "admin":
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have access to perform this action"
                )
        

        user_to_restore = await user_collection.find_one({"_id":ObjectId(current_user)})
        if not user_to_restore:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
            )
            
        if user_to_restore['is_deleted'] == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "You are Trying to restore a non deleted user"
            )
        
        updated_user = await user_collection.find_one_and_update(
            {"_id": ObjectId(user_id), "is_deleted": True}, 
            {"$set": {"is_deleted": False}},  
            return_document=True 
        )

        trash =  await trash_collection.find_one_and_delete({"user_id" :user_id})
        if trash:
            return {"success" : "Usccessfully restored user"}

      
    except Exception as e:
        print(e)

    return {"success" : "succuess"}






















# @trash_routes.post("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
# async def soft_delete_user(user_id : str, current_user =Depends(get_current_user_id)):

#     is_admin_user = False
#     logged_in_user = await user_collection.find_one({"_id":ObjectId(current_user)})

#     if logged_in_user and logged_in_user['role'] == "admin":
#         is_admin_user = True

#     if current_user == user_id or is_admin_user:
#         user = await user_collection.find_one({"_id":ObjectId(user_id)})
#         if user:
#             if user['is_deleted']:
#                 raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Alredy Deleted"
#             )

#             condition = {"_id": ObjectId(user_id)}
#             update = {"$set": {"is_deleted": True}}

#             user = await user_collection.update_one(condition,update)
#             trash = {
#                 "user_id":user_id,
#                 "deleted_by" :current_user,
#                 "deleted_at" : datetime.now()
#             }

#             await trash_collection.insert_one(trash)

#             print(trash, " --")

#             return

#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User Doesn't Exists"
#             )
#     else:
#         raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="You don't have access to performe this action"
#             )



