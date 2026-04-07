from fastapi import APIRouter

from app.api import auth, users, projects, members, files, chat, llm_config, bmad, stt, activity, admin, guide

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(llm_config.router, prefix="/llm", tags=["llm"])
api_router.include_router(bmad.router, prefix="/bmad", tags=["bmad"])
api_router.include_router(stt.router, prefix="/stt", tags=["stt"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(guide.router, prefix="/guide", tags=["guide"])
