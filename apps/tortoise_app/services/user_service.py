from __future__ import annotations

from tortoise.exceptions import IntegrityError
from typing import List, Optional

from ..models import User, Post
from ..schemas import UserCreate, UserResponse, PostResponse


class UserService:
    """User 관련 비즈니스 로직"""
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """사용자 생성"""
        try:
            db_user = await User.create(
                name=user_data.name, 
                email=user_data.email
            )
            return UserResponse(
                id=db_user.id,
                name=db_user.name,
                email=db_user.email
            )
        except IntegrityError:
            raise ValueError("Email already exists")
    
    async def get_users(self, skip: int, limit: int) -> List[UserResponse]:
        """사용자 목록 조회"""
        users = await User.all().offset(skip).limit(limit).order_by("id")
        return [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email
            ) for user in users
        ]
    
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """단일 사용자 조회"""
        user = await User.get_or_none(id=user_id)
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    
    async def get_user_posts(
        self, 
        user_id: int, 
        skip: int, 
        limit: int
    ) -> List[PostResponse]:
        """사용자의 게시글 조회"""
        # User 존재 확인
        user = await User.get_or_none(id=user_id)
        if not user:
            raise ValueError("User not found")
        
        # Posts 조회
        posts = await Post.filter(user_id=user_id).offset(skip).limit(limit).order_by("id")
        return [
            PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                user_id=post.user_id
            ) for post in posts
        ]


# 싱글톤 인스턴스
user_service = UserService() 