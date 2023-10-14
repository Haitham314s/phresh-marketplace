from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.repositories import user_repo
from app.models.schemas.token import AccessToken
from app.services import auth_service

router = APIRouter()


@router.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)) -> AccessToken:
    user = await user_repo.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AccessToken(access_token=auth_service.create_access_token(user), token_type="bearer")
