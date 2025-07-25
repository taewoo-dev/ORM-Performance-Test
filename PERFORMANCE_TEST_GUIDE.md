# FastAPI ORM 성능 테스트 가이드

> 📋 **기본 설정 및 서버 실행**: [QUICK_START.md](QUICK_START.md) 먼저 완료 필요  
> 📊 **프로젝트 개요**: [README.md](README.md) 참조

## 🎯 **성능 테스트 개요**

이 가이드는 **SQLAlchemy v2**, **Tortoise ORM**, **EdgeDB**의 실제 성능을 측정하고 비교하는 방법을 제공합니다.

### **테스트 조건**
- **성능 지표**: P95 응답시간, 평균 QPS
- **목표 RPS**: 20 (실제 운영 환경 시나리오)
- **Connection Pool**: 각 ORM별 최적화된 설정
- **테스트 도구**: Locust + 내장 벤치마크

## 📊 **1. 개별 벤치마크 테스트**

각 ORM의 내장 벤치마크를 실행하여 기본 성능을 측정합니다.

### SQLAlchemy v2 - Greenlet 성능
```bash
# Greenlet 기반 sync-to-async 변환 성능
curl http://localhost:8001/benchmark/sync-to-async

# 예상 결과:
# {
#   "total_conversions": 10,
#   "total_time": 0.028,
#   "average_conversion_time": 0.0028,
#   "conversions_per_second": 357
# }
```

### Tortoise ORM - 네이티브 비동기 성능
```bash
# 네이티브 비동기 쿼리 성능
curl http://localhost:8002/benchmark/native-async

# 예상 결과:
# {
#   "total_queries": 10,
#   "total_time": 0.024,
#   "average_query_time": 0.0024,
#   "queries_per_second": 412
# }
```

### EdgeDB - 네이티브 EdgeQL 성능
```bash
# EdgeQL 네이티브 쿼리 성능
curl http://localhost:8003/benchmark/edgedb-native

# 예상 결과:
# {
#   "total_queries": 10,
#   "total_time": 0.019,
#   "average_query_time": 0.0019,
#   "queries_per_second": 525
# }
```

## 🔥 **2. API 엔드포인트 성능 테스트**

실제 CRUD 작업의 성능을 측정합니다.

### 사용자 생성 성능 비교
```bash
# SQLAlchemy v2
time curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "User1", "email": "user1@test.com"}'

# Tortoise ORM  
time curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"name": "User2", "email": "user2@test.com"}'

# EdgeDB
time curl -X POST http://localhost:8003/users \
  -H "Content-Type: application/json" \
  -d '{"name": "User3", "email": "user3@test.com"}'
```

### 사용자 조회 성능 비교
```bash
# 각 ORM별 사용자 목록 조회
curl http://localhost:8001/users
curl http://localhost:8002/users  
curl http://localhost:8003/users
```

## 🚀 **3. Locust 부하 테스트**

실제 부하 상황에서의 성능을 측정합니다.

### 테스트 준비
```bash
cd tests/locust_tests

# 모든 ORM 서버가 실행 중인지 확인
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### SQLAlchemy v2 부하 테스트
```bash
# 20 RPS로 60초간 테스트
locust -f locust_test.py SQLAlchemyUser -H http://localhost:8001 \
  --users 20 --spawn-rate 2 --run-time 60s --headless

# 결과 분석 포인트:
# - P95 응답시간
# - 평균 RPS
# - 에러율
```

### Tortoise ORM 부하 테스트
```bash
# 동일 조건으로 테스트
locust -f locust_test.py TortoiseUser -H http://localhost:8002 \
  --users 20 --spawn-rate 2 --run-time 60s --headless
```

### EdgeDB 부하 테스트
```bash
# 동일 조건으로 테스트
locust -f locust_test.py EdgeDBUser -H http://localhost:8003 \
  --users 20 --spawn-rate 2 --run-time 60s --headless
```

## 📈 **4. 성능 분석 가이드**

### 측정 지표 해석

| 지표 | 의미 | 목표값 |
|------|------|--------|
| **평균 응답시간** | 일반적인 성능 | < 50ms |
| **P95 응답시간** | 최악의 5% 케이스 | < 200ms |
| **RPS** | 초당 처리 요청 수 | > 100 |
| **에러율** | 실패한 요청 비율 | < 1% |

### 성능 비교 체크리스트

```bash
# 1. 메모리 사용량 비교
ps aux | grep uvicorn

# 2. CPU 사용률 모니터링  
top -p $(pgrep -f "uvicorn.*8001|uvicorn.*8002|uvicorn.*8003")

# 3. 데이터베이스 연결 수 확인
# PostgreSQL
docker exec orm_test_postgres psql -U testuser -d orm_test \
  -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# EdgeDB  
docker exec orm_test_edgedb edgedb query "SELECT count(sys::ClientConnectionInfo)"
```

## 🔍 **5. 상세 프로파일링**

성능 병목 지점을 찾기 위한 세부 분석:

### Python 프로파일링
```bash
# cProfile을 이용한 세부 분석
poetry run python -m cProfile -o profile_sqlalchemy.prof \
  -c "import apps.sqlalchemy_app.main"

# 결과 분석
poetry run python -c "
import pstats
stats = pstats.Stats('profile_sqlalchemy.prof')
stats.sort_stats('cumtime').print_stats(10)
"
```

### 데이터베이스 쿼리 분석
```bash
# PostgreSQL 슬로우 쿼리 로그 활성화
docker exec orm_test_postgres psql -U testuser -d orm_test \
  -c "ALTER SYSTEM SET log_min_duration_statement = 10;"
```

## 📊 **6. 결과 정리 템플릿**

```markdown
## 성능 테스트 결과 (YYYY-MM-DD)

### 테스트 환경
- CPU: [사양]
- Memory: [사양]  
- PostgreSQL: [버전]
- EdgeDB: [버전]

### 벤치마크 결과
| ORM | 평균 응답시간 | P95 응답시간 | RPS | 에러율 |
|-----|-------------|-------------|-----|-------|
| SQLAlchemy v2 | [ms] | [ms] | [수] | [%] |
| Tortoise ORM | [ms] | [ms] | [수] | [%] |
| EdgeDB | [ms] | [ms] | [수] | [%] |

### 승자: [ORM명] 
- 이유: [성능 우위 요인]
- 차이: [정량적 비교]
```

---

**�� 성능 챔피언을 가려보세요!** 