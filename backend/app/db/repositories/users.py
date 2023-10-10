from app.models.schemas.user import UserCreateIn, UserPublicOut
from app.models.user import User


class UserRepository:
    async def register_new_user(self, new_user: UserCreateIn) -> UserPublicOut:
        user = await User.create(**new_user.model_dump())
        return UserPublicOut.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserPublicOut or None:
        return await User.get_or_none(email=email)
