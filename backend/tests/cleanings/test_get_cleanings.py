from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from app.models.schemas.cleaning import CleaningOut

from ..shared.cleanings import create_cleaning_info


@pytest.mark.anyio
async def test_get_all_cleanings(client: AsyncClient):
    test_cleaning = await create_cleaning_info()
    res = await client.get("/cleanings")
    cleanings = [CleaningOut(**cleaning) for cleaning in res.json()]

    assert res.status_code == 200
    assert isinstance(cleanings, list)
    assert len(cleanings) > 0
    assert test_cleaning in cleanings


@pytest.mark.anyio
async def test_get_cleaning_by_id(client: AsyncClient):
    test_cleaning = await create_cleaning_info()
    res = await client.get(f"/cleaning/{str(test_cleaning.id)}")
    assert res.status_code == 200

    assert test_cleaning == CleaningOut(**res.json())


@pytest.mark.parametrize(
    "cleaning_id, status_code",
    (
        (uuid4(), 404),
        (uuid4(), 404),
        (None, 422),
    ),
)
@pytest.mark.anyio
async def test_get_cleaning_by_wrong_id(
    client: AsyncClient, cleaning_id: UUID, status_code: int
):
    res = await client.get(f"/cleaning/{cleaning_id}")
    assert res.status_code == status_code
