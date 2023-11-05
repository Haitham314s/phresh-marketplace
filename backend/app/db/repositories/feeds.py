from tortoise import connections

from app.models.schemas.feed import CleaningFeedItem


class FeedRepository:
    async def get_cleaning_job_feeds(self, limit: int = 10, page: int = 0) -> list[CleaningFeedItem]:
        conn = connections.get("default")
        cleaning_query = (
            "SELECT id, name, description, price, type, user_id, created_at, modified_at, 'is_create' AS event_type, "
            "created_at AS event_timestamp, ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_number "
            f"FROM cleaning ORDER BY created_at DESC LIMIT {limit} OFFSET {page * limit}; "
        )

        _, results = await conn.execute_query(cleaning_query)
        return [CleaningFeedItem(**dict(cleaning)) for cleaning in results]
