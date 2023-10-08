import logging

from tortoise import Tortoise

from app.core.config import DATABASE_URL

logger = logging.getLogger(__name__)


async def connect_to_db() -> None:
    try:
        await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.models"]})
        await Tortoise.generate_schemas()
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection():
    try:
        await Tortoise.close_connections()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")
