from fastapi import Depends

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories import offer_repo
from app.models import Cleaning, Offer, User
from .auth import get_current_user
from .cleanings import get_cleaning_by_id
from ...models.offer import OfferStatus


async def check_create_evaluation_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)
) -> Offer:
    if cleaning.user_id != user.id:
        raise APIException(ErrorCode.evaluation_unauthorized_access)
    offer = await offer_repo.get_accepted_offer_from_id(cleaning.id)
    if offer.status != OfferStatus.accepted:
        raise APIException(ErrorCode.offer_has_wrong_status)

    return offer
