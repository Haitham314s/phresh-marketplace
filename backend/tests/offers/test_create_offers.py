from typing import Callable
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from app.models import User
from app.models.schemas.offer import OfferOut
from tests.shared.cleanings import new_cleaning, get_or_create_cleaning


async def test_user_create_offer(
    create_authorized_client: Callable,
    test_users: list[User],
):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning(test_users[0])

    res = await authorized_client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code == status.HTTP_201_CREATED

    offer = OfferOut(**res.json())
    assert offer.user_id == user.id
    assert offer.cleaning_id == cleaning.id
    assert offer.status == "pending"


async def test_user_create_duplicate_offers(
    create_authorized_client: Callable,
    test_users: list[User],
) -> None:
    user = test_users[1]
    authorized_client = create_authorized_client(user)
    cleaning = await new_cleaning(user)

    res = await authorized_client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code == status.HTTP_201_CREATED

    res = await authorized_client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code == status.HTTP_400_BAD_REQUEST


async def test_user_create_own_cleaning_offer(
    authorized_client: AsyncClient,
    test_user: User,
):
    cleaning = await get_or_create_cleaning(test_user)
    res = await authorized_client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code == status.HTTP_400_BAD_REQUEST


async def test_unauthenticated_user_create_offers(client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)
    res = await client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "cleaning_id, status_code",
    (
        (uuid4(), 404),
        (-1, 422),
        (None, 422),
    ),
)
async def test_wrong_id_gives_proper_error_status(
    create_authorized_client: Callable,
    test_users: list[User],
    cleaning_id,
    status_code: int,
) -> None:
    user = test_users[2]
    authorized_client = create_authorized_client(user=user)
    res = await authorized_client.post(f"/cleaning/{cleaning_id}/offer")
    assert res.status_code == status_code
