from uuid import UUID

from fastapi import Depends

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories import offer_repo
from app.models import User, Cleaning, Offer
from .auth import get_current_user
from .cleanings import get_cleaning_by_id


async def check_create_offer_permission(
    user: User = Depends(get_current_user), cleaning: Cleaning = Depends(get_cleaning_by_id)
) -> None:
    if cleaning.user_id == user.id:
        raise APIException(ErrorCode.offer_method_not_allowed)


async def check_get_offer_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)
) -> Cleaning:
    if cleaning.user_id != user.id:
        raise APIException(ErrorCode.offer_unauthorized_access)

    return cleaning


async def get_offer_by_id(offer_id: UUID) -> Offer:
    return await offer_repo.get_cleaning_offer_by_id(offer_id, False)


async def check_update_offer_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id),
    offer: Offer = Depends(get_offer_by_id),
    user: User = Depends(get_current_user),
) -> Cleaning:
    if user.id not in [cleaning.user_id, offer.user_id]:
        raise APIException(ErrorCode.offer_method_not_allowed)

    return cleaning


async def check_delete_offer_permission(
    offer: Offer = Depends(get_offer_by_id),
    user: User = Depends(get_current_user),
) -> None:
    if user.id != offer.user_id:
        raise APIException(ErrorCode.offer_unauthorized_access)
