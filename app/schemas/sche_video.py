from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole
from app.schemas.sche_base import MappingByFieldName


class UserBase(MappingByFieldName):

    class Config:
        orm_mode = True


class VideoItemResponse(MappingByFieldName):
    id: int
    user_name: Optional[str]
    youtube_url: str
    title: str
    description: str


class VideoCreateRequest(UserBase):
    video_url: str

