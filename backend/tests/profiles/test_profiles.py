import pytest
from httpx import AsyncClient

from app.db.repositories import profile_repo
from app.models import User, Profile


@pytest.mark.anyio
async def test_created_profile(client: AsyncClient):
    new_user = {"email": "dwayne@johnson.io", "username": "therock", "password": "dwaynetherockjohnson"}
    res = await client.post("/auth/user", json=new_user)
    assert res.status_code == 201

    user_res = res.json()
    user = await User.get_or_none(id=user_res["id"])
    user_profile = await profile_repo.get_user_profile(user)
    assert user_profile is not None
    assert isinstance(user_profile, Profile)


@pytest.mark.anyio
async def test_routes(client: AsyncClient, test_user: User):
    res = await client.get("/auth/user/profile")
    assert res.status_code != 404

    # Update own profile
    res = await client.put("/auth/user/profile", json={})
    assert res.status_code != 404
