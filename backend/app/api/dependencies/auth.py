from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models import User
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(f"{config.api_prefix}/auth/token")


async def get_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        user = await auth_service.get_user_from_token(token, config.secret_key)
    except APIException as e:
        raise e

    if user is None:
        raise APIException(ErrorCode.user_not_found)
    return user


def get_current_user(current_user: User = Depends(get_user)) -> User:
    if current_user is None:
        raise APIException(ErrorCode.user_not_found, {"WWW-Authenticate": "Bearer"})
    if not current_user.is_active:
        raise APIException(ErrorCode.user_not_active, {"WWW-Authenticate": "Bearer"})
    return current_user
