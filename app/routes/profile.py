from fastapi import HTTPException, status, APIRouter, File, UploadFile, Depends
import os
import uuid
from app.utils.get_current_logged_in_user import get_current_user_id
from pymongo.collection import Collection
from app.database.db import get_db
from bson import ObjectId

profile_routes = APIRouter(prefix="/api/v1/profile-upload", tags=["profile"])


@profile_routes.post("/", status_code=status.HTTP_200_OK)
async def upolad_profile_picture(
    image: UploadFile = File(...),
    current_user: str = Depends(get_current_user_id),
    db=Depends(get_db),
):

    user_collection: Collection = db["users"]

    user = await user_collection.find_one({"_id": ObjectId(current_user)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    file_name_with_extension = image.filename
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    allowed_types: list = [".jpg", ".jpeg", ".png"]
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Please upload a .jpg, .jpeg, or .png file.",
        )

    image_data = await image.read()

    upload_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "uploaded_images"
    )

    os.makedirs(upload_folder, exist_ok=True)

    unique_filename = f"{file_name.lower()}_{uuid.uuid4().hex}{file_extension.lower()}"

    image_path = os.path.join(upload_folder, unique_filename)

    await user_collection.update_one(
        {"_id": ObjectId(current_user)}, {"$set": {"profile_image": unique_filename}}
    )

    with open(image_path, "wb") as f:
        f.write(image_data)

    return {"message": "File uploaded successfully!", "filename": unique_filename}
