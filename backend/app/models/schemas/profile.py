from uuid import UUID

from pydantic import HttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.profile import Profile
from app.models.schemas.core import CoreModel

ProfileGenOut = pydantic_model_creator(Profile, exclude=("id", "created_at", "modified_at"))


class ProfileBase(CoreModel):
    full_name: str | None = None
    phone: str | None = None
    description: str | None = None
    image: HttpUrl | None = None


class ProfileCreateIn(ProfileBase):
    user_id: UUID


class ProfileUpdateIn(ProfileBase):
    pass


class ProfileOut(ProfileGenOut, CoreModel):
    user_id: UUID
    username: str | None = None
    email: str | None = None
