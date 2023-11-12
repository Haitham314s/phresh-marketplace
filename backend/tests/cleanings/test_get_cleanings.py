from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from fastapi import status

from app.models import User
from app.models.schemas.public_out import CleaningOut
from ..shared.cleanings import get_or_create_cleaning, new_cleaning_list


@pytest.mark.anyio
async def test_get_all_cleanings(authorized_client: AsyncClient, test_user: User):
    test_cleaning = await get_or_create_cleaning(test_user)
    res = await authorized_client.get("/cleanings")

    cleanings = [CleaningOut(**cleaning) for cleaning in res.json()]
    cleaning_ids = [cleaning.id for cleaning in cleanings]

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(cleanings, list)
    assert len(cleanings) > 0
    assert test_cleaning.id in cleaning_ids
    for cleaning in cleanings:
        assert cleaning.user_id == test_user.id

    test_cleanings = await new_cleaning_list(test_user)
    assert all(cl.id not in cleaning_ids for cl in test_cleanings)


@pytest.mark.anyio
async def test_get_cleaning_by_id(authorized_client: AsyncClient, test_user: User):
    test_cleaning = await get_or_create_cleaning(test_user)
    res = await authorized_client.get(f"/cleaning/{str(test_cleaning.id)}")
    assert res.status_code == 200
    assert test_cleaning == CleaningOut(**res.json())


@pytest.mark.anyio
async def test_unauthorized_user_cleaning_access(client: AsyncClient, test_user: User):
    res = await client.get(f"/cleaning/{uuid4()}")
    assert res.status_code == 401


@pytest.mark.parametrize(
    "cleaning_id, status_code",
    (
        (uuid4(), 404),
        (-1, 422),
        (None, 422),
    ),
)
@pytest.mark.anyio
async def test_get_cleaning_by_wrong_id(authorized_client: AsyncClient, cleaning_id: UUID, status_code: int):
    res = await authorized_client.get(f"/cleaning/{cleaning_id}")
    assert res.status_code == status_code
