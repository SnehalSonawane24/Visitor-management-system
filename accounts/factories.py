import factory
from faker import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password
from accounts.models import UserAccount

fake = Faker()


class UserAccountFactory(DjangoModelFactory):
    """
    Factory for user account
    """

    class Meta:
        model = UserAccount

    @staticmethod
    def generate_unique_email(n):
        return f"user{n}@example.com"

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True
    is_staff = True
    is_superuser = True
    password = factory.LazyFunction(lambda: make_password("user@123"))

    @factory.post_generation
    def set_password(self, obj, create, **kwargs):
        if create:
            self.set_password("user@123")
            self.save()
