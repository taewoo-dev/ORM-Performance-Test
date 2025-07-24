from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

# Database URL - PostgreSQL 사용
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://testuser:testpass@localhost:5432/orm_test")

# AsyncEngine 생성 (connection pool 설정)
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,  # Connection pool size
    max_overflow=0,
    echo=False,  # SQL 로깅 비활성화 (성능 테스트를 위해)
)

# AsyncSession 설정
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base 클래스
Base = declarative_base()

# Dependency: 데이터베이스 세션 가져오기
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 