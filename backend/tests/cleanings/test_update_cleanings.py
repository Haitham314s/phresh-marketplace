from typing import Any, Dict
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from app.models import User
from app.models.schemas.cleaning import CleaningUpdateIn
from ..shared.cleanings import get_or_create_cleaning


@pytest.mark.parametrize(
    "cleaning_object",
    (
        ({"name": "new fake cleaning name"}),
        ({"description": "new fake cleaning description"}),
        ({"price": 3.14}),
        ({"type": "full_clean"}),
        (
            {
                "name": "extra new fake cleaning name",
                "description": "extra new fake cleaning description",
            }
        ),
        ({"price": 42.00, "type": "dust_up"}),
    ),
)
@pytest.mark.anyio
async def test_valid_update_cleaning_by_id(
    authorized_client: AsyncClient, cleaning_object: Dict[str, Any], test_user: User
):
    test_cleaning = await get_or_create_cleaning(test_user)
    res = await authorized_client.put(f"/cleaning/{str(test_cleaning.id)}", json=cleaning_object)
    assert res.status_code == 200

    updated_cleaning = res.json()
    assert updated_cleaning["id"] == str(test_cleaning.id)
    for key, value in cleaning_object.items():
        assert updated_cleaning[key] == value


@pytest.mark.anyio
async def test_unauthorized_update_cleaning(authorized_client: AsyncClient, test_user2: User):
    cleaning = await get_or_create_cleaning(test_user2)
    cleaning_in = CleaningUpdateIn.model_validate(cleaning, from_attributes=True).model_dump()
    res = await authorized_client.put(f"/cleaning/{cleaning.id}", json=cleaning_in)
    assert res.status_code == 403


@pytest.mark.parametrize(
    "cleaning_id, cleaning_payload, status_code",
    (
        (uuid4(), {"name": "test"}, 404),
        (uuid4(), {"name": "test2"}, 404),
        (uuid4(), {"name": "test3"}, 404),
        (uuid4(), None, 422),
        (500, {"type": "invalid cleaning type"}, 422),
        (uuid4(), {"type": None}, 404),
    ),
)
@pytest.mark.anyio
async def test_invalid_update_cleaning(
    authorized_client: AsyncClient,
    cleaning_id: UUID,
    cleaning_payload: Dict[str, Any] | None,
    status_code: int,
):
    res = await authorized_client.put(f"/cleaning/{cleaning_id}", json=cleaning_payload)
    assert res.status_code == status_code
