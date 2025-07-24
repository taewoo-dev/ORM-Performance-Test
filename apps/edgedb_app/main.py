from fastapi import FastAPI, HTTPException, Query
from typing import List
import time
import edgedb

from .database import get_edgedb_client, close_edgedb_client
from .models import (
    UserCreate, UserResponse, PostCreate, PostResponse, UserWithPostsResponse
)

# FastAPI app
app = FastAPI(title="EdgeDB Performance Test")

@app.on_event("startup")
async def startup():
    # EdgeDB 클라이언트 초기화
    await get_edgedb_client()

@app.on_event("shutdown")
async def shutdown():
    await close_edgedb_client()

@app.get("/health")
async def health_check():
    return {"status": "ok", "orm": "edgedb"}

# User endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    start_time = time.time()
    client = await get_edgedb_client()
    
    try:
        result = await client.query_single(
            """
            INSERT User {
                name := <str>$name,
                email := <str>$email
            }
            """,
            name=user.name,
            email=user.email,
        )
        
        # 생성된 사용자 조회
        created_user = await client.query_single(
            """
            SELECT User {
                id,
                name,
                email
            }
            FILTER .email = <str>$email
            """,
            email=user.email,
        )
        
        creation_time = time.time() - start_time
        print(f"EdgeDB User Creation - Time: {creation_time:.4f}s")
        
        return UserResponse(
            id=str(created_user.id),
            name=created_user.name,
            email=created_user.email
        )
    except edgedb.ConstraintViolationError:
        raise HTTPException(status_code=400, detail="Email already exists")

@app.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    client = await get_edgedb_client()
    
    users = await client.query(
        """
        SELECT User {
            id,
            name,
            email
        }
        ORDER BY .id
        OFFSET <int64>$skip
        LIMIT <int64>$limit
        """,
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

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    start_time = time.time()
    client = await get_edgedb_client()
    
    try:
        user = await client.query_single(
            """
            SELECT User {
                id,
                name,
                email,
                created_at
            }
            FILTER .id = <uuid>$user_id
            """,
            user_id=user_id,
        )
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        query_time = time.time() - start_time
        print(f"EdgeDB User Get - Time: {query_time:.4f}s")
        
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )
    except edgedb.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def get_user_posts(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    client = await get_edgedb_client()
    
    try:
        # User 존재 확인 및 Posts 조회를 한 번에
        result = await client.query_single(
            """
            SELECT User {
                id,
                posts: {
                    id,
                    title,
                    content,
                    created_at
                } ORDER BY .id OFFSET <int64>$skip LIMIT <int64>$limit
            }
            FILTER .id = <uuid>$user_id
            """,
            user_id=user_id,
            skip=skip,
            limit=limit,
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
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
    except edgedb.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

# Post endpoints
@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate):
    start_time = time.time()
    client = await get_edgedb_client()
    
    try:
        result = await client.query_single(
            """
            INSERT Post {
                title := <str>$title,
                content := <str>$content,
                user := (SELECT User FILTER .id = <uuid>$user_id)
            }
            """,
            title=post.title,
            content=post.content,
            user_id=post.user_id,
        )
        
        # 생성된 게시글 조회
        created_post = await client.query_single(
            """
            SELECT Post {
                id,
                title,
                content,
                user: { id }
            }
            FILTER .title = <str>$title AND .user.id = <uuid>$user_id
            ORDER BY .id DESC
            LIMIT 1
            """,
            title=post.title,
            user_id=post.user_id,
        )
        
        creation_time = time.time() - start_time
        print(f"EdgeDB Post Creation - Time: {creation_time:.4f}s")
        
        return PostResponse(
            id=str(created_post.id),
            title=created_post.title,
            content=created_post.content,
            user_id=str(created_post.user.id)
        )
    except edgedb.InvalidValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except edgedb.MissingValueError:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    start_time = time.time()
    client = await get_edgedb_client()
    
    posts = await client.query(
        """
        SELECT Post {
            id,
            title,
            content,
            user: { id }
        }
        ORDER BY .id DESC
        OFFSET <int64>$skip
        LIMIT <int64>$limit
        """,
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

# EdgeDB 성능 테스트용 엔드포인트
@app.get("/benchmark/edgedb-native")
async def benchmark_edgedb_native():
    """EdgeDB 네이티브 쿼리 성능 테스트"""
    start_time = time.time()
    client = await get_edgedb_client()
    
    # 여러 번의 쿼리 테스트
    for i in range(10):
        query_start = time.time()
        
        # 간단한 카운트 쿼리
        count = await client.query_single("SELECT count(User)")
        
        query_time = time.time() - query_start
        print(f"EdgeDB native query #{i+1} - Time: {query_time:.4f}s")
    
    total_time = time.time() - start_time
    avg_time = total_time / 10
    
    return {
        "total_queries": 10,
        "total_time": total_time,
        "average_query_time": avg_time,
        "queries_per_second": 10 / total_time
    } 