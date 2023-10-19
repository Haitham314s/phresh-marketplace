from uuid import UUID

from fastapi import Depends

from app.api.dependencies.auth import get_current_user
from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories import cleaning_repo
from app.models import User, Cleaning


async def get_cleaning_by_id(cleaning_id: UUID, user: User = Depends(get_current_user)):
    cleaning = await cleaning_repo.get_cleaning_by_id(cleaning_id, user)
    if cleaning is None:
        raise APIException(ErrorCode.cleaning_not_found)

    return cleaning


def check_cleaning_permission(user: User = Depends(get_current_user), cleaning: Cleaning = Depends(get_cleaning_by_id)):
    if cleaning.user_id != user.id:
        raise APIException(ErrorCode.cleaning_unauthorized_access)
