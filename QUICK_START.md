# 🚀 FastAPI ORM 성능 비교 - 빠른 시작 가이드

**5분 내에 3개 ORM 서버를 실행하고 성능 비교를 시작해보세요!**

> 📊 **프로젝트 개요 및 현재 상황**: [README.md](README.md) 참조  
> 📈 **성능 테스트 상세 가이드**: [PERFORMANCE_TEST_GUIDE.md](PERFORMANCE_TEST_GUIDE.md) 참조

## ⚡ **1단계: 환경 준비** (2분)

```bash
# 1. 프로젝트 클론 및 설치
git clone <repository>
cd orm_test

# 2. Poetry 설치 및 의존성
poetry install
poetry shell

# 3. PostgreSQL 시작 (Docker)
docker run -d --name orm_test_postgres \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=orm_test \
  -p 5432:5432 postgres:15

# 4. EdgeDB 시작 (Docker)
docker run -d --name orm_test_edgedb \
  -e EDGEDB_SERVER_SECURITY=insecure_dev_mode \
  -p 5656:5656 edgedb/edgedb:latest
```

## 🚀 **2단계: 서버 실행** (1분)

각각 별도 터미널에서 실행:

```bash
# Terminal 1: SQLAlchemy v2 (포트 8001)
cd apps/sqlalchemy_app
poetry run uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Tortoise ORM (포트 8002)  
cd apps/tortoise_app
poetry run uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3: EdgeDB (포트 8003)
cd apps/edgedb_app  
poetry run uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

## ✅ **3단계: 빠른 테스트** (2분)

### SQLAlchemy v2 테스트
```bash
# Health check
curl http://localhost:8001/health

# 사용자 생성
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# 벤치마크
curl http://localhost:8001/benchmark/sync-to-async
```

### Tortoise ORM 테스트
```bash
# Health check
curl http://localhost:8002/health

# 사용자 생성
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "email": "bob@example.com"}'

# 벤치마크
curl http://localhost:8002/benchmark/native-async
```

### EdgeDB 테스트

**먼저 마이그레이션 실행:**
```bash
# 마이그레이션 실행 (스키마 생성)
gel -H localhost -P 5656 --tls-security=insecure migrate
```

**그 다음 API 테스트:**
```bash
# Health check
curl http://localhost:8003/health

# 사용자 생성
curl -X POST http://localhost:8003/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie", "email": "charlie@example.com"}'

# 벤치마크
curl http://localhost:8003/benchmark/edgedb-native
```

## 🎯 **결과 확인**

### 성공 지표
- ✅ **Health Check**: 모든 서버에서 `{"status": "ok", "orm": "..."}`
- ✅ **사용자 생성**: JSON 응답으로 새 사용자 정보 반환
- ✅ **벤치마크**: 성능 지표 (시간, QPS) 출력

### 문제 해결
```bash
# PostgreSQL 연결 확인
docker logs orm_test_postgres

# EdgeDB 연결 확인  
docker logs orm_test_edgedb

# 포트 충돌 확인
lsof -i :8001 -i :8002 -i :8003
```

## 📊 **다음 단계**

성공적으로 실행되었다면:

1. **상세 API 테스트**: 각 엔드포인트 (`/users`, `/posts`) 테스트
2. **성능 비교**: [PERFORMANCE_TEST_GUIDE.md](PERFORMANCE_TEST_GUIDE.md)로 이동
3. **부하 테스트**: Locust를 이용한 실제 성능 측정

---

**🎉 3개 ORM 준비 완료! 이제 성능 비교를 시작해보세요!** 