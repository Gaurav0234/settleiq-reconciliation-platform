from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes.health import router as health_router

from app.api.routes.auth import router as auth_router

from app.api.routes.partners import router as partners_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Order-to-cash reconciliation platform for D2C businesses.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(health_router)

app.include_router(auth_router)

app.include_router(partners_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "settleiq-api",
        "version": settings.app_version,
    }