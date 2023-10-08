from typing import List
from uuid import UUID

from fastapi import HTTPException, status

from app.models.cleaning import Cleaning
from app.models.schemas.cleaning import CleaningBase, CleaningOut


class CleaningRepository:
    async def get_cleanings(self) -> List[CleaningOut]:
        return await Cleaning.all()

    async def get_cleaning(self, cleaning_id: UUID) -> CleaningOut | None:
        cleaning = await Cleaning.get_or_none(id=cleaning_id)
        if cleaning is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cleaning object not found",
            )

        return cleaning

    async def create_cleaning(self, new_cleaning: CleaningBase) -> CleaningOut:
        cleaning = await Cleaning.create(**new_cleaning.model_dump())
        return CleaningOut.model_validate(cleaning)

    async def delete_cleaning(self, cleaning_id: UUID):
        cleaning = await Cleaning.get_or_none(id=cleaning_id)
        if cleaning is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cleaning object not found",
            )

        await cleaning.delete()
