import graphene
from django.db.models import Q
from organisation.graphql_types import (
    OrganisationType,
    UnitType,
    GateType,
    DepartmentType,
    EmployeeProfileType,
)
from organisation.models import EmployeeProfile

from organisation.helper import (
    get_user_account,
    get_organisation,
    get_unit,
    get_gate,
    get_department,
    get_employee_profile,
    create_or_update_organisation,
    create_or_update_unit,
    create_or_update_gate,
    create_or_update_department,
    create_or_update_employee_profile,
)


# Define GenderEnum
class GenderEnum(graphene.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# Define MaritalStatusEnum
class MaritalStatusEnum(graphene.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class OrganisationInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    org_type = graphene.String(required=True)
    email = graphene.String(required=True)
    org_address = graphene.String(required=True)
    created_by_id = graphene.ID()
    updated_by_id = graphene.ID(required=True)


class UnitInput(graphene.InputObjectType):
    id = graphene.String()
    name = graphene.String(required=True)
    address = graphene.String(required=True)
    description = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    org_id = graphene.ID(required=True)
    created_by_id = graphene.ID(required=True)
    updated_by_id = graphene.ID(required=True)


class GateInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    unit = graphene.String(required=True)
    created_by_id = graphene.ID(required=True)
    updated_by_id = graphene.ID(required=True)


class DepartmentInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    departmentType = graphene.String(required=True)
    orgId = graphene.ID(required=True)
    unitId = graphene.ID(required=True)
    createdById = graphene.ID(required=True)
    updatedById = graphene.ID(required=True)


class EmployeeProfileInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String(required=True)
    middle_name = graphene.String()
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    mobile_number = graphene.String(required=True)
    address = graphene.String(required=True)
    # gender = GenderEnum(required=True)
    gender = graphene.String(required=False)
    date_of_birth = graphene.Date(required=True)
    # marital_status = MaritalStatusEnum(required=False)
    marital_status = graphene.String(required=False)
    photo = graphene.String()
    department_id = graphene.ID(required=True)
    created_by_id = graphene.ID(required=True)
    updated_by_id = graphene.ID(required=True)


class SaveOrganisation(graphene.Mutation):
    class Arguments:
        input = OrganisationInput(required=True)

    organisation = graphene.Field(OrganisationType)

    def mutate(self, info, input):
        created_by = (
            get_user_account(input.created_by_id) if input.created_by_id else None
        )
        updated_by = get_user_account(input.updated_by_id)
        organisation = create_or_update_organisation(input, created_by, updated_by)
        return SaveOrganisation(organisation=organisation)


class DeleteOrganisation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        organisation = get_organisation(id)
        organisation.delete()
        return DeleteOrganisation(success=True)


class SaveUnit(graphene.Mutation):
    class Arguments:
        input = UnitInput(required=True)

    unit = graphene.Field(UnitType)

    def mutate(self, info, input):
        organisation = get_organisation(input.org_id)
        created_by = get_user_account(input.created_by_id)
        updated_by = get_user_account(input.updated_by_id)
        unit = create_or_update_unit(input, organisation, created_by, updated_by)
        return SaveUnit(unit=unit)


class DeleteUnit(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        unit = get_unit(id)
        unit.delete()
        return DeleteUnit(success=True)


class CreateOrUpdateGate(graphene.Mutation):
    class Arguments:
        input = GateInput(required=True)

    gate = graphene.Field(GateType)

    def mutate(self, info, input):
        created_by = get_user_account(input.created_by_id)
        updated_by = get_user_account(input.updated_by_id)
        unit = get_unit(input.unit)
        gate = create_or_update_gate(input, unit, created_by, updated_by)
        return CreateOrUpdateGate(gate=gate)


class DeleteGate(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        gate = get_gate(id)
        gate.delete()
        return DeleteGate(success=True)


class CreateOrUpdateDepartment(graphene.Mutation):
    class Arguments:
        input = DepartmentInput(required=True)

    department = graphene.Field(DepartmentType)

    def mutate(self, info, input):
        created_by = get_user_account(input.createdById)
        updated_by = get_user_account(input.updatedById)
        org = get_organisation(input.orgId)
        unit = get_unit(input.unitId)
        department = create_or_update_department(
            input, org, unit, created_by, updated_by
        )
        return CreateOrUpdateDepartment(department=department)


class DeleteDepartment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        department = get_department(id)
        department.delete()
        return DeleteDepartment(success=True)


class CreateOrUpdateEmployeeProfile(graphene.Mutation):
    class Arguments:
        input = EmployeeProfileInput(required=True)

    emp_profile = graphene.Field(EmployeeProfileType)

    def mutate(self, info, input):
        created_by = get_user_account(input.created_by_id)
        updated_by = get_user_account(input.updated_by_id)
        department = get_department(input.department_id)

        # Check if there's an existing profile with the provided email or mobile number
        existing_profile = EmployeeProfile.objects.filter(
            Q(email=input.email) | Q(mobile_number=input.mobile_number)
        ).first()

        if existing_profile:
            # Handle the case of an existing profile
            existing_profile = create_or_update_employee_profile(
                input, department, created_by, updated_by
            )
            return CreateOrUpdateEmployeeProfile(emp_profile=existing_profile)
        else:
            # Create a new profile if no existing profile found
            emp_profile = create_or_update_employee_profile(
                input, department, created_by, updated_by
            )
            return CreateOrUpdateEmployeeProfile(emp_profile=emp_profile)


class DeleteEmployeeProfile(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        emp_profile = get_employee_profile(id)
        emp_profile.delete()
        return DeleteEmployeeProfile(success=True)


class Mutation(graphene.ObjectType):
    # Organisation
    save_organisation = SaveOrganisation.Field()
    delete_organisation = DeleteOrganisation.Field()

    # Unit
    save_unit = SaveUnit.Field()
    delete_unit = DeleteUnit.Field()

    # Gate
    create_or_update_gate = CreateOrUpdateGate.Field()
    delete_gate = DeleteGate.Field()

    # Department
    create_or_update_department = CreateOrUpdateDepartment.Field()
    delete_department = DeleteDepartment.Field()

    # EmployeeProfile
    create_or_update_employee_profile = CreateOrUpdateEmployeeProfile.Field()
    delete_emp_profile = DeleteEmployeeProfile.Field()


schema = graphene.Schema(mutation=Mutation)
