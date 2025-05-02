from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from project_tasker.core.config import settings
from project_tasker.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Automated project management integration tool",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Project Tasker API",
        "documentation": f"{settings.API_V1_PREFIX}/docs"
    }
