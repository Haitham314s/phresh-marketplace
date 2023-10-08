from typing import List

from fastapi import APIRouter, status

from app.db.repositories.cleanings import CleaningRepository
from app.models.schemas.cleaning import CleaningBase, CleaningOut

router = APIRouter()


@router.get("/")
async def get_all_cleanings() -> List[dict]:
    return [
        {
            "id": 1,
            "name": "My house",
            "cleaning_type": "full_clean",
            "price_per_hour": 29.99,
        },
        {
            "id": 2,
            "name": "Someone else's house",
            "cleaning_type": "spot_clean",
            "price_per_hour": 19.99,
        },
    ]


@router.post(
    "/",
    response_model=CleaningOut,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_cleaning(new_cleaning: CleaningBase):
    cleaning_repo = CleaningRepository()
    cleaning_out = await cleaning_repo.create_cleaning(new_cleaning)
    print(f"CLEANING_OUT: {cleaning_out}")
    return cleaning_out
