from __future__ import annotations

from uuid import UUID

from app.models.offer import OfferStatus
from .cleaning import CleaningPydanticOut
from .core import CoreModel
from .user import UserPublicOut


class CleaningOut(CleaningPydanticOut, CoreModel):
    user_id: UUID | None = None
    price: float
    total_offers: int | None = 0
    offers: list[OfferDetailOut] | None = []


class OfferDetailOut(CoreModel):
    user: UserPublicOut
    cleaning: CleaningOut
    status: OfferStatus | None = OfferStatus.pending


CleaningOut.model_rebuild()
