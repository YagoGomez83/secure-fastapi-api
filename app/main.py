from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints.user import router as user_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "env": settings.APP_ENV
    }


app.include_router(
    user_router,
    prefix="/api/v1",
    tags=["Users"]
)