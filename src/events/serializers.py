from rest_framework import serializers

from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source="venue.name", read_only=True)

    class Meta:
        model = Event
        fields = ["id", "name", "date", "status", "venue", "venue_name"]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ("id", "event", "status", "created_at", "updated_at")
        read_only_fields = ("status",)
