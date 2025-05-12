from collections.abc import Awaitable
from typing import Callable

import fastapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from config import app_settings


class AllowedOriginsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate request origin against allowed origins.
    """
    async def dispatch(
            self,
            request: fastapi.Request,
            call_next: Callable[[fastapi.Request],
            Awaitable[Response]]
    ) -> Response:
        """
        Process incoming HTTP request and reject it if the origin is not allowed.

        Args:
            request (Request): Incoming HTTP request.
            call_next (Callable): Function to process the next middleware or endpoint.

        Returns:
            Response: JSON 403 response if origin is invalid; otherwise, proceeds with the request.
        """
        # Use "origin" or "referer" headers to determine the request's source
        origin = request.headers.get("origin") or request.headers.get("referer") or ""

        if not any(origin.startswith(allowed) for allowed in app_settings.allowed_origins):
            return JSONResponse(
                {"error": "Forbidden: invalid origin"},
                status_code=403
            )

        return await call_next(request)
