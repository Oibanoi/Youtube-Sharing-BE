from sqlalchemy import Column, String, Boolean, DateTime

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
