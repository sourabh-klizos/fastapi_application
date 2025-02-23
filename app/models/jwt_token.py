from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenReqModel(BaseModel):
    refresh_token: str
