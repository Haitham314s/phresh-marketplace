import asyncio
from typing import Callable

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.api.server import app
from app.core.config import config
from app.db.repositories import user_repo
from app.models import User
from app.models.schemas.user import UserCreateIn
from app.services import auth_service
from .helpers import user_fixture_helper

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
    user_in = UserCreateIn(email="test@gmail.com", username="test", password="test123456")
    return await user_fixture_helper(user_in)


@pytest.fixture(scope="session")
async def test_user2():
    user_in = UserCreateIn(email="test2@gmail.com", username="test2", password="test123456")
    return await user_fixture_helper(user_in)


@pytest.fixture(scope="session")
async def test_users():
    return await asyncio.gather(
        *[
            user_fixture_helper(
                UserCreateIn(email=f"test{index}@gmail.com", username=f"test{index}", password="test123456")
            )
            for index in range(3, 7)
        ]
    )


@pytest.fixture(scope="session")
async def authorized_client(client: AsyncClient, test_user: User):
    access_token = auth_service.create_access_token(test_user, config.secret_key)
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8001/api",
        headers={**client.headers, "Authorization": f"{config.jwt_token_prefix} {access_token}"},
    ) as authorized_client:
        yield authorized_client


@pytest.fixture(scope="session")
def create_authorized_client(client: AsyncClient) -> Callable:
    def _create_authorized_client(user: User) -> AsyncClient:
        access_token = auth_service.create_access_token(user, config.secret_key)
        async with AsyncClient(
            app=app,
            base_url="http://localhost:8001/api",
            headers={**client.headers, "Authorization": f"{config.jwt_token_prefix} {access_token}"},
        ) as authorized_client:
            yield authorized_client

    return _create_authorized_client
