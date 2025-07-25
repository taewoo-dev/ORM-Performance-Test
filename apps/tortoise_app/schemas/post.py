from __future__ import annotations

from pydantic import BaseModel
from .frozen_config import FROZEN_CONFIG


# Post Request Models
class PostCreate(BaseModel):
    model_config = FROZEN_CONFIG

    title: str
    content: str
    user_id: int


# Post Response Models
class PostResponse(BaseModel):
    model_config = FROZEN_CONFIG

    id: int
    title: str
    content: str
    user_id: int 