# Backend Structure

현재 백엔드는 Python 3.10 기반 FastAPI 프로젝트이며, 패키지 관리는 `uv`를 사용한다.
아래 구조는 소스 코드와 프로젝트 설정 파일 기준이며, 로컬 생성물인 `.venv`, `.pytest_cache`, `__pycache__`는 제외했다.

```text
backend/
├── .python-version          # 백엔드에서 사용하는 Python 버전 고정
├── README.md                # 백엔드 실행, 패키지 설치, 협업 안내
├── pyproject.toml           # 프로젝트 메타데이터와 Python 의존성 선언
├── uv.lock                  # uv가 생성한 의존성 잠금 파일
├── docs/
│   └── structure.md         # 백엔드 디렉토리 구조 설명 문서
├── app/
│   ├── __init__.py          # app 패키지 초기화 파일
│   ├── main.py              # FastAPI 애플리케이션 생성 및 라우터 등록 진입점
│   ├── api/
│   │   ├── __init__.py      # API 패키지 초기화 파일
│   │   └── v1/
│   │       ├── __init__.py  # v1 API 패키지 초기화 파일
│   │       ├── router.py    # v1 엔드포인트 라우터를 하나로 모으는 파일
│   │       └── endpoints/
│   │           ├── __init__.py  # 엔드포인트 패키지 초기화 파일
│   │           └── health.py    # 서버 상태 확인용 health API
│   ├── schemas/
│   │   ├── __init__.py      # 스키마 패키지 초기화 파일
│   │   ├── health.py        # health API 응답 모델
│   │   └── url.py           # URL 관련 요청/응답 모델
│   └── services/
│       ├── __init__.py      # 서비스 패키지 초기화 파일
│       ├── openai_service.py    # OpenAI 연동 로직을 담당하는 서비스
│       └── web_risk_service.py  # 웹 위험도 판단 로직을 담당하는 서비스
└── tests/
    ├── __init__.py          # 테스트 패키지 초기화 파일
    └── api/
        ├── __init__.py      # API 테스트 패키지 초기화 파일
        └── test_health.py   # health API 동작 검증 테스트
```

## 역할 요약

- `app/main.py`: FastAPI 앱의 시작점이다. 서버 실행 시 `app.main:app`으로 참조된다.
- `app/api/v1/`: 버전이 있는 API 라우팅 계층이다. 새 API는 우선 이 하위에 추가한다.
- `app/schemas/`: Pydantic 모델을 모아 요청과 응답 데이터 형태를 관리한다.
- `app/services/`: 외부 API 호출, 위험도 판단 같은 비즈니스 로직을 분리한다.
- `tests/`: API와 서비스 동작을 검증하는 테스트 코드를 둔다.
