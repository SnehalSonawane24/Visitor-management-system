from rest_framework import viewsets, filters
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
)
from organisation.serializers import (
    OrganisationSerializer,
    UnitSerializer,
    GateSerializer,
    DepartmentSerializer,
    EmployeeProfileSerializer,
    EmployeeAuthorizationSerializer,
)
from visitor.views import organisations_details
from utils.helper import CustomPagination


class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name", "org_type", "email"]
    ordering_fields = ["id", "name", "org_type", "email"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)
            return organisations
        return Organisation.objects.none()


class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name", "address"]
    ordering_fields = ["id", "name", "address"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)
            units = Unit.objects.filter(org__in=organisations)
            return units
        return Unit.objects.none()


class GateViewSet(viewsets.ModelViewSet):
    serializer_class = GateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = [
        "id",
        "name",
    ]

    ordering_fields = [
        "id",
        "name",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)
            units = Unit.objects.filter(org__in=organisations)
            gates = Gate.objects.filter(unit__in=units)
            return gates
        return Gate.objects.none()


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination

    search_fields = [
        "id",
        "name",
        "department_type",
    ]
    ordering_fields = [
        "id",
        "name",
        "department_type",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)
            departments = Department.objects.select_related("org").filter(
                org__in=organisations
            )
            return departments
        return Department.objects.none()


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination

    search_fields = [
        "id",
        "first_name",
        "last_name",
        "department__name",
    ]
    ordering_fields = ["id"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)

            employees = EmployeeProfile.objects.select_related("department").filter(
                department__org__in=organisations
            )
            return employees
        return EmployeeProfile.objects.none()


class EmployeeAuthorizationViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeAuthorizationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = [
        "employee__user__name",
        "user_acc__name",
    ]

    ordering_fields = [
        "id",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            organisations, _, _ = organisations_details(user)
            employee_auths = EmployeeAuthorization.objects.select_related(
                "employee__department__org"
            ).filter(employee__department__org__in=organisations)
            return employee_auths
        return EmployeeAuthorization.objects.none()
