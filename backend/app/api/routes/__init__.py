from fastapi import APIRouter

from .auth import router as auth_router
from .cleanings import router as cleanings_router
from .profiles import router as profile_router
from .users import router as users_router

router = APIRouter()

router.include_router(cleanings_router, prefix="/cleaning", tags=["Cleaning"])
router.include_router(users_router, prefix="/user", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(profile_router, prefix="/user/profile", tags=["Profile"])
