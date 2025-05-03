from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

ALLOWED_ORIGINS = [
    "https://nasa-bot-web-app.ru",
    "https://t.me",
    "https://web.telegram.org",
]


class OriginFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin") or request.headers.get("referer") or ""

        if not any(origin.startswith(allowed) for allowed in ALLOWED_ORIGINS):
            return JSONResponse(
                {"error": "Forbidden: invalid origin"},
                status_code=403
            )

        return await call_next(request)
