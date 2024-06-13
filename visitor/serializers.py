from rest_framework import serializers
from visitor.models import VisitorProfile, Visit


class VisitorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorProfile
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    visitor = VisitorProfileSerializer()

    class Meta:
        model = Visit
        fields = "__all__"