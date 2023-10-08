from app.db.repositories.cleanings import CleaningRepository
from app.models.schemas.cleaning import CleaningBase, CleaningOut


async def create_cleaning_info() -> CleaningOut:
    cleaning_repo = CleaningRepository()
    cleaning = await cleaning_repo.get_all_cleanings()
    if len(cleaning):
        return CleaningOut.model_validate(cleaning[0])

    cleaning = CleaningBase(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )

    return await cleaning_repo.create_cleaning(cleaning)
