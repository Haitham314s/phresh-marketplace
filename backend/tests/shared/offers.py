import asyncio

from app.db.repositories import cleaning_repo, offer_repo
from app.models import User, Cleaning
from app.models.schemas.cleaning import CleaningBase
from app.models.schemas.offer import OfferBase


async def new_cleaning_offer(user: User, users: list[User]) -> Cleaning:
    cleaning_in = CleaningBase(
        name="cleaning with offers",
        description="desc for cleaning",
        price=9.99,
        cleaning_type="full_clean",
    )
    cleaning = await cleaning_repo.create_cleaning(cleaning_in, user)

    await asyncio.gather(
        *[
            offer_repo.create_cleaning_offer(OfferBase(cleaning_id=cleaning.id, user_id=current_user.id))
            for current_user in users
        ]
    )
    return cleaning
