from accounts.models import UserAccount
from visitor.models import VisitorProfile, Visit
from django.forms import ValidationError


def get_user_account(user_id):
    try:
        return UserAccount.objects.get(pk=user_id)
    except UserAccount.DoesNotExist:
        raise ValidationError("UserAccount with the given ID does not exist.")


def get_visitor_profile(visitor_id):
    try:
        return VisitorProfile.objects.get(pk=visitor_id)
    except VisitorProfile.DoesNotExist:
        raise ValidationError("Visitor Profile with the given ID does not exists.")


def get_visit(visit_id):
    try:
        return Visit.objects.get(pk=visit_id)
    except Visit.DoesNotExist:
        raise ValidationError("Visit with the given ID does not exists.")


def create_or_update_visitor_profile(input, created_by, updated_by):
    if input.id:
        visitor_profile = VisitorProfile.objects.get(id=input.id)
        visitor_profile.first_name = input.first_name
        visitor_profile.mobile_number = input.middle_name
        visitor_profile.last_name = input.last_name
        visitor_profile.email = input.email
        visitor_profile.mobile_number = input.mobile_number
        visitor_profile.address = input.address
        visitor_profile.gender = input.gender
        visitor_profile.photo = input.photo
        visitor_profile.no_of_individuals = input.no_of_individuals
        visitor_profile.updated_by = updated_by
    else:
        visitor_profile = VisitorProfile.objects.create(
            first_name=input.first_name,
            middle_name=input.middle_name,
            last_name=input.last_name,
            email=input.email,
            mobile_number=input.mobile_number,
            address=input.address,
            gender=input.gender,
            photo=input.photo,
            no_of_individuals=input.no_of_individuals,
            created_by=created_by,
            updated_by=updated_by,
        )

    visitor_profile.save()
    return visitor_profile


def create_or_update_visit(input, visitor, employee, gate, created_by, updated_by):
    if input.id:
        visit = Visit.objects.get(id=input.id)
        visit.purpose = input.purpose
        visit.check_in = input.check_in
        visit.check_out = input.check_out
        visit.visitor = visitor
        visit.employee = employee
        visit.gate = gate
        visit.updated_by = updated_by
    else:
        visit = Visit.objects.create(
            purpose=input.purpose,
            check_in=input.check_in,
            check_out=input.check_out,
            visitor=visitor,
            employee=employee,
            gate=gate,
            created_by=created_by,
            updated_by=updated_by,
        )
    visit.save()
    return visit
