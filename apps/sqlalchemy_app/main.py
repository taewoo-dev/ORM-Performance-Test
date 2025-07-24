from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
import time
from datetime import datetime

from .database import engine, get_db, Base
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
app = FastAPI(title="SQLAlchemy v2 Performance Test")

@app.on_event("startup")
async def startup():
    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "ok", "orm": "sqlalchemy_v2"}

# User endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    try:
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        # greenlet 변환 시간 측정
        conversion_time = time.time() - start_time
        print(f"SQLAlchemy User Creation - Total time: {conversion_time:.4f}s")
        
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

@app.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    
    # SQLAlchemy v2 async query
    result = await db.execute(
        select(User).offset(skip).limit(limit).order_by(User.id)
    )
    users = result.scalars().all()
    
    query_time = time.time() - start_time
    print(f"SQLAlchemy Users Query - Time: {query_time:.4f}s, Count: {len(users)}")
    
    return list(users)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    start_time = time.time()
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query_time = time.time() - start_time
    print(f"SQLAlchemy User Get - Time: {query_time:.4f}s")
    
    return user

@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    
    # User 존재 확인
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Posts 조회
    result = await db.execute(
        select(Post)
        .where(Post.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Post.id)
    )
    posts = result.scalars().all()
    
    query_time = time.time() - start_time
    print(f"SQLAlchemy User Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
    
    return list(posts)

# Post endpoints
@app.post("/posts", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    
    # User 존재 확인
    result = await db.execute(select(User).where(User.id == post.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    
    creation_time = time.time() - start_time
    print(f"SQLAlchemy Post Creation - Time: {creation_time:.4f}s")
    
    return db_post

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    
    result = await db.execute(
        select(Post).offset(skip).limit(limit).order_by(Post.id.desc())
    )
    posts = result.scalars().all()
    
    query_time = time.time() - start_time
    print(f"SQLAlchemy Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
    
    return list(posts)

# Greenlet 성능 테스트용 엔드포인트
@app.get("/benchmark/sync-to-async")
async def benchmark_sync_to_async(db: AsyncSession = Depends(get_db)):
    """Greenlet을 통한 동기→비동기 변환 성능 테스트"""
    start_time = time.time()
    
    # 여러 번의 변환 테스트
    for i in range(10):
        conversion_start = time.time()
        
        # 간단한 쿼리를 동기식으로 실행 (greenlet 변환)
        async with engine.begin() as conn:
            result = await conn.run_sync(
                lambda sync_conn: sync_conn.execute(select(func.count(User.id))).scalar()
            )
        
        conversion_time = time.time() - conversion_start
        print(f"Greenlet conversion #{i+1} - Time: {conversion_time:.4f}s")
    
    total_time = time.time() - start_time
    avg_time = total_time / 10
    
    return {
        "total_conversions": 10,
        "total_time": total_time,
        "average_conversion_time": avg_time,
        "conversions_per_second": 10 / total_time
    } 