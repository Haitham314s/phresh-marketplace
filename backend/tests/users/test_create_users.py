import pytest
from httpx import AsyncClient

from app.db.repositories.users import UserRepository
from app.models.schemas.user import UserPublicOut

test_new_user = {
    "email": "test@gmail.com",
    "username": "test_username",
    "password": "testpassword123",
}


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient):
    res = await client.get("/user")
    assert res.status_code == 404


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    user_repo = UserRepository()
    user = await user_repo.get_user_by_email(test_new_user["email"])
    assert user is None

    res = await client.post("/user", json=test_new_user)
    print(res.json())
    assert res.status_code == 201

    user = await user_repo.get_user_by_email(test_new_user["email"])
    assert user is not None
    assert user.email == test_new_user["email"]
    assert user.username == test_new_user["username"]

    created_user = UserPublicOut(**res.json())
    assert created_user == UserPublicOut.model_validate(user)


@pytest.mark.parametrize(
    "new_user, status_code",
    (
        ({"email": "test@gmail.com"}, 400),
        ({"username": "test"}, 400),
        ({"email": "invalid_email@one@two.io"}, 422),
        ({"password": "short"}, 422),
        ({"username": "shakira@#$%^<>"}, 422),
        ({"username": "ab"}, 422),
    ),
)
@pytest.mark.anyio
async def test_invalid_test_registration(
    client: AsyncClient, new_user: dict, status_code: int
):
    user_object = {
        "email": "nottaken@email.io",
        "username": "not_taken_username",
        "password": "freepassword",
    }
    for key, value in new_user.items():
        user_object[key] = value

    res = await client.post("/user", json=user_object)
    assert res.status_code == status_code
