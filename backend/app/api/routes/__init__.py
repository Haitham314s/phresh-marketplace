from fastapi import APIRouter

from .auth import router as auth_router
from .cleanings import router as cleanings_router
from .evaluations import router as evaluations_router
from .offers import router as offers_router
from .profiles import router as profile_router
from .users import router as users_router
from .feeds import router as feeds_router

router = APIRouter()

router.include_router(cleanings_router, prefix="/cleaning", tags=["Cleaning"])
router.include_router(users_router, prefix="/user", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(profile_router, prefix="/user/profile", tags=["Profile"])
router.include_router(offers_router, prefix="/cleaning/{cleaning_id}/offer", tags=["Offers"])
router.include_router(evaluations_router, prefix="/evaluation", tags=["Evaluations"])
router.include_router(feeds_router, prefix="/feed", tags=["Feeds"])
