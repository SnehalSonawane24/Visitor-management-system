from accounts.models import UserAccount
from organisation.models import Organisation, Unit, Gate, Department, EmployeeProfile
from django.forms import ValidationError
from datetime import date


def get_user_account(user_id):
    try:
        return UserAccount.objects.get(pk=user_id)
    except UserAccount.DoesNotExist:
        raise ValidationError("UserAccount with the given ID does not exist.")


def get_organisation(org_id):
    try:
        return Organisation.objects.get(pk=org_id)
    except Organisation.DoesNotExist:
        raise ValidationError("Organisation with the given ID does not exist.")


def get_unit(unit_id):
    try:
        return Unit.objects.get(pk=unit_id)
    except Unit.DoesNotExist:
        raise ValidationError("Unit with the given ID does not exist.")


def get_gate(gate_id):
    try:
        return Gate.objects.get(pk=gate_id)
    except Gate.DoesNotExist:
        raise ValidationError("Gate with the given ID does not exist.")


def get_department(department_id):
    try:
        return Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        raise ValidationError("Department with the given ID does not exist.")


def get_employee_profile(employee_id):
    try:
        return EmployeeProfile.objects.get(pk=employee_id)
    except EmployeeProfile.DoesNotExist:
        raise ValidationError("EmployeeProfile with the given ID does not exist.")


def create_or_update_organisation(input, created_by=None, updated_by=None):
    if input.id:
        organisation = get_organisation(input.id)
    else:
        organisation = Organisation()

    organisation.name = input.name
    organisation.org_type = input.org_type
    organisation.email = input.email
    organisation.org_address = input.org_address
    organisation.created_by = created_by
    organisation.updated_by = updated_by

    organisation.save()
    return organisation


def create_or_update_unit(input, organisation, created_by=None, updated_by=None):
    if input.id:
        unit = get_unit(input.id)
    else:
        unit = Unit()

    unit.name = input.name
    unit.address = input.address
    unit.description = input.description
    unit.is_active = input.is_active
    unit.org = organisation
    unit.created_by = created_by
    unit.updated_by = updated_by

    unit.save()
    return unit


def create_or_update_gate(input, unit, created_by, updated_by):
    if input.id:
        gate = get_gate(input.id)
        gate.name = input.name
        gate.description = input.description
        gate.unit = unit
        gate.updated_by = updated_by
    else:
        gate = Gate.objects.create(
            name=input.name,
            unit=unit,
            created_by=created_by,
            updated_by=updated_by,
        )
    gate.save()
    return gate


def create_or_update_department(input, org, unit, created_by, updated_by):
    if input.id:
        department = get_department(input.id)
        department.name = input.name
        department.department_type = input.departmentType
        department.org = org
        department.unit = unit
        department.updated_by = updated_by
    else:
        department = Department.objects.create(
            name=input.name,
            department_type=input.departmentType,
            org=org,
            unit=unit,
            created_by=created_by,
            updated_by=updated_by,
        )
    department.save()
    return department


def create_or_update_employee_profile(input, department, created_by, updated_by):
    if input.id:
        employee_profile = EmployeeProfile.objects.get(id=input.id)
        employee_profile.first_name = input.first_name
        employee_profile.middle_name = input.middle_name
        employee_profile.last_name = input.last_name
        employee_profile.email = input.email
        employee_profile.mobile_number = input.mobile_number
        employee_profile.address = input.address
        employee_profile.gender = input.gender
        employee_profile.date_of_birth = input.date_of_birth
        employee_profile.marital_status = input.marital_status
        employee_profile.photo = input.photo
        employee_profile.department = department
        employee_profile.updated_by = updated_by
    else:
        employee_profile = EmployeeProfile.objects.create(
            first_name=input.first_name,
            middle_name=input.middle_name,
            last_name=input.last_name,
            email=input.email,
            mobile_number=input.mobile_number,
            address=input.address,
            gender=input.gender,
            date_of_birth=input.date_of_birth,
            marital_status=input.marital_status,
            photo=input.photo,
            department=department,
            created_by=created_by,
            updated_by=updated_by,
        )
    employee_profile.save()
    return employee_profile
