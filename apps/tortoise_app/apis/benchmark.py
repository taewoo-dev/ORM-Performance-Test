from __future__ import annotations

from fastapi import APIRouter
from typing import Dict, Any

from ..services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


@router.get("/native-async")
async def benchmark_native_async() -> Dict[str, Any]:
    """네이티브 비동기 성능 테스트"""
    return await benchmark_service.run_native_async_benchmark() 