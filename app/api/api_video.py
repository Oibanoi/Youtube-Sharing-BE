import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi_sqlalchemy import db

from app.core.ws_manager import WebSocketManager
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required
from app.helpers.paging import Page, PaginationParams, paginate
from app.models import User, Video
from app.schemas.sche_base import DataResponse
from app.schemas.sche_video import VideoItemResponse, VideoCreateRequest
from app.services.srv_user import UserService
from app.services.srv_video import VideoService

logger = logging.getLogger()
router = APIRouter()

ws_manager = WebSocketManager()

@router.get("", dependencies=[Depends(login_required)], response_model=Page[VideoItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Video
    """
    try:
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

async def send_noti(video_data:VideoItemResponse):
    message= "User :{} just post new video {}".format(video_data.user_name,video_data.title)
    print(message)
    await ws_manager.broadcast(message)

@router.post("", dependencies=[Depends(login_required)], response_model=DataResponse[VideoItemResponse])
def create(video_data: VideoCreateRequest, background_tasks: BackgroundTasks, video_service: VideoService = Depends(), current_user: User = Depends(login_required)) -> Any:
    """
    API Create video
    """
    try:
        new_video = video_service.create_video(video_data, current_user.id)
        resp:VideoItemResponse = VideoItemResponse(
            id=new_video.id,
            title=new_video.title,
            description=new_video.description,
            user_name=current_user.email,
            youtube_url=new_video.youtube_url,
        )
        background_tasks.add_task(send_noti, resp)
        return DataResponse().success_response(data=resp)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


