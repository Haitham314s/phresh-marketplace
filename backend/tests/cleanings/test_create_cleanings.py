import pytest
from httpx import AsyncClient

from app.models.schemas.cleaning import CleaningBase


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
