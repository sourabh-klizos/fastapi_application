from pydantic import BaseModel


class ImageData(BaseModel):
    image: bytes
