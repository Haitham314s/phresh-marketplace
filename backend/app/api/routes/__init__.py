from fastapi import APIRouter

from .cleanings import router as cleanings_router
from .users import router as users_rouer
from .auth import router as auth_router

router = APIRouter()

router.include_router(cleanings_router, prefix="/cleaning", tags=["Cleanings"])
router.include_router(users_rouer, prefix="/user", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
