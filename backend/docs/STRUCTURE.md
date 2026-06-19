# Backend Structure

현재 백엔드는 Python 3.10 기반 FastAPI 프로젝트이며, 패키지 관리는 `uv`를 사용한다.
아래 구조는 소스 코드와 프로젝트 설정 파일 기준이며, 로컬 생성물인 `.venv`, `.pytest_cache`, `__pycache__`는 제외했다.

```text
backend/
├── .python-version          # Python 버전 고정
├── .env.example             # 환경변수 템플릿 (실제 .env는 gitignore)
├── alembic.ini              # Alembic 설정 파일
├── pyproject.toml           # 프로젝트 메타데이터와 의존성
├── uv.lock                  # uv 의존성 잠금 파일
├── docs/
│   └── STRUCTURE.md         # 이 파일
├── alembic/
│   ├── env.py               # Alembic 실행 환경 (DATABASE_URL, 모델 메타데이터)
│   ├── script.py.mako       # migration 파일 생성 템플릿
│   └── versions/
│       └── 0001_initial_schema.py  # 1차 배포 초기 스키마 migration
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 생성 및 라우터 등록 진입점
│   ├── core/
│   │   └── config.py        # DATABASE_URL 등 환경변수 로딩
│   ├── db/
│   │   ├── base.py          # SQLAlchemy DeclarativeBase
│   │   ├── session.py       # engine과 SessionLocal 생성
│   │   ├── dependencies.py  # FastAPI DB session dependency (get_db)
│   │   └── seed.py          # categories, promotion_products 기준 데이터 삽입
│   ├── models/
│   │   ├── __init__.py      # 모든 모델 re-export (Alembic autogenerate 용)
│   │   ├── category.py      # Category
│   │   ├── user.py          # User, UserInterest, UserFollow
│   │   ├── service.py       # Service, ServiceEntryLog
│   │   ├── feedback.py      # Feedback
│   │   ├── point.py         # PointLog, Attendance
│   │   ├── promotion.py     # PromotionProduct, Promotion
│   │   ├── community.py     # CommunityPost, CommunityComment
│   │   └── report.py        # Report
│   ├── api/
│   │   └── v1/
│   │       ├── router.py    # v1 엔드포인트 라우터
│   │       └── endpoints/
│   │           └── health.py
│   ├── schemas/
│   │   ├── health.py
│   │   └── url.py
│   └── services/
│       ├── openai_service.py
│       └── web_risk_service.py
└── tests/
    └── api/
        └── test_health.py
```

## DB 연결 기준

- backend는 환경변수 `DATABASE_URL`로만 DB 접속 정보를 읽는다.
- 로컬 `.env`는 Docker PostgreSQL 연결 문자열을 사용한다 (`.env.example` 참고).
- 운영 EC2 `.env`는 RDS PostgreSQL 연결 문자열을 사용한다.
- API handler는 `from app.db.dependencies import get_db`를 주입받아 DB에 접근한다.

## DB 초기화 순서 (로컬)

```bash
# 1. Docker PostgreSQL 실행
docker compose up -d db

# 2. .env 파일 준비
cp .env.example .env  # 필요시 수정

# 3. migration 적용
cd backend
uv run alembic upgrade head

# 4. (선택) 기준 데이터 삽입
uv run python -c "
from app.db.session import SessionLocal
from app.db.seed import run_seed
db = SessionLocal()
run_seed(db)
db.close()
"
```

## 새 API 엔드포인트 추가 기준

1. `app/api/v1/endpoints/` 아래 담당 기능 파일을 만든다.
2. `app/api/v1/router.py`에 include_router로 등록한다.
3. DB가 필요하면 `Depends(get_db)`로 session을 주입받는다.
4. 스키마 변경이 필요하면 `alembic revision --autogenerate -m "설명"` 후 검토한다.
