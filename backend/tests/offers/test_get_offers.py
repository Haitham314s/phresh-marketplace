from typing import Callable

import pytest
from fastapi import status
from httpx import AsyncClient

from app.models import User, Cleaning
from app.models.schemas.offer import OfferBase
from tests.shared.offers import new_cleaning_offer


@pytest.mark.anyio
async def test_get_cleaning_offer(create_authorized_client: Callable, test_user2: User, test_users: list[User]):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_offer(test_user2, test_users)

    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offers")
    offers = [OfferBase(**offer) for offer in res.json()]
    assert res.status_code == status.HTTP_200_OK

    user_ids = [user.id for user in test_users]
    for offer in offers:
        assert offer.user_id in user_ids


@pytest.mark.anyio
async def test_user_get_cleaning_offer(create_authorized_client: Callable, test_users: list[User]):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning_offer(user, test_users[1:])

    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offers")
    assert res.status_code == status.HTTP_200_OK
    offer = OfferBase(**res.json()[0])
    user_cleaning = await Cleaning.get_or_none(id=offer.cleaning_id)
    assert user_cleaning.user_id == user.id


@pytest.mark.anyio
async def test_authenticated_get_other_user_cleaning_offer(create_authorized_client: Callable, test_users: list[User]):
    user_1 = test_users[0]
    user_2 = test_users[1]
    authorized_client = create_authorized_client(user_2)
    cleaning = await new_cleaning_offer(user_1, test_users[1:])

    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offers")
    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_user_forbidden_get_all_cleaning_offers(authorized_client: AsyncClient, test_users: list[User]):
    cleaning = await new_cleaning_offer(test_users[0], test_users[1:])
    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offers")
    assert res.status_code == status.HTTP_403_FORBIDDEN
