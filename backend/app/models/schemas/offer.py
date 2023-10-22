from uuid import UUID

from app.models.offer import OfferStatus
from app.models.schemas.cleaning import CleaningOut
from app.models.schemas.core import CoreModel
from app.models.schemas.user import UserPublicOut


class OfferBase(CoreModel):
    user_id: UUID
    cleaning_id: UUID
    status: OfferStatus | None = OfferStatus.pending


class OfferUpdateIn(CoreModel):
    user_id: UUID | None = None
    cleaning_id: UUID | None = None
    status: OfferStatus


class OfferDetailOut(CoreModel):
    user: UserPublicOut
    cleaning: CleaningOut
    status: OfferStatus | None = OfferStatus.pending
