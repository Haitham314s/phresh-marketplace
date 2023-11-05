from .cleaner_evaluations import CleanerEvaluationRepository
from .cleanings import CleaningRepository
from .feeds import FeedRepository
from .offers import OfferRepository
from .profiles import ProfileRepository
from .users import UserRepository

user_repo = UserRepository()  # noqa
cleaning_repo = CleaningRepository()  # noqa
profile_repo = ProfileRepository()  # noqa
offer_repo = OfferRepository()  # noqa
eval_repo = CleanerEvaluationRepository()  # noqa
feed_repo = FeedRepository()  # noqa
