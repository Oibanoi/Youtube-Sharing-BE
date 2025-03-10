from fastapi import HTTPException
from fastapi_sqlalchemy import db

from app.helpers.video_handler import get_youtube_info_api
from app.models import Video
from app.schemas.sche_video import VideoCreateRequest


class VideoService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    def create_video(self, data: VideoCreateRequest, user_id: int) -> Video:

        if not data.video_url:
            raise HTTPException(status_code=400, detail='URL is null')
        new_video = Video(
            user_id=user_id,
            youtube_url=data.video_url,
            title="",
            description="",
        )
        video_info = get_youtube_info_api(data.video_url)
        if video_info:
            new_video.title = video_info["title"]
            new_video.description = video_info["description"]
        if not new_video.title and not new_video.description:
            raise HTTPException(status_code=400, detail='Video not found')
        db.session.add(new_video)
        db.session.commit()
        return new_video



