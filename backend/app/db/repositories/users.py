from fastapi import HTTPException, status

from app.models.schemas.user import UserCreateIn, UserPublicOut
from app.models.user import User


class UserRepository:
    async def get_user_by_email(self, email: str) -> UserPublicOut | None:
        user = await User.get_or_none(email=email)
        return UserPublicOut.model_validate(user) if user is not None else None

    async def get_user_by_username(self, username: str) -> UserPublicOut | None:
        user = await User.get_or_none(username=username)
        return UserPublicOut.model_validate(user) if user is not None else None

    async def register_new_user(self, new_user: UserCreateIn) -> UserPublicOut:
        if await self.get_user_by_email(new_user.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken"
            )
        if await self.get_user_by_username(new_user.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        user = await User.create(**new_user.model_dump())
        return UserPublicOut.model_validate(user)
