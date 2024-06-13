from requests import Response
from rest_framework import viewsets, filters
from accounts.models import UserAccount
from accounts.serializers import UserAccountSerialiser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from organisation.models import EmployeeAuthorization


class UserAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAccountSerialiser
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_manager", "is_superuser", "is_staff"]
    search_fields = ["email", "name"]
    ordering_fields = ["name", "email"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return UserAccount.objects.all()
            else:
                return UserAccount.objects.filter(id=user.id)


class StaffViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAccountSerialiser
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_manager", "is_superuser", "is_staff"]
    search_fields = ["email", "name"]
    ordering_fields = ["name", "email"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                user_authorization = EmployeeAuthorization.objects.get(user_acc=user)
                user_organization = user_authorization.employee.department.org
                return UserAccount.objects.filter(
                    user_acc_emp__employee__department__org=user_organization,
                    is_staff=True,
                )
            except EmployeeAuthorization.DoesNotExist:
                return UserAccount.objects.none()


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAccountSerialiser
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_manager", "is_superuser", "is_staff"]
    search_fields = ["email", "name"]
    ordering_fields = ["name", "email"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                user_authorization = EmployeeAuthorization.objects.get(user_acc=user)
                user_organization = user_authorization.employee.department.org
                return UserAccount.objects.filter(
                    user_acc_emp__employee__department__org=user_organization,
                    is_manager=True,
                )
            except EmployeeAuthorization.DoesNotExist:
                return UserAccount.objects.none()
