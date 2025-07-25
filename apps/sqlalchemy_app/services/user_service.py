from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from ..models import User, Post
from ..schemas import UserCreate, UserResponse, PostResponse


class UserService:
    """User 관련 비즈니스 로직"""
    
    async def create_user(self, user_data: UserCreate, db: AsyncSession) -> UserResponse:
        """사용자 생성"""
        try:
            db_user = User(name=user_data.name, email=user_data.email)
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            raise ValueError("Email already exists")
    
    async def get_users(self, skip: int, limit: int, db: AsyncSession) -> List[UserResponse]:
        """사용자 목록 조회"""
        result = await db.execute(
            select(User).offset(skip).limit(limit).order_by(User.id)
        )
        users = result.scalars().all()
        return list(users)
    
    async def get_user(self, user_id: int, db: AsyncSession) -> Optional[UserResponse]:
        """단일 사용자 조회"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_posts(
        self, 
        user_id: int, 
        skip: int, 
        limit: int, 
        db: AsyncSession
    ) -> List[PostResponse]:
        """사용자의 게시글 조회"""
        # User 존재 확인
        user = await self.get_user(user_id, db)
        if not user:
            raise ValueError("User not found")
        
        # Posts 조회
        result = await db.execute(
            select(Post)
            .where(Post.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Post.id)
        )
        posts = result.scalars().all()
        return list(posts)


# 싱글톤 인스턴스
user_service = UserService() 