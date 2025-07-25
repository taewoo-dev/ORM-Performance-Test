from __future__ import annotations

from pydantic import BaseModel
from typing import List
from .frozen_config import FROZEN_CONFIG


# User Request Models
class UserCreate(BaseModel):
    model_config = FROZEN_CONFIG

    name: str
    email: str


# User Response Models  
class UserResponse(BaseModel):
    model_config = FROZEN_CONFIG

    id: str
    name: str
    email: str


class UserWithPostsResponse(BaseModel):
    model_config = FROZEN_CONFIG

    id: str
    name: str
    email: str
    posts: List[PostResponse] = []


# Future annotations을 사용하므로 TYPE_CHECKING이 필요 없음
# model_rebuild도 필요 없음 