from datetime import datetime
from typing import Literal
from uuid import UUID

from .public_out import CleaningOut
from .core import CoreModel
from .user import UserPublicOut


class FeedItem(CoreModel):
    row_number: int | None = None
    event_timestamp: datetime | None = None


class CleaningFeedItem(CleaningOut, FeedItem):
    event_type: Literal["is_update", "is_create"] | None = None
    created_at: datetime
    modified_at: datetime
    user_id: UUID
    user: UserPublicOut | None = None
