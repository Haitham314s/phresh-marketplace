import asyncio
from typing import List
from uuid import UUID

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories.offers import OfferRepository
from app.models import User
from app.models.cleaning import Cleaning, CleaningType
from app.models.schemas.cleaning import CleaningBase, CleaningUpdateIn
from app.models.schemas.public_out import CleaningOut, OfferDetailOut


class CleaningRepository:
    def __init__(self):
        self.offer_repo = OfferRepository()

    async def populate_cleaning(self, cleaning: Cleaning) -> Cleaning:
        offers = await self.offer_repo.get_cleaning_offers(cleaning.id)
        cleaning.offers = [OfferDetailOut.model_validate(offer, from_attributes=True) for offer in offers]
        cleaning.total_offers = len(offers)
        return cleaning

    async def get_all_cleanings(self, user: User, populate: bool = True) -> List[CleaningOut]:
        cleanings = await Cleaning.filter(user_id=user.id, type__not=CleaningType.deleted).order_by("-created_at")

        if populate:
            cleanings = await asyncio.gather(*[self.populate_cleaning(cleaning) for cleaning in cleanings])
            return [CleaningOut.model_validate(cleaning) for cleaning in cleanings]

        return [CleaningOut.model_validate(cleaning) for cleaning in cleanings]

    async def get_cleaning_by_id(self, cleaning_id: UUID, user: User | None = None, populate: bool = True) -> Cleaning:
        cleaning = await Cleaning.get_or_none(id=cleaning_id, type__not=CleaningType.deleted)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if user is not None and cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)
        if populate:
            await cleaning.fetch_related("user")
            return await self.populate_cleaning(cleaning)

        return cleaning

    async def create_cleaning(self, new_cleaning: CleaningBase, user: User) -> Cleaning:
        return await Cleaning.create(**new_cleaning.model_dump(), user_id=user.id)

    async def update_cleaning(self, cleaning_id: UUID, cleaning_in: CleaningUpdateIn, user: User) -> Cleaning:
        cleaning = await Cleaning.get_or_none(id=cleaning_id, type__not=CleaningType.deleted)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)

        cleaning_dict = CleaningOut.model_validate(cleaning).model_dump()
        cleaning_dict |= {key: value for key, value in cleaning_in.model_dump().items() if value is not None}

        await cleaning.update_from_dict(cleaning_dict)
        return cleaning

    async def delete_cleaning(self, cleaning_id: UUID, user: User):
        cleaning = await Cleaning.get_or_none(id=cleaning_id)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)

        cleaning.type = CleaningType.deleted
        await cleaning.save()
