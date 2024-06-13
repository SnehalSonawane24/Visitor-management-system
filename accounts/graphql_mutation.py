import graphene
from accounts.models import UserAccount
from accounts.graphql_types import UserAccountType


class UpsertUserAccount(graphene.Mutation):
    user = graphene.Field(UserAccountType)

    class Arguments:
        id = graphene.ID()
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        is_active = graphene.Boolean()
        is_staff = graphene.Boolean()
        is_manager = graphene.Boolean()
        is_superuser = graphene.Boolean()

    def mutate(
        self,
        info,
        email,
        name,
        password,
        id=None,
        is_active=None,
        is_staff=None,
        is_manager=None,
        is_superuser=None,
    ):
        if id:
            try:
                user = UserAccount.objects.get(pk=id)
            except UserAccount.DoesNotExist:
                raise Exception("User not found")

            if email:
                user.email = email
            if name:
                user.name = name
            if password:
                user.set_password(password)
            if is_active is not None:
                user.is_active = is_active
            if is_staff is not None:
                user.is_staff = is_staff
            if is_manager is not None:
                user.is_manager = is_manager
            if is_superuser is not None:
                user.is_superuser = is_superuser

            user.save()
        else:
            user = UserAccount.objects.create_user(
                email=email, name=name, password=password
            )
            if is_active is not None:
                user.is_active = is_active
            if is_staff is not None:
                user.is_staff = is_staff
            if is_manager is not None:
                user.is_manager = is_manager
            if is_superuser is not None:
                user.is_superuser = is_superuser

            user.save()

        return UpsertUserAccount(user=user)


class DeleteUserAccount(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            user = UserAccount.objects.get(pk=id)
            user.delete()
            return DeleteUserAccount(success=True)
        except UserAccount.DoesNotExist:
            raise Exception("User not found")


class Mutation(graphene.ObjectType):
    create_update_user_account = UpsertUserAccount.Field()
    delete_user_account = DeleteUserAccount.Field()


schema = graphene.Schema(mutation=Mutation)
