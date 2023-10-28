import asyncio
from random import randint

from app.db.repositories import cleaning_repo, offer_repo, eval_repo
from app.models import User, Cleaning
from app.models.cleaning import CleaningType
from app.models.offer import OfferStatus
from app.models.schemas.cleaner_evaluation import CleanerEvaluationBase
from app.models.schemas.cleaning import CleaningBase
from app.models.schemas.offer import OfferBase, OfferUpdateIn


async def create_cleaning_with_evaluation_helper(
    cleaning_in: CleaningBase, evaluation_in: CleanerEvaluationBase, user: User, cleaner: User
) -> Cleaning:
    cleaning = await cleaning_repo.create_cleaning(cleaning_in, user)
    offer = await offer_repo.create_cleaning_offer(OfferBase(cleaning_id=cleaning.id, user_id=cleaner.id))
    await offer_repo.update_cleaning_offer(
        offer.id, OfferUpdateIn(user_id=user.id, cleaning_id=cleaning.id, status=OfferStatus.accepted)
    )
    await eval_repo.create_cleaner_evaluation(cleaning, evaluation_in, offer)
    return cleaning


def generate_cleaning_in(index: int) -> CleaningBase:
    return CleaningBase(
        name=f"test cleaning - {index}",
        description=f"test description - {index}",
        price=float(f"{index}9.99"),
        type=CleaningType.full_clean,
    )


def generate_evaluation_in(index: int) -> CleanerEvaluationBase:
    return CleanerEvaluationBase(
        hidden=False,
        headline=f"test headline - {index}",
        comment=f"test comment - {index}",
        professionalism=randint(0, 5),
        completeness=randint(0, 5),
        efficiency=randint(0, 5),
    )


async def new_evaluated_cleaning_list(user: User, cleaner: User) -> tuple[Cleaning]:
    return await asyncio.gather(
        *[
            create_cleaning_with_evaluation_helper(
                generate_cleaning_in(index), generate_evaluation_in(index), user, cleaner
            )
            for index in range(5)
        ]
    )
