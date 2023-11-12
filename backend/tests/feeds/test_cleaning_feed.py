from collections import Counter

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
    assert all(["is_create" == event_type for event_type in event_types[1:]])


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


@pytest.mark.anyio
async def test_correct_paginated_cleaning_feed(
    authorized_client: AsyncClient, test_new_and_updated_cleanings: list[Cleaning]
):
    limit = 10
    combos = []
    for page in range(5):
        res = await authorized_client.get("/feed/cleanings", params={"page": page, "limit": limit})
        assert res.status_code == status.HTTP_200_OK
        page_json = res.json()
        assert len(page_json) == limit
        id_and_event = set(f"{item['id']}-{item['eventType']}" for item in page_json)
        combos.append(id_and_event)

    id_combo_len = sum(len(combo) for combo in combos)
    assert id_combo_len == len(set().union(*combos))


@pytest.mark.anyio
async def test_created_and_updated_cleaning_feed(
    authorized_client: AsyncClient, test_new_and_updated_cleanings: list[Cleaning]
):
    res_page1 = await authorized_client.get("/feed/cleanings", params={"limit": 30})
    assert res_page1.status_code == status.HTTP_200_OK
    ids_page1 = [feed_item["id"] for feed_item in res_page1.json()]

    res_page2 = await authorized_client.get("/feed/cleanings", params={"limit": 30, "page": 1})
    assert res_page2.status_code == status.HTTP_200_OK
    ids_page2 = [feed_item["id"] for feed_item in res_page2.json()]

    id_counts = Counter(ids_page1 + ids_page2)
    assert len([feed_id for feed_id, cnt in id_counts.items() if cnt > 1]) == 0
