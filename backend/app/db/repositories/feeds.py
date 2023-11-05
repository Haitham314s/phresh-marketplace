from tortoise import connections

from app.models.schemas.feed import CleaningFeedItem


class FeedRepository:
    async def get_cleaning_job_feeds(self, limit: int = 10, page: int = 0) -> list[CleaningFeedItem]:
        conn = connections.get("default")
        # greatest_func = "GREATEST"
        greatest_func = "MAX"

        cleaning_query = (
            "SELECT id, name, description, price, type, user_id, created_at, modified_at, "
            "CASE WHEN created_at = modified_at THEN 'is_create' ELSE 'is_update' END AS event_type, "
            f"{greatest_func}(created_at, modified_at) AS event_timestamp, "
            f"ROW_NUMBER() OVER (ORDER BY {greatest_func}(created_at, modified_at) DESC) AS row_number "
            f"FROM cleaning ORDER BY {greatest_func}(created_at, modified_at) DESC LIMIT {limit} OFFSET {page * limit};"
        )

        _, results = await conn.execute_query(cleaning_query)
        return [CleaningFeedItem(**dict(cleaning)) for cleaning in results]
