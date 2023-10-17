import pytest
from httpx import AsyncClient

from app.models import User
from app.models.schemas.cleaning import CleaningBase
from tests.shared.cleanings import new_cleaning


@pytest.mark.anyio
async def test_valid_create_cleaning(authorized_client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)
    cleaning_dict = CleaningBase.model_validate(cleaning, from_attributes=True).model_dump()

    res = await authorized_client.post("/cleaning", json=cleaning_dict)
    created_cleaning = CleaningBase(**res.json())

    assert res.status_code == 201
    assert created_cleaning.name == cleaning.name
    assert created_cleaning.price == cleaning.price
    assert created_cleaning.type == cleaning.type


@pytest.mark.anyio
async def test_unauthorized_user_access_cleaning_create(client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)
    cleaning_dict = CleaningBase.model_validate(cleaning, from_attributes=True).model_dump()

    res = await client.post("/cleaning", json=cleaning_dict)
    assert res.status_code == 401


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
async def test_invalid_create_cleaning(authorized_client: AsyncClient, invalid_payload: dict | None, status_code: int):
    res = await authorized_client.post("/cleaning", json=invalid_payload)
    assert res.status_code == status_code
