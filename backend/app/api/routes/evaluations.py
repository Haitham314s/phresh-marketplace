from uuid import UUID

from fastapi import Depends, status, APIRouter, Query

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.cleanings import get_cleaning_by_id
from app.api.dependencies.evaluations import (
    check_create_evaluation_permission,
    check_get_cleaning_evaluation_permission,
)
from app.db.repositories import eval_repo
from app.models import Offer, Cleaning, CleanerEvaluation
from app.models.schemas.cleaner_evaluation import (
    CleanerEvaluationBase,
    CleanerEvaluationOut,
    CleanerEvaluationAggregateOut,
)

router = APIRouter()


@router.post("/{cleaning_id}", status_code=status.HTTP_201_CREATED, response_model=CleanerEvaluationOut)
async def create_cleaner_evaluation(
    evaluation_in: CleanerEvaluationBase,
    cleaning: Cleaning = Depends(get_cleaning_by_id),
    offer: Offer = Depends(check_create_evaluation_permission),
):
    evaluation = await eval_repo.create_cleaner_evaluation(cleaning, evaluation_in, offer)
    return CleanerEvaluationOut.model_validate(evaluation)


@router.get("s", response_model=list[CleanerEvaluationOut], dependencies=[Depends(get_current_user)])
async def get_cleaner_evaluations(cleaner_id: UUID = Query()):
    evaluations = await eval_repo.get_cleaner_evaluations(cleaner_id)
    return [CleanerEvaluationOut.model_validate(evaluation) for evaluation in evaluations]


@router.get("/stats", response_model=CleanerEvaluationAggregateOut, dependencies=[Depends(get_current_user)])
async def get_cleaner_stats(cleaner_id: UUID = Query()):
    return await eval_repo.get_cleaner_evaluation_stats(cleaner_id)


@router.get("/{cleaning_id}", response_model=CleanerEvaluationOut)
async def get_cleaner_evaluation_from_id(
    evaluation: CleanerEvaluation = Depends(check_get_cleaning_evaluation_permission),
):
    return CleanerEvaluationOut.model_validate(evaluation)
