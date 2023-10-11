from functools import lru_cache
from uuid import uuid4

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.api.server import app
from app.db.repositories.users import UserRepository
from app.models.schemas.user import UserCreateIn

DATABASE_URL = "sqlite://test-db.sqlite"


async def init_db(create_db: bool = False, schemas: bool = False):
    await Tortoise.init(
        db_url=DATABASE_URL, modules={"models": ["app.models"]}, _create_db=create_db
    )
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
