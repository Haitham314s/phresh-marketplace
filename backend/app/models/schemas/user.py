from pydantic import EmailStr, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.schemas.token import AccessToken
from app.models.user import User
from .core import CoreModel
from .profile import ProfileOut

UserGenOut = pydantic_model_creator(User, exclude=("salt", "hashed_password", "created_at", "modified_at"))


class UserBase(CoreModel):
    email: EmailStr | None = None
    username: str | None = None
    email_verified: bool
    is_active: bool
    is_superuser: bool


class UserCreateIn(CoreModel):
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, pattern="^[a-zA-Z0-9_-]+$")


class UserUpdateIn(CoreModel):
    email: EmailStr | None = None
    username: constr(min_length=3, pattern="^[a-zA-Z0-9_-]+$") | None = None


class UserPasswordIn(CoreModel):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPasswordOut(CoreModel):
    password: str
    salt: str


class UserPublicOut(UserGenOut, CoreModel):
    profile: ProfileOut | None = None
