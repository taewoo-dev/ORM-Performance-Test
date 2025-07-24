#!/usr/bin/env python3
"""
ORM 성능 테스트 실행 스크립트
각 ORM별로 동일한 조건에서 성능 테스트를 실행하고 결과를 비교합니다.
"""

import subprocess
import time
import json
import os
from datetime import datetime
from pathlib import Path

class PerformanceTestRunner:
    def __init__(self):
        self.test_config = {
            "users": 20,  # RPS 20에 맞춤
            "spawn_rate": 5,  # 초당 5명씩 생성
            "run_time": "2m",  # 2분간 테스트
            "processes": 4  # 워커 4개
        }
        
        self.orm_configs = {
            "sqlalchemy": {
                "port": 8001,
                "name": "SQLAlchemy v2",
                "description": "greenlet을 사용한 동기→비동기 변환"
            },
            "tortoise": {
                "port": 8002,
                "name": "Tortoise ORM",
                "description": "네이티브 비동기 ORM"
            },
            "edgedb": {
                "port": 8003,
                "name": "EdgeDB",
                "description": "차세대 관계형 데이터베이스"
            }
        }
        
        self.results = {}

    def check_server_health(self, port):
        """서버 상태 확인"""
        import requests
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def run_locust_test(self, orm_name, port):
        """특정 ORM에 대해 Locust 테스트 실행"""
        print(f"\n{'='*50}")
        print(f"Testing {self.orm_configs[orm_name]['name']}")
        print(f"Description: {self.orm_configs[orm_name]['description']}")
        print(f"Port: {port}")
        print(f"{'='*50}")
        
        # 서버 상태 확인
        if not self.check_server_health(port):
            print(f"❌ Server at port {port} is not responding. Skipping {orm_name}.")
            return None
        
        # Locust 명령어 구성
        cmd = [
            "locust",
            "-f", "tests/locust_tests/locust_test.py",
            f"--host=http://localhost:{port}",
            f"--users={self.test_config['users']}",
            f"--spawn-rate={self.test_config['spawn_rate']}",
            f"--run-time={self.test_config['run_time']}",
            f"--processes={self.test_config['processes']}",
            "--headless",
            "--print-stats",
            "--only-summary",
            f"--html=results/{orm_name}_report.html",
            f"--csv=results/{orm_name}"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        try:
            # 결과 디렉토리 생성
            os.makedirs("results", exist_ok=True)
            
            # Locust 실행
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5분 타임아웃
            )
            
            if result.returncode == 0:
                print(f"✅ {orm_name} test completed successfully")
                
                # 결과 파싱
                output_lines = result.stdout.split('\n')
                stats = self.parse_locust_output(output_lines)
                stats['orm'] = orm_name
                stats['description'] = self.orm_configs[orm_name]['description']
                
                return stats
            else:
                print(f"❌ {orm_name} test failed")
                print(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ {orm_name} test timed out")
            return None
        except Exception as e:
            print(f"❌ {orm_name} test error: {e}")
            return None

    def parse_locust_output(self, output_lines):
        """Locust 출력에서 통계 파싱"""
        stats = {
            "total_requests": 0,
            "failures": 0,
            "avg_response_time": 0,
            "p95_response_time": 0,
            "p99_response_time": 0,
            "rps": 0,
            "failure_rate": 0
        }
        
        # 출력에서 통계 추출 (실제 Locust 출력 형식에 맞게 조정 필요)
        for line in output_lines:
            if "Total requests" in line or "Aggregated" in line:
                # 요청 수, 실패율, 응답시간 등 파싱
                # 실제 구현시 정확한 파싱 로직 필요
                pass
        
        return stats

    def run_all_tests(self):
        """모든 ORM에 대해 테스트 실행"""
        print("🚀 Starting ORM Performance Tests")
        print(f"Configuration: {self.test_config}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        for orm_name, config in self.orm_configs.items():
            result = self.run_locust_test(orm_name, config["port"])
            if result:
                self.results[orm_name] = result
            
            # 테스트 간 대기
            time.sleep(10)
        
        # 결과 저장 및 출력
        self.save_results()
        self.print_comparison()

    def save_results(self):
        """결과를 JSON 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/performance_comparison_{timestamp}.json"
        
        os.makedirs("results", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "test_config": self.test_config,
                "results": self.results
            }, f, indent=2)
        
        print(f"\n📊 Results saved to: {filename}")

    def print_comparison(self):
        """결과 비교 출력"""
        if not self.results:
            print("❌ No results to compare")
            return
        
        print("\n" + "="*80)
        print("🏆 PERFORMANCE COMPARISON RESULTS")
        print("="*80)
        
        # 헤더
        print(f"{'ORM':<15} {'P95 (ms)':<10} {'RPS':<8} {'Failure Rate':<12} {'Description'}")
        print("-" * 80)
        
        # 각 ORM 결과 출력
        for orm_name, stats in self.results.items():
            print(f"{stats['orm'].upper():<15} "
                  f"{stats.get('p95_response_time', 'N/A'):<10} "
                  f"{stats.get('rps', 'N/A'):<8} "
                  f"{stats.get('failure_rate', 'N/A'):<12} "
                  f"{stats['description']}")
        
        print("="*80)
        
        # 승자 결정 (P95 기준)
        if len(self.results) > 1:
            p95_results = {orm: stats.get('p95_response_time', float('inf')) 
                          for orm, stats in self.results.items() 
                          if isinstance(stats.get('p95_response_time'), (int, float))}
            
            if p95_results:
                winner = min(p95_results.keys(), key=lambda x: p95_results[x])
                print(f"🏆 P95 응답시간 기준 우승자: {winner.upper()}")
                print(f"   응답시간: {p95_results[winner]:.2f}ms")

def main():
    """메인 실행 함수"""
    print("🔧 ORM Performance Test Runner")
    print("Make sure all servers are running before starting tests:")
    print("  - SQLAlchemy: http://localhost:8001")
    print("  - Tortoise:   http://localhost:8002") 
    print("  - EdgeDB:     http://localhost:8003")
    print()
    
    input("Press Enter to start tests...")
    
    runner = PerformanceTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main() 