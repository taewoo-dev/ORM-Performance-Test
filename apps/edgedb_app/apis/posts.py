from fastapi import APIRouter, HTTPException, Query
from typing import List
import gel

from ..schemas import PostCreate, PostResponse
from ..services.post_service import post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse)
async def create_post(post: PostCreate):
    """게시글 생성"""
    try:
        return await post_service.create_post(post)
    except gel.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except gel.MissingValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """게시글 목록 조회"""
    return await post_service.get_posts(skip=skip, limit=limit) 