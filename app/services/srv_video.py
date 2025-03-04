import jwt

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import User, Video
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_user import UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest, UserRegisterRequest
from app.schemas.sche_video import VideoCreateRequest


class VideoService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    def create_video(self, data: VideoCreateRequest):
        new_video = Video(
            user_id=data.user_id,
            youtube_url=data.video_url,
            title="YouTube",
            description="Video description",
        )
        db.session.add(new_video)
        db.session.commit()
        return new_video



