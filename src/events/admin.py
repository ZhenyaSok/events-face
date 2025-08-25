from django.contrib import admin

from django.contrib import admin
from .models import Venue, Event


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "status", "venue")
    list_filter = ("status", "date", "venue")
    search_fields = ("name",)
