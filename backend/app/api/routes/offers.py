from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories import cleaning_repo
from app.models import User
from app.models.schemas.offer import OfferBase

router = APIRouter()


@router.post("")
async def create_offer(cleaning_id: UUID, user: User = Depends(get_current_user)):
    cleaning = await cleaning_repo.get_cleaning_by_id(cleaning_id)
    if cleaning is None:
        raise APIException(ErrorCode.cleaning_not_found)
    if cleaning.user_id == user.id:
        raise APIException(ErrorCode.offer_not_allowed)

    offer_in = OfferBase(user_id=cleaning.user_id, cleaning_id=cleaning.id)
    return await offer_repo.create_cleaning_offer(offer_in)


@router.get("s")
async def list_cleaning_offers():
    pass


@router.get("")
async def get_offer(user: User = Depends(get_current_user)):
    pass


@router.put("")
async def update_offer_state():
    pass


@router.delete("")
async def delete_offer():
    pass
