import graphene
from graphene_django import DjangoObjectType
from .models import UserAccount


class UserAccountType(DjangoObjectType):
    class Meta:
        model = UserAccount
        fields = ("id", "email", "name", "is_active",
                  "is_staff", "is_superuser", "is_manager")
