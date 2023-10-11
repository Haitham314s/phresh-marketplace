from fastapi import HTTPException, status

from app.models.schemas.user import UserCreateIn, UserPublicOut
from app.models.user import User
from app.services import auth_service


class UserRepository:
    def __init__(self) -> None:
        self.auth_service = auth_service

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

        user_object = new_user.model_dump()
        user_password = self.auth_service.create_salt_and_hashed_password(
            new_user.password
        )
        user_object |= user_password.model_dump()

        user = await User.create(**user_object)
        return UserPublicOut.model_validate(user, from_attributes=True)
