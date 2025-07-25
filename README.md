# FastAPI ORM 성능 비교 프로젝트

FastAPI와 세 가지 ORM(SQLAlchemy v2, Tortoise ORM, EdgeDB)의 성능을 비교하는 프로젝트입니다.

## 🎯 **프로젝트 목표**

- **동일한 Clean Architecture**로 3개 ORM 구현
- **실제 운영 환경** 시나리오 기반 성능 비교
- **현대적 기술 스택** 활용 (SQLAlchemy v2, Pydantic v2, EdgeDB)

## 📊 **현재 구현 상황** (2025-07-25 업데이트)

### ✅ **완료된 ORM**

| ORM | 개발 완료도 | 아키텍처 | 기술 스택 | 상태 |
|-----|-------------|----------|-----------|------|
| **SQLAlchemy v2** | **100%** | ✅ Clean Architecture | Mapped[] + DeclarativeBase | ✅ 준비 완료 |
| **Tortoise ORM** | **100%** | ✅ Clean Architecture | 네이티브 비동기 | ✅ 준비 완료 |
| **EdgeDB** | **100%** | ✅ Clean Architecture | EdgeQL + 타입 안전성 | ✅ 준비 완료 |

> **현황**: 모든 3개 ORM이 **동일한 아키텍처**로 완성되어 **성능 비교 준비 완료**!

## 🏗️ **공통 아키텍처**

모든 앱이 동일한 구조로 구현되어 공정한 성능 비교가 가능합니다:

```
각 ORM 앱 구조:
├── schemas/     # DTO 모델 (Frozen Config + Future Annotations)
├── apis/        # FastAPI 라우터 분리
├── services/    # 비즈니스 로직 레이어
├── models.py    # ORM 모델 정의
├── database.py  # 데이터베이스 연결 설정
└── main.py      # 앱 구성 (20-25줄)
```

## 🚀 **기술 스택**

### **공통 기술**
- **FastAPI**
- **Pydantic v2**
- **PostgreSQL** - 데이터베이스 (SQLAlchemy, Tortoise 공용)


### **ORM별 특징**

#### **🥉 SQLAlchemy v2**
- **역사**: 2006년부터 시작된 Python ORM의 표준
- **참고자료**: 풍부한 문서와 커뮤니티 지원
- **비동기 지원**: Greenlet을 통한 동기→비동기 전환 (오버헤드 ~0.4ms)
- **성능**: 검증된 안정성과 성숙한 최적화

#### **🥈 Tortoise ORM** - 네이티브 비동기
- **아키텍처**: 처음부터 비동기로 설계된 네이티브 비동기 ORM
- **성능**: Greenlet 오버헤드 없이 직접적인 비동기 처리
- **API**: Django ORM과 유사한 직관적인 인터페이스
- **특징**: 비동기 컨텍스트에서 최적화된 성능

#### **🥇 EdgeDB** - 차세대 그래프-관계형
- **아키텍처**: 그래프와 관계형의 장점을 결합한 차세대 DB
- **쿼리 최적화**: Code Generation으로 직접 쿼리 생성 (ORM 오버헤드 최소화)
- **성능**: EdgeQL의 효율적인 쿼리 실행으로 최고 성능 달성
- **특징**: ORM보다 빠른 네이티브 쿼리 성능

## 📊 **성능 비교 결과** (2025-07-25)

### **🏆 최종 성능 순위**

| 순위 | ORM | 평균 응답시간 | RPS | 에러율 | P95 최대값 | 특징 |
|------|-----|---------------|-----|--------|------------|------|
| 🥇 **1위** | **EdgeDB** | 11ms | 24.78 | 0.04% | 29ms | Code Generation |
| 🥈 **2위** | **Tortoise ORM** | 13ms | 24.63 | 0.06% | 38ms | 네이티브 비동기 |
| 🥉 **3위** | **SQLAlchemy v2** | 15ms | 24.73 | 0% | 45ms | Greenlet 비동기 |

### **🎯 성능 분석**
- **EdgeDB**: Code Generation으로 ORM 오버헤드 최소화, 최고 성능
- **Tortoise ORM**: 네이티브 비동기로 Greenlet 오버헤드 없음
- **SQLAlchemy v2**: Greenlet 오버헤드(~0.4ms)에도 불구하고 안정적 성능

## 📖 **문서 가이드**

- **🚀 빠른 시작**: [QUICK_START.md](QUICK_START.md) - 환경 설정 및 서버 실행
- **📊 상세 성능 결과**: [PERFORMANCE_RESULTS.md](PERFORMANCE_RESULTS.md)

---

