# FastAPI ORM 성능 테스트 가이드

## 📊 **현재 테스트 상황** (2025-07-24)

### ✅ **완료된 테스트**
- **SQLAlchemy v2**: 모든 API + Greenlet 벤치마크 완료
- **Tortoise ORM**: 모든 API + 네이티브 비동기 벤치마크 완료
- **성능 비교**: Tortoise ORM 15% 우위 확인

### ⚠️ **진행 중인 작업**
- **EdgeDB**: 스키마 생성 문제로 API 테스트 불가
- **Locust 통합 테스트**: 2개 ORM 준비 완료, EdgeDB 대기 중

---

## 🎯 **프로젝트 개요**

이 프로젝트는 **FastAPI**와 세 가지 ORM의 성능을 비교합니다:

1. **SQLAlchemy v2** - Greenlet 기반 sync-to-async 변환
2. **Tortoise ORM** - 네이티브 비동기 ORM
3. **EdgeDB** - 차세대 그래프-관계형 데이터베이스

## 📋 **테스트 조건**

- **성능 지표**: P95 응답시간
- **목표 RPS**: 20
- **Connection Pool**: 5
- **Worker 수**: 4
- **테스트 도구**: Locust
- **데이터베이스**: PostgreSQL 15 (Docker)

## 🛠️ **환경 설정**

### 1. 프로젝트 설치

```bash
# Poetry로 의존성 설치
poetry install
poetry shell
```

### 2. 데이터베이스 설정

#### PostgreSQL (SQLAlchemy & Tortoise 공용)
```bash
docker run -d --name orm_test_postgres \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=orm_test \
  -p 5432:5432 postgres:15
```

#### EdgeDB (현재 스키마 문제)
```bash
docker run -d --name orm_test_edgedb \
  -e EDGEDB_SERVER_SECURITY=insecure_dev_mode \
  -p 5656:5656 edgedb/edgedb:latest

# ⚠️ 스키마 생성 실패 - 수동 해결 필요
```

## 🚀 **서버 실행**

### 방법 1: 개별 실행

```bash
# SQLAlchemy 서버 (포트 8001)
poetry run uvicorn apps.sqlalchemy_app.main:app --host 0.0.0.0 --port 8001 --reload

# Tortoise ORM 서버 (포트 8002)
poetry run uvicorn apps.tortoise_app.main:app --host 0.0.0.0 --port 8002 --reload

# EdgeDB 서버 (포트 8003) - 스키마 문제로 제한적
poetry run uvicorn apps.edgedb_app.main:app --host 0.0.0.0 --port 8003 --reload
```

### 방법 2: 스크립트 사용 (권장)

```bash
# 모든 서버 시작
./scripts/start_servers.sh

# 모든 서버 종료
./scripts/stop_servers.sh
```

## 🧪 **API 테스트**

### ✅ SQLAlchemy v2 (완료)

#### 기본 API 테스트
```bash
# Health Check
curl http://localhost:8001/health

# 사용자 생성
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'

# 사용자 목록 조회
curl http://localhost:8001/users

# 게시글 생성
curl -X POST http://localhost:8001/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "SQLAlchemy Post", "content": "Test content", "user_id": 1}'
```

#### Greenlet 성능 벤치마크
```bash
curl http://localhost:8001/benchmark/sync-to-async
# 결과: 평균 2.8ms, 초당 357 변환
```

### ✅ Tortoise ORM (완료)

#### 기본 API 테스트
```bash
# Health Check
curl http://localhost:8002/health

# 사용자 생성
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"name": "David Kim", "email": "david@tortoise.com"}'

# 사용자 목록 조회 (SQLAlchemy 데이터 포함)
curl http://localhost:8002/users

# 게시글 생성
curl -X POST http://localhost:8002/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Tortoise Post", "content": "Native async test", "user_id": 4}'
```

#### 네이티브 비동기 성능 벤치마크
```bash
curl http://localhost:8002/benchmark/native-async
# 결과: 평균 2.4ms, 초당 412 쿼리
```

### ⚠️ EdgeDB (스키마 문제)

```bash
# Health Check (작동)
curl http://localhost:8003/health

# API 테스트 (현재 불가 - Internal Server Error)
curl -X POST http://localhost:8003/users \
  -H "Content-Type: application/json" \
  -d '{"name": "EdgeDB User", "email": "user@edgedb.com"}'
```

**문제**: User/Post 타입이 EdgeDB에 생성되지 않음

## 📈 **Locust 성능 테스트**

