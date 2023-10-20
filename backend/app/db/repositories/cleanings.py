from typing import List
from uuid import UUID

from app.core.error import APIException
from app.core.error_code import ErrorCode
from app.models import User
from app.models.cleaning import Cleaning, CleaningType
from app.models.schemas.cleaning import CleaningBase, CleaningOut, CleaningUpdateIn


class CleaningRepository:
    async def get_all_cleanings(self, user: User) -> List[CleaningOut]:
        return [
            CleaningOut.model_validate(cleaning)
            for cleaning in await Cleaning.filter(user_id=user.id, type__not=CleaningType.deleted).order_by(
                "-created_at"
            )
        ]

    async def get_cleaning_by_id(self, cleaning_id: UUID, user: User | None = None) -> Cleaning:
        cleaning = await Cleaning.get_or_none(id=cleaning_id, type__not=CleaningType.deleted)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if user is not None and cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)

        return cleaning

    async def create_cleaning(self, new_cleaning: CleaningBase, user: User) -> Cleaning:
        return await Cleaning.create(**new_cleaning.model_dump(), user_id=user.id)

    async def update_cleaning(self, cleaning_id: UUID, cleaning_in: CleaningUpdateIn, user: User) -> Cleaning:
        cleaning = await Cleaning.get_or_none(id=cleaning_id, type__not=CleaningType.deleted)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)

        cleaning_dict = CleaningOut.model_validate(cleaning).model_dump()
        cleaning_dict |= {key: value for key, value in cleaning_in.model_dump().items() if value is not None}

        await cleaning.update_from_dict(cleaning_dict)
        return cleaning

    async def delete_cleaning(self, cleaning_id: UUID, user: User):
        cleaning = await Cleaning.get_or_none(id=cleaning_id)
        if cleaning is None:
            raise APIException(ErrorCode.cleaning_not_found)
        if cleaning.user_id != user.id:
            raise APIException(ErrorCode.cleaning_unauthorized_access)

        cleaning.type = CleaningType.deleted
        await cleaning.save()
