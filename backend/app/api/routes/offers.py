from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.cleanings import get_cleaning_by_id
from app.api.dependencies.offers import check_create_offer_permission, check_get_offer_permission
from app.db.repositories import offer_repo
from app.models import User, Cleaning
from app.models.schemas.offer import OfferBase, OfferDetailOut

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=OfferBase,
    dependencies=[Depends(check_create_offer_permission)],
)
async def create_offer(cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)):
    offer_in = OfferBase(user_id=user.id, cleaning_id=cleaning.id)
    return await offer_repo.create_cleaning_offer(offer_in)


@router.get("s", response_model=list[OfferBase])
async def list_cleaning_offers(cleaning: Cleaning = Depends(check_get_offer_permission)):
    cleaning_offers = await offer_repo.get_cleaning_offers(cleaning.id)
    return [OfferBase.model_validate(offer, from_attributes=True) for offer in cleaning_offers]


@router.get(
    "/{offer_id}",
    response_model=OfferDetailOut,
    dependencies=[Depends(check_get_offer_permission), Depends(get_current_user)],
)
async def get_offer(offer_id: UUID):
    cleaning_offers = await offer_repo.get_cleaning_offer(offer_id)
    return OfferDetailOut.model_validate(cleaning_offers)


@router.put("")
async def update_offer_state():
    pass


@router.delete("")
async def delete_offer():
    pass
