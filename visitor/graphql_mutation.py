import graphene
from visitor.graphql_types import VisitorProfileType, VisitType
from visitor.models import VisitorProfile
from visitor.helper import (
    get_user_account,
    get_visitor_profile,
    get_visit,
    create_or_update_visitor_profile,
    create_or_update_visit,
)

from organisation.helper import get_employee_profile, get_gate


class VisitorProfileInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String(required=True)
    middle_name = graphene.String(required=False)
    last_name = graphene.String(required=True)
    email = graphene.String(required=False)
    mobile_number = graphene.String(required=False)
    address = graphene.String(required=True)
    gender = graphene.String(required=False)
    photo = graphene.String()
    no_of_individuals = graphene.String()
    created_by_id = graphene.ID(required=True)
    updated_by_id = graphene.ID(required=True)


class VisitInput(graphene.InputObjectType):
    id = graphene.UUID(required=False)
    purpose = graphene.String(required=True)
    check_in = graphene.DateTime(required=True)
    check_out = graphene.DateTime(required=False)
    visitor = graphene.UUID(required=True)
    employee = graphene.UUID(required=True)
    gate = graphene.String(required=True)
    created_by_id = graphene.ID(required=True)
    updated_by_id = graphene.ID(required=True)


class VisitFilterInput(graphene.InputObjectType):
    check_in = graphene.DateTime(required=True)
    check_out = graphene.DateTime(required=False)
    organisation_id = graphene.ID(required=True)


class CreateOrUpdateVisitorProfile(graphene.Mutation):
    class Arguments:
        input = VisitorProfileInput(required=True)

    visitor_profile = graphene.Field(VisitorProfileType)

    def mutate(self, info, input):
        created_by = get_user_account(input.created_by_id)
        updated_by = get_user_account(input.updated_by_id)

        visitor_profile = create_or_update_visitor_profile(
            input, created_by, updated_by
        )

        return CreateOrUpdateVisitorProfile(visitor_profile=visitor_profile)


class DeleteVisitorProfile(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        visitor_profile = get_visitor_profile(id)
        visitor_profile.delete()
        return DeleteVisitorProfile(success=True)


class CreateOrUpdateVisit(graphene.Mutation):
    class Arguments:
        input = VisitInput(required=True)

    visit = graphene.Field(VisitType)

    def mutate(self, info, input):
        visitor = VisitorProfile.objects.get(id=input.visitor)
        employee = get_employee_profile(input.employee)
        gate = get_gate(input.gate)
        created_by = get_user_account(input.created_by_id)
        updated_by = get_user_account(input.updated_by_id)

        visit = create_or_update_visit(
            input, visitor, employee, gate, created_by, updated_by
        )

        return CreateOrUpdateVisit(visit=visit)


class DeleteVisit(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        visit = get_visit(id)
        visit.delete()
        return DeleteVisit(success=True)


class Mutation(graphene.ObjectType):
    # Visitor Profile
    create_or_update_visitor_profile = CreateOrUpdateVisitorProfile.Field()
    delete_visitor_profile = DeleteVisitorProfile.Field()

    # Visit
    create_or_update_visit = CreateOrUpdateVisit.Field()
    delete_visit = DeleteVisit.Field()


schema = graphene.Schema(mutation=Mutation)
