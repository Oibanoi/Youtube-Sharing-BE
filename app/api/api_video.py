import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse, UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest
from app.schemas.sche_video import VideoItemResponse, VideoCreateRequest
from app.services.srv_user import UserService
from app.models import User, Video
from app.services.srv_video import VideoService

logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(login_required)], response_model=Page[VideoItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Video
    """
    try:
        # _query = db.session.query(User)
        _query = db.session.query(
            Video.id,
            Video.youtube_url,
            Video.title,
            Video.description,
            User.email.label("user_name")  # Đổi user_id thành username
        ).join(User, Video.user_id == User.id)
        videos = paginate(model=User, query=_query, params=params)
        return videos
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))


@router.post("", dependencies=[Depends(login_required)], response_model=DataResponse[VideoItemResponse])
def create(video_data: VideoCreateRequest, video_service: VideoService = Depends()) -> Any:
    """
    API Create User
    """
    try:
        new_video = video_service.create_video(video_data)
        return DataResponse().success_response(data=new_video)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


