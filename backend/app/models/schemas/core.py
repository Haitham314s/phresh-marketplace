from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CoreModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class IDModelMixin(BaseModel):
    id: int
