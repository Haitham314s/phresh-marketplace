from .cleanings import CleaningRepository
from .offers import OfferRepository
from .profiles import ProfileRepository
from .users import UserRepository

user_repo = UserRepository()  # noqa
cleaning_repo = CleaningRepository()  # noqa
profile_repo = ProfileRepository()  # noqa
offer_repo = OfferRepository()  # noqa
