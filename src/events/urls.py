from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventRegistrationView, EventViewSet

router = DefaultRouter()
router.register(r"", EventViewSet, basename="events")

urlpatterns = [
    # Эндпоинт регистрации на конкретное мероприятие
    path(
        "<uuid:event_id>/register/",
        EventRegistrationView.as_view(),
        name="event-register",
    ),
    # Все остальные маршруты через router (список мероприятий)
    path("", include(router.urls)),
]