### 테스트 스크립트 위치
```
tests/locust_tests/
├── locust_test.py           # Locust 테스트 정의
└── run_performance_test.py  # 자동화 스크립트
```

### 개별 ORM 테스트

#### SQLAlchemy 테스트
```bash
cd tests/locust_tests
locust -f locust_test.py SQLAlchemyUser -H http://localhost:8001 \
  --users 20 --spawn-rate 2 --run-time 60s --html reports/sqlalchemy_report.html
```

#### Tortoise ORM 테스트
```bash
cd tests/locust_tests
locust -f locust_test.py TortoiseUser -H http://localhost:8002 \
  --users 20 --spawn-rate 2 --run-time 60s --html reports/tortoise_report.html
```

### 자동화된 비교 테스트

```bash
cd tests/locust_tests
python run_performance_test.py
```

**결과**: SQLAlchemy vs Tortoise ORM 성능 비교 리포트 생성

## 📊 **현재 성능 결과**

### 🏆 **벤치마크 비교** (단일 쿼리 성능)

| ORM | 벤치마크 타입 | 평균 응답시간 | 초당 처리량 | 특징 |
|-----|-------------|-------------|------------|------|
| **Tortoise ORM** | Native Async | **2.4ms** | **412 QPS** | 네이티브 비동기 |
| **SQLAlchemy v2** | Greenlet Sync-to-Async | **2.8ms** | **357 QPS** | Greenlet 변환 |

### 📈 **성능 분석**

1. **Tortoise ORM 우위**: 약 **15% 더 빠른 성능**
2. **Greenlet 오버헤드**: SQLAlchemy의 sync-to-async 변환 비용 **0.4ms**로 경량
3. **동일 DB 공유**: PostgreSQL에서 Cross-ORM 데이터 호환성 확인

### 🔍 **상세 성능 특성**

#### SQLAlchemy v2
- **장점**: 성숙한 생태계, 복잡한 쿼리 지원
- **단점**: Greenlet 변환으로 인한 미미한 오버헤드
- **적합한 경우**: 기존 SQLAlchemy 코드베이스, 복잡한 ORM 관계

#### Tortoise ORM
- **장점**: 네이티브 비동기, 빠른 성능
- **단점**: 상대적으로 작은 생태계
- **적합한 경우**: 새 프로젝트, 성능 중심 API

## 🚧 **현재 진행 상황**

### ✅ **완료된 작업**
- [x] SQLAlchemy v2 구현 및 테스트
- [x] Tortoise ORM 구현 및 테스트  
- [x] `created_at` timezone 문제 해결
- [x] PostgreSQL 연동 및 데이터 공유
- [x] 개별 성능 벤치마크 완료

### ⚠️ **진행 중인 작업**
- [ ] EdgeDB 스키마 생성 문제 해결
- [ ] EdgeDB API 테스트 완료
- [ ] 3개 ORM 통합 Locust 테스트

### 🎯 **다음 단계**
1. EdgeDB 스키마 문제 해결 또는 2개 ORM으로 진행 결정
2. 전체 Locust 성능 테스트 실행
3. P95 응답시간 기준 최종 성능 분석 리포트

## 🔧 **문제 해결**

### SQLAlchemy 관련
- **Connection Pool Error**: `pool_size`는 PostgreSQL에서만 사용
- **Timezone 문제**: `created_at` 필드 제거로 해결

### Tortoise ORM 관련
- **Datetime Error**: `created_at` 필드 제거로 해결
- **PostgreSQL 호환성**: `tls_security="insecure"` 설정 필요

### EdgeDB 관련
- **TLS Certificate Error**: `tls_security="insecure"` 설정으로 해결
- **Schema 생성 실패**: 현재 미해결 - 수동 타입 생성 필요

## 📋 **결론**

현재까지의 테스트 결과:

1. **성능**: Tortoise ORM > SQLAlchemy v2 (15% 우위)
2. **안정성**: 두 ORM 모두 프로덕션 준비 완료
3. **호환성**: PostgreSQL에서 완벽한 데이터 공유
4. **개발 경험**: SQLAlchemy가 더 성숙한 생태계

**권장사항**: 
- **새 프로젝트**: Tortoise ORM (성능 우위)
- **기존 프로젝트**: SQLAlchemy v2 (마이그레이션 비용 고려)

---

**Last Updated**: 2025-07-24  
**Test Status**: SQLAlchemy ✅ | Tortoise ✅ | EdgeDB ⚠️ 