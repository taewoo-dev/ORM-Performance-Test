from fastapi import FastAPI

from .database import get_edgedb_client, close_edgedb_client
from .apis import health, users, posts

# FastAPI app
app = FastAPI(title="EdgeDB Performance Test")

# 라우터 등록
app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)



@app.on_event("startup")
async def startup():
    """앱 시작 시 EdgeDB 클라이언트 초기화"""
    await get_edgedb_client()


@app.on_event("shutdown")
async def shutdown():
    """앱 종료 시 EdgeDB 클라이언트 정리"""
    await close_edgedb_client() 