# 🚀 FastAPI ORM 성능 비교 - 빠른 시작 가이드

**5분 내에 3개 ORM 서버를 실행하고 성능 비교를 시작해보세요!**

> 📊 **프로젝트 개요 및 현재 상황**: [README.md](README.md) 참조  
> 📈 **성능 테스트 결과**: [PERFORMANCE_RESULTS.md](PERFORMANCE_RESULTS.md) 참조

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

## 🚀 **2단계: 서버 실행**

### **SQLAlchemy v2 서버**
```bash
# SQLAlchemy v2 (포트 8001)
poetry run gunicorn apps.sqlalchemy_app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### **Tortoise ORM 서버**
```bash
# Tortoise ORM (포트 8002)
poetry run gunicorn apps.tortoise_app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002
```

### **EdgeDB 서버**
```bash
# EdgeDB 마이그레이션 (필수)
gel -H localhost -P 5656 --tls-security=insecure migrate

# EdgeDB (포트 8003)
poetry run gunicorn apps.edgedb_app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003
```

## 📊 **3단계: 성능 테스트** (10분)

### **테스트 환경**
- **서버 설정**: 워커 2개, 커넥션 풀 5개
- **데이터베이스**: 모든 ORM에 인덱스 최적화 적용
- **테스트 도구**: Locust 웹 UI
- **테스트 방법**: 단계별 부하 증가

### **테스트 조건**
- **최종 부하**: 사용자 50명, Ramp up 10명/초
- **목표 RPS**: 20 (실제 운영 환경 시나리오)
- **성능 지표**: P95 응답시간, 평균 QPS

### **Locust 부하 테스트 실행**
```bash
# 프로젝트 루트에서 실행
cd tests/locust_tests

# SQLAlchemy v2
locust -f locustfile.py SQLAlchemyUser -H http://localhost:8001

# Tortoise ORM
locust -f locustfile.py TortoiseUser -H http://localhost:8002

# EdgeDB
locust -f locustfile.py EdgeDBUser -H http://localhost:8003
```

### **웹 UI 설정**
1. 브라우저에서 `http://localhost:8089` 접속
2. **Number of users**: 50
3. **Spawn rate**: 10
4. **Start swarming** 클릭

### **성능 지표 해석**

| 지표 | 의미 | 목표값 |
|------|------|--------|
| **평균 응답시간** | 일반적인 성능 | < 50ms |
| **P95 응답시간** | 최악의 5% 케이스 | < 200ms |
| **RPS** | 초당 처리 요청 수 | > 100 |
| **에러율** | 실패한 요청 비율 | < 1% |

## 📈 **다음 단계**

성공적으로 실행되었다면:

1. **성능 결과 확인**: [PERFORMANCE_RESULTS.md](PERFORMANCE_RESULTS.md)에서 실제 테스트 결과 비교
2. **상세 분석**: 각 ORM별 성능 특성 분석

---

**🎉 3개 ORM 준비 완료! 이제 성능 비교를 시작해보세요!** 