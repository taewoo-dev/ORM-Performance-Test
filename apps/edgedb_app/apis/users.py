from fastapi import APIRouter, HTTPException, Query
from typing import List
import gel

from ..schemas import UserCreate, UserResponse, PostResponse
from ..services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
async def create_user(user: UserCreate):
    """사용자 생성"""
    try:
        return await user_service.create_user(user)
    except gel.ConstraintViolationError:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """사용자 목록 조회"""
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """단일 사용자 조회"""
    try:
        user = await user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except gel.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")


@router.get("/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """사용자의 게시글 조회"""
    try:
        posts = await user_service.get_user_posts(user_id, skip=skip, limit=limit)
        if not posts:
            # 빈 리스트인지 사용자가 없는지 확인
            user = await user_service.get_user(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return posts
    except gel.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format") 