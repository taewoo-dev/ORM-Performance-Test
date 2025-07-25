from __future__ import annotations

from sqlalchemy import select, func
from typing import Dict, Any
import time

from ..database import engine
from ..models import User


class BenchmarkService:
    """벤치마크 관련 비즈니스 로직"""
    
    async def run_sync_to_async_benchmark(self) -> Dict[str, Any]:
        """Greenlet을 통한 동기→비동기 변환 성능 테스트"""
        start_time = time.time()
        
        # 여러 번의 변환 테스트
        for i in range(10):
            conversion_start = time.time()
            
            # 간단한 쿼리를 동기식으로 실행 (greenlet 변환)
            async with engine.begin() as conn:
                result = await conn.run_sync(
                    lambda sync_conn: sync_conn.execute(select(func.count(User.id))).scalar()
                )
            
            conversion_time = time.time() - conversion_start
            print(f"Greenlet conversion #{i+1} - Time: {conversion_time:.4f}s")
        
        total_time = time.time() - start_time
        avg_time = total_time / 10
        
        return {
            "total_conversions": 10,
            "total_time": total_time,
            "average_conversion_time": avg_time,
            "conversions_per_second": 10 / total_time
        }


# 싱글톤 인스턴스
benchmark_service = BenchmarkService() 