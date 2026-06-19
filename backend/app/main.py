from fastapi import FastAPI

from app.api.v1.router import api_router
import app.models  # noqa: F401 — Base.metadata에 모든 모델 등록

app = FastAPI(title="BuildBack API")

app.include_router(api_router, prefix="/api/v1")
