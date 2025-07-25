from __future__ import annotations

from typing import List

from ..models import User, Post
from ..schemas import PostCreate, PostResponse


class PostService:
    """Post 관련 비즈니스 로직"""
    
    async def create_post(self, post_data: PostCreate) -> PostResponse:
        """게시글 생성"""
        # User 존재 확인
        user = await User.get_or_none(id=post_data.user_id)
        if not user:
            raise ValueError("User not found")
        
        db_post = await Post.create(
            title=post_data.title,
            content=post_data.content,
            user_id=post_data.user_id
        )
        
        return PostResponse(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            user_id=db_post.user_id
        )
    
    async def get_posts(self, skip: int, limit: int) -> List[PostResponse]:
        """게시글 목록 조회"""
        posts = await Post.all().offset(skip).limit(limit).order_by("-id")
        return [
            PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                user_id=post.user_id
            ) for post in posts
        ]


# 싱글톤 인스턴스
post_service = PostService() 