from app.db.repositories import cleaning_repo
from app.models import User
from app.models.cleaning import CleaningType, Cleaning
from app.models.schemas.cleaning import CleaningBase, CleaningOut


async def get_or_create_cleaning(user: User) -> Cleaning:
    cleaning = await cleaning_repo.get_all_cleanings(user)
    if len(cleaning):
        return cleaning[0]

    cleaning = CleaningBase(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        type=CleaningType.spot_clean,
    )

    return await cleaning_repo.create_cleaning(cleaning, user)


async def new_cleaning(user: User) -> Cleaning:
    cleaning = CleaningBase(
        name="test cleaning",
        description="test description",
        price=10.00,
        type=CleaningType.spot_clean,
    )

    return await cleaning_repo.create_cleaning(cleaning, user)


async def new_cleaning_list(user: User, limit: 5) -> list[CleaningOut]:
    return [
        CleaningOut.model_validate(
            cleaning_repo.create_cleaning(
                CleaningBase(
                    name=f"test cleaning {i}",
                    description=f"test description {i}",
                    price=10.00,
                    type=CleaningType.full_clean,
                ),
                user,
            )
        )
        for i in range(limit)
    ]
