# Structure

```
buildback/
├── .gitignore
├── ai/
│   └── ai.md
├── backend/
│   ├── .python-version
│   ├── README.md
│   ├── backend.md
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           └── health.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── url.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── openai_service.py
│   │       └── web_risk_service.py
│   └── tests/
│       ├── __init__.py
│       └── api/
│           ├── __init__.py
│           └── test_health.py
├── frontend/
│   └── frontend.md
└── docs/
    ├── ai-data-roadmap.md
    ├── concept.md
    ├── phase1-plan.md
    ├── STRUCTURE.md
    ├── TECHSPEC.md
    └── team-plans/
        ├── README.md
        ├── cho-hyeonjeong.md
        ├── kim-eungyeong.md
        ├── kim-hyeonjin.md
        ├── park-geonil.md
        └── park-jaebeom.md

```
