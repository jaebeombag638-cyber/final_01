from app.schemas.url import UrlCheckResponse


class WebRiskService:
    def check_url(self, url: str) -> UrlCheckResponse:
        raise NotImplementedError

