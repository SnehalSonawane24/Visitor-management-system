from time import strftime
import pytz
from datetime import timezone

from django.db import models
from django.contrib.auth.models import AnonymousUser

from organisation.models import EmployeeProfile, Gate, Department
from config.abstract import (
    AbstractActiveStatus,
    AbstractUUID,
    AbstractProfile,
)
from accounts.models import UserAccount
from . import VISITOR_TYPE


class VisitorProfile(AbstractUUID, AbstractProfile):
    """
    For storing visitor data
    """

    email = models.EmailField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    photo = models.FileField(upload_to="visitor_photo", null=True, blank=True)
   
    created_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
    )

    updated_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        verbose_name_plural = "1. Visitor"
        # ordering = ["-created_at"]

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Visit(AbstractActiveStatus, AbstractUUID):
    """
    For storing visit's data of visitor with respective employee
    """

    purpose = models.TextField(max_length=256)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    no_of_individuals = models.IntegerField(default=1)
    vehicle_number = models.CharField(max_length=32, null=True, blank=True)
    # F.K's
    visitor = models.ForeignKey(
        VisitorProfile, on_delete=models.RESTRICT, related_name="visit_visitor"
    )

    employee = models.ForeignKey(
        EmployeeProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="visit_employee"
    )

    gate = models.ForeignKey(Gate, on_delete=models.RESTRICT, null=True, blank=True, related_name="visit_gate")

    created_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
    )

    updated_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        verbose_name_plural = "2. Visit"
        # ordering = ["-created_at"]

    def str(self):
        return f"{self.visitor} - {self.is_active}"

    @property
    def checkout_timezone(self):
        if self.check_out:
            checkout_time_kolkata = self.check_out.astimezone(
                pytz.timezone("Asia/Kolkata")
            )
            formatted_checkout_time = checkout_time_kolkata.strftime(
                "%B %d, %Y, %I:%M %p"
            )
            return formatted_checkout_time
        else:
            return None

    @property
    def checkin_timezone(self):
        return self.check_in.strftime("%B %d, %Y, %I:%M %p")

    def deactivate_visit(self):
        """
        Deactivate the visit by setting is_active to False
        """
        self.is_active = False
        self.save()
