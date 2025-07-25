import time
from typing import Dict, Any

from ..database import get_edgedb_client


class BenchmarkService:
    """벤치마크 관련 비즈니스 로직"""
    
    async def run_edgedb_native_benchmark(self) -> Dict[str, Any]:
        """EdgeDB 네이티브 쿼리 성능 테스트"""
        start_time = time.time()
        client = await get_edgedb_client()
        
        # 여러 번의 쿼리 테스트
        for i in range(10):
            query_start = time.time()
            
            # 간단한 카운트 쿼리
            count = await client.query_single("SELECT count(User)")
            
            query_time = time.time() - query_start
            print(f"EdgeDB native query #{i+1} - Time: {query_time:.4f}s")
        
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