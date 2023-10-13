from fastapi import APIRouter, status

from app.db.repositories.users import UserRepository
from app.models.schemas.token import AccessToken
from app.models.schemas.user import UserCreateIn, UserPublicOut
from app.services import auth_service

router = APIRouter()


@router.post("", response_model=UserPublicOut, status_code=status.HTTP_201_CREATED)
async def register_new_user(new_user: UserCreateIn):
    user_repo = UserRepository()
    user = await user_repo.register_new_user(new_user)

    user.access_token = AccessToken(
        access_token=auth_service.create_access_token(user=user), token_type="Bearer"
    )
    return UserPublicOut.model_validate(user)
