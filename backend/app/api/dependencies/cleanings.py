from uuid import UUID

from fastapi import Depends

from app.api.dependencies.auth import get_current_user
from app.db.repositories import cleaning_repo
from app.models import User


async def get_cleaning_by_id(cleaning_id: UUID, user: User = Depends(get_current_user)):
    return await cleaning_repo.get_cleaning_by_id(cleaning_id)
