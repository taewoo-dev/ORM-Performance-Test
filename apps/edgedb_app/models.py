from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

# Request models
class UserCreate(BaseModel):
    name: str
    email: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: str  # EdgeDB는 UUID를 사용

# Response models
class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    user_id: str

class UserWithPostsResponse(BaseModel):
    id: str
    name: str
    email: str
    posts: List[PostResponse] = [] 