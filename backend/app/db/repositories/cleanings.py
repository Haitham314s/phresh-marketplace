from app.models.cleaning import Cleaning
from app.models.schemas.cleaning import CleaningBase, CleaningOut


class CleaningRepository:
    async def create_cleaning(self, new_cleaning: CleaningBase) -> CleaningOut:
        cleaning = await Cleaning.create(**new_cleaning.model_dump())
        return CleaningOut.model_validate(cleaning)
