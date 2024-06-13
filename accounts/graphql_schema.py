import graphene
from accounts.models import UserAccount
from accounts.graphql_types import UserAccountType


class Query(graphene.ObjectType):
    user_accounts = graphene.List(UserAccountType)

    def resolve_user_accounts(self, info):
        return UserAccount.objects.all()
