from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import config
from app.models.schemas.token import JWTCreds, JWTMeta, JWTPayload
from app.models.schemas.user import UserPasswordOut
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on
    """

    pass


class AuthService:
    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def create_salt_and_hashed_password(self, password: str) -> UserPasswordOut:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password, salt=salt)
        return UserPasswordOut(salt=salt, password=hashed_password)

    def verify_password(self, password: str, salt: str, hashed_password: str) -> bool:
        return pwd_context.verify(f"{password}{salt}", hashed_password)

    def create_access_token(
        self,
        user: User | None,
        secret_key: str = config.secret_key,
        audience: str = config.jwt_audience,
        expires_in: int = config.access_token_expire_minutes,
    ) -> str:
        if user is None or not isinstance(user, User):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )

        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(**jwt_meta.model_dump(), **jwt_creds.model_dump())

        return jwt.encode(token_payload.model_dump(), secret_key, algorithm=config.jwt_algorithm)

    async def get_user_from_token(self, token: str, secret_key: str):
        try:
            decoded_token = jwt.decode(
                token, secret_key, audience=config.jwt_audience, algorithms=[config.jwt_algorithm]
            )
            payload = JWTPayload(**decoded_token)
            return await User.get_or_none(username=payload.username)
        except (ValidationError, JWTError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
