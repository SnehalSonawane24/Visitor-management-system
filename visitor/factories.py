import factory
from django.utils.timezone import now
from factory.django import DjangoModelFactory
from faker import Faker
from visitor.models import VisitorProfile, Visit
from organisation import GENDER_CHOICES
from accounts.factories import UserAccountFactory
from organisation.factories import GateFactory, EmployeeProfileFactory
from factory import SubFactory
from accounts.factories import UserAccountFactory

import pytz

fake = Faker()


class VisitorProfileFactory(DjangoModelFactory):
    """
    Factory for Visitor Profile
    """

    class Meta:
        model = VisitorProfile

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    mobile_number = factory.Faker("phone_number")
    address = factory.Faker("address")
    gender = factory.Faker(
        "random_element", elements=[choice[0] for choice in GENDER_CHOICES]
    )
    photo = factory.django.FileField(
        filename=f'photos/{fake.file_name(category="image", extension="jpg")}'
    )
    no_of_individuals = factory.Faker("random_int", min=1, max=10)
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")


class VisitFactory(DjangoModelFactory):
    """
    Factory for Visit
    """

    class Meta:
        model = Visit

    purpose = factory.Faker("text", max_nb_chars=256)
    check_in = factory.LazyFunction(lambda: fake.date_time_this_decade(tzinfo=pytz.UTC))
    check_out = factory.LazyFunction(
        lambda: (
            fake.date_time_this_month(tzinfo=pytz.UTC)
            if fake.boolean(chance_of_getting_true=80)
            else None
        )
    )
    visitor = SubFactory(VisitorProfileFactory)
    employee = SubFactory(EmployeeProfileFactory)
    gate = SubFactory(GateFactory)
    created_by = SubFactory(UserAccountFactory)
    updated_by = factory.SelfAttribute("created_by")
    is_active = True
