import pytest
from httpx import AsyncClient

from app.models import User
from app.models.schemas.profile import ProfileOut


@pytest.mark.anyio
async def test_authenticated_user_profile(authorized_client: AsyncClient, test_user: User):
    res = await authorized_client.get("/auth/user/profile")
    assert res.status_code == 200
    profile = ProfileOut(**res.json())
    assert profile.username == test_user.username


@pytest.mark.anyio
async def test_unauthorized_user_profile(client: AsyncClient, test_user: User):
    res = await client.get("/auth/user/profile")
    assert res.status_code == 401
