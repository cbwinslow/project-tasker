from fastapi import APIRouter
from project_tasker.api.endpoints import auth, projects

api_router = APIRouter()
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
