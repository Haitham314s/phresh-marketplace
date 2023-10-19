from typing import Callable

import pytest
from fastapi import status

from app.models import User
from app.models.schemas.offer import OfferBase
from tests.shared.offers import new_cleaning_offer


@pytest.mark.anyio
async def test_get_cleaning_offer(create_authorized_client: Callable, test_user2: User, test_users: list[User]):
    authorized_client = create_authorized_client(test_user2)
    cleaning = await new_cleaning_offer(test_user2, test_users)

    res = await authorized_client.get(f"/cleaning/{cleaning.id}/offers")
    offers = [OfferBase(**offer) for offer in res.json()]
    assert res.status_code == status.HTTP_200_OK

    user_ids = [user.id for user in test_users]
    for offer in offers:
        assert offer.user_id in user_ids
