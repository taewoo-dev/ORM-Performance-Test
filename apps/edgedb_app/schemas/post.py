from __future__ import annotations

from pydantic import BaseModel
from .frozen_config import FROZEN_CONFIG


# Post Request Models
class PostCreate(BaseModel):
    model_config = FROZEN_CONFIG

    title: str
    content: str
    user_id: str  # EdgeDB는 UUID를 사용


# Post Response Models
class PostResponse(BaseModel):
    model_config = FROZEN_CONFIG

    id: str
    title: str
    content: str
    user_id: str 