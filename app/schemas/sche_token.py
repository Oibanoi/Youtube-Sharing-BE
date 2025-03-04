from typing import Optional

from pydantic import BaseModel

from app.schemas.sche_base import MappingByFieldName


class Token(MappingByFieldName):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(MappingByFieldName):
    user_id: Optional[int] = None
