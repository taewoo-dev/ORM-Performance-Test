from __future__ import annotations

from typing import Dict, Any
import time

from ..models import User


class BenchmarkService:
    """벤치마크 관련 비즈니스 로직"""
    
    async def run_native_async_benchmark(self) -> Dict[str, Any]:
        """네이티브 비동기 성능 테스트"""
        start_time = time.time()
        
        # 여러 번의 쿼리 테스트
        for i in range(10):
            query_start = time.time()
            
            # 간단한 카운트 쿼리
            count = await User.all().count()
            
            query_time = time.time() - query_start
            print(f"Tortoise native async query #{i+1} - Time: {query_time:.4f}s")
        
        total_time = time.time() - start_time
        avg_time = total_time / 10
        
        return {
            "total_queries": 10,
            "total_time": total_time,
            "average_query_time": avg_time,
            "queries_per_second": 10 / total_time
        }


# 싱글톤 인스턴스
benchmark_service = BenchmarkService() 