from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import time
from datetime import datetime, timezone
from tortoise.exceptions import IntegrityError

from .database import init_tortoise, close_tortoise
from .models import User, Post

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Tortoise ORM Performance Test")

@app.on_event("startup")
async def startup():
    await init_tortoise()

@app.on_event("shutdown")
async def shutdown():
    await close_tortoise()

@app.get("/health")
async def health_check():
    return {"status": "ok", "orm": "tortoise"}

# User endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    start_time = time.time()
    try:
        db_user = await User.create(
            name=user.name, 
            email=user.email,
            created_at=datetime.now(timezone.utc)  # timezone-naive
        )
        
        creation_time = time.time() - start_time
        print(f"Tortoise User Creation - Time: {creation_time:.4f}s")
        
        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")

@app.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    
    users = await User.all().offset(skip).limit(limit).order_by("id")
    
    query_time = time.time() - start_time
    print(f"Tortoise Users Query - Time: {query_time:.4f}s, Count: {len(users)}")
    
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        ) for user in users
    ]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    start_time = time.time()
    
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query_time = time.time() - start_time
    print(f"Tortoise User Get - Time: {query_time:.4f}s")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    
    # User 존재 확인
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Posts 조회
    posts = await Post.filter(user_id=user_id).offset(skip).limit(limit).order_by("id")
    
    query_time = time.time() - start_time
    print(f"Tortoise User Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
    
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            user_id=post.user_id
        ) for post in posts
    ]

# Post endpoints
@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate):
    start_time = time.time()
    
    # User 존재 확인
    user = await User.get_or_none(id=post.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_post = await Post.create(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )
    
    creation_time = time.time() - start_time
    print(f"Tortoise Post Creation - Time: {creation_time:.4f}s")
    
    return PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        user_id=db_post.user_id
    )

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    
    posts = await Post.all().offset(skip).limit(limit).order_by("-id")
    
    query_time = time.time() - start_time
    print(f"Tortoise Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
    
    return [
        PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            user_id=post.user_id
        ) for post in posts
    ]

# Native async 성능 테스트용 엔드포인트
@app.get("/benchmark/native-async")
async def benchmark_native_async():
    """네이티브 비동기 성능 테스트"""
    start_time = time.time()
    
    # 여러 번의 쿼리 테스트
    for i in range(10):
        query_start = time.time()
        
        # 간단한 카운트 쿼리
        count = await User.all().count()
        
        query_time = time.time() - query_start
        print(f"Tortoise native async query #{i+1} - Time: {query_time:.4f}s")
    
    total_time = time.time() - start_time
    avg_time = total_time / 10
    
    return {
        "total_queries": 10,
        "total_time": total_time,
        "average_query_time": avg_time,
        "queries_per_second": 10 / total_time
    } 