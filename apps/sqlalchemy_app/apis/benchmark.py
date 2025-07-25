from __future__ import annotations

from fastapi import APIRouter
from typing import Dict, Any

from ..services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


@router.get("/sync-to-async")
async def benchmark_sync_to_async() -> Dict[str, Any]:
    """Greenlet을 통한 동기→비동기 변환 성능 테스트"""
    return await benchmark_service.run_sync_to_async_benchmark() 