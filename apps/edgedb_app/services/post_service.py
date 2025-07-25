import time
import uuid
from typing import List

from ..database import get_edgedb_client
from ..queries.post.create_post_async_edgeql import create_post as create_post_query
from ..queries.post.get_posts_async_edgeql import get_posts as get_posts_query
from ..schemas import PostCreate, PostResponse


class PostService:
    """게시글 관련 비즈니스 로직"""
    
    async def create_post(self, post: PostCreate) -> PostResponse:
        """게시글 생성"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 create_post_query 함수 사용
        created_post = await create_post_query(
            client,
            title=post.title,
            content=post.content,
            user_id=uuid.UUID(post.user_id),
        )
        
        creation_time = time.time() - start_time
        print(f"EdgeDB Post Creation - Time: {creation_time:.4f}s")
        
        return PostResponse(
            id=str(created_post.id),
            title=created_post.title,
            content=created_post.content,
            user_id=str(created_post.user.id)
        )
    
    async def get_posts(self, skip: int = 0, limit: int = 10) -> List[PostResponse]:
        """게시글 목록 조회"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # gel CLI로 생성된 get_posts_query 함수 사용
        posts = await get_posts_query(
            client,
            skip=skip,
            limit=limit,
        )
        
        query_time = time.time() - start_time
        print(f"EdgeDB Posts Query - Time: {query_time:.4f}s, Count: {len(posts)}")
        
        return [
            PostResponse(
                id=str(post.id),
                title=post.title,
                content=post.content,
                user_id=str(post.user.id)
            ) for post in posts
        ]


# 싱글톤 인스턴스
post_service = PostService() 