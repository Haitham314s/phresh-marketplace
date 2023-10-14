from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.models import User
from app.models.schemas.token import AccessToken
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(f"{config.api_prefix}/auth/token")


async def get_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        user = await auth_service.get_user_from_token(token, config.secret_key)
    except HTTPException as e:
        raise e

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


def get_current_user(current_user: User = Depends(get_user)) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no authenticated user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not an active user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
