from enum import Enum
from uuid import uuid4

from tortoise import fields
from tortoise.models import Model

from app.models.user import User


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"
    deleted = "deleted"


class Cleaning(Model):
    class Meta:
        table = "cleaning"

    id = fields.UUIDField(pk=True, unique=True, index=True, default=uuid4)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="cleaning_user", on_delete=fields.CASCADE, index=True
    )

    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    type = fields.CharEnumField(CleaningType, index=True, default=CleaningType.spot_clean)
    price = fields.DecimalField(max_digits=10, decimal_places=2, index=True)

    modified_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
