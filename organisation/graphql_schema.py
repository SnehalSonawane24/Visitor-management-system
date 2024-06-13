import graphene
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
)

from organisation.graphql_types import (
    OrganisationType,
    UnitType,
    GateType,
    DepartmentType,
    EmployeeProfileType,
    EmployeeAuthorizationType,
)


class Query(graphene.ObjectType):
    all_organisations = graphene.List(OrganisationType)
    organisation_by_id = graphene.Field(OrganisationType, id=graphene.UUID())
    all_units = graphene.List(UnitType)
    unit_by_id = graphene.Field(UnitType, id=graphene.UUID())
    all_gates = graphene.List(GateType)
    gate_by_id = graphene.Field(GateType, id=graphene.UUID())
    all_departments = graphene.List(DepartmentType)
    department_by_id = graphene.Field(DepartmentType, id=graphene.UUID())
    all_employee_profiles = graphene.List(EmployeeProfileType)
    employee_profile_by_id = graphene.Field(EmployeeProfileType, id=graphene.UUID())
    all_employee_authorizations = graphene.List(EmployeeAuthorizationType)
    employee_authorization_by_id = graphene.Field(
        EmployeeAuthorizationType, id=graphene.UUID()
    )

    def resolve_all_organisations(root, info):
        return Organisation.objects.all()

    def resolve_organisation_by_id(root, info, id):
        try:
            return Organisation.objects.get(pk=id)
        except Organisation.DoesNotExist:
            return None

    def resolve_all_units(root, info):
        return Unit.objects.all()

    def resolve_unit_by_id(root, info, id):
        try:
            return Unit.objects.get(pk=id)
        except Unit.DoesNotExist:
            return None

    def resolve_all_gates(root, info):
        return Gate.objects.all()

    def resolve_gate_by_id(root, info, id):
        try:
            return Gate.objects.get(pk=id)
        except Gate.DoesNotExist:
            return None

    def resolve_all_departments(root, info):
        return Department.objects.all()

    def resolve_department_by_id(root, info, id):
        try:
            return Department.objects.get(pk=id)
        except Department.DoesNotExist:
            return None

    def resolve_all_employee_profiles(root, info):
        return EmployeeProfile.objects.all()

    def resolve_employee_profile_by_id(root, info, id):
        try:
            return EmployeeProfile.objects.get(pk=id)
        except EmployeeProfile.DoesNotExist:
            return None

    def resolve_all_employee_authorizations(root, info):
        return EmployeeAuthorization.objects.all()

    def resolve_employee_authorization_by_id(root, info, id):
        try:
            return EmployeeAuthorization.objects.get(pk=id)
        except EmployeeAuthorization.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
