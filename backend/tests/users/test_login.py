import pytest
from httpx import AsyncClient
from jose import jwt

from app.core.config import config
from app.models import User


@pytest.mark.anyio
async def test_user_login(client: AsyncClient, test_user: User):
    client.headers["content-type"] = "application/x-www-form-urlencoded"
    login_data = {"username": test_user.username, "password": "test123"}

    res = await client.post("/auth/token", data=login_data)
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

    res = await client.post("/auth/token", data=login_data)
    assert res.status_code == status_code
    assert "access_token" not in res.json()
