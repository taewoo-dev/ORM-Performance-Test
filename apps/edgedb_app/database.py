import edgedb
import os
from typing import Optional

# EdgeDB connection pool
_client: Optional[edgedb.AsyncIOClient] = None

async def get_edgedb_client() -> edgedb.AsyncIOClient:
    """EdgeDB 클라이언트 생성 또는 기존 클라이언트 반환"""
    global _client
    if _client is None:
        # EdgeDB 연결 설정
        _client = edgedb.create_async_client(
            # Docker EdgeDB 인스턴스 연결
            host="localhost",
            port=5656,
            # Connection pool 설정
            max_concurrency=5,
            # TLS 비활성화 (개발 환경용)
            tls_security="insecure",
            database="edgedb"
        )
    return _client

async def close_edgedb_client():
    """EdgeDB 클라이언트 종료"""
    global _client
    if _client:
        await _client.aclose()
        _client = None 