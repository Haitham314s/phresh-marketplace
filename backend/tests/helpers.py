from app.db.repositories import user_repo
from app.models import User
from app.models.schemas.user import UserCreateIn


async def user_fixture_helper(user_in: UserCreateIn) -> User:
    user = await user_repo.get_user_by_email(user_in.email)
    return user if user is not None else await user_repo.register_new_user(user_in)
