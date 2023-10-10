from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class CoreModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DateTimeModelMixin(BaseModel):
    created_at: datetime | None = None
    modified_at: datetime | None = None

    @field_validator("created_at", "modified_at")
    @classmethod
    def default_datetime(cls, v: datetime | None) -> datetime:
        return v or datetime.now()


class IDModelMixin(BaseModel):
    id: UUID
