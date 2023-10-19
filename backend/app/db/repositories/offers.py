from uuid import UUID

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories.cleanings import CleaningRepository
from app.models import User
from app.models.offer import Offer, OfferStatus
from app.models.schemas.offer import OfferBase


class OfferRepository:
    async def create_cleaning_offer(self, offer_in: OfferBase) -> Offer:
        if await Offer.filter(cleaning_id=offer_in.cleaning_id, user_id=offer_in.user_id).count():
            raise APIException(ErrorCode.offer_already_created)

        return await Offer.create(**offer_in.model_dump())

    async def get_cleaning_offers(self, cleaning_id: UUID, user: User):
        await CleaningRepository().get_cleaning_by_id(cleaning_id, user)
        return await Offer.filter(cleaning_id=cleaning_id, status__not=OfferStatus.deleted)
