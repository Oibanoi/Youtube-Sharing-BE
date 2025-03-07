import logging
import faker.providers

from app.helpers.enums import UserRole
from app.models import User, Video
from fastapi_sqlalchemy import db
from app.core.security import get_password_hash

logger = logging.getLogger()
fake = faker.Faker()


class VideoProvider(faker.providers.BaseProvider):
    @staticmethod
    def video(data={}):
        """
        Fake a video in db for testing
        :return: user model object
        """
        videos =(
        Video(
            title=data.get('title'),
            description=data.get('description'),
            youtube_url=data.get('youtube_url'),
            user_id=data.get('user_id'),
        ))
        with db():
            db.session.add(videos)
            db.session.commit()
            db.session.refresh(videos)
        return videos
