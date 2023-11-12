import asyncio

from app.db.repositories import cleaning_repo, offer_repo
from app.models import User, Cleaning
from app.models.offer import OfferStatus
from app.models.schemas.cleaning import CleaningBase
from app.models.schemas.offer import OfferBase, OfferUpdateIn


async def new_cleaning_with_offers(user: User, users: list[User], index: int | None = None) -> Cleaning:
    cleaning_in = CleaningBase(
        name=f"cleaning with offers{f' - {index}' if index is not None else ''}",
        description=f"desc for cleaning{f' - {index}' if index is not None else ''}",
        price=float(f"{index if index is not None else ''}9.99"),
        cleaning_type=f"{'full_clean' if index is not None else 'spot_clean'}",
    )
    cleaning = await cleaning_repo.create_cleaning(cleaning_in, user)

    await asyncio.gather(
        *[
            offer_repo.create_cleaning_offer(OfferBase(cleaning_id=cleaning.id, user_id=current_user.id))
            for current_user in users
        ]
    )
    return cleaning


async def new_cleaning_with_accepted_offer(user: User, users: list[User]) -> Cleaning:
    cleaning = await new_cleaning_with_offers(user, users)
    cleaning_offers = await offer_repo.get_cleaning_offers(cleaning.id)
    offer = [offer for offer in cleaning_offers if offer.user_id == users[0].id][0]

    offer_in = OfferUpdateIn(status=OfferStatus.accepted, cleaning_id=cleaning.id, user_id=user.id)
    await offer_repo.update_cleaning_offer(offer.id, offer_in)
    return cleaning


async def new_cleanings_with_pending_offer(user: User, users: list[User]) -> list[Cleaning]:
    cleanings: tuple[Cleaning] = await asyncio.gather(
        *[new_cleaning_with_offers(user, users, index) for index in range(5)]
    )
    return list(cleanings)
