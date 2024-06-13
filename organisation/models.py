from django.db import models
from organisation import MARIATAL_STATUS_CHOICES
from accounts.models import UserAccount
from config.abstract import (
    AbstractCreater,
    AbstractUpdater,
    AbstractActiveStatus,
    AbstractUUID,
    AbstractProfile,
)


class Organisation(
    AbstractCreater, AbstractUpdater, AbstractActiveStatus, AbstractUUID
):
    name = models.CharField(max_length=128)
    org_type = models.CharField(
        max_length=100,
        help_text="Type of organisation e.g: Technical company"
    )
    email = models.EmailField(max_length=64, unique=True)
    org_address = models.TextField(max_length=256)

    class Meta:
        verbose_name_plural = "1. Organisation"
        unique_together = ['name', 'org_type']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"


class Unit(
    AbstractCreater, AbstractUpdater, AbstractActiveStatus, AbstractUUID
):
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=256)
    description = models.TextField(max_length=256, null=True, blank=True)

    # F.K's
    org = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="unit_org"
    )

    class Meta:
        verbose_name_plural = "2. Unit"
        unique_together = ["name", "org"]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"

    def deactivate_unit(self):
        """
        Deactivate the unit by setting is_active to False
        """
        self.is_active = False
        self.save()


class Gate(
    AbstractCreater, AbstractUpdater, AbstractActiveStatus
):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256, null=True, blank=True)

    # F.K's
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="gate_unit"
    )

    class Meta:
        verbose_name_plural = "3. Gate"
        unique_together = ["name", "unit"]
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"

    def deactivate_gate(self):
        """
        Deactivate the gate by setting is_active to False
        """
        self.is_active = False
        self.save()


class Department(AbstractCreater, AbstractUpdater, AbstractActiveStatus,
                 AbstractUUID):
    name = models.CharField(max_length=64)
    department_type = models.CharField(
        max_length=100,
        help_text="Type of department e.g: Technical Department"
    )

    # F.K's
    org = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="dept_org"
    )

    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="dept_unit"
    )

    class Meta:
        verbose_name_plural = "4. Department"
        unique_together = ["name", "org"]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"

    def deactivate_department(self):
        """
        Deactivate the department by setting is_active to False
        """
        self.is_active = False
        self.save()


class EmployeeProfile(AbstractCreater, AbstractUpdater, AbstractUUID,
                      AbstractProfile, AbstractActiveStatus):
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=16,
                                      choices=MARIATAL_STATUS_CHOICES)
    photo = models.FileField(upload_to="emp_photo", blank=True, null=True)

    # F.K's
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="dept_emp"
    )

    class Meta:
        verbose_name_plural = "5. Employee Profile"
        unique_together = ["email", "mobile_number"]
        ordering = ['-created_at']

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    def deactivate_employee(self):
        """
        Deactivate the employee by setting is_active to False
        """
        self.is_active = False
        self.save()


class EmployeeAuthorization(AbstractCreater, AbstractUpdater):
    employee = models.ForeignKey(
        EmployeeProfile, on_delete=models.CASCADE, related_name="permissions"
    )
    user_acc = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="user_acc_emp"
    )

    class Meta:
        verbose_name_plural = "6. Employee Authorization"
        unique_together = ["employee", "user_acc"]


class UnitAccessAuthorization(AbstractCreater, AbstractUpdater):
    user_acc = models.ForeignKey(
        UserAccount, on_delete=models.RESTRICT, related_name="user_acc_unit"
    )

    unit = models.ForeignKey(
        Unit, on_delete=models.RESTRICT, related_name="unit_auth"
    )

    class Meta:
        verbose_name_plural = "7. Unit Access Authorization"
        unique_together = ["unit", "user_acc"]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.unit.name} - {self.user_acc.name}"
