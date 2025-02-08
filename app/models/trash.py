from pydantic import BaseModel, EmailStr
from datetime import datetime





class TrashRequestModel(BaseModel):
    user_id: str
    deleted_by: str
    deleted_at: datetime = datetime.now()


class TrashResponseModel(TrashRequestModel):
    username: str

