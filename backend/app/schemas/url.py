from pydantic import BaseModel, HttpUrl


class UrlCheckRequest(BaseModel):
    url: HttpUrl


class UrlCheckResponse(BaseModel):
    url: HttpUrl
    is_risky: bool
    reason: str | None = None

