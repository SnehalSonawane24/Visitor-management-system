import graphene
from graphene_django import DjangoObjectType
from visitor.models import VisitorProfile, Visit
from visitor.graphql_types import VisitorProfileType, VisitType


class Query(graphene.ObjectType):
    all_visitor_profile = graphene.List(VisitorProfileType)
    visitor_profile_by_id = graphene.List(VisitorProfileType, id=graphene.UUID())

    all_visit = graphene.List(VisitType)
    visit_by_id = graphene.List(VisitType, id=graphene.UUID())

    def resolve_all_visitor_profile(root, info):
        return VisitorProfile.objects.all()

    def resolve_visitor_profile_by_id(root, info, id):
        try:
            return VisitorProfile.objects.get(pk=id)
        except VisitorProfile.DoesNotExist:
            return None

    def resolve_all_visit(root, info):
        return Visit.objects.all()

    def resolve_visit_by_id(root, info, id):
        try:
            return Visit.objects.get(pk=id)

        except Visit.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
