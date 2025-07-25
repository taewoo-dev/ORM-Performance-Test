from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..models import User, Post
from ..schemas import PostCreate, PostResponse


class PostService:
    """Post 관련 비즈니스 로직"""
    
    async def create_post(self, post_data: PostCreate, db: AsyncSession) -> PostResponse:
        """게시글 생성"""
        # User 존재 확인
        result = await db.execute(select(User).where(User.id == post_data.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("User not found")
        
        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            user_id=post_data.user_id
        )
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    
    async def get_posts(self, skip: int, limit: int, db: AsyncSession) -> List[PostResponse]:
        """게시글 목록 조회"""
        result = await db.execute(
            select(Post).offset(skip).limit(limit).order_by(Post.id.desc())
        )
        posts = result.scalars().all()
        return list(posts)


# 싱글톤 인스턴스
post_service = PostService() 