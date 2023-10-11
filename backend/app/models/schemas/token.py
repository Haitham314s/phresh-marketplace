from datetime import datetime, timedelta

from pydantic import EmailStr

from app.core.config import config
from app.models.schemas.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "phresh.io"
    aud: str = config.jwt_audience
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=config.access_token_expire_minutes)
    )


class JWTCreds(CoreModel):
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str
