from django.contrib import admin

from .models import Event, Registration, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "status", "venue")
    list_filter = ("status", "date", "venue")
    search_fields = ("name",)
    ordering = ("date",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "created_at", "updated_at")
    list_filter = ("status", "event")
    search_fields = ("user__username", "event__name")
    ordering = ("-created_at",)
