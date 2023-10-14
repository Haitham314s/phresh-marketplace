from httpx import AsyncClient
import pytest
from jose import jwt

from app.core.config import config
from app.models import User
from app.models.schemas.user import UserPublicOut
from app.services import auth_service


@pytest.mark.anyio
async def test_user_login(client: AsyncClient, test_user: User):
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {"username": test_user.username, "password": "test123"}

    res = await client.post("/user/token", data=login_data)
    assert res.status_code == 200

    token = res.json().get("access_token")
    creds = jwt.decode(token, config.secret_key, audience=config.jwt_audience, algorithms=[config.jwt_algorithm])

    assert "username" in creds
    assert creds["username"] == test_user.username
    assert "sub" in creds
    assert creds["sub"] in [test_user.username, test_user.email]
    assert "token_type" in res.json()
    assert res.json().get("token_type") == "bearer"


@pytest.mark.parametrize(
    "form_data, status_code",
    (
        ({"email": "wrong@email.com"}, 401),
        ({"email": None}, 401),
        ({"email": "notemail"}, 401),
        ({"password": "wrongpassword"}, 401),
        ({"password": None}, 422),
    ),
)
@pytest.mark.anyio
async def test_invalid_user_login(client: AsyncClient, test_user: User, form_data: dict, status_code: int):
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    user_data = test_user.__dict__
    user_data |= form_data

    login_data = {
        "username": user_data["username"],
        "password": user_data["password"] if "password" in user_data else user_data["hashed_password"],
    }

    res = await client.post("/user/token", data=login_data)
    assert res.status_code == status_code
    assert "access_token" not in res.json()


@pytest.mark.anyio
async def test_authenticated_user_login(authorized_client: AsyncClient, test_user: User):
    res = await authorized_client.get("/user/token")
    assert res.status_code == 200

    user = UserPublicOut(**res.json())
    assert user.email == test_user.email
    assert user.username == test_user.username
    assert user.id == test_user.id


@pytest.mark.anyio
async def test_unauthorized_user_access(client: AsyncClient, test_user: User):
    res = await client.get("/user")
    assert res.status_code == 401


@pytest.mark.parametrize("jwt_prefix", (("",), ("value",), ("Token",), ("JWT",), ("Swearer",),))
@pytest.mark.anyio
async def test_user_invalid_token(client: AsyncClient, test_user: User, jwt_prefix: str):
    token = auth_service.create_access_token_for_user(user=test_user, secret_key=config.secret_key)
    res = await client.get("/user", headers={"Authorization": f"{jwt_prefix} {token}"})
    assert res.status_code == 401
