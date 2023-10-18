import pytest
from fastapi import status
from httpx import AsyncClient

from app.models import User
from tests.shared.cleanings import new_cleaning


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)
    res = await client.post(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code != status.HTTP_404_NOT_FOUND

    res = await client.get(f"/cleaning/{cleaning.id}/offers")
    assert res.status_code != status.HTTP_404_NOT_FOUND

    res = await client.put(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code != status.HTTP_404_NOT_FOUND

    res = await client.put(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code != status.HTTP_404_NOT_FOUND

    res = await client.delete(f"/cleaning/{cleaning.id}/offer")
    assert res.status_code != status.HTTP_404_NOT_FOUND
