import factory
from django.utils.timezone import now
from factory.django import DjangoModelFactory
from faker import Faker
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
)
from organisation import GENDER_CHOICES, MARIATAL_STATUS_CHOICES

fake = Faker()


class OrganisationFactory(DjangoModelFactory):
    """
    Factory for organisation
    """

    class Meta:
        model = Organisation

    name = factory.Faker("company")
    org_type = factory.LazyAttribute(lambda _: fake.job())
    email = factory.Faker("email")
    org_address = factory.Faker("address")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")


class UnitFactory(DjangoModelFactory):
    """
    Factory for unit
    """

    class Meta:
        model = Unit

    name = factory.Faker("company")
    address = factory.Faker("address")
    description = factory.Faker("text", max_nb_chars=256)
    org = factory.SubFactory("organisation.factories.OrganisationFactory")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")


class GateFactory(DjangoModelFactory):
    """
    Factory for gate
    """

    class Meta:
        model = Gate

    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=256)
    unit = factory.SubFactory("organisation.factories.UnitFactory")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")
    is_active = True


class DepartmentFactory(DjangoModelFactory):
    """
    Factory for department
    """

    class Meta:
        model = Department

    name = factory.Faker("company")
    department_type = factory.LazyAttribute(lambda _: fake.job())
    org = factory.SubFactory("organisation.factories.OrganisationFactory")
    unit = factory.SubFactory("organisation.factories.UnitFactory")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")
    is_active = True


class EmployeeProfileFactory(DjangoModelFactory):
    """
    Factory for employee profile
    """

    class Meta:
        model = EmployeeProfile

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    mobile_number = factory.Faker("phone_number")
    address = factory.Faker("address")
    gender = factory.Faker(
        "random_element", elements=[choice[0] for choice in GENDER_CHOICES]
    )
    date_of_birth = factory.Faker("date_of_birth")
    marital_status = factory.Faker(
        "random_element", elements=[choice[0] for choice in MARIATAL_STATUS_CHOICES]
    )
    photo = factory.django.FileField(
        filename=f'photos/{fake.file_name(category="image", extension="jpg")}'
    )
    department = factory.SubFactory("organisation.factories.DepartmentFactory")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")
    is_active = True


class EmployeeAuthorizationFactory(DjangoModelFactory):
    """
    Factory for employee authorization
    """

    class Meta:
        model = EmployeeAuthorization

    employee = factory.SubFactory("organisation.factories.EmployeeProfileFactory")
    user_acc = factory.SubFactory("accounts.factories.UserAccountFactory")
    created_by = factory.SubFactory("accounts.factories.UserAccountFactory")
    updated_by = factory.SelfAttribute("created_by")
