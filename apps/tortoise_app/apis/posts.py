from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import List
import time

from ..schemas import PostCreate, PostResponse
from ..services.post_service import post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse)
async def create_post(post: PostCreate):
    """게시글 생성"""
    start_time = time.time()
    
    try:
        result = await post_service.create_post(post)
        
        creation_time = time.time() - start_time
        print(f"Tortoise Post Creation - Time: {creation_time:.4f}s")
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """게시글 목록 조회"""
    start_time = time.time()
    
    posts = await post_service.get_posts(skip, limit)
    
    query_time = time.time() - start_time
    print(f"Tortoise Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
    
    return posts 