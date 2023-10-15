import pytest
from httpx import AsyncClient

from app.models import User
from app.models.schemas.profile import ProfileOut


@pytest.mark.parametrize(
    "profile_in",
    (
        ({"full_name": "Lebron James"}),
        ({"phone": "555-333-1000"}),
        ({"description": "This is a test bio"}),
        ({"image": "http://testimages.com/testimage"}),
    ),
)
@pytest.mark.anyio
async def test_update_user_profile(authorized_client: AsyncClient, test_user: User, profile_in: dict):
    for key, value in profile_in.items():
        assert getattr(test_user.profile, key) != value

    res = await authorized_client.put("/user/profile", json=profile_in)
    assert res.status_code == 200
    profile = ProfileOut(**res.json())

    for key, value in profile_in.items():
        assert getattr(profile, key) == value


@pytest.mark.parametrize(
    "profile_in, status_code",
    (
        ({"full_name": []}, 422),
        ({"description": {}}, 422),
        ({"image": "./image-string.png"}, 422),
        ({"image": 5}, 422),
    ),
)
@pytest.mark.anyio
async def test_invalid_update_user_profile(
    authorized_client: AsyncClient, test_user: User, profile_in: dict, status_code
):
    res = await authorized_client.put("/user/profile", json=profile_in)
    assert res.status_code == status_code
