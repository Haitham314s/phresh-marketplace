from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CoreModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class IDModelMixin(BaseModel):
    id: UUID
