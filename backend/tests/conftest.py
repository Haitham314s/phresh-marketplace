import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.api.server import app
from app.core.config import config
from app.db.repositories.users import UserRepository
from app.models import User
from app.models.schemas.user import UserCreateIn
from app.services import auth_service

DATABASE_URL = "sqlite://test-db.sqlite"


async def init_db(create_db: bool = False, schemas: bool = False):
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.models"]}, _create_db=create_db)
    if schemas:
        await Tortoise.generate_schemas()
    if create_db:
        print(f"Database created: {DATABASE_URL}")


async def init():
    await init_db(True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8001/api",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session", autouse=True)
async def test_user():
    new_user = UserCreateIn(email="test@gmail.com", username="test", password="test123")

    user_repo = UserRepository()
    user = await user_repo.get_user_by_email(email=new_user.email)
    if user is not None:
        return user

    return await user_repo.register_new_user(new_user)


@pytest.fixture(scope="session")
async def authorized_client(client: AsyncClient, test_user: User):
    access_token = auth_service.create_access_token(test_user, config.secret_key)
    client.headers = {**client.headers, "Authorizatiion": f"{config.jwt_token_prefix} {access_token}"}
    return client
