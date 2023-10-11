from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = "user"

    id = fields.UUIDField(pk=True, unique=True, index=True, default=uuid4)
    username = fields.CharField(max_length=255, index=True)
    email = fields.CharField(max_length=255, index=True)
    email_verified = fields.BooleanField(default=False, index=True)

    salt = fields.TextField(null=True)
    hashed_password = fields.TextField(null=True)

    is_active = fields.BooleanField(default=True, index=True)
    is_superuser = fields.BooleanField(default=False)

    modified_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)
