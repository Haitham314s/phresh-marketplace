from enum import Enum
from uuid import uuid4

from tortoise import fields
from tortoise.models import Model

from app.models.cleaning import Cleaning
from app.models.user import User


class OfferStatus(str, Enum):
    accepted = "accepted"
    pending = "pending"
    rejected = "rejected"
    cancelled = "cancelled"


class Offer(Model):
    id = fields.UUIDField(pk=True, unique=True, default=uuid4)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="offer_for_user", on_delete=fields.CASCADE, index=True
    )
    cleaning: fields.ForeignKeyRelation[Cleaning] = fields.ForeignKeyField(
        "models.Cleaning", related_name="offer_for_cleaning", on_delete=fields.CASCADE, index=True
    )
    status = fields.CharEnumField(OfferStatus, index=True, default=OfferStatus.pending)

    modified_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
