import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.repositories import user_repo
from app.models.schemas.user import UserPublicOut
from app.services import auth_service

faker = Faker()
Faker.seed(0)


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient):
    client.headers = {**client.headers, "content-type": "application/json"}
    res = await client.get("/auth/user")
    assert res.status_code == 401


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    fake_profile: dict = faker.profile()
    new_user = {
        "email": fake_profile["mail"],
        "username": fake_profile["username"],
        "password": f"{fake_profile['username']}123456",
    }

    user = await user_repo.get_user_by_email(new_user["email"])
    assert user is None

    res = await client.post("/auth/user", json=new_user)
    assert res.status_code == 201

    user = await user_repo.get_user_by_email(new_user["email"], populate=False)
    assert user is not None
    assert user.email == new_user["email"]
    assert user.username == new_user["username"]

    created_user = UserPublicOut(**res.json()).model_dump(exclude={"access_token", "profile"})
    assert created_user == UserPublicOut.model_validate(user).model_dump(exclude={"access_token", "profile"})


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
async def test_invalid_user_registration(client: AsyncClient, new_user: dict, status_code: int):
    user_object = {
        "email": "nottaken@email.io",
        "username": "not_taken_username",
        "password": "freepassword",
    }
    for key, value in new_user.items():
        user_object[key] = value

    res = await client.post("/auth/user", json=user_object)
    assert res.status_code == status_code


@pytest.mark.anyio
async def test_user_password_registration(client: AsyncClient):
    fake_profile: dict = faker.profile()
    new_user = {
        "email": fake_profile["mail"],
        "username": fake_profile["username"],
        "password": f"{fake_profile['username']}123",
    }

    res = await client.post("/auth/user", json=new_user)
    assert res.status_code == 201

    user = await user_repo.get_user_by_email(email=new_user["email"], populate=False)
    assert user is not None
    assert user.salt is not None and user.salt != "123"
    assert user.hashed_password != new_user["password"]
    assert auth_service.verify_password(
        password=str(new_user["password"]),
        salt=user.salt,
        hashed_password=user.hashed_password,
    )
