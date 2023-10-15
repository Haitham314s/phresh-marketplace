from uuid import uuid4

from tortoise import fields
from tortoise.models import Model

from app.models.user import User


class Profile(Model):
    class Meta:
        table = "profile"

    id = fields.UUIDField(pk=True, unique=True, index=True, default=uuid4)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="user_profile", on_delete=fields.CASCADE, index=True
    )

    full_name = fields.CharField(max_length=255, index=True, null=True)
    phone = fields.CharField(max_length=255, index=True, null=True)
    description = fields.CharField(max_length=255, null=True)
    image = fields.CharField(max_length=255, null=True)

    modified_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)
