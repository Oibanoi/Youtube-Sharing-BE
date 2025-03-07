from __future__ import annotations

from typing import List

import faker.providers
from sqlalchemy.orm import Session

from app.models.model_base import BareBaseModel


class CommonProvider(faker.providers.BaseProvider):
    @staticmethod
    def create(session: Session, models: List[BareBaseModel] | BareBaseModel = None) -> List[BareBaseModel]:
        if not models:
            models = []
        if not isinstance(models, list):
            models = [models]
        if len(models) > 0:
            session.add_all(models)
            session.commit()
        return models
