from uuid import UUID

from tortoise.transactions import atomic

from app.models import Cleaning, Offer
from app.models.cleaner_evaluation import CleanerEvaluation
from app.models.offer import OfferStatus
from app.models.schemas.cleaner_evaluation import CleanerEvaluationAggregateOut, CleanerEvaluationBase


class CleanerEvaluationRepository:
    @atomic("default")
    async def create_cleaner_evaluation(
        self, cleaning: Cleaning, evaluation_in: CleanerEvaluationBase, offer: Offer
    ) -> CleanerEvaluation:
        evaluation = await CleanerEvaluation.create(
            **evaluation_in.model_dump(), cleaning_id=cleaning.id, user_id=offer.user_id
        )

        offer.status = OfferStatus.completed
        await offer.save()
        return evaluation

    async def get_cleaner_evaluations(self) -> list[CleanerEvaluation]:
        pass

    async def get_cleaner_evaluations_by_id(self, cleaning_id: UUID) -> CleanerEvaluation:
        pass

    async def get_cleaner_evaluation_stats(self) -> CleanerEvaluationAggregateOut:
        pass
