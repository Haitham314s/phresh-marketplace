import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_cleaning(client: AsyncClient):
    res = await client.get("/cleanings")
    assert res.status_code == 200


@pytest.mark.anyio
async def test_create_cleaning(client: AsyncClient):
    new_cleaning = {
        "name": "test cleaning",
        "type": "spot_clean",
        "price": 29.99,
    }
    res = await client.post("/cleaning", json=new_cleaning)
    assert res.status_code == 201
