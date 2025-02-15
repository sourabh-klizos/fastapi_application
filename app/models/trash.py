from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class TrashResponseModel(BaseModel):
    id: str
    user_id: str
    deleted_by: str
    deleted_at: datetime = datetime.now()


class PaginatedTrashResponseModel(BaseModel):
    total: int
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None
    data: List[TrashResponseModel]


class BulkTrashIds(BaseModel):
    ids: List[str]
    reason: str


#     await getter
# asyncio.exceptions.CancelledError
