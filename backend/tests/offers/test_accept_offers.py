from typing import Callable

import pytest
from fastapi import status
from httpx import AsyncClient

from app.db.repositories import offer_repo
from app.models import User
from app.models.offer import OfferStatus
from app.models.schemas.offer import OfferBase, OfferDetailOut
from tests.shared.offers import new_cleaning_with_offers


offer_in = {"status": OfferStatus.accepted}


@pytest.mark.anyio
async def test_accept_offer_successfully(create_authorized_client: Callable, test_user2: User, test_users: list[User]):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_offers(test_user2, test_users)
    offer = (await offer_repo.get_cleaning_offers(cleaning.id))[0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offer.id}", json=offer_in)
    assert res.status_code == status.HTTP_200_OK

    accepted_offer = OfferDetailOut(**res.json())
    assert accepted_offer.status == OfferStatus.accepted
    assert accepted_offer.user.id == offer.user_id
    assert accepted_offer.cleaning.id == cleaning.id


@pytest.mark.anyio
async def test_unauthorized_user_accept_offer(authorized_client: AsyncClient, test_users: list[User]):
    cleaning = await new_cleaning_with_offers(test_users[0], test_users[1:])
    offer = (await offer_repo.get_cleaning_offers(cleaning.id))[0]
    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offer.id}", json=offer_in)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_accept_multiple_offers(create_authorized_client: Callable, test_user2: User, test_users: list[User]):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_offers(test_user2, test_users)
    offers = await offer_repo.get_cleaning_offers(cleaning.id)
    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offers[0].id}", json=offer_in)
    assert res.status_code == status.HTTP_200_OK

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offers[0].id}", json=offer_in)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_accept_offer_reject_other_offers(
    create_authorized_client: Callable, test_user2: User, test_users: list[User]
):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_offers(test_user2, test_users)
    cleaning_offer = (await offer_repo.get_cleaning_offers(cleaning.id))[0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{cleaning_offer.id}", json=offer_in)
    assert res.status_code == status.HTTP_200_OK

    res = await authorized_client.get(f"cleaning/{cleaning.id}/offers")
    assert res.status_code == status.HTTP_200_OK
    offers = [OfferBase(**offer) for offer in res.json()]
    for offer in offers:
        if offer.user_id == cleaning_offer.user_id:
            assert offer.status == OfferStatus.accepted
        else:
            assert offer.status == OfferStatus.rejected
