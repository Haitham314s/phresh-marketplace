from enum import Enum

from tortoise import fields
from tortoise.models import Model


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class Cleaning(Model):
    class Meta:
        table = "cleaning"

    id = fields.UUIDField(pk=True, unique=True, index=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    type = fields.CharEnumField(
        CleaningType, index=True, default=CleaningType.spot_clean
    )
    price = fields.DecimalField(max_digits=10, decimal_places=2, null=True, index=True)

    modified = fields.DatetimeField(auto_now=True)
    created = fields.DatetimeField(auto_now_add=True)
