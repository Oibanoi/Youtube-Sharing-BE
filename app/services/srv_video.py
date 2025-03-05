from fastapi_sqlalchemy import db

from app.helpers.video_handler import get_youtube_info_api
from app.models import Video
from app.schemas.sche_video import VideoCreateRequest


class VideoService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    def create_video(self, data: VideoCreateRequest):
        new_video = Video(
            user_id=data.user_id,
            youtube_url=data.video_url,
            title="title",
            description="description",
        )
        video_info = get_youtube_info_api(data.video_url)
        if video_info:
            new_video.title = video_info["title"]
            new_video.description = video_info["description"]
        db.session.add(new_video)
        db.session.commit()
        return new_video



