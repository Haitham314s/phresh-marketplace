from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.models import User
from tests.shared.cleanings import new_cleaning


@pytest.mark.anyio
async def test_delete_cleaning(authorized_client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)
    res = await authorized_client.delete(f"/cleaning/{cleaning.id}")
    assert res.status_code == 200


@pytest.mark.anyio
async def test_delete_other_user_cleanings(authorized_client: AsyncClient, test_user2: User):
    cleaning = await new_cleaning(test_user2)
    res = await authorized_client.delete(f"/cleaning/{cleaning.id}")
    assert res.status_code == 403


@pytest.mark.parametrize("cleaning_id, status_code", ((uuid4(), 404), (0, 422), (-1, 422), (None, 422)))
@pytest.mark.anyio
async def test_delete_with_wrong_id(authorized_client: AsyncClient, cleaning_id, status_code: int):
    res = await authorized_client.delete(f"/cleaning/{cleaning_id}")
    assert res.status_code == status_code
