import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.repositories.users import UserRepository
from app.models.schemas.user import UserPublicOut
from app.services import auth_service

faker = Faker()
Faker.seed(0)


@pytest.mark.anyio
async def test_routes_exist(client: AsyncClient):
    res = await client.get("/user")
    assert res.status_code == 405


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    user_repo = UserRepository()
    fake_profile: dict = faker.profile()
    new_user = {
        "email": fake_profile["mail"],
        "username": fake_profile["username"],
        "password": f"{fake_profile['username']}123",
    }

    user_repo = UserRepository()
    user = await user_repo.get_user_by_email(new_user["email"])
    assert user is None

    res = await client.post("/user", json=new_user)
    assert res.status_code == 201

    user = await user_repo.get_user_by_email(new_user["email"])
    assert user is not None
    assert user.email == new_user["email"]
    assert user.username == new_user["username"]

    created_user = UserPublicOut(**res.json())
    assert created_user == UserPublicOut.model_validate(user)


@pytest.mark.parametrize(
    "new_user, status_code",
    (
        ({"email": "testnewuser@gmail.com"}, 400),
        ({"username": "test_new_username"}, 400),
        ({"email": "invalid_email@one@two.io"}, 422),
        ({"password": "short"}, 422),
        ({"username": "shakira@#$%^<>"}, 422),
        ({"username": "ab"}, 422),
    ),
)
@pytest.mark.anyio
async def test_invalid_user_registration(
    client: AsyncClient, new_user: dict, status_code: int
):
    user_object = {
        "email": "nottaken@email.io",
        "username": "not_taken_username",
        "password": "freepassword",
    }
    for key, value in new_user.items():
        user_object[key] = value

    print(f"USER_OBJECT: {user_object}")
    res = await client.post("/user", json=user_object)
    assert res.status_code == status_code


@pytest.mark.anyio
async def test_user_password_registration(client: AsyncClient):
    user_repo = UserRepository()
    fake_profile: dict = faker.profile()
    new_user = {
        "email": fake_profile["mail"],
        "username": fake_profile["username"],
        "password": f"{fake_profile['username']}123",
    }

    res = await client.post("/user", json=new_user)
    assert res.status_code == 201

    user = await user_repo.get_user_by_email(email=new_user["email"])
    assert user is not None
    assert user.salt is not None and user.salt != "123"
    assert user.password != new_user["password"]
    assert auth_service.verify_password(
        password=new_user["password"],
        salt=user.salt,
        hashed_pw=user.password,
    )
