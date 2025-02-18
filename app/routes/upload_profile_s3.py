import boto3
from fastapi import File, UploadFile, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import uuid
from app.database.db import get_db
from app.utils.get_current_logged_in_user import get_current_user_id
from pymongo.collection import Collection
from bson import ObjectId

profile_upolad_s3 = APIRouter(
    prefix="/api/v1/profile-upload-s3", tags=["profile_upload"]
)


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = "fastapi-s3-bucket-sourabh"
AWS_REGION = "eu-north-1"


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


@profile_upolad_s3.post("/")
async def upload_image(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    try:

        file_extension = os.path.splitext(file.filename)[1].lower()
        allowed_types: list = [".jpg", ".jpeg", ".png"]
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type not allowed. \
                    Please upload a .jpg, .jpeg, or .png file.",
            )

        unique_filename = f"{file.filename.lower()}_{uuid.uuid4()}{file_extension}"
        image_data = await file.read()

        s3_client.put_object(
            Bucket=AWS_BUCKET_NAME,
            Key=unique_filename,
            Body=image_data,
            ContentType=file.content_type,
        )

        file_url = (
            f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        )

        user_collection: Collection = db["users"]
        await user_collection.update_one(
            {"_id": ObjectId(current_user)},
            {"$set": {"profile_image": file_url}},
        )

        return JSONResponse(
            content={"message": "Image uploaded successfully!", "filename": file_url},
            status_code=200,
        )

    except HTTPException as http_error:
        raise HTTPException(
            status_code=http_error.status_code,
            detail=http_error.detail,
        )

    except (NoCredentialsError, PartialCredentialsError) as e:
        return JSONResponse(
            content={"message": f"Credentials error: {str(e)}"}, status_code=400
        )
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)


# https://sourabh-fastapi-bucket.s3.eu-north-1.amazonaws.com/premium_photo-1664474619075-644dd191935f.jpg
