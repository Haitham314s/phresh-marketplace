import pytest
from httpx import AsyncClient
from fastapi import status

from app.models import Cleaning


@pytest.mark.anyio
async def test_valid_cleaning_feed(authorized_client: AsyncClient, test_new_and_updated_cleanings: list[Cleaning]):
    cleaning_ids = [str(cleaning.id) for cleaning in test_new_and_updated_cleanings]

    res = await authorized_client.get("/feed/cleanings")
    assert res.status_code == status.HTTP_200_OK
    cleaning_feed = res.json()
    assert isinstance(cleaning_feed, list)
    assert len(cleaning_feed) == 10
    assert set(feed_item["id"] for feed_item in cleaning_feed).issubset(set(cleaning_ids))


@pytest.mark.anyio
async def test_ordered_cleaning_feeds(authorized_client: AsyncClient, test_new_and_updated_cleanings: list[Cleaning]):
    res = await authorized_client.get("/feed/cleanings")
    assert res.status_code == status.HTTP_200_OK
    cleaning_feeds = res.json()

    event_types = [feed["eventType"] for feed in cleaning_feeds]
    assert all(["is_create" == event_type for event_type in event_types])


@pytest.mark.anyio
async def test_paginated_cleaning_feeds(authorized_client: AsyncClient, test_new_and_updated_cleanings: list[Cleaning]):
    res_page1 = await authorized_client.get("/feed/cleanings")
    assert res_page1.status_code == status.HTTP_200_OK
    cleaning_feed1 = res_page1.json()
    assert len(cleaning_feed1) == 10
    ids_page1 = set(feed_item["id"] for feed_item in cleaning_feed1)

    res_page2 = await authorized_client.get("/feed/cleanings", params={"page": 1, "limit": 10})
    assert res_page2.status_code == status.HTTP_200_OK
    cleaning_feed2 = res_page2.json()
    assert len(cleaning_feed2) == 10
    ids_page2 = set(feed_item["id"] for feed_item in cleaning_feed2)

    assert ids_page1 != ids_page2
