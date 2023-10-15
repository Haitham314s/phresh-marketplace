from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.db.repositories import profile_repo
from app.models import User
from app.models.schemas.profile import ProfileOut, ProfileUpdateIn

router = APIRouter()


@router.get("", response_model=ProfileOut)
async def get_user_profile(user: User = Depends(get_current_user)):
    profile = await profile_repo.get_user_profile(user)
    profile.username = user.username
    profile.email = user.email
    return ProfileOut.model_validate(profile)


@router.put("", response_model=ProfileOut)
async def update_user_profile(profile_in: ProfileUpdateIn, user: User = Depends(get_current_user)):
    profile = await profile_repo.update_user_profile(user, profile_in)
    profile.username = user.username
    profile.email = user.email
    return ProfileOut.model_validate(profile)
