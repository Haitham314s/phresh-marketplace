from uuid import UUID

from tortoise.queryset import QuerySet
from tortoise.transactions import atomic

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models.offer import Offer, OfferStatus
from app.models.schemas.offer import OfferBase, OfferUpdateIn


class OfferRepository:
    async def create_cleaning_offer(self, offer_in: OfferBase) -> Offer:
        if await Offer.filter(cleaning_id=offer_in.cleaning_id, user_id=offer_in.user_id).count():
            raise APIException(ErrorCode.offer_already_created)

        return await Offer.create(**offer_in.model_dump())

    async def get_cleaning_offers(self, cleaning_id: UUID, populate: bool = True) -> list[Offer]:
        offer_query = Offer.filter(cleaning_id=cleaning_id, status__not=OfferStatus.deleted)
        if populate:
            return await offer_query.prefetch_related("user", "cleaning")
        return await offer_query

    async def get_cleaning_offer_by_id(self, offer_id: UUID, populate: bool = True) -> Offer:
        offer = await Offer.get_or_none(id=offer_id, status__not=OfferStatus.deleted)
        if offer is None:
            raise APIException(ErrorCode.offer_not_found)
        if populate:
            await offer.fetch_related("cleaning", "user")

        return offer

    @atomic("default")
    async def accept_cleaning_offer(
        self, offer: Offer, offers_query: QuerySet[Offer], offer_in: OfferUpdateIn
    ) -> Offer:
        if offer.cleaning.user_id != offer_in.user_id:
            raise APIException(ErrorCode.offer_unauthorized_access)
        if offer.status != OfferStatus.pending:
            raise APIException(ErrorCode.offer_method_not_allowed)
        if OfferStatus.accepted in [offer.status for offer in await offers_query]:
            raise APIException(ErrorCode.offer_method_not_allowed)

        await offers_query.update(status=OfferStatus.rejected)
        offer.status = offer_in.status
        await offer.save()
        return offer

    async def reject_cleaning_offer(self, offer: Offer, offer_in: OfferUpdateIn) -> Offer:
        # TODO: Add reject restrictions

        offer.status = offer_in.status
        await offer.save()
        return offer

    @atomic("default")
    async def cancel_cleaning_offer(
        self, offer: Offer, offers_query: QuerySet[Offer], offer_in: OfferUpdateIn
    ) -> Offer:
        if offer.user.id != offer_in.user_id:
            raise APIException(ErrorCode.offer_unauthorized_access)
        if offer.status != OfferStatus.accepted:
            raise APIException(ErrorCode.offer_method_not_allowed)

        await offers_query.update(status=OfferStatus.pending)
        offer.status = offer_in.status
        await offer.save()
        return offer

    async def complete_cleaning_offer(self, offer: Offer, offer_in: OfferUpdateIn) -> Offer:
        if offer.status != OfferStatus.accepted:
            raise APIException(ErrorCode.offer_has_wrong_status)

        offer.status = offer_in.status
        await offer.save()
        return offer

    async def update_cleaning_offer(self, offer_id: UUID, offer_in: OfferUpdateIn) -> Offer:
        offer = await self.get_cleaning_offer_by_id(offer_id)
        offers_query = Offer.filter(id__not=offer_id, cleaning_id=offer_in.cleaning_id)

        if offer_in.status == OfferStatus.accepted:
            offers_query = offers_query.filter(status=OfferStatus.pending)
            return await self.accept_cleaning_offer(offer, offers_query, offer_in)
        elif offer_in.status == OfferStatus.rejected:
            return await self.reject_cleaning_offer(offer, offer_in)
        elif offer_in.status == OfferStatus.cancelled:
            offers_query = offers_query.filter(status=OfferStatus.rejected)
            return await self.cancel_cleaning_offer(offer, offers_query, offer_in)
        elif offer_in.status == OfferStatus.completed:
            return await self.complete_cleaning_offer(offer, offer_in)

        raise APIException(ErrorCode.system_not_implemented)

    async def delete_cleaning_offer_by_id(self, offer_id: UUID) -> None:
        offer = await Offer.get_or_none(id=offer_id, status__not=OfferStatus.deleted)
        if offer is None:
            raise APIException(ErrorCode.offer_not_found)
        if offer.status != OfferStatus.pending:
            raise APIException(ErrorCode.offer_has_wrong_status)

        offer.status = OfferStatus.deleted
        await offer.save()

    async def get_accepted_offer_from_id(self, cleaning_id: UUID) -> Offer:
        offer = await Offer.get_or_none(cleaning_id=cleaning_id, status=OfferStatus.accepted)
        if offer is None:
            raise APIException(ErrorCode.offer_not_found)

        return offer

    async def get_rejected_offers_from_id(self, cleaning_id: UUID) -> list[Offer]:
        offers = await Offer.filter(cleaning_id=cleaning_id, status=OfferStatus.rejected)
        if len(offers) == 0:
            raise APIException(ErrorCode.offer_not_found)

        return offers
