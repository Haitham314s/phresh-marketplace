from statistics import mean

from pydantic import conint, confloat, model_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.cleaner_evaluation import CleanerEvaluation
from app.models.schemas.cleaning import CleaningOut
from app.models.schemas.core import CoreModel
from app.models.schemas.user import UserPublicOut

CleanerEvaluationGenOut = pydantic_model_creator(CleanerEvaluation, exclude=("modified_at", "created_at"))


class CleanerEvaluationBase(CoreModel):
    hidden: bool | None = None
    headline: str | None = None
    comment: str | None = None
    professionalism: conint(ge=0, le=5)
    completeness: conint(ge=0, le=5)
    efficiency: conint(ge=0, le=5)
    overall_rating: confloat(ge=0, le=5) | None = None

    @model_validator(mode="after")
    def calculate_overall_rating(self) -> "CleanerEvaluationBase":
        if self.overall_rating is not None:
            return self

        self.overall_rating = round(mean([self.professionalism, self.completeness, self.efficiency]), 2)
        return self


class CleanerEvaluationOut(CleanerEvaluationGenOut, CoreModel):
    overall_rating: float
    cleaner: UserPublicOut | None = None
    cleaning: CleaningOut | None = None


class CleanerEvaluationAggregateOut(CoreModel):
    avg_professionalism: confloat(ge=0, le=5)
    avg_completeness: confloat(ge=0, le=5)
    avg_efficiency: confloat(ge=0, le=5)
    avg_overall_rating: confloat(ge=0, le=5)
    max_overall_rating: confloat(ge=0, le=5)
    min_overall_rating: confloat(ge=0, le=5)
    one_stars: conint(ge=0)
    two_stars: conint(ge=0)
    three_stars: conint(ge=0)
    four_stars: conint(ge=0)
    five_stars: conint(ge=0)
    total_evaluations: conint(ge=0)
    total_hidden: conint(ge=0)
