from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.db.repositories.cleanings import CleaningRepository
from app.models.schemas.cleaning import CleaningBase, CleaningOut, CleaningUpdateIn

router = APIRouter()


@router.get("s", response_model=List[CleaningOut])
async def get_all_cleanings():
    cleaning_repo = CleaningRepository()
    return await cleaning_repo.get_all_cleanings()


@router.get("/{cleaning_id}", response_model=CleaningOut)
async def get_cleaning(cleaning_id: UUID):
    cleaning_repo = CleaningRepository()
    cleaning = await cleaning_repo.get_cleaning_by_id(cleaning_id)

    return cleaning


@router.post(
    "",
    response_model=CleaningOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_cleaning(new_cleaning: CleaningBase):
    cleaning_repo = CleaningRepository()
    return await cleaning_repo.create_cleaning(new_cleaning)


@router.put("/{cleaning_id}", response_model=CleaningOut)
async def update_cleaning(cleaning_id: UUID, cleaning_in: CleaningUpdateIn):
    cleaning_repo = CleaningRepository()
    return await cleaning_repo.update_cleaning(cleaning_id, cleaning_in)


@router.delete("/{cleaning_id}")
async def get_cleaning(cleaning_id: UUID):
    cleaning_repo = CleaningRepository()
    await cleaning_repo.delete_cleaning(cleaning_id)
    return {"status": "success"}
