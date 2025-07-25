import time
import uuid
from typing import List, Optional

from ..database import get_edgedb_client
from ..queries.user.insert_user_async_edgeql import insert_user
from ..queries.user.get_users_async_edgeql import get_users as get_users_query
from ..queries.user.get_user_async_edgeql import get_user as get_user_query
from ..queries.user.get_user_posts_async_edgeql import get_user_posts as get_user_posts_query
from ..schemas import UserCreate, UserResponse, PostResponse


class UserService:
    """사용자 관련 비즈니스 로직"""
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        """사용자 생성"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 insert_user 함수 사용
        created_user = await insert_user(
            client,
            name=user.name,
            email=user.email,
        )
        
        creation_time = time.time() - start_time
        print(f"EdgeDB User Creation - Time: {creation_time:.4f}s")
        
        return UserResponse(
            id=str(created_user.id),
            name=created_user.name,
            email=created_user.email
        )
    
    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        """사용자 목록 조회"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 get_users_query 함수 사용
        users = await get_users_query(
            client,
            skip=skip,
            limit=limit,
        )
        
        query_time = time.time() - start_time
        print(f"EdgeDB Users Query - Time: {query_time:.4f}s, Count: {len(users)}")
        
        return [
            UserResponse(
                id=str(user.id),
                name=user.name,
                email=user.email
            ) for user in users
        ]
    
    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        """단일 사용자 조회"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 get_user_query 함수 사용
        user = await get_user_query(
            client,
            user_id=uuid.UUID(user_id),
        )
        
        if not user:
            return None
        
        query_time = time.time() - start_time
        print(f"EdgeDB User Get - Time: {query_time:.4f}s")
        
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )
    
    async def get_user_posts(self, user_id: str, skip: int = 0, limit: int = 10) -> List[PostResponse]:
        """사용자의 게시글 조회"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 get_user_posts_query 함수 사용
        result = await get_user_posts_query(
            client,
            user_id=uuid.UUID(user_id),
            skip=skip,
            limit=limit,
        )
        
        if not result:
            return []
        
        query_time = time.time() - start_time
        print(f"EdgeDB User Posts Query - Time: {query_time:.4f}s, Count: {len(result.posts)}")
        
        return [
            PostResponse(
                id=str(post.id),
                title=post.title,
                content=post.content,
                user_id=user_id
            ) for post in result.posts
        ]


# 싱글톤 인스턴스
user_service = UserService() 