from accounts.models import UserAccount
from django.db import models
from config import GENDER_CHOICES

import uuid


class AbstractCreater(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UserAccount,
        on_delete=models.PROTECT,
        related_name="%(class)s_created_by",
    )

    class Meta:
        abstract = True


class AbstractUpdater(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        UserAccount,
        on_delete=models.PROTECT,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        abstract = True


class AbstractActiveStatus(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AbstractUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AbstractProfile(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64,  null=True, blank=True)

    email = models.CharField(max_length=128)
    mobile_number = models.CharField(max_length=16)
    address = models.TextField(max_length=256, null=True, blank=True)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default='MALE', null=True, blank=True)

    class Meta:
        abstract = True
