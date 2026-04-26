import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger, request_id_var
from app.db.database import create_tables

# Configure JSON logging before anything else emits a record.
configure_logging(level=logging.DEBUG if settings.DEBUG else logging.INFO)

logger = get_logger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Assign a unique correlation ID to every incoming request.

    * Reads X-Request-ID from the incoming headers (lets callers propagate
      an existing trace ID across service boundaries).
    * Falls back to a freshly generated uuid4 when no header is present.
    * Stores the ID in ``request_id_var`` so every log record emitted
      during this request is automatically annotated – no plumbing needed.
    * Echoes the ID back via the X-Request-ID response header so clients
      can correlate logs with the requests they issued.
    """

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = request_id_var.set(correlation_id)
        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(token)
        response.headers["X-Request-ID"] = correlation_id
        return response


class _UnhandledExceptionMiddleware(BaseHTTPMiddleware):
    """Catch every exception that was not handled by a route or FastAPI handler.

    * Logs the real error (including traceback) with the structured JSON logger.
    * Returns a generic HTTP 500 to the client – no internal details leak out.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            user_id = getattr(request.state, "user_id", None)
            logger.error(
                "Unhandled exception",
                exc_info=True,
                extra={"user_id": user_id},
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

app.add_middleware(_UnhandledExceptionMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# Initialise database tables on startup
create_tables()


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok", "env": settings.APP_ENV}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1", tags=["Users"])
