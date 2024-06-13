from graphene_django import DjangoObjectType
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
)


class OrganisationType(DjangoObjectType):
    class Meta:
        model = Organisation
        fields = (
            "id",
            "name",
            "org_type",
            "email",
            "org_address",
            "created_at",
            "updated_at",
            "is_active",
        )


class UnitType(DjangoObjectType):
    class Meta:
        model = Unit
        fields = ("id", "name", "address", "description", "org", "is_active")


class GateType(DjangoObjectType):
    class Meta:
        model = Gate
        fields = ("id", "name", "description", "unit", "is_active")


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        fields = ("id", "name", "department_type", "org", "unit")


class EmployeeProfileType(DjangoObjectType):
    class Meta:
        model = EmployeeProfile
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "mobile_number",
            "address",
            "gender",
            "date_of_birth",
            "marital_status",
            "photo",
            "department",
        )


class EmployeeAuthorizationType(DjangoObjectType):
    class Meta:
        model = EmployeeAuthorization
        fields = (
            "employee",
            "user_acc",
        )
