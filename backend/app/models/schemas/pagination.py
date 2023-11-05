from pydantic import Field

from app.models.schemas.core import CoreModel


class Pagination(CoreModel):
    page: int | None = Field(default=0)
    limit: int | None = Field(default=10, ge=1, le=50, description="Limit of cleaning feeds to return to response")
