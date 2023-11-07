from uuid import UUID

from pydantic import EmailStr

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories.profiles import ProfileRepository
from app.models.schemas.profile import ProfileCreateIn
from app.models.schemas.user import UserCreateIn
from app.models.user import User
from app.services import auth_service


class UserRepository:
    def __init__(self) -> None:
        self.auth_service = auth_service
        self.profile_repo = ProfileRepository()

    async def populate_user(self, user: User | None) -> User | None:
        if user is None:
            return None

        profile = await self.profile_repo.get_user_profile(user)
        user.profile = profile
        return user

    async def get_user_by_email(self, email: EmailStr, populate: bool = True) -> User | None:
        user = await User.get_or_none(email=email)
        if populate:
            return await self.populate_user(user)

        return user if user is not None else None

    async def get_user_by_username(self, username: str, populate: bool = True) -> User | None:
        user = await User.get_or_none(username=username)
        if populate:
            return await self.populate_user(user)

        return user if user is not None else None

    async def get_user_by_id(self, user_id: UUID, populate: bool = True) -> User | None:
        user = await User.get_or_none(id=user_id)
        if populate:
            return await self.populate_user(user)

        return user if user is not None else None

    async def register_new_user(self, new_user: UserCreateIn) -> User:
        if await self.get_user_by_email(new_user.email) is not None:
            raise APIException(ErrorCode.email_already_used)
        if await self.get_user_by_username(new_user.username) is not None:
            raise APIException(ErrorCode.username_already_used)

        user_object = new_user.model_dump()
        user_password = self.auth_service.create_salt_and_hashed_password(new_user.password)
        user_object |= {
            "hashed_password": user_password.password,
            "salt": user_password.salt,
        }

        user = await User.create(**user_object)
        await self.profile_repo.create_user_profile(ProfileCreateIn(user_id=user.id))
        return await self.populate_user(user)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.get_user_by_email(username, populate=False) or await self.get_user_by_username(
            username, populate=False
        )
        if user is None:
            return None
        if not self.auth_service.verify_password(password, user.salt, user.hashed_password):
            return None

        return user
