from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from app.models.schemas.cleaning import CleaningBase, CleaningOut

from ..shared.cleanings import create_cleaning_info


@pytest.mark.anyio
async def test_get_all_cleanings(client: AsyncClient):
    res = await client.get("/cleanings")
    assert res.status_code == 200


@pytest.mark.anyio
async def test_valid_create_cleaning(client: AsyncClient):
    new_cleaning = {
        "name": "test cleaning",
        "type": "spot_clean",
        "price": 29.99,
    }

    res = await client.post("/cleaning", json=new_cleaning)
    assert res.status_code == 201
    assert CleaningBase(**new_cleaning) == CleaningBase(**res.json())


@pytest.mark.parametrize(
    "invalid_payload, status_code",
    (
        (None, 422),
        ({}, 422),
        ({"name": "test_name"}, 422),
        ({"price": 10.00}, 422),
        ({"name": "test_name", "description": "test"}, 422),
    ),
)
@pytest.mark.anyio
async def test_invalid_create_cleaning(
    client: AsyncClient, invalid_payload: dict | None, status_code: int
):
    res = await client.post("/cleaning", json=invalid_payload)
    assert res.status_code == status_code


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
