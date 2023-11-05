import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient):
    res = await client.get("/feed/cleanings")
    assert res.status_code != status.HTTP_404_NOT_FOUND
