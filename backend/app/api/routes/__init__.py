from fastapi import APIRouter

from .cleanings import router as cleanings_router
from .users import router as users_rouer

router = APIRouter()

router.include_router(cleanings_router, prefix="/cleaning", tags=["Cleanings"])
router.include_router(users_rouer, prefix="/user", tags=["Users"])
