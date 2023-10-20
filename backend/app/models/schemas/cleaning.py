from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.cleaning import Cleaning, CleaningType
from .core import CoreModel

CleaningPydanticOut = pydantic_model_creator(Cleaning)


class CleaningBase(CoreModel):
    name: str
    description: str | None = None
    price: float
    type: CleaningType | None = CleaningType.spot_clean


class CleaningUpdateIn(CleaningBase):
    name: str | None = None
    price: float | None = None
    type: CleaningType | None = None


class CleaningOut(CleaningPydanticOut, CoreModel):
    price: float
