from fastapi import HTTPException, status

from app.models.schemas.user import UserCreateIn
from app.models.user import User
from app.services import auth_service


class UserRepository:
    def __init__(self) -> None:
        self.auth_service = auth_service

    async def get_user_by_email(self, email: str) -> User | None:
        user = await User.get_or_none(email=email)
        return user if user is not None else None

    async def get_user_by_username(self, username: str) -> User | None:
        user = await User.get_or_none(username=username)
        return user if user is not None else None

    async def register_new_user(self, new_user: UserCreateIn) -> User:
        if await self.get_user_by_email(new_user.email) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")
        if await self.get_user_by_username(new_user.username) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        user_object = new_user.model_dump()
        user_password = self.auth_service.create_salt_and_hashed_password(new_user.password)
        user_object |= {
            "hashed_password": user_password.password,
            "salt": user_password.salt,
        }

        return await User.create(**user_object)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.get_user_by_email(username) or await self.get_user_by_username(username)
        if user is None:
            return None
        if not self.auth_service.verify_password(password, user.salt, user.hashed_password):
            return None

        return user
