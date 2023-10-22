from typing import Callable, Any

import pytest
from fastapi import status

from app.db.repositories import offer_repo
from app.models import User
from app.models.offer import OfferStatus
from app.models.schemas.cleaner_evaluation import CleanerEvaluationBase, CleanerEvaluationOut
from tests.shared.offers import new_cleaning_with_accepted_offer


def get_evaluation_in(rating: int) -> dict[str, Any]:
    return CleanerEvaluationBase(
        hidden=False, professionalism=rating, completeness=rating, efficiency=rating
    ).model_dump()


@pytest.mark.anyio
async def test_create_successful_evaluation(
    create_authorized_client: Callable, test_user2: User, test_users: list[User]
):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_accepted_offer(test_user2, test_users)
    offer = [
        offer for offer in await offer_repo.get_cleaning_offers(cleaning.id) if offer.status == OfferStatus.accepted
    ][0]
    evaluation_in = CleanerEvaluationBase(
        hidden=False,
        headline="Excellent job",
        comment=f"""
Really appreciated the hard work and effort they put into this job!
Though the cleaner took their time, I would definitely hire them again for the quality of their work.
            """,
        professionalism=5,
        completeness=5,
        efficiency=4,
    )

    res = await authorized_client.post(f"/evaluation/{cleaning.id}", json=evaluation_in.model_dump())
    assert res.status_code == status.HTTP_201_CREATED

    evaluation = CleanerEvaluationOut(**res.json())
    assert evaluation.hidden == evaluation_in.hidden
    assert evaluation.headline == evaluation_in.headline
    assert evaluation.overall_rating == evaluation_in.overall_rating

    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offer/{offer.id}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == OfferStatus.completed


@pytest.mark.anyio
async def test_unauthorized_user_create_evaluation(
    create_authorized_client: Callable, test_user: User, test_users: list[User]
):
    user = test_users[1]
    cleaning = await new_cleaning_with_accepted_offer(test_user, test_users)
    authorized_client = create_authorized_client(user)

    evaluation_in = get_evaluation_in(2)
    res = await authorized_client.post(f"/evaluation/{cleaning.id}", json=evaluation_in)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_evaluation_for_wrong_user(
    create_authorized_client: Callable, test_user: User, test_user2: User, test_users: list[User]
):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_accepted_offer(test_user, test_users)

    evaluation_in = get_evaluation_in(1)
    res = await authorized_client.post(f"/evaluation/{cleaning.id}", json=evaluation_in)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_multiple_reviews(create_authorized_client: Callable, test_user2: User, test_users: list[User]):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_with_accepted_offer(test_user2, test_users)

    evaluation_in = get_evaluation_in(3)
    res = await authorized_client.post(f"/evaluation/{cleaning.id}", json=evaluation_in)
    assert res.status_code == status.HTTP_201_CREATED

    evaluation_in = get_evaluation_in(1)
    res = await authorized_client.post(f"/evaluation/{cleaning.id}", json=evaluation_in)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
