from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import List
import time

from ..schemas import UserCreate, UserResponse, PostResponse
from ..services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(user: UserCreate):
    """사용자 생성"""
    start_time = time.time()
    try:
        result = await user_service.create_user(user)
        
        creation_time = time.time() - start_time
        print(f"Tortoise User Creation - Time: {creation_time:.4f}s")
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """사용자 목록 조회"""
    start_time = time.time()
    
    users = await user_service.get_users(skip, limit)
    
    query_time = time.time() - start_time
    print(f"Tortoise Users Query - Time: {query_time:.4f}s, Count: {len(users)}")
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """단일 사용자 조회"""
    start_time = time.time()
    
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query_time = time.time() - start_time
    print(f"Tortoise User Get - Time: {query_time:.4f}s")
    
    return user


@router.get("/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """사용자의 게시글 조회"""
    start_time = time.time()
    
    try:
        posts = await user_service.get_user_posts(user_id, skip, limit)
        
        query_time = time.time() - start_time
        print(f"Tortoise User Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
        
        return posts
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 