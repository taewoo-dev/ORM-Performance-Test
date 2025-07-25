from __future__ import annotations

from fastapi import FastAPI

from .database import engine
from .models import Base
from .apis import health, users, posts, benchmark

# FastAPI app
app = FastAPI(title="SQLAlchemy v2 Performance Test")

# 라우터 등록
app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(benchmark.router)


@app.on_event("startup")
async def startup():
    """앱 시작 시 테이블 생성"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 