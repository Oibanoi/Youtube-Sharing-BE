from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole
from app.schemas.sche_base import MappingByFieldName


class UserBase(MappingByFieldName):
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True


class UserItemResponse(UserBase):
    id: int
    email: EmailStr

class UserCreateRequest(UserBase):
    full_name: Optional[str]
    password: str
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.GUEST


class UserRegisterRequest(MappingByFieldName):
    email: EmailStr
    password: str


class UserUpdateMeRequest(MappingByFieldName):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserUpdateRequest(MappingByFieldName):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool] = True
    role: Optional[UserRole]
