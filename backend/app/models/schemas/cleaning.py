from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.cleaning import Cleaning, CleaningType

from .core import CoreModel, IDModelMixin

CleaningPydanticOut = pydantic_model_creator(Cleaning)


class CleaningBase(CoreModel):
    name: str
    description: str | None = None
    price: float
    type: CleaningType | None = CleaningType.spot_clean


class CleaningUpdateIn(IDModelMixin, CleaningBase):
    pass


class CleaningOut(CleaningPydanticOut, CoreModel):
    pass
