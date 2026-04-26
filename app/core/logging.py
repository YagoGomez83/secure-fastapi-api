import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

# Holds the correlation ID for the current async task / request context.
# Default is an empty string so the field is simply omitted when not set.
request_id_var: ContextVar[str] = ContextVar("request_id_var", default="")


class _JSONFormatter(logging.Formatter):
    """Emits every log record as a single-line JSON object.

    Guaranteed fields: timestamp, level, logger, message.
    Optional field:    user_id  (injected via extra={"user_id": ...}).
    On exceptions:     exc_info (formatted traceback as a string).
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = request_id_var.get()
        if request_id:
            payload["request_id"] = request_id

        user_id = getattr(record, "user_id", None)
        if user_id is not None:
            payload["user_id"] = user_id

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger to emit JSON. Call once at application startup."""
    handler = logging.StreamHandler()
    handler.setFormatter(_JSONFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger that inherits the JSON handler from the root logger."""
    return logging.getLogger(name)
