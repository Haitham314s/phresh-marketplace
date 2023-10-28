from uuid import UUID

from tortoise.expressions import Q
from tortoise.functions import Avg, Min, Max, Count, Sum
from tortoise.transactions import atomic

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models import Cleaning, Offer
from app.models.cleaner_evaluation import CleanerEvaluation
from app.models.offer import OfferStatus
from app.models.schemas.cleaner_evaluation import CleanerEvaluationAggregateOut, CleanerEvaluationBase


class CleanerEvaluationRepository:
    @atomic("default")
    async def create_cleaner_evaluation(
        self, cleaning: Cleaning, evaluation_in: CleanerEvaluationBase, offer: Offer, populate: bool = True
    ) -> CleanerEvaluation:
        evaluation = await CleanerEvaluation.create(
            **evaluation_in.model_dump(), cleaning_id=cleaning.id, cleaner_id=offer.user_id
        )
        if populate:
            await evaluation.fetch_related("cleaning", "cleaner")

        offer.status = OfferStatus.completed
        await offer.save()
        return evaluation

    async def get_cleaner_evaluations(self, cleaner_id: UUID) -> list[CleanerEvaluation]:
        return await CleanerEvaluation.filter(hidden=False, cleaner_id=cleaner_id).prefetch_related(
            "cleaning", "cleaner"
        )

    async def get_cleaner_evaluation_by_id(self, cleaning_id: UUID, populate: bool = True) -> CleanerEvaluation:
        evaluation = await CleanerEvaluation.get_or_none(hidden=False, cleaning_id=cleaning_id)
        if evaluation is None:
            raise APIException(ErrorCode.evaluation_not_found)
        if populate:
            await evaluation.fetch_related("cleaning", "cleaner")

        return evaluation

    async def get_cleaner_evaluation_stats(self, cleaner_id: UUID) -> CleanerEvaluationAggregateOut:
        evaluation_result = (
            await CleanerEvaluation.filter(hidden=False, cleaner_id=cleaner_id)
            .annotate(
                avg_professionalism=Avg("professionalism"),
                avg_completeness=Avg("completeness"),
                avg_efficiency=Avg("efficiency"),
                avg_overall_rating=Avg("overall_rating"),
                min_overall_rating=Min("overall_rating"),
                max_overall_rating=Max("overall_rating"),
                total_evaluations=Count("cleaning_id"),
                total_hidden=Sum("hidden"),
                one_stars=Count("overall_rating", _filter=Q(overall_rating=1)),
                two_stars=Count("overall_rating", _filter=Q(overall_rating=2)),
                three_stars=Count("overall_rating", _filter=Q(overall_rating=3)),
                four_stars=Count("overall_rating", _filter=Q(overall_rating=4)),
                five_stars=Count("overall_rating", _filter=Q(overall_rating=5)),
            )
            .first()
            .values(
                "avg_professionalism",
                "avg_completeness",
                "avg_efficiency",
                "avg_overall_rating",
                "min_overall_rating",
                "max_overall_rating",
                "total_evaluations",
                "total_hidden",
                "one_stars",
                "two_stars",
                "three_stars",
                "four_stars",
                "five_stars",
            )
        )

        return CleanerEvaluationAggregateOut(**dict(evaluation_result))
