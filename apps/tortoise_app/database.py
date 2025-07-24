from tortoise import Tortoise
import os

# Database configuration - PostgreSQL 사용
DATABASE_URL = os.getenv("TORTOISE_DATABASE_URL", "postgresql://testuser:testpass@localhost:5432/orm_test")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": 5432,
                "user": "testuser",
                "password": "testpass",
                "database": "orm_test",
                "minsize": 1,
                "maxsize": 5,  # Connection pool size
                "schema": "public",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["apps.tortoise_app.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,  # 또는 False
    "timezone": "UTC",
}

async def init_tortoise():
    """Tortoise ORM 초기화"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close_tortoise():
    """Tortoise ORM 종료"""
    await Tortoise.close_connections() 