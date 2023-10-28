from fastapi import Depends

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.db.repositories import offer_repo, eval_repo
from app.models import Cleaning, Offer, User, CleanerEvaluation
from .auth import get_current_user
from .cleanings import get_cleaning_by_id
from .offers import check_get_offer_permission
from ...models.offer import OfferStatus


async def check_create_evaluation_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)
) -> Offer:
    offers = await offer_repo.get_cleaning_offers(cleaning.id)
    offer_statuses = [offer.status for offer in offers]

    if cleaning.user_id != user.id:
        raise APIException(ErrorCode.evaluation_unauthorized_access)
    if OfferStatus.completed in offer_statuses:
        raise APIException(ErrorCode.evaluation_already_created)
    if OfferStatus.accepted not in offer_statuses:
        raise APIException(ErrorCode.offer_has_wrong_status)

    return [offer for offer in offers if offer.status == OfferStatus.accepted][0]


async def check_get_cleaning_evaluation_permission(
    cleaning: Cleaning = Depends(get_cleaning_by_id), user: User = Depends(get_current_user)
) -> CleanerEvaluation:
    evaluation = await eval_repo.get_cleaner_evaluation_by_id(cleaning.id)
    if user.id not in [evaluation.cleaner.id, evaluation.cleaning.user_id]:
        raise APIException(ErrorCode.evaluation_unauthorized_access)

    return evaluation
