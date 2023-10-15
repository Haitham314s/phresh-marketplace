from typing import Type

import pytest
from httpx import AsyncClient
from jose import jwt
from jose.exceptions import JWSError, JWTClaimsError
from pydantic import ValidationError

from app.core.config import config
from app.core.error import APIException
from app.models.user import User
from app.services import auth_service


@pytest.mark.anyio
async def test_create_access_token(test_user: User) -> None:
    access_token = auth_service.create_access_token(
        user=test_user,
        secret_key=config.secret_key,
        audience=config.jwt_audience,
        expires_in=config.access_token_expire_minutes,
    )

    creds = jwt.decode(
        access_token,
        config.secret_key,
        audience=config.jwt_audience,
        algorithms=[config.jwt_algorithm],
    )
    assert creds.get("username") is not None
    assert creds.get("username") == test_user.username
    assert creds.get("aud") == config.jwt_audience


@pytest.mark.anyio
async def test_token_with_invalid_user() -> None:
    with pytest.raises(APIException):
        access_token = auth_service.create_access_token(
            user=None,
            secret_key=config.secret_key,
            audience=config.jwt_audience,
            expires_in=config.access_token_expire_minutes,
        )

        jwt.decode(access_token, config.secret_key, audience=config.jwt_audience)


@pytest.mark.parametrize(
    "secret_key, jwt_audience, exception",
    (
        # ("wrong-secret", config.jwt_audience, JWTError),
        (None, config.jwt_audience, JWSError),
        (config.secret_key, "othersite:auth", JWTClaimsError),
        (config.secret_key, None, ValidationError),
    ),
)
@pytest.mark.anyio
async def test_invalid_token_content(
    test_user: User,
    secret_key: str | None,
    jwt_audience: str,
    exception: Type[BaseException],
):
    with pytest.raises(exception):
        access_token = auth_service.create_access_token(
            user=test_user,
            secret_key=secret_key,
            audience=jwt_audience,
            expires_in=config.access_token_expire_minutes,
        )

        jwt.decode(
            access_token,
            secret_key,
            audience=config.jwt_audience,
            algorithms=[config.jwt_algorithm],
        )


@pytest.mark.anyio
async def test_username_from_token(client: AsyncClient, test_user: User):
    token = auth_service.create_access_token(test_user, config.secret_key)
    user = await auth_service.get_user_from_token(token, config.secret_key)
    assert user.username == test_user.username


@pytest.mark.parametrize(
    "secret, wrong_token",
    (
        (config.secret_key, "asdf"),  # use wrong token
        (config.secret_key, ""),  # use wrong token
        (config.secret_key, None),  # use wrong token
        ("ABC123", "use correct token"),  # use wrong secret
    ),
)
@pytest.mark.anyio
async def test_token_or_secret_error(test_user: User, secret: str, wrong_token: str | None):
    token = auth_service.create_access_token(test_user, config.secret_key)
    if wrong_token == "use correct token":
        wrong_token = token

    with pytest.raises(APIException):
        await auth_service.get_user_from_token(wrong_token, secret)
