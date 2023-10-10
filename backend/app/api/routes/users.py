from fastapi import APIRouter, status

from app.db.repositories.users import UserRepository
from app.models.schemas.user import UserCreateIn, UserPublicOut

router = APIRouter()


@router.post("", response_model=UserPublicOut, status_code=status.HTTP_201_CREATED)
async def register_new_user(new_user: UserCreateIn):
    user_repo = UserRepository()
    return await user_repo.register_new_user(new_user)
