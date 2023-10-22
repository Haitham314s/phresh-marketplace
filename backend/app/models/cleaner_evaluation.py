from uuid import uuid4

from tortoise import Model, fields

from app.models.user import User
from app.models.cleaning import Cleaning


class CleanerEvaluation(Model):
    class Meta:
        table = "cleaner_evaluation"

    id = fields.UUIDField(pk=True, unique=True, default=uuid4)
    cleaning: fields.ForeignKeyRelation[Cleaning] = fields.ForeignKeyField(
        "models.Cleaning", related_name="evaluation_for_cleaning", on_delete=fields.SET_NULL, null=True, index=True
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="cleaner_user", on_delete=fields.SET_NULL, null=True, index=True
    )

    hidden = fields.BooleanField(index=True, default=False)
    headline = fields.CharField(max_length=256, null=True)
    comment = fields.CharField(max_length=256, null=True)
    professionalism = fields.IntField()
    completeness = fields.IntField()
    efficiency = fields.IntField()
    overall_rating = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    modified_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
