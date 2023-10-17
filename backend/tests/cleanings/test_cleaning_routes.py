import pytest
from httpx import AsyncClient
from fastapi import status

from app.models import User
from tests.shared.cleanings import new_cleaning


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient, test_user: User):
    cleaning = await new_cleaning(test_user)

    res = await client.post("/cleaning", json={})
    assert res.status_code != status.HTTP_404_NOT_FOUND
    res = await client.get(f"/cleaning/{cleaning.id}")
    assert res.status_code != status.HTTP_404_NOT_FOUND
    res = await client.get("/cleanings")
    assert res.status_code != status.HTTP_404_NOT_FOUND
    res = await client.put(f"/cleaning/{cleaning.id}")
    assert res.status_code != status.HTTP_404_NOT_FOUND

    res = await client.delete(f"/cleaning/{cleaning.id}")
    assert res.status_code != status.HTTP_404_NOT_FOUND
