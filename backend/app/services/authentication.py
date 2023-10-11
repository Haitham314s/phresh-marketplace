import bcrypt
from passlib.context import CryptContext

from app.models.schemas.user import UserPasswordOut

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

    def verify_password(password: str, salt: str, hashed_password: str) -> bool:
        return pwd_context.verify(password + salt, hashed_password)
