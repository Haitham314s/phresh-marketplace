from statistics import mean
from typing import Callable

from fastapi import status
import pytest
from httpx import AsyncClient

from app.models import User, Cleaning
from app.models.schemas.cleaner_evaluation import CleanerEvaluationOut, CleanerEvaluationAggregateOut


@pytest.mark.anyio
async def test_authenticated_get_evaluation(
    create_authorized_client: Callable, test_users: list[User], test_evaluated_cleanings: list[Cleaning]
):
    authorized_client = create_authorized_client(test_users[0])
    res = await authorized_client.get(f"/evaluation/{test_evaluated_cleanings[0].id}")
    assert res.status_code == status.HTTP_200_OK

    evaluation = CleanerEvaluationOut(**res.json())
    assert evaluation.cleaning.id == test_evaluated_cleanings[0].id
    assert evaluation.cleaner.id == test_users[0].id
    assert "test headline" in evaluation.headline
    assert "test comment" in evaluation.comment

    assert 0 <= evaluation.professionalism <= 5
    assert 0 <= evaluation.completeness <= 5
    assert 0 <= evaluation.efficiency <= 5
    assert 0 <= evaluation.overall_rating <= 5


@pytest.mark.anyio
async def test_get_cleaner_evaluations(
    create_authorized_client: Callable, test_users: list[User], test_evaluated_cleanings: list[Cleaning]
):
    user = test_users[0]
    authorized_client = create_authorized_client(user)
    res = await authorized_client.get("/evaluations", params={"cleaner_id": user.id})
    assert res.status_code == status.HTTP_200_OK
    evaluations = [CleanerEvaluationOut(**evaluation) for evaluation in res.json()]
    assert len(evaluations) > 1

    for evaluation in evaluations:
        assert evaluation.cleaner.id == user.id
        assert evaluation.overall_rating >= 0


@pytest.mark.anyio
async def test_get_aggregate_cleaner_stats(
    create_authorized_client: Callable, test_users: list[User], test_evaluated_cleanings: list[Cleaning]
):
    authorized_client: AsyncClient = create_authorized_client(test_users[1])
    res = await authorized_client.get("/evaluations", params={"cleaner_id": test_users[0].id})
    assert res.status_code == status.HTTP_200_OK
    evaluations = [CleanerEvaluationOut(**evaluation) for evaluation in res.json()]

    res = await authorized_client.get("/evaluation/stats", params={"cleaner_id": test_users[0].id})
    assert res.status_code == status.HTTP_200_OK
    stats = CleanerEvaluationAggregateOut(**res.json())

    assert len(evaluations) == stats.total_evaluations
    assert max([e.overall_rating for e in evaluations]) == stats.max_overall_rating
    assert min([e.overall_rating for e in evaluations]) == stats.min_overall_rating
    assert round(mean([e.overall_rating for e in evaluations]), 2) == stats.avg_overall_rating
    assert (
        round(mean([e.professionalism for e in evaluations if e.professionalism is not None]))
        == stats.avg_professionalism
    )
    assert round(mean([e.completeness for e in evaluations if e.completeness is not None])) == stats.avg_completeness
    assert round(mean([e.efficiency for e in evaluations if e.efficiency is not None])) == stats.avg_efficiency
    assert len([e for e in evaluations if e.overall_rating == 1]) == stats.one_stars
    assert len([e for e in evaluations if e.overall_rating == 2]) == stats.two_stars
    assert len([e for e in evaluations if e.overall_rating == 3]) == stats.three_stars
    assert len([e for e in evaluations if e.overall_rating == 4]) == stats.four_stars
    assert len([e for e in evaluations if e.overall_rating == 5]) == stats.five_stars


@pytest.mark.anyio
async def test_unauthenticated_user_get_evaluations(
    client: AsyncClient, test_users: list[User], test_evaluated_cleanings: list[Cleaning]
):
    res = await client.get(f"/evaluation/{test_evaluated_cleanings[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    res = await client.get("/evaluations", params={"cleaner_id": test_users[0].id})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
