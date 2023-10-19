from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models import User
from app.models.offer import Offer
from app.models.schemas.offer import OfferBase


class OfferRepository:
    async def create_cleaning_offer(self, offer_in: OfferBase, user: User) -> Offer:
        if await Offer.filter(user_id=user.id).count():
            raise APIException(ErrorCode.offer_already_created)

        return await Offer.create(**offer_in.model_dump())
