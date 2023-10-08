from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cleaning" RENAME COLUMN "modified" TO "modified_at";
        ALTER TABLE "cleaning" RENAME COLUMN "created" TO "created_at";
        ALTER TABLE "cleaning" ALTER COLUMN "type" SET DEFAULT 'spot_clean';
        ALTER TABLE "cleaning" ALTER COLUMN "type" TYPE VARCHAR(10) USING "type"::VARCHAR(10);
        ALTER TABLE "cleaning" ALTER COLUMN "price" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cleaning" RENAME COLUMN "modified_at" TO "modified";
        ALTER TABLE "cleaning" RENAME COLUMN "created_at" TO "created";
        ALTER TABLE "cleaning" ALTER COLUMN "type" DROP DEFAULT;
        ALTER TABLE "cleaning" ALTER COLUMN "type" TYPE VARCHAR(10) USING "type"::VARCHAR(10);
        ALTER TABLE "cleaning" ALTER COLUMN "price" DROP NOT NULL;"""
