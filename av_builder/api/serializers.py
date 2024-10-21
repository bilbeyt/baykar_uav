from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from aircrafts.models import Aircraft, AircraftPart, AircraftPartName


class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    team_members = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "team_name", "team_members"]

    def get_team_name(self, obj):
        return obj.groups.first().name

    def get_team_members(self, obj):
        return User.objects.filter(groups__name=self.get_team_name(obj)).values_list("username", flat=True)


class AircraftPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftPart
        fields = ["name", "model", "aircraft", "created_at", "id"]


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["model", "created_at", "id"]

    def create(self, validated_data):
        with transaction.atomic():
            aircraft = super().create(validated_data)
            updated_parts = []
            for part_name in AircraftPartName:
                part = AircraftPart.objects.filter(aircraft__isnull=True, name=part_name).first()
                if not part:
                    raise ValidationError(f"{part_name} is missing for {validated_data["model"]}")
                part.aircraft = aircraft
                updated_parts.append(part)
            AircraftPart.objects.bulk_update(updated_parts, ["aircraft"])
            return aircraft