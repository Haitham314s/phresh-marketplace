from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.cleanings import get_cleaning_by_id
from app.core.response import SUCCESS_RESPONSE
from app.db.repositories import cleaning_repo
from app.models import User, Cleaning
from app.models.schemas.cleaning import CleaningBase, CleaningOut, CleaningUpdateIn

router = APIRouter()


@router.get("s", response_model=List[CleaningOut])
async def get_all_cleanings(user: User = Depends(get_current_user)):
    return await cleaning_repo.get_all_cleanings(user)


@router.get("/{cleaning_id}", response_model=CleaningOut)
async def get_cleaning(cleaning: Cleaning = Depends(get_cleaning_by_id)):
    return CleaningOut.model_validate(cleaning)


@router.post("", response_model=CleaningOut, status_code=status.HTTP_201_CREATED)
async def create_new_cleaning(new_cleaning: CleaningBase, user: User = Depends(get_current_user)):
    cleaning = await cleaning_repo.create_cleaning(new_cleaning, user)
    return CleaningOut.model_validate(cleaning)


@router.put("/{cleaning_id}", response_model=CleaningOut)
async def update_cleaning(cleaning_id: UUID, cleaning_in: CleaningUpdateIn, user: User = Depends(get_current_user)):
    cleaning = await cleaning_repo.update_cleaning(cleaning_id, cleaning_in, user)
    return CleaningOut.model_validate(cleaning)


@router.delete("/{cleaning_id}")
async def delete_cleaning(cleaning_id: UUID, user: User = Depends(get_current_user)):
    await cleaning_repo.delete_cleaning(cleaning_id, user)
    return SUCCESS_RESPONSE
