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
- **FastAPI** - 고성능 웹 프레임워크
- **Pydantic v2** - 데이터 검증 (Frozen Config 적용)
- **PostgreSQL** - 데이터베이스 (SQLAlchemy, Tortoise 공용)
- **Python 3.12** - Future Annotations 활용

### **ORM별 특징**
- **SQLAlchemy v2**: Modern Mapped[] 타입 + async_sessionmaker
- **Tortoise ORM**: 네이티브 비동기 + Django-like API  
- **EdgeDB**: 차세대 그래프-관계형 + EdgeQL

## 📖 **문서 가이드**

- **🚀 빠른 시작**: [QUICK_START.md](QUICK_START.md) - 환경 설정 및 서버 실행
- **📊 성능 테스트**: [PERFORMANCE_TEST_GUIDE.md](PERFORMANCE_TEST_GUIDE.md) - 벤치마크 및 부하 테스트

## 🎊 **개발 성과**

### **코드 품질 개선**
```
Before: 거대한 단일 파일 (200+ 줄)
After:  모듈화된 깔끔한 구조 (20-25 줄)

리팩토링 결과:
- EdgeDB:     213줄 → 25줄
- SQLAlchemy: 213줄 → 20줄  
- Tortoise:   211줄 → 22줄
```

### **현대적 패턴 적용**
- **SQLAlchemy v2** 완전 적용
- **Frozen Config** 모든 DTO에 적용
- **Future Annotations** 타입 안전성 확보
- **Clean Architecture** 일관성 있는 구조

---

**Ready for Performance Battle!** 🔥
