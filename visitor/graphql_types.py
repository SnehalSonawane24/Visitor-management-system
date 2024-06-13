from graphene_django import DjangoObjectType
from visitor.models import VisitorProfile, Visit


class VisitorProfileType(DjangoObjectType):
    class Meta:
        model = VisitorProfile
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "mobile_number",
            "address",
            "gender",
            "photo",
            "no_of_individuals",
            "created_by",
            "updated_by",
        )


class VisitType(DjangoObjectType):
    class Meta:
        model = Visit

        fields = (
            "id",
            "purpose",
            "check_in",
            "check_out",
            "visitor",
            "employee",
            "gate",
            "created_by",
            "updated_by",
        )
