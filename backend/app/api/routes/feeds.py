from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_user
from app.db.repositories import feed_repo
from app.models import User
from app.models.schemas.feed import CleaningFeedItem
from app.models.schemas.pagination import Pagination

router = APIRouter()


@router.get("/cleanings", response_model=list[CleaningFeedItem], dependencies=[Depends(get_current_user)])
async def get_cleaning_feeds(filters: Pagination = Depends()):
    return await feed_repo.get_cleaning_job_feeds(filters.limit, filters.page)
