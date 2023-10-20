from fastapi import Depends

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.cleanings import get_cleaning_by_id
from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models import User, Cleaning


async def check_create_offer_permission(
    user: User = Depends(get_current_user), cleaning: Cleaning = Depends(get_cleaning_by_id)
):
    if cleaning.user_id == user.id:
        raise APIException(ErrorCode.offer_method_not_allowed)


async def check_get_offer_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)
):
    if cleaning.user_id != user.id:
        raise APIException(ErrorCode.offer_unauthorized_access)

    return cleaning
