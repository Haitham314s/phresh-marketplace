from typing import Callable

import pytest
from fastapi import status
from httpx import AsyncClient

from app.db.repositories import cleaning_repo
from app.models import User, Cleaning
from app.models.schemas.public_out import CleaningOut


@pytest.mark.anyio
async def test_populated_cleaning_offers(
    authorized_client: AsyncClient,
    test_user: User,
    test_users: list[User],
    test_new_cleanings_with_pending_offer: list[Cleaning],
):
    test_user_ids = [user.id for user in test_users]
    test_cleaning_ids = [cleaning.id for cleaning in test_new_cleanings_with_pending_offer]

    res = await authorized_client.get("/cleanings")
    assert res.status_code == status.HTTP_200_OK

    cleanings = [CleaningOut(**cleaning) for cleaning in res.json()]
    for cl in cleanings:
        if cl.id in test_cleaning_ids:
            assert len(cl.offers) == len(test_users)
            assert cl.total_offers == len(test_users)
            for offer in cl.offers:
                assert offer.user.id in test_user_ids
                assert offer.user.id != cl.user_id
                assert offer.cleaning.id == cl.id


@pytest.mark.anyio
async def test_total_cleaning_offers(
    create_authorized_client: Callable,
    test_user2: User,
    test_new_cleanings_with_pending_offer: list[Cleaning],
    test_users: list[User],
):
    authorized_client = create_authorized_client(test_user2)
    test_cleaning = test_new_cleanings_with_pending_offer[0]
    res = await authorized_client.get(f"/cleaning/{test_cleaning.id}")
    assert res.status_code == status.HTTP_200_OK

    cleaning = CleaningOut(**res.json())
    assert cleaning.total_offers > 0
    assert cleaning.total_offers == len(test_users)

    test_cleaning = await cleaning_repo.get_cleaning_by_id(test_cleaning.id)
    assert cleaning.offers == test_cleaning.offers
