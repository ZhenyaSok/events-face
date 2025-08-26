from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.response import Response

from .models import Event, Registration
from .pagination import EventCursorPagination
from .serializers import EventSerializer, RegistrationSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    # permission_classes = [permissions.IsAuthenticated]  # TODO защита JWT
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["name"]  # фильтрация по названию
    search_fields = ["name"]  # поиск по названию
    ordering_fields = ["date"]  # сортировка по дате
    ordering = ["date"]  # сортировка по умолчанию
    pagination_class = EventCursorPagination  # подключаем курсорную пагинацию

    def get_queryset(self):
        """
        Возвращаем только мероприятия со статусом OPEN.
        Используем select_related для площадки, чтобы избежать N+1.
        """
        return (
            Event.objects.filter(status=Event.Status.OPEN).select_related(
                "venue"
            )  # предотвращаем N+1
        )


class EventRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        registration, created = Registration.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={"status": Registration.Status.PENDING},
        )
        if not created:
            return Response({"message": "Already registered"}, status=400)

        # Асинхронная обработка подтверждения
        from events.tasks import process_registration

        process_registration.delay(registration.id)

        return Response(
            {"message": "Registration received, confirmation will arrive shortly"}
        )
