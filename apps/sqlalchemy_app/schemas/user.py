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

    id: int
    name: str
    email: str


class UserWithPostsResponse(BaseModel):
    model_config = FROZEN_CONFIG

    id: int
    name: str
    email: str
    posts: List[PostResponse] = [] 