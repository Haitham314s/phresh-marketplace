from datetime import datetime
from typing import Literal
from uuid import UUID

from app.models.schemas.cleaning import CleaningOut
from app.models.schemas.core import CoreModel


class FeedItem(CoreModel):
    row_number: int | None = None
    event_timestamp: datetime | None = None


class CleaningFeedItem(CleaningOut, FeedItem):
    event_type: Literal["is_update", "is_create"] | None = None
    created_at: datetime
    modified_at: datetime
    user_id: UUID
