from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from ..schemas import UserCreate, UserResponse, PostResponse
from ..database import get_db
from ..services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """사용자 생성"""
    try:
        result = await user_service.create_user(user, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """사용자 목록 조회"""
    users = await user_service.get_users(skip, limit, db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """단일 사용자 조회"""
    user = await user_service.get_user(user_id, db)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """사용자의 게시글 조회"""
    try:
        posts = await user_service.get_user_posts(user_id, skip, limit, db)
        return posts
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 