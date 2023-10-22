from typing import Callable

import pytest
from fastapi import status

from app.db.repositories import offer_repo
from app.models import User
from app.models.offer import OfferStatus
from tests.shared.offers import new_cleaning_with_offers, new_cleaning_with_accepted_offer
from .test_cancel_offers import cancel_offer_in


@pytest.mark.anyio
async def test_successfully_rescind_offer(create_authorized_client: Callable, test_user: User, test_users: list[User]):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_offers(test_user, test_users)
    deleted_offer = (await offer_repo.get_cleaning_offers(cleaning.id))[0]

    res = await authorized_client.delete(f"/cleaning/{cleaning.id}/offer/{deleted_offer.id}")
    assert res.status_code == status.HTTP_200_OK

    offers = await offer_repo.get_cleaning_offers(cleaning.id)
    user_ids = [user.id for user in test_users if user.id != deleted_offer.user_id]
    for offer in offers:
        assert offer.user_id in user_ids and offer.user_id != deleted_offer


@pytest.mark.anyio
async def test_rescind_accepted_offers(create_authorized_client: Callable, test_user: User, test_users: list[User]):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_accepted_offer(test_user, test_users)
    offer = [
        offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.status == OfferStatus.accepted
    ][0]

    res = await authorized_client.delete(f"/cleaning/{cleaning.id}/offer/{offer.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_rescind_cancelled_offers(create_authorized_client: Callable, test_user: User, test_users: list[User]):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_accepted_offer(test_user, test_users)
    offer = [
        offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.status == OfferStatus.accepted
    ][0]

    res = await authorized_client.put(f"/cleaning/{cleaning.id}/offer/{offer.id}", json=cancel_offer_in)
    assert res.status_code == status.HTTP_200_OK

    res = await authorized_client.delete(f"/cleaning/{cleaning.id}/offer/{offer.id}")
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_unauthorized_user_rescind_offer(
    create_authorized_client: Callable, test_user: User, test_users: list[User]
):
    user = test_users[1]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_with_offers(test_user, test_users)
    offer = [offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.user_id == test_users[0].id][
        0
    ]

    res = await authorized_client.delete(f"/cleaning/{cleaning.id}/offer/{offer.id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN
