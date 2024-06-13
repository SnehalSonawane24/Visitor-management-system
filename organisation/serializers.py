from rest_framework import serializers
from organisation.models import (
    Organisation,
    Unit,
    Gate,
    Department,
    EmployeeProfile,
    EmployeeAuthorization,
)


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"

class OrganisationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = "__all__"


class EmployeeAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAuthorization
        fields = "__all__"
