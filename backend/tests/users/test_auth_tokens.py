# from typing import Type

# import pytest
# from httpx import AsyncClient
# from jose import JWTError, jwt

# from app.core.config import config
# from app.models.schemas.user import UserPublicOut
# from app.services import auth_service


# @pytest.mark.anyio
# async def test_create_access_token(
#     client: AsyncClient, test_user: UserPublicOut
# ) -> None:
#     access_token = auth_service.create_access_token(
#         user=test_user,
#         secret_key=config.secret_key,
#         audience=config.jwt_audience,
#         expires_in=config.access_token_expire_minutes,
#     )

#     creds = jwt.decode(
#         access_token,
#         config.secret_key,
#         audience=config.jwt_audience,
#         algorithms=[config.jwt_algorithm],
#     )
#     assert creds.get("username") is not None
#     assert creds.get("username") == test_user.username
#     assert creds.get("aud") == config.jwt_audience


# @pytest.mark.anyio
# async def test_token_with_invalid_user(client: AsyncClient) -> None:
#     access_token = auth_service.create_access_token(
#         user=None,
#         secret_key=config.secret_key,
#         audience=config.jwt_audience,
#         expires_in=config.access_token_expire_minutes,
#     )

#     with pytest.raises(JWTError):
#         jwt.decode(access_token, config.secret_key, audience=config.jwt_audience)


# @pytest.mark.parametrize(
#     "secret_key, jwt_audience, exception",
#     (
#         ("wrong-secret", config.jwt_audience, JWTError),
#         (None, config.jwt_audience, JWTError),
#         (config.secret_key, config.jwt_audience, JWTError),
#         (config.secret_key, None, JWTError),
#     ),
# )
# @pytest.mark.anyio
# async def test_invalid_token_content(
#     test_user: UserPublicOut,
#     secret_key: str | None,
#     jwt_audience: str,
#     exception: Type[BaseException],
# ):
#     with pytest.raises(exception):
#         access_token = auth_service.create_access_token(
#             user=test_user,
#             secret_key=secret_key,
#             audience=jwt_audience,
#             expires_in=config.access_token_expire_minutes,
#         )

#         jwt.decode(
#             access_token,
#             secret_key,
#             audience=config.jwt_audience,
#             algorithms=[config.jwt_algorithm],
#         )
