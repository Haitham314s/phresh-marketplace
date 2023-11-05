from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.cleanings import get_cleaning_by_id
from app.api.dependencies.offers import (
    check_create_offer_permission,
    check_get_offer_permission,
    check_update_offer_permission,
    check_delete_offer_permission,
)
from app.core.response import SUCCESS_RESPONSE
from app.db.repositories import offer_repo
from app.models import User, Cleaning
from app.models.schemas.offer import OfferBase, OfferDetailOut, OfferUpdateIn, OfferUserMixin

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


@router.get("s", response_model=list[OfferUserMixin])
async def list_cleaning_offers(cleaning: Cleaning = Depends(check_get_offer_permission)):
    cleaning_offers = await offer_repo.get_cleaning_offers(cleaning.id)
    return [OfferUserMixin.model_validate(offer, from_attributes=True) for offer in cleaning_offers]


@router.get(
    "/{offer_id}",
    response_model=OfferDetailOut,
    dependencies=[Depends(check_get_offer_permission), Depends(get_current_user)],
)
async def get_offer(offer_id: UUID):
    cleaning_offer = await offer_repo.get_cleaning_offer_by_id(offer_id)
    return OfferDetailOut.model_validate(cleaning_offer, from_attributes=True)


@router.put("/{offer_id}", response_model=OfferDetailOut)
async def update_offer_state(
    offer_id: UUID,
    offer_in: OfferUpdateIn,
    cleaning: Cleaning = Depends(check_update_offer_permission),
    user: User = Depends(get_current_user),
):
    offer_in = OfferUpdateIn(status=offer_in.status, cleaning_id=cleaning.id, user_id=user.id)
    offer = await offer_repo.update_cleaning_offer(offer_id, offer_in)
    return OfferDetailOut.model_validate(offer, from_attributes=True)


@router.delete("/{offer_id}", dependencies=[Depends(check_delete_offer_permission)])
async def rescind_offer(offer_id: UUID):
    await offer_repo.delete_cleaning_offer_by_id(offer_id)
    return SUCCESS_RESPONSE
