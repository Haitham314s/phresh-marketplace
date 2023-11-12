from typing import Callable

import pytest
from fastapi import status

from app.db.repositories import offer_repo
from app.models import User
from app.models.offer import OfferStatus
from app.models.schemas.public_out import OfferDetailOut
from tests.shared.offers import new_cleaning_with_accepted_offer


cancel_offer_in = {"status": OfferStatus.cancelled}


@pytest.mark.anyio
async def test_cancel_accepted_offer(create_authorized_client: Callable, test_users: list[User]):
    user = test_users[1]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_accepted_offer(test_users[0], test_users[1:])
    offer = [
        offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.status == OfferStatus.accepted
    ][0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offer.id}", json=cancel_offer_in)
    assert res.status_code == status.HTTP_200_OK

    cancelled_offer = OfferDetailOut(**res.json())
    assert cancelled_offer.status == OfferStatus.cancelled
    assert cancelled_offer.user.id == offer.user_id
    assert cancelled_offer.cleaning.id == cleaning.id


@pytest.mark.anyio
async def test_only_cancel_accepted_offers(create_authorized_client: Callable, test_users: list[User]):
    authorized_client = create_authorized_client(test_users[1])
    cleaning = await new_cleaning_with_accepted_offer(test_users[0], test_users[1:])
    offer = [
        offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.status != OfferStatus.accepted
    ][0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offer.id}", json=cancel_offer_in)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_other_offers_when_cancelled(create_authorized_client: Callable, test_users: list[User]):
    user = test_users[1]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_accepted_offer(test_users[0], test_users[1:])
    offers = await offer_repo.get_cleaning_offers(cleaning.id)
    accepted_offer = [offer for offer in offers if offer.status == OfferStatus.accepted][0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{accepted_offer.id}", json=cancel_offer_in)
    assert res.status_code == status.HTTP_200_OK

    offers = await offer_repo.get_cleaning_offers(cleaning.id)
    for offer in offers:
        if offer.user_id == user.id:
            assert offer.status == OfferStatus.cancelled
        else:
            assert offer.status == OfferStatus.pending
