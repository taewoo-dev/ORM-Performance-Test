from __future__ import annotations

from fastapi import FastAPI

from .database import init_tortoise, close_tortoise
from .apis import health, users, posts

# FastAPI app
app = FastAPI(title="Tortoise ORM Performance Test")

# 라우터 등록
app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)



@app.on_event("startup")
async def startup():
    """앱 시작 시 Tortoise ORM 초기화"""
    await init_tortoise()


@app.on_event("shutdown")
async def shutdown():
    """앱 종료 시 Tortoise ORM 정리"""
    await close_tortoise() 