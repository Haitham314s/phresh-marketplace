import pytest
from httpx import AsyncClient

from app.core.config import config
from app.models import User
from app.services import auth_service


@pytest.mark.anyio
async def test_unauthorized_user_access(client: AsyncClient, test_user: User):
    res = await client.get("/user")
    assert res.status_code == 401


@pytest.mark.parametrize(
    "jwt_prefix",
    (
        ("",),
        ("value",),
        ("Token",),
        ("JWT",),
        ("Swearer",),
    ),
)
@pytest.mark.anyio
async def test_user_invalid_token(client: AsyncClient, test_user: User, jwt_prefix: str):
    token = auth_service.create_access_token_for_user(user=test_user, secret_key=config.secret_key)
    res = await client.get("/user", headers={"Authorization": f"{jwt_prefix} {token}"})
    assert res.status_code == 401
