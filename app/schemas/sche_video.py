from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole
from app.schemas.sche_base import MappingByFieldName


class UserBase(MappingByFieldName):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class VideoItemResponse(MappingByFieldName):
    id: int
    user_name: str
    youtube_url: str
    title: str
    description: str


class VideoCreateRequest(UserBase):
    user_id: int
    video_url: str

