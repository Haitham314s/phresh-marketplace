from app.models import Profile
from app.models import User
from app.models.schemas.profile import ProfileCreateIn, ProfileUpdateIn, ProfileOut


class ProfileRepository:
    async def get_user_profile(self, user: User) -> Profile:
        return await Profile.get_or_none(user_id=user.id)

    async def create_user_profile(self, profile_in: ProfileCreateIn) -> Profile:
        profile_dict = {
            "full_name": profile_in.full_name,
            "phone": profile_in.phone,
            "description": profile_in.description,
            "image": profile_in.image,
            "user_id": profile_in.user_id,
        }

        return await Profile.create(**profile_dict)

    async def update_user_profile(self, user: User, profile_in: ProfileUpdateIn) -> Profile:
        profile = await Profile.get_or_none(user_id=user.id)
        if profile is None:
            profile = await self.create_user_profile(ProfileCreateIn(user_id=user.id, **profile_in.model_dump()))

        profile_dict = ProfileOut.model_validate(profile).model_dump(exclude={"id", "created_at", "modified_at"})
        profile_dict |= {key: value for key, value in profile_in.model_dump().items() if value is not None}

        await profile.update_from_dict(profile_dict)
        return profile
