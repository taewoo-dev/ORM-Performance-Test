from fastapi import APIRouter
from typing import Dict, Any

from ..services.benchmark_service import benchmark_service

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


@router.get("/edgedb-native")
async def benchmark_edgedb_native() -> Dict[str, Any]:
    """EdgeDB 네이티브 쿼리 성능 테스트"""
    return await benchmark_service.run_edgedb_native_benchmark() 