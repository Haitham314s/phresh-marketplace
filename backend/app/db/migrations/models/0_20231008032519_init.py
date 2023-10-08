from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cleaning" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "type" VARCHAR(10) NOT NULL,
    "price" DECIMAL(10,2),
    "modified" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_cleaning_name_3a223a" ON "cleaning" ("name");
CREATE INDEX IF NOT EXISTS "idx_cleaning_type_6a3acc" ON "cleaning" ("type");
CREATE INDEX IF NOT EXISTS "idx_cleaning_price_3d89d2" ON "cleaning" ("price");
COMMENT ON COLUMN "cleaning"."type" IS 'spot_clean: spot_clean\nunclean: unclean';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
