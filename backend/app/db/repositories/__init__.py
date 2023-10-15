from .cleanings import CleaningRepository
from .profiles import ProfileRepository
from .users import UserRepository

user_repo = UserRepository()  # noqa
cleaning_repo = CleaningRepository()  # noqa
profile_repo = ProfileRepository()  # noqa
