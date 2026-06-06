"""路由模块"""
from .auth import router as auth_router
from .interview import router as interview_router
from .questions import router as questions_router
from .assessment import router as assessment_router
from .learning import router as learning_router
from .profile import router as profile_router
from .enterprise import router as enterprise_router

__all__ = [
    "auth_router",
    "interview_router",
    "questions_router",
    "assessment_router",
    "learning_router",
    "profile_router",
    "enterprise_router"
]
