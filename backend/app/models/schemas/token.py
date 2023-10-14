from datetime import datetime, timedelta

from pydantic import EmailStr, BaseModel

from app.core.config import config


class JWTMeta(BaseModel):
    iss: str = "phresh.io"
    aud: str = config.jwt_audience
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=config.access_token_expire_minutes))


class JWTCreds(BaseModel):
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    pass


class AccessToken(BaseModel):
    access_token: str
    token_type: str
