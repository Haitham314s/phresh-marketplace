from uuid import UUID

from tortoise.transactions import in_transaction

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories.cleanings import CleaningRepository
from app.models import User
from app.models.offer import Offer, OfferStatus
from app.models.schemas.offer import OfferBase, OfferUpdateIn


class OfferRepository:
    async def create_cleaning_offer(self, offer_in: OfferBase) -> Offer:
        if await Offer.filter(cleaning_id=offer_in.cleaning_id, user_id=offer_in.user_id).count():
            raise APIException(ErrorCode.offer_already_created)

        return await Offer.create(**offer_in.model_dump())

    async def get_cleaning_offers(self, cleaning_id: UUID) -> list[Offer]:
        return await Offer.filter(cleaning_id=cleaning_id, status__not=OfferStatus.deleted)

    async def get_cleaning_offer_by_id(self, offer_id: UUID, populate: bool = True) -> Offer:
        offer = await Offer.get_or_none(id=offer_id, status__not=OfferStatus.deleted)
        if offer is None:
            raise APIException(ErrorCode.offer_not_found)
        if populate:
            await offer.fetch_related("cleaning", "user")

        return offer

    async def update_cleaning_offer(self, offer_id: UUID, offer_in: OfferUpdateIn):
        offer = await self.get_cleaning_offer_by_id(offer_id)
        offers_query = Offer.filter(id__not=offer_id, cleaning_id=offer_in.cleaning_id, status__not=OfferStatus.deleted)

        if offer.status != OfferStatus.pending:
            raise APIException(ErrorCode.offer_method_not_allowed)
        if OfferStatus.accepted in [offer.status for offer in await offers_query]:
            raise APIException(ErrorCode.offer_method_not_allowed)

        async with in_transaction(connection_name="default"):
            if offer_in.status == OfferStatus.accepted:
                await offers_query.update(status=OfferStatus.rejected)

            offer.status = offer_in.status
            await offer.save()

        return offer
