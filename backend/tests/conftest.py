import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from app.api.server import app

# from app.core.config import DATABASE_URL

DATABASE_URL = "sqlite://test-db.sqlite"


async def init_db(create_db: bool = False, schemas: bool = False):
    await Tortoise.init(
        db_url=DATABASE_URL, modules={"models": ["app.models"]}, _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()
    if create_db:
        print(f"database created: {DATABASE_URL}")


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
