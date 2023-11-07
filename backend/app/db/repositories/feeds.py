from tortoise import connections

from app.db.repositories.users import UserRepository
from app.models.schemas.feed import CleaningFeedItem


class FeedRepository:
    def __init__(self) -> None:
        self.user_repo = UserRepository()

    async def get_cleaning_job_feeds(
        self, limit: int = 10, page: int = 0, populate: bool = True
    ) -> list[CleaningFeedItem]:
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
        users = {}
        cleaning_feeds = []
        for cleaning_feed in results:
            if cleaning_feed["user_id"] not in users:
                users[cleaning_feed["user_id"]] = await self.user_repo.get_user_by_id(cleaning_feed["user_id"])

            cleaning_dict = dict(cleaning_feed)
            cleaning_dict |= {"user": users[cleaning_feed["user_id"]]}
            cleaning_feeds.append(CleaningFeedItem(**cleaning_dict))

        return cleaning_feeds
